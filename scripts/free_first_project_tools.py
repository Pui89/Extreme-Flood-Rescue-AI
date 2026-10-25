"""Free-first, offline, standard-library project validation tools.

No network, model download, paid API, telemetry, or hardware control.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json_report(path: str | Path, payload: Mapping[str, Any]) -> None:
    """Write deterministic, human-readable JSON locally; never uploads the report."""
    Path(path).write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def finite_unit_interval(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and math.isfinite(value)
        and 0.0 <= value <= 1.0
    )


def required_nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def simulate_search_scenario(width: int, height: int, agents: list[dict[str, Any]],
                           obstacles: set[tuple[int, int]], communication_available: bool = True) -> dict[str, Any]:
    """Tiny deterministic grid scenario for software tests, not hydrodynamics or rescue validation.

    Each agent checks its current grid cell. With communications unavailable,
    agents stay in safe-hold and no new coordinated movement is proposed.
    """
    if (isinstance(width, bool) or isinstance(height, bool) or not isinstance(width, int) or not isinstance(height, int) or width < 1 or height < 1):
        raise ValueError("grid dimensions must be positive integers")
    if not communication_available:
        return {"status": "safe_hold", "visited": [], "coverage": 0.0,
                "reason": "communications unavailable; no movement proposed"}
    visited = set()
    accepted_agents = 0
    for agent in agents:
        cell = agent.get("cell")
        if not isinstance(cell, (tuple, list)) or len(cell) != 2:
            continue
        x, y = cell
        if (isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, int)
                or not isinstance(y, int) or not (0 <= x < width and 0 <= y < height)):
            continue
        if (x, y) in obstacles:
            continue
        visited.add((x, y))
        accepted_agents += 1
    total_free = width * height - sum(1 for x, y in obstacles if 0 <= x < width and 0 <= y < height)
    coverage = len(visited) / total_free if total_free > 0 else 0.0
    return {"status": "simulated_observation", "visited": [list(p) for p in sorted(visited)],
            "coverage": coverage, "accepted_agents": accepted_agents,
            "note": "Toy grid coverage only; not a flood, vehicle, navigation, or safety model."}


def binary_classification_metrics(y_true: Iterable[int | bool], y_pred: Iterable[int | bool]) -> dict[str, float | int]:
    """Compute reproducible binary metrics without third-party dependencies.

    Inputs must be equal-length, non-empty sequences containing only 0/1 or bool.
    This reports metrics; it does not certify a model or set a deployment threshold.
    """
    truth, predicted = list(y_true), list(y_pred)
    if not truth or len(truth) != len(predicted):
        raise ValueError("y_true and y_pred must be non-empty and have equal lengths")
    if any(not isinstance(v, bool) and (not isinstance(v, int) or v not in (0, 1)) for v in truth + predicted):
        raise ValueError("labels must contain only integer 0/1 values or booleans")
    truth = [int(v) for v in truth]
    predicted = [int(v) for v in predicted]
    tp = sum(t == 1 and p == 1 for t, p in zip(truth, predicted))
    tn = sum(t == 0 and p == 0 for t, p in zip(truth, predicted))
    fp = sum(t == 0 and p == 1 for t, p in zip(truth, predicted))
    fn = sum(t == 1 and p == 0 for t, p in zip(truth, predicted))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "sample_count": len(truth), "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "accuracy": (tp + tn) / len(truth), "precision": precision,
        "recall": recall, "f1": f1,
    }
