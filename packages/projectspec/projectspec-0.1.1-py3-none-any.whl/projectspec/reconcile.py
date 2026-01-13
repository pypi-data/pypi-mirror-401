#!/usr/bin/env python3
"""
Reconciliation script for project specs.

Compares spec declarations against actual files to surface gaps.
Schema-driven: reads KindDefinitions to understand how to reconcile each kind.

@implements feature:reconciliation/schema-driven
  - Reads KindDefinitions from spec/kinds/
  - Supports any user-defined kind, not just Capability
  - Applies reconciliation rules from KindDefinition specs
  - Validates specs against JSON Schema from KindDefinition
"""

import argparse
import ast
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml

# Import shared types and functions from core module
from projectspec.core import (
    EntityRef,
    WhenCondition,
    ReferenceCheck,
    EvidenceDefinition,
    CoverageConfig,
    RelationshipDefinition,
    VerificationConfig,
    ValidationConfig,
    KindDefinition,
    Relationship,
    RelationshipGraphResult,
    Issue,
    IndexedEntity,
    find_spec_files,
    parse_spec_file,
    resolve_substitutions,
    load_kind_definitions,
    index_entities,
    get_field_value,
    evaluate_condition,
    extract_field_values,
    check_path_exists,
    verify_entity_references,
    validate_entity_schema,
    build_relationship_graph,
    ProjectConfig,
    load_config,
    get_kinds_dir,
    # Coverage extraction
    get_evidence_definition,
    get_requirements_field,
    extract_requirements,
    extract_evidence_sources,
    should_check_coverage,
    # Adapter registry
    MarkerMatch,
    MarkerAdapter,
    AdapterRegistry,
    get_adapter_registry,
    get_adapter,
)


# =============================================================================
# Reconcile-Specific Data Classes
# =============================================================================

@dataclass
class FeatureResult:
    """Result for a single feature/entity."""
    kind: str
    name: str
    parent: Optional[str]
    status: str  # ok, error, warning, planned
    spec_file: str
    issues: list[Issue] = field(default_factory=list)


@dataclass
class ReconcileResult:
    """Results of reconciliation."""
    issues: list[Issue] = field(default_factory=list)
    features: list[FeatureResult] = field(default_factory=list)
    ok_count: int = 0
    planned_count: int = 0
    unlinked_files: list[str] = field(default_factory=list)
    # Evidence coverage results keyed by evidence name (e.g., "tested", "implemented")
    evidence_results: dict[str, "EvidenceCoverageResult"] = field(default_factory=dict)
    relationship_graph: Optional[RelationshipGraphResult] = None

    @property
    def has_errors(self) -> bool:
        return any(i.severity == "error" for i in self.issues)

    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.severity == "error"])

    @property
    def warning_count(self) -> int:
        return len([i for i in self.issues if i.severity == "warning"])

    @property
    def total_uncovered(self) -> int:
        """Total uncovered criteria across all evidence types."""
        return sum(len(r.uncovered) for r in self.evidence_results.values())

    @property
    def total_orphans(self) -> int:
        """Total orphan claims across all evidence types."""
        return sum(len(r.orphans) for r in self.evidence_results.values())


# =============================================================================
# Requirements Extraction and Normalization
# =============================================================================

def extract_requirements_for_evidence(
    entities: dict[str, IndexedEntity],
    evidence_name: str,
) -> dict[str, list[str]]:
    """
    Extract requirements from indexed entities for a specific evidence type.

    Uses KindDefinition's coverage config to:
    - Determine which field contains requirements (coverage.requirementsField)
    - Check evidence-level conditions (evidence.when)

    Returns dict mapping entity_ref -> list of criterion texts.

    Args:
        entities: Dict of indexed entities
        evidence_name: Name of evidence type (e.g., "tested", "implemented", "documented")

    @implements feature:kind-system/verification-coverage
      - Coverage defined in verification.coverage block
      - Requirements field path configurable
    """
    criteria: dict[str, list[str]] = {}

    for ref_str, entity in entities.items():
        # Check if coverage verification should run for this evidence type
        if not should_check_coverage(entity, evidence_name):
            continue

        # Extract requirements using KindDefinition config
        requirements = extract_requirements(entity)
        if not requirements:
            continue

        criteria[ref_str] = [
            normalize_criterion(c) for c in requirements
        ]

    return criteria


