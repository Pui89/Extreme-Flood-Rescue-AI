"""Dependency-free conformance test for the shared PUI89 report schema."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SharedReportSchemaTests(unittest.TestCase):
    def test_schema_is_valid_json_and_covers_all_projects(self):
        schema = json.loads((ROOT / "schemas/pui89-intelligence-report.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["project"]["enum"], [
            "coconut-harvest-ai", "flood-rescue-ai",
            "multimodal-narcotics-screening-ai", "homeguard-ai-nomad",
        ])

    def test_evidence_uncertainty_and_safety_are_required(self):
        schema = json.loads((ROOT / "schemas/pui89-intelligence-report.schema.json").read_text(encoding="utf-8"))
        self.assertTrue({"world_state", "evidence", "uncertainty", "risks", "recommendations", "safety_gate", "verification"} <= set(schema["required"]))
        self.assertIs(schema["properties"]["safety_gate"]["properties"]["physical_actuation_permitted"]["const"], False)

if __name__ == "__main__":
    unittest.main()
