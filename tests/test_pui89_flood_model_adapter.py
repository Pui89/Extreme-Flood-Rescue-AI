import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from pui89_flood_model_adapter import adapt_flood_mock

def request():
    return {"request_id":"flood-1","timestamp":"2026-11-01T00:00:01Z",
      "evidence":{"source_id":"fixture-1","source_ref":"synthetic://flood/1",
        "timestamp":"2026-11-01T00:00:00Z","evidence_kind":"synthetic","lineage":["unit-test"]},
      "mock_observation":{"scenario_depth_m":15,"hazard_observations":["simulated fast current","debris in route"]}}

class FloodModelAdapterTests(unittest.TestCase):
    def test_valid_fixture_is_simulation_review_only(self):
        r=adapt_flood_mock(request())
        self.assertEqual(r["project_id"],"extreme_flood_rescue")
        self.assertEqual(r["status"],"MOCK_OBSERVATION_REVIEW_REQUIRED")
        self.assertEqual(r["observations"][0]["scenario_depth_m"],15.0)
        self.assertEqual(r["proposed_actions"],[])
        self.assertFalse(r["physical_actuation_permitted"])
    def test_depth_above_scenario_range_rejected(self):
        q=request(); q["mock_observation"]["scenario_depth_m"]=15.1
        with self.assertRaises(ValueError): adapt_flood_mock(q)
    def test_negative_depth_rejected(self):
        q=request(); q["mock_observation"]["scenario_depth_m"]=-0.1
        with self.assertRaises(ValueError): adapt_flood_mock(q)
    def test_boolean_depth_rejected(self):
        q=request(); q["mock_observation"]["scenario_depth_m"]=True
        with self.assertRaises(ValueError): adapt_flood_mock(q)
    def test_empty_hazards_rejected(self):
        q=request(); q["mock_observation"]["hazard_observations"]=[]
        with self.assertRaises(ValueError): adapt_flood_mock(q)
    def test_hardware_command_rejected(self):
        q=request(); q["motor_command"]={"move":"forward"}
        with self.assertRaises(ValueError): adapt_flood_mock(q)
if __name__=="__main__": unittest.main()
