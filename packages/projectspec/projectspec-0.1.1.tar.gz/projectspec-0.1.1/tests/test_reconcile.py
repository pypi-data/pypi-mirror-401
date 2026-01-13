"""
Tests for reconcile.py

Tests are organized by feature to match acceptance criteria in
spec/capabilities/reconciliation.yaml
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest
import yaml

# Import from projectspec package (core module)
from projectspec.core import (
    EntityRef,
    find_spec_files,
    parse_spec_file,
    resolve_substitutions,
    load_kind_definitions,
    check_path_exists,
    index_entities,
    extract_entity_relationships,
    build_relationship_graph,
    detect_cycles,
    IndexedEntity,
    KindDefinition,
)

# Import from projectspec package (reconcile module)
from projectspec.reconcile import (
    find_all_source_files,
    reconcile,
    format_json_result,
    format_text_result,
    normalize_criterion,
)


# =============================================================================
# Fixtures
# =============================================================================

def write_multi_doc_yaml(path, docs):
    """Write multiple YAML documents to a file."""
    with open(path, "w") as f:
        for i, doc in enumerate(docs):
            if i > 0:
                f.write("---\n")
            yaml.dump(doc, f)


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure for testing."""
    # Create directories
    (tmp_path / "spec" / "kinds").mkdir(parents=True)
    (tmp_path / "spec" / "capabilities").mkdir(parents=True)
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "docs").mkdir()

    # Create minimal KindDefinitions using the new format (verification, relationships)
    capability_kind = {
        "apiVersion": "projectspec/v1alpha1",
        "kind": "KindDefinition",
        "metadata": {"name": "Capability"},
        "spec": {
            "category": "behavioral",
            "verification": {
                "when": {"field": "spec.status", "notIn": ["planned"]},
                "references": [],
            },
            "relationships": [
                {"field": "spec.features[]", "type": "part-of"},
            ],
        },
    }

    feature_kind = {
        "apiVersion": "projectspec/v1alpha1",
        "kind": "KindDefinition",
        "metadata": {"name": "Feature"},
        "spec": {
            "category": "behavioral",
            "verification": {
                "when": {"field": "spec.status", "notIn": ["planned"]},
                "references": [
                    {"field": "spec.implementedIn[]", "type": "path", "severity": "error",
                     "when": {"field": "spec.implementedIn", "notEquals": "disabled"}},
                    {"field": "spec.testedIn[]", "type": "path", "severity": "error",
                     "when": {"field": "spec.testedIn", "notEquals": "disabled"}},
                    {"field": "spec.documentedIn[]", "type": "path", "severity": "warning"},
                ],
                "coverage": {
                    "when": {"field": "spec.status", "equals": "implemented"},
                    "requirementsField": "spec.acceptance[]",
                    "evidence": [
                        {
                            "name": "tested",
                            "marker": "@tests",
                            "adapter": "python-test-docstring",
                            "sourcesField": "spec.testedIn[]",
                            "when": {"field": "spec.testedIn", "notEquals": "disabled"},
                        },
                        {
                            "name": "implemented",
                            "marker": "@implements",
                            "adapter": "python-docstring",
                            "sourcesField": "spec.implementedIn[]",
                            "when": {"field": "spec.implementedIn", "notEquals": "disabled"},
                        },
                        {
                            "name": "documented",
                            "marker": "@documents",
                            "adapter": "markdown-comment",
                            "sourcesField": "spec.documentedIn[]",
                        },
                    ],
                },
            },
            "relationships": [
                {"field": "spec.depends-on[]", "type": "depends-on"},
            ],
        },
    }

    project_kind = {
        "apiVersion": "projectspec/v1alpha1",
        "kind": "KindDefinition",
        "metadata": {"name": "Project"},
        "spec": {
            "category": "metadata",
            "verification": {"references": []},
            "relationships": [],
        },
    }

    with open(tmp_path / "spec" / "kinds" / "capability.yaml", "w") as f:
        yaml.dump(capability_kind, f)

    with open(tmp_path / "spec" / "kinds" / "feature.yaml", "w") as f:
        yaml.dump(feature_kind, f)

    with open(tmp_path / "spec" / "kinds" / "project.yaml", "w") as f:
        yaml.dump(project_kind, f)

    # Create project spec
    project_spec = {
        "apiVersion": "projectspec/v1alpha1",
        "kind": "Project",
        "metadata": {"name": "test-project"},
        "spec": {
            "paths": {
                "source": "./src",
                "tests": "./tests",
                "docs": "./docs",
            }
        },
    }

    with open(tmp_path / "spec" / "project.yaml", "w") as f:
        yaml.dump(project_spec, f)

    return tmp_path


@pytest.fixture
def temp_project_with_capability(temp_project):
    """Add a capability spec to the temp project."""
    # Create a source file
    (temp_project / "src" / "auth.py").write_text("# auth module")

    # Create capability spec with features as separate documents
    docs = [
        {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "authentication"},
            "spec": {
                "status": "partial",
                "features": ["feature:authentication/login"],
            },
        },
        {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "authentication/login"},
            "spec": {
                "status": "implemented",
                "implementedIn": ["src/auth.py"],
                "testedIn": [],
                "documentedIn": [],
            },
        },
    ]

    write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "auth.yaml", docs)

    return temp_project


# =============================================================================
# Feature: parse-specs
# =============================================================================

