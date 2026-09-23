"""Validation for imagegen-backed LP visual assets."""

from __future__ import annotations

from pathlib import Path, PurePosixPath


SECTION_IDS = ("hero", "problems", "solution", "use-cases", "process", "final-cta")
HERO_LAYOUTS = {
    "split-text-left-visual-right",
    "centered-copy-over-background",
}
MOBILE_STRATEGIES = {"responsive-crop", "dedicated-asset"}
ASSET_DECISIONS = {"generated-image", "generated-background", "not-needed"}


def _combined_text(paths: list[Path]) -> str:
    parts: list[str] = []
    for path in paths:
        if path.is_file():
            parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


def validate_visual_assets(root: Path, manifest: dict, errors: list[str]) -> None:
    """Append visual-policy violations to ``errors``."""

    if manifest.get("schema_version") != "2.0":
        errors.append("design/assets-manifest.json: schema_version must be 2.0")
    if manifest.get("visual_policy_version") != 2:
        errors.append("design/assets-manifest.json: visual_policy_version must be 2")

    assets_value = manifest.get("assets")
    assets = assets_value if isinstance(assets_value, list) else []
    if not assets:
        errors.append("design/assets-manifest.json: assets must be a non-empty list")

    assets_by_id: dict[str, dict] = {}
    for index, asset in enumerate(assets):
        label = f"design/assets-manifest.json: assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{label} must be an object")
            continue
        asset_id = str(asset.get("id", "")).strip()
        if not asset_id:
            errors.append(f"{label} is missing id")
            continue
        if asset_id in assets_by_id:
            errors.append(f"design/assets-manifest.json: duplicate asset id {asset_id}")
        assets_by_id[asset_id] = asset

        generator = str(asset.get("generator", "")).lower()
        if "imagegen" not in generator and "image_gen" not in generator:
            errors.append(f"{label}: generator must be built-in imagegen")
        if asset.get("text_free") is not True:
            errors.append(f"{label}: text_free must be true")
        if asset.get("no_embedded_copy") is not True:
            errors.append(f"{label}: no_embedded_copy must be true")
        if not str(asset.get("prompt", "")).strip():
            errors.append(f"{label}: prompt is required")
        if not str(asset.get("safe_area", "")).strip():
            errors.append(f"{label}: safe_area is required")
        if not str(asset.get("crop_behavior", "")).strip():
            errors.append(f"{label}: crop_behavior is required")
        if not asset.get("width") or not asset.get("height"):
            errors.append(f"{label}: width and height are required")
        if len(str(asset.get("sha256", ""))) != 64:
            errors.append(f"{label}: sha256 is required")

        relative = str(asset.get("path", "")).strip()
        try:
            relative_path = PurePosixPath(relative)
        except TypeError:
            relative_path = PurePosixPath("")
        if relative_path.is_absolute() or ".." in relative_path.parts:
            errors.append(f"{label}: path must be a safe relative path")
        elif not relative.startswith("assets/generated/"):
            errors.append(f"{label}: path must be under assets/generated/")
        else:
            disk_path = root.joinpath(*relative_path.parts)
            if not disk_path.is_file() or disk_path.stat().st_size == 0:
                errors.append(f"{label}: missing generated file {relative}")

    hero = manifest.get("hero")
    if not isinstance(hero, dict):
        errors.append("design/assets-manifest.json: hero object is required")
        hero = {}
    if hero.get("layout") not in HERO_LAYOUTS:
        errors.append("design/assets-manifest.json: invalid hero.layout")
    if hero.get("copy_rendering") != "html":
        errors.append("design/assets-manifest.json: hero.copy_rendering must be html")
    hero_desktop_id = str(hero.get("desktop_asset_id", ""))
    if hero_desktop_id not in assets_by_id:
        errors.append("design/assets-manifest.json: hero.desktop_asset_id does not reference an asset")

    mobile = hero.get("mobile")
    if not isinstance(mobile, dict):
        errors.append("design/assets-manifest.json: hero.mobile object is required")
        mobile = {}
    mobile_strategy = mobile.get("strategy")
    if mobile_strategy not in MOBILE_STRATEGIES:
        errors.append("design/assets-manifest.json: invalid hero.mobile.strategy")
    if not str(mobile.get("reason", "")).strip():
        errors.append("design/assets-manifest.json: hero.mobile.reason is required")
    if mobile_strategy == "dedicated-asset":
        mobile_asset_id = str(mobile.get("asset_id", ""))
        if mobile_asset_id not in assets_by_id:
            errors.append("design/assets-manifest.json: dedicated mobile Hero asset is missing")

    final_cta = manifest.get("final_cta")
    if not isinstance(final_cta, dict):
        errors.append("design/assets-manifest.json: final_cta object is required")
        final_cta = {}
    if final_cta.get("copy_rendering") != "html":
        errors.append("design/assets-manifest.json: final_cta.copy_rendering must be html")
    final_cta_id = str(final_cta.get("background_asset_id", ""))
    if final_cta_id not in assets_by_id:
        errors.append("design/assets-manifest.json: final_cta.background_asset_id does not reference an asset")
    if final_cta_id and final_cta_id == hero_desktop_id:
        errors.append("design/assets-manifest.json: Hero and final CTA must use separate assets")

    plan_value = manifest.get("section_asset_plan")
    plan = plan_value if isinstance(plan_value, list) else []
    plans_by_section = {
        item.get("section"): item
        for item in plan
        if isinstance(item, dict) and item.get("section") in SECTION_IDS
    }
    if set(plans_by_section) != set(SECTION_IDS):
        errors.append("design/assets-manifest.json: section_asset_plan must cover all six sections")
    for section_id in SECTION_IDS:
        item = plans_by_section.get(section_id)
        if not item:
            continue
        decision = item.get("decision")
        if decision not in ASSET_DECISIONS:
            errors.append(f"design/assets-manifest.json: invalid decision for {section_id}")
        if not str(item.get("reason", "")).strip():
            errors.append(f"design/assets-manifest.json: asset reason is required for {section_id}")
        if decision != "not-needed":
            asset_ids = item.get("asset_ids")
            if not isinstance(asset_ids, list) or not asset_ids:
                errors.append(f"design/assets-manifest.json: asset_ids required for {section_id}")
            else:
                for asset_id in asset_ids:
                    if str(asset_id) not in assets_by_id:
                        errors.append(f"design/assets-manifest.json: unknown asset {asset_id} for {section_id}")

    mapping_value = manifest.get("asset_mapping")
    mappings = mapping_value if isinstance(mapping_value, list) else []
    mappings_by_id = {
        str(item.get("asset_id")): item
        for item in mappings
        if isinstance(item, dict) and item.get("asset_id")
    }
    required_asset_ids = {hero_desktop_id, final_cta_id}
    if mobile_strategy == "dedicated-asset":
        required_asset_ids.add(str(mobile.get("asset_id", "")))

    public_source = _combined_text([root / "index.html", root / "styles.css"])
    prototype_source = _combined_text(
        [root / "design" / "prototype" / "index.html", root / "design" / "prototype" / "styles.css"]
    )
    for asset_id in required_asset_ids:
        if not asset_id:
            continue
        mapping = mappings_by_id.get(asset_id)
        if not mapping:
            errors.append(f"design/assets-manifest.json: mapping missing for {asset_id}")
            continue
        public_path = str(mapping.get("public_src", "")).strip()
        prototype_path = str(mapping.get("prototype_src", "")).strip()
        if not public_path or public_path not in public_source:
            errors.append(f"public implementation does not reference mapped asset {asset_id}")
        if not prototype_path or prototype_path not in prototype_source:
            errors.append(f"design prototype does not reference mapped asset {asset_id}")

