"""
Tests for speccore module - shared core logic for projectspec tooling.

@tests feature:kind-system/when-conditions
  - Conditions evaluate field values against operators
  - Supports equals, notEquals, in, notIn, exists operators
  - Supports all/any for combined conditions
  - Conditions can be attached at entity, section, and check levels

@tests feature:kind-system/shared-core-module
  - Shared types defined in core.py
  - KindDefinition parsing shared between reconcile and audit
  - Entity indexing shared between tools
  - Condition evaluation shared between tools

@tests feature:kind-system/verification-coverage
  - Coverage defined in verification.coverage block
  - Requirements field path configurable
  - Evidence types with marker and adapter
  - Per-evidence conditions via when clause

@tests feature:kind-system/verification-references
  - Reference checks defined in verification.references block
  - Supports path and entity-ref types
  - Per-check conditions via when clause
  - Severity configurable per check

@tests feature:kind-system/relationships-modeling
  - Relationships defined in separate relationships block
  - Relationship types configurable (depends-on, part-of, implements, extends)
  - Separated from verification (modeling vs checking)
  - No hardcoded kind checks in relationship extraction
"""

import pytest
from pathlib import Path

# Import from projectspec package (core module)
from projectspec.core import (
    EntityRef,
    WhenCondition,
    evaluate_condition,
    get_field_value,
    ReferenceCheck,
    EvidenceDefinition,
    CoverageConfig,
    RelationshipDefinition,
    VerificationConfig,
    KindDefinition,
    find_spec_files,
    parse_spec_file,
    index_entities,
    # Tooling config
    ProjectConfig,
    load_config,
    get_kinds_dir,
)


# =============================================================================
# EntityRef Tests
# =============================================================================

class TestEntityRef:
    """Tests for entity reference parsing."""

    def test_parse_simple_ref(self):
        """Parse kind:name format."""
        ref = EntityRef.parse("feature:login")
        assert ref is not None
        assert ref.kind == "feature"
        assert ref.name == "login"
        assert ref.parent is None

    def test_parse_hierarchical_ref(self):
        """Parse kind:parent/name format."""
        ref = EntityRef.parse("feature:auth/login")
        assert ref is not None
        assert ref.kind == "feature"
        assert ref.parent == "auth"
        assert ref.name == "login"

    def test_parse_invalid_ref(self):
        """Invalid ref returns None."""
        assert EntityRef.parse("invalid") is None
        assert EntityRef.parse("") is None

    def test_str_representation(self):
        """String representation matches input."""
        ref = EntityRef(kind="Feature", name="login", parent="auth")
        assert str(ref) == "Feature:auth/login"

    def test_to_ref_string_lowercase(self):
        """to_ref_string returns lowercase kind."""
        ref = EntityRef(kind="Feature", name="login", parent="auth")
        assert ref.to_ref_string() == "feature:auth/login"


# =============================================================================
# Condition Evaluation Tests
# =============================================================================