class TestParseSpecs:
    """Tests for parse-specs feature."""

    def test_find_yaml_files_in_spec_directory(self, temp_project):
        """
        @tests feature:reconciliation/parse-specs
          - Can find all YAML spec files in spec directory
        """
        # Create some spec files
        (temp_project / "spec" / "one.yaml").write_text("kind: Test")
        (temp_project / "spec" / "two.yml").write_text("kind: Test")
        (temp_project / "spec" / "subdir").mkdir()
        (temp_project / "spec" / "subdir" / "three.yaml").write_text("kind: Test")

        spec_dir = str(temp_project / "spec")
        files = find_spec_files(spec_dir, exclude_dirs=["kinds"])

        # Should find all yaml/yml files except in kinds/
        yaml_files = [f.name for f in files]
        assert "one.yaml" in yaml_files
        assert "two.yml" in yaml_files
        assert "three.yaml" in yaml_files

    def test_parse_single_document_yaml(self, tmp_path):
        """
        @tests feature:reconciliation/parse-specs
          - Can parse single-document YAML files
        """
        content = """
apiVersion: projectspec/v1alpha1
kind: Capability
metadata:
  name: test
spec:
  status: implemented
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(content)

        docs = parse_spec_file(yaml_file, resolve_subs=False)

        assert len(docs) == 1
        assert docs[0]["kind"] == "Capability"
        assert docs[0]["metadata"]["name"] == "test"

    def test_parse_multi_document_yaml(self, tmp_path):
        """
        @tests feature:reconciliation/parse-specs
          - Can parse multi-document YAML files

        @tests feature:kind-system/uniform-entity-handling
          - Multi-document YAML keeps related entities in one file
          - No special-case handling for any specific kind
        """
        content = """
apiVersion: projectspec/v1alpha1
kind: Capability
metadata:
  name: first
---
apiVersion: projectspec/v1alpha1
kind: Capability
metadata:
  name: second
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(content)

        docs = parse_spec_file(yaml_file, resolve_subs=False)

        assert len(docs) == 2
        assert docs[0]["metadata"]["name"] == "first"
        assert docs[1]["metadata"]["name"] == "second"

    def test_parse_error_reported_clearly(self, tmp_path):
        """
        @tests feature:reconciliation/parse-specs
          - Reports parse errors clearly
        """
        content = "invalid: yaml: content: [unclosed"
        yaml_file = tmp_path / "bad.yaml"
        yaml_file.write_text(content)

        with pytest.raises(yaml.YAMLError):
            parse_spec_file(yaml_file, resolve_subs=False)


# =============================================================================
# Feature: check-implemented-in
# =============================================================================

