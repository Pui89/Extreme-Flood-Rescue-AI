from __future__ import annotations

import unittest

from flood_robot.perception.condition_stratified_metrics import (
    EvaluationInputError,
    evaluate_condition_strata,
)


def sample_payload() -> dict:
    return {
        "schema_version": "1.0",
        "dataset_id": "synthetic-fixture-v1",
        "model_id": "detector-under-test",
        "model_revision": "revision-1",
        "split": "test",
        "test_split_frozen": True,
        "records": [
            {
                "sample_id": "scene-001",
                "condition_tags": ["night", "rain"],
                "tp": 2,
                "fp": 1,
                "fn": 1,
            },
            {
                "sample_id": "scene-002",
                "condition_tags": ["daylight", "occlusion"],
                "tp": 1,
                "fp": 0,
                "fn": 2,
            },
        ],
    }


class ConditionStratifiedMetricsTests(unittest.TestCase):
    def test_reports_overall_and_overlapping_condition_strata(self) -> None:
        report = evaluate_condition_strata(sample_payload())
        self.assertEqual(report["evidence_scope"], "held_out_test")
        self.assertEqual(report["sample_count"], 2)
        self.assertEqual(report["overall"]["tp"], 3)
        self.assertEqual(report["overall"]["fp"], 1)
        self.assertEqual(report["overall"]["fn"], 3)
        self.assertAlmostEqual(report["overall"]["recall"], 0.5)
        self.assertEqual(report["conditions"]["night"]["sample_count"], 1)
        self.assertEqual(report["conditions"]["rain"]["fn"], 1)
        self.assertEqual(report["conditions"]["occlusion"]["false_negative_rate"], 1.0)

    def test_non_test_or_unfrozen_split_is_diagnostic_only(self) -> None:
        payload = sample_payload()
        payload["split"] = "validation"
        report = evaluate_condition_strata(payload)
        self.assertEqual(report["evidence_scope"], "diagnostic_only")
        self.assertTrue(report["warnings"])

    def test_duplicate_sample_ids_are_rejected(self) -> None:
        payload = sample_payload()
        payload["records"][1]["sample_id"] = "scene-001"
        with self.assertRaises(EvaluationInputError):
            evaluate_condition_strata(payload)

    def test_unknown_condition_is_rejected(self) -> None:
        payload = sample_payload()
        payload["records"][0]["condition_tags"] = ["underwater_camera"]
        with self.assertRaises(EvaluationInputError):
            evaluate_condition_strata(payload)

    def test_negative_or_boolean_counts_are_rejected(self) -> None:
        for value in (-1, True, 1.5, "2"):
            payload = sample_payload()
            payload["records"][0]["tp"] = value
            with self.subTest(value=value):
                with self.assertRaises(EvaluationInputError):
                    evaluate_condition_strata(payload)

    def test_zero_support_is_reported_as_undefined_not_zero(self) -> None:
        payload = sample_payload()
        payload["records"] = [{
            "sample_id": "empty-predictions",
            "condition_tags": ["low_visibility"],
            "tp": 0,
            "fp": 0,
            "fn": 0,
        }]
        report = evaluate_condition_strata(payload)
        self.assertIsNone(report["overall"]["precision"])
        self.assertIsNone(report["overall"]["recall"])
        self.assertIsNone(report["overall"]["f1"])
        self.assertTrue(report["warnings"])

    def test_missing_frozen_flag_is_rejected(self) -> None:
        payload = sample_payload()
        del payload["test_split_frozen"]
        with self.assertRaises(EvaluationInputError):
            evaluate_condition_strata(payload)


if __name__ == "__main__":
    unittest.main()