class TestConditionEvaluation:
    """
    Tests for when condition evaluation.

    @tests feature:kind-system/when-conditions
      - Conditions evaluate field values against operators
      - Conditions can be attached at entity, section, and check levels

    @tests feature:kind-system/shared-core-module
      - Condition evaluation shared between tools
    """

    @pytest.fixture
    def sample_entity(self):
        return {
            "kind": "Feature",
            "metadata": {
                "name": "auth/login",
                "labels": {
                    "priority": "high",
                    "verified": True,
                }
            },
            "spec": {
                "status": "implemented",
                "acceptance": ["User can log in"],
                "implementedIn": ["src/auth.py"],
                "testedIn": "disabled",
            }
        }

    def test_get_field_value_simple(self, sample_entity):
        """
        Get simple field value.

        @tests feature:kind-system/when-conditions
          - Conditions evaluate field values against operators
        """
        assert get_field_value(sample_entity, "kind") == "Feature"

    def test_get_field_value_nested(self, sample_entity):
        """Get nested field value."""
        assert get_field_value(sample_entity, "spec.status") == "implemented"
        assert get_field_value(sample_entity, "metadata.labels.priority") == "high"

    def test_get_field_value_missing(self, sample_entity):
        """Missing field returns None."""
        assert get_field_value(sample_entity, "spec.missing") is None
        assert get_field_value(sample_entity, "nonexistent.path") is None

    def test_condition_equals(self, sample_entity):
        """
        @tests feature:kind-system/when-conditions
          - Supports equals, notEquals, in, notIn, exists operators
        """
        cond = WhenCondition(field="spec.status", equals="implemented")
        assert evaluate_condition(cond, sample_entity) is True

        cond = WhenCondition(field="spec.status", equals="planned")
        assert evaluate_condition(cond, sample_entity) is False

    def test_condition_not_equals(self, sample_entity):
        """notEquals operator."""
        cond = WhenCondition(field="spec.status", notEquals="planned")
        assert evaluate_condition(cond, sample_entity) is True

        cond = WhenCondition(field="spec.status", notEquals="implemented")
        assert evaluate_condition(cond, sample_entity) is False

    def test_condition_in(self, sample_entity):
        """in operator."""
        cond = WhenCondition(field="spec.status", in_=["implemented", "deprecated"])
        assert evaluate_condition(cond, sample_entity) is True

        cond = WhenCondition(field="spec.status", in_=["planned", "proposed"])
        assert evaluate_condition(cond, sample_entity) is False

    def test_condition_not_in(self, sample_entity):
        """notIn operator."""
        cond = WhenCondition(field="spec.status", notIn=["planned", "proposed"])
        assert evaluate_condition(cond, sample_entity) is True

        cond = WhenCondition(field="spec.status", notIn=["implemented", "deprecated"])
        assert evaluate_condition(cond, sample_entity) is False

    def test_condition_exists(self, sample_entity):
        """exists operator."""
        cond = WhenCondition(field="spec.status", exists=True)
        assert evaluate_condition(cond, sample_entity) is True

        cond = WhenCondition(field="spec.missing", exists=True)
        assert evaluate_condition(cond, sample_entity) is False

        cond = WhenCondition(field="spec.missing", exists=False)
        assert evaluate_condition(cond, sample_entity) is True

    def test_condition_all_combined(self, sample_entity):
        """
        @tests feature:kind-system/when-conditions
          - Supports all/any for combined conditions
        """
        cond = WhenCondition(all_=[
            WhenCondition(field="spec.status", equals="implemented"),
            WhenCondition(field="metadata.labels.priority", equals="high"),
        ])
        assert evaluate_condition(cond, sample_entity) is True

        cond = WhenCondition(all_=[
            WhenCondition(field="spec.status", equals="implemented"),
            WhenCondition(field="metadata.labels.priority", equals="low"),
        ])
        assert evaluate_condition(cond, sample_entity) is False

    def test_condition_any_combined(self, sample_entity):
        """any (OR) combined conditions."""
        cond = WhenCondition(any_=[
            WhenCondition(field="spec.status", equals="planned"),
            WhenCondition(field="spec.status", equals="implemented"),
        ])
        assert evaluate_condition(cond, sample_entity) is True

        cond = WhenCondition(any_=[
            WhenCondition(field="spec.status", equals="planned"),
            WhenCondition(field="spec.status", equals="proposed"),
        ])
        assert evaluate_condition(cond, sample_entity) is False

    def test_condition_from_dict(self):
        """Parse condition from dictionary."""
        data = {
            "field": "spec.status",
            "in": ["implemented", "deprecated"],
        }
        cond = WhenCondition.from_dict(data)
        assert cond.field == "spec.status"
        assert cond.in_ == ["implemented", "deprecated"]

    def test_condition_from_dict_nested(self):
        """Parse nested conditions from dictionary."""
        data = {
            "all": [
                {"field": "spec.status", "equals": "implemented"},
                {"field": "spec.testedIn", "notEquals": "disabled"},
            ]
        }
        cond = WhenCondition.from_dict(data)
        assert cond.all_ is not None
        assert len(cond.all_) == 2

    def test_empty_condition_is_true(self, sample_entity):
        """Empty condition (no constraints) evaluates to True."""
        cond = WhenCondition()
        assert evaluate_condition(cond, sample_entity) is True


