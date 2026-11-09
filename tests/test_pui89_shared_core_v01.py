import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pui89_flood_model_adapter import adapt_flood_mock
from pui89_shared_core_v01 import build_flood_v01_records

def request():
    return {
        "request_id": "flood-v01-1",
        "timestamp": "2026-11-01T00:00:01Z",
        "evidence": {
            "source_id": "fixture-v01-1",
            "source_ref": "synthetic://flood/v01/1",
            "timestamp": "2026-11-01T00:00:00Z",
            "evidence_kind": "synthetic",
            "lineage": ["unit-test"],
        },
        "mock_observation": {
            "scenario_depth_m": 15,
            "hazard_observations": ["simulated fast current", "debris in route"],
        },
    }

class FloodSharedCoreV01Tests(unittest.TestCase):
    def test_maps_to_simulation_observation_and_advisory_proposal(self):
        bundle = build_flood_v01_records(adapt_flood_mock(request()))
        observation = bundle["observation"]
        proposal = bundle["action_proposal"]
        self.assertEqual(observation["schema_version"], "0.1.0")
        self.assertEqual(observation["source"]["source_type"], "simulation")
        self.assertEqual(observation["quality"]["status"], "unknown")
        self.assertEqual(observation["payload"]["scenario_observations"][0]["scenario_depth_m"], 15.0)
        self.assertEqual(proposal["authority"]["mode"], "advisory_only")
        self.assertIs(proposal["authority"]["human_approval_required"], True)
        self.assertIs(proposal["authority"]["execution_authorized"], False)
        self.assertEqual(proposal["actions"][0]["evidence_refs"], ["fixture-v01-1"])

    def test_mapper_rejects_timezone_missing(self):
        envelope = adapt_flood_mock(request())
        envelope["evidence"]["timestamp"] = "2026-11-01T00:00:00"
        with self.assertRaises(ValueError):
            build_flood_v01_records(envelope)

    def test_shared_core_schema_required_fields_match(self):
        core_dir = os.environ.get("PUI89_SHARED_CORE_DIR")
        if not core_dir:
            self.skipTest("Shared AI Core checkout is supplied by GitHub Actions")
        schema_dir = Path(core_dir) / "schemas" / "v0.1"
        bundle = build_flood_v01_records(adapt_flood_mock(request()))
        for key, filename in (
            ("observation", "observation.schema.json"),
            ("action_proposal", "action-proposal.schema.json"),
        ):
            schema = json.loads((schema_dir / filename).read_text(encoding="utf-8"))
            self.assertEqual(schema["properties"]["schema_version"]["const"], "0.1.0")
            self.assertTrue(set(schema["required"]).issubset(bundle[key].keys()))

if __name__ == "__main__":
    unittest.main()
