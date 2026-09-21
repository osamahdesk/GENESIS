from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="genesis",
        description="Run reproducible GENESIS AI experiments.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="genesis 0.1.0.dev0",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    print("GENESIS foundation is ready. Follow docs/daily/day-01-foundation.md.")
    return 0