# =============================================================================
# Reference Check Tests
# =============================================================================

class TestReferenceCheck:
    """
    Tests for reference check parsing.

    @tests feature:kind-system/verification-references
      - Reference checks defined in verification.references block
      - Supports path and entity-ref types
      - Per-check conditions via when clause
      - Severity configurable per check
    """

    def test_from_dict_simple(self):
        """Parse simple reference check."""
        data = {
            "field": "spec.implementedIn[]",
            "type": "path",
            "severity": "error",
        }
        check = ReferenceCheck.from_dict(data)
        assert check.field == "spec.implementedIn[]"
        assert check.type == "path"
        assert check.severity == "error"
        assert check.when is None

    def test_from_dict_with_condition(self):
        """
        Parse reference check with condition.

        @tests feature:kind-system/verification-references
          - Per-check conditions via when clause
        """
        data = {
            "field": "spec.implementedIn[]",
            "type": "path",
            "severity": "error",
            "when": {
                "field": "spec.implementedIn",
                "notEquals": "disabled",
            }
        }
        check = ReferenceCheck.from_dict(data)
        assert check.when is not None
        assert check.when.field == "spec.implementedIn"
        assert check.when.notEquals == "disabled"


# =============================================================================
# Coverage Config Tests
# =============================================================================

class TestCoverageConfig:
    """
    Tests for coverage configuration parsing.

    @tests feature:kind-system/verification-coverage
      - Coverage defined in verification.coverage block
      - Requirements field path configurable
      - Evidence types with marker and adapter
      - Per-evidence conditions via when clause
    """

    def test_from_dict(self):
        """
        Parse coverage configuration.

        @tests feature:kind-system/verification-coverage
          - Coverage defined in verification.coverage block
          - Requirements field path configurable
          - Evidence types with marker and adapter
          - Per-evidence conditions via when clause
        """
        data = {
            "requirementsField": "spec.acceptance[]",
            "evidence": [
                {
                    "name": "tested",
                    "marker": "@tests",
                    "adapter": "python-test-docstring",
                    "sourcesField": "spec.testedIn[]",
                },
                {
                    "name": "implemented",
                    "marker": "@implements",
                    "adapter": "python-docstring",
                    "sourcesField": "spec.implementedIn[]",
                }
            ]
        }
        config = CoverageConfig.from_dict(data)
        assert config.requirementsField == "spec.acceptance[]"
        assert len(config.evidence) == 2
        assert config.evidence[0].name == "tested"
        assert config.evidence[0].marker == "@tests"


# =============================================================================
# KindDefinition Tests
# =============================================================================

