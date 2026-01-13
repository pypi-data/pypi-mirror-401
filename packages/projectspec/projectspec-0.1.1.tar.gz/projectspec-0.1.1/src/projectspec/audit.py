#!/usr/bin/env python3
"""
Spec audit tool for comparing specs between two versions.

Produces a semantic diff of what the project "promises", highlighting:
- Added/removed/modified features
- Status transitions (progressions and regressions)
- Acceptance criteria changes

@implements feature:ci-integration/spec-audit
  - Detects changes to spec files between base and head
  - Reports what changed (added, removed, modified features)
  - Reports status changes (e.g., implemented to planned)
  - Outputs human-readable diff of intent changes

@implements feature:reconciliation/audit-semantics
  - audit.py reads field metadata from KindDefinitions (no hardcoding)
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional

# Import shared functions from core module
from projectspec.core import (
    find_spec_files,
    parse_spec_file,
    load_kind_definitions,
    KindDefinition,
)


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class FieldChange:
    """A change to a specific field within an entity."""
    field: str
    change_type: str  # "added", "removed", "modified"
    old_value: Any = None
    new_value: Any = None
    items_added: list[str] = field(default_factory=list)
    items_removed: list[str] = field(default_factory=list)
    is_regression: bool = False


@dataclass
class EntityChange:
    """A change to an entity (capability, feature, component, etc.)."""
    entity_ref: str
    entity_type: str  # "Capability", "Feature", "Component"
    change_type: str  # "added", "removed", "modified"
    spec_file: str
    severity: str = "info"  # "info", "warning"
    field_changes: list[FieldChange] = field(default_factory=list)


@dataclass
class AuditSummary:
    """Summary statistics for the audit - fully schema-driven."""
    entities_added: int = 0
    entities_removed: int = 0
    entities_modified: int = 0
    # Generic counts by kind (e.g., {"Feature": 2, "Capability": 1})
    added_by_kind: dict = field(default_factory=dict)
    removed_by_kind: dict = field(default_factory=dict)
    modified_by_kind: dict = field(default_factory=dict)
    # Ordinal field regressions (any field with progression semantics)
    ordinal_regressions: int = 0
    # Requirements field changes (any field marked as requirementsField)
    requirements_added: int = 0
    requirements_removed: int = 0


@dataclass
class AuditResult:
    """Complete result of a spec audit."""
    base_path: str
    head_path: str
    changes: list[EntityChange] = field(default_factory=list)
    summary: AuditSummary = field(default_factory=AuditSummary)


# =============================================================================
# Ordinal Regression Detection (Schema-Driven)
# =============================================================================

def get_ordinal_config(
    kind_def: Optional[KindDefinition],
    field_path: str,
) -> Optional[dict]:
    """
    Get ordinal configuration for a field from KindDefinition.

    Returns dict with 'progression' and 'terminal' arrays, or None if not found.

    @implements feature:reconciliation/audit-semantics
      - Ordinal fields declare progression order for regression detection
    """
    if not kind_def or not kind_def.audit:
        return None

    for ordinal in kind_def.audit.ordinals:
        if ordinal.field == field_path:
            return {
                "field": ordinal.field,
                "progression": ordinal.progression,
                "terminal": ordinal.terminal,
            }
    return None


def is_ordinal_regression(
    ordinal_config: dict,
    old_value: str,
    new_value: str,
) -> bool:
    """
    Check if a value change is a regression based on ordinal configuration.

    A regression occurs when moving backward in the progression order,
    unless the new value is a terminal state.

    @implements feature:reconciliation/audit-semantics
      - Ordinal fields declare progression order for regression detection
    """
    progression = ordinal_config.get("progression", [])
    terminal = ordinal_config.get("terminal", [])

    # Moving to terminal state is not a regression
    if new_value in terminal:
        return False

    # Check if moving backward in progression
    if old_value in progression and new_value in progression:
        old_idx = progression.index(old_value)
        new_idx = progression.index(new_value)
        return new_idx < old_idx

    return False


def get_requirements_field(kind_def: Optional[KindDefinition]) -> Optional[str]:
    """
    Get the requirements field path from KindDefinition.

    Reads from verification.coverage.requirementsField.

    @implements feature:reconciliation/audit-semantics
      - Requirements removal derived from verification.coverage.requirementsField
    """
    if not kind_def or not kind_def.verification:
        return None

    coverage = kind_def.verification.coverage
    if not coverage or not coverage.requirementsField:
        return None

    req_field = coverage.requirementsField
    # Strip [] suffix if present (e.g., "spec.acceptance[]" -> "spec.acceptance")
    return req_field.rstrip("[]")


def get_relationship_fields(kind_def: Optional[KindDefinition]) -> list[str]:
    """
    Get relationship field paths from KindDefinition.

    @implements feature:reconciliation/audit-semantics
      - Relationship removal derived from relationships section
    """
    if not kind_def:
        return []

    fields = []
    for rel in kind_def.relationships:
        field = rel.field
        # Strip [] suffix if present
        fields.append(field.rstrip("[]"))
    return fields


# =============================================================================
# Spec Loading and Indexing (delegates to speccore)
# =============================================================================

def load_and_index_specs(
    spec_dir: Path,
) -> tuple[dict[str, "IndexedEntity"], dict[str, KindDefinition]]:
    """
    Load all specs from a directory and build an entity index.

    Delegates to speccore for centralized loading and validation.
    KindDefinitions are required - speccore raises ValueError if missing.

    Returns tuple of:
      - dict mapping entity_ref -> IndexedEntity
      - dict mapping kind_name -> KindDefinition

    @implements feature:kind-system/audit-schema-driven
      - Audit tool uses speccore for entity indexing
    """
    from projectspec.core import index_entities, IndexedEntity

    # Load KindDefinitions
    kinds_dir = spec_dir / "kinds"
    kind_definitions = load_kind_definitions(str(kinds_dir)) if kinds_dir.exists() else {}

    spec_files = find_spec_files(str(spec_dir), exclude_dirs=["kinds"])

    # Build combined index using speccore
    combined_index: dict[str, IndexedEntity] = {}

    for spec_file in spec_files:
        try:
            docs = parse_spec_file(spec_file, resolve_subs=True)
        except Exception as e:
            print(f"Warning: Failed to parse {spec_file}: {e}", file=sys.stderr)
            continue

        # Use relative path for cleaner output
        try:
            rel_path = str(spec_file.relative_to(spec_dir.parent))
        except ValueError:
            rel_path = str(spec_file)

        # Use speccore's index_entities (enforces KindDefinition requirement)
        file_index = index_entities(docs, kind_definitions, rel_path)
        combined_index.update(file_index)

    return combined_index, kind_definitions


# =============================================================================
# Field Comparison
# =============================================================================

def normalize_list(value: Any) -> list[str]:
    """Normalize a value to a list of strings for comparison."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def diff_list_field(old_val: Any, new_val: Any) -> tuple[list[str], list[str]]:
    """
    Compare two list values and return (items_added, items_removed).
    """
    old_set = set(normalize_list(old_val))
    new_set = set(normalize_list(new_val))

    items_added = list(new_set - old_set)
    items_removed = list(old_set - new_set)

    return items_added, items_removed


