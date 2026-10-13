#!/usr/bin/env python3
"""Check resource structure; does not substitute for Designer/runtime validation."""
import argparse
import json
import sys
from project_lib import ProjectError, load_files, validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Project directory or export ZIP")
    parser.add_argument("--strict", action="store_true", help="Return failure for warnings as well as errors")
    args = parser.parse_args()
    try:
        result = validate(load_files(args.source))
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] and not (args.strict and result["issues"]) else 1
    except ProjectError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
