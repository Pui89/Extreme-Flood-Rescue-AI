"""Dependency-free temporal video evidence scaffold.

This module records upstream-provided detections/track IDs and segmentation
evidence. It does not decode video, detect objects, generate masks, associate
objects between frames, or authorize physical actions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import re
from typing import Any, Iterable


_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")
    return value.strip()


def _confidence(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("confidence must be a finite number in [0, 1]")
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError("confidence must be a finite number in [0, 1]")
    return float(value)


def _sha256(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ValueError(f"{field_name} must be a 64-character lowercase SHA-256 hex digest")
    return value


@dataclass(frozen=True)
class VideoFrame:
    frame_index: int
    timestamp_seconds: float
    source_id: str
    source_sha256: str
    width: int
    height: int

    def __post_init__(self) -> None:
        if isinstance(self.frame_index, bool) or not isinstance(self.frame_index, int) or self.frame_index < 0:
            raise ValueError("frame_index must be a non-negative integer")
        if (isinstance(self.timestamp_seconds, bool)
                or not isinstance(self.timestamp_seconds, (int, float))
                or not math.isfinite(self.timestamp_seconds)
                or self.timestamp_seconds < 0):
            raise ValueError("timestamp_seconds must be finite and non-negative")
        object.__setattr__(self, "source_id", _text(self.source_id, "source_id"))
        object.__setattr__(self, "source_sha256", _sha256(self.source_sha256, "source_sha256"))
        for name in ("width", "height"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True)
class PanopticSegment:
    """A mask reference plus semantic and instance identity supplied upstream."""
    semantic_label: str
    semantic_kind: str
    mask_sha256: str
    confidence: float
    instance_id: str | None = None
    generated_pseudo_label: bool = False
    review_status: str = "UNREVIEWED"

    def __post_init__(self) -> None:
        object.__setattr__(self, "semantic_label", _text(self.semantic_label, "semantic_label"))
        kind = _text(self.semantic_kind, "semantic_kind").upper()
        if kind not in {"THING", "STUFF"}:
            raise ValueError("semantic_kind must be THING or STUFF")
        object.__setattr__(self, "semantic_kind", kind)
        object.__setattr__(self, "mask_sha256", _sha256(self.mask_sha256, "mask_sha256"))
        object.__setattr__(self, "confidence", _confidence(self.confidence))
        if kind == "THING":
            object.__setattr__(self, "instance_id", _text(self.instance_id, "instance_id"))
        elif self.instance_id is not None:
            raise ValueError("STUFF segments must not carry an instance_id")
        if not isinstance(self.generated_pseudo_label, bool):
            raise ValueError("generated_pseudo_label must be boolean")
        status = _text(self.review_status, "review_status").upper()
        if status not in {"UNREVIEWED", "APPROVED", "REJECTED"}:
            raise ValueError("review_status must be UNREVIEWED, APPROVED, or REJECTED")
        object.__setattr__(self, "review_status", status)


@dataclass(frozen=True)
class VideoFrameEvidence:
    frame: VideoFrame
    segments: tuple[PanopticSegment, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.frame, VideoFrame):
            raise TypeError("frame must be a VideoFrame")
        segments = tuple(self.segments)
        if any(not isinstance(item, PanopticSegment) for item in segments):
            raise TypeError("segments must contain PanopticSegment records")
        instance_ids = [s.instance_id for s in segments if s.semantic_kind == "THING"]
        if len(instance_ids) != len(set(instance_ids)):
            raise ValueError("duplicate instance_id within one frame")
        object.__setattr__(self, "segments", segments)


@dataclass
class TemporalVideoLedger:
    """Append-only-in-memory frame ledger with conservative track consistency checks.

    Track IDs are supplied by an upstream tracker. This ledger never performs
    visual association and cannot measure identity switches without ground truth.
    """
    _frames: list[VideoFrameEvidence] = field(default_factory=list)
    _tracks: dict[str, dict[str, Any]] = field(default_factory=dict)
    _events: list[dict[str, Any]] = field(default_factory=list)

    def add(self, evidence: VideoFrameEvidence) -> dict[str, Any]:
        if not isinstance(evidence, VideoFrameEvidence):
            raise TypeError("evidence must be a VideoFrameEvidence")
        frame = evidence.frame
        if self._frames:
            previous = self._frames[-1].frame
            if frame.frame_index <= previous.frame_index:
                raise ValueError("frame_index must increase strictly")
            if frame.timestamp_seconds <= previous.timestamp_seconds:
                raise ValueError("timestamps must increase strictly")
        seen: set[str] = set()
        frame_events: list[dict[str, Any]] = []
        for segment in evidence.segments:
            if segment.semantic_kind != "THING":
                continue
            track_id = segment.instance_id
            assert track_id is not None
            if track_id in seen:
                raise ValueError("duplicate track identity within one frame")
            seen.add(track_id)
            previous_track = self._tracks.get(track_id)
            if previous_track is None:
                self._tracks[track_id] = {
                    "track_id": track_id,
                    "first_frame": frame.frame_index,
                    "last_frame": frame.frame_index,
                    "observed_frames": [frame.frame_index],
                    "labels": [segment.semantic_label],
                    "max_inter_frame_gap": 0,
                }
                continue
            gap = frame.frame_index - previous_track["last_frame"]
            previous_track["max_inter_frame_gap"] = max(previous_track["max_inter_frame_gap"], gap - 1)
            previous_track["last_frame"] = frame.frame_index
            previous_track["observed_frames"].append(frame.frame_index)
            if segment.semantic_label not in previous_track["labels"]:
                previous_track["labels"].append(segment.semantic_label)
                event = {
                    "type": "TRACK_LABEL_CONFLICT",
                    "track_id": track_id,
                    "frame_index": frame.frame_index,
                    "previous_labels": list(previous_track["labels"][:-1]),
                    "new_label": segment.semantic_label,
                    "status": "HUMAN_REVIEW_REQUIRED",
                }
                self._events.append(event)
                frame_events.append(event)
        self._frames.append(evidence)
        return {
            "accepted": True,
            "frame_index": frame.frame_index,
            "track_count": len(self._tracks),
            "events": frame_events,
        }

    def report(self) -> dict[str, Any]:
        tracks = []
        for track_id in sorted(self._tracks):
            item = self._tracks[track_id]
            tracks.append({
                **item,
                "labels": list(item["labels"]),
                "observed_frames": list(item["observed_frames"]),
                "label_consistent": len(item["labels"]) == 1,
                "status": "TRACK_REVIEW_REQUIRED" if len(item["labels"]) > 1 else "UNASSESSED",
            })
        return {
            "frame_count": len(self._frames),
            "track_count": len(tracks),
            "tracks": tracks,
            "events": [dict(event) for event in self._events],
            "identity_switches_measured": False,
            "identity_switches_note": "Requires independently reviewed ground-truth identities; not inferred from supplied track IDs.",
            "limitations": [
                "No video decoding, object detection, segmentation, optical flow, depth estimation or visual tracking is performed.",
                "Track IDs and mask hashes are supplied by an upstream component and are not independently verified.",
                "Frame gaps and label changes are review signals, not proof of identity switches.",
                "This report is software evidence only and does not establish flood-scene detection accuracy or rescue safety.",
            ],
            "hardware_actuation": False,
        }


def assess_pseudo_label(segment: PanopticSegment, *, min_confidence: float = 0.80) -> dict[str, Any]:
    """Fail closed: generated labels require explicit human approval."""
    if not isinstance(segment, PanopticSegment):
        raise TypeError("segment must be a PanopticSegment")
    threshold = _confidence(min_confidence)
    if segment.review_status == "REJECTED":
        status, reason = "REJECT", "human_rejected"
    elif segment.review_status != "APPROVED":
        status, reason = "REVIEW", "human_approval_missing"
    elif segment.confidence < threshold:
        status, reason = "REVIEW", "confidence_below_threshold"
    else:
        status, reason = "ACCEPT_FOR_OFFLINE_EVALUATION", "human_approved_and_threshold_met"
    return {
        "status": status,
        "reason": reason,
        "generated_pseudo_label": segment.generated_pseudo_label,
        "requires_human_review": status == "REVIEW",
        "may_enter_offline_evaluation": status == "ACCEPT_FOR_OFFLINE_EVALUATION",
        "may_actuate_hardware": False,
    }


def build_video_evidence_report(
    frames: Iterable[VideoFrameEvidence],
) -> dict[str, Any]:
    """Build a deterministic report from an ordered iterable of frame evidence."""
    ledger = TemporalVideoLedger()
    for frame in frames:
        ledger.add(frame)
    return ledger.report()