class TestKindDefinition:
    """
    Tests for KindDefinition parsing.

    @tests feature:kind-system/shared-core-module
      - Shared types defined in core.py
      - KindDefinition parsing shared between reconcile and audit

    @tests feature:kind-system/relationships-modeling
      - Relationships defined in separate relationships block
      - Relationship types configurable (depends-on, part-of, implements, extends)
      - Separated from verification (modeling vs checking)
      - No hardcoded kind checks in relationship extraction
    """

    def test_from_dict_new_format(self):
        """
        Parse KindDefinition with new verification format.

        @tests feature:kind-system/shared-core-module
          - Shared types defined in core.py
          - KindDefinition parsing shared between reconcile and audit

        @tests feature:kind-system/relationships-modeling
          - Relationships defined in separate relationships block
          - Relationship types configurable (depends-on, part-of, implements, extends)
          - Separated from verification (modeling vs checking)
          - No hardcoded kind checks in relationship extraction
        """
        doc = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "KindDefinition",
            "metadata": {"name": "Feature"},
            "spec": {
                "category": "behavioral",
                "validation": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"},
                            "acceptance": {"type": "array"},
                        }
                    }
                },
                "verification": {
                    "when": {
                        "field": "spec.status",
                        "in": ["implemented", "deprecated"],
                    },
                    "references": [
                        {
                            "field": "spec.implementedIn[]",
                            "type": "path",
                            "severity": "error",
                        }
                    ],
                    "coverage": {
                        "requirementsField": "spec.acceptance[]",
                        "evidence": [
                            {
                                "name": "tested",
                                "marker": "@tests",
                                "adapter": "python-test-docstring",
                                "sourcesField": "spec.testedIn[]",
                            }
                        ]
                    }
                },
                "relationships": [
                    {"field": "spec.depends-on[]", "type": "depends-on"}
                ]
            }
        }

        kind_def = KindDefinition.from_dict(doc)
        assert kind_def is not None
        assert kind_def.name == "Feature"
        assert kind_def.category == "behavioral"
        assert kind_def.validation is not None
        assert kind_def.verification is not None
        assert kind_def.verification.when is not None
        assert len(kind_def.verification.references) == 1
        assert kind_def.verification.coverage is not None
        assert len(kind_def.relationships) == 1

    def test_get_schema_fields(self):
        """Get field names from schema."""
        doc = {
            "metadata": {"name": "Feature"},
            "spec": {
                "validation": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"},
                            "acceptance": {"type": "array"},
                            "implementedIn": {"type": "array"},
                        }
                    }
                }
            }
        }
        kind_def = KindDefinition.from_dict(doc)
        fields = kind_def.get_schema_fields()
        assert "status" in fields
        assert "acceptance" in fields
        assert "implementedIn" in fields

    def test_get_list_fields(self):
        """Get fields that are arrays."""
        doc = {
            "metadata": {"name": "Feature"},
            "spec": {
                "validation": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"},
                            "acceptance": {"type": "array"},
                            "implementedIn": {
                                "oneOf": [
                                    {"type": "array"},
                                    {"const": "disabled"}
                                ]
                            },
                        }
                    }
                }
            }
        }
        kind_def = KindDefinition.from_dict(doc)
        list_fields = kind_def.get_list_fields()
        assert "status" not in list_fields
        assert "acceptance" in list_fields
        assert "implementedIn" in list_fields  # Has array in oneOf


# =============================================================================
# Entity Indexing Tests
# =============================================================================

class TestEntityIndexing:
    """Tests for entity indexing."""

    def test_index_entities(self):
        """
        Index entities from specs.

        @tests feature:kind-system/shared-core-module
          - Entity indexing shared between tools
          - Condition evaluation shared between tools
        """
        # Create mock KindDefinitions
        kind_defs = {
            "Capability": KindDefinition(name="Capability", category="behavioral"),
            "Feature": KindDefinition(name="Feature", category="behavioral"),
        }

        specs = [
            {
                "kind": "Capability",
                "metadata": {"name": "auth"},
                "spec": {"status": "implemented"},
            },
            {
                "kind": "Feature",
                "metadata": {"name": "auth/login"},
                "spec": {"status": "implemented"},
            },
            {
                "kind": "Feature",
                "metadata": {"name": "auth/logout"},
                "spec": {"status": "planned"},
            },
        ]

        index = index_entities(specs, kind_defs, spec_file="test.yaml")

        assert "capability:auth" in index
        assert "feature:auth/login" in index
        assert "feature:auth/logout" in index

        assert index["feature:auth/login"].ref.parent == "auth"
        assert index["feature:auth/login"].ref.name == "login"

    def test_index_excludes_kind_definitions(self):
        """KindDefinitions are not indexed as entities."""
        # Create mock KindDefinition for Feature
        kind_defs = {
            "Feature": KindDefinition(name="Feature", category="behavioral"),
        }

        specs = [
            {
                "kind": "KindDefinition",
                "metadata": {"name": "Feature"},
                "spec": {},
            },
            {
                "kind": "Feature",
                "metadata": {"name": "test"},
                "spec": {},
            },
        ]

        index = index_entities(specs, kind_defs)
        assert "kinddefinition:feature" not in index.keys()
        assert "feature:test" in index


# =============================================================================
# File Operations Tests
# =============================================================================