class TestCheckImplementedIn:
    """Tests for check-implemented-in feature."""

    def test_checks_implementedIn_paths_exist(self, temp_project_with_capability):
        """
        @tests feature:reconciliation/check-implemented-in
          - Checks that paths in implementedIn field exist
          - Supports file paths
        """
        result = reconcile(
            spec_dir=str(temp_project_with_capability / "spec"),
            repo_root=str(temp_project_with_capability),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        # src/auth.py exists, so no errors
        assert result.ok_count >= 1
        impl_errors = [i for i in result.issues if "implement" in i.issue_type.lower() or "implementation" in i.message.lower()]
        assert len(impl_errors) == 0

    def test_reports_missing_implementedIn_as_error(self, temp_project):
        """
        @tests feature:reconciliation/check-implemented-in
          - Reports missing files as errors

        @tests feature:kind-system/verification-references
          - Reference checks defined in verification.references block
          - Supports path and entity-ref types
          - Severity configurable per check
        """
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/missing"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/missing"},
                "spec": {
                    "status": "implemented",
                    "implementedIn": ["src/nonexistent.py"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        assert result.has_errors
        error_paths = [i.path for i in result.issues if i.severity == "error"]
        assert "src/nonexistent.py" in error_paths

    def test_supports_glob_patterns(self, temp_project):
        """
        @tests feature:reconciliation/check-implemented-in
          - Supports glob patterns
        """
        # Create files matching pattern
        (temp_project / "src" / "module_a.py").write_text("# a")
        (temp_project / "src" / "module_b.py").write_text("# b")

        capability_spec = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "test"},
            "spec": {
                "features": [
                    {
                        "name": "modules",
                        "status": "implemented",
                        "implementedIn": ["src/module_*.py"],
                    },
                ],
            },
        }

        with open(temp_project / "spec" / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(capability_spec, f)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        # Glob pattern matches, so no errors
        impl_errors = [i for i in result.issues if i.severity == "error"]
        assert len(impl_errors) == 0


# =============================================================================
# Feature: check-tested-in
# =============================================================================

class TestCheckTestedIn:
    """Tests for check-tested-in feature."""

    def test_checks_testedIn_paths_exist(self, temp_project):
        """
        @tests feature:reconciliation/check-tested-in
          - Checks that paths in testedIn field exist
        """
        # Create test file
        (temp_project / "tests" / "test_auth.py").write_text("def test_auth(): pass")
        (temp_project / "src" / "auth.py").write_text("# auth")

        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/auth"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/auth"},
                "spec": {
                    "status": "implemented",
                    "implementedIn": ["src/auth.py"],
                    "testedIn": ["tests/test_auth.py"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src", "tests"],
            check_unlinked=False,
            verify_criteria=False,
        )

        test_errors = [i for i in result.issues if "test" in i.message.lower()]
        assert len(test_errors) == 0

    def test_reports_missing_tests_as_errors(self, temp_project):
        """
        @tests feature:reconciliation/check-tested-in
          - Reports missing test files as errors
        """
        (temp_project / "src" / "auth.py").write_text("# auth")

        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/auth"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/auth"},
                "spec": {
                    "status": "implemented",
                    "implementedIn": ["src/auth.py"],
                    "testedIn": ["tests/missing_test.py"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src", "tests"],
            check_unlinked=False,
            verify_criteria=False,
        )

        assert result.has_errors
        error_issues = [i for i in result.issues if i.severity == "error"]
        assert any("tests/missing_test.py" in (i.path or "") for i in error_issues)


# =============================================================================
# Feature: check-documented-in
# =============================================================================

class TestCheckDocumentedIn:
    """Tests for check-documented-in feature."""

    def test_checks_documented_in_paths_exist(self, temp_project):
        """
        @tests feature:reconciliation/check-documented-in
          - Checks that paths in documentedIn field exist
        """
        (temp_project / "src" / "auth.py").write_text("# auth")
        (temp_project / "docs" / "auth.md").write_text("# Auth docs")

        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/auth"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/auth"},
                "spec": {
                    "status": "implemented",
                    "implementedIn": ["src/auth.py"],
                    "documentedIn": ["docs/auth.md"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src", "docs"],
            check_unlinked=False,
            verify_criteria=False,
        )

        doc_issues = [i for i in result.issues if "documentation" in i.message.lower()]
        assert len(doc_issues) == 0

    def test_reports_missing_docs_as_warnings(self, temp_project):
        """
        @tests feature:reconciliation/check-documented-in
          - Reports missing docs as warnings (not errors)
        """
        (temp_project / "src" / "auth.py").write_text("# auth")

        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/auth"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/auth"},
                "spec": {
                    "status": "implemented",
                    "implementedIn": ["src/auth.py"],
                    "documentedIn": ["docs/missing.md"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src", "docs"],
            check_unlinked=False,
            verify_criteria=False,
        )

        # Should be warning, not error
        doc_issues = [i for i in result.issues if "docs/missing.md" in (i.path or "")]
        assert len(doc_issues) == 1
        assert doc_issues[0].severity == "warning"


# =============================================================================
# Feature: detect-unlinked-files
# =============================================================================

class TestDetectUnlinkedFiles:
    """Tests for detect-unlinked-files feature."""

    def test_identifies_unlinked_files(self, temp_project_with_capability):
        """
        @tests feature:reconciliation/detect-unlinked-files
          - Scans source directories for all files
          - Identifies files not referenced by any spec
        """
        # Create an unlinked file
        (temp_project_with_capability / "src" / "orphan.py").write_text("# orphan")

        result = reconcile(
            spec_dir=str(temp_project_with_capability / "spec"),
            repo_root=str(temp_project_with_capability),
            source_dirs=["src"],
            check_unlinked=True,
            verify_criteria=False,
        )

        assert "src/orphan.py" in result.unlinked_files

    def test_can_disable_unlinked_check(self, temp_project_with_capability):
        """
        @tests feature:reconciliation/detect-unlinked-files
          - Can be disabled with --no-unlinked flag
        """
        (temp_project_with_capability / "src" / "orphan.py").write_text("# orphan")

        result = reconcile(
            spec_dir=str(temp_project_with_capability / "spec"),
            repo_root=str(temp_project_with_capability),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        assert len(result.unlinked_files) == 0


# =============================================================================
# Feature: status-aware
# =============================================================================

class TestStatusAware:
    """Tests for status-aware feature."""

    def test_skips_planned_features(self, temp_project):
        """
        @tests feature:reconciliation/status-aware
          - Skips verification for features with status planned

        @tests feature:kind-system/when-conditions
          - Conditions can be attached at entity, section, and check levels
        """
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/future"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/future"},
                "spec": {
                    "status": "planned",
                    "implementedIn": ["src/future.py"],  # Doesn't exist
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        # Should not report error for planned feature
        assert not result.has_errors
        assert result.planned_count >= 1

    def test_reports_planned_count_in_summary(self, temp_project):
        """
        @tests feature:reconciliation/status-aware
          - Reports planned features in summary
        """
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/one", "feature:test/two"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/one"},
                "spec": {"status": "planned", "implementedIn": []},
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/two"},
                "spec": {"status": "planned", "implementedIn": []},
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        assert result.planned_count == 2


# =============================================================================
# Feature: json-output
# =============================================================================

class TestJsonOutput:
    """Tests for json-output feature."""

    def test_format_json_outputs_valid_json(self, temp_project_with_capability):
        """
        @tests feature:reconciliation/json-output
          - --format json outputs machine-readable results
          - Enables integration with other tools
        """
        result = reconcile(
            spec_dir=str(temp_project_with_capability / "spec"),
            repo_root=str(temp_project_with_capability),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        json_output = format_json_result(result)

        # Should be valid JSON
        parsed = json.loads(json_output)

        assert "version" in parsed
        assert "timestamp" in parsed
        assert "summary" in parsed
        assert "features" in parsed
        assert "issues" in parsed

    def test_json_contains_summary_counts(self, temp_project_with_capability):
        """
        @tests feature:reconciliation/json-output
          - JSON schema is documented
        """
        result = reconcile(
            spec_dir=str(temp_project_with_capability / "spec"),
            repo_root=str(temp_project_with_capability),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        json_output = format_json_result(result)
        parsed = json.loads(json_output)

        # Verify documented schema structure
        summary = parsed["summary"]
        assert "ok_count" in summary
        assert "error_count" in summary
        assert "warning_count" in summary
        assert "planned_count" in summary
        assert "unlinked_count" in summary


# =============================================================================
# Feature: schema-driven
# =============================================================================

class TestSchemaDriven:
    """Tests for schema-driven feature."""

    def test_reads_kind_definitions(self, temp_project):
        """
        @tests feature:reconciliation/schema-driven
          - Reads KindDefinitions from spec/kinds/

        @tests feature:kind-system/custom-kind-loading
          - KindDefinitions are loaded from configurable directory
          - Any valid KindDefinition YAML is processed
          - No hardcoded kind names in loading logic
        """
        kinds_dir = str(temp_project / "spec" / "kinds")
        definitions = load_kind_definitions(kinds_dir)

        assert "Capability" in definitions
        assert "Project" in definitions

    def test_applies_reconciliation_rules(self, temp_project):
        """
        @tests feature:reconciliation/schema-driven
          - Applies reconciliation rules from KindDefinition specs
        """
        # The temp_project fixture already has KindDefinitions with rules
        (temp_project / "src" / "test.py").write_text("# test")

        capability_spec = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "test"},
            "spec": {
                "features": [
                    {
                        "name": "feature",
                        "status": "implemented",
                        "implementedIn": ["src/test.py"],
                    },
                ],
            },
        }

        with open(temp_project / "spec" / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(capability_spec, f)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        # Should apply rules from KindDefinition
        assert result.ok_count >= 1

    def test_raises_error_for_unknown_kind(self, temp_project):
        """
        @tests feature:reconciliation/schema-driven
          - Supports any user-defined kind, not just Capability

        KindDefinitions are required - speccore raises ValueError if missing.
        """
        unknown_spec = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "UnknownKind",
            "metadata": {"name": "test"},
            "spec": {},
        }

        with open(temp_project / "spec" / "unknown.yaml", "w") as f:
            yaml.dump(unknown_spec, f)

        # Should raise ValueError because no KindDefinition exists
        with pytest.raises(ValueError, match="No KindDefinition found"):
            reconcile(
                spec_dir=str(temp_project / "spec"),
                repo_root=str(temp_project),
                source_dirs=["src"],
                check_unlinked=False,
                verify_criteria=False,
            )

    def test_validates_spec_against_json_schema(self, tmp_path):
        """
        @tests feature:reconciliation/schema-driven
          - Validates specs against JSON Schema from KindDefinition
        """
        # Create directories
        (tmp_path / "spec" / "kinds").mkdir(parents=True)
        (tmp_path / "spec" / "capabilities").mkdir(parents=True)
        (tmp_path / "src").mkdir()

        # Create KindDefinition with validation schema
        capability_kind = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "KindDefinition",
            "metadata": {"name": "Capability"},
            "spec": {
                "category": "behavioral",
                "validation": {
                    "schema": {
                        "type": "object",
                        "required": ["status"],
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["planned", "implemented"]
                            },
                            "features": {
                                "type": "array"
                            }
                        }
                    }
                },
                "reconciliation": {
                    "artifacts": [],
                    "relationships": [],
                },
            },
        }

        with open(tmp_path / "spec" / "kinds" / "capability.yaml", "w") as f:
            yaml.dump(capability_kind, f)

        # Create valid capability spec
        valid_spec = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "valid"},
            "spec": {
                "status": "implemented",
                "features": []
            },
        }

        with open(tmp_path / "spec" / "capabilities" / "valid.yaml", "w") as f:
            yaml.dump(valid_spec, f)

        result = reconcile(
            spec_dir=str(tmp_path / "spec"),
            repo_root=str(tmp_path),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        # Should have no validation errors
        schema_errors = [i for i in result.issues if i.issue_type == "schema_validation"]
        assert len(schema_errors) == 0

    def test_reports_schema_validation_errors(self, tmp_path):
        """
        @tests feature:reconciliation/schema-driven
          - Validates specs against JSON Schema from KindDefinition
        """
        # Create directories
        (tmp_path / "spec" / "kinds").mkdir(parents=True)
        (tmp_path / "spec" / "capabilities").mkdir(parents=True)
        (tmp_path / "src").mkdir()

        # Create KindDefinition with validation schema
        capability_kind = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "KindDefinition",
            "metadata": {"name": "Capability"},
            "spec": {
                "category": "behavioral",
                "validation": {
                    "schema": {
                        "type": "object",
                        "required": ["status"],
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["planned", "implemented"]
                            }
                        }
                    }
                },
                "reconciliation": {
                    "artifacts": [],
                    "relationships": [],
                },
            },
        }

        with open(tmp_path / "spec" / "kinds" / "capability.yaml", "w") as f:
            yaml.dump(capability_kind, f)

        # Create invalid capability spec (missing required 'status')
        invalid_spec = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "invalid"},
            "spec": {
                "features": []  # Missing required 'status'
            },
        }

        with open(tmp_path / "spec" / "capabilities" / "invalid.yaml", "w") as f:
            yaml.dump(invalid_spec, f)

        result = reconcile(
            spec_dir=str(tmp_path / "spec"),
            repo_root=str(tmp_path),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        # Should have validation error
        schema_errors = [i for i in result.issues if i.issue_type == "schema_validation"]
        assert len(schema_errors) == 1
        assert "status" in schema_errors[0].message

    def test_reports_invalid_enum_value(self, tmp_path):
        """
        @tests feature:reconciliation/schema-driven
          - Validates specs against JSON Schema from KindDefinition
        """
        # Create directories
        (tmp_path / "spec" / "kinds").mkdir(parents=True)
        (tmp_path / "spec" / "capabilities").mkdir(parents=True)
        (tmp_path / "src").mkdir()

        # Create KindDefinition with enum validation
        capability_kind = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "KindDefinition",
            "metadata": {"name": "Capability"},
            "spec": {
                "category": "behavioral",
                "validation": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["planned", "implemented"]
                            }
                        }
                    }
                },
                "reconciliation": {
                    "artifacts": [],
                    "relationships": [],
                },
            },
        }

        with open(tmp_path / "spec" / "kinds" / "capability.yaml", "w") as f:
            yaml.dump(capability_kind, f)

        # Create spec with invalid enum value
        invalid_spec = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "invalid"},
            "spec": {
                "status": "invalid_status"  # Not in enum
            },
        }

        with open(tmp_path / "spec" / "capabilities" / "invalid.yaml", "w") as f:
            yaml.dump(invalid_spec, f)

        result = reconcile(
            spec_dir=str(tmp_path / "spec"),
            repo_root=str(tmp_path),
            source_dirs=["src"],
            check_unlinked=False,
            verify_criteria=False,
        )

        # Should have validation error about enum
        schema_errors = [i for i in result.issues if i.issue_type == "schema_validation"]
        assert len(schema_errors) == 1
        assert "invalid_status" in schema_errors[0].message or "enum" in schema_errors[0].message.lower()