def get_compare_fields_from_schema(
    kind_def: Optional[KindDefinition],
    entity_type: str = "",
) -> tuple[list[str], set[str]]:
    """
    Extract which fields to compare and which are lists from KindDefinition schema.

    Returns (compare_fields, list_fields) tuple.

    KindDefinition is required - speccore enforces this during entity indexing.

    @implements feature:reconciliation/audit-semantics
      - audit.py reads field metadata from KindDefinitions (no hardcoding)

    @implements feature:kind-system/audit-schema-driven
      - Field comparison driven by KindDefinition schema when available
    """
    if not kind_def or not kind_def.validation or not kind_def.validation.schema:
        # No schema defined - compare no fields
        # (KindDefinition exists but may not have validation.schema)
        return [], set()

    schema = kind_def.validation.schema
    properties = schema.get("properties", {})

    compare_fields = list(properties.keys())
    list_fields = set()

    # Determine which fields are arrays from the schema
    for field_name, field_schema in properties.items():
        if isinstance(field_schema, dict):
            field_type = field_schema.get("type")
            if field_type == "array":
                list_fields.add(field_name)
            # Handle oneOf with array option (like implementedIn)
            elif "oneOf" in field_schema:
                for option in field_schema["oneOf"]:
                    if isinstance(option, dict) and option.get("type") == "array":
                        list_fields.add(field_name)
                        break

    return compare_fields, list_fields


