"""Condition-stratified evaluation of externally matched flood-scene detections.

Input counts must come from a documented matching procedure against human-verified
ground truth. This module does not run a detector, match boxes, or validate labels.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ALLOWED_CONDITIONS = {
    "daylight",
    "dusk",
    "night",
    "rain",
    "glare",
    "occlusion",
    "debris",
    "low_visibility",
    "camera_motion",
    "missing_modality",
    "stale_sensor",
    "communication_loss",
    "geographic_shift",
    "unknown_environment",
}


class EvaluationInputError(ValueError):
    """Raised when the supplied evaluation record is malformed."""


def _non_empty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationInputError(f"{field} must be a non-empty string")
    return value.strip()


def _count(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise EvaluationInputError(f"{field} must be a non-negative integer")
    return value


def _metrics(tp: int, fp: int, fn: int) -> dict[str, int | float | None]:
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision is not None and recall is not None and precision + recall
        else None
    )
    false_negative_rate = fn / (tp + fn) if tp + fn else None
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_negative_rate": false_negative_rate,
    }


def evaluate_condition_strata(payload: dict[str, Any]) -> dict[str, Any]:
    """Summarise overall and per-condition detection counts without model inference."""
    if not isinstance(payload, dict):
        raise EvaluationInputError("top-level JSON value must be an object")

    schema_version = _non_empty_string(payload.get("schema_version"), "schema_version")
    if schema_version != "1.0":
        raise EvaluationInputError("schema_version must be '1.0'")

    dataset_id = _non_empty_string(payload.get("dataset_id"), "dataset_id")
    model_id = _non_empty_string(payload.get("model_id"), "model_id")
    model_revision = _non_empty_string(payload.get("model_revision"), "model_revision")
    split = _non_empty_string(payload.get("split"), "split").lower()
    if split not in {"train", "validation", "test"}:
        raise EvaluationInputError("split must be train, validation, or test")
    frozen = payload.get("test_split_frozen")
    if not isinstance(frozen, bool):
        raise EvaluationInputError("test_split_frozen must be a boolean")

    records = payload.get("records")
    if not isinstance(records, list) or not records:
        raise EvaluationInputError("records must be a non-empty list")

    seen_ids: set[str] = set()
    overall = [0, 0, 0]
    strata: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"sample_ids": set(), "counts": [0, 0, 0]}
    )

    for index, record in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(record, dict):
            raise EvaluationInputError(f"{prefix} must be an object")
        sample_id = _non_empty_string(record.get("sample_id"), f"{prefix}.sample_id")
        if sample_id in seen_ids:
            raise EvaluationInputError(f"duplicate sample_id: {sample_id}")
        seen_ids.add(sample_id)

        tags = record.get("condition_tags")
        if not isinstance(tags, list) or not tags:
            raise EvaluationInputError(f"{prefix}.condition_tags must be a non-empty list")
        clean_tags: list[str] = []
        for tag in tags:
            tag = _non_empty_string(tag, f"{prefix}.condition_tags item")
            if tag not in ALLOWED_CONDITIONS:
                raise EvaluationInputError(f"unsupported condition tag: {tag}")
            if tag in clean_tags:
                raise EvaluationInputError(f"duplicate condition tag {tag!r} in {sample_id}")
            clean_tags.append(tag)

        counts = [
            _count(record.get("tp"), f"{prefix}.tp"),
            _count(record.get("fp"), f"{prefix}.fp"),
            _count(record.get("fn"), f"{prefix}.fn"),
        ]
        for i, value in enumerate(counts):
            overall[i] += value
        for tag in clean_tags:
            strata[tag]["sample_ids"].add(sample_id)
            for i, value in enumerate(counts):
                strata[tag]["counts"][i] += value

    is_held_out = split == "test" and frozen
    warnings: list[str] = []
    if not is_held_out:
        warnings.append(
            "Results are diagnostic only: a frozen held-out test split was not declared."
        )
    if overall[0] + overall[2] == 0:
        warnings.append("No positive ground-truth instances were represented; recall is undefined.")
    if overall[0] + overall[1] == 0:
        warnings.append("No predicted instances were represented; precision is undefined.")

    condition_results: dict[str, Any] = {}
    for tag in sorted(strata):
        counts = strata[tag]["counts"]
        condition_results[tag] = {
            "sample_count": len(strata[tag]["sample_ids"]),
            **_metrics(*counts),
        }

    return {
        "schema_version": "1.0",
        "evaluation_type": "condition_stratified_detection_counts",
        "dataset_id": dataset_id,
        "model_id": model_id,
        "model_revision": model_revision,
        "split": split,
        "test_split_frozen": frozen,
        "evidence_scope": "held_out_test" if is_held_out else "diagnostic_only",
        "sample_count": len(records),
        "overall": _metrics(*overall),
        "conditions": condition_results,
        "warnings": warnings,
        "limitations": [
            "Counts must be produced by a separately documented detector-to-ground-truth matching procedure.",
            "This tool does not inspect images, run models, validate labels, or verify dataset rights.",
            "Condition strata overlap when a sample has multiple tags; condition totals must not be summed as a dataset total.",
            "No confidence calibration, localization quality, temporal tracking, navigation, or rescue performance is measured.",
            "A held-out software metric does not validate flood physics or physical robot capability.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON file containing matched TP/FP/FN counts")
    parser.add_argument("--output", default="-", help="JSON output path, or '-' for stdout")
    args = parser.parse_args(argv)

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        report = evaluate_condition_strata(payload)
    except (OSError, json.JSONDecodeError, EvaluationInputError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output == "-":
        sys.stdout.write(rendered)
    else:
        output_path = Path(args.output)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Report written: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