def normalize_criterion(text: str) -> str:
    """Normalize criterion text for comparison."""
    # Strip whitespace, normalize internal whitespace
    return " ".join(text.split())


# =============================================================================
# Evidence Path Extraction
# =============================================================================

def extract_evidence_paths(
    entities: dict[str, IndexedEntity],
    evidence_name: str,
) -> list[str]:
    """
    Extract file paths for a specific evidence type from indexed entities.

    Uses KindDefinition's coverage config to:
    - Determine which field contains source paths (evidence.sourcesField)
    - Check evidence-level conditions (evidence.when)

    @implements feature:kind-system/verification-coverage
      - Evidence types with marker and adapter
    """
    paths = []

    for ref_str, entity in entities.items():
        # Use speccore's extract_evidence_sources which handles conditions
        entity_paths = extract_evidence_sources(entity, evidence_name)
        paths.extend(entity_paths)

    return paths


# =============================================================================
# Unlinked File Detection
# =============================================================================

def find_all_source_files(repo_root: str, source_dirs: list[str]) -> set[str]:
    """
    Find all source files in the repo.

    @implements feature:reconciliation/detect-unlinked-files
      - Scans source directories for all files
      - Identifies files not referenced by any spec
    """
    files = set()

    for source_dir in source_dirs:
        dir_path = os.path.join(repo_root, source_dir)
        if not os.path.exists(dir_path):
            continue

        for root, _, filenames in os.walk(dir_path):
            for filename in filenames:
                # Skip hidden files and common non-source files
                if filename.startswith("."):
                    continue
                if filename.endswith((".pyc", ".pyo", ".class")):
                    continue

                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, repo_root)
                files.add(rel_path)

    return files


def collect_referenced_paths(entities: dict[str, IndexedEntity]) -> set[str]:
    """Collect all file paths referenced by entities."""
    paths = set()

    for ref_str, entity in entities.items():
        spec = entity.doc.get("spec", {})

        # Collect from common path fields
        for field in ["implementedIn", "testedIn", "documentedIn"]:
            value = spec.get(field, [])
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        paths.add(item)
            elif isinstance(value, str) and value != "disabled":
                paths.add(value)

    return paths


# =============================================================================
# Adapter-Based Marker Collection
# =============================================================================

@dataclass
class EvidenceMarker:
    """A marker found by an adapter, converted to common format."""
    file_path: str
    location: str
    line: int
    entity_ref: str
    criteria: list[str]


def collect_markers_with_adapter(
    source_paths: list[str],
    adapter_name: str,
    marker: str,
    repo_root: str,
) -> dict[str, list[EvidenceMarker]]:
    """
    Collect markers from files using a specific adapter.

    Args:
        source_paths: List of file paths to scan
        adapter_name: Name of the adapter to use (e.g., "python-test-docstring")
        marker: The marker to look for (e.g., "@tests")
        repo_root: Repository root for resolving paths

    Returns:
        Dict mapping entity_ref -> list of EvidenceMarker

    @implements feature:kind-system/verification-coverage
      - Evidence types with marker and adapter
    """
    adapter = get_adapter(adapter_name)
    if not adapter:
        print(f"Warning: Unknown adapter '{adapter_name}'", file=sys.stderr)
        return {}

    markers: dict[str, list[EvidenceMarker]] = {}

    for path_str in source_paths:
        file_path = Path(repo_root) / path_str
        if not file_path.exists():
            continue

        # Extract markers using the adapter
        matches = adapter.extract_markers(file_path, marker)

        for match in matches:
            evidence_marker = EvidenceMarker(
                file_path=match.file_path,
                location=match.location,
                line=match.line,
                entity_ref=match.entity_ref,
                criteria=match.criteria,
            )

            if match.entity_ref not in markers:
                markers[match.entity_ref] = []
            markers[match.entity_ref].append(evidence_marker)

    return markers


