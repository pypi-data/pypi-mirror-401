"""
jsonviewertool-cli
A tiny CLI for JSON validation/formatting/minifying and YAML->JSON conversion.

Website: https://jsonviewertool.com
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, TextIO


def _read_text(path: str | None, stdin: TextIO) -> str:
    if path and path != "-":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return stdin.read()


def _write_text(text: str) -> None:
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")


def cmd_validate(args: argparse.Namespace) -> int:
    raw = _read_text(args.file, sys.stdin)
    try:
        json.loads(raw)
        if not args.quiet:
            _write_text("✅ Valid JSON")
        return 0
    except json.JSONDecodeError as e:
        _write_text(f"❌ Invalid JSON: {e}")
        return 2


def cmd_format(args: argparse.Namespace) -> int:
    raw = _read_text(args.file, sys.stdin)
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        _write_text(f"❌ Invalid JSON: {e}")
        return 2

    indent = args.indent
    ensure_ascii = not args.unicode
    formatted = json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, sort_keys=args.sort_keys)
    _write_text(formatted)
    return 0


def cmd_minify(args: argparse.Namespace) -> int:
    raw = _read_text(args.file, sys.stdin)
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        _write_text(f"❌ Invalid JSON: {e}")
        return 2

    ensure_ascii = not args.unicode
    minified = json.dumps(obj, separators=(",", ":"), ensure_ascii=ensure_ascii)
    _write_text(minified)
    return 0


def cmd_yaml2json(args: argparse.Namespace) -> int:
    raw = _read_text(args.file, sys.stdin)
    try:
        import yaml  # type: ignore
    except Exception:
        _write_text(
            "❌ Missing dependency 'PyYAML'.\n"
            "Install it with: pip install jsonviewertool-cli[yaml]\n"
            "Or: pip install PyYAML"
        )
        return 3

    try:
        data: Any = yaml.safe_load(raw)
    except Exception as e:
        _write_text(f"❌ Invalid YAML: {e}")
        return 2

    ensure_ascii = not args.unicode
    indent = args.indent
    out = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, sort_keys=args.sort_keys)
    _write_text(out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="jsonviewertool",
        description="Validate/format/minify JSON and convert YAML → JSON. Website: https://jsonviewertool.com",
    )
    p.add_argument("--version", action="version", version="jsonviewertool-cli 0.1.0")

    sub = p.add_subparsers(dest="command", required=True)

    # validate
    pv = sub.add_parser("validate", help="Validate a JSON file (or stdin)")
    pv.add_argument("file", nargs="?", default="-", help="Path to JSON file or '-' for stdin")
    pv.add_argument("-q", "--quiet", action="store_true", help="Only return exit code")
    pv.set_defaults(func=cmd_validate)

    # format
    pf = sub.add_parser("format", help="Pretty-format JSON (or stdin)")
    pf.add_argument("file", nargs="?", default="-", help="Path to JSON file or '-' for stdin")
    pf.add_argument("-i", "--indent", type=int, default=2, help="Indent level (default: 2)")
    pf.add_argument("--sort-keys", action="store_true", help="Sort object keys")
    pf.add_argument("--unicode", action="store_true", help="Do not escape non-ASCII characters")
    pf.set_defaults(func=cmd_format)

    # minify
    pm = sub.add_parser("minify", help="Minify JSON (or stdin)")
    pm.add_argument("file", nargs="?", default="-", help="Path to JSON file or '-' for stdin")
    pm.add_argument("--unicode", action="store_true", help="Do not escape non-ASCII characters")
    pm.set_defaults(func=cmd_minify)

    # yaml2json
    py = sub.add_parser("yaml2json", help="Convert YAML → JSON (requires optional dependency)")
    py.add_argument("file", nargs="?", default="-", help="Path to YAML file or '-' for stdin")
    py.add_argument("-i", "--indent", type=int, default=2, help="Indent level (default: 2)")
    py.add_argument("--sort-keys", action="store_true", help="Sort object keys")
    py.add_argument("--unicode", action="store_true", help="Do not escape non-ASCII characters")
    py.set_defaults(func=cmd_yaml2json)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