class TestFileOperations:
    """Tests for spec file discovery and parsing."""

    def test_find_spec_files(self, tmp_path):
        """Find YAML files in directory."""
        # Create test files
        (tmp_path / "spec").mkdir()
        (tmp_path / "spec" / "test.yaml").write_text("kind: Test")
        (tmp_path / "spec" / "other.yml").write_text("kind: Other")
        (tmp_path / "spec" / "kinds").mkdir()
        (tmp_path / "spec" / "kinds" / "feature.yaml").write_text("kind: KindDefinition")

        # Find files excluding kinds
        files = find_spec_files(str(tmp_path / "spec"), exclude_dirs=["kinds"])

        file_names = [f.name for f in files]
        assert "test.yaml" in file_names
        assert "other.yml" in file_names
        assert "feature.yaml" not in file_names

    def test_parse_spec_file_multi_document(self, tmp_path):
        """Parse multi-document YAML file."""
        content = """
kind: Capability
metadata:
  name: auth
---
kind: Feature
metadata:
  name: auth/login
"""
        spec_file = tmp_path / "auth.yaml"
        spec_file.write_text(content)

        docs = parse_spec_file(spec_file)
        assert len(docs) == 2
        assert docs[0]["kind"] == "Capability"
        assert docs[1]["kind"] == "Feature"


# =============================================================================
# Adapter Registry Tests
# =============================================================================

from projectspec.core import (
    MarkerMatch,
    MarkerAdapter,
    AdapterRegistry,
    PythonDocstringAdapter,
    PythonTestDocstringAdapter,
    MarkdownCommentAdapter,
    get_adapter_registry,
    get_adapter,
    create_default_registry,
    _parse_marker_block,
)


class TestMarkerParsing:
    """
    Tests for marker block parsing.

    @tests feature:reconciliation/criteria-verification
      - Marker format is MARKER entity:name followed by indented criteria list
      - Static parsing, no code execution required
    """

    def test_parse_marker_with_criteria(self):
        """
        Parse marker with indented criteria list.

        @tests feature:reconciliation/criteria-verification
          - Marker format is MARKER entity:name followed by indented criteria list
          - Static parsing, no code execution required
        """
        content = """
@implements feature:auth/login
  - User can log in
  - Session is created
"""
        results = _parse_marker_block(content, "@implements")

        assert len(results) == 1
        entity_ref, criteria = results[0]
        assert entity_ref == "feature:auth/login"
        assert len(criteria) == 2
        assert "User can log in" in criteria
        assert "Session is created" in criteria

    def test_parse_configurable_marker_name(self):
        """
        Marker name is passed as parameter, not hardcoded.

        @tests feature:reconciliation/criteria-verification
          - Marker name is configurable via KindDefinition evidence.marker field
        """
        content = """
@verifies feature:custom/thing
  - Custom criterion
"""
        # Using a custom marker name
        results = _parse_marker_block(content, "@verifies")

        assert len(results) == 1
        assert results[0][0] == "feature:custom/thing"
        assert "Custom criterion" in results[0][1]

    def test_parse_multiple_markers(self):
        """
        Parse multiple marker blocks in same content.

        @tests feature:reconciliation/criteria-verification
          - Markers in code declare which criteria they cover via docstring or comment
        """
        content = """
@implements feature:one
  - First criterion

@implements feature:two
  - Second criterion
"""
        results = _parse_marker_block(content, "@implements")

        assert len(results) == 2
        refs = [r[0] for r in results]
        assert "feature:one" in refs
        assert "feature:two" in refs


