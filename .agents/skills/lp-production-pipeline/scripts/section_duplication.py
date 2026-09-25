#!/usr/bin/env python3
"""Deterministic evidence checks for cross-section LP duplication."""

from __future__ import annotations

import html as html_module
import re
import unicodedata
from collections import defaultdict


SECTION_IDS = ("hero", "problems", "solution", "use-cases", "process", "final-cta")
DUPLICATION_AUDIT_MARKER = "SECTION_DUPLICATION_AUDIT: PASS"
MIN_DUPLICATE_BLOCK_CHARACTERS = 14


def _normalized_text(fragment: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", fragment)
    decoded = html_module.unescape(without_tags)
    normalized = unicodedata.normalize("NFKC", decoded)
    return re.sub(r"\s+", "", normalized).strip()


def find_exact_cross_section_duplicates(page_html: str) -> list[tuple[str, tuple[str, ...]]]:
    """Return meaningful text blocks copied verbatim across different sections."""
    occurrences: dict[str, set[str]] = defaultdict(set)
    for section_id in SECTION_IDS:
        section = re.search(
            rf"<section\b[^>]*\bid=[\"']{re.escape(section_id)}[\"'][^>]*>(.*?)</section>",
            page_html,
            flags=re.I | re.S,
        )
        if not section:
            continue
        for block in re.findall(
            r"<(?:h[1-6]|p|li|dt|dd)\b[^>]*>.*?</(?:h[1-6]|p|li|dt|dd)>",
            section.group(1),
            flags=re.I | re.S,
        ):
            if "data-line-cta" in block:
                continue
            text = _normalized_text(block)
            if len(text) >= MIN_DUPLICATE_BLOCK_CHARACTERS:
                occurrences[text].add(section_id)

    return sorted(
        (text, tuple(sorted(section_ids)))
        for text, section_ids in occurrences.items()
        if len(section_ids) > 1
    )


def validate_html_section_duplication(page_html: str, label: str, errors: list[str]) -> None:
    for section_id in SECTION_IDS:
        if not re.search(
            rf"<section\b[^>]*\bid=[\"']{re.escape(section_id)}[\"'][^>]*>",
            page_html,
            flags=re.I | re.S,
        ):
            errors.append(
                f"{label}: fixed id {section_id} must be assigned to a section element"
            )
    for text, section_ids in find_exact_cross_section_duplicates(page_html):
        preview = text[:40] + ("…" if len(text) > 40 else "")
        errors.append(
            f"{label}: exact cross-section copy is duplicated in {', '.join(section_ids)}: {preview}"
        )


def validate_section_role_audit(copy: dict, errors: list[str]) -> None:
    """Require the copy owner to record a six-section semantic responsibility audit."""
    audit = copy.get("section_role_audit")
    if not isinstance(audit, dict):
        errors.append("content/lp-copy.json: section_role_audit is missing")
        return

    if audit.get("status") != "PASS":
        errors.append("content/lp-copy.json: section_role_audit status is not PASS")

    reviewed = audit.get("reviewed_sections")
    if reviewed != list(SECTION_IDS):
        errors.append(
            "content/lp-copy.json: section_role_audit reviewed_sections must list all six sections in contract order"
        )

    roles = audit.get("unique_roles")
    if not isinstance(roles, dict) or set(roles) != set(SECTION_IDS):
        errors.append("content/lp-copy.json: section_role_audit unique_roles must cover exactly all six sections")
    else:
        normalized_roles: list[str] = []
        for section_id in SECTION_IDS:
            role = roles.get(section_id)
            if not isinstance(role, str) or len(_normalized_text(role)) < 6:
                errors.append(
                    f"content/lp-copy.json: section_role_audit unique role for {section_id} is missing or too vague"
                )
                continue
            normalized_roles.append(_normalized_text(role))
        if len(normalized_roles) == len(SECTION_IDS) and len(set(normalized_roles)) != len(SECTION_IDS):
            errors.append("content/lp-copy.json: section_role_audit contains repeated section roles")

    if not isinstance(audit.get("removed_or_moved_overlaps"), list):
        errors.append("content/lp-copy.json: section_role_audit removed_or_moved_overlaps must be an array")

    standalone = audit.get("standalone_context_blocks")
    if standalone != []:
        errors.append(
            "content/lp-copy.json: section_role_audit standalone_context_blocks must be an empty array"
        )


def validate_review_duplication_marker(review: dict, label: str, errors: list[str]) -> None:
    evidence = review.get("evidence")
    if not isinstance(evidence, list):
        errors.append(f"{label}: evidence must be an array")
        return
    audit_entries = [
        item for item in evidence
        if isinstance(item, str) and item.startswith(DUPLICATION_AUDIT_MARKER)
    ]
    if len(audit_entries) != 1:
        errors.append(
            f"{label}: requires exactly one {DUPLICATION_AUDIT_MARKER} evidence entry"
        )
        return
    missing = [section_id for section_id in SECTION_IDS if section_id not in audit_entries[0]]
    if missing:
        errors.append(
            f"{label}: duplication audit marker is missing section ids: {', '.join(missing)}"
        )
