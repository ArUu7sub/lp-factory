#!/usr/bin/env python3

from __future__ import annotations

import unittest

from section_duplication import (
    DUPLICATION_AUDIT_MARKER,
    SECTION_IDS,
    find_exact_cross_section_duplicates,
    validate_html_section_duplication,
    validate_review_duplication_marker,
    validate_section_role_audit,
)


def page(blocks: dict[str, str]) -> str:
    return "".join(
        f'<section id="{section_id}"><p>{blocks.get(section_id, section_id + "固有の説明テキストです")}</p></section>'
        for section_id in SECTION_IDS
    )


class SectionDuplicationTests(unittest.TestCase):
    def test_exact_copy_in_two_sections_is_blocking(self) -> None:
        repeated = "参加者の予約から視聴後フォローまでを順番につなぎます"
        duplicates = find_exact_cross_section_duplicates(
            page({"hero": repeated, "process": repeated})
        )
        self.assertEqual([(repeated, ("hero", "process"))], duplicates)

    def test_distinct_section_copy_passes(self) -> None:
        self.assertEqual([], find_exact_cross_section_duplicates(page({})))

    def test_fixed_id_on_div_cannot_bypass_section_gate(self) -> None:
        invalid = page({}).replace(
            '<section id="hero"><p>',
            '<div id="hero"><p>',
        ).replace(
            '</p></section><section id="problems">',
            '</p></div><section id="problems">',
            1,
        )
        errors: list[str] = []
        validate_html_section_duplication(invalid, "public HTML", errors)
        self.assertIn(
            "public HTML: fixed id hero must be assigned to a section element",
            errors,
        )

    def test_structured_role_audit_requires_distinct_six_roles(self) -> None:
        errors: list[str] = []
        validate_section_role_audit(
            {
                "section_role_audit": {
                    "status": "PASS",
                    "reviewed_sections": list(SECTION_IDS),
                    "unique_roles": {
                        section_id: f"{section_id}だけが担う固有の情報責任"
                        for section_id in SECTION_IDS
                    },
                    "removed_or_moved_overlaps": [],
                    "standalone_context_blocks": [],
                }
            },
            errors,
        )
        self.assertEqual([], errors)

    def test_structured_role_audit_blocks_standalone_context_copy(self) -> None:
        errors: list[str] = []
        validate_section_role_audit(
            {
                "section_role_audit": {
                    "status": "PASS",
                    "reviewed_sections": list(SECTION_IDS),
                    "unique_roles": {
                        section_id: f"{section_id}だけが担う固有の情報責任"
                        for section_id in SECTION_IDS
                    },
                    "removed_or_moved_overlaps": [],
                    "standalone_context_blocks": ["全業種対応の補足帯"],
                }
            },
            errors,
        )
        self.assertIn(
            "content/lp-copy.json: section_role_audit standalone_context_blocks must be an empty array",
            errors,
        )

    def test_review_requires_one_complete_audit_marker(self) -> None:
        errors: list[str] = []
        marker = f"{DUPLICATION_AUDIT_MARKER} — " + ", ".join(SECTION_IDS)
        validate_review_duplication_marker({"evidence": [marker]}, "review.json", errors)
        self.assertEqual([], errors)

        missing_errors: list[str] = []
        validate_review_duplication_marker({"evidence": []}, "review.json", missing_errors)
        self.assertTrue(missing_errors)


if __name__ == "__main__":
    unittest.main()
