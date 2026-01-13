#!/usr/bin/env python3
"""
Shared core logic for projectspec tooling.

This module contains types and functions shared between reconcile.py and audit.py,
implementing the five semantic patterns:
1. Validation - Schema conformance
2. References - Path and entity validity
3. Coverage - Requirements satisfaction
4. Relationships - System modeling
5. Conditions - Gating verification

@implements feature:kind-system/shared-core-module
  - Shared types defined in core.py
  - KindDefinition parsing shared between reconcile and audit
  - Entity indexing shared between tools
  - Condition evaluation shared between tools
"""

import glob as glob_module
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml


# =============================================================================
# Entity References
# =============================================================================

@dataclass
class EntityRef:
    """
    A reference to an entity.

    Format: kind:name or kind:parent/name
    """
    kind: str
    name: str
    parent: Optional[str] = None

    @classmethod
    def parse(cls, ref_str: str) -> Optional["EntityRef"]:
        """
        Parse entity reference string.

        Formats:
          - kind:name (top-level entity)
          - kind:parent/name (nested entity)
        """
        if ":" not in ref_str:
            return None

        kind, rest = ref_str.split(":", 1)
        if "/" in rest:
            parent, name = rest.split("/", 1)
            return cls(kind=kind, name=name, parent=parent)
        else:
            return cls(kind=kind, name=rest)

    def __str__(self) -> str:
        if self.parent:
            return f"{self.kind}:{self.parent}/{self.name}"
        return f"{self.kind}:{self.name}"

    def to_ref_string(self) -> str:
        """Return lowercase entity reference string."""
        if self.parent:
            return f"{self.kind.lower()}:{self.parent}/{self.name}"
        return f"{self.kind.lower()}:{self.name}"

    def __eq__(self, other) -> bool:
        """Case-insensitive comparison for kind, case-sensitive for name/parent."""
        if not isinstance(other, EntityRef):
            return False
        return (
            self.kind.lower() == other.kind.lower()
            and self.name == other.name
            and self.parent == other.parent
        )

    def __hash__(self):
        return hash((self.kind.lower(), self.name, self.parent))


# =============================================================================
# Condition Types (Pattern 5: Conditions)
# =============================================================================

@dataclass
class WhenCondition:
    """
    A condition that gates verification.

    Conditions evaluate to true/false based on entity field values.
    Can be combined with all/any for complex conditions.

    @implements feature:kind-system/when-conditions
      - Conditions evaluate field values against operators
      - Supports equals, notEquals, in, notIn, exists operators
      - Supports all/any for combined conditions
    """
    field: Optional[str] = None
    equals: Optional[Any] = None
    notEquals: Optional[Any] = None
    in_: Optional[list[Any]] = None  # 'in' is reserved
    notIn: Optional[list[Any]] = None
    exists: Optional[bool] = None
    all_: Optional[list["WhenCondition"]] = None  # AND
    any_: Optional[list["WhenCondition"]] = None  # OR

    @classmethod
    def from_dict(cls, data: dict) -> "WhenCondition":
        """Parse a condition from a dictionary."""
        all_conditions = None
        any_conditions = None

        if "all" in data:
            all_conditions = [cls.from_dict(c) for c in data["all"]]
        if "any" in data:
            any_conditions = [cls.from_dict(c) for c in data["any"]]

        return cls(
            field=data.get("field"),
            equals=data.get("equals"),
            notEquals=data.get("notEquals"),
            in_=data.get("in"),
            notIn=data.get("notIn"),
            exists=data.get("exists"),
            all_=all_conditions,
            any_=any_conditions,
        )


def get_field_value(entity: dict, field_path: str) -> Any:
    """
    Get a value from an entity using a field path.

    Supports paths like:
      - spec.status
      - spec.implementedIn
      - metadata.labels.priority
    """
    parts = field_path.split(".")
    value = entity

    for part in parts:
        if isinstance(value, dict):
            value = value.get(part)
        else:
            return None

    return value


def evaluate_condition(condition: WhenCondition, entity: dict) -> bool:
    """
    Evaluate a when condition against an entity.

    Returns True if the condition is satisfied, False otherwise.
    """
    # Handle combined conditions
    if condition.all_:
        return all(evaluate_condition(c, entity) for c in condition.all_)

    if condition.any_:
        return any(evaluate_condition(c, entity) for c in condition.any_)

    # Handle simple field conditions
    if condition.field is None:
        return True  # No condition = always true

    value = get_field_value(entity, condition.field)

    # exists check
    if condition.exists is not None:
        if condition.exists:
            return value is not None
        else:
            return value is None

    # equals check
    if condition.equals is not None:
        return value == condition.equals

    # notEquals check
    if condition.notEquals is not None:
        return value != condition.notEquals

    # in check
    if condition.in_ is not None:
        return value in condition.in_

    # notIn check
    if condition.notIn is not None:
        return value not in condition.notIn

    return True  # No specific check = true


# =============================================================================
# Reference Types (Pattern 2: References)
# =============================================================================

@dataclass
class ReferenceCheck:
    """
    A reference integrity check.

    Verifies that referenced paths or entities exist.

    @implements feature:kind-system/verification-references
      - Reference checks defined in verification.references block
      - Supports path and entity-ref types
      - Per-check conditions via when clause
      - Severity configurable per check
    """
    field: str  # Field path, e.g., "spec.implementedIn[]"
    type: str   # "path" or "entity-ref"
    severity: str = "error"
    when: Optional[WhenCondition] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ReferenceCheck":
        when = None
        if "when" in data:
            when = WhenCondition.from_dict(data["when"])

        return cls(
            field=data.get("field", ""),
            type=data.get("type", "path"),
            severity=data.get("severity", "error"),
            when=when,
        )