def collect_all_evidence_markers(
    entities: dict[str, IndexedEntity],
    evidence_name: str,
    repo_root: str,
) -> dict[str, list[EvidenceMarker]]:
    """
    Collect all markers for an evidence type across all entities.

    Uses the evidence definition from KindDefinitions to determine:
    - Which adapter to use
    - Which marker to look for
    - Which files to scan

    Args:
        entities: Dict of indexed entities
        evidence_name: Name of evidence type (e.g., "tested", "implemented")
        repo_root: Repository root for resolving paths

    Returns:
        Dict mapping entity_ref -> list of EvidenceMarker
    """
    all_markers: dict[str, list[EvidenceMarker]] = {}

    # Group entities by their evidence configuration
    # (adapter + marker combination)
    evidence_configs: dict[tuple[str, str], list[str]] = {}

    for ref_str, entity in entities.items():
        evidence = get_evidence_definition(entity.kind_def, evidence_name)
        if not evidence:
            continue

        # Check evidence condition
        if evidence.when and not evaluate_condition(evidence.when, entity.doc):
            continue

        # Get source paths for this entity
        source_paths = extract_evidence_sources(entity, evidence_name)
        if not source_paths:
            continue

        config_key = (evidence.adapter, evidence.marker)
        if config_key not in evidence_configs:
            evidence_configs[config_key] = []
        evidence_configs[config_key].extend(source_paths)

    # Collect markers for each unique configuration
    for (adapter_name, marker), paths in evidence_configs.items():
        # Deduplicate paths
        unique_paths = list(set(paths))
        markers = collect_markers_with_adapter(unique_paths, adapter_name, marker, repo_root)

        # Merge into all_markers
        for entity_ref, marker_list in markers.items():
            if entity_ref not in all_markers:
                all_markers[entity_ref] = []
            all_markers[entity_ref].extend(marker_list)

    return all_markers


def collect_evidence_types(kind_definitions: dict[str, KindDefinition]) -> list[str]:
    """
    Collect all unique evidence type names from KindDefinitions.

    Returns list of evidence names (e.g., ["tested", "implemented", "documented"]).
    """
    evidence_types: set[str] = set()

    for kind_def in kind_definitions.values():
        if not kind_def.verification or not kind_def.verification.coverage:
            continue

        for evidence in kind_def.verification.coverage.evidence:
            evidence_types.add(evidence.name)

    return sorted(evidence_types)


def get_marker_for_evidence(kind_definitions: dict[str, KindDefinition], evidence_name: str) -> str:
    """
    Get the marker string for an evidence type from KindDefinitions.

    Returns the marker (e.g., "@implements") for the given evidence name.
    """
    for kind_def in kind_definitions.values():
        if not kind_def.verification or not kind_def.verification.coverage:
            continue

        for evidence in kind_def.verification.coverage.evidence:
            if evidence.name == evidence_name:
                return evidence.marker

    return evidence_name  # Fallback to evidence name if no marker found


@dataclass
class EvidenceCoverageResult:
    """Results of evidence coverage verification."""
    evidence_name: str
    marker: str  # The marker used (e.g., "@implements") for aggregation
    covered: list[tuple[str, str, str, str]]  # (entity_ref, criterion, file_path, location)
    uncovered: list[tuple[str, str]]  # (entity_ref, criterion)
    orphans: list[tuple[str, str, str, str]]  # (file_path, location, entity_ref, criterion)


