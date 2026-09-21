from __future__ import annotations

import argparse
import json
from pathlib import Path

from genesis.core import Coordinator
from genesis.evaluation import IndependentEvaluator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="genesis", description="Run reproducible GENESIS AI experiments.")
    parser.add_argument("--version", action="version", version="genesis 0.1.0.dev0")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init", help="create the local GENESIS directory")
    run = subparsers.add_parser("run", help="run one offline baseline experiment")
    run.add_argument("--root", default=".genesis")
    status = subparsers.add_parser("status", help="list stored experiments")
    status.add_argument("--root", default=".genesis")
    dashboard = subparsers.add_parser("dashboard", help="open the local visual dashboard")
    dashboard.add_argument("--root", default=".genesis")
    dashboard.add_argument("--host", default="127.0.0.1")
    dashboard.add_argument("--port", type=int, default=8765)
    experiment = subparsers.add_parser("experiment", help="inspect one experiment")
    experiment.add_argument("experiment_id")
    experiment.add_argument("--root", default=".genesis")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init":
        Path(".genesis/artifacts").mkdir(parents=True, exist_ok=True)
        print("Initialized .genesis")
        return 0
    if args.command == "run":
        result = Coordinator(args.root).run_once()
        print(json.dumps(result, indent=2, default=str))
        return 0
    if args.command == "status":
        print(json.dumps(Coordinator(args.root).db.list_experiments(), indent=2, default=str))
        return 0
    if args.command == "dashboard":
        from genesis.ui import serve

        serve(args.root, args.host, args.port)
        return 0
    if args.command == "experiment":
        record = Coordinator(args.root).db.get_experiment(args.experiment_id)
        if record is None:
            print(f"Experiment not found: {args.experiment_id}")
            return 1
        print(json.dumps(record, indent=2, default=str))
        return 0
    print("GENESIS foundation is ready. Use `genesis run` to execute the offline baseline.")
    return 0
