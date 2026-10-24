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

    def test_sensor_failure_triggers_safe_stop_without_observations(self):
        result = run_simulation(seed=7, fail_sensor_at=2)
        self.assertEqual(result["status"], "SAFE_STOP_SIMULATED")
        self.assertFalse(result["mission"]["reached_observation_waypoint"])
        self.assertEqual(result["synthetic_observations"], [])
        self.assertEqual(result["events"][-1]["event"], "SAFE_STOP")
        self.assertIn("sensor failure", result["stop_reason"])

    def test_sensor_failure_before_first_move_keeps_rover_at_start(self):
        result = run_simulation(seed=7, fail_sensor_at=1)
        self.assertEqual(result["status"], "SAFE_STOP_SIMULATED")
        self.assertEqual(result["mission"]["visited_path_xy"], [list(START)])
        self.assertEqual(result["synthetic_observations"], [])

    def test_invalid_sensor_failure_step_is_rejected(self):
        for step in (0, -1):
            with self.subTest(step=step):
                with self.assertRaises(ValueError):
                    run_simulation(fail_sensor_at=step)

    def test_unknown_cells_are_reported_not_marked_safe(self):
        result = run_simulation()
        self.assertTrue(result["mission"]["unknown_cells_preserved"])
        self.assertIn("SYNTHETIC_GRID_SIMULATION", result["evidence_type"])


    def test_communication_loss_before_first_move_keeps_rover_at_start(self):
        result = run_simulation(seed=7, fail_comms_at=1)
        self.assertEqual(result["status"], "SAFE_STOP_SIMULATED")
        self.assertEqual(result["mission"]["visited_path_xy"], [list(START)])
        self.assertFalse(result["mission"]["reached_observation_waypoint"])
        self.assertEqual(result["synthetic_observations"], [])
        self.assertEqual(result["events"][-1]["event"], "SAFE_STOP")

    def test_no_route_returns_none_when_goal_is_blocked(self):
        self.assertIsNone(find_path(START, OBSERVATION_POINT, OBSTACLES | WATER | {OBSERVATION_POINT}))

    def test_invalid_path_coordinates_are_rejected(self):
        invalid_cases = [
            ((-1, 0), OBSERVATION_POINT),
            (START, (14, 2)),
            ((1.5, 2), OBSERVATION_POINT),
            (START, (True, 2)),
            ((1,), OBSERVATION_POINT),
        ]
        for start, goal in invalid_cases:
            with self.subTest(start=start, goal=goal):
                with self.assertRaises(ValueError):
                    find_path(start, goal, OBSTACLES | WATER)

    def test_planned_and_visited_paths_never_enter_blocked_cells(self):
        result = run_simulation(seed=89)
        blocked = OBSTACLES | WATER
        for cell in result["mission"]["planned_path_xy"]:
            self.assertNotIn(tuple(cell), blocked)
        for cell in result["mission"]["visited_path_xy"]:
            self.assertNotIn(tuple(cell), blocked)

    def test_communication_failure_does_not_create_person_observations(self):
        result = run_simulation(seed=7, fail_comms_at=2)
        self.assertEqual(result["synthetic_observations"], [])
        self.assertFalse(result["mission"]["reached_observation_waypoint"])


if __name__ == "__main__":
    unittest.main()