def verify_evidence_coverage(
    spec_requirements: dict[str, list[str]],
    evidence_markers: dict[str, list[EvidenceMarker]],
    evidence_name: str,
    marker: str,
) -> EvidenceCoverageResult:
    """
    Verify that requirements are covered by evidence markers.

    This is the generic version that works with any evidence type and
    uses the adapter-based marker collection.

    Args:
        spec_requirements: Dict mapping entity_ref -> list of requirement texts
        evidence_markers: Dict mapping entity_ref -> list of EvidenceMarker
        evidence_name: Name of evidence type for the result
        marker: The marker string (e.g., "@implements") for aggregation

    Returns:
        EvidenceCoverageResult with covered, uncovered, and orphan info

    @implements feature:reconciliation/criteria-verification
      - Criteria listed under markers are matched against spec acceptance criteria
      - Reports unverified acceptance criteria as warnings
      - Reports criteria in markers that don't match spec as orphan errors
    """
    result = EvidenceCoverageResult(
        evidence_name=evidence_name,
        marker=marker,
        covered=[],
        uncovered=[],
        orphans=[],
    )

    # Track which requirements have been covered
    covered_requirements: dict[str, set[str]] = {}

    # Process evidence markers
    for entity_ref, markers in evidence_markers.items():
        for marker in markers:
            for claimed_requirement in marker.criteria:
                normalized_claim = normalize_criterion(claimed_requirement)

                # Check if this entity exists in specs
                if entity_ref not in spec_requirements:
                    # Orphan claim - entity doesn't exist
                    result.orphans.append((
                        marker.file_path,
                        marker.location,
                        entity_ref,
                        claimed_requirement,
                    ))
                    continue

                # Check if requirement matches any spec requirement
                requirement_list = spec_requirements[entity_ref]
                matched = False
                for requirement in requirement_list:
                    if normalize_criterion(requirement) == normalized_claim:
                        matched = True
                        # Record as covered
                        if entity_ref not in covered_requirements:
                            covered_requirements[entity_ref] = set()
                        covered_requirements[entity_ref].add(requirement)

                        result.covered.append((
                            entity_ref,
                            requirement,
                            marker.file_path,
                            marker.location,
                        ))
                        break

                if not matched:
                    # Orphan claim - requirement doesn't match
                    result.orphans.append((
                        marker.file_path,
                        marker.location,
                        entity_ref,
                        claimed_requirement,
                    ))

    # Find uncovered requirements
    for entity_ref, requirement_list in spec_requirements.items():
        covered_set = covered_requirements.get(entity_ref, set())
        for requirement in requirement_list:
            if requirement not in covered_set:
                result.uncovered.append((entity_ref, requirement))

    return result


# =============================================================================
# Main Reconciliation
# =============================================================================