class TestAdapterRegistry:
    """
    Tests for marker adapter registry.

    @tests feature:kind-system/verification-coverage
      - Evidence types with marker and adapter
    """

    def test_create_default_registry(self):
        """
        Default registry has all built-in adapters.

        @tests feature:reconciliation/python-docstring-adapter
          - Registered as python-docstring adapter in KindDefinitions

        @tests feature:reconciliation/python-test-docstring-adapter
          - Registered as python-test-docstring adapter in KindDefinitions

        @tests feature:reconciliation/markdown-comment-adapter
          - Registered as markdown-comment adapter in KindDefinitions

        @tests feature:reconciliation/yaml-comment-adapter
          - Registered as yaml-comment adapter in KindDefinitions

        @tests feature:reconciliation/jsdoc-comment-adapter
          - Registered as jsdoc-comment adapter in KindDefinitions
        """
        registry = create_default_registry()

        assert registry.get("python-docstring") is not None
        assert registry.get("python-test-docstring") is not None
        assert registry.get("markdown-comment") is not None
        assert registry.get("yaml-comment") is not None
        assert registry.get("jsdoc-comment") is not None

    def test_list_available_adapters(self):
        """List all registered adapters."""
        registry = create_default_registry()
        available = registry.list_available()

        assert "python-docstring" in available
        assert "python-test-docstring" in available
        assert "markdown-comment" in available
        assert "yaml-comment" in available
        assert "jsdoc-comment" in available

    def test_get_unknown_adapter_returns_none(self):
        """Unknown adapter name returns None."""
        registry = create_default_registry()
        assert registry.get("unknown-adapter") is None

    def test_global_registry(self):
        """Global registry is accessible."""
        registry = get_adapter_registry()
        assert registry is not None
        assert get_adapter("python-docstring") is not None


class TestPythonTestDocstringAdapter:
    """Tests for the Python test docstring adapter."""

    def test_extracts_tests_marker(self, tmp_path):
        """
        Extract markers from test functions.

        @tests feature:reconciliation/python-test-docstring-adapter
          - Parses configurable markers from Python test function docstrings
          - Only scans functions with test_ prefix (pytest convention)
        """
        test_file = tmp_path / "test_example.py"
        test_file.write_text('''
def test_login():
    """
    @tests feature:auth/login
      - User can log in
      - User can log out
    """
    pass

def test_signup():
    """
    @tests feature:auth/signup
      - User can create account
    """
    pass

def helper_function():
    """
    @tests feature:should/not-match
      - This should not be matched
    """
    pass
''')

        adapter = PythonTestDocstringAdapter()
        matches = adapter.extract_markers(test_file, "@tests")

        assert len(matches) == 2

        # Check first match
        login_match = next(m for m in matches if "login" in m.entity_ref)
        assert login_match.entity_ref == "feature:auth/login"
        assert len(login_match.criteria) == 2
        assert "User can log in" in login_match.criteria

        # Check second match
        signup_match = next(m for m in matches if "signup" in m.entity_ref)
        assert signup_match.entity_ref == "feature:auth/signup"
        assert len(signup_match.criteria) == 1


class TestPythonDocstringAdapter:
    """Tests for the Python docstring adapter."""

    def test_extracts_implements_marker(self, tmp_path):
        """
        Extract markers from module/class/function docstrings.

        @tests feature:reconciliation/python-docstring-adapter
          - Parses configurable markers from Python module docstrings
          - Parses configurable markers from Python class docstrings
          - Parses configurable markers from Python function docstrings
        """
        py_file = tmp_path / "auth.py"
        py_file.write_text('''
"""
Module for authentication.

@implements feature:auth/login
  - User can log in
"""

def login():
    """
    @implements feature:auth/login
      - User can log out
    """
    pass

class AuthService:
    """
    @implements feature:auth/service
      - Service handles auth
    """
    pass
''')

        adapter = PythonDocstringAdapter()
        matches = adapter.extract_markers(py_file, "@implements")

        assert len(matches) == 3

        # Module level
        module_match = next(m for m in matches if m.location == "module")
        assert module_match.entity_ref == "feature:auth/login"

        # Function level
        func_match = next(m for m in matches if m.location == "login")
        assert func_match.entity_ref == "feature:auth/login"

        # Class level
        class_match = next(m for m in matches if "class" in m.location)
        assert class_match.entity_ref == "feature:auth/service"


