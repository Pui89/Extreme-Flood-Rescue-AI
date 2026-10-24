"""Regression tests for terrain-aware flood hazard decisions."""
import unittest

from pui89_autonomy.flood_hazard import (
    FloodHazardInputs,
    HazardState,
    assess_flood_hazard,
)


def safe_ground(**overrides):
    values = dict(
        platform="ground",
        water_depth_m=0.5,
        current_speed_mps=0.2,
        slope_deg=5.0,
        bank_stable=True,
        debris_clear=True,
        structure_clear=True,
        localization_ok=True,
        communication_ok=True,
        sensor_age_s=0.5,
        max_sensor_age_s=2.0,
        platform_depth_limit_m=1.0,
        platform_current_limit_mps=0.5,
        platform_slope_limit_deg=15.0,
        emergency_stop_active=False,
        safety_monitor_ok=True,
        battery_ok=True,
        propulsion_ok=True,
    )
    values.update(overrides)
    return FloodHazardInputs(**values)


class FloodHazardTests(unittest.TestCase):
    def test_healthy_inputs_only_allow_simulation_candidate(self):
        decision = assess_flood_hazard(safe_ground(), decision_time="2026-10-25T00:00:00Z")
        self.assertEqual(decision.state, HazardState.PROCEED_SIMULATION)
        self.assertFalse(decision.audit_record["physical_safety_validated"])
        self.assertEqual(decision.audit_record["evidence_type"], "SUPPLIED_INPUT_SOFTWARE_GATE")

    def test_ground_depth_is_checked_against_explicit_configured_limit(self):
        for depth in (1.01, 5.5, 15.0):
            with self.subTest(depth=depth):
                decision = assess_flood_hazard(safe_ground(water_depth_m=depth))
                self.assertEqual(decision.state, HazardState.SAFE_HOLD)
                self.assertTrue(any("configured platform limit" in reason for reason in decision.reasons))

    def test_ground_requires_an_explicit_platform_depth_limit(self):
        decision = assess_flood_hazard(safe_ground(platform_depth_limit_m=None))
        self.assertEqual(decision.state, HazardState.SAFE_HOLD)
        self.assertTrue(any("depth limit is not configured" in reason for reason in decision.reasons))

    def test_configured_ground_limit_can_be_above_5_5_for_simulation_only(self):
        decision = assess_flood_hazard(safe_ground(water_depth_m=15.0, platform_depth_limit_m=15.0))
        self.assertEqual(decision.state, HazardState.PROCEED_SIMULATION)
        self.assertFalse(decision.audit_record["physical_safety_validated"])

    def test_missing_depth_or_current_fails_safe(self):
        for field in ("water_depth_m", "current_speed_mps"):
            with self.subTest(field=field):
                decision = assess_flood_hazard(safe_ground(**{field: None}))
                self.assertEqual(decision.state, HazardState.SAFE_HOLD)

    def test_stale_or_invalid_sensor_age_fails_safe(self):
        for age in (2.01, None, -1.0, float("nan"), float("inf")):
            with self.subTest(age=age):
                decision = assess_flood_hazard(safe_ground(sensor_age_s=age))
                self.assertEqual(decision.state, HazardState.SAFE_HOLD)

    def test_missing_status_fails_safe(self):
        for field in ("bank_stable", "debris_clear", "structure_clear", "localization_ok", "communication_ok", "emergency_stop_active", "safety_monitor_ok", "battery_ok", "propulsion_ok"):
            with self.subTest(field=field):
                self.assertEqual(
                    assess_flood_hazard(safe_ground(**{field: None})).state,
                    HazardState.SAFE_HOLD,
                )

    def test_emergency_stop_or_robot_health_fault_fails_safe(self):
        for overrides in (
            {"emergency_stop_active": True},
            {"safety_monitor_ok": False},
            {"battery_ok": False},
            {"propulsion_ok": False},
        ):
            with self.subTest(overrides=overrides):
                decision = assess_flood_hazard(safe_ground(**overrides))
                self.assertEqual(decision.state, HazardState.SAFE_HOLD)

    def test_non_boolean_safety_status_is_rejected(self):
        for field in ("emergency_stop_active", "safety_monitor_ok", "battery_ok", "propulsion_ok"):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    assess_flood_hazard(safe_ground(**{field: "yes"}))

    def test_lost_localization_or_communications_fails_safe(self):
        for field in ("localization_ok", "communication_ok"):
            with self.subTest(field=field):
                self.assertEqual(
                    assess_flood_hazard(safe_ground(**{field: False})).state,
                    HazardState.SAFE_HOLD,
                )

    def test_fast_current_over_limit_fails_safe(self):
        decision = assess_flood_hazard(safe_ground(current_speed_mps=0.8))
        self.assertEqual(decision.state, HazardState.SAFE_HOLD)
        self.assertTrue(any("current speed exceeds" in reason for reason in decision.reasons))

    def test_unstable_bank_or_debris_requests_replan(self):
        for overrides in ({"bank_stable": False}, {"debris_clear": False}, {"structure_clear": False}):
            with self.subTest(overrides=overrides):
                self.assertEqual(
                    assess_flood_hazard(safe_ground(**overrides)).state,
                    HazardState.REPLAN_HANDOFF,
                )

    def test_slope_over_limit_requests_replan(self):
        decision = assess_flood_hazard(safe_ground(slope_deg=20))
        self.assertEqual(decision.state, HazardState.REPLAN_HANDOFF)

    def test_sensor_conflict_requests_human_review(self):
        self.assertEqual(
            assess_flood_hazard(safe_ground(sensor_conflict=True)).state,
            HazardState.HUMAN_REVIEW,
        )

    def test_missing_terrain_slope_fails_safe(self):
        self.assertEqual(
            assess_flood_hazard(safe_ground(slope_deg=None)).state,
            HazardState.SAFE_HOLD,
        )

    def test_invalid_platform_rejected(self):
        with self.assertRaises(ValueError):
            assess_flood_hazard(safe_ground(platform="submarine"))

    def test_invalid_configured_limit_rejected(self):
        with self.assertRaises(ValueError):
            assess_flood_hazard(safe_ground(platform_depth_limit_m=float("nan")))

    def test_boat_requires_depth_and_current_but_not_ground_depth_boundary(self):
        values = dict(safe_ground().__dict__)
        values.update(platform="boat", water_depth_m=8.0, current_speed_mps=0.5, platform_depth_limit_m=10.0)
        decision = assess_flood_hazard(FloodHazardInputs(**values))
        self.assertEqual(decision.state, HazardState.PROCEED_SIMULATION)

    def test_drone_still_requires_fresh_status_and_terrain_data(self):
        values = dict(safe_ground().__dict__)
        values.update(platform="drone", water_depth_m=None, current_speed_mps=None)
        decision = assess_flood_hazard(FloodHazardInputs(**values))
        self.assertEqual(decision.state, HazardState.PROCEED_SIMULATION)

    def test_audit_record_contains_inputs_reasons_and_time(self):
        decision = assess_flood_hazard(safe_ground(water_depth_m=6), decision_time="2026-10-25T00:00:00Z")
        record = decision.audit_record
        self.assertEqual(record["decision_time"], "2026-10-25T00:00:00Z")
        self.assertEqual(record["state"], "safe_hold")
        self.assertTrue(record["reasons"])
        self.assertEqual(record["inputs"]["water_depth_m"], 6)


if __name__ == "__main__":
    unittest.main()
