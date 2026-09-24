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
FORBIDDEN_PUBLIC_COPY = ("公式LINEのリンクは準備中です。", "公式LINEは準備中です。")
FORBIDDEN_NAV_COPY = ("ページの先頭", "TOPへ", "トップへ")
SHARED_NAVIGATION = (
    ("できること", "#solution"),
    ("活用例", "#use-cases"),
    ("利用の流れ", "#process"),
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
    for phrase in FORBIDDEN_PUBLIC_COPY:
        if phrase in html:
            errors.append(f"{label}: contains forbidden LINE preparation notice")
    if "data-balanced-heading" not in html:
        errors.append(f"{label}: Hero heading is missing data-balanced-heading")
    for phrase in FORBIDDEN_NAV_COPY:
        if phrase in html:
            errors.append(f"{label}: contains forbidden back-to-top copy {phrase}")
    if "site-header-shell" not in html:
        errors.append(f"{label}: sticky header shell is missing")
    header = re.search(r"<header\b[^>]*class=[\"'][^\"']*site-header[^\"']*[\"'][^>]*>(.*?)</header>", html, flags=re.I | re.S)
    if not header:
        errors.append(f"{label}: missing fixed site-header")
    else:
        header_html = header.group(1)
        for expected in ("24H", "AI", "できること", "活用例", "利用の流れ", '#solution', '#use-cases', '#process'):
            if expected not in header_html:
                errors.append(f"{label}: fixed header is missing {expected}")
    footer = re.search(r"<footer\b[^>]*class=[\"'][^\"']*site-footer[^\"']*[\"'][^>]*>(.*?)</footer>", html, flags=re.I | re.S)
    if not footer:
        errors.append(f"{label}: missing shared site-footer")
    else:
        footer_html = footer.group(1)
        for expected in ("24H", "AI"):
            if expected not in footer_html:
                errors.append(f"{label}: shared footer is missing {expected}")
        for nav_label, nav_target in SHARED_NAVIGATION:
            if nav_label not in footer_html or nav_target not in footer_html:
                errors.append(f"{label}: shared footer is missing {nav_label} ({nav_target})")
    if "mini-flow" in html:
        flow_container = re.search(r"<ol\b[^>]*class=[\"'][^\"']*mini-flow[^\"']*[\"'][^>]*>(.*?)</ol>", html, flags=re.I | re.S)
        flow_items = re.findall(r"<li\b[^>]*>.*?</li>", flow_container.group(1), flags=re.I | re.S) if flow_container else []
        if len(flow_items) < 3:
            errors.append(f"{label}: Hero overview needs at least three stages")
        for index, item in enumerate(flow_items, start=1):
            if "flow-step-number" not in item or "<strong" not in item or "<small" not in item:
                errors.append(f"{label}: Hero overview stage {index} needs a number, label, and action/outcome")


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

    for relative in ("styles.css", "design/prototype/styles.css"):
        css_path = root / relative
        if css_path.is_file():
            css = css_path.read_text(encoding="utf-8")
            if ".balanced-heading" not in css or "text-wrap:balance" not in css.replace(" ", ""):
                errors.append(f"{relative}: phrase-aware heading rules are missing")
            normalized_css = re.sub(r"\s+", "", css.lower())
            if ".site-header-shell" not in css or "position:sticky" not in normalized_css:
                errors.append(f"{relative}: shared header is not sticky")
            if ".site-footer-inner" not in css:
                errors.append(f"{relative}: shared footer layout rules are missing")
            if ".mini-flow" in css and "grid-template-columns:1fr" not in normalized_css:
                errors.append(f"{relative}: mobile Hero overview is not a vertical sequence")

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