class TestMarkdownCommentAdapter:
    """Tests for the Markdown comment adapter."""

    def test_extracts_implements_from_markdown(self, tmp_path):
        """
        Extract markers from markdown HTML comments.

        @tests feature:reconciliation/markdown-comment-adapter
          - Parses configurable markers from markdown HTML comments
          - Extracts marker blocks from <!-- --> comment syntax
        """
        md_file = tmp_path / "readme.md"
        md_file.write_text('''
# Component

<!-- @implements feature:core/component
  - Component is initialized
  - Component handles events
-->

Implementation details here.
''')

        adapter = MarkdownCommentAdapter()
        matches = adapter.extract_markers(md_file, "@implements")

        assert len(matches) == 1
        assert matches[0].entity_ref == "feature:core/component"
        assert len(matches[0].criteria) == 2
        assert "Component is initialized" in matches[0].criteria
        assert "Component handles events" in matches[0].criteria

    def test_extracts_documents_marker(self, tmp_path):
        """
        Extract markers from HTML comments using different marker names.

        @tests feature:reconciliation/markdown-comment-adapter
          - Parses configurable markers from markdown HTML comments
        """
        md_file = tmp_path / "guide.md"
        md_file.write_text('''
# User Guide

<!-- @documents feature:docs/user-guide
  - Explains how to use the system
  - Includes examples
-->

This is the user guide content.

<!-- @documents feature:docs/api-reference
  - Documents API endpoints
-->

More content here.
''')

        adapter = MarkdownCommentAdapter()
        matches = adapter.extract_markers(md_file, "@documents")

        assert len(matches) == 2

        # First match
        guide_match = next(m for m in matches if "user-guide" in m.entity_ref)
        assert guide_match.entity_ref == "feature:docs/user-guide"
        assert len(guide_match.criteria) == 2

        # Second match
        api_match = next(m for m in matches if "api-reference" in m.entity_ref)
        assert api_match.entity_ref == "feature:docs/api-reference"
        assert len(api_match.criteria) == 1


class TestYamlCommentAdapter:
    """Tests for the YAML comment adapter."""

    def test_extracts_markers_from_yaml_comments(self, tmp_path):
        """
        Extract markers from YAML comment lines.

        @tests feature:reconciliation/yaml-comment-adapter
          - Parses configurable markers from YAML hash comments
          - Works with spec files and other YAML configuration
        """
        from projectspec.core import YamlCommentAdapter

        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text('''
# @implements feature:config/settings
#   - Loads configuration from file
#   - Supports environment overrides

settings:
  debug: true
  port: 8080

# @implements feature:config/database
#   - Database connection settings
database:
  host: localhost
''')

        adapter = YamlCommentAdapter()
        matches = adapter.extract_markers(yaml_file, "@implements")

        assert len(matches) == 2

        # First match - settings
        settings_match = next(m for m in matches if "settings" in m.entity_ref)
        assert settings_match.entity_ref == "feature:config/settings"
        assert len(settings_match.criteria) == 2
        assert "Loads configuration from file" in settings_match.criteria

        # Second match - database
        db_match = next(m for m in matches if "database" in m.entity_ref)
        assert db_match.entity_ref == "feature:config/database"
        assert len(db_match.criteria) == 1

    def test_handles_different_comment_styles(self, tmp_path):
        """
        Handles various YAML comment formatting styles.

        @tests feature:reconciliation/yaml-comment-adapter
          - Parses configurable markers from YAML hash comments
        """
        from projectspec.core import YamlCommentAdapter

        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text('''
#@tests feature:test/compact
#  - No space after hash

# @tests feature:test/spaced
#   - Space after hash

key: value
''')

        adapter = YamlCommentAdapter()
        matches = adapter.extract_markers(yaml_file, "@tests")

        assert len(matches) == 2