def diff_entity(
    base_data: dict,
    head_data: dict,
    entity_type: str,
    kind_def: Optional[KindDefinition] = None,
) -> list[FieldChange]:
    """
    Compare two entity dicts field by field.

    Returns list of FieldChange objects for modified fields.
    All entities are full documents with kind/metadata/spec structure.

    """
    changes: list[FieldChange] = []

    # All entities are full documents - extract spec field
    base_spec = base_data.get("spec", {})
    head_spec = head_data.get("spec", {})

    # Get fields to compare from schema (or fallback based on entity_type)
    compare_fields, list_fields = get_compare_fields_from_schema(kind_def, entity_type)

    for field_name in compare_fields:
        base_val = base_spec.get(field_name)
        head_val = head_spec.get(field_name)

        # Skip if both are None/empty
        if base_val is None and head_val is None:
            continue
        if base_val == [] and head_val == []:
            continue

        # Check if values are equal
        if base_val == head_val:
            continue

        # Determine change type
        if base_val is None or base_val == []:
            change_type = "added"
        elif head_val is None or head_val == []:
            change_type = "removed"
        else:
            change_type = "modified"

        # Handle list fields specially
        if field_name in list_fields:
            items_added, items_removed = diff_list_field(base_val, head_val)

            # Skip if no actual changes (order changes only)
            if not items_added and not items_removed:
                continue

            fc = FieldChange(
                field=field_name,
                change_type=change_type,
                old_value=base_val,
                new_value=head_val,
                items_added=items_added,
                items_removed=items_removed,
            )
        else:
            # Scalar field
            fc = FieldChange(
                field=field_name,
                change_type=change_type,
                old_value=base_val,
                new_value=head_val,
            )

            # Check for ordinal regression using schema-driven detection
            if change_type == "modified":
                ordinal_config = get_ordinal_config(kind_def, f"spec.{field_name}")
                if ordinal_config:
                    if is_ordinal_regression(ordinal_config, str(base_val), str(head_val)):
                        fc.is_regression = True

        changes.append(fc)

    return changes


def get_entity_type(entity_ref: str) -> str:
    """
    Extract entity type from reference.

    Entity refs are in format `kind:name` where kind is lowercase.
    Returns the kind with first letter capitalized (e.g., "feature" -> "Feature").
    """
    if ":" not in entity_ref:
        return "Entity"
    kind = entity_ref.split(":")[0]
    return kind.capitalize()


# =============================================================================
# Diff Algorithm
# =============================================================================

