#!/usr/bin/env python3
"""Inventory a single Perspective project directory or export ZIP."""
import argparse
import json
import sys
from project_lib import ProjectError, inspect, load_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Project directory or export ZIP")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(load_files(args.source)), indent=2))
    except ProjectError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
