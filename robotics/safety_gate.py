from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str


def validate_proposed_action(
    *,
    sensor_health_ok: bool,
    localization_confidence: float,
    collision_free: bool,
    authorized: bool,
    emergency_stop: bool,
) -> SafetyDecision:
    """Deterministic software boundary for candidate actions.

    This function does not command hardware. It only accepts or blocks a
    proposed action before an authorized robotics control layer can consume it.
    Confidence must be a finite probability in [0, 1]. Safety flags must be
    actual booleans; malformed or ambiguous inputs fail closed.
    """
    # Validate safety-critical flags by type before interpreting their values.
    # For example, the string "false" is truthy in Python and must not be
    # mistaken for a valid sensor or authorization signal.
    flags = (
        ("emergency_stop", emergency_stop, "invalid_emergency_stop_flag"),
        ("sensor_health_ok", sensor_health_ok, "invalid_sensor_health_flag"),
        ("collision_free", collision_free, "invalid_collision_free_flag"),
        ("authorized", authorized, "invalid_authorization_flag"),
    )
    for _name, value, reason in flags:
        if not isinstance(value, bool):
            return SafetyDecision(False, reason)

    if emergency_stop:
        return SafetyDecision(False, "emergency_stop")
    if not sensor_health_ok:
        return SafetyDecision(False, "sensor_health")

    if isinstance(localization_confidence, bool) or not isinstance(
        localization_confidence, (int, float)
    ):
        return SafetyDecision(False, "invalid_localization_confidence")
    try:
        confidence_is_finite = math.isfinite(localization_confidence)
    except (OverflowError, TypeError, ValueError):
        # Huge integers can overflow during float conversion inside isfinite.
        return SafetyDecision(False, "invalid_localization_confidence")
    if not confidence_is_finite or not 0.0 <= localization_confidence <= 1.0:
        return SafetyDecision(False, "invalid_localization_confidence")

    if localization_confidence < 0.8:
        return SafetyDecision(False, "low_localization_confidence")
    if not collision_free:
        return SafetyDecision(False, "collision_risk")
    if not authorized:
        return SafetyDecision(False, "operator_or_policy_not_authorized")
    return SafetyDecision(True, "validated")
