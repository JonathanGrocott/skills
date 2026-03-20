#!/usr/bin/env python3
"""Validate WebPresentationTemplate structure and references."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SLIDE_ID_RE = re.compile(r'id="(slide-(\d+))"')
NAV_DOT_RE = re.compile(
    r'<button[^>]*class="[^"]*nav-dot[^"]*"[^>]*data-slide="(\d+)"[^>]*aria-label="Slide\s+(\d+)"',
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check slide sequencing, nav-dot mapping, slide-config references, "
            "and asset naming rules for WebPresentationTemplate."
        )
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Path to the presentation project root (default: current directory).",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Unable to read {path}: {exc}") from exc


def check_slide_ids(index_html: str, errors: list[str]) -> set[str]:
    slide_numbers = [int(match.group(2)) for match in SLIDE_ID_RE.finditer(index_html)]

    if not slide_numbers:
        errors.append("No slide IDs found in index.html.")
        return set()

    expected = list(range(1, len(slide_numbers) + 1))
    if slide_numbers != expected:
        errors.append(
            "Slide IDs are not strictly sequential starting at 1. "
            f"Found: {slide_numbers}; expected: {expected}."
        )

    # Preserve exact labels for downstream validation.
    return {f"slide-{n}" for n in slide_numbers}


def check_nav_dots(index_html: str, slide_count: int, errors: list[str]) -> None:
    matches = NAV_DOT_RE.findall(index_html)

    if len(matches) != slide_count:
        errors.append(
            f"Nav-dot count ({len(matches)}) does not match slide count ({slide_count})."
        )
        # Continue checking what we can.

    data_values = [int(data_slide) for data_slide, _ in matches]
    label_values = [int(aria_label) for _, aria_label in matches]

    expected_data = list(range(len(matches)))
    if data_values != expected_data:
        errors.append(
            "Nav-dot data-slide values are not sequential 0-indexed. "
            f"Found: {data_values}; expected: {expected_data}."
        )

    expected_labels = [i + 1 for i in range(len(matches))]
    if label_values != expected_labels:
        errors.append(
            "Nav-dot aria-label values are not sequential 1-indexed. "
            f"Found: {label_values}; expected: {expected_labels}."
        )


def uncommented_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        stripped = raw.lstrip()
        if stripped.startswith("//"):
            continue
        # Remove trailing line comments; adequate for this config format.
        no_comment = re.sub(r"//.*$", "", raw)
        if no_comment.strip():
            lines.append(no_comment)
    return lines


def check_slide_config(slide_config_text: str, known_slide_ids: set[str], errors: list[str]) -> None:
    for line in uncommented_lines(slide_config_text):
        for match in re.finditer(r"\bslide-(\d+)\b", line):
            slide_id = f"slide-{match.group(1)}"
            if slide_id not in known_slide_ids:
                errors.append(
                    "slide-config.js references missing slide ID "
                    f"'{slide_id}' in line: {line.strip()}"
                )


def is_camel_case_filename(path: Path) -> bool:
    stem = path.stem
    return bool(re.match(r"^[a-z][A-Za-z0-9]*$", stem))


def check_assets(project_root: Path, errors: list[str]) -> None:
    for relative_dir in ("assets/images", "assets/video"):
        asset_dir = project_root / relative_dir
        if not asset_dir.exists():
            continue

        for file_path in sorted(p for p in asset_dir.rglob("*") if p.is_file()):
            if " " in file_path.name or not is_camel_case_filename(file_path):
                errors.append(
                    "Asset filename must be camelCase with no spaces: "
                    f"{file_path.relative_to(project_root)}"
                )


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    index_path = project_root / "index.html"
    config_path = project_root / "js" / "slide-config.js"

    errors: list[str] = []

    if not index_path.exists():
        errors.append(f"Missing required file: {index_path}")
    if not config_path.exists():
        errors.append(f"Missing required file: {config_path}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    index_html = read_text(index_path)
    slide_config = read_text(config_path)

    known_slide_ids = check_slide_ids(index_html, errors)
    check_nav_dots(index_html, len(known_slide_ids), errors)
    check_slide_config(slide_config, known_slide_ids, errors)
    check_assets(project_root, errors)

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("OK: Presentation structure is consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