# =============================================================================
# Coverage Types (Pattern 3: Coverage)
# =============================================================================

@dataclass
class EvidenceDefinition:
    """
    Definition of an evidence type for coverage verification.

    Evidence connects requirements (acceptance criteria) to proof
    in files via markers like @tests, @implements, @documents.
    """
    name: str
    marker: str  # e.g., "@tests"
    adapter: str  # e.g., "python-test-docstring"
    sourcesField: str  # e.g., "spec.testedIn[]"
    when: Optional[WhenCondition] = None

    @classmethod
    def from_dict(cls, data: dict) -> "EvidenceDefinition":
        when = None
        if "when" in data:
            when = WhenCondition.from_dict(data["when"])

        return cls(
            name=data.get("name", ""),
            marker=data.get("marker", ""),
            adapter=data.get("adapter", ""),
            sourcesField=data.get("sourcesField", ""),
            when=when,
        )


@dataclass
class CoverageConfig:
    """
    Configuration for coverage verification.

    Defines where to find requirements and what evidence types
    can satisfy them.

    @implements feature:kind-system/verification-coverage
      - Coverage defined in verification.coverage block
      - Requirements field path configurable
      - Evidence types with marker and adapter
      - Per-evidence conditions via when clause
    """
    requirementsField: str  # e.g., "spec.acceptance[]"
    evidence: list[EvidenceDefinition] = field(default_factory=list)
    when: Optional[WhenCondition] = None

    @classmethod
    def from_dict(cls, data: dict) -> "CoverageConfig":
        when = None
        if "when" in data:
            when = WhenCondition.from_dict(data["when"])

        evidence = [
            EvidenceDefinition.from_dict(e)
            for e in data.get("evidence", [])
        ]

        return cls(
            requirementsField=data.get("requirementsField", ""),
            evidence=evidence,
            when=when,
        )


# =============================================================================
# Relationship Types (Pattern 4: Relationships)
# =============================================================================

@dataclass
class RelationshipDefinition:
    """
    Definition of a structural relationship.

    Relationships model the system structure for analysis
    (cycles, impact, ordering).

    @implements feature:kind-system/relationships-modeling
      - Relationships defined in separate relationships block
      - Relationship types configurable (depends-on, part-of, implements, extends)
      - Separated from verification (modeling vs checking)
    """
    field: str  # Field path, e.g., "spec.depends-on[]"
    type: str   # "depends-on", "part-of", "implements", "extends"

    @classmethod
    def from_dict(cls, data: dict) -> "RelationshipDefinition":
        return cls(
            field=data.get("field", ""),
            type=data.get("type", ""),
        )


@dataclass
class Relationship:
    """A relationship between entities."""
    source: EntityRef
    target: EntityRef
    rel_type: str


@dataclass
class RelationshipGraphResult:
    """Results of relationship graph analysis."""
    entities: list[EntityRef] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    broken_refs: list[tuple[EntityRef, EntityRef, str]] = field(default_factory=list)
    cycles: list[list[EntityRef]] = field(default_factory=list)


# =============================================================================
# Verification Config (Pattern 2 + 3 combined)
# =============================================================================

@dataclass
class VerificationConfig:
    """
    Configuration for all verification (references + coverage).
    """
    when: Optional[WhenCondition] = None
    references: list[ReferenceCheck] = field(default_factory=list)
    coverage: Optional[CoverageConfig] = None

    @classmethod
    def from_dict(cls, data: dict) -> "VerificationConfig":
        when = None
        if "when" in data:
            when = WhenCondition.from_dict(data["when"])

        references = [
            ReferenceCheck.from_dict(r)
            for r in data.get("references", [])
        ]

        coverage = None
        if "coverage" in data:
            coverage = CoverageConfig.from_dict(data["coverage"])

        return cls(
            when=when,
            references=references,
            coverage=coverage,
        )


# =============================================================================
# Validation Config (Pattern 1: Validation)
# =============================================================================

@dataclass
class ValidationConfig:
    """
    Configuration for schema validation.
    """
    schema: Optional[dict] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ValidationConfig":
        return cls(schema=data.get("schema"))


# =============================================================================
# Audit Config (Pattern 6: Audit)
# =============================================================================

@dataclass
class OrdinalConfig:
    """Configuration for an ordinal field with progression semantics."""
    field: str
    progression: list[str] = field(default_factory=list)
    terminal: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "OrdinalConfig":
        return cls(
            field=data.get("field", ""),
            progression=data.get("progression", []),
            terminal=data.get("terminal", []),
        )