def diff_specs(
    base_index: dict,  # dict[str, IndexedEntity]
    head_index: dict,  # dict[str, IndexedEntity]
    kind_definitions: dict[str, KindDefinition] = None,
) -> list[EntityChange]:
    """
    Compare two spec indexes and return list of changes.

    Uses kind_definitions to determine which fields to compare based on schema.
    Indexes contain IndexedEntity objects from speccore.
    """
    changes: list[EntityChange] = []
    kind_definitions = kind_definitions or {}

    base_refs = set(base_index.keys())
    head_refs = set(head_index.keys())

    # Added entities (in head but not in base)
    for ref in sorted(head_refs - base_refs):
        entity = head_index[ref]
        entity_type = get_entity_type(ref)

        changes.append(EntityChange(
            entity_ref=ref,
            entity_type=entity_type,
            change_type="added",
            spec_file=entity.spec_file,
            severity="info",
        ))

    # Removed entities (in base but not in head)
    for ref in sorted(base_refs - head_refs):
        entity = base_index[ref]
        entity_type = get_entity_type(ref)

        changes.append(EntityChange(
            entity_ref=ref,
            entity_type=entity_type,
            change_type="removed",
            spec_file=entity.spec_file,
            severity="warning",  # Removing entities is a warning
        ))

    # Potentially modified entities (in both)
    for ref in sorted(base_refs & head_refs):
        base_entity = base_index[ref]
        head_entity = head_index[ref]
        entity_type = get_entity_type(ref)

        # Get KindDefinition for this entity type (from the entity or lookup)
        kind_def = head_entity.kind_def or kind_definitions.get(entity_type)

        # Compare fields using schema-driven comparison
        field_changes = diff_entity(base_entity.doc, head_entity.doc, entity_type, kind_def)

        if field_changes:
            # Determine severity based on field changes
            severity = "info"

            # Get requirements field from schema (e.g., "spec.acceptance" -> "acceptance")
            req_field_path = get_requirements_field(kind_def)
            req_field_name = req_field_path.split(".")[-1] if req_field_path else None

            for fc in field_changes:
                if fc.is_regression:
                    severity = "warning"
                    break
                # Check if items were removed from the requirements field
                if req_field_name and fc.field == req_field_name and fc.items_removed:
                    severity = "warning"
                    break

            changes.append(EntityChange(
                entity_ref=ref,
                entity_type=entity_type,
                change_type="modified",
                spec_file=head_entity.spec_file,
                severity=severity,
                field_changes=field_changes,
            ))

    return changes


# =============================================================================
# Summary Computation
# =============================================================================

def compute_summary(changes: list[EntityChange]) -> AuditSummary:
    """
    Compute summary statistics from changes.

    All counts are schema-driven - no hardcoded kind or field names.
    """
    summary = AuditSummary()

    for change in changes:
        kind = change.entity_type

        if change.change_type == "added":
            summary.entities_added += 1
            summary.added_by_kind[kind] = summary.added_by_kind.get(kind, 0) + 1

        elif change.change_type == "removed":
            summary.entities_removed += 1
            summary.removed_by_kind[kind] = summary.removed_by_kind.get(kind, 0) + 1

        elif change.change_type == "modified":
            summary.entities_modified += 1
            summary.modified_by_kind[kind] = summary.modified_by_kind.get(kind, 0) + 1

            for fc in change.field_changes:
                # Count regressions on any ordinal field (schema-driven)
                if fc.is_regression:
                    summary.ordinal_regressions += 1

                # Count array item changes
                summary.requirements_added += len(fc.items_added)
                summary.requirements_removed += len(fc.items_removed)

    return summary


# =============================================================================
# Audit Execution
# =============================================================================

def audit_specs(base_path: str, head_path: str) -> AuditResult:
    """
    Run spec audit comparing base and head directories.
    """
    base_dir = Path(base_path)
    head_dir = Path(head_path)

    # Load and index both versions (includes KindDefinitions)
    base_index, base_kinds = load_and_index_specs(base_dir)
    head_index, head_kinds = load_and_index_specs(head_dir)

    # Use head's KindDefinitions for schema-driven comparison
    # (comparing base against head schema is the right approach)
    kind_definitions = head_kinds

    # Compute diff using schema-driven comparison
    changes = diff_specs(base_index, head_index, kind_definitions)

    # Compute summary
    summary = compute_summary(changes)

    return AuditResult(
        base_path=base_path,
        head_path=head_path,
        changes=changes,
        summary=summary,
    )


# =============================================================================
# Text Formatting
# =============================================================================

