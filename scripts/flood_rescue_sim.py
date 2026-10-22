#!/usr/bin/env python3
"""Deterministic, dependency-free 2D flood reconnaissance simulation.

All map, hazard and possible-person observations are synthetic. This is not a
physics simulator, perception model, or validated rescue robot.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

W, H = 14, 9
START = (0, 0)
OBSERVATION_POINT = (12, 7)
# Synthetic blocked cells: debris/walls and deep/fast water are both no-go.
OBSTACLES = {
    (3, 0), (3, 1), (3, 2), (3, 3), (6, 2), (7, 2), (8, 2),
    (8, 3), (8, 4), (5, 5), (6, 5), (7, 5), (10, 6), (10, 7),
}
WATER = {
    (1, 4), (2, 4), (3, 4), (4, 4), (9, 0), (9, 1), (9, 2),
    (11, 4), (11, 5), (11, 6), (4, 7), (5, 7),
}
POSSIBLE_PEOPLE = [(11, 7), (12, 6)]
UNKNOWN = {(4, 1), (4, 2), (9, 5), (12, 3)}


def neighbors(cell: tuple[int, int]):
    x, y = cell
    for candidate in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        cx, cy = candidate
        if 0 <= cx < W and 0 <= cy < H:
            yield candidate


def find_path(start: tuple[int, int], goal: tuple[int, int],
              blocked: set[tuple[int, int]]) -> list[tuple[int, int]] | None:
    """Breadth-first shortest path through free cells; None means no route."""
    if start in blocked or goal in blocked:
        return None
    queue = deque([start])
    previous = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = previous[current]
            return list(reversed(path))
        for nxt in neighbors(current):
            if nxt not in blocked and nxt not in previous:
                previous[nxt] = current
                queue.append(nxt)
    return None


def render_map(path: list[tuple[int, int]], rover: tuple[int, int]) -> str:
    path_cells = set(path)
    lines = []
    for y in range(H):
        row = []
        for x in range(W):
            p = (x, y)
            if p == rover:
                char = "R"
            elif p == START:
                char = "S"
            elif p == OBSERVATION_POINT:
                char = "G"
            elif p in POSSIBLE_PEOPLE:
                char = "P"
            elif p in WATER:
                char = "~"
            elif p in OBSTACLES:
                char = "#"
            elif p in UNKNOWN:
                char = "?"
            elif p in path_cells:
                char = "*"
            else:
                char = "."
            row.append(char)
        lines.append("".join(row))
    return "\n".join(lines)


def run_simulation(seed: int = 7, fail_comms_at: int | None = None) -> dict:
    """Run a synthetic reconnaissance mission and return auditable results."""
    if fail_comms_at is not None and fail_comms_at < 1:
        raise ValueError("fail_comms_at must be >= 1 when provided")
    rng = random.Random(seed)
    blocked = OBSTACLES | WATER
    path = find_path(START, OBSERVATION_POINT, blocked)
    if path is None:
        raise RuntimeError("No safe route exists in this scenario.")

    events = []
    state = "COMPLETED_SIMULATION"
    visited = [path[0]]
    stop_reason = None
    # Simulated comms failure is injected before taking the indexed step.
    for step_index, cell in enumerate(path[1:], start=1):
        if fail_comms_at is not None and step_index >= fail_comms_at:
            state = "SAFE_STOP_SIMULATED"
            stop_reason = f"Injected communication loss at step {step_index}"
            events.append({"step": step_index, "event": "SAFE_STOP",
                           "detail": stop_reason, "cell": list(visited[-1])})
            break
        # Defensive invariant: no generated path cell can enter blocked terrain.
        if cell in blocked:
            state = "SAFE_STOP_SIMULATED"
            stop_reason = "Blocked-cell invariant violated"
            events.append({"step": step_index, "event": "SAFE_STOP",
                           "detail": stop_reason, "cell": list(visited[-1])})
            break
        visited.append(cell)
        events.append({"step": step_index, "event": "MOVE_SIMULATED",
                       "cell": list(cell)})

    reached_waypoint = visited[-1] == OBSERVATION_POINT
    detections = []
    if reached_waypoint:
        for person_cell in POSSIBLE_PEOPLE:
            # Synthetic observation event, not an AI vision model prediction.
            detections.append({
                "location_grid_xy": list(person_cell),
                "label": "POSSIBLE_PERSON_SYNTHETIC",
                "confidence": round(rng.uniform(0.55, 0.95), 2),
                "requires_human_verification": True,
            })
        events.append({"step": len(visited) - 1, "event": "OBSERVATION_POINT_REACHED",
                       "cell": list(OBSERVATION_POINT)})

    safe_steps = sum(1 for p in visited if p not in blocked)
    return {
        "title": "Flood Rescue AI — synthetic 2D reconnaissance demo",
        "status": state,
        "evidence_type": "SYNTHETIC_GRID_SIMULATION",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "map": {"width": W, "height": H, "legend": {
            "S": "start", "R": "current rover", "G": "observation waypoint",
            "P": "synthetic possible-person marker", "~": "blocked water",
            "#": "blocked debris/structure", "?": "unknown/unobserved cell",
            "*": "planned path", ".": "unclassified free cell"},
            "ascii": render_map(path, visited[-1])},
        "mission": {
            "start_xy": list(START),
            "observation_waypoint_xy": list(OBSERVATION_POINT),
            "planned_path_xy": [list(p) for p in path],
            "visited_path_xy": [list(p) for p in visited],
            "planned_steps": len(path) - 1,
            "executed_steps": len(visited) - 1,
            "reached_observation_waypoint": reached_waypoint,
            "path_contains_blocked_cell": any(p in blocked for p in path),
            "safe_visited_cells": safe_steps,
            "unknown_cells_preserved": [list(p) for p in sorted(UNKNOWN)],
        },
        "synthetic_observations": detections,
        "stop_reason": stop_reason,
        "events": events,
        "limitations": [
            "Map, people markers, obstacles and detections are synthetic.",
            "No camera, thermal sensor, LiDAR, trained AI model, ROS, or physical robot is used.",
            "Grid path planning is not floodwater dynamics or vehicle physics.",
            "A possible-person marker is not a real person detection or rescue confirmation.",
            "This output is not evidence of field safety or operational performance.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=7, help="Random seed for repeatable synthetic confidence values.")
    parser.add_argument("--out", default="runs/flood_rescue_sim", help="Output path prefix; writes .json and .csv.")
    parser.add_argument("--fail-comms-at", type=int, default=None,
                        help="Inject simulated communication loss at this 1-based movement step.")
    args = parser.parse_args()
    if args.fail_comms_at is not None and args.fail_comms_at < 1:
        parser.error("--fail-comms-at must be >= 1")

    result = run_simulation(args.seed, args.fail_comms_at)
    prefix = Path(args.out)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = prefix.with_suffix(".json")
    csv_path = prefix.with_suffix(".csv")
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["step", "event", "cell", "detail"])
        writer.writeheader()
        for event in result["events"]:
            writer.writerow({
                "step": event.get("step", ""),
                "event": event.get("event", ""),
                "cell": event.get("cell", ""),
                "detail": event.get("detail", ""),
            })
    print(f"Status: {result['status']}")
    print(f"Evidence type: {result['evidence_type']}")
    print(f"Reached observation waypoint: {result['mission']['reached_observation_waypoint']}")
    print(f"Executed movement steps: {result['mission']['executed_steps']}")
    print(f"Synthetic possible-person markers: {len(result['synthetic_observations'])}")
    print("\nMap legend: S=start R=rover G=goal P=synthetic person ~=water #=blocked ?=unknown *=path")
    print(result["map"]["ascii"])
    print(f"\nJSON report: {json_path.resolve()}")
    print(f"CSV event log: {csv_path.resolve()}")
    print("Reminder: synthetic simulation only; not field or AI-model validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
