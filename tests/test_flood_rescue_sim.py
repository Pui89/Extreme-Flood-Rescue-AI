import unittest

from scripts.flood_rescue_sim import (
    OBSERVATION_POINT, OBSTACLES, START, WATER, find_path, run_simulation,
)


class FloodRescueSimulationTests(unittest.TestCase):
    def test_path_avoids_blocked_cells(self):
        path = find_path(START, OBSERVATION_POINT, OBSTACLES | WATER)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], START)
        self.assertEqual(path[-1], OBSERVATION_POINT)
        self.assertTrue(all(cell not in OBSTACLES | WATER for cell in path))

    def test_same_seed_is_reproducible_for_core_outputs(self):
        first = run_simulation(seed=42)
        second = run_simulation(seed=42)
        self.assertEqual(first["mission"], second["mission"])
        self.assertEqual(first["synthetic_observations"], second["synthetic_observations"])
        self.assertEqual(first["status"], "COMPLETED_SIMULATION")

    def test_communication_loss_triggers_safe_stop(self):
        result = run_simulation(seed=7, fail_comms_at=2)
        self.assertEqual(result["status"], "SAFE_STOP_SIMULATED")
        self.assertFalse(result["mission"]["reached_observation_waypoint"])
        self.assertEqual(result["events"][-1]["event"], "SAFE_STOP")

    def test_unknown_cells_are_reported_not_marked_safe(self):
        result = run_simulation()
        self.assertTrue(result["mission"]["unknown_cells_preserved"])
        self.assertIn("SYNTHETIC_GRID_SIMULATION", result["evidence_type"])


if __name__ == "__main__":
    unittest.main()
