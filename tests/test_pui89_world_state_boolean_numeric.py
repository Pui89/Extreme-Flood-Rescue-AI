"""Regression tests: bool is not accepted as a numeric measurement."""
import unittest

from tools.pui89_world_state import Observation, assess_observation


class BooleanNumericValidationTests(unittest.TestCase):
    def test_boolean_now_is_rejected(self):
        with self.assertRaises(ValueError):
            assess_observation(Observation("target", "sensor", 1.0, 0.9), now=True)

    def test_boolean_max_age_is_rejected(self):
        with self.assertRaises(ValueError):
            assess_observation(Observation("target", "sensor", 1.0, 0.9), now=2.0, max_age_seconds=True)

    def test_boolean_min_confidence_is_rejected(self):
        with self.assertRaises(ValueError):
            assess_observation(Observation("target", "sensor", 1.0, 0.9), now=2.0, min_confidence=False)

    def test_boolean_timestamp_is_rejected(self):
        result = assess_observation(Observation("target", "sensor", True, 0.9), now=2.0)
        self.assertEqual(result.status, "REJECT")
        self.assertIn("invalid_timestamp", result.reasons)

    def test_boolean_confidence_is_rejected(self):
        result = assess_observation(Observation("target", "sensor", 1.0, True), now=2.0)
        self.assertEqual(result.status, "REJECT")
        self.assertIn("invalid_confidence_range", result.reasons)


if __name__ == "__main__":
    unittest.main()
