import unittest
from datetime import datetime, timezone, timedelta

from pui89_aerial.observation import validate_observation


class AerialObservationContractTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 13, 10, 0, tzinfo=timezone.utc)
        self.sample = {
            "schema_version": "1.0", "observation_id": "obs-001",
            "source_id": "drone-camera-a", "modality": "thermal",
            "captured_at": self.now.isoformat(), "image_ref": "local://frame-001",
            "sequence": 1, "location": {"latitude": 14.0, "longitude": 100.0},
        }

    def test_valid_thermal_metadata_is_accepted_not_detected(self):
        result = validate_observation(self.sample, now=self.now)
        self.assertTrue(result["accepted"])
        self.assertIsNone(result["person_detected"])
        self.assertFalse(result["actuation_authorized"])

    def test_rgb_modality_is_supported(self):
        sample = dict(self.sample, modality="rgb")
        self.assertTrue(validate_observation(sample, now=self.now)["accepted"])

    def test_missing_source_is_rejected(self):
        sample = dict(self.sample, source_id=" ")
        self.assertIn("missing_or_blank:source_id", validate_observation(sample, now=self.now)["errors"])

    def test_unknown_modality_is_rejected(self):
        sample = dict(self.sample, modality="lidar")
        self.assertIn("unsupported_modality", validate_observation(sample, now=self.now)["errors"])

    def test_stale_frame_is_rejected(self):
        sample = dict(self.sample, captured_at=(self.now - timedelta(seconds=6)).isoformat())
        self.assertIn("stale_observation", validate_observation(sample, now=self.now)["errors"])

    def test_future_frame_is_rejected(self):
        sample = dict(self.sample, captured_at=(self.now + timedelta(seconds=8)).isoformat())
        self.assertIn("timestamp_in_future", validate_observation(sample, now=self.now)["errors"])

    def test_naive_timestamp_is_rejected(self):
        sample = dict(self.sample, captured_at="2026-11-13T10:00:00")
        self.assertIn("invalid_or_timezone_missing_timestamp", validate_observation(sample, now=self.now)["errors"])

    def test_invalid_coordinates_are_rejected(self):
        sample = dict(self.sample, location={"latitude": 120, "longitude": 100})
        self.assertIn("invalid_location_coordinates", validate_observation(sample, now=self.now)["errors"])

    def test_negative_sequence_is_rejected(self):
        sample = dict(self.sample, sequence=-1)
        self.assertIn("invalid_sequence", validate_observation(sample, now=self.now)["errors"])

    def test_non_object_is_rejected(self):
        self.assertFalse(validate_observation([], now=self.now)["accepted"])


if __name__ == "__main__":
    unittest.main()
