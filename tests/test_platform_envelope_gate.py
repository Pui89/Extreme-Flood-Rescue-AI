import unittest

from scripts.platform_envelope_gate import evaluate_platform_envelope


BASE_SCENARIO = {
    "depth_m": 1.2,
    "current_mps": 0.3,
    "sensor_data_fresh": True,
    "sensors_valid": True,
    "communications_available": True,
    "safety_monitor_healthy": True,
    "emergency_stop_active": False,
    "recovery_path_available": True,
}
BASE_ENVELOPE = {
    "platform_type": "simulation-ground-platform",
    "max_depth_m": 1.5,
    "max_current_mps": 0.5,
    "limits_reviewed": True,
    "evidence_reference": "test-fixture-only",
}


class PlatformEnvelopeGateTests(unittest.TestCase):
    def test_reviewed_scenario_inside_limits_passes_simulation_gate_only(self):
        result = evaluate_platform_envelope(BASE_SCENARIO, BASE_ENVELOPE)
        self.assertEqual(result["decision"], "SIMULATION_ONLY_GATE_PASS")
        self.assertIn("not a physical safety approval", result["warning"])

    def test_exact_depth_and_current_limits_are_inclusive(self):
        scenario = {**BASE_SCENARIO, "depth_m": 1.5, "current_mps": 0.5}
        result = evaluate_platform_envelope(scenario, BASE_ENVELOPE)
        self.assertEqual(result["decision"], "SIMULATION_ONLY_GATE_PASS")
        self.assertEqual(result["reason_codes"], [])

    def test_just_over_each_limit_fails_closed(self):
        for key, value, reason in (
            ("depth_m", 1.500001, "DEPTH_LIMIT_EXCEEDED"),
            ("current_mps", 0.500001, "CURRENT_LIMIT_EXCEEDED"),
        ):
            with self.subTest(key=key):
                result = evaluate_platform_envelope(
                    {**BASE_SCENARIO, key: value}, BASE_ENVELOPE
                )
                self.assertEqual(result["decision"], "SAFE_HOLD")
                self.assertIn(reason, result["reason_codes"])

    def test_missing_platform_limit_fails_closed(self):
        envelope = {key: value for key, value in BASE_ENVELOPE.items() if key != "max_depth_m"}
        result = evaluate_platform_envelope(BASE_SCENARIO, envelope)
        self.assertEqual(result["decision"], "SAFE_HOLD")
        self.assertIn("MISSING_REQUIRED_INPUT", result["reason_codes"])

    def test_depth_over_limit_enters_safe_hold(self):
        scenario = {**BASE_SCENARIO, "depth_m": 15.0}
        result = evaluate_platform_envelope(scenario, BASE_ENVELOPE)
        self.assertEqual(result["decision"], "SAFE_HOLD")
        self.assertIn("DEPTH_LIMIT_EXCEEDED", result["reason_codes"])

    def test_current_over_limit_enters_safe_hold(self):
        scenario = {**BASE_SCENARIO, "current_mps": 2.0}
        result = evaluate_platform_envelope(scenario, BASE_ENVELOPE)
        self.assertEqual(result["decision"], "SAFE_HOLD")
        self.assertIn("CURRENT_LIMIT_EXCEEDED", result["reason_codes"])

    def test_unreviewed_limits_fail_closed(self):
        envelope = {**BASE_ENVELOPE, "limits_reviewed": False}
        result = evaluate_platform_envelope(BASE_SCENARIO, envelope)
        self.assertEqual(result["decision"], "SAFE_HOLD")
        self.assertIn("LIMITS_NOT_REVIEWED", result["reason_codes"])

    def test_stale_sensor_or_lost_communications_fails_closed(self):
        for key, reason in (
            ("sensor_data_fresh", "SENSOR_DATA_STALE"),
            ("communications_available", "COMMUNICATIONS_UNAVAILABLE"),
        ):
            with self.subTest(key=key):
                scenario = {**BASE_SCENARIO, key: False}
                result = evaluate_platform_envelope(scenario, BASE_ENVELOPE)
                self.assertEqual(result["decision"], "SAFE_HOLD")
                self.assertIn(reason, result["reason_codes"])

    def test_unhealthy_safety_monitor_fails_closed(self):
        scenario = {**BASE_SCENARIO, "safety_monitor_healthy": False}
        result = evaluate_platform_envelope(scenario, BASE_ENVELOPE)
        self.assertEqual(result["decision"], "SAFE_HOLD")
        self.assertIn("SAFETY_MONITOR_UNHEALTHY", result["reason_codes"])

    def test_emergency_stop_and_missing_recovery_path_fail_closed(self):
        for key, value, reason in (
            ("emergency_stop_active", True, "EMERGENCY_STOP_ACTIVE"),
            ("recovery_path_available", False, "RECOVERY_PATH_UNAVAILABLE"),
        ):
            with self.subTest(key=key):
                scenario = {**BASE_SCENARIO, key: value}
                result = evaluate_platform_envelope(scenario, BASE_ENVELOPE)
                self.assertEqual(result["decision"], "SAFE_HOLD")
                self.assertIn(reason, result["reason_codes"])

    def test_nan_boolean_and_negative_values_are_rejected(self):
        for key, value in (("depth_m", float("nan")), ("current_mps", -1), ("sensors_valid", 1)):
            with self.subTest(key=key):
                scenario = {**BASE_SCENARIO, key: value}
                result = evaluate_platform_envelope(scenario, BASE_ENVELOPE)
                self.assertEqual(result["decision"], "SAFE_HOLD")
                self.assertIn("INVALID_REQUIRED_INPUT", result["reason_codes"])


if __name__ == "__main__":
    unittest.main()
