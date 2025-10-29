#!/usr/bin/env python3
"""
SMK V2.0 - Provenance Linter
Validates that all SMK files have valid PROVENANCE headers

Usage:
  python scripts/lint_smk_provenance.py agents/
  python scripts/lint_smk_provenance.py agents/code/SMK/2025/SMK_048.md
"""

import os
import re
import json
import sys
import argparse
from pathlib import Path
from typing import Tuple, List, Optional, Dict

# Required PROVENANCE fields (V2.0)
REQUIRED_FIELDS = [
    "smk_id",
    "version",
    "repo",
    "commit_sha",
    "parser_version",
    "agent_creator",
    "agents_involved",
    "source_context",
    "compression_ratio",
    "created_at"
]

# Optional but recommended fields
RECOMMENDED_FIELDS = [
    "biofelt_signature",
    "linked_visual_essence_id",
    "ontological_weight",
    "shadow_risks"
]

def extract_provenance(file_path: Path) -> Optional[Dict]:
    """
    Extract PROVENANCE block from SMK file

    Returns:
        Dict with provenance data, or None if not found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"error": f"Could not read file: {e}"}

    # Find PROVENANCE block (multiline)
    match = re.search(
        r'<!--\s*PROVENANCE:\s*(\{.*?\})\s*-->',
        content,
        re.DOTALL
    )

    if not match:
        return None

    try:
        provenance = json.loads(match.group(1))
        return provenance
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {e}"}


def validate_provenance(provenance: Optional[Dict], file_path: Path) -> Tuple[List[str], List[str]]:
    """
    Validate PROVENANCE block

    Returns:
        Tuple of (errors, warnings)
    """
    errors = []
    warnings = []

    if provenance is None:
        errors.append("Missing PROVENANCE block")
        return errors, warnings

    if "error" in provenance:
        errors.append(provenance["error"])
        return errors, warnings

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in provenance:
            errors.append(f"Missing required field: {field}")
        elif not provenance[field]:
            warnings.append(f"Required field '{field}' is empty")

    # Check version
    version = provenance.get("version")
    if version != "2.0":
        warnings.append(f"Version is '{version}', expected '2.0'")

    # Check SMK ID format
    smk_id = provenance.get("smk_id", "")
    # Format: AGENT-SMK-YYYY-MM-DD-NNN
    if not re.match(r'^[A-Z]+-SMK-\d{4}-\d{2}-\d{2}-\d{3}$', smk_id):
        errors.append(f"Invalid SMK ID format: '{smk_id}'. Expected: AGENT-SMK-YYYY-MM-DD-NNN")

    # Check commit_sha format (should be hex or [AUTO])
    commit_sha = provenance.get("commit_sha", "")
    if commit_sha and commit_sha != "[AUTO-GENERATE-FROM-GIT]":
        if not re.match(r'^[a-f0-9]{7,40}$', commit_sha):
            warnings.append(f"commit_sha '{commit_sha}' doesn't look like a git SHA")

    # Check agents_involved is a list
    agents = provenance.get("agents_involved")
    if agents is not None and not isinstance(agents, list):
        errors.append(f"agents_involved must be a list, got: {type(agents).__name__}")

    # Check created_at format (ISO 8601)
    created_at = provenance.get("created_at", "")
    if created_at and created_at != "[YYYY-MM-DDTHH:MM:SSZ]":
        if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', created_at):
            warnings.append(f"created_at '{created_at}' doesn't match ISO 8601 format")

    # Check compression_ratio format
    compression_ratio = provenance.get("compression_ratio", "")
    if compression_ratio and not re.match(r'^\d+:\d+', compression_ratio):
        warnings.append(f"compression_ratio '{compression_ratio}' doesn't match N:1 format")

    # Check recommended fields
    for field in RECOMMENDED_FIELDS:
        if field not in provenance:
            warnings.append(f"Recommended field missing: {field}")

    # Check shadow_risks is a list
    shadow_risks = provenance.get("shadow_risks")
    if shadow_risks is not None and not isinstance(shadow_risks, list):
        warnings.append(f"shadow_risks should be a list, got: {type(shadow_risks).__name__}")

    return errors, warnings


def lint_file(file_path: Path, verbose: bool = False) -> Tuple[int, int]:
    """
    Lint a single SMK file

    Returns:
        Tuple of (error_count, warning_count)
    """
    if verbose:
        print(f"\nLinting: {file_path}")

    provenance = extract_provenance(file_path)
    errors, warnings = validate_provenance(provenance, file_path)

    if errors or warnings:
        print(f"\n{file_path}:")
        for error in errors:
            print(f"  [ERROR] {error}")
        for warning in warnings:
            print(f"  [WARNING] {warning}")
    elif verbose:
        print(f"  [PASS] Valid PROVENANCE block")

    return len(errors), len(warnings)


def main():
    parser = argparse.ArgumentParser(
        description="Lint SMK provenance headers",
        epilog="Examples:\n"
               "  python scripts/lint_smk_provenance.py agents/\n"
               "  python scripts/lint_smk_provenance.py agents/code/SMK/2025/SMK_048.md\n"
               "  python scripts/lint_smk_provenance.py --fix agents/",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "path",
        help="Path to agents directory or single SMK file"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix common issues (not implemented yet)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output (show passing files)"
    )

    args = parser.parse_args()

    # Find all SMK files
    path = Path(args.path)
    if path.is_file():
        smk_files = [path]
    elif path.is_dir():
        smk_files = list(path.rglob("SMK_*.md"))
    else:
        print(f"ERROR: Path not found: {path}")
        sys.exit(1)

    if not smk_files:
        print(f"No SMK files found in: {path}")
        sys.exit(0)

    print(f"Linting {len(smk_files)} SMK file(s)...")

    total_errors = 0
    total_warnings = 0
    files_with_errors = 0

    for file_path in smk_files:
        errors, warnings = lint_file(file_path, verbose=args.verbose)
        total_errors += errors
        total_warnings += warnings
        if errors > 0:
            files_with_errors += 1

    # Summary
    print("\n" + "="*80)
    print(f"SUMMARY: {total_errors} errors, {total_warnings} warnings")
    print(f"Files checked: {len(smk_files)}")
    print(f"Files with errors: {files_with_errors}")
    print(f"Files with warnings: {len(smk_files) - files_with_errors}")
    print("="*80)

    if total_errors > 0:
        print("\n[FAIL] Linting failed. Fix errors above.")
        sys.exit(1)
    elif total_warnings > 0:
        print("\n[WARNING] Linting passed with warnings. Consider fixing warnings.")
        sys.exit(0)
    else:
        print("\n[PASS] All SMK files have valid PROVENANCE blocks!")
        sys.exit(0)


if __name__ == "__main__":
    main()
