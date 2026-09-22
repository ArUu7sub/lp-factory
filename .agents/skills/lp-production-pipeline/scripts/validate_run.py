#!/usr/bin/env python3
"""Validate a completed fixed-format LP production run."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "index.html",
    "styles.css",
    "script.js",
    "content.json",
    "review.md",
    "pipeline-state.json",
    "research/references.md",
    "strategy/marketing-brief.md",
    "content/lp-copy.json",
    "design/wireframe.png",
    "design/wireframe-spec.json",
    "design/desktop.png",
    "design/mobile.png",
    "design/design-spec.json",
    "design/assets-manifest.json",
    "implementation/screenshots/desktop.png",
    "implementation/screenshots/mobile.png",
    "reviews/creative-review.json",
    "reviews/implementation-review.json",
)
SECTION_IDS = ("hero", "problems", "solution", "use-cases", "process", "final-cta")
PNG_FILES = (
    "design/wireframe.png",
    "design/desktop.png",
    "design/mobile.png",
    "implementation/screenshots/desktop.png",
    "implementation/screenshots/mobile.png",
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("job_file", type=Path)
    parser.add_argument("target_workspace", type=Path)
    args = parser.parse_args()

    job = load_json(args.job_file.resolve())
    job_id = str(job.get("job_id", ""))
    output_rel = Path(str(job.get("output_dir", "")))
    expected_rel = Path("generated") / job_id
    errors: list[str] = []

    if not job_id:
        errors.append("job_id is missing")
    if output_rel != expected_rel:
        errors.append(f"output_dir must be {expected_rel}, got {output_rel}")

    root = (args.target_workspace.resolve() / output_rel).resolve()
    workspace = args.target_workspace.resolve()
    if workspace not in root.parents:
        errors.append("output_dir escapes the target workspace")

    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {relative}")

    for relative in PNG_FILES:
        path = root / relative
        if path.is_file():
            data = path.read_bytes()
            if len(data) < 1024 or not data.startswith(b"\x89PNG\r\n\x1a\n"):
                errors.append(f"invalid PNG: {relative}")

    html_path = root / "index.html"
    if html_path.is_file():
        html = html_path.read_text(encoding="utf-8")
        positions = []
        for section_id in SECTION_IDS:
            match = re.search(rf'\bid=["\']{re.escape(section_id)}["\']', html)
            if not match:
                errors.append(f"missing section id: {section_id}")
            else:
                positions.append(match.start())
        if positions and positions != sorted(positions):
            errors.append("section ids are out of order")
        if "file://" in html:
            errors.append("public HTML contains file:// URL")
        line_links = re.findall(r"<a\b[^>]*data-line-cta[^>]*>", html, flags=re.I)
        if not line_links:
            errors.append("no data-line-cta link found")
        for link in line_links:
            href = re.search(r'\bhref=["\']([^"\']*)["\']', link, flags=re.I)
            if href and href.group(1) not in ("", "#"):
                errors.append("LINE CTA URL must remain empty or #")

    for relative, gate in (
        ("reviews/creative-review.json", "creative"),
        ("reviews/implementation-review.json", "implementation"),
    ):
        path = root / relative
        if path.is_file():
            try:
                review = load_json(path)
                if review.get("gate") != gate:
                    errors.append(f"{relative}: incorrect gate")
                if review.get("status") != "PASS":
                    errors.append(f"{relative}: review is not PASS")
                if review.get("blockingIssues"):
                    errors.append(f"{relative}: blocking issues remain")
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                errors.append(str(exc))

    state_path = root / "pipeline-state.json"
    if state_path.is_file():
        try:
            state = load_json(state_path)
            if state.get("jobId") != job_id:
                errors.append("pipeline-state jobId does not match")
            if state.get("status") != "ready_for_preview":
                errors.append("pipeline-state status is not ready_for_preview")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    generated_assets = root / "assets" / "generated"
    if not generated_assets.is_dir() or not any(generated_assets.iterdir()):
        errors.append("assets/generated contains no generated assets")

    if errors:
        print("LP run validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "job_id": job_id, "output_dir": str(root)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