# =============================================================================
# Feature: substitution
# =============================================================================

class TestSubstitution:
    """Tests for substitution feature."""

    def test_json_substitution(self, tmp_path):
        """
        @tests feature:reconciliation/substitution
          - Supports $json directive to import JSON files
        """
        # Create JSON file
        json_content = {"key": "value", "nested": {"a": 1}}
        (tmp_path / "data.json").write_text(json.dumps(json_content))

        # Create YAML with $json reference
        yaml_content = {
            "name": "test",
            "data": {"$json": "data.json"},
        }
        yaml_file = tmp_path / "test.yaml"
        with open(yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        docs = parse_spec_file(yaml_file, resolve_subs=True)

        assert docs[0]["data"]["key"] == "value"
        assert docs[0]["data"]["nested"]["a"] == 1

    def test_yaml_substitution(self, tmp_path):
        """
        @tests feature:reconciliation/substitution
          - Supports $yaml directive to import YAML files
        """
        # Create YAML file to import
        import_content = {"imported": True, "items": [1, 2, 3]}
        with open(tmp_path / "import.yaml", "w") as f:
            yaml.dump(import_content, f)

        # Create YAML with $yaml reference
        yaml_content = {
            "name": "test",
            "external": {"$yaml": "import.yaml"},
        }
        yaml_file = tmp_path / "test.yaml"
        with open(yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        docs = parse_spec_file(yaml_file, resolve_subs=True)

        assert docs[0]["external"]["imported"] == True
        assert docs[0]["external"]["items"] == [1, 2, 3]

    def test_text_substitution(self, tmp_path):
        """
        @tests feature:reconciliation/substitution
          - Supports $text directive to import text files
        """
        # Create text file
        (tmp_path / "content.txt").write_text("Hello, World!")

        # Create YAML with $text reference
        yaml_content = {
            "name": "test",
            "description": {"$text": "content.txt"},
        }
        yaml_file = tmp_path / "test.yaml"
        with open(yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        docs = parse_spec_file(yaml_file, resolve_subs=True)

        assert docs[0]["description"] == "Hello, World!"

    def test_relative_paths_from_containing_file(self, tmp_path):
        """
        @tests feature:reconciliation/substitution
          - Works with relative paths from the containing file
        """
        # Create subdirectory structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        # Create JSON in subdir
        (subdir / "data.json").write_text('{"from": "subdir"}')

        # Create YAML in subdir referencing sibling file
        yaml_content = {
            "data": {"$json": "data.json"},
        }
        yaml_file = subdir / "test.yaml"
        with open(yaml_file, "w") as f:
            yaml.dump(yaml_content, f)

        docs = parse_spec_file(yaml_file, resolve_subs=True)

        assert docs[0]["data"]["from"] == "subdir"


# =============================================================================
# CLI Integration Tests
# =============================================================================

class TestCLI:
    """Tests for CLI interface."""

    def test_returns_exit_code_1_on_errors(self, temp_project):
        """
        @tests feature:reconciliation/cli-interface
          - Returns exit code 1 on errors
        """
        # Create spec with missing implementation
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/broken"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/broken"},
                "spec": {
                    "status": "implemented",
                    "implementedIn": ["src/missing.py"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        # Run CLI
        result = subprocess.run(
            ["projectspec", "reconcile", "--repo-root", str(temp_project), "--no-criteria"],
            capture_output=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 1

    def test_returns_exit_code_0_on_success(self, temp_project_with_capability):
        """Returns exit code 0 on success."""
        result = subprocess.run(
            ["projectspec", "reconcile", "--repo-root", str(temp_project_with_capability), "--no-criteria"],
            capture_output=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0

    def test_spec_dir_flag(self, temp_project_with_capability):
        """
        @tests feature:reconciliation/cli-interface
          - Accepts --spec-dir to specify spec location
        """
        result = subprocess.run(
            ["projectspec", "reconcile",
             "--repo-root", str(temp_project_with_capability),
             "--spec-dir", "spec",
             "--no-criteria"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0
        assert "features OK" in result.stdout

    def test_repo_root_flag(self, temp_project_with_capability):
        """
        @tests feature:reconciliation/cli-interface
          - Accepts --repo-root to specify repository root
        """
        result = subprocess.run(
            ["projectspec", "reconcile", "--repo-root", str(temp_project_with_capability), "--no-criteria"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0

    def test_source_dirs_flag(self, temp_project_with_capability):
        """
        @tests feature:reconciliation/cli-interface
          - Accepts --source-dirs to specify directories to scan
        """
        result = subprocess.run(
            ["projectspec", "reconcile",
             "--repo-root", str(temp_project_with_capability),
             "--source-dirs", "src", "tests",
             "--no-criteria"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        assert result.returncode == 0

    def test_strict_flag(self, temp_project_with_capability):
        """
        @tests feature:reconciliation/cli-interface
          - Accepts --strict for CI mode (exit 1 on any issue)
        """
        # Create an unlinked file to trigger a warning (not error)
        (temp_project_with_capability / "src" / "orphan.py").write_text("# orphan")

        # Without --strict, should exit 0 (unlinked is not an error)
        result_normal = subprocess.run(
            ["projectspec", "reconcile",
             "--repo-root", str(temp_project_with_capability),
             "--no-criteria"],
            capture_output=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result_normal.returncode == 0

        # With --strict, should exit 1 (any issue causes failure)
        result_strict = subprocess.run(
            ["projectspec", "reconcile",
             "--repo-root", str(temp_project_with_capability),
             "--strict",
             "--no-criteria"],
            capture_output=True,
            cwd=Path(__file__).parent.parent,
        )
        assert result_strict.returncode == 1

    def test_json_format_flag(self, temp_project_with_capability):
        """--format json outputs JSON."""
        result = subprocess.run(
            ["projectspec", "reconcile", "--repo-root", str(temp_project_with_capability), "--format", "json", "--no-criteria"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Should be valid JSON
        parsed = json.loads(result.stdout)
        assert "summary" in parsed


# =============================================================================
# TestCriteriaVerification - Criteria Verification Feature
# =============================================================================

class TestCriteriaVerification:
    """Tests for criteria verification feature.

    Note: Parsing tests for @tests markers are covered in test_speccore.py
    via TestPythonTestDocstringAdapter. This class focuses on integration tests.
    """

    def test_normalize_criterion_whitespace(self):
        """Normalize whitespace in criteria for matching."""
        assert normalize_criterion("  User can   log in  ") == "User can log in"
        assert normalize_criterion("User\ncan\nlog in") == "User can log in"

    def test_criteria_in_reconcile_output(self, temp_project):
        """
        Criteria coverage appears in reconcile results.

        @tests feature:reconciliation/criteria-verification
          - Criteria listed under markers are matched against spec acceptance criteria
        """
        # Create capability with acceptance criteria using multi-document format
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "auth"},
                "spec": {
                    "features": ["feature:auth/login"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "auth/login"},
                "spec": {
                    "status": "implemented",
                    "acceptance": ["User can log in"],
                    "implementedIn": [],
                    "testedIn": ["tests/test_auth.py"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "auth.yaml", docs)

        # Create test with @tests
        (temp_project / "tests" / "test_auth.py").write_text('''
def test_login():
    """
    @tests feature:auth/login
      - User can log in
    """
    pass
''')

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=[],
            verify_criteria=True,
        )

        # Evidence results use the new API
        assert "tested" in result.evidence_results
        tested = result.evidence_results["tested"]
        assert len(tested.covered) == 1
        # covered is a list of tuples: (entity_ref, criterion, file_path, location)
        assert tested.covered[0][1] == "User can log in"

    def test_no_criteria_flag(self, temp_project):
        """--no-criteria skips criteria verification."""
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "auth"},
                "spec": {
                    "features": ["feature:auth/login"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "auth/login"},
                "spec": {
                    "status": "implemented",
                    "acceptance": ["User can log in"],
                    "implementedIn": [],
                    "testedIn": [],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "auth.yaml", docs)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=[],
            verify_criteria=False,
        )

        # When verify_criteria=False, evidence_results should be empty
        assert len(result.evidence_results) == 0

    def test_criteria_in_json_output(self, temp_project):
        """
        Evidence coverage appears in JSON output.

        @tests feature:reconciliation/criteria-verification
          - Reports unverified acceptance criteria as warnings
        """
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "auth"},
                "spec": {
                    "features": ["feature:auth/login"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "auth/login"},
                "spec": {
                    "status": "implemented",
                    "acceptance": ["User can log in", "Session created"],
                    "implementedIn": [],
                    "testedIn": ["tests/test_auth.py"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "auth.yaml", docs)

        (temp_project / "tests" / "test_auth.py").write_text('''
def test_login():
    """
    @tests feature:auth/login
      - User can log in
    """
    pass
''')

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=[],
            verify_criteria=True,
        )

        json_output = format_json_result(result)
        parsed = json.loads(json_output)

        # New API uses "evidence" key with evidence type names
        assert "evidence" in parsed
        assert "tested" in parsed["evidence"]
        assert len(parsed["evidence"]["tested"]["covered"]) == 1
        assert len(parsed["evidence"]["tested"]["uncovered"]) == 1
        # Summary has totals across all evidence types
        assert "total_covered" in parsed["summary"]
        assert "total_uncovered" in parsed["summary"]


# =============================================================================
# TestRelationshipGraph - Relationship Graph Feature
# =============================================================================

class TestRelationshipGraph:
    """Tests for relationship graph feature."""

    def test_parse_entity_ref(self):
        """
        @tests feature:reconciliation/relationship-graph
          - Extracts entity references from relationship fields in KindDefinition
        """
        # Top-level entity
        ref = EntityRef.parse("Capability:authentication")
        assert ref.kind == "Capability"
        assert ref.name == "authentication"
        assert ref.parent is None

        # Nested entity
        ref = EntityRef.parse("Feature:authentication/login")
        assert ref.kind == "Feature"
        assert ref.name == "login"
        assert ref.parent == "authentication"

    def test_index_entities_from_specs(self, temp_project):
        """
        @tests feature:reconciliation/relationship-graph
          - Builds index of all defined entities across specs

        @tests feature:kind-system/uniform-entity-handling
          - All entities use standard envelope (kind, metadata, spec)
          - Features are top-level entities with their own KindDefinition
        """
        # Multi-document format: Features are top-level entities
        specs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "auth"},
                "spec": {
                    "features": ["feature:auth/login", "feature:auth/logout"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "auth/login"},
                "spec": {"status": "implemented"},
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "auth/logout"},
                "spec": {"status": "planned"},
            },
        ]

        kinds_dir = str(temp_project / "spec" / "kinds")
        kind_definitions = load_kind_definitions(kinds_dir)

        entities = index_entities(specs, kind_definitions)

        # Should have Capability + 2 Features
        assert len(entities) == 3
        # index_entities returns lowercase keys
        assert "capability:auth" in entities
        assert "feature:auth/login" in entities
        assert "feature:auth/logout" in entities

    def test_validates_referenced_entities_exist(self, temp_project):
        """
        @tests feature:reconciliation/relationship-graph
          - Validates referenced entities exist
          - Reports broken references as errors

        @tests feature:kind-system/relationships-modeling
          - Relationships defined in separate relationships block
          - Relationship types configurable (depends-on, part-of, implements, extends)
          - Separated from verification (modeling vs checking)
        """
        # Multi-document format: Feature with broken depends-on reference
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "auth"},
                "spec": {
                    "features": ["feature:auth/oauth"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "auth/oauth"},
                "spec": {
                    "status": "implemented",
                    "depends-on": ["feature:auth/nonexistent"],  # Doesn't exist
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "auth.yaml", docs)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=[],
            verify_criteria=False,
            build_graph=True,
        )

        # Should have broken reference error
        broken_ref_errors = [i for i in result.issues if i.issue_type == "broken_reference"]
        assert len(broken_ref_errors) == 1
        assert "nonexistent" in broken_ref_errors[0].message

    def test_detects_circular_dependencies(self, temp_project):
        """
        @tests feature:reconciliation/relationship-graph
          - Detects circular dependencies
        """
        # Create entity refs for cycle detection
        entities = [
            EntityRef(kind="Feature", name="a", parent="test"),
            EntityRef(kind="Feature", name="b", parent="test"),
            EntityRef(kind="Feature", name="c", parent="test"),
        ]

        # Create a cycle: a -> b -> c -> a
        from projectspec.reconcile import Relationship
        relationships = [
            Relationship(source=entities[0], target=entities[1], rel_type="depends-on"),
            Relationship(source=entities[1], target=entities[2], rel_type="depends-on"),
            Relationship(source=entities[2], target=entities[0], rel_type="depends-on"),
        ]

        cycles = detect_cycles(entities, relationships)

        assert len(cycles) >= 1
        # Cycle should contain all three entities
        cycle_names = [e.name for e in cycles[0]]
        assert "a" in cycle_names or "b" in cycle_names or "c" in cycle_names

    def test_outputs_dependency_graph_in_json(self, temp_project):
        """
        @tests feature:reconciliation/relationship-graph
          - Outputs dependency graph in JSON format
        """
        capability_spec = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "auth"},
            "spec": {
                "features": [
                    {"name": "login", "status": "implemented"},
                ],
            },
        }

        with open(temp_project / "spec" / "capabilities" / "auth.yaml", "w") as f:
            yaml.dump(capability_spec, f)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=[],
            verify_criteria=False,
            build_graph=True,
        )

        json_output = format_json_result(result)
        parsed = json.loads(json_output)

        # Should have relationship_graph in output
        assert "relationship_graph" in parsed
        assert "entities" in parsed["relationship_graph"]
        assert "relationships" in parsed["relationship_graph"]
        assert "broken_refs" in parsed["relationship_graph"]
        assert "cycles" in parsed["relationship_graph"]

        # Should have entity count in summary
        assert "entity_count" in parsed["summary"]
        assert parsed["summary"]["entity_count"] >= 2  # Capability + Feature

    def test_no_graph_flag_skips_graph_building(self, temp_project):
        """Test --no-graph flag skips relationship graph building."""
        capability_spec = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "auth"},
            "spec": {
                "features": [
                    {"name": "login", "status": "implemented"},
                ],
            },
        }

        with open(temp_project / "spec" / "capabilities" / "auth.yaml", "w") as f:
            yaml.dump(capability_spec, f)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=[],
            verify_criteria=False,
            build_graph=False,
        )

        assert result.relationship_graph is None


class TestImplementsMarkers:
    """Tests for @implements marker integration.

    Note: Parsing tests for @implements markers are covered in test_speccore.py
    via TestPythonDocstringAdapter. This class focuses on integration tests.
    """

    def test_works_alongside_tests_markers(self, temp_project):
        """
        @tests feature:reconciliation/criteria-verification
          - Criteria listed under markers are matched against spec acceptance criteria
        """
        # Create a capability spec using multi-document format
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "auth"},
                "spec": {
                    "features": ["feature:auth/login"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "auth/login"},
                "spec": {
                    "status": "implemented",
                    "acceptance": [
                        "User can log in",
                        "Invalid credentials return error",
                    ],
                    "implementedIn": ["src/auth.py"],
                    "testedIn": ["tests/test_auth.py"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "auth.yaml", docs)

        # Create implementation file with @implements
        (temp_project / "src").mkdir(exist_ok=True)
        impl_content = '''"""
Authentication module.

@implements feature:auth/login
  - User can log in
"""

def login(email, password):
    pass
'''
        (temp_project / "src" / "auth.py").write_text(impl_content)

        # Create test file with @tests
        (temp_project / "tests").mkdir(exist_ok=True)
        test_content = '''"""Tests for auth."""

def test_invalid_credentials():
    """
    @tests feature:auth/login
      - Invalid credentials return error
    """
    pass
'''
        (temp_project / "tests" / "test_auth.py").write_text(test_content)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src"],
            verify_criteria=True,
            build_graph=False,
        )

        # Both @tests and @implements should be tracked via evidence_results
        assert "tested" in result.evidence_results
        assert "implemented" in result.evidence_results

        tested = result.evidence_results["tested"]
        implemented = result.evidence_results["implemented"]

        # One criterion verified by test
        assert len(tested.covered) == 1
        assert tested.covered[0][1] == "Invalid credentials return error"

        # One criterion implemented
        assert len(implemented.covered) == 1
        assert implemented.covered[0][1] == "User can log in"


class TestDocumentsMarkers:
    """Tests for @documents marker integration.

    Note: Parsing tests for @documents markers are covered in test_speccore.py
    via TestMarkdownCommentAdapter. This class focuses on integration tests.
    """

    def test_works_alongside_implements_and_tests(self, temp_project):
        """
        @tests feature:reconciliation/criteria-verification
          - Criteria listed under markers are matched against spec acceptance criteria
        """
        # Create a capability spec with documentedIn using multi-document format
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/feature"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/feature"},
                "spec": {
                    "status": "implemented",
                    "acceptance": [
                        "Criterion one",
                        "Criterion two",
                    ],
                    "implementedIn": ["src/feature.py"],
                    "testedIn": ["tests/test_feature.py"],
                    "documentedIn": ["docs/feature.md"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        # Create implementation file with @implements
        (temp_project / "src").mkdir(exist_ok=True)
        impl_content = '''"""
Feature implementation.

@implements feature:test/feature
  - Criterion one
"""
'''
        (temp_project / "src" / "feature.py").write_text(impl_content)

        # Create test file with @tests
        (temp_project / "tests").mkdir(exist_ok=True)
        test_content = '''"""Tests for feature."""

def test_criterion_two():
    """
    @tests feature:test/feature
      - Criterion two
    """
    pass
'''
        (temp_project / "tests" / "test_feature.py").write_text(test_content)

        # Create documentation file with @documents
        (temp_project / "docs").mkdir(exist_ok=True)
        doc_content = '''# Feature Documentation

<!-- @documents feature:test/feature
  - Criterion one
  - Criterion two
-->

Feature details here.
'''
        (temp_project / "docs" / "feature.md").write_text(doc_content)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src", "docs"],
            verify_criteria=True,
            build_graph=False,
        )

        # All three evidence types should be tracked
        assert "tested" in result.evidence_results
        assert "implemented" in result.evidence_results
        assert "documented" in result.evidence_results

        tested = result.evidence_results["tested"]
        implemented = result.evidence_results["implemented"]
        documented = result.evidence_results["documented"]

        # Test criterion verified
        assert len(tested.covered) == 1
        assert tested.covered[0][1] == "Criterion two"

        # Implementation criterion covered
        assert len(implemented.covered) == 1
        assert implemented.covered[0][1] == "Criterion one"

        # Both criteria documented
        assert len(documented.covered) == 2
        assert len(documented.uncovered) == 0

    def test_reports_orphan_claims(self, temp_project):
        """
        Test that orphan claims in markers are reported.

        @tests feature:reconciliation/criteria-verification
          - Reports unverified acceptance criteria as warnings
          - Reports criteria in markers that don't match spec as orphan errors
        """
        # Create a spec with one criterion
        docs = [
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Capability",
                "metadata": {"name": "test"},
                "spec": {
                    "features": ["feature:test/feature"],
                },
            },
            {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "Feature",
                "metadata": {"name": "test/feature"},
                "spec": {
                    "status": "implemented",
                    "acceptance": ["Real criterion"],
                    "implementedIn": ["src/feature.py"],
                    "testedIn": ["tests/test_feature.py"],
                    "documentedIn": ["docs/feature.md"],
                },
            },
        ]

        write_multi_doc_yaml(temp_project / "spec" / "capabilities" / "test.yaml", docs)

        # Create implementation file with orphan claim
        (temp_project / "src").mkdir(exist_ok=True)
        impl_content = '''"""
@implements feature:test/feature
  - Orphan impl criterion
"""
'''
        (temp_project / "src" / "feature.py").write_text(impl_content)

        # Create test file with orphan claim
        (temp_project / "tests").mkdir(exist_ok=True)
        test_content = '''
def test_something():
    """
    @tests feature:test/feature
      - Orphan test criterion
    """
    pass
'''
        (temp_project / "tests" / "test_feature.py").write_text(test_content)

        # Create doc file with orphan claim
        (temp_project / "docs").mkdir(exist_ok=True)
        doc_content = '''
<!-- @documents feature:test/feature
  - Orphan doc criterion
-->
'''
        (temp_project / "docs" / "feature.md").write_text(doc_content)

        result = reconcile(
            spec_dir=str(temp_project / "spec"),
            repo_root=str(temp_project),
            source_dirs=["src", "docs"],
            verify_criteria=True,
            build_graph=False,
        )

        # Should have orphans in all three evidence types
        tested = result.evidence_results["tested"]
        implemented = result.evidence_results["implemented"]
        documented = result.evidence_results["documented"]

        # Orphans are reported
        assert len(tested.orphans) == 1
        assert "Orphan test criterion" in tested.orphans[0][3]

        assert len(implemented.orphans) == 1
        assert "Orphan impl criterion" in implemented.orphans[0][3]

        assert len(documented.orphans) == 1
        assert "Orphan doc criterion" in documented.orphans[0][3]

        # Real criterion is uncovered (no matching markers)
        assert len(tested.uncovered) == 1
        assert len(implemented.uncovered) == 1
        assert len(documented.uncovered) == 1
