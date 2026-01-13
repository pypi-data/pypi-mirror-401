"""
Tests for audit.py - Spec Audit feature

Tests are organized to match acceptance criteria in
spec/capabilities/ci-integration.yaml
"""

import json
from pathlib import Path

import pytest
import yaml

# Import from projectspec package
from projectspec.audit import (
    audit_specs,
    load_and_index_specs,
    diff_specs,
    diff_entity,
    get_ordinal_config,
    is_ordinal_regression,
    get_requirements_field,
    get_relationship_fields,
    format_text_audit,
    format_json_audit,
    compute_summary,
    EntityChange,
    FieldChange,
    AuditResult,
    AuditSummary,
)
from projectspec.core import (
    KindDefinition,
    AuditConfig,
    OrdinalConfig,
    VerificationConfig,
    CoverageConfig,
    RelationshipDefinition,
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


def create_kind_definitions(spec_dir):
    """Create KindDefinitions with audit section for testing."""
    (spec_dir / "kinds").mkdir(parents=True, exist_ok=True)

    # Feature KindDefinition with audit section
    feature_kind = {
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
                        "acceptance": {"type": "array", "items": {"type": "string"}},
                        "implementedIn": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "verification": {
                "coverage": {
                    "requirementsField": "spec.acceptance[]",
                },
            },
            "audit": {
                "ordinals": [{
                    "field": "spec.status",
                    "progression": ["proposed", "planned", "partial", "implemented"],
                    "terminal": ["deprecated"],
                }]
            },
        },
    }
    with open(spec_dir / "kinds" / "feature.yaml", "w") as f:
        yaml.dump(feature_kind, f)

    # Capability KindDefinition with audit section
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
                        "status": {"type": "string"},
                        "features": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "audit": {
                "ordinals": [{
                    "field": "spec.status",
                    "progression": ["proposed", "planned", "partial", "implemented"],
                    "terminal": ["deprecated"],
                }]
            },
        },
    }
    with open(spec_dir / "kinds" / "capability.yaml", "w") as f:
        yaml.dump(capability_kind, f)


@pytest.fixture
def base_spec_dir(tmp_path):
    """Create a base spec directory for testing."""
    base = tmp_path / "base" / "spec"
    (base / "capabilities").mkdir(parents=True)

    # Create KindDefinitions with audit section
    create_kind_definitions(base)

    # Create a capability with features as separate documents
    docs = [
        {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "auth"},
            "spec": {
                "status": "partial",
                "features": [
                    "feature:auth/login",
                    "feature:auth/logout",
                ],
            },
        },
        {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "auth/login"},
            "spec": {
                "status": "implemented",
                "acceptance": [
                    "User can log in with email",
                    "Session token returned",
                ],
                "implementedIn": ["src/auth.py"],
            },
        },
        {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "auth/logout"},
            "spec": {
                "status": "implemented",
                "acceptance": ["User can log out"],
            },
        },
    ]

    write_multi_doc_yaml(base / "capabilities" / "auth.yaml", docs)

    return base


@pytest.fixture
def head_spec_dir(tmp_path):
    """Create a head spec directory (modified version) for testing."""
    head = tmp_path / "head" / "spec"
    (head / "capabilities").mkdir(parents=True)

    # Create KindDefinitions with audit section
    create_kind_definitions(head)

    # Modified capability - changes from base:
    # - login status: implemented -> partial (regression)
    # - login acceptance: removed "Session token returned", added "OAuth supported"
    # - logout: removed entirely
    # - oauth: added (new feature)
    docs = [
        {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "auth"},
            "spec": {
                "status": "partial",
                "features": [
                    "feature:auth/login",
                    "feature:auth/oauth",
                ],
            },
        },
        {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "auth/login"},
            "spec": {
                "status": "partial",
                "acceptance": [
                    "User can log in with email",
                    "OAuth supported",
                ],
                "implementedIn": ["src/auth.py"],
            },
        },
        {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "auth/oauth"},
            "spec": {
                "status": "planned",
                "acceptance": ["User can authenticate via Google"],
            },
        },
    ]

    write_multi_doc_yaml(head / "capabilities" / "auth.yaml", docs)

    return head


