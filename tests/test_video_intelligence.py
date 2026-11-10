import unittest

from pui89_autonomy.video_intelligence import (
    PanopticSegment,
    VideoFrame,
    VideoFrameEvidence,
    TemporalVideoLedger,
    assess_pseudo_label,
    build_video_evidence_report,
)

HASH_A = "a" * 64
HASH_B = "b" * 64


def frame(index, timestamp=None, segments=()):
    return VideoFrameEvidence(
        VideoFrame(
            frame_index=index,
            timestamp_seconds=float(index if timestamp is None else timestamp),
            source_id="synthetic-flood-sequence-01",
            source_sha256=HASH_A,
            width=640,
            height=480,
        ),
        tuple(segments),
    )


def thing(track_id, label="person", confidence=0.9, review="UNREVIEWED", generated=False):
    return PanopticSegment(
        semantic_label=label,
        semantic_kind="THING",
        mask_sha256=HASH_B,
        confidence=confidence,
        instance_id=track_id,
        review_status=review,
        generated_pseudo_label=generated,
    )


def stuff(label="water"):
    return PanopticSegment(
        semantic_label=label,
        semantic_kind="STUFF",
        mask_sha256=HASH_B,
        confidence=0.95,
    )


class VideoIntelligenceTests(unittest.TestCase):
    def test_frame_metadata_rejects_bad_hash_and_time(self):
        with self.assertRaises(ValueError):
            VideoFrame(0, float("nan"), "cam", HASH_A, 640, 480)
        with self.assertRaises(ValueError):
            VideoFrame(0, 0.0, "cam", "bad", 640, 480)

    def test_frame_contract_rejects_duplicate_instance_ids(self):
        with self.assertRaises(ValueError):
            frame(0, segments=(thing("p1"), thing("p1", "animal")))

    def test_ledger_tracks_supplied_identity_across_frames(self):
        ledger = TemporalVideoLedger()
        ledger.add(frame(0, segments=(thing("p1"), stuff())))
        ledger.add(frame(1, segments=(thing("p1"),)))
        report = ledger.report()
        self.assertEqual(report["frame_count"], 2)
        self.assertEqual(report["track_count"], 1)
        self.assertEqual(report["tracks"][0]["observed_frames"], [0, 1])
        self.assertTrue(report["tracks"][0]["label_consistent"])
        self.assertFalse(report["identity_switches_measured"])
        self.assertFalse(report["hardware_actuation"])

    def test_frame_gaps_are_recorded_without_claiming_identity_switch(self):
        ledger = TemporalVideoLedger()
        ledger.add(frame(0, segments=(thing("p1"),)))
        ledger.add(frame(3, segments=(thing("p1"),)))
        report = ledger.report()
        self.assertEqual(report["tracks"][0]["max_inter_frame_gap"], 2)
        self.assertFalse(report["identity_switches_measured"])

    def test_label_change_triggers_human_review(self):
        ledger = TemporalVideoLedger()
        ledger.add(frame(0, segments=(thing("p1", "person"),)))
        result = ledger.add(frame(1, segments=(thing("p1", "animal"),)))
        report = ledger.report()
        self.assertEqual(result["events"][0]["type"], "TRACK_LABEL_CONFLICT")
        self.assertEqual(report["tracks"][0]["status"], "TRACK_REVIEW_REQUIRED")
        self.assertEqual(report["events"][0]["status"], "HUMAN_REVIEW_REQUIRED")

    def test_non_increasing_frame_or_timestamp_rejected(self):
        ledger = TemporalVideoLedger()
        ledger.add(frame(2, timestamp=2))
        with self.assertRaises(ValueError):
            ledger.add(frame(2, timestamp=3))
        with self.assertRaises(ValueError):
            ledger.add(frame(3, timestamp=2))

    def test_generated_pseudo_label_needs_human_approval(self):
        result = assess_pseudo_label(thing("p1", generated=True))
        self.assertEqual(result["status"], "REVIEW")
        self.assertFalse(result["may_enter_offline_evaluation"])
        self.assertFalse(result["may_actuate_hardware"])

    def test_approved_pseudo_label_can_enter_offline_evaluation_only(self):
        result = assess_pseudo_label(thing("p1", confidence=0.9, review="APPROVED", generated=True))
        self.assertEqual(result["status"], "ACCEPT_FOR_OFFLINE_EVALUATION")
        self.assertTrue(result["may_enter_offline_evaluation"])
        self.assertFalse(result["may_actuate_hardware"])

    def test_low_confidence_and_rejected_labels_do_not_pass(self):
        low = assess_pseudo_label(thing("p1", confidence=0.5, review="APPROVED"))
        rejected = assess_pseudo_label(thing("p2", review="REJECTED"))
        self.assertEqual(low["status"], "REVIEW")
        self.assertEqual(rejected["status"], "REJECT")

    def test_report_is_deterministic_for_identical_inputs(self):
        sequence = [frame(0, segments=(thing("p1"),)), frame(1, segments=(thing("p1"),))]
        self.assertEqual(build_video_evidence_report(sequence), build_video_evidence_report(sequence))


if __name__ == "__main__":
    unittest.main()
