#!/usr/bin/env python3
"""Validate a completed fixed-format LP production run."""

from __future__ import annotations

import argparse
import hashlib
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
    "review.md",
    "pipeline-state.json",
    "research/references.md",
    "strategy/marketing-brief.md",
    "content/lp-copy.json",
    "assets/fonts/NotoSansJP-Variable.ttf",
    "assets/fonts/OFL.txt",
    "design/wireframe.html",
    "design/wireframe.png",
    "design/wireframe-spec.json",
    "design/prototype/index.html",
    "design/prototype/styles.css",
    "design/desktop.png",
    "design/mobile.png",
    "design/design-spec.json",
    "design/assets-manifest.json",
    "implementation/screenshots/desktop.png",
    "implementation/screenshots/mobile.png",
    "implementation/render-evidence.json",
    "reviews/creative-source-review.json",
    "reviews/creative-review.json",
    "reviews/implementation-review.json",
)
JAPANESE_FONT_SHA256 = "c2f3b4d463500a2ddcd3849cded1fceeb9fd6d1c32e6cbecd568453ba50fc68f"
SECTION_IDS = ("hero", "problems", "solution", "use-cases", "process", "final-cta")
PNG_FILES = (
    "design/wireframe.png",
    "design/desktop.png",
    "design/mobile.png",
    "implementation/screenshots/desktop.png",
    "implementation/screenshots/mobile.png",
)
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

    root = (args.target_workspace.resolve() / output_rel).resolve()
    workspace = args.target_workspace.resolve()
    if workspace not in root.parents:
        errors.append("output_dir escapes the target workspace")

    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {relative}")

    references_path = root / "research" / "references.md"
    if references_path.is_file():
        check_required_references(references_path, errors)

    for relative in PNG_FILES:
        path = root / relative
        if path.is_file():
            data = path.read_bytes()
            if len(data) < 1024 or not data.startswith(b"\x89PNG\r\n\x1a\n"):
                errors.append(f"invalid PNG: {relative}")

    font_path = root / "assets" / "fonts" / "NotoSansJP-Variable.ttf"
    if font_path.is_file():
        font_sha256 = hashlib.sha256(font_path.read_bytes()).hexdigest()
        if font_sha256 != JAPANESE_FONT_SHA256:
            errors.append("assets/fonts/NotoSansJP-Variable.ttf: unexpected SHA-256")

    for relative in ("styles.css", "design/prototype/styles.css"):
        css_path = root / relative
        if css_path.is_file():
            css = css_path.read_text(encoding="utf-8")
            if 'font-family: "LP Noto Sans JP"' not in css or "NotoSansJP-Variable.ttf" not in css:
                errors.append(f"{relative}: bundled Japanese font is not configured")

    wireframe_path = root / "design" / "wireframe.html"
    if wireframe_path.is_file():
        wireframe_html = wireframe_path.read_text(encoding="utf-8")
        if "data-lp-factory-japanese-font" not in wireframe_html:
            errors.append("design/wireframe.html: bundled Japanese font is not configured")

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
        ("reviews/creative-source-review.json", "creative"),
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

    render_evidence_path = root / "implementation" / "render-evidence.json"
    if render_evidence_path.is_file():
        try:
            render_evidence = load_json(render_evidence_path)
            if render_evidence.get("pass") is not True:
                errors.append("implementation/render-evidence.json: render checks did not pass")
            if len(render_evidence.get("results", [])) != 5:
                errors.append("implementation/render-evidence.json: expected five captures")
            renderer_font = render_evidence.get("renderer", {}).get("japaneseFont", {})
            if renderer_font.get("sha256") != JAPANESE_FONT_SHA256:
                errors.append("implementation/render-evidence.json: Japanese font evidence is missing or invalid")
            for result in render_evidence.get("results", []):
                dom = result.get("dom", {})
                if dom.get("japaneseFontReady") is not True:
                    errors.append(f"implementation/render-evidence.json: Japanese font was not ready for {result.get('name', 'unknown capture')}")
                if "LP Noto Sans JP" not in str(dom.get("bodyFontFamily", "")):
                    errors.append(f"implementation/render-evidence.json: Japanese font was not applied for {result.get('name', 'unknown capture')}")
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

    asset_manifest_path = root / "design" / "assets-manifest.json"
    if asset_manifest_path.is_file():
        try:
            validate_visual_assets(root, load_json(asset_manifest_path), errors)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    review_summary = root / "review.md"
    if review_summary.is_file() and "APPROVAL_STATUS: pending" not in review_summary.read_text(encoding="utf-8"):
        errors.append("review.md must contain APPROVAL_STATUS: pending")

    if errors:
        print("LP run validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "job_id": job_id, "output_dir": str(root)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
