#!/usr/bin/env python3
"""
Surface spec changes in PRs for human review.

Posts a comment summarizing what changed, adds labels for filtering,
and optionally blocks merge for significant changes.

@implements feature:ci-integration/spec-review
  - Posts comment on PRs summarizing spec changes (entities, status, criteria)
  - Comment highlights regressions and removals requiring attention
  - Applies severity-based labels (spec-info, spec-warning, spec-error)
  - Configurable enforcement modes (inform, warn, block)
  - Block threshold configurable by severity (info, warning, none)

@implements feature:reconciliation/audit-semantics
  - review.py formats comments generically using field names from audit

Usage:
  python review.py <pr-number> [options]

Options:
  --spec-dir DIR       Spec directory (default: spec)
  --enforcement MODE   inform|warn|block (default: warn)
  --block-on SEVERITY  Block threshold: none|info|warning (default: none)
  --dry-run            Don't post comment or add labels
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


# =============================================================================
# Severity Levels
# =============================================================================

SEVERITY_LEVELS = ["info", "warning", "error"]
SEVERITY_LABELS = {
    "info": "spec-info",
    "warning": "spec-warning",
    "error": "spec-error",
}


def get_max_severity(changes: list[dict]) -> str:
    """
    Get the maximum severity from a list of changes.

    Returns 'info' if no changes or all are info-level.
    """
    if not changes:
        return "info"

    has_warning = any(c.get("severity") == "warning" for c in changes)
    return "warning" if has_warning else "info"


def severity_meets_threshold(severity: str, threshold: str) -> bool:
    """
    Check if severity meets or exceeds the threshold.

    Severity order: info < warning < error
    """
    if threshold == "none":
        return False

    severity_order = {"info": 0, "warning": 1, "error": 2}
    return severity_order.get(severity, 0) >= severity_order.get(threshold, 0)


# =============================================================================
# GitHub CLI Helpers
# =============================================================================

def run_gh(*args, check: bool = True) -> subprocess.CompletedProcess:
    """Run gh CLI command."""
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"gh error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def get_pr_info(pr_number: str) -> dict:
    """Get PR details including changed files and base ref."""
    result = run_gh(
        "pr", "view", pr_number,
        "--json", "files,baseRefName,headRefName,number"
    )
    return json.loads(result.stdout)


def add_label(pr_number: str, label: str) -> None:
    """Add label to PR, creating the label if it doesn't exist."""
    # Try to create label (no-op if exists)
    run_gh("label", "create", label, "--force", check=False)
    # Add to PR
    run_gh("pr", "edit", pr_number, "--add-label", label)
    print(f"Added label: {label}")


def find_existing_comment(pr_number: str) -> str | None:
    """Find existing spec-review comment on PR, return comment ID if found."""
    # Get repo info
    result = run_gh("repo", "view", "--json", "owner,name", check=False)
    if result.returncode != 0:
        return None

    repo_info = json.loads(result.stdout)
    owner = repo_info["owner"]["login"]
    repo = repo_info["name"]

    # List comments on PR
    result = run_gh(
        "api", f"repos/{owner}/{repo}/issues/{pr_number}/comments",
        "--jq", ".[] | select(.body | contains(\"projectspec\") and contains(\"spec-review\")) | .id",
        check=False
    )

    if result.returncode == 0 and result.stdout.strip():
        # Return first matching comment ID
        return result.stdout.strip().split("\n")[0]

    return None


def update_comment(comment_id: str, body: str) -> None:
    """Update an existing comment."""
    # Get repo info
    result = run_gh("repo", "view", "--json", "owner,name")
    repo_info = json.loads(result.stdout)
    owner = repo_info["owner"]["login"]
    repo = repo_info["name"]

    # Update the comment
    run_gh(
        "api", "--method", "PATCH",
        f"repos/{owner}/{repo}/issues/comments/{comment_id}",
        "-f", f"body={body}"
    )
    print("Updated existing review comment")


def post_or_update_comment(pr_number: str, body: str) -> None:
    """Post new comment or update existing one."""
    existing_id = find_existing_comment(pr_number)

    if existing_id:
        update_comment(existing_id, body)
    else:
        run_gh("pr", "comment", pr_number, "--body", body)
        print("Posted review comment")


