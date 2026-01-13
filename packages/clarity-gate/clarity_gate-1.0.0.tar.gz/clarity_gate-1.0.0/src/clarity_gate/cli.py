#!/usr/bin/env python3
"""
clarity-gate CLI

Usage:
    clarity-gate check <file>           Auto-detect and validate
    clarity-gate validate-cgd <file>    Validate as CGD
    clarity-gate validate-sot <file>    Validate as SOT

Options:
    --json          Output as JSON
    --strict        Treat warnings as errors
    --compute-hash  Show computed body-sha256
    --help          Show help
    --version       Show version
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

from . import (
    __version__,
    validate,
    validate_cgd,
    validate_sot,
    detect_type,
    ValidationResult,
    ValidateOptions,
)


# ANSI colors
class Colors:
    RESET = "\x1b[0m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    DIM = "\x1b[2m"
    BOLD = "\x1b[1m"


def color(c: str, text: str, no_color: bool = False) -> str:
    """Apply ANSI color to text."""
    if no_color:
        return text
    return f"{c}{text}{Colors.RESET}"


def format_error(err, show_line: bool = True, no_color: bool = False) -> str:
    """Format a validation error for display."""
    if err.severity == "error":
        severity = color(Colors.RED, "ERROR", no_color)
    else:
        severity = color(Colors.YELLOW, "WARN", no_color)

    code = color(Colors.DIM, f"[{err.code}]", no_color)
    line = color(Colors.DIM, f":{err.line}", no_color) if show_line and err.line else ""

    return f"  {severity} {code}{line} {err.message}"


def print_result(
    result: ValidationResult,
    file_path: str,
    json_output: bool = False,
    compute_hash: bool = False,
    no_color: bool = False,
) -> None:
    """Print validation result."""
    if json_output:
        output = {
            "file": file_path,
            "valid": result.valid,
            "documentType": result.document_type,
            "errors": [
                {
                    "code": e.code,
                    "severity": e.severity,
                    "message": e.message,
                    "line": e.line,
                }
                for e in result.errors
            ],
            "warnings": [
                {
                    "code": w.code,
                    "severity": w.severity,
                    "message": w.message,
                    "line": w.line,
                }
                for w in result.warnings
            ],
        }

        if result.computed:
            output["computed"] = {
                "ragIngestable": result.computed.rag_ingestable,
                "bodyHash": result.computed.body_hash,
                "exclusionsCoverage": result.computed.exclusions_coverage,
            }

        print(json.dumps(output, indent=2))
        return

    # Human-readable output
    if result.valid:
        status = color(Colors.GREEN, "✓ VALID", no_color)
    else:
        status = color(Colors.RED, "✗ INVALID", no_color)

    doc_type = color(Colors.DIM, f"({result.document_type})", no_color)
    print(f"\n{color(Colors.BOLD, file_path, no_color)} {doc_type} {status}\n")

    if result.errors:
        print(color(Colors.RED, f"{len(result.errors)} error(s):", no_color))
        for err in result.errors:
            print(format_error(err, no_color=no_color))
        print()

    if result.warnings:
        print(color(Colors.YELLOW, f"{len(result.warnings)} warning(s):", no_color))
        for warn in result.warnings:
            print(format_error(warn, no_color=no_color))
        print()

    if result.computed:
        print(color(Colors.BLUE, "Computed fields:", no_color))
        print(f"  rag-ingestable: {result.computed.rag_ingestable}")

        if compute_hash and result.computed.body_hash:
            print(f"  body-sha256: {result.computed.body_hash}")

        if (
            result.computed.exclusions_coverage is not None
            and result.computed.exclusions_coverage > 0
        ):
            print(f"  exclusions-coverage: {result.computed.exclusions_coverage * 100:.1f}%")
        print()


def read_file(file_path: str) -> str:
    """Read file content."""
    path = Path(file_path)
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(2)
    except PermissionError:
        print(f"Error: Permission denied: {file_path}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(2)


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="clarity-gate",
        description="Pre-ingestion verification for RAG systems",
    )
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--compute-hash", action="store_true", help="Show computed body-sha256")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # check command
    check_parser = subparsers.add_parser("check", help="Auto-detect and validate")
    check_parser.add_argument("file", help="File to validate")

    # validate-cgd command
    cgd_parser = subparsers.add_parser("validate-cgd", help="Validate as CGD")
    cgd_parser.add_argument("file", help="File to validate")

    # validate-sot command
    sot_parser = subparsers.add_parser("validate-sot", help="Validate as SOT")
    sot_parser.add_argument("file", help="File to validate")

    # detect command
    detect_parser = subparsers.add_parser("detect", help="Detect document type")
    detect_parser.add_argument("file", help="File to detect")

    args = parser.parse_args()

    # Check for NO_COLOR environment variable
    no_color = args.no_color or bool(os.environ.get("NO_COLOR"))

    if args.version:
        print(f"clarity-gate v{__version__}")
        return 0

    if not args.command:
        parser.print_help()
        return 2

    file_path = args.file
    content = read_file(file_path)
    options = ValidateOptions(strict=args.strict)

    result: Optional[ValidationResult] = None

    if args.command == "check":
        result = validate(content, options)

    elif args.command == "validate-cgd":
        result = validate_cgd(content, options)

    elif args.command == "validate-sot":
        result = validate_sot(content, options)

    elif args.command == "detect":
        doc_type = detect_type(content)
        if args.json:
            print(json.dumps({"file": file_path, "type": doc_type}))
        else:
            print(f"{file_path}: {doc_type}")
        return 0

    if result:
        print_result(
            result,
            file_path,
            json_output=args.json,
            compute_hash=args.compute_hash,
            no_color=no_color,
        )
        return 0 if result.valid else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())