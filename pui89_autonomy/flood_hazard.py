"""Terrain-aware flood hazard gate for software simulation and test scenarios.

This module evaluates explicitly supplied values. It does not read sensors, estimate
flood conditions, control a robot, or certify a route as physically safe.
"""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
import math
from typing import Optional



class HazardState(str, Enum):
    PROCEED_SIMULATION = "proceed_simulation"
    HUMAN_REVIEW = "human_review"
    SAFE_HOLD = "safe_hold"
    REPLAN_HANDOFF = "replan_handoff"


@dataclass(frozen=True)
class FloodHazardInputs:
    platform: str
    water_depth_m: Optional[float]
    current_speed_mps: Optional[float]
    slope_deg: Optional[float]
    bank_stable: Optional[bool]
    debris_clear: Optional[bool]
    structure_clear: Optional[bool]
    localization_ok: Optional[bool]
    communication_ok: Optional[bool]
    sensor_age_s: Optional[float]
    max_sensor_age_s: float = 2.0
    platform_depth_limit_m: Optional[float] = None
    platform_current_limit_mps: Optional[float] = None
    platform_slope_limit_deg: Optional[float] = None
    sensor_conflict: bool = False
    emergency_stop_active: Optional[bool] = None
    safety_monitor_ok: Optional[bool] = None
    battery_ok: Optional[bool] = None
    propulsion_ok: Optional[bool] = None


@dataclass(frozen=True)
class HazardDecision:
    state: HazardState
    reasons: tuple[str, ...]
    audit_record: dict


