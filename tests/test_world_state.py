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
