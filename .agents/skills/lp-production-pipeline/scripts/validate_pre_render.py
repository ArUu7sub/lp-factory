#!/usr/bin/env python3
"""Validate deterministic LP source before trusted browser rendering."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from asset_policy import validate_visual_assets


REQUIRED_FILES = (
    "index.html",
    "styles.css",
    "script.js",
    "content.json",
    "pipeline-state.json",
    "research/references.md",
    "strategy/marketing-brief.md",
    "content/lp-copy.json",
    "design/wireframe.html",
    "design/wireframe-spec.json",
    "design/prototype/index.html",
    "design/prototype/styles.css",
    "design/design-spec.json",
    "design/assets-manifest.json",
    "reviews/creative-source-review.json",
)
SECTION_IDS = ("hero", "problems", "solution", "use-cases", "process", "final-cta")
REQUIRED_REFERENCE_MARKERS = {
    "SANKOU!": "sankoudesign.com",
    "81-web.com": "81-web.com",
    "Web Design Clip": "webdesignclip.com",
    "ちょうどいいWebデザインギャラリー": "choooodoii.com",
    "21st.dev": "21st.dev",
    "Xserver wireframe guide": "xserver.ne.jp/bizhp/homepage-wire-frame",
    "Pinterest wireframe board": "pinterest.com",
    "Google wireframe image search": "google.com/search",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def check_html(path: Path, label: str, errors: list[str]) -> None:
    html = path.read_text(encoding="utf-8")
    positions: list[int] = []
    for section_id in SECTION_IDS:
        match = re.search(rf'\bid=["\']{re.escape(section_id)}["\']', html)
        if not match:
            errors.append(f"{label}: missing section id {section_id}")
        else:
            positions.append(match.start())
    if positions and positions != sorted(positions):
        errors.append(f"{label}: section ids are out of order")
    if "file://" in html:
        errors.append(f"{label}: contains file:// URL")


def check_required_references(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8").lower()
    for label, marker in REQUIRED_REFERENCE_MARKERS.items():
        if marker.lower() not in text:
            errors.append(f"research/references.md: missing required source record for {label}")


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

    workspace = args.target_workspace.resolve()
    root = (workspace / output_rel).resolve()
    if workspace not in root.parents:
        errors.append("output_dir escapes the target workspace")

    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {relative}")

    for relative, label in (
        ("index.html", "public implementation"),
        ("design/wireframe.html", "wireframe source"),
        ("design/prototype/index.html", "design prototype"),
    ):
        path = root / relative
        if path.is_file():
            check_html(path, label, errors)

    references_path = root / "research" / "references.md"
    if references_path.is_file():
        check_required_references(references_path, errors)

    html_path = root / "index.html"
    if html_path.is_file():
        html = html_path.read_text(encoding="utf-8")
        line_links = re.findall(r"<a\b[^>]*data-line-cta[^>]*>", html, flags=re.I)
        if not line_links:
            errors.append("no data-line-cta link found")
        for link in line_links:
            href = re.search(r'\bhref=["\']([^"\']*)["\']', link, flags=re.I)
            if href and href.group(1) not in ("", "#"):
                errors.append("LINE CTA URL must remain empty or #")

    review_path = root / "reviews" / "creative-source-review.json"
    if review_path.is_file():
        try:
            review = load_json(review_path)
            if review.get("gate") != "creative":
                errors.append("creative-source-review.json: incorrect gate")
            if review.get("status") != "PASS":
                errors.append("creative-source-review.json: review is not PASS")
            if review.get("blockingIssues"):
                errors.append("creative-source-review.json: blocking issues remain")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    state_path = root / "pipeline-state.json"
    if state_path.is_file():
        try:
            state = load_json(state_path)
            if state.get("jobId") != job_id:
                errors.append("pipeline-state jobId does not match")
            if state.get("status") != "awaiting_render_review":
                errors.append("pipeline-state status is not awaiting_render_review")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    generated_assets = root / "assets" / "generated"
    if not generated_assets.is_dir() or not any(generated_assets.iterdir()):
        errors.append("assets/generated contains no generated assets")

    asset_manifest_path = root / "design" / "assets-manifest.json"
    if asset_manifest_path.is_file():
        try:
            validate_visual_assets(root, load_json(asset_manifest_path), errors)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    if errors:
        print("LP pre-render validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "job_id": job_id, "output_dir": str(root)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