def _valid_nonnegative(value: Optional[float]) -> bool:
    return value is not None and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def assess_flood_hazard(
    inputs: FloodHazardInputs,
    *,
    decision_time: Optional[str] = None,
) -> HazardDecision:
    """Return a conservative advisory state and an auditable, JSON-friendly record.

    Unknown/stale required readings fail to SAFE_HOLD. A route hazard that could
    be avoided leads to REPLAN_HANDOFF. Uncertainty/conflicting sensors leads to
    HUMAN_REVIEW. No state commands physical actuators.
    """
    reasons: list[str] = []
    hard_holds: list[str] = []
    replan: list[str] = []
    review: list[str] = []

    if inputs.platform not in {"ground", "boat", "drone"}:
        raise ValueError("platform must be 'ground', 'boat', or 'drone'")

    boolean_inputs = {
        "bank_stable": inputs.bank_stable,
        "debris_clear": inputs.debris_clear,
        "structure_clear": inputs.structure_clear,
        "localization_ok": inputs.localization_ok,
        "communication_ok": inputs.communication_ok,
        "sensor_conflict": inputs.sensor_conflict,
        "emergency_stop_active": inputs.emergency_stop_active,
        "safety_monitor_ok": inputs.safety_monitor_ok,
        "battery_ok": inputs.battery_ok,
        "propulsion_ok": inputs.propulsion_ok,
    }
    malformed_booleans = [name for name, value in boolean_inputs.items() if value is not None and not isinstance(value, bool)]
    if malformed_booleans:
        raise ValueError("status inputs must be booleans or None: " + ", ".join(malformed_booleans))

    required_common = {
        "bank_stable": inputs.bank_stable,
        "debris_clear": inputs.debris_clear,
        "structure_clear": inputs.structure_clear,
        "localization_ok": inputs.localization_ok,
        "communication_ok": inputs.communication_ok,
        "emergency_stop_active": inputs.emergency_stop_active,
        "safety_monitor_ok": inputs.safety_monitor_ok,
        "battery_ok": inputs.battery_ok,
        "propulsion_ok": inputs.propulsion_ok,
    }
    missing = [name for name, value in required_common.items() if value is None]
    if missing:
        hard_holds.append("required hazard/status input missing: " + ", ".join(missing))

    if not _valid_nonnegative(inputs.sensor_age_s):
        hard_holds.append("sensor age is missing or invalid")
    elif not _valid_nonnegative(inputs.max_sensor_age_s) or inputs.max_sensor_age_s <= 0:
        raise ValueError("max_sensor_age_s must be finite and greater than zero")
    elif inputs.sensor_age_s > inputs.max_sensor_age_s:
        hard_holds.append("sensor data is stale")

    if inputs.sensor_conflict:
        review.append("sensor inputs conflict; human review required")

    if inputs.emergency_stop_active is True:
        hard_holds.append("emergency stop is active")
    for name, value in (
        ("localization_ok", inputs.localization_ok),
        ("communication_ok", inputs.communication_ok),
        ("safety_monitor_ok", inputs.safety_monitor_ok),
        ("battery_ok", inputs.battery_ok),
        ("propulsion_ok", inputs.propulsion_ok),
    ):
        if value is False:
            hard_holds.append(name.replace("_", " ") + " is unavailable")

    if inputs.bank_stable is False:
        replan.append("bank or route-edge stability is not confirmed")
    if inputs.debris_clear is False:
        replan.append("debris or submerged-obstacle clearance is not confirmed")
    if inputs.structure_clear is False:
        replan.append("structure or crossing clearance is not confirmed")

    if inputs.platform in {"ground", "boat"}:
        if not _valid_nonnegative(inputs.water_depth_m):
            hard_holds.append("water depth is missing or invalid")
        if not _valid_nonnegative(inputs.current_speed_mps):
            hard_holds.append("current speed is missing or invalid")
        if inputs.water_depth_m is not None and _valid_nonnegative(inputs.water_depth_m):
            if inputs.platform_depth_limit_m is None:
                hard_holds.append("platform depth limit is not configured")
            elif _valid_nonnegative(inputs.platform_depth_limit_m) and inputs.water_depth_m > inputs.platform_depth_limit_m:
                hard_holds.append("water depth exceeds the configured platform limit")
        if inputs.platform_current_limit_mps is None:
            hard_holds.append("platform current limit is not configured")
        elif (
            _valid_nonnegative(inputs.current_speed_mps)
            and inputs.current_speed_mps > inputs.platform_current_limit_mps
        ):
            hard_holds.append("current speed exceeds the configured platform limit")

    if inputs.slope_deg is None or not isinstance(inputs.slope_deg, (int, float)) or not math.isfinite(inputs.slope_deg):
        hard_holds.append("terrain slope is missing or invalid")
    elif inputs.slope_deg < 0 or inputs.slope_deg > 90:
        hard_holds.append("terrain slope is outside the valid [0, 90] degree range")
    elif inputs.platform == "ground" and inputs.platform_slope_limit_deg is None:
        hard_holds.append("platform slope limit is not configured")
    elif (
        inputs.platform == "ground"
        and inputs.platform_slope_limit_deg is not None
        and _valid_nonnegative(inputs.platform_slope_limit_deg)
        and inputs.slope_deg > inputs.platform_slope_limit_deg
    ):
        replan.append("terrain slope exceeds the configured platform limit")

    for limit_name, value in (
        ("platform_depth_limit_m", inputs.platform_depth_limit_m),
        ("platform_current_limit_mps", inputs.platform_current_limit_mps),
        ("platform_slope_limit_deg", inputs.platform_slope_limit_deg),
    ):
        if value is not None and not _valid_nonnegative(value):
            raise ValueError(limit_name + " must be finite and nonnegative when provided")

    if hard_holds:
        state = HazardState.SAFE_HOLD
        reasons = hard_holds + review + replan
    elif review:
        state = HazardState.HUMAN_REVIEW
        reasons = review + replan
    elif replan:
        state = HazardState.REPLAN_HANDOFF
        reasons = replan
    else:
        state = HazardState.PROCEED_SIMULATION
        reasons = ["supplied inputs passed configured software checks; not physical safety approval"]

    timestamp = decision_time or datetime.now(timezone.utc).isoformat()
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise ValueError("decision_time must be a non-empty ISO-8601 string when provided")

    record = {
        "decision_time": timestamp,
        "evidence_type": "SUPPLIED_INPUT_SOFTWARE_GATE",
        "platform": inputs.platform,
        "inputs": asdict(inputs),
        "state": state.value,
        "reasons": list(reasons),
        "physical_safety_validated": False,
    }
    return HazardDecision(state=state, reasons=tuple(reasons), audit_record=record)