def reconcile_entity(
    entity: IndexedEntity,
    repo_root: str,
    entity_index: dict[str, IndexedEntity],
) -> tuple[list[Issue], FeatureResult]:
    """
    Reconcile a single entity using speccore's verification.

    Returns (issues, feature_result).

    @implements feature:reconciliation/check-implemented-in
      - Checks that paths in implementedIn field exist
      - Supports file paths
      - Supports glob patterns
      - Reports missing files as errors

    @implements feature:reconciliation/check-tested-in
      - Checks that paths in testedIn field exist
      - Reports missing test files as errors

    @implements feature:reconciliation/check-documented-in
      - Checks that paths in documentedIn field exist
      - Reports missing docs as warnings (not errors)

    @implements feature:reconciliation/status-aware
      - Skips verification for features with status planned
      - Reports planned features in summary

    @implements feature:kind-system/uniform-entity-handling
      - All entities use standard envelope (kind, metadata, spec)
      - Features are top-level entities with their own KindDefinition
      - No special-case handling for any specific kind
    """
    issues = []
    kind_def = entity.kind_def
    entity_name = entity.doc.get("metadata", {}).get("name", "unknown")

    # Parse parent from name if present
    parent = None
    if "/" in entity_name:
        parent, _ = entity_name.rsplit("/", 1)

    kind = entity.doc.get("kind", "Unknown")

    # Check entity-level condition - if not met, entity is "planned"
    if kind_def and kind_def.verification and kind_def.verification.when:
        if not evaluate_condition(kind_def.verification.when, entity.doc):
            return [], FeatureResult(
                kind=kind,
                name=entity_name,
                parent=parent,
                status="planned",
                spec_file=entity.spec_file,
            )

    # Validate schema
    schema_issues = validate_entity_schema(entity)
    issues.extend(schema_issues)

    # Verify references
    ref_issues = verify_entity_references(entity, repo_root, entity_index)
    issues.extend(ref_issues)

    # Determine status
    has_errors = any(i.severity == "error" for i in issues)
    has_warnings = any(i.severity == "warning" for i in issues)

    if has_errors:
        status = "error"
    elif has_warnings:
        status = "warning"
    else:
        status = "ok"

    return issues, FeatureResult(
        kind=kind,
        name=entity_name,
        parent=parent,
        status=status,
        spec_file=entity.spec_file,
        issues=issues,
    )


def reconcile(
    spec_dir: str,
    repo_root: str,
    source_dirs: list[str],
    kinds_dir: Optional[str] = None,
    check_unlinked: bool = True,
    verify_criteria: bool = True,
    test_dirs: Optional[list[str]] = None,
    build_graph: bool = True,
) -> ReconcileResult:
    """
    Run reconciliation across all specs.

    @implements feature:reconciliation/parse-specs
      - Reports parse errors clearly

    @implements feature:reconciliation/tooling-config
      - Reads optional projectspec.yaml from repo root
      - Supports kinds field to override KindDefinitions location
      - Supports ignore field to exclude directories from scanning
      - Uses convention (spec/kinds/) when no config present
    """
    result = ReconcileResult()

    # Load tooling config from repo root
    config = load_config(repo_root)

    if kinds_dir is None:
        kinds_dir = get_kinds_dir(config, spec_dir)

    # Load KindDefinitions using speccore
    kind_definitions = load_kind_definitions(kinds_dir)

    if not kind_definitions:
        print(f"No KindDefinitions found in {kinds_dir}", file=sys.stderr)
        print("Ensure spec/kinds/ contains KindDefinition files or set kinds in projectspec.yaml", file=sys.stderr)
        return result

    # Build global entity index
    all_entities: dict[str, IndexedEntity] = {}

    # Find spec files, excluding the kinds directory and ignored paths
    exclude_dirs = ["kinds"] + config.ignore
    spec_files = find_spec_files(spec_dir, exclude_dirs=exclude_dirs)

    if not spec_files:
        print(f"No spec files found in {spec_dir}", file=sys.stderr)
        return result

    for spec_file in spec_files:
        try:
            docs = parse_spec_file(spec_file)
        except yaml.YAMLError as e:
            result.issues.append(Issue(
                severity="error",
                spec_file=str(spec_file),
                entity="",
                issue_type="parse_error",
                message=f"Failed to parse YAML: {e}",
            ))
            continue
        except Exception as e:
            result.issues.append(Issue(
                severity="error",
                spec_file=str(spec_file),
                entity="",
                issue_type="parse_error",
                message=f"Failed to parse file: {e}",
            ))
            continue

        # Index entities from this file
        try:
            rel_path = str(spec_file.relative_to(repo_root))
        except ValueError:
            rel_path = str(spec_file)

        file_entities = index_entities(docs, kind_definitions, rel_path)

        # Check for unknown kinds
        for doc in docs:
            kind = doc.get("kind", "")
            if kind and kind != "KindDefinition" and kind not in kind_definitions:
                result.issues.append(Issue(
                    severity="error",
                    spec_file=rel_path,
                    entity=doc.get("metadata", {}).get("name", "unknown"),
                    issue_type="unknown_kind",
                    message=f"No KindDefinition found for kind '{kind}'",
                ))

        all_entities.update(file_entities)

    # Reconcile each entity
    for ref_str, entity in all_entities.items():
        issues, feature_result = reconcile_entity(entity, repo_root, all_entities)
        result.issues.extend(issues)
        result.features.append(feature_result)

        if feature_result.status == "ok":
            result.ok_count += 1
        elif feature_result.status == "planned":
            result.planned_count += 1

    # Check for unlinked files
    if check_unlinked and source_dirs:
        all_files = find_all_source_files(repo_root, source_dirs)
        referenced_paths = collect_referenced_paths(all_entities)
        unlinked = all_files - referenced_paths
        result.unlinked_files = sorted(unlinked)

    # Criteria verification using adapter-based marker collection
    # Discovers all evidence types from KindDefinitions and verifies each
    if verify_criteria:
        # Discover all unique evidence types across all KindDefinitions
        evidence_types = collect_evidence_types(kind_definitions)

        # Verify coverage for each evidence type
        for evidence_name in evidence_types:
            # Extract requirements for entities with this evidence configured
            requirements = extract_requirements_for_evidence(all_entities, evidence_name)

            # Collect markers using adapters
            markers = collect_all_evidence_markers(all_entities, evidence_name, repo_root)

            # Get the marker string for this evidence type
            marker = get_marker_for_evidence(kind_definitions, evidence_name)

            # Verify coverage
            coverage = verify_evidence_coverage(requirements, markers, evidence_name, marker)

            # Store in result
            result.evidence_results[evidence_name] = coverage

    # Build relationship graph using speccore
    if build_graph and all_entities:
        result.relationship_graph = build_relationship_graph(all_entities)

        # Add issues for broken references
        for source, target, rel_type in result.relationship_graph.broken_refs:
            result.issues.append(Issue(
                severity="error",
                spec_file="",
                entity=str(source),
                issue_type="broken_reference",
                message=f"Broken {rel_type} reference to '{target}' - entity does not exist",
                path=None,
            ))

        # Add issues for cycles
        for cycle in result.relationship_graph.cycles:
            cycle_str = " -> ".join(str(e) for e in cycle)
            result.issues.append(Issue(
                severity="warning",
                spec_file="",
                entity=str(cycle[0]),
                issue_type="circular_dependency",
                message=f"Circular dependency detected: {cycle_str}",
                path=None,
            ))

    return result


