"""Dependency-free semantic-segmentation and track-continuity metrics.

Inputs must already be aligned/reviewed. This module does not run models,
decode images, associate detections, or establish physical rescue safety.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence


def _class_ids(values: Sequence[int]) -> tuple[int, ...]:
    if not values:
        raise ValueError("class_ids must not be empty")
    result = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("class_ids must be unique non-negative integers")
        result.append(value)
    if len(set(result)) != len(result):
        raise ValueError("class_ids must be unique")
    return tuple(result)


def semantic_segmentation_metrics(
    ground_truth: Iterable[int],
    prediction: Iterable[int],
    *,
    class_ids: Sequence[int],
    ignore_index: int | None = None,
) -> dict[str, Any]:
    """Compute confusion matrix, per-class IoU/Dice/precision/recall.

    Ground-truth pixels equal to ignore_index are excluded. Predictions at
    retained pixels must belong to class_ids. A class with no union is None,
    not a fabricated zero. The function accepts flat, already-aligned labels.
    """
    classes = _class_ids(class_ids)
    gt, pred = list(ground_truth), list(prediction)
    if not gt or len(gt) != len(pred):
        raise ValueError("ground_truth and prediction must be non-empty and equal length")
    if ignore_index is not None and (isinstance(ignore_index, bool) or not isinstance(ignore_index, int)):
        raise ValueError("ignore_index must be an integer or None")
    index = {class_id: i for i, class_id in enumerate(classes)}
    matrix = [[0 for _ in classes] for _ in classes]
    ignored = 0
    for actual, estimated in zip(gt, pred):
        if isinstance(actual, bool) or not isinstance(actual, int):
            raise ValueError("ground-truth labels must be integers")
        if isinstance(estimated, bool) or not isinstance(estimated, int):
            raise ValueError("predicted labels must be integers")
        if ignore_index is not None and actual == ignore_index:
            ignored += 1
            continue
        if actual not in index:
            raise ValueError(f"unknown ground-truth class id: {actual}")
        if estimated not in index:
            raise ValueError(f"unknown predicted class id: {estimated}")
        matrix[index[actual]][index[estimated]] += 1

    per_class: dict[str, Any] = {}
    total = sum(sum(row) for row in matrix)
    correct = sum(matrix[i][i] for i in range(len(classes)))
    ious, dices = [], []
    for i, class_id in enumerate(classes):
        tp = matrix[i][i]
        support = sum(matrix[i])
        predicted_count = sum(row[i] for row in matrix)
        fp, fn = predicted_count - tp, support - tp
        union = tp + fp + fn
        iou = tp / union if union else None
        dice_denominator = 2 * tp + fp + fn
        dice = (2 * tp / dice_denominator) if dice_denominator else None
        precision = tp / predicted_count if predicted_count else None
        recall = tp / support if support else None
        per_class[str(class_id)] = {
            "support_pixels": support,
            "predicted_pixels": predicted_count,
            "tp": tp, "fp": fp, "fn": fn,
            "iou": iou, "dice": dice,
            "precision": precision, "recall": recall,
        }
        if iou is not None:
            ious.append(iou)
        if dice is not None:
            dices.append(dice)
    return {
        "metric_schema": "pui89.semantic-segmentation.v1",
        "pixel_count": total,
        "ignored_pixel_count": ignored,
        "pixel_accuracy": correct / total if total else None,
        "mean_iou": sum(ious) / len(ious) if ious else None,
        "mean_dice": sum(dices) / len(dices) if dices else None,
        "class_ids": list(classes),
        "confusion_matrix_rows_ground_truth_columns_prediction": matrix,
        "per_class": per_class,
        "limitations": [
            "Labels must be aligned, independently reviewed and drawn from a documented split.",
            "Metrics summarize supplied labels; no image, model or mask is loaded or evaluated.",
            "Pixel metrics do not establish person-detection, water-depth, navigation or rescue capability.",
        ],
    }


def tracking_identity_continuity(
    frames: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Count identity switches and track fragmentations from supplied matches.

    Each frame contains:
      {"ground_truth_ids": [...], "matches": {ground_truth_id: predicted_id}}
    Matches must already be produced by a separately documented spatial matcher.
    A fragmentation is a matched reappearance after at least one frame in which
    that ground-truth identity was present but unmatched. This is not IDF1/HOTA/MOTA.
    """
    if not frames:
        raise ValueError("frames must not be empty")
    state: dict[str, dict[str, Any]] = {}
    total_gt = total_matched = 0
    for frame_index, frame in enumerate(frames):
        if not isinstance(frame, Mapping):
            raise ValueError("each frame must be a mapping")
        gt_ids = frame.get("ground_truth_ids")
        matches = frame.get("matches")
        if not isinstance(gt_ids, (list, tuple)) or not isinstance(matches, Mapping):
            raise ValueError("each frame requires ground_truth_ids and matches")
        if len(set(gt_ids)) != len(gt_ids):
            raise ValueError("ground_truth_ids must be unique within a frame")
        if any(not isinstance(x, str) or not x.strip() for x in gt_ids):
            raise ValueError("ground_truth_ids must contain non-empty strings")
        if not set(matches).issubset(set(gt_ids)):
            raise ValueError("matches may only reference ground-truth IDs present in the frame")
        pred_ids = list(matches.values())
        if any(not isinstance(x, str) or not x.strip() for x in pred_ids):
            raise ValueError("predicted IDs must be non-empty strings")
        if len(set(pred_ids)) != len(pred_ids):
            raise ValueError("predicted IDs must be unique within a frame")
        total_gt += len(gt_ids)
        total_matched += len(matches)
        for gt_id in gt_ids:
            item = state.setdefault(gt_id, {
                "present_frames": 0, "matched_frames": 0, "missed_frames": 0,
                "identity_switches": 0, "fragmentations": 0,
                "last_predicted_id": None, "was_missed": False,
            })
            item["present_frames"] += 1
            if gt_id not in matches:
                item["missed_frames"] += 1
                if item["matched_frames"]:
                    item["was_missed"] = True
                continue
            pred_id = matches[gt_id]
            if item["last_predicted_id"] is not None and pred_id != item["last_predicted_id"]:
                item["identity_switches"] += 1
            if item["was_missed"]:
                item["fragmentations"] += 1
            item["matched_frames"] += 1
            item["last_predicted_id"] = pred_id
            item["was_missed"] = False

    tracks = []
    for gt_id in sorted(state):
        item = dict(state[gt_id])
        item.pop("last_predicted_id")
        item.pop("was_missed")
        tracks.append({"ground_truth_id": gt_id, **item})
    switches = sum(x["identity_switches"] for x in tracks)
    fragments = sum(x["fragmentations"] for x in tracks)
    return {
        "metric_schema": "pui89.track-continuity.v1",
        "ground_truth_observations": total_gt,
        "matched_observations": total_matched,
        "unmatched_ground_truth_observations": total_gt - total_matched,
        "identity_switches": switches,
        "fragmentations": fragments,
        "tracks": tracks,
        "limitations": [
            "Input matches must be independently generated and documented; this module does not associate objects.",
            "Identity switches and fragmentations are continuity diagnostics, not IDF1, HOTA or MOTA.",
            "No model inference, video decoding or physical action is performed.",
        ],
    }
