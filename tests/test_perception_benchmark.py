import unittest

from pui89_autonomy.perception_benchmark import (
    semantic_segmentation_metrics,
    tracking_identity_continuity,
)


class SemanticSegmentationMetricsTests(unittest.TestCase):
    def test_confusion_iou_dice_and_ignore_index(self):
        result = semantic_segmentation_metrics(
            [0, 0, 1, 1, 255],
            [0, 1, 1, 0, 1],
            class_ids=[0, 1],
            ignore_index=255,
        )
        self.assertEqual(result["pixel_count"], 4)
        self.assertEqual(result["ignored_pixel_count"], 1)
        self.assertEqual(result["confusion_matrix_rows_ground_truth_columns_prediction"],
                         [[1, 1], [1, 1]])
        self.assertEqual(result["pixel_accuracy"], 0.5)
        self.assertEqual(result["per_class"]["0"]["iou"], 1 / 3)
        self.assertEqual(result["per_class"]["1"]["dice"], 0.5)

    def test_absent_class_is_not_reported_as_zero(self):
        result = semantic_segmentation_metrics([0, 0], [0, 0], class_ids=[0, 1])
        self.assertIsNone(result["per_class"]["1"]["iou"])
        self.assertEqual(result["mean_iou"], 1.0)

    def test_rejects_mismatched_or_unknown_labels(self):
        with self.assertRaises(ValueError):
            semantic_segmentation_metrics([0], [], class_ids=[0])
        with self.assertRaises(ValueError):
            semantic_segmentation_metrics([0], [2], class_ids=[0, 1])
        with self.assertRaises(ValueError):
            semantic_segmentation_metrics([0], [0], class_ids=[0, 0])


class TrackingContinuityTests(unittest.TestCase):
    def test_counts_identity_switch_and_fragmentation(self):
        result = tracking_identity_continuity([
            {"ground_truth_ids": ["person-A"], "matches": {"person-A": "track-1"}},
            {"ground_truth_ids": ["person-A"], "matches": {}},
            {"ground_truth_ids": ["person-A"], "matches": {"person-A": "track-2"}},
        ])
        self.assertEqual(result["identity_switches"], 1)
        self.assertEqual(result["fragmentations"], 1)
        self.assertEqual(result["unmatched_ground_truth_observations"], 1)

    def test_multiple_tracks_and_deterministic_order(self):
        result = tracking_identity_continuity([
            {"ground_truth_ids": ["z", "a"], "matches": {"z": "p-z", "a": "p-a"}},
        ])
        self.assertEqual([x["ground_truth_id"] for x in result["tracks"]], ["a", "z"])
        self.assertEqual(result, tracking_identity_continuity([
            {"ground_truth_ids": ["z", "a"], "matches": {"z": "p-z", "a": "p-a"}},
        ]))

    def test_rejects_invalid_frame_matches(self):
        invalid = [
            [{"ground_truth_ids": ["a"], "matches": {"b": "p"}}],
            [{"ground_truth_ids": ["a"], "matches": {"a": "p", "x": "q"}}],
            [{"ground_truth_ids": ["a", "b"], "matches": {"a": "p", "b": "p"}}],
        ]
        for frames in invalid:
            with self.subTest(frames=frames):
                with self.assertRaises(ValueError):
                    tracking_identity_continuity(frames)


if __name__ == "__main__":
    unittest.main()