# =============================================================================
# Spec Change Detection
# =============================================================================

def has_spec_changes(files: list[dict], spec_dir: str = "spec") -> bool:
    """Check if any changed files are in spec directory."""
    return any(f["path"].startswith(f"{spec_dir}/") for f in files)


def extract_base_specs(base_ref: str, spec_dir: str, dest: str) -> None:
    """Extract spec directory from base ref to destination."""
    # Try origin/base_ref first (common in CI), fall back to base_ref
    for ref in [f"origin/{base_ref}", base_ref]:
        result = subprocess.run(
            f"git archive {ref} -- {spec_dir}/ | tar -x -C {dest}",
            shell=True,
            capture_output=True
        )
        if result.returncode == 0:
            return
    # If both failed, raise with the original ref
    raise subprocess.CalledProcessError(
        result.returncode, f"git archive {base_ref}", result.stderr
    )


def run_audit(base_spec_dir: str, head_spec_dir: str) -> dict | None:
    """Run spec audit and return parsed result."""
    result = subprocess.run(
        ["projectspec", "audit",
         "--base", base_spec_dir,
         "--head", head_spec_dir,
         "--format", "json"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0 and not result.stdout:
        print(f"audit error: {result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Failed to parse audit output: {result.stdout}", file=sys.stderr)
        return None


# =============================================================================
# Comment Formatting
# =============================================================================

def format_comment(audit_result: dict) -> str:
    """Format audit result as markdown comment."""
    summary = audit_result["summary"]
    changes = audit_result["changes"]

    lines = ["## Spec Review", ""]

    # Summary line - use kind breakdown when available
    parts = []

    # Show modified breakdown by kind
    modified_by_kind = summary.get("modified_by_kind", {})
    if modified_by_kind:
        for kind, count in sorted(modified_by_kind.items()):
            parts.append(f"{count} {kind} modified")
    elif summary.get("entities_modified"):
        parts.append(f"{summary['entities_modified']} modified")

    # Show added breakdown by kind
    added_by_kind = summary.get("added_by_kind", {})
    if added_by_kind:
        for kind, count in sorted(added_by_kind.items()):
            parts.append(f"{count} {kind} added")
    elif summary.get("entities_added"):
        parts.append(f"{summary['entities_added']} added")

    # Show removed breakdown by kind
    removed_by_kind = summary.get("removed_by_kind", {})
    if removed_by_kind:
        for kind, count in sorted(removed_by_kind.items()):
            parts.append(f"{count} {kind} removed")
    elif summary.get("entities_removed"):
        parts.append(f"{summary['entities_removed']} removed")

    if parts:
        lines.append(f"**{', '.join(parts)}**")
    else:
        lines.append("**No significant changes**")
    lines.append("")

    # Attention section - show full context for warned entities
    warnings = [c for c in changes if c.get("severity") == "warning"]
    if warnings:
        lines.append("### Attention Required")
        lines.append("")

        for change in warnings:
            lines.append(f"**{change['entity_ref']}**")
            lines.append("")

            if change.get("change_type") == "removed":
                entity_type = change.get("entity_type", "Entity")
                lines.append(f"_{entity_type} was removed entirely_")
            else:
                # Show table with full context: what was removed AND what was added
                lines.append("| Field | Removed | Added |")
                lines.append("|-------|---------|-------|")

                for fc in change.get("field_changes", []):
                    field_name = fc.get("field", "unknown")

                    if fc.get("items_removed") or fc.get("items_added"):
                        # Array field - show each removed/added pair
                        removed_items = fc.get("items_removed", [])
                        added_items = fc.get("items_added", [])
                        max_len = max(len(removed_items), len(added_items))

                        for i in range(max_len):
                            removed = removed_items[i] if i < len(removed_items) else ""
                            added = added_items[i] if i < len(added_items) else ""
                            # Truncate long values
                            removed_display = f'"{removed[:60]}..."' if len(removed) > 60 else f'"{removed}"' if removed else "—"
                            added_display = f'"{added[:60]}..."' if len(added) > 60 else f'"{added}"' if added else "—"
                            # Only show field name on first row for this field
                            field_display = f"`{field_name}`" if i == 0 else ""
                            lines.append(f"| {field_display} | {removed_display} | {added_display} |")
                    else:
                        # Scalar field change (e.g., status regression)
                        old_val = fc.get("old_value", "")
                        new_val = fc.get("new_value", "")
                        regression_marker = " ⚠️" if fc.get("is_regression") else ""
                        lines.append(f"| `{field_name}`{regression_marker} | {old_val} | {new_val} |")

            lines.append("")

    # All changes in collapsible section
    if changes:
        lines.append("<details>")
        lines.append("<summary><b>All Changes</b></summary>")
        lines.append("")

        for change in changes:
            status_marker = " ⚠️" if change.get("severity") == "warning" else ""
            lines.append(
                f"**{change['entity_ref']}** [{change['change_type']}]{status_marker}"
            )

            if change.get("change_type") in ("added", "removed"):
                lines.append(f"- {change['change_type'].capitalize()}")
            else:
                for fc in change.get("field_changes", []):
                    field_name = fc.get("field", "unknown")
                    if fc.get("items_removed") or fc.get("items_added"):
                        # Array field changes
                        for item in fc.get("items_removed", []):
                            lines.append(f'- `{field_name}` removed: "{item}"')
                        for item in fc.get("items_added", []):
                            lines.append(f'- `{field_name}` added: "{item}"')
                    else:
                        # Scalar field change
                        lines.append(
                            f"- `{field_name}`: {fc.get('old_value')} → {fc.get('new_value')}"
                        )
            lines.append("")

        lines.append("</details>")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append(
        "*[projectspec](https://github.com/codewithcheese/projectspec) spec-review*"
    )

    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Surface spec changes in PRs for human review"
    )
    parser.add_argument("pr_number", help="PR number")
    parser.add_argument(
        "--spec-dir",
        default="spec",
        help="Spec directory (default: spec)"
    )
    parser.add_argument(
        "--enforcement",
        choices=["inform", "warn", "block"],
        default="warn",
        help="Enforcement mode (default: warn)"
    )
    parser.add_argument(
        "--block-on",
        choices=["none", "info", "warning"],
        default="none",
        help="Block threshold severity: none|info|warning (default: none)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't post comment or add labels"
    )
    args = parser.parse_args()

    # Get PR info
    try:
        pr_info = get_pr_info(args.pr_number)
    except SystemExit:
        print("Failed to get PR info. Is gh CLI authenticated?", file=sys.stderr)
        return 1

    files = pr_info.get("files", [])
    base_ref = pr_info.get("baseRefName", "main")

    # Check for spec changes
    if not has_spec_changes(files, args.spec_dir):
        print("No spec changes detected")
        return 0

    print(f"Spec changes detected in PR #{args.pr_number}")

    # Run audit
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            extract_base_specs(base_ref, args.spec_dir, tmpdir)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not extract base specs from {base_ref}")
            print(f"Error: {e.stderr.decode() if e.stderr else 'unknown'}")
            return 0

        # git archive extracts to tmpdir/spec_dir
        base_spec_path = str(Path(tmpdir) / args.spec_dir)
        audit_result = run_audit(base_spec_path, args.spec_dir)

    if not audit_result:
        print("Error: Audit failed", file=sys.stderr)
        return 1

    # Determine severity and apply label
    changes = audit_result.get("changes", [])
    max_severity = get_max_severity(changes)

    # In block mode, if threshold met, severity escalates to error
    should_block = (
        args.enforcement == "block" and
        severity_meets_threshold(max_severity, args.block_on)
    )
    if should_block:
        max_severity = "error"

    # Apply severity label
    label = SEVERITY_LABELS[max_severity]
    if not args.dry_run:
        add_label(args.pr_number, label)

    # Format and post/update comment
    comment = format_comment(audit_result)
    if not args.dry_run:
        post_or_update_comment(args.pr_number, comment)
    else:
        print("\n--- Comment Preview ---")
        print(comment)
        print("--- End Preview ---\n")

    # Block if threshold met
    if should_block:
        print(f"\nBlocked: severity '{max_severity}' meets threshold '{args.block_on}'")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