def format_text_audit(result: AuditResult) -> str:
    """
    Format audit result as human-readable text.
    """
    lines: list[str] = []

    # Header
    lines.append(f"Spec Audit: {result.base_path} -> {result.head_path}")
    lines.append("")

    # Summary
    s = result.summary
    lines.append("Summary:")

    if s.entities_added:
        lines.append(f"  {s.entities_added} entities added")
        # Show breakdown by kind
        for kind, count in sorted(s.added_by_kind.items()):
            lines.append(f"    {count} {kind}")
    if s.entities_removed:
        lines.append(f"  {s.entities_removed} entities removed")
        # Show breakdown by kind
        for kind, count in sorted(s.removed_by_kind.items()):
            lines.append(f"    {count} {kind}")
    if s.entities_modified:
        lines.append(f"  {s.entities_modified} entities modified")
    if s.ordinal_regressions:
        lines.append(f"  {s.ordinal_regressions} regressions")
    if s.requirements_added or s.requirements_removed:
        lines.append(f"  {s.requirements_added} items added, {s.requirements_removed} removed")

    if not result.changes:
        lines.append("  No changes detected")

    lines.append("")

    if not result.changes:
        return "\n".join(lines)

    # Separator
    lines.append("-" * 60)
    lines.append("")

    # Group changes by spec file for readability
    changes_by_file: dict[str, list[EntityChange]] = {}
    for change in result.changes:
        if change.spec_file not in changes_by_file:
            changes_by_file[change.spec_file] = []
        changes_by_file[change.spec_file].append(change)

    for spec_file in sorted(changes_by_file.keys()):
        file_changes = changes_by_file[spec_file]
        lines.append(f"{spec_file}:")
        lines.append("")

        for change in file_changes:
            # Entity header
            severity_marker = " [REGRESSION]" if change.severity == "warning" else ""
            lines.append(f"  {change.entity_ref} [{change.change_type}]{severity_marker}")

            if change.change_type == "added":
                # Show key fields for added entities
                entity_data = None
                # We don't have the data here, just mark as added
                pass

            elif change.change_type == "removed":
                # Just note removal
                pass

            elif change.change_type == "modified":
                for fc in change.field_changes:
                    if fc.field == "status":
                        regression_mark = " [REGRESSION]" if fc.is_regression else ""
                        lines.append(f"    ~ {fc.field}: {fc.old_value} -> {fc.new_value}{regression_mark}")

                    elif fc.items_added or fc.items_removed:
                        # List field with changes
                        for item in fc.items_removed:
                            lines.append(f"    - {fc.field}: {item}")
                        for item in fc.items_added:
                            lines.append(f"    + {fc.field}: {item}")

                    else:
                        # Scalar field change
                        lines.append(f"    ~ {fc.field}: {fc.old_value} -> {fc.new_value}")

            lines.append("")

    return "\n".join(lines)


# =============================================================================
# JSON Formatting
# =============================================================================

def format_json_audit(result: AuditResult) -> str:
    """
    Format audit result as JSON.
    """
    output = {
        "version": "1",
        "base_path": result.base_path,
        "head_path": result.head_path,
        "summary": asdict(result.summary),
        "changes": [
            {
                "entity_ref": c.entity_ref,
                "entity_type": c.entity_type,
                "change_type": c.change_type,
                "spec_file": c.spec_file,
                "severity": c.severity,
                "field_changes": [
                    {
                        "field": fc.field,
                        "change_type": fc.change_type,
                        "old_value": fc.old_value,
                        "new_value": fc.new_value,
                        "items_added": fc.items_added,
                        "items_removed": fc.items_removed,
                        "is_regression": fc.is_regression,
                    }
                    for fc in c.field_changes
                ],
            }
            for c in result.changes
        ],
    }

    return json.dumps(output, indent=2)


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI entry point for spec audit."""
    parser = argparse.ArgumentParser(
        description="Audit spec changes between two versions"
    )
    parser.add_argument(
        "--base",
        required=True,
        help="Path to base spec directory",
    )
    parser.add_argument(
        "--head",
        required=True,
        help="Path to head spec directory",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit code 1 if warnings (regressions) detected",
    )

    args = parser.parse_args()

    # Validate paths
    base_path = Path(args.base)
    head_path = Path(args.head)

    if not base_path.exists():
        print(f"Error: Base path does not exist: {args.base}", file=sys.stderr)
        sys.exit(1)

    if not head_path.exists():
        print(f"Error: Head path does not exist: {args.head}", file=sys.stderr)
        sys.exit(1)

    # Run audit
    result = audit_specs(args.base, args.head)

    # Output
    if args.format == "json":
        print(format_json_audit(result))
    else:
        print(format_text_audit(result))

    # Exit code
    if args.fail_on_warning:
        has_warnings = any(c.severity == "warning" for c in result.changes)
        if has_warnings:
            sys.exit(1)


if __name__ == "__main__":
    main()