# =============================================================================
# Output Formatting
# =============================================================================

def format_text_result(result: ReconcileResult) -> str:
    """Format reconciliation result as human-readable text."""
    lines = []

    # Summary
    total = result.ok_count + result.error_count
    lines.append(f"Reconciliation complete: {result.ok_count}/{total} features OK")
    if result.planned_count:
        lines.append(f"  ({result.planned_count} planned features skipped)")
    lines.append("")

    # Group issues by spec file
    issues_by_file: dict[str, list[Issue]] = {}
    for issue in result.issues:
        if issue.spec_file not in issues_by_file:
            issues_by_file[issue.spec_file] = []
        issues_by_file[issue.spec_file].append(issue)

    for spec_file, issues in sorted(issues_by_file.items()):
        lines.append(f"{spec_file}:")
        for issue in issues:
            severity_marker = "ERROR" if issue.severity == "error" else "WARN"
            entity_str = f"  {issue.entity}: " if issue.entity else "  "
            lines.append(f"{entity_str}[{severity_marker}] {issue.message}")
            if issue.path:
                lines.append(f"    → {issue.path}")
        lines.append("")

    # Unlinked files
    if result.unlinked_files:
        lines.append("Unlinked files (not referenced in any spec):")
        for f in result.unlinked_files[:20]:
            lines.append(f"  {f}")
        if len(result.unlinked_files) > 20:
            lines.append(f"  ... and {len(result.unlinked_files) - 20} more")
        lines.append("")

    # Evidence coverage - aggregate by marker, not by evidence type
    # Group evidence results by marker (e.g., all @implements evidence types together)
    by_marker: dict[str, list[EvidenceCoverageResult]] = {}
    for coverage in result.evidence_results.values():
        if coverage.marker not in by_marker:
            by_marker[coverage.marker] = []
        by_marker[coverage.marker].append(coverage)

    # For each marker, compute truly uncovered requirements
    # (not covered by ANY adapter for that marker)
    for marker, coverages in sorted(by_marker.items()):
        # Collect all covered (entity_ref, criterion) pairs across all adapters
        all_covered: set[tuple[str, str]] = set()
        for cov in coverages:
            for entity_ref, criterion, _, _ in cov.covered:
                all_covered.add((entity_ref, normalize_criterion(criterion)))

        # Collect all uncovered, then subtract what's covered by other adapters
        truly_uncovered: dict[str, list[str]] = {}
        for cov in coverages:
            for entity_ref, criterion in cov.uncovered:
                normalized = normalize_criterion(criterion)
                if (entity_ref, normalized) not in all_covered:
                    if entity_ref not in truly_uncovered:
                        truly_uncovered[entity_ref] = []
                    if criterion not in truly_uncovered[entity_ref]:
                        truly_uncovered[entity_ref].append(criterion)

        if truly_uncovered:
            lines.append(f"Uncovered requirements (missing {marker} evidence):")
            for entity in sorted(truly_uncovered.keys()):
                lines.append(f"  {entity}:")
                for criterion in truly_uncovered[entity]:
                    lines.append(f"    - {criterion}")
            lines.append("")

    # Orphan claims - aggregate by marker as well
    for marker, coverages in sorted(by_marker.items()):
        all_orphans = []
        for cov in coverages:
            all_orphans.extend(cov.orphans)

        if all_orphans:
            lines.append(f"Orphan {marker} claims (in markers but not in specs):")
            for file_path, location, entity_ref, criterion in all_orphans:
                lines.append(f"  {file_path}::{location}")
                lines.append(f"    Claims: \"{criterion}\"")
                lines.append(f"    Entity: {entity_ref}")
            lines.append("")

    return "\n".join(lines)


