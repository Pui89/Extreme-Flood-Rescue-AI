"""Documentation smoke tests: these do not validate rescue performance or field safety."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def test_core_project_evidence_files_exist():
    required = [
        "README.md",
        "docs/COMPLETE_SYSTEM_BLUEPRINT.md",
        "docs/VALIDATION_MATRIX.md",
        "docs/images/flood-rescue-amphibious-robot-concept.svg",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    assert not missing, f"Missing project evidence/documentation files: {missing}"


def test_readme_links_to_architecture_validation_and_visual():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for relative_path in (
        "docs/COMPLETE_SYSTEM_BLUEPRINT.md",
        "docs/VALIDATION_MATRIX.md",
        "docs/images/flood-rescue-amphibious-robot-concept.svg",
    ):
        assert relative_path in readme, f"README should link to {relative_path}"


def test_robot_concept_svg_is_well_formed():
    root = ET.parse(ROOT / "docs/images/flood-rescue-amphibious-robot-concept.svg").getroot()
    assert root.tag.endswith("svg"), "Robot concept must have an SVG root element"


def test_readme_keeps_field_validation_boundary_explicit():
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "not yet demonstrated" in readme or "not validated" in readme
    assert "real-world" in readme or "field" in readme
