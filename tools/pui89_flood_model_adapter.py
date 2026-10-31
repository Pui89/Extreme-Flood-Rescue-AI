"""Extreme Flood Rescue project adapter: simulated hazard observations only."""
from __future__ import annotations
import math
from typing import Any
from pui89_project_adapter_common import build_review_envelope

def adapt_flood_mock(request: Any) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("request must be an object")
    sample = request.get("mock_observation")
    if not isinstance(sample, dict):
        raise ValueError("mock_observation must be an object")
    depth = sample.get("scenario_depth_m")
    if isinstance(depth, bool) or not isinstance(depth, (int, float)) or not math.isfinite(depth):
        raise ValueError("scenario_depth_m must be a finite number")
    if not 0 <= depth <= 15:
        raise ValueError("scenario_depth_m must be within the 0-15 m simulation scenario range")
    hazards = sample.get("hazard_observations")
    if not isinstance(hazards, list) or not hazards or not all(
        isinstance(item, str) and item.strip() for item in hazards
    ):
        raise ValueError("hazard_observations must be a non-empty list of descriptive strings")
    observation = {
        "domain": "extreme_flood_rescue",
        "observation_type": "simulated_hazard_context",
        "scenario_depth_m": float(depth),
        "hazard_observations": hazards,
        "interpretation": "simulation_fixture_for_operator_review",
    }
    return build_review_envelope(
        project_id="extreme_flood_rescue", request=request,
        observation=observation, modality="simulation_mock_fixture",
        limitations=[
            "Depth is a simulated scenario input, not a demonstrated operating limit.",
            "This adapter does not detect people, animals, currents or obstacles from sensor data.",
            "It does not generate routes, rescue commands or movement instructions.",
            "No claim of operation at 15 m flood depth or in real flood conditions is made.",
        ],
    )
