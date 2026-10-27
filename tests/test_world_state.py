import unittest
from pui89_autonomy.world_state import WorldStateTracker

class WorldStateTests(unittest.TestCase):
    def test_latest_snapshot_and_hazards(self):
        t=WorldStateTracker(0.6)
        t.update({"object_id":"c1","label":"mature","timestamp":1,"confidence":0.9,"source":"cam"})
        t.update({"object_id":"h1","label":"water","timestamp":2,"confidence":0.8,"source":"sim","hazard":True})
        self.assertEqual(t.snapshot(3)["usable_track_count"],2)
        self.assertEqual(t.snapshot(3)["hazard_ids"],["h1"])
        self.assertEqual(t.snapshot(3),t.snapshot(3))
    def test_old_observation_rejected(self):
        t=WorldStateTracker()
        t.update({"object_id":"x","label":"A","timestamp":2,"confidence":0.9,"source":"s"})
        self.assertFalse(t.update({"object_id":"x","label":"B","timestamp":1,"confidence":0.9,"source":"s"})["accepted"])
        self.assertEqual(t.snapshot(2)["tracks"][0]["label"],"A")
    def test_conflict_becomes_unknown(self):
        t=WorldStateTracker()
        t.update({"object_id":"x","label":"A","timestamp":2,"confidence":0.9,"source":"s1"})
        t.update({"object_id":"x","label":"B","timestamp":2,"confidence":0.8,"source":"s2"})
        s=t.snapshot(2)
        self.assertEqual(s["conflict_ids"],["x"])
        self.assertEqual(s["unknown_ids"],["x"])
        self.assertIsNone(s["tracks"][0]["label"])
    def test_stale_low_confidence_and_bad_input(self):
        t=WorldStateTracker(0.8)
        t.update({"object_id":"x","label":"maybe","timestamp":1,"confidence":0.5,"source":"s"})
        self.assertEqual(t.snapshot(10,2)["stale_ids"],["x"])
        with self.assertRaises(ValueError):
            t.snapshot(0,-1)
        with self.assertRaises(ValueError):
            t.update({"object_id":"x","label":"A","timestamp":float("nan"),"confidence":0.9,"source":"s"})

if __name__ == "__main__": unittest.main()

    def test_confidence_must_be_finite_and_not_boolean(self):
        tracker = WorldStateTracker()
        for confidence in (True, -0.01, 1.01, float("nan"), float("inf")):
            with self.subTest(confidence=confidence):
                with self.assertRaises(ValueError):
                    tracker.update({"object_id":"x","label":"A","timestamp":1,"confidence":confidence,"source":"s"})

    def test_timestamp_must_be_finite_nonnegative_and_not_boolean(self):
        tracker = WorldStateTracker()
        for timestamp in (True, -1, float("nan"), float("inf")):
            with self.subTest(timestamp=timestamp):
                with self.assertRaises(ValueError):
                    tracker.update({"object_id":"x","label":"A","timestamp":timestamp,"confidence":0.9,"source":"s"})

    def test_missing_identity_fields_and_non_boolean_hazard_are_rejected(self):
        tracker = WorldStateTracker()
        for observation in (
            {"label":"A","timestamp":1,"confidence":0.9,"source":"s"},
            {"object_id":"x","label":" ","timestamp":1,"confidence":0.9,"source":"s"},
            {"object_id":"x","label":"A","timestamp":1,"confidence":0.9,"source":"s","hazard":"yes"},
        ):
            with self.subTest(observation=observation):
                with self.assertRaises(ValueError):
                    tracker.update(observation)

    def test_stale_boundary_is_inclusive_and_track_order_is_stable(self):
        tracker = WorldStateTracker()
        tracker.update({"object_id":"z","label":"Z","timestamp":1,"confidence":0.9,"source":"s"})
        tracker.update({"object_id":"a","label":"A","timestamp":1,"confidence":0.9,"source":"s"})
        snapshot = tracker.snapshot(6, stale_after=5)
        self.assertEqual([track["object_id"] for track in snapshot["tracks"]], ["a", "z"])
        self.assertEqual(snapshot["stale_ids"], [])
        self.assertEqual(snapshot["usable_track_count"], 2)