def format_json_result(result: ReconcileResult) -> str:
    """
    Format reconciliation result as JSON.

    @implements feature:reconciliation/json-output
      - --format json outputs machine-readable results
      - JSON schema is documented
      - Enables integration with other tools
    """
    output = {
        "version": "1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "ok_count": result.ok_count,
            "error_count": result.error_count,
            "warning_count": result.warning_count,
            "planned_count": result.planned_count,
            "unlinked_count": len(result.unlinked_files),
        },
        "features": [
            {
                "kind": f.kind,
                "name": f.name,
                "parent": f.parent,
                "status": f.status,
                "spec_file": f.spec_file,
                "issues": [asdict(i) for i in f.issues] if f.issues else [],
            }
            for f in result.features
        ],
        "issues": [asdict(i) for i in result.issues],
        "unlinked_files": result.unlinked_files,
    }

    # Add evidence coverage results
    if result.evidence_results:
        output["summary"]["total_covered"] = sum(
            len(r.covered) for r in result.evidence_results.values()
        )
        output["summary"]["total_uncovered"] = result.total_uncovered
        output["summary"]["total_orphans"] = result.total_orphans

        output["evidence"] = {}
        for evidence_name, coverage in result.evidence_results.items():
            output["evidence"][evidence_name] = {
                "covered": [
                    {
                        "entity_ref": entity_ref,
                        "criterion": criterion,
                        "file_path": file_path,
                        "location": location,
                    }
                    for entity_ref, criterion, file_path, location in coverage.covered
                ],
                "uncovered": [
                    {
                        "entity_ref": entity_ref,
                        "criterion": criterion,
                    }
                    for entity_ref, criterion in coverage.uncovered
                ],
                "orphans": [
                    {
                        "file_path": file_path,
                        "location": location,
                        "entity_ref": entity_ref,
                        "criterion": criterion,
                    }
                    for file_path, location, entity_ref, criterion in coverage.orphans
                ],
            }

    # Add relationship graph if present
    if result.relationship_graph:
        graph = result.relationship_graph
        output["summary"]["entity_count"] = len(graph.entities)
        output["summary"]["relationship_count"] = len(graph.relationships)
        output["summary"]["broken_ref_count"] = len(graph.broken_refs)
        output["summary"]["cycle_count"] = len(graph.cycles)

        output["relationship_graph"] = {
            "entities": [
                {
                    "kind": e.kind,
                    "name": e.name,
                    "parent": e.parent,
                    "ref": str(e),
                }
                for e in graph.entities
            ],
            "relationships": [
                {
                    "source": str(r.source),
                    "target": str(r.target),
                    "type": r.rel_type,
                }
                for r in graph.relationships
            ],
            "broken_refs": [
                {
                    "source": str(source),
                    "target": str(target),
                    "type": rel_type,
                }
                for source, target, rel_type in graph.broken_refs
            ],
            "cycles": [
                [str(e) for e in cycle]
                for cycle in graph.cycles
            ],
        }

    return json.dumps(output, indent=2)