# =============================================================================
# Test: Detects changes to spec files between base and head
# =============================================================================

class TestDetectsChanges:
    """Tests for detecting changes between base and head specs."""

    def test_detects_added_entity(self, tmp_path):
        """
        @tests feature:ci-integration/spec-audit
          - Detects changes to spec files between base and head

        @tests feature:kind-system/audit-schema-driven
          - Audit tool uses speccore for entity indexing
        """
        # Base: empty (but with KindDefinitions)
        base = tmp_path / "base" / "spec"
        (base / "capabilities").mkdir(parents=True)
        create_kind_definitions(base)

        # Head: one capability with feature
        head = tmp_path / "head" / "spec"
        (head / "capabilities").mkdir(parents=True)
        create_kind_definitions(head)

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
                "spec": {"status": "planned"},
            },
        ]
        write_multi_doc_yaml(head / "capabilities" / "auth.yaml", docs)

        result = audit_specs(str(base), str(head))

        # Should detect added entities
        assert result.summary.entities_added >= 1
        added_refs = [c.entity_ref for c in result.changes if c.change_type == "added"]
        assert "capability:auth" in added_refs or "feature:auth/login" in added_refs

    def test_detects_removed_entity(self, tmp_path):
        """
        @tests feature:ci-integration/spec-audit
          - Detects changes to spec files between base and head
        """
        # Base: one capability with feature
        base = tmp_path / "base" / "spec"
        (base / "capabilities").mkdir(parents=True)
        create_kind_definitions(base)

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
                "spec": {"status": "implemented"},
            },
        ]
        write_multi_doc_yaml(base / "capabilities" / "auth.yaml", docs)

        # Head: empty (but with KindDefinitions)
        head = tmp_path / "head" / "spec"
        (head / "capabilities").mkdir(parents=True)
        create_kind_definitions(head)

        result = audit_specs(str(base), str(head))

        # Should detect removed entities
        assert result.summary.entities_removed >= 1
        removed_refs = [c.entity_ref for c in result.changes if c.change_type == "removed"]
        assert len(removed_refs) >= 1

    def test_detects_modified_entity(self, base_spec_dir, head_spec_dir):
        """
        @tests feature:ci-integration/spec-audit
          - Detects changes to spec files between base and head
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))

        # Should detect modifications
        assert result.summary.entities_modified >= 1
        modified = [c for c in result.changes if c.change_type == "modified"]
        assert len(modified) >= 1

    def test_no_changes_when_identical(self, base_spec_dir):
        """No changes detected when comparing identical specs."""
        result = audit_specs(str(base_spec_dir), str(base_spec_dir))

        assert result.summary.entities_added == 0
        assert result.summary.entities_removed == 0
        assert result.summary.entities_modified == 0
        assert len(result.changes) == 0


# =============================================================================
# Test: Reports what changed (added, removed, modified features)
# =============================================================================

class TestReportsFeatureChanges:
    """Tests for reporting feature-level changes."""

    def test_reports_added_feature(self, base_spec_dir, head_spec_dir):
        """
        @tests feature:ci-integration/spec-audit
          - Reports what changed (added, removed, modified features)
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))

        # Head has oauth feature that base doesn't
        added = [c for c in result.changes if c.change_type == "added"]
        added_refs = [c.entity_ref for c in added]

        assert "feature:auth/oauth" in added_refs
        assert result.summary.added_by_kind.get("Feature", 0) >= 1

    def test_reports_removed_feature(self, base_spec_dir, head_spec_dir):
        """
        @tests feature:ci-integration/spec-audit
          - Reports what changed (added, removed, modified features)
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))

        # Base has logout feature that head doesn't
        removed = [c for c in result.changes if c.change_type == "removed"]
        removed_refs = [c.entity_ref for c in removed]

        assert "feature:auth/logout" in removed_refs
        assert result.summary.removed_by_kind.get("Feature", 0) >= 1

    def test_reports_modified_feature(self, base_spec_dir, head_spec_dir):
        """
        @tests feature:ci-integration/spec-audit
          - Reports what changed (added, removed, modified features)
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))

        # login feature was modified
        modified = [c for c in result.changes if c.change_type == "modified"]
        modified_refs = [c.entity_ref for c in modified]

        assert "feature:auth/login" in modified_refs

    def test_reports_acceptance_criteria_changes(self, base_spec_dir, head_spec_dir):
        """
        Reports added and removed acceptance criteria.

        @tests feature:kind-system/audit-schema-driven
          - Field comparison driven by KindDefinition schema when available
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))

        # login feature had criteria changes
        login_change = next(
            c for c in result.changes
            if c.entity_ref == "feature:auth/login" and c.change_type == "modified"
        )

        acceptance_change = next(
            fc for fc in login_change.field_changes
            if fc.field == "acceptance"
        )

        assert "Session token returned" in acceptance_change.items_removed
        assert "OAuth supported" in acceptance_change.items_added


# =============================================================================
# Test: Reports status changes (e.g., implemented to planned)
# =============================================================================

class TestReportsStatusChanges:
    """Tests for reporting status changes."""

    def test_detects_status_change(self, base_spec_dir, head_spec_dir):
        """
        @tests feature:ci-integration/spec-audit
          - Reports status changes (e.g., implemented to planned)
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))

        login_change = next(
            c for c in result.changes
            if c.entity_ref == "feature:auth/login"
        )

        status_change = next(
            fc for fc in login_change.field_changes
            if fc.field == "status"
        )

        assert status_change.old_value == "implemented"
        assert status_change.new_value == "partial"

    def test_detects_status_regression(self, base_spec_dir, head_spec_dir):
        """
        @tests feature:ci-integration/spec-audit
          - Reports status changes (e.g., implemented to planned)
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))

        # implemented -> partial is a regression (counted in ordinal_regressions)
        assert result.summary.ordinal_regressions >= 1

        login_change = next(
            c for c in result.changes
            if c.entity_ref == "feature:auth/login"
        )

        status_change = next(
            fc for fc in login_change.field_changes
            if fc.field == "status"
        )

        assert status_change.is_regression is True

    def test_status_progression_not_regression(self):
        """
        Status progression (planned -> implemented) is not a regression.

        @tests feature:reconciliation/audit-semantics
          - Ordinal fields declare progression order for regression detection
        """
        ordinal_config = {
            "field": "spec.status",
            "progression": ["proposed", "planned", "partial", "implemented"],
            "terminal": ["deprecated"],
        }
        assert is_ordinal_regression(ordinal_config, "planned", "implemented") is False
        assert is_ordinal_regression(ordinal_config, "proposed", "planned") is False
        assert is_ordinal_regression(ordinal_config, "partial", "implemented") is False

    def test_status_regression_detection(self):
        """
        Status regression (implemented -> planned) is detected.

        @tests feature:reconciliation/audit-semantics
          - Ordinal fields declare progression order for regression detection
        """
        ordinal_config = {
            "field": "spec.status",
            "progression": ["proposed", "planned", "partial", "implemented"],
            "terminal": ["deprecated"],
        }
        assert is_ordinal_regression(ordinal_config, "implemented", "planned") is True
        assert is_ordinal_regression(ordinal_config, "implemented", "partial") is True
        assert is_ordinal_regression(ordinal_config, "partial", "planned") is True

    def test_terminal_state_not_regression(self):
        """
        Moving to terminal state is not a regression.

        @tests feature:reconciliation/audit-semantics
          - Ordinal fields declare progression order for regression detection
        """
        ordinal_config = {
            "field": "spec.status",
            "progression": ["proposed", "planned", "partial", "implemented"],
            "terminal": ["deprecated"],
        }
        # Moving to deprecated is never a regression
        assert is_ordinal_regression(ordinal_config, "implemented", "deprecated") is False
        assert is_ordinal_regression(ordinal_config, "planned", "deprecated") is False

    def test_regression_sets_warning_severity(self, base_spec_dir, head_spec_dir):
        """Regressions result in warning severity."""
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))

        login_change = next(
            c for c in result.changes
            if c.entity_ref == "feature:auth/login"
        )

        assert login_change.severity == "warning"


# =============================================================================
# Test: Outputs human-readable diff of intent changes
# =============================================================================

class TestHumanReadableOutput:
    """Tests for human-readable output format."""

    def test_text_output_has_summary(self, base_spec_dir, head_spec_dir):
        """
        @tests feature:ci-integration/spec-audit
          - Outputs human-readable diff of intent changes
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))
        text = format_text_audit(result)

        assert "Summary:" in text
        assert "added" in text.lower()
        assert "removed" in text.lower()
        assert "modified" in text.lower()

    def test_text_output_uses_symbols(self, base_spec_dir, head_spec_dir):
        """
        @tests feature:ci-integration/spec-audit
          - Outputs human-readable diff of intent changes
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))
        text = format_text_audit(result)

        # Should use +/-/~ symbols for changes
        assert "+" in text  # Added
        assert "-" in text  # Removed
        assert "~" in text  # Modified

    def test_text_output_shows_regression_marker(self, base_spec_dir, head_spec_dir):
        """
        @tests feature:ci-integration/spec-audit
          - Outputs human-readable diff of intent changes
        """
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))
        text = format_text_audit(result)

        # Should highlight regressions
        assert "REGRESSION" in text

    def test_text_output_groups_by_file(self, base_spec_dir, head_spec_dir):
        """Text output groups changes by spec file."""
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))
        text = format_text_audit(result)

        # Should show file path
        assert "auth.yaml" in text

    def test_json_output_valid(self, base_spec_dir, head_spec_dir):
        """JSON output is valid and parseable."""
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))
        json_str = format_json_audit(result)

        # Should be valid JSON
        parsed = json.loads(json_str)

        assert "version" in parsed
        assert "summary" in parsed
        assert "changes" in parsed

    def test_json_output_contains_all_data(self, base_spec_dir, head_spec_dir):
        """JSON output contains all audit data."""
        result = audit_specs(str(base_spec_dir), str(head_spec_dir))
        json_str = format_json_audit(result)
        parsed = json.loads(json_str)

        # Summary should have all counts (schema-driven fields)
        summary = parsed["summary"]
        assert "entities_added" in summary
        assert "entities_removed" in summary
        assert "entities_modified" in summary
        assert "added_by_kind" in summary
        assert "removed_by_kind" in summary
        assert "ordinal_regressions" in summary
        assert "requirements_added" in summary
        assert "requirements_removed" in summary

        # Changes should have details
        assert len(parsed["changes"]) > 0
        change = parsed["changes"][0]
        assert "entity_ref" in change
        assert "change_type" in change
        assert "severity" in change


# =============================================================================
# Additional Tests
# =============================================================================

class TestSchemaDriverComparison:
    """Tests for schema-driven field comparison."""

    def test_schema_driven_comparison_uses_kinddefinition(self, tmp_path):
        """
        Verify that when KindDefinitions are present, schema-driven comparison is used.

        @tests feature:kind-system/audit-schema-driven
          - Field comparison driven by KindDefinition schema when available
        """
        # Create base and head with a kinds directory containing Feature KindDefinition
        base = tmp_path / "base" / "spec"
        head = tmp_path / "head" / "spec"

        for spec_dir in [base, head]:
            (spec_dir / "kinds").mkdir(parents=True)
            (spec_dir / "capabilities").mkdir(parents=True)

            # Write a Feature KindDefinition with custom schema
            # Include a custom field "custom_field" in the schema
            kind_def = {
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
                                "acceptance": {"type": "array", "items": {"type": "string"}},
                                "custom_field": {"type": "string"},  # Custom field for testing
                            },
                        },
                    },
                },
            }
            with open(spec_dir / "kinds" / "feature.yaml", "w") as f:
                yaml.dump(kind_def, f)

        # Base feature with custom_field
        base_feature = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "test-feature"},
            "spec": {
                "status": "implemented",
                "custom_field": "old_value",
            },
        }
        with open(base / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(base_feature, f)

        # Head feature with modified custom_field
        head_feature = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "test-feature"},
            "spec": {
                "status": "implemented",
                "custom_field": "new_value",
            },
        }
        with open(head / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(head_feature, f)

        result = audit_specs(str(base), str(head))

        # Should detect the custom_field change (only possible with schema-driven comparison)
        modified = [c for c in result.changes if c.entity_ref == "feature:test-feature"]
        assert len(modified) == 1

        field_changes = modified[0].field_changes
        custom_field_change = next(
            (fc for fc in field_changes if fc.field == "custom_field"),
            None
        )

        assert custom_field_change is not None, "Schema-driven comparison should detect custom_field"
        assert custom_field_change.old_value == "old_value"
        assert custom_field_change.new_value == "new_value"

    def test_error_when_no_kinddefinition(self, tmp_path):
        """
        Verify error when no KindDefinition is present.

        KindDefinitions are required - speccore should fail validation.
        """
        # Create base and head WITHOUT kinds directory
        base = tmp_path / "base" / "spec"
        head = tmp_path / "head" / "spec"

        for spec_dir in [base, head]:
            (spec_dir / "capabilities").mkdir(parents=True)

        # Base feature (no KindDefinition for Feature)
        base_feature = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "test-feature"},
            "spec": {
                "status": "planned",
            },
        }
        with open(base / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(base_feature, f)

        # Head feature
        head_feature = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "test-feature"},
            "spec": {
                "status": "implemented",
            },
        }
        with open(head / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(head_feature, f)

        # Should raise error because no KindDefinition exists
        with pytest.raises(ValueError, match="No KindDefinition found"):
            audit_specs(str(base), str(head))


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_base_dir(self, tmp_path):
        """Handle empty base directory."""
        base = tmp_path / "base" / "spec"
        base.mkdir(parents=True)
        create_kind_definitions(base)

        head = tmp_path / "head" / "spec"
        (head / "capabilities").mkdir(parents=True)
        create_kind_definitions(head)

        capability = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "test"},
            "spec": {"features": []},
        }
        with open(head / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(capability, f)

        # Should not crash
        result = audit_specs(str(base), str(head))
        assert result.summary.entities_added >= 1

    def test_empty_head_dir(self, tmp_path):
        """Handle empty head directory."""
        base = tmp_path / "base" / "spec"
        (base / "capabilities").mkdir(parents=True)
        create_kind_definitions(base)

        capability = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "test"},
            "spec": {"features": []},
        }
        with open(base / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(capability, f)

        head = tmp_path / "head" / "spec"
        head.mkdir(parents=True)
        create_kind_definitions(head)

        # Should not crash
        result = audit_specs(str(base), str(head))
        assert result.summary.entities_removed >= 1

    def test_component_changes_detected(self, tmp_path):
        """Detect changes to Component specs."""
        base = tmp_path / "base" / "spec"
        (base / "components").mkdir(parents=True)
        (base / "kinds").mkdir(parents=True)

        head = tmp_path / "head" / "spec"
        (head / "components").mkdir(parents=True)
        (head / "kinds").mkdir(parents=True)

        # Create Component KindDefinition for both
        for spec_dir in [base, head]:
            component_kind = {
                "apiVersion": "projectspec/v1alpha1",
                "kind": "KindDefinition",
                "metadata": {"name": "Component"},
                "spec": {
                    "category": "structural",
                    "validation": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "status": {"type": "string"},
                            },
                        },
                    },
                },
            }
            with open(spec_dir / "kinds" / "component.yaml", "w") as f:
                yaml.dump(component_kind, f)

        # Base component
        base_comp = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Component",
            "metadata": {"name": "api"},
            "spec": {"status": "planned"},
        }
        with open(base / "components" / "api.yaml", "w") as f:
            yaml.dump(base_comp, f)

        # Head component (status changed)
        head_comp = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Component",
            "metadata": {"name": "api"},
            "spec": {"status": "implemented"},
        }
        with open(head / "components" / "api.yaml", "w") as f:
            yaml.dump(head_comp, f)

        result = audit_specs(str(base), str(head))

        # Should detect component change
        modified = [c for c in result.changes if c.entity_ref == "component:api"]
        assert len(modified) == 1
        assert modified[0].change_type == "modified"

    def test_removed_entity_has_warning_severity(self, tmp_path):
        """Removed entities have warning severity."""
        base = tmp_path / "base" / "spec"
        (base / "capabilities").mkdir(parents=True)
        create_kind_definitions(base)

        capability = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Capability",
            "metadata": {"name": "auth"},
            "spec": {"features": []},
        }
        with open(base / "capabilities" / "auth.yaml", "w") as f:
            yaml.dump(capability, f)

        head = tmp_path / "head" / "spec"
        head.mkdir(parents=True)
        create_kind_definitions(head)

        result = audit_specs(str(base), str(head))

        removed = [c for c in result.changes if c.change_type == "removed"]
        for r in removed:
            assert r.severity == "warning"


# =============================================================================
# Test: Audit Semantics (Schema-Driven Change Detection)
# =============================================================================

class TestAuditSemantics:
    """Tests for schema-driven audit change detection."""

    def test_get_ordinal_config_from_kind_definition(self):
        """
        @tests feature:reconciliation/audit-semantics
          - KindDefinition supports audit section for change tracking semantics
        """
        kind_def = KindDefinition(
            name="Feature",
            category="behavioral",
            audit=AuditConfig(
                ordinals=[
                    OrdinalConfig(
                        field="spec.status",
                        progression=["planned", "partial", "implemented"],
                        terminal=["deprecated"],
                    )
                ]
            ),
        )

        ordinal = get_ordinal_config(kind_def, "spec.status")
        assert ordinal is not None
        assert ordinal["progression"] == ["planned", "partial", "implemented"]
        assert ordinal["terminal"] == ["deprecated"]

    def test_get_ordinal_config_returns_none_when_not_found(self):
        """Returns None when ordinal config is not found."""
        kind_def = KindDefinition(
            name="Feature",
            category="behavioral",
            audit=AuditConfig(
                ordinals=[
                    OrdinalConfig(
                        field="spec.status",
                        progression=["planned", "implemented"],
                    )
                ]
            ),
        )

        ordinal = get_ordinal_config(kind_def, "spec.other_field")
        assert ordinal is None

    def test_get_ordinal_config_returns_none_when_no_audit(self):
        """Returns None when no audit section exists."""
        kind_def = KindDefinition(
            name="Feature",
            category="behavioral",
        )

        ordinal = get_ordinal_config(kind_def, "spec.status")
        assert ordinal is None

    def test_get_requirements_field_from_kind_definition(self):
        """
        @tests feature:reconciliation/audit-semantics
          - Requirements removal derived from verification.coverage.requirementsField
        """
        kind_def = KindDefinition(
            name="Feature",
            category="behavioral",
            verification=VerificationConfig(
                coverage=CoverageConfig(
                    requirementsField="spec.acceptance[]",
                ),
            ),
        )

        req_field = get_requirements_field(kind_def)
        assert req_field == "spec.acceptance"

    def test_get_requirements_field_returns_none_when_not_defined(self):
        """Returns None when no requirements field is defined."""
        kind_def = KindDefinition(
            name="Feature",
            category="behavioral",
        )

        req_field = get_requirements_field(kind_def)
        assert req_field is None

    def test_get_relationship_fields(self):
        """
        @tests feature:reconciliation/audit-semantics
          - Relationship removal derived from relationships section
        """
        kind_def = KindDefinition(
            name="Feature",
            category="behavioral",
            relationships=[
                RelationshipDefinition(field="spec.depends-on[]", type="depends-on"),
                RelationshipDefinition(field="spec.extends[]", type="extends"),
            ],
        )

        fields = get_relationship_fields(kind_def)
        assert "spec.depends-on" in fields
        assert "spec.extends" in fields

    def test_schema_driven_regression_detection(self, tmp_path):
        """
        @tests feature:reconciliation/audit-semantics
          - audit.py reads field metadata from KindDefinitions (no hardcoding)
        """
        # Create spec dirs with KindDefinitions
        base = tmp_path / "base" / "spec"
        head = tmp_path / "head" / "spec"

        for spec_dir in [base, head]:
            (spec_dir / "kinds").mkdir(parents=True)
            (spec_dir / "capabilities").mkdir(parents=True)

            # Feature KindDefinition with audit section
            kind_def = {
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
                            },
                        },
                    },
                    "audit": {
                        "ordinals": [{
                            "field": "spec.status",
                            "progression": ["planned", "partial", "implemented"],
                            "terminal": ["deprecated"],
                        }]
                    },
                },
            }
            with open(spec_dir / "kinds" / "feature.yaml", "w") as f:
                yaml.dump(kind_def, f)

        # Base: feature at implemented
        base_feature = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "test-feature"},
            "spec": {"status": "implemented"},
        }
        with open(base / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(base_feature, f)

        # Head: feature regressed to partial
        head_feature = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "test-feature"},
            "spec": {"status": "partial"},
        }
        with open(head / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(head_feature, f)

        result = audit_specs(str(base), str(head))

        # Should detect regression using schema-driven detection
        modified = [c for c in result.changes if c.entity_ref == "feature:test-feature"]
        assert len(modified) == 1

        status_change = next(
            fc for fc in modified[0].field_changes if fc.field == "status"
        )
        assert status_change.is_regression is True
        assert modified[0].severity == "warning"

    def test_terminal_state_not_detected_as_regression(self, tmp_path):
        """
        @tests feature:reconciliation/audit-semantics
          - Ordinal fields declare progression order for regression detection
        """
        # Create spec dirs with KindDefinitions
        base = tmp_path / "base" / "spec"
        head = tmp_path / "head" / "spec"

        for spec_dir in [base, head]:
            (spec_dir / "kinds").mkdir(parents=True)
            (spec_dir / "capabilities").mkdir(parents=True)

            # Feature KindDefinition with terminal state
            kind_def = {
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
                            },
                        },
                    },
                    "audit": {
                        "ordinals": [{
                            "field": "spec.status",
                            "progression": ["planned", "partial", "implemented"],
                            "terminal": ["deprecated"],
                        }]
                    },
                },
            }
            with open(spec_dir / "kinds" / "feature.yaml", "w") as f:
                yaml.dump(kind_def, f)

        # Base: feature at implemented
        base_feature = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "test-feature"},
            "spec": {"status": "implemented"},
        }
        with open(base / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(base_feature, f)

        # Head: feature moved to deprecated (terminal state)
        head_feature = {
            "apiVersion": "projectspec/v1alpha1",
            "kind": "Feature",
            "metadata": {"name": "test-feature"},
            "spec": {"status": "deprecated"},
        }
        with open(head / "capabilities" / "test.yaml", "w") as f:
            yaml.dump(head_feature, f)

        result = audit_specs(str(base), str(head))

        # Should NOT detect as regression (terminal state)
        modified = [c for c in result.changes if c.entity_ref == "feature:test-feature"]
        assert len(modified) == 1

        status_change = next(
            fc for fc in modified[0].field_changes if fc.field == "status"
        )
        assert status_change.is_regression is False
        # Should be info severity since not a regression
        assert modified[0].severity == "info"
