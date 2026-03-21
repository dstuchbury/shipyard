from __future__ import annotations

import argparse
import sys

from shipyard.adopt import run_adopt
from shipyard.docker import (
    attach_project,
    down_all,
    down_project,
    restart_project,
    rebuild_project,
    list_status,
    up_core,
    up_project,
    restart_core,
    rebuild_core,
)
from shipyard.init import run_init
from shipyard.banner import print_banner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shipyard",
        description="Shipyard - Local Laravel Runtime Manager"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialise the Shipyard runtime")

    adopt_parser = subparsers.add_parser("adopt", help="Adopt a Laravel project into Shipyard")
    adopt_parser.add_argument("path", help="Path to the Laravel project")

    up_parser = subparsers.add_parser("up", help="Start Shipyard core runtime or a project")
    up_parser.add_argument("project", nargs="?", help="Optional project slug")

    up_parser = subparsers.add_parser("restart", help="Restart Shipyard core runtime or a project")
    up_parser.add_argument("project", nargs="?", help="Optional project slug")

    up_parser = subparsers.add_parser("rebuild", help="Rebuild Shipyard core runtime or a project")
    up_parser.add_argument("project", nargs="?", help="Optional project slug")

    down_parser = subparsers.add_parser(
        "down",
        help="Stop everything, or stop a specific project if provided",
    )
    down_parser.add_argument("project", nargs="?", help="Optional project slug")

    attach_parser = subparsers.add_parser(
        "attach",
        help="Open a shell inside an adopted project service container",
    )
    attach_parser.add_argument("project", help="Project slug")
    attach_parser.add_argument("service", nargs="?", help="Optional service alias")

    subparsers.add_parser("list", help="Show Shipyard core and project runtime status")

    return parser


def main() -> int:
    parser = build_parser()
    # If no arguments were supplied, show the banner.
    if len(sys.argv) == 1:
        print_banner()
        return 0

    args = parser.parse_args()

    try:
        if args.command == "init":
            run_init()
            return 0

        if args.command == "adopt":
            run_adopt(args.path)
            return 0

        if args.command == "up":
            if args.project:
                up_project(args.project)
            else:
                up_core()
            return 0

        if args.command == "down":
            if args.project:
                down_project(args.project)
            else:
                down_all()
            return 0

        if args.command == "restart":
            if args.project:
                restart_project(args.project)
            else:
                restart_core()
            return 0

        if args.command == "rebuild":
            if args.project:
                rebuild_project(args.project)
            else:
                rebuild_core()
            return 0

        if args.command == "attach":
            attach_project(args.project, args.service)
            return 0

        if args.command == "list":
            list_status()
            return 0

        parser.print_help()
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