# =============================================================================
# CLI
# =============================================================================

def main():
    """
    CLI entry point for reconciliation.

    @implements feature:reconciliation/cli-interface
      - Accepts --spec-dir to specify spec location
      - Accepts --repo-root to specify repository root
      - Accepts --source-dirs to specify directories to scan
      - Accepts --strict for CI mode (exit 1 on any issue)
      - Returns exit code 1 on errors

    @implements feature:reconciliation/detect-unlinked-files
      - Can be disabled with --no-unlinked flag
    """
    parser = argparse.ArgumentParser(
        description="Reconcile project specs against implementation"
    )
    parser.add_argument(
        "--spec-dir",
        default="spec",
        help="Directory containing spec files (default: spec)"
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root directory (default: current directory)"
    )
    parser.add_argument(
        "--source-dirs",
        nargs="+",
        default=["src", "tests", "docs"],
        help="Source directories to scan for unlinked files (default: src tests docs)"
    )
    parser.add_argument(
        "--kinds-dir",
        default=None,
        help="Directory containing KindDefinitions (default: spec/kinds)"
    )
    parser.add_argument(
        "--no-unlinked",
        action="store_true",
        help="Skip checking for unlinked files"
    )
    parser.add_argument(
        "--no-criteria",
        action="store_true",
        help="Skip criteria verification"
    )
    parser.add_argument(
        "--no-graph",
        action="store_true",
        help="Skip relationship graph building"
    )
    parser.add_argument(
        "--test-dirs",
        nargs="+",
        default=None,
        help="Directories to scan for test files (default: from Project spec or 'tests')"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code if any issues found"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    spec_dir = os.path.join(repo_root, args.spec_dir)
    kinds_dir = args.kinds_dir
    if kinds_dir:
        kinds_dir = os.path.join(repo_root, kinds_dir)

    result = reconcile(
        spec_dir=spec_dir,
        repo_root=repo_root,
        source_dirs=args.source_dirs,
        kinds_dir=kinds_dir,
        check_unlinked=not args.no_unlinked,
        verify_criteria=not args.no_criteria,
        test_dirs=args.test_dirs,
        build_graph=not args.no_graph,
    )

    if args.format == "json":
        print(format_json_result(result))
    else:
        print(format_text_result(result))

    if args.strict and (result.has_errors or result.unlinked_files):
        sys.exit(1)
    elif result.has_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
