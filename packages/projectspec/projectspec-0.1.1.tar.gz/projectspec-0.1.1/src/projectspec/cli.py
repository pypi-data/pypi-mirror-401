#!/usr/bin/env python3
"""
ProjectSpec CLI - Machine-readable specs that link intent to code.

Usage:
    projectspec reconcile [options]
    projectspec audit --base PATH --head PATH [options]
    projectspec review PR_NUMBER [options]

@implements feature:distribution/unified-cli
  - Single entry point 'projectspec' command
  - Subcommand 'reconcile' runs reconciliation
  - Subcommand 'audit' compares spec versions
  - Subcommand 'review' handles PR review
  - Help available via --help on all commands
  - Version available via --version
"""

import argparse
import sys

from projectspec import __version__


def add_reconcile_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add reconcile subcommand parser."""
    parser = subparsers.add_parser(
        "reconcile",
        help="Compare specs against implementation",
        description="Reconcile project specs against actual implementation to surface gaps.",
    )
    parser.add_argument(
        "--spec-dir",
        default="spec",
        help="Directory containing spec files (default: spec)",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root directory (default: current directory)",
    )
    parser.add_argument(
        "--source-dirs",
        nargs="+",
        default=["src", "tests", "docs"],
        help="Source directories to scan for unlinked files (default: src tests docs)",
    )
    parser.add_argument(
        "--kinds-dir",
        default=None,
        help="Directory containing KindDefinitions (default: spec/kinds)",
    )
    parser.add_argument(
        "--no-unlinked",
        action="store_true",
        help="Skip checking for unlinked files",
    )
    parser.add_argument(
        "--no-criteria",
        action="store_true",
        help="Skip criteria verification",
    )
    parser.add_argument(
        "--no-graph",
        action="store_true",
        help="Skip relationship graph building",
    )
    parser.add_argument(
        "--test-dirs",
        nargs="+",
        default=None,
        help="Directories to scan for test files (default: from Project spec or 'tests')",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code if any issues found",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )


def add_audit_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add audit subcommand parser."""
    parser = subparsers.add_parser(
        "audit",
        help="Compare specs between two versions",
        description="Audit spec changes between two versions to highlight regressions.",
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


def add_review_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add review subcommand parser."""
    parser = subparsers.add_parser(
        "review",
        help="Review spec changes in a PR",
        description="Surface spec changes in PRs for human review.",
    )
    parser.add_argument(
        "pr_number",
        help="PR number",
    )
    parser.add_argument(
        "--spec-dir",
        default="spec",
        help="Spec directory (default: spec)",
    )
    parser.add_argument(
        "--enforcement",
        choices=["inform", "warn", "block"],
        default="warn",
        help="Enforcement mode (default: warn)",
    )
    parser.add_argument(
        "--block-on",
        choices=["none", "info", "warning"],
        default="none",
        help="Block threshold severity: none|info|warning (default: none)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't post comment or add labels",
    )


def run_reconcile(args: argparse.Namespace) -> int:
    """Run the reconcile command."""
    from projectspec.reconcile import reconcile, format_text_result, format_json_result
    import os

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
        return 1
    elif result.has_errors:
        return 1

    return 0


def run_audit(args: argparse.Namespace) -> int:
    """Run the audit command."""
    from projectspec.audit import audit_specs, format_text_audit, format_json_audit
    from pathlib import Path

    base_path = Path(args.base)
    head_path = Path(args.head)

    if not base_path.exists():
        print(f"Error: Base path does not exist: {args.base}", file=sys.stderr)
        return 1

    if not head_path.exists():
        print(f"Error: Head path does not exist: {args.head}", file=sys.stderr)
        return 1

    result = audit_specs(args.base, args.head)

    if args.format == "json":
        print(format_json_audit(result))
    else:
        print(format_text_audit(result))

    if args.fail_on_warning:
        has_warnings = any(c.severity == "warning" for c in result.changes)
        if has_warnings:
            return 1

    return 0


def run_review(args: argparse.Namespace) -> int:
    """Run the review command."""
    from projectspec.review import main as review_main

    # Build sys.argv for the review module
    argv = [args.pr_number]
    argv.extend(["--spec-dir", args.spec_dir])
    argv.extend(["--enforcement", args.enforcement])
    argv.extend(["--block-on", args.block_on])
    if args.dry_run:
        argv.append("--dry-run")

    # Temporarily replace sys.argv and call review main
    old_argv = sys.argv
    sys.argv = ["projectspec-review"] + argv
    try:
        return review_main()
    finally:
        sys.argv = old_argv


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="projectspec",
        description="Machine-readable specs that link intent to code, with tooling to surface drift",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="command")

    add_reconcile_parser(subparsers)
    add_audit_parser(subparsers)
    add_review_parser(subparsers)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "reconcile":
        return run_reconcile(args)
    elif args.command == "audit":
        return run_audit(args)
    elif args.command == "review":
        return run_review(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