@dataclass
class AuditConfig:
    """
    Configuration for change tracking and regression detection.

    @implements feature:reconciliation/audit-semantics
      - KindDefinition supports audit section for change tracking semantics
    """
    ordinals: list[OrdinalConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "AuditConfig":
        ordinals = [
            OrdinalConfig.from_dict(o)
            for o in data.get("ordinals", [])
        ]
        return cls(ordinals=ordinals)


# =============================================================================
# KindDefinition (Complete)
# =============================================================================

@dataclass
class KindDefinition:
    """
    Complete definition of a kind's behavior.

    Encompasses all six semantic patterns:
    1. Validation - via validation.schema
    2. References - via verification.references
    3. Coverage - via verification.coverage
    4. Relationships - via relationships
    5. Conditions - via when clauses throughout
    6. Audit - via audit.ordinals
    """
    name: str
    category: str = "unknown"
    description: str = ""
    validation: Optional[ValidationConfig] = None
    verification: Optional[VerificationConfig] = None
    relationships: list[RelationshipDefinition] = field(default_factory=list)
    audit: Optional[AuditConfig] = None

    @classmethod
    def from_dict(cls, doc: dict) -> Optional["KindDefinition"]:
        """Parse a KindDefinition from a document."""
        metadata = doc.get("metadata", {})
        spec = doc.get("spec", {})

        name = metadata.get("name")
        if not name:
            return None

        # Parse validation
        validation = None
        if "validation" in spec:
            validation = ValidationConfig.from_dict(spec["validation"])

        # Parse verification
        verification = None
        if "verification" in spec:
            verification = VerificationConfig.from_dict(spec["verification"])

        # Parse relationships
        relationships = [
            RelationshipDefinition.from_dict(r)
            for r in spec.get("relationships", [])
        ]

        # Parse audit
        audit = None
        if "audit" in spec:
            audit = AuditConfig.from_dict(spec["audit"])

        return cls(
            name=name,
            category=spec.get("category", "unknown"),
            description=spec.get("description", ""),
            validation=validation,
            verification=verification,
            relationships=relationships,
            audit=audit,
        )

    def get_schema_fields(self) -> list[str]:
        """Get list of fields defined in the validation schema."""
        if not self.validation or not self.validation.schema:
            return []

        schema = self.validation.schema
        properties = schema.get("properties", {})
        return list(properties.keys())

    def get_list_fields(self) -> set[str]:
        """Get set of fields that are arrays according to schema."""
        if not self.validation or not self.validation.schema:
            return set()

        schema = self.validation.schema
        properties = schema.get("properties", {})

        list_fields = set()
        for name, prop in properties.items():
            if prop.get("type") == "array":
                list_fields.add(name)
            elif "oneOf" in prop:
                # Check if any option is array
                for option in prop["oneOf"]:
                    if option.get("type") == "array":
                        list_fields.add(name)
                        break

        return list_fields


# =============================================================================
# Issue Type (Shared between reconcile and audit)
# =============================================================================

@dataclass
class Issue:
    """A verification issue."""
    severity: str  # error, warning, info
    spec_file: str
    entity: str
    issue_type: str
    message: str
    path: Optional[str] = None


# =============================================================================
# Spec Discovery & Parsing
# =============================================================================

def find_spec_files(spec_dir: str, exclude_dirs: list[str] = None) -> list[Path]:
    """
    Find all YAML spec files, excluding specified directories.

    @implements feature:reconciliation/parse-specs
      - Can find all YAML spec files in spec directory
    """
    spec_path = Path(spec_dir)
    if not spec_path.exists():
        return []

    exclude_dirs = exclude_dirs or []
    files = []

    for pattern in ["**/*.yaml", "**/*.yml"]:
        for f in spec_path.glob(pattern):
            # Check if file is in excluded directory
            excluded = False
            for exclude in exclude_dirs:
                if exclude in f.parts:
                    excluded = True
                    break
            if not excluded:
                files.append(f)

    return files


def resolve_substitutions(data: Any, base_path: Path) -> Any:
    """
    Resolve $json, $yaml, $text substitution directives.

    Paths are relative to the file containing the directive.

    @implements feature:reconciliation/substitution
      - Supports $json directive to import JSON files
      - Supports $yaml directive to import YAML files
      - Supports $text directive to import text files
      - Works with relative paths from the containing file
    """
    if isinstance(data, dict):
        # Check for substitution directive
        if len(data) == 1:
            if "$json" in data:
                file_path = base_path / data["$json"]
                with open(file_path) as f:
                    import json
                    return json.load(f)
            elif "$yaml" in data:
                file_path = base_path / data["$yaml"]
                with open(file_path) as f:
                    return yaml.safe_load(f)
            elif "$text" in data:
                file_path = base_path / data["$text"]
                with open(file_path) as f:
                    return f.read()

        # Recurse into dict
        return {k: resolve_substitutions(v, base_path) for k, v in data.items()}

    elif isinstance(data, list):
        return [resolve_substitutions(item, base_path) for item in data]

    return data


def parse_spec_file(path: Path, resolve_subs: bool = True) -> list[dict]:
    """
    Parse a YAML file, handling multi-document files and substitutions.

    @implements feature:reconciliation/parse-specs
      - Can parse single-document YAML files
      - Can parse multi-document YAML files

    @implements feature:kind-system/uniform-entity-handling
      - Multi-document YAML keeps related entities in one file
    """
    with open(path) as f:
        content = f.read()

    docs = []
    for doc in yaml.safe_load_all(content):
        if doc:  # Skip empty documents
            if resolve_subs:
                doc = resolve_substitutions(doc, path.parent)
            docs.append(doc)
    return docs


def load_kind_definitions(kinds_dir: str) -> dict[str, KindDefinition]:
    """
    Load all KindDefinitions from the kinds directory.

    @implements feature:kind-system/custom-kind-loading
      - KindDefinitions are loaded from configurable directory
      - Any valid KindDefinition YAML is processed
      - No hardcoded kind names in loading logic
    """
    kinds_path = Path(kinds_dir)
    if not kinds_path.exists():
        return {}

    definitions = {}

    for path in kinds_path.glob("*.yaml"):
        try:
            docs = parse_spec_file(path, resolve_subs=True)
            for doc in docs:
                if doc.get("kind") == "KindDefinition":
                    kind_def = KindDefinition.from_dict(doc)
                    if kind_def:
                        definitions[kind_def.name] = kind_def
        except Exception as e:
            print(f"Warning: Failed to load KindDefinition from {path}: {e}", file=sys.stderr)

    return definitions


# =============================================================================
# Entity Indexing
# =============================================================================

@dataclass
class IndexedEntity:
    """An entity in the index with its metadata."""
    ref: EntityRef
    doc: dict
    spec_file: str
    kind_def: Optional[KindDefinition] = None


def index_entities(
    specs: list[dict],
    kind_definitions: dict[str, KindDefinition],
    spec_file: str = "",
) -> dict[str, IndexedEntity]:
    """
    Build an index of entities from loaded specs.

    Returns dict mapping entity_ref string -> IndexedEntity
    """
    index: dict[str, IndexedEntity] = {}

    for doc in specs:
        kind = doc.get("kind", "")
        metadata = doc.get("metadata", {})
        name = metadata.get("name", "")

        if not kind or not name or kind == "KindDefinition":
            continue

        # Parse entity ref from name
        if "/" in name:
            parent, entity_name = name.split("/", 1)
            ref = EntityRef(kind=kind, name=entity_name, parent=parent)
        else:
            ref = EntityRef(kind=kind, name=name)

        ref_str = ref.to_ref_string()
        kind_def = kind_definitions.get(kind)

        if kind_def is None:
            raise ValueError(
                f"No KindDefinition found for kind '{kind}' "
                f"(entity: {ref_str}, file: {spec_file}). "
                f"All kinds must have a KindDefinition in the kinds directory."
            )

        index[ref_str] = IndexedEntity(
            ref=ref,
            doc=doc,
            spec_file=spec_file,
            kind_def=kind_def,
        )

    return index


# =============================================================================
# Field Extraction (JSONPath-like)
# =============================================================================

def extract_field_values(data: dict, field_path: str) -> list[Any]:
    """
    Extract values from data using a JSONPath-like field selector.

    Supports:
    - spec.field - direct field access
    - spec.items[] - iterate over array
    - spec.items[].field - field from each array item

    Returns list of values found.
    """
    parts = field_path.split(".")
    return _extract_recursive(data, parts)


def _extract_recursive(data: Any, parts: list[str]) -> list[Any]:
    """Recursively extract field values."""
    if not parts:
        if data is not None:
            return [data]
        return []

    part = parts[0]
    remaining = parts[1:]

    # Handle array notation: field[]
    if part.endswith("[]"):
        field_name = part[:-2]
        items = data.get(field_name, []) if isinstance(data, dict) else []

        # Handle "disabled" special value
        if items == "disabled":
            return []

        if not isinstance(items, list):
            items = []

        results = []
        for item in items:
            results.extend(_extract_recursive(item, remaining))
        return results

    # Handle direct field access
    if isinstance(data, dict) and part in data:
        return _extract_recursive(data[part], remaining)

    return []


# =============================================================================
# Reference Verification (Pattern 2: References)
# =============================================================================

def check_path_exists(path: str, repo_root: str) -> bool:
    """Check if a path exists, supporting glob patterns."""
    full_path = os.path.join(repo_root, path)

    # If it contains glob characters, check if any matches
    if any(c in path for c in ["*", "?", "["]):
        matches = glob_module.glob(full_path)
        return len(matches) > 0

    return os.path.exists(full_path)


def verify_reference(
    ref_check: ReferenceCheck,
    entity: dict,
    entity_name: str,
    spec_file: str,
    repo_root: str,
    entity_index: dict[str, "IndexedEntity"],
) -> list[Issue]:
    """
    Verify a single reference check against an entity.

    Returns list of issues found.
    """
    issues = []

    # Check reference-level condition
    if ref_check.when and not evaluate_condition(ref_check.when, entity):
        return issues  # Condition not met, skip this check

    # Extract values from the field
    values = extract_field_values(entity, ref_check.field)

    for value in values:
        if not isinstance(value, str):
            continue

        if ref_check.type == "path":
            # Check file/directory exists
            if not check_path_exists(value, repo_root):
                issues.append(Issue(
                    severity=ref_check.severity,
                    spec_file=spec_file,
                    entity=entity_name,
                    issue_type="missing_path",
                    message=f"Path does not exist: {value}",
                    path=value,
                ))

        elif ref_check.type == "entity-ref":
            # Check entity exists in index
            ref = EntityRef.parse(value)
            if ref and ref.to_ref_string() not in entity_index:
                issues.append(Issue(
                    severity=ref_check.severity,
                    spec_file=spec_file,
                    entity=entity_name,
                    issue_type="missing_entity",
                    message=f"Referenced entity does not exist: {value}",
                    path=None,
                ))

    return issues


def verify_entity_references(
    entity: IndexedEntity,
    repo_root: str,
    entity_index: dict[str, IndexedEntity],
) -> list[Issue]:
    """
    Verify all reference checks for an entity.

    Returns list of issues found.

    @implements feature:kind-system/when-conditions
      - Conditions can be attached at entity, section, and check levels
    """
    issues = []

    if not entity.kind_def or not entity.kind_def.verification:
        return issues

    verification = entity.kind_def.verification
    entity_name = entity.doc.get("metadata", {}).get("name", "unknown")

    # Check entity-level condition
    if verification.when and not evaluate_condition(verification.when, entity.doc):
        return issues  # Entity-level condition not met, skip all verification

    # Check each reference
    for ref_check in verification.references:
        ref_issues = verify_reference(
            ref_check,
            entity.doc,
            entity_name,
            entity.spec_file,
            repo_root,
            entity_index,
        )
        issues.extend(ref_issues)

    return issues


# =============================================================================
# Relationship Graph (Pattern 4: Relationships)
# =============================================================================

def extract_entity_relationships(
    entity: IndexedEntity,
) -> list[Relationship]:
    """
    Extract relationships from an entity based on its KindDefinition.

    @implements feature:kind-system/relationships-modeling
      - No hardcoded kind checks in relationship extraction
    """
    relationships = []

    if not entity.kind_def:
        return relationships

    source_ref = entity.ref

    for rel_def in entity.kind_def.relationships:
        # Extract values from the relationship field
        values = extract_field_values(entity.doc, rel_def.field)

        for value in values:
            if isinstance(value, str):
                target_ref = EntityRef.parse(value)
                if target_ref:
                    relationships.append(Relationship(
                        source=source_ref,
                        target=target_ref,
                        rel_type=rel_def.type,
                    ))

    return relationships


def build_relationship_graph(
    entities: dict[str, IndexedEntity],
) -> RelationshipGraphResult:
    """
    Build relationship graph from indexed entities.

    Extracts entities and relationships, validates references, detects cycles.

    @implements feature:reconciliation/relationship-graph
      - Extracts entity references from relationship fields in KindDefinition
      - Builds index of all defined entities across specs
      - Validates referenced entities exist
      - Reports broken references as errors
      - Detects circular dependencies
      - Outputs dependency graph in JSON format
    """
    result = RelationshipGraphResult()

    # Collect all entities
    result.entities = [e.ref for e in entities.values()]
    entity_set = set(result.entities)

    # Extract all relationships
    for entity in entities.values():
        rels = extract_entity_relationships(entity)
        result.relationships.extend(rels)

    # Validate references - check that targets exist
    for rel in result.relationships:
        if rel.target not in entity_set:
            result.broken_refs.append((rel.source, rel.target, rel.rel_type))

    # Detect cycles using DFS
    result.cycles = detect_cycles(result.entities, result.relationships)

    return result


def detect_cycles(
    entities: list[EntityRef],
    relationships: list[Relationship],
) -> list[list[EntityRef]]:
    """
    Detect cycles in the relationship graph using DFS.

    Returns list of cycles found (each cycle is a list of EntityRefs).
    """
    # Build adjacency list
    adj: dict[EntityRef, list[EntityRef]] = {e: [] for e in entities}
    for rel in relationships:
        if rel.source in adj:
            adj[rel.source].append(rel.target)

    cycles = []
    visited = set()
    rec_stack = set()
    path = []

    def dfs(node: EntityRef) -> bool:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                if neighbor in adj:  # Only follow edges to known entities
                    if dfs(neighbor):
                        return True
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
                return False  # Continue looking for more cycles

        path.pop()
        rec_stack.remove(node)
        return False

    for entity in entities:
        if entity not in visited:
            dfs(entity)

    return cycles


# =============================================================================
# Schema Validation (Pattern 1: Validation)
# =============================================================================

def validate_entity_schema(
    entity: IndexedEntity,
) -> list[Issue]:
    """
    Validate an entity against its KindDefinition's JSON Schema.

    Returns list of validation issues.
    """
    issues = []

    if not entity.kind_def or not entity.kind_def.validation:
        return issues

    validation = entity.kind_def.validation
    if not validation.schema:
        return issues

    entity_name = entity.doc.get("metadata", {}).get("name", "unknown")
    spec = entity.doc.get("spec", {})

    try:
        import jsonschema
        jsonschema.validate(instance=spec, schema=validation.schema)
    except ImportError:
        # jsonschema not available, skip validation
        pass
    except Exception as e:
        if hasattr(e, 'absolute_path'):
            path = ".".join(str(p) for p in e.absolute_path) if e.absolute_path else "root"
            message = f"Schema validation failed at '{path}': {e.message}"
        else:
            message = f"Schema validation failed: {e}"

        issues.append(Issue(
            severity="error",
            spec_file=entity.spec_file,
            entity=entity_name,
            issue_type="schema_validation",
            message=message,
            path=None,
        ))

    return issues


# =============================================================================
# Tooling Configuration (projectspec.yaml)
# =============================================================================

@dataclass
class ProjectConfig:
    """
    Tooling configuration loaded from projectspec.yaml.

    This is NOT a spec entity - it's plain config for the reconcile tool.
    Located in repo root, not in spec directory.
    """

    kinds: Optional[str] = None  # Path to KindDefinitions directory
    ignore: list[str] = field(default_factory=list)  # Directories to ignore


def load_config(repo_root: str) -> ProjectConfig:
    """
    Load tooling configuration from projectspec.yaml in repo root.

    If no config file exists, returns default configuration.

    @implements feature:reconciliation/tooling-config
      - Reads optional projectspec.yaml from repo root
      - Plain YAML config, no envelope (not a spec entity)
      - Uses convention (spec/kinds/) when no config present
    """
    root_path = Path(repo_root)

    for name in ["projectspec.yaml", "projectspec.yml"]:
        config_file = root_path / name
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    data = yaml.safe_load(f) or {}

                return ProjectConfig(
                    kinds=data.get("kinds"),
                    ignore=data.get("ignore", []),
                )
            except Exception:
                pass

    return ProjectConfig()


def get_kinds_dir(config: ProjectConfig, spec_dir: str) -> str:
    """
    Get KindDefinitions directory path from config, or use convention.

    Convention: spec/kinds/
    Override: kinds field in projectspec.yaml (relative to repo root)

    @implements feature:reconciliation/tooling-config
      - Supports kinds field to override KindDefinitions location
    """
    if config.kinds:
        # Resolve relative to repo root (parent of spec_dir by convention)
        repo_root = Path(spec_dir).parent
        return str((repo_root / config.kinds).resolve())

    # Convention: spec/kinds
    return os.path.join(spec_dir, "kinds")


# =============================================================================
# Coverage Extraction (Pattern 3: Coverage)
# =============================================================================

def get_evidence_definition(
    kind_def: Optional[KindDefinition],
    evidence_name: str,
) -> Optional[EvidenceDefinition]:
    """
    Get an evidence definition by name from a KindDefinition.

    Returns None if kind_def is None, has no coverage config,
    or doesn't have evidence with that name.
    """
    if not kind_def or not kind_def.verification or not kind_def.verification.coverage:
        return None

    for evidence in kind_def.verification.coverage.evidence:
        if evidence.name == evidence_name:
            return evidence

    return None


def get_requirements_field(kind_def: Optional[KindDefinition]) -> Optional[str]:
    """
    Get the requirements field path from a KindDefinition's coverage config.

    Returns None if no coverage config.
    """
    if not kind_def or not kind_def.verification or not kind_def.verification.coverage:
        return None

    return kind_def.verification.coverage.requirementsField


def extract_requirements(entity: IndexedEntity) -> list[str]:
    """
    Extract requirements from an entity using its KindDefinition's coverage config.

    Uses coverage.requirementsField to determine which field contains requirements.
    Falls back to spec.acceptance[] if no coverage config.

    @implements feature:kind-system/verification-coverage
      - Requirements field path configurable
    """
    kind_def = entity.kind_def
    doc = entity.doc

    # Get requirements field from coverage config, or use default
    requirements_field = get_requirements_field(kind_def)
    if not requirements_field:
        requirements_field = "spec.acceptance[]"

    # Extract values from the field
    values = extract_field_values(doc, requirements_field)

    # Filter to strings only
    return [v for v in values if isinstance(v, str)]


def extract_evidence_sources(
    entity: IndexedEntity,
    evidence_name: str,
) -> list[str]:
    """
    Extract source file paths for a specific evidence type.

    Uses the evidence definition's sourcesField to find paths.
    Checks evidence-level conditions.

    @implements feature:kind-system/verification-coverage
      - Evidence types with marker and adapter
      - Per-evidence conditions via when clause
    """
    evidence = get_evidence_definition(entity.kind_def, evidence_name)
    if not evidence:
        return []

    # Check evidence-level condition
    if evidence.when and not evaluate_condition(evidence.when, entity.doc):
        return []

    # Extract values from sourcesField
    values = extract_field_values(entity.doc, evidence.sourcesField)

    # Filter to strings only
    return [v for v in values if isinstance(v, str)]


def should_check_coverage(
    entity: IndexedEntity,
    evidence_name: Optional[str] = None,
) -> bool:
    """
    Check if coverage verification should run for an entity.

    Evaluates:
    1. Entity-level condition (verification.when)
    2. Coverage-level condition (coverage.when)
    3. Evidence-level condition (evidence.when) if evidence_name provided

    Returns True if all applicable conditions pass.
    """
    kind_def = entity.kind_def
    doc = entity.doc

    if not kind_def or not kind_def.verification:
        return False

    verification = kind_def.verification

    # Check entity-level condition
    if verification.when and not evaluate_condition(verification.when, doc):
        return False

    # Check if coverage config exists
    if not verification.coverage:
        return False

    coverage = verification.coverage

    # Check coverage-level condition
    if coverage.when and not evaluate_condition(coverage.when, doc):
        return False

    # Check evidence-level condition if specified
    if evidence_name:
        evidence = get_evidence_definition(kind_def, evidence_name)
        if evidence and evidence.when:
            if not evaluate_condition(evidence.when, doc):
                return False

    return True


# =============================================================================
# Marker Adapters (Pattern 3: Coverage - Pluggable Parsing)
# =============================================================================

@dataclass
class MarkerMatch:
    """
    A match found by a marker adapter.

    Represents a single occurrence of a marker in a file,
    along with the entity reference and criteria it claims.
    """
    file_path: str
    location: str       # e.g., function name, class name, "module", "file"
    line: int
    entity_ref: str     # e.g., "feature:auth/login"
    criteria: list[str] # List of criterion texts


class MarkerAdapter:
    """
    Base class for marker adapters.

    Adapters extract markers from files. Each adapter knows how to
    parse a specific file format and extract marker declarations.

    @implements feature:kind-system/verification-coverage
      - Evidence types with marker and adapter
    """
    name: str = ""
    file_patterns: list[str] = field(default_factory=list)

    def extract_markers(
        self,
        file_path: Path,
        marker: str,
    ) -> list[MarkerMatch]:
        """
        Extract all occurrences of a marker from a file.

        Args:
            file_path: Path to the file to parse
            marker: The marker to look for (e.g., "@tests")

        Returns:
            List of MarkerMatch objects for each marker found

        @implements feature:reconciliation/criteria-verification
          - Marker name is configurable via KindDefinition evidence.marker field
          - Markers in code declare which criteria they cover via docstring or comment
        """
        raise NotImplementedError


def _parse_marker_block(content: str, marker: str) -> list[tuple[str, list[str]]]:
    """
    Parse marker declarations from text content.

    Looks for patterns like:
        @marker entity:ref
          - criterion 1
          - criterion 2

    Returns list of (entity_ref, criteria) tuples.

    @implements feature:reconciliation/criteria-verification
      - Marker format is MARKER entity:name followed by indented criteria list
      - Static parsing, no code execution required
    """
    import re

    results = []
    lines = content.split("\n")

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Look for marker tag (e.g., @tests, @implements, @documents)
        if line.startswith(marker):
            # Extract entity ref from the marker line
            match = re.match(rf"{re.escape(marker)}\s+(\S+)", line)
            if match:
                entity_ref = match.group(1)
                criteria = []

                # Collect criteria from following lines
                i += 1
                while i < len(lines):
                    criterion_line = lines[i]
                    # Check for indented list item (spaces, dash, space, text)
                    criterion_match = re.match(r"^\s+-\s+(.+)$", criterion_line)
                    if criterion_match:
                        criterion_text = criterion_match.group(1).strip()
                        criteria.append(criterion_text)
                        i += 1
                    elif criterion_line.strip() == "":
                        # Blank line ends criteria list
                        break
                    elif criterion_line.strip().startswith("@"):
                        # Another tag starts
                        break
                    else:
                        # Non-matching line, stop
                        break

                if criteria:
                    results.append((entity_ref, criteria))
                continue

        i += 1

    return results


class PythonDocstringAdapter(MarkerAdapter):
    """
    Adapter for extracting markers from Python docstrings.

    Looks in module, class, and function docstrings for marker declarations.

    @implements feature:reconciliation/python-docstring-adapter
      - Parses configurable markers from Python module docstrings
      - Parses configurable markers from Python class docstrings
      - Parses configurable markers from Python function docstrings
      - Registered as python-docstring adapter in KindDefinitions
    """
    name = "python-docstring"
    file_patterns = ["**/*.py"]

    def extract_markers(
        self,
        file_path: Path,
        marker: str,
    ) -> list[MarkerMatch]:
        import ast

        try:
            source = file_path.read_text()
            tree = ast.parse(source)
        except SyntaxError:
            return []
        except Exception:
            return []

        results = []

        # Check module docstring
        module_docstring = ast.get_docstring(tree)
        if module_docstring and marker in module_docstring:
            for entity_ref, criteria in _parse_marker_block(module_docstring, marker):
                results.append(MarkerMatch(
                    file_path=str(file_path),
                    location="module",
                    line=1,
                    entity_ref=entity_ref,
                    criteria=criteria,
                ))

        # Walk AST for classes and functions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                if not docstring or marker not in docstring:
                    continue

                location = node.name
                if isinstance(node, ast.ClassDef):
                    location = f"class {node.name}"

                for entity_ref, criteria in _parse_marker_block(docstring, marker):
                    results.append(MarkerMatch(
                        file_path=str(file_path),
                        location=location,
                        line=node.lineno,
                        entity_ref=entity_ref,
                        criteria=criteria,
                    ))

        return results


class PythonTestDocstringAdapter(MarkerAdapter):
    """
    Adapter for extracting markers from Python test docstrings.

    Only looks in test function docstrings (functions starting with test_).

    @implements feature:reconciliation/python-test-docstring-adapter
      - Parses configurable markers from Python test function docstrings
      - Only scans functions with test_ prefix (pytest convention)
      - Registered as python-test-docstring adapter in KindDefinitions
    """
    name = "python-test-docstring"
    file_patterns = ["**/test_*.py"]

    def extract_markers(
        self,
        file_path: Path,
        marker: str,
    ) -> list[MarkerMatch]:
        import ast

        try:
            source = file_path.read_text()
            tree = ast.parse(source)
        except SyntaxError:
            return []
        except Exception:
            return []

        results = []

        for node in ast.walk(tree):
            # Only look at test functions
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith("test_"):
                    continue

                docstring = ast.get_docstring(node)
                if not docstring or marker not in docstring:
                    continue

                for entity_ref, criteria in _parse_marker_block(docstring, marker):
                    results.append(MarkerMatch(
                        file_path=str(file_path),
                        location=node.name,
                        line=node.lineno,
                        entity_ref=entity_ref,
                        criteria=criteria,
                    ))

        return results


class MarkdownCommentAdapter(MarkerAdapter):
    """
    Adapter for extracting markers from Markdown HTML comments.

    Looks for markers inside <!-- --> HTML comments.

    @implements feature:reconciliation/markdown-comment-adapter
      - Parses configurable markers from markdown HTML comments
      - Extracts marker blocks from <!-- --> comment syntax
      - Registered as markdown-comment adapter in KindDefinitions
    """
    name = "markdown-comment"
    file_patterns = ["**/*.md", "**/*.markdown"]

    def extract_markers(
        self,
        file_path: Path,
        marker: str,
    ) -> list[MarkerMatch]:
        import re

        try:
            content = file_path.read_text()
        except Exception:
            return []

        results = []

        # Find HTML comments containing the marker
        comment_pattern = re.compile(r"<!--(.*?)-->", re.DOTALL)

        for match in comment_pattern.finditer(content):
            comment_content = match.group(1)
            if marker not in comment_content:
                continue

            # Calculate line number
            line_num = content[:match.start()].count("\n") + 1

            for entity_ref, criteria in _parse_marker_block(comment_content, marker):
                results.append(MarkerMatch(
                    file_path=str(file_path),
                    location="file",
                    line=line_num,
                    entity_ref=entity_ref,
                    criteria=criteria,
                ))

        return results


class YamlCommentAdapter(MarkerAdapter):
    """
    Adapter for extracting markers from YAML comments.

    Looks for markers in lines starting with #.

    @implements feature:reconciliation/yaml-comment-adapter
      - Parses configurable markers from YAML hash comments
      - Works with spec files and other YAML configuration
      - Registered as yaml-comment adapter in KindDefinitions
    """
    name = "yaml-comment"
    file_patterns = ["**/*.yaml", "**/*.yml"]

    def extract_markers(
        self,
        file_path: Path,
        marker: str,
    ) -> list[MarkerMatch]:
        import re

        try:
            content = file_path.read_text()
        except Exception:
            return []

        results = []
        lines = content.split("\n")

        # Collect consecutive comment lines into blocks
        i = 0
        while i < len(lines):
            line = lines[i]

            # Check if this is a comment line containing the marker
            if line.strip().startswith("#") and marker in line:
                # Collect the comment block
                comment_lines = []
                block_start = i + 1  # 1-indexed line number

                while i < len(lines) and lines[i].strip().startswith("#"):
                    # Strip the # prefix and any leading whitespace after it
                    comment_text = re.sub(r"^#\s?", "", lines[i].strip())
                    comment_lines.append(comment_text)
                    i += 1

                # Parse the collected comment block
                comment_content = "\n".join(comment_lines)
                for entity_ref, criteria in _parse_marker_block(comment_content, marker):
                    results.append(MarkerMatch(
                        file_path=str(file_path),
                        location="file",
                        line=block_start,
                        entity_ref=entity_ref,
                        criteria=criteria,
                    ))
                continue

            i += 1

        return results


class JSDocCommentAdapter(MarkerAdapter):
    """
    Adapter for extracting markers from JSDoc comments.

    Looks for markers inside /** ... */ JSDoc-style comments.

    @implements feature:reconciliation/jsdoc-comment-adapter
      - Parses configurable markers from JSDoc comments (/** ... */)
      - Cleans JSDoc formatting (removes leading * from lines)
      - Works with JavaScript and TypeScript files
      - Registered as jsdoc-comment adapter in KindDefinitions
    """
    name = "jsdoc-comment"
    file_patterns = [
        "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx",
        "**/*.mjs", "**/*.mts", "**/*.cjs", "**/*.cts",
        "**/*.vue", "**/*.svelte", "**/*.astro",
    ]

    def extract_markers(
        self,
        file_path: Path,
        marker: str,
    ) -> list[MarkerMatch]:
        import re

        try:
            content = file_path.read_text()
        except Exception:
            return []

        results = []

        # Pattern for JSDoc comments: /** ... */
        jsdoc_pattern = re.compile(r'/\*\*\s*(.*?)\*/', re.DOTALL)

        for match in jsdoc_pattern.finditer(content):
            comment_content = match.group(1)
            if marker not in comment_content:
                continue

            # Clean up JSDoc formatting (* at start of lines)
            cleaned_lines = []
            for line in comment_content.split('\n'):
                # Remove leading whitespace and * prefix
                cleaned = re.sub(r'^\s*\*\s?', '', line)
                cleaned_lines.append(cleaned)

            cleaned_content = "\n".join(cleaned_lines)

            # Calculate line number
            line_num = content[:match.start()].count("\n") + 1

            for entity_ref, criteria in _parse_marker_block(cleaned_content, marker):
                results.append(MarkerMatch(
                    file_path=str(file_path),
                    location="file",
                    line=line_num,
                    entity_ref=entity_ref,
                    criteria=criteria,
                ))

        return results


class AdapterRegistry:
    """
    Registry for marker adapters.

    Provides lookup of adapters by name, used when processing
    evidence definitions from KindDefinitions.
    """

    def __init__(self):
        self._adapters: dict[str, MarkerAdapter] = {}

    def register(self, adapter: MarkerAdapter) -> None:
        """Register an adapter by its name."""
        self._adapters[adapter.name] = adapter

    def get(self, name: str) -> Optional[MarkerAdapter]:
        """Get an adapter by name, or None if not found."""
        return self._adapters.get(name)

    def list_available(self) -> list[str]:
        """List all registered adapter names."""
        return list(self._adapters.keys())


def create_default_registry() -> AdapterRegistry:
    """
    Create a registry with all built-in adapters.

    Built-in adapters:
    - python-docstring: @marker in Python module/class/function docstrings
    - python-test-docstring: @marker in Python test function docstrings
    - markdown-comment: @marker in Markdown HTML comments
    - yaml-comment: @marker in YAML comments (lines starting with #)
    - jsdoc-comment: @marker in JSDoc comments (/** ... */)
    """
    registry = AdapterRegistry()
    registry.register(PythonDocstringAdapter())
    registry.register(PythonTestDocstringAdapter())
    registry.register(MarkdownCommentAdapter())
    registry.register(YamlCommentAdapter())
    registry.register(JSDocCommentAdapter())
    return registry


# Global default registry
_default_registry: Optional[AdapterRegistry] = None


def get_adapter_registry() -> AdapterRegistry:
    """Get the global adapter registry, creating it if needed."""
    global _default_registry
    if _default_registry is None:
        _default_registry = create_default_registry()
    return _default_registry


def get_adapter(name: str) -> Optional[MarkerAdapter]:
    """Get an adapter by name from the global registry."""
    return get_adapter_registry().get(name)
