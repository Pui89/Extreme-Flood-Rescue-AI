"""Fail-closed, simulation-only platform-envelope gate for flood scenarios.

This module checks declared scenario values against explicit, reviewed limits.
It does not model hydrodynamics, certify a platform, or control hardware.
Unknown/missing inputs always produce SAFE_HOLD.
"""
from __future__ import annotations

import math
from typing import Any, Mapping


def _finite_nonnegative(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and math.isfinite(value)
        and value >= 0
    )


def evaluate_platform_envelope(
    scenario: Mapping[str, Any],
    envelope: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a conservative software decision; never commands or controls a robot.

    Required scenario fields: depth_m, current_mps, sensor_data_fresh,
    sensors_valid, communications_available, safety_monitor_healthy,
    emergency_stop_active, recovery_path_available.

    Required envelope fields: platform_type, max_depth_m, max_current_mps,
    limits_reviewed, evidence_reference. The limits must be explicit and
    reviewed for this simulation; this does not establish physical capability.
    """
    required_scenario = (
        "depth_m", "current_mps", "sensor_data_fresh", "sensors_valid",
        "communications_available", "safety_monitor_healthy",
        "emergency_stop_active", "recovery_path_available",
    )
    required_envelope = (
        "platform_type", "max_depth_m", "max_current_mps",
        "limits_reviewed", "evidence_reference",
    )

    missing = [f"scenario.{key}" for key in required_scenario if key not in scenario]
    missing += [f"envelope.{key}" for key in required_envelope if key not in envelope]
    if missing:
        return {
            "decision": "SAFE_HOLD",
            "reason_codes": ["MISSING_REQUIRED_INPUT"],
            "missing_fields": missing,
            "scope": "simulation-only software gate; no hardware control",
        }

    invalid = []
    for key in ("depth_m", "current_mps"):
        if not _finite_nonnegative(scenario.get(key)):
            invalid.append(f"scenario.{key}")
    for key in ("max_depth_m", "max_current_mps"):
        if not _finite_nonnegative(envelope.get(key)):
            invalid.append(f"envelope.{key}")
    for key in (
        "sensor_data_fresh", "sensors_valid", "communications_available",
        "safety_monitor_healthy", "emergency_stop_active",
        "recovery_path_available", "limits_reviewed",
    ):
        owner = "envelope" if key == "limits_reviewed" else "scenario"
        value = envelope.get(key) if owner == "envelope" else scenario.get(key)
        if not isinstance(value, bool):
            invalid.append(f"{owner}.{key}")
    for key in ("platform_type", "evidence_reference"):
        if not isinstance(envelope.get(key), str) or not envelope[key].strip():
            invalid.append(f"envelope.{key}")

    if invalid:
        return {
            "decision": "SAFE_HOLD",
            "reason_codes": ["INVALID_REQUIRED_INPUT"],
            "invalid_fields": invalid,
            "scope": "simulation-only software gate; no hardware control",
        }

    reasons = []
    if envelope["limits_reviewed"] is not True:
        reasons.append("LIMITS_NOT_REVIEWED")
    if scenario["sensor_data_fresh"] is not True:
        reasons.append("SENSOR_DATA_STALE")
    if scenario["sensors_valid"] is not True:
        reasons.append("SENSOR_INVALID")
    if scenario["communications_available"] is not True:
        reasons.append("COMMUNICATIONS_UNAVAILABLE")
    if scenario["safety_monitor_healthy"] is not True:
        reasons.append("SAFETY_MONITOR_UNHEALTHY")
    if scenario["emergency_stop_active"] is True:
        reasons.append("EMERGENCY_STOP_ACTIVE")
    if scenario["recovery_path_available"] is not True:
        reasons.append("RECOVERY_PATH_UNAVAILABLE")
    if scenario["depth_m"] > envelope["max_depth_m"]:
        reasons.append("DEPTH_LIMIT_EXCEEDED")
    if scenario["current_mps"] > envelope["max_current_mps"]:
        reasons.append("CURRENT_LIMIT_EXCEEDED")

    return {
        "decision": "SAFE_HOLD" if reasons else "SIMULATION_ONLY_GATE_PASS",
        "reason_codes": reasons,
        "platform_type": envelope["platform_type"],
        "evidence_reference": envelope["evidence_reference"],
        "scope": "simulation-only software gate; no hardware control",
        "warning": (
            "A gate pass is not a physical safety approval, depth rating, "
            "rescue-performance result, or authorization to deploy."
        ),
    }