class TestJSDocCommentAdapter:
    """Tests for the JSDoc comment adapter."""

    def test_extracts_markers_from_jsdoc(self, tmp_path):
        """
        Extract markers from JSDoc comments.

        @tests feature:reconciliation/jsdoc-comment-adapter
          - Parses configurable markers from JSDoc comments (/** ... */)
          - Cleans JSDoc formatting (removes leading * from lines)
        """
        from projectspec.core import JSDocCommentAdapter

        js_file = tmp_path / "auth.js"
        js_file.write_text('''
/**
 * @implements feature:auth/login
 *   - User can log in with email
 *   - Session token is returned
 */
function login(email, password) {
    return fetch('/api/login', { email, password });
}

/**
 * @implements feature:auth/logout
 *   - Session is invalidated
 */
function logout() {
    return fetch('/api/logout');
}
''')

        adapter = JSDocCommentAdapter()
        matches = adapter.extract_markers(js_file, "@implements")

        assert len(matches) == 2

        # First match - login
        login_match = next(m for m in matches if "login" in m.entity_ref)
        assert login_match.entity_ref == "feature:auth/login"
        assert len(login_match.criteria) == 2
        assert "User can log in with email" in login_match.criteria
        assert "Session token is returned" in login_match.criteria

        # Second match - logout
        logout_match = next(m for m in matches if "logout" in m.entity_ref)
        assert logout_match.entity_ref == "feature:auth/logout"
        assert len(logout_match.criteria) == 1

    def test_works_with_typescript(self, tmp_path):
        """
        Works with TypeScript files.

        @tests feature:reconciliation/jsdoc-comment-adapter
          - Works with JavaScript and TypeScript files
        """
        from projectspec.core import JSDocCommentAdapter

        ts_file = tmp_path / "utils.ts"
        ts_file.write_text('''
/**
 * @tests feature:utils/format
 *   - Formats dates correctly
 */
export function formatDate(date: Date): string {
    return date.toISOString();
}
''')

        adapter = JSDocCommentAdapter()
        matches = adapter.extract_markers(ts_file, "@tests")

        assert len(matches) == 1
        assert matches[0].entity_ref == "feature:utils/format"
        assert "Formats dates correctly" in matches[0].criteria


# =============================================================================
# Tooling Config Tests
# =============================================================================

class TestToolingConfig:
    """Tests for tooling configuration (projectspec.yaml)."""

    def test_load_config_default(self, tmp_path):
        """
        Returns default config when no projectspec.yaml exists.

        @tests feature:reconciliation/tooling-config
          - Reads optional projectspec.yaml from repo root
          - Plain YAML config, no envelope (not a spec entity)
          - Uses convention (spec/kinds/) when no config present
        """
        config = load_config(str(tmp_path))

        assert config.kinds is None
        assert config.ignore == []

    def test_load_config_with_kinds(self, tmp_path):
        """
        Loads kinds path from projectspec.yaml.

        @tests feature:reconciliation/tooling-config
          - Supports kinds field to override KindDefinitions location
        """
        config_file = tmp_path / "projectspec.yaml"
        config_file.write_text("kinds: ./shared/kinds\n")

        config = load_config(str(tmp_path))

        assert config.kinds == "./shared/kinds"
        assert config.ignore == []

    def test_load_config_with_ignore(self, tmp_path):
        """
        Loads ignore patterns from projectspec.yaml.

        @tests feature:reconciliation/tooling-config
          - Supports ignore field to exclude directories from scanning
        """
        config_file = tmp_path / "projectspec.yaml"
        config_file.write_text("ignore:\n  - examples\n  - archive\n")

        config = load_config(str(tmp_path))

        assert config.kinds is None
        assert config.ignore == ["examples", "archive"]

    def test_load_config_full(self, tmp_path):
        """Loads all config fields from projectspec.yaml."""
        config_file = tmp_path / "projectspec.yaml"
        config_file.write_text("""
kinds: ../shared/kinds
ignore:
  - examples
  - vendor
""")

        config = load_config(str(tmp_path))

        assert config.kinds == "../shared/kinds"
        assert config.ignore == ["examples", "vendor"]

    def test_get_kinds_dir_default(self, tmp_path):
        """Uses convention spec/kinds when no config."""
        config = ProjectConfig()
        spec_dir = str(tmp_path / "spec")

        kinds_dir = get_kinds_dir(config, spec_dir)

        assert kinds_dir == str(tmp_path / "spec" / "kinds")

    def test_get_kinds_dir_from_config(self, tmp_path):
        """Uses kinds path from config when provided."""
        config = ProjectConfig(kinds="./shared/kinds")
        spec_dir = str(tmp_path / "spec")

        kinds_dir = get_kinds_dir(config, spec_dir)

        # Resolved relative to repo root (parent of spec_dir)
        assert kinds_dir == str((tmp_path / "shared" / "kinds").resolve())
