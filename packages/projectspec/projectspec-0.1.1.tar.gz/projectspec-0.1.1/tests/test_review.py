"""
Tests for review.py - Spec Review feature for CI integration.

Tests cover comment formatting, severity detection, label logic,
and block threshold behavior.
"""

import pytest

# Import from projectspec package
from projectspec.review import (
    format_comment,
    has_spec_changes,
    get_max_severity,
    severity_meets_threshold,
    SEVERITY_LABELS,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def audit_result_with_warnings():
    """Audit result with regressions and removals."""
    return {
        "summary": {
            "entities_added": 1,
            "entities_removed": 1,
            "entities_modified": 1,
            "added_by_kind": {"Feature": 1},
            "removed_by_kind": {"Feature": 1},
            "ordinal_regressions": 1,
            "requirements_added": 1,
            "requirements_removed": 1,
        },
        "changes": [
            {
                "entity_ref": "feature:auth/login",
                "entity_type": "Feature",
                "change_type": "modified",
                "severity": "warning",
                "field_changes": [
                    {
                        "field": "status",
                        "old_value": "implemented",
                        "new_value": "partial",
                        "is_regression": True,
                    },
                    {
                        "field": "acceptance",
                        "items_removed": ["Session persists across restart"],
                        "items_added": ["Session expires after 24h"],
                    },
                ],
            },
            {
                "entity_ref": "feature:auth/logout",
                "entity_type": "Feature",
                "change_type": "removed",
                "severity": "warning",
                "field_changes": [],
            },
            {
                "entity_ref": "feature:auth/oauth",
                "entity_type": "Feature",
                "change_type": "added",
                "severity": "info",
                "field_changes": [],
            },
        ],
    }


@pytest.fixture
def audit_result_no_warnings():
    """Audit result with only additions (no warnings)."""
    return {
        "summary": {
            "entities_added": 2,
            "entities_removed": 0,
            "entities_modified": 0,
            "added_by_kind": {"Feature": 2},
            "removed_by_kind": {},
            "ordinal_regressions": 0,
            "requirements_added": 3,
            "requirements_removed": 0,
        },
        "changes": [
            {
                "entity_ref": "feature:auth/oauth",
                "entity_type": "Feature",
                "change_type": "added",
                "severity": "info",
                "field_changes": [],
            },
            {
                "entity_ref": "feature:auth/mfa",
                "entity_type": "Feature",
                "change_type": "added",
                "severity": "info",
                "field_changes": [],
            },
        ],
    }


@pytest.fixture
def audit_result_empty():
    """Audit result with no changes."""
    return {
        "summary": {
            "entities_added": 0,
            "entities_removed": 0,
            "entities_modified": 0,
            "added_by_kind": {},
            "removed_by_kind": {},
            "ordinal_regressions": 0,
            "requirements_added": 0,
            "requirements_removed": 0,
        },
        "changes": [],
    }


# =============================================================================
# Test: Posts comment on PRs summarizing spec changes
# =============================================================================

class TestCommentFormatting:
    """Tests for comment formatting."""

    def test_comment_has_header(self, audit_result_with_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Posts comment on PRs summarizing spec changes (entities, status, criteria)
        """
        comment = format_comment(audit_result_with_warnings)
        assert "## Spec Review" in comment

    def test_comment_has_summary(self, audit_result_with_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Posts comment on PRs summarizing spec changes (entities, status, criteria)
        """
        comment = format_comment(audit_result_with_warnings)
        assert "modified" in comment
        assert "added" in comment
        assert "removed" in comment

    def test_comment_shows_entity_counts(self, audit_result_with_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Posts comment on PRs summarizing spec changes (entities, status, criteria)
        """
        comment = format_comment(audit_result_with_warnings)
        assert "1 modified" in comment
        # Now shows kind breakdown: "1 Feature added" instead of "1 added"
        assert "1 Feature added" in comment
        assert "1 Feature removed" in comment

    def test_empty_changes_shows_no_significant_changes(self, audit_result_empty):
        """Comment shows 'no significant changes' when empty."""
        comment = format_comment(audit_result_empty)
        assert "No significant changes" in comment


# =============================================================================
# Test: Comment highlights regressions and removals
# =============================================================================

class TestAttentionSection:
    """Tests for the attention/warning section."""

    def test_attention_section_present_with_warnings(self, audit_result_with_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Comment highlights regressions and removals requiring attention
        """
        comment = format_comment(audit_result_with_warnings)
        assert "### Attention Required" in comment

    def test_attention_section_absent_without_warnings(self, audit_result_no_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Comment highlights regressions and removals requiring attention
        """
        comment = format_comment(audit_result_no_warnings)
        assert "### Attention Required" not in comment

    def test_status_regression_in_attention(self, audit_result_with_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Comment highlights regressions and removals requiring attention

        @tests feature:reconciliation/audit-semantics
          - review.py formats comments generically using field names from audit
        """
        comment = format_comment(audit_result_with_warnings)
        # Shows full context table with Removed and Added columns
        assert "| Field | Removed | Added |" in comment
        assert "`status`" in comment
        assert "implemented" in comment
        assert "partial" in comment

    def test_criteria_removed_in_attention(self, audit_result_with_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Comment highlights regressions and removals requiring attention

        @tests feature:reconciliation/audit-semantics
          - review.py formats comments generically using field names from audit
        """
        comment = format_comment(audit_result_with_warnings)
        # Shows full context table with what was removed and added
        assert "`acceptance`" in comment
        assert "Session persists" in comment

    def test_entity_removed_in_attention(self, audit_result_with_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Comment highlights regressions and removals requiring attention

        @tests feature:reconciliation/audit-semantics
          - review.py formats comments generically using field names from audit
        """
        comment = format_comment(audit_result_with_warnings)
        # Entity removal shown with descriptive message
        assert "was removed entirely" in comment
        assert "feature:auth/logout" in comment


# =============================================================================
# Test: Severity-based labels
# =============================================================================

class TestSeverityLabels:
    """Tests for severity-based labeling."""

    def test_severity_labels_defined(self):
        """
        @tests feature:ci-integration/spec-review
          - Applies severity-based labels (spec-info, spec-warning, spec-error)
        """
        assert SEVERITY_LABELS["info"] == "spec-info"
        assert SEVERITY_LABELS["warning"] == "spec-warning"
        assert SEVERITY_LABELS["error"] == "spec-error"

    def test_max_severity_with_warnings(self, audit_result_with_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Applies severity-based labels (spec-info, spec-warning, spec-error)
        """
        severity = get_max_severity(audit_result_with_warnings["changes"])
        assert severity == "warning"

    def test_max_severity_info_only(self, audit_result_no_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Applies severity-based labels (spec-info, spec-warning, spec-error)
        """
        severity = get_max_severity(audit_result_no_warnings["changes"])
        assert severity == "info"

    def test_max_severity_empty(self, audit_result_empty):
        """Empty changes returns info severity."""
        severity = get_max_severity(audit_result_empty["changes"])
        assert severity == "info"


# =============================================================================
# Test: Spec change detection
# =============================================================================

class TestSpecChangeDetection:
    """Tests for spec change detection."""

    def test_detects_spec_file_changes(self):
        """Detects when spec files are modified."""
        files = [{"path": "spec/capabilities/auth.yaml"}]
        assert has_spec_changes(files) is True

    def test_ignores_non_spec_files(self):
        """Ignores non-spec file changes."""
        files = [{"path": "src/main.py"}, {"path": "tests/test_auth.py"}]
        assert has_spec_changes(files) is False

    def test_custom_spec_dir(self):
        """Respects custom spec directory."""
        files = [{"path": "specifications/auth.yaml"}]
        assert has_spec_changes(files, spec_dir="specifications") is True
        assert has_spec_changes(files, spec_dir="spec") is False


# =============================================================================
# Test: Block threshold
# =============================================================================

class TestBlockThreshold:
    """Tests for severity-based block threshold."""

    def test_none_threshold_never_blocks(self):
        """
        @tests feature:ci-integration/spec-review
          - Block threshold configurable by severity (info, warning, none)
        """
        assert severity_meets_threshold("info", "none") is False
        assert severity_meets_threshold("warning", "none") is False
        assert severity_meets_threshold("error", "none") is False

    def test_info_threshold_blocks_all(self):
        """
        @tests feature:ci-integration/spec-review
          - Block threshold configurable by severity (info, warning, none)
        """
        assert severity_meets_threshold("info", "info") is True
        assert severity_meets_threshold("warning", "info") is True
        assert severity_meets_threshold("error", "info") is True

    def test_warning_threshold_blocks_warning_and_error(self):
        """
        @tests feature:ci-integration/spec-review
          - Block threshold configurable by severity (info, warning, none)
        """
        assert severity_meets_threshold("info", "warning") is False
        assert severity_meets_threshold("warning", "warning") is True
        assert severity_meets_threshold("error", "warning") is True


# =============================================================================
# Test: Enforcement modes
# =============================================================================

class TestEnforcementModes:
    """Tests for enforcement mode behavior."""

    def test_info_does_not_meet_warning_threshold(self, audit_result_no_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Configurable enforcement modes (inform, warn, block)
        """
        severity = get_max_severity(audit_result_no_warnings["changes"])
        assert severity == "info"
        assert severity_meets_threshold(severity, "warning") is False

    def test_warning_meets_warning_threshold(self, audit_result_with_warnings):
        """
        @tests feature:ci-integration/spec-review
          - Configurable enforcement modes (inform, warn, block)
        """
        severity = get_max_severity(audit_result_with_warnings["changes"])
        assert severity == "warning"
        assert severity_meets_threshold(severity, "warning") is True


# =============================================================================
# Test: Comment structure
# =============================================================================

class TestCommentStructure:
    """Tests for overall comment structure."""

    def test_comment_has_collapsible_details(self, audit_result_with_warnings):
        """Comment has collapsible details section."""
        comment = format_comment(audit_result_with_warnings)
        assert "<details>" in comment
        assert "</details>" in comment
        assert "All Changes" in comment

    def test_comment_has_footer(self, audit_result_with_warnings):
        """Comment has footer with project link."""
        comment = format_comment(audit_result_with_warnings)
        assert "projectspec" in comment
        assert "spec-review" in comment

    def test_warning_emoji_on_warnings(self, audit_result_with_warnings):
        """Warning emoji shown for warning severity changes."""
        comment = format_comment(audit_result_with_warnings)
        assert "⚠️" in comment

    def test_no_warning_emoji_on_info(self, audit_result_no_warnings):
        """No warning emoji for info severity changes."""
        comment = format_comment(audit_result_no_warnings)
        # Should not have warning emoji (only info changes)
        assert "⚠️" not in comment
