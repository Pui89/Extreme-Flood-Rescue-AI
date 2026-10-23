"""Executable fault-injection tests for the software safety gate.

These tests inject deterministic faults into proposed-action inputs. They do not
simulate physical hardware, communications, navigation, or rescue outcomes.
"""
import math

import pytest

from robotics.safety_gate import validate_proposed_action


def nominal_inputs(**overrides):
    values = {
        "sensor_health_ok": True,
        "localization_confidence": 0.95,
        "collision_free": True,
        "authorized": True,
        "emergency_stop": False,
    }
    values.update(overrides)
    return values


# Each row injects one fault while keeping the other inputs nominal.
FAULT_CASES = [
    pytest.param({"sensor_health_ok": False}, "sensor_health", id="sensor-unhealthy"),
    pytest.param({"localization_confidence": 0.79}, "low_localization_confidence", id="localization-low"),
    pytest.param({"localization_confidence": math.nan}, "invalid_localization_confidence", id="localization-nan"),
    pytest.param({"localization_confidence": math.inf}, "invalid_localization_confidence", id="localization-positive-infinity"),
    pytest.param({"localization_confidence": -math.inf}, "invalid_localization_confidence", id="localization-negative-infinity"),
    pytest.param({"localization_confidence": True}, "invalid_localization_confidence", id="localization-boolean"),
    pytest.param({"localization_confidence": 1.01}, "invalid_localization_confidence", id="localization-out-of-range"),
    pytest.param({"collision_free": False}, "collision_risk", id="collision-risk"),
    pytest.param({"authorized": False}, "operator_or_policy_not_authorized", id="authorization-missing"),
    pytest.param({"emergency_stop": True}, "emergency_stop", id="emergency-stop"),
]


@pytest.mark.parametrize("fault, expected_reason", FAULT_CASES)
def test_injected_safety_fault_never_allows_action(fault, expected_reason):
    """Fault injection must fail closed and expose the expected blocking reason."""
    decision = validate_proposed_action(**nominal_inputs(**fault))

    assert decision.allowed is False
    assert decision.reason == expected_reason


@pytest.mark.parametrize(
    "field, malformed_value, expected_reason",
    [
        pytest.param("emergency_stop", "false", "invalid_emergency_stop_flag", id="estop-string"),
        pytest.param("emergency_stop", 0, "invalid_emergency_stop_flag", id="estop-integer"),
        pytest.param("sensor_health_ok", "true", "invalid_sensor_health_flag", id="sensor-string"),
        pytest.param("sensor_health_ok", None, "invalid_sensor_health_flag", id="sensor-null"),
        pytest.param("collision_free", 1, "invalid_collision_free_flag", id="collision-integer"),
        pytest.param("collision_free", "yes", "invalid_collision_free_flag", id="collision-string"),
        pytest.param("authorized", "false", "invalid_authorization_flag", id="authorization-string"),
        pytest.param("authorized", 1, "invalid_authorization_flag", id="authorization-integer"),
    ],
)
def test_malformed_safety_flags_fail_closed(field, malformed_value, expected_reason):
    """Truthiness must never substitute for explicit boolean safety signals."""
    decision = validate_proposed_action(**nominal_inputs(**{field: malformed_value}))

    assert decision.allowed is False
    assert decision.reason == expected_reason


def test_nominal_control_case_allows_candidate_action():
    """Control case ensures the test suite distinguishes a fault from nominal input."""
    decision = validate_proposed_action(**nominal_inputs())

    assert decision.allowed is True
    assert decision.reason == "validated"


@pytest.mark.parametrize(
    "confidence, expected_allowed, expected_reason",
    [
        pytest.param(0.8, True, "validated", id="localization-exact-threshold"),
        pytest.param(math.nextafter(0.8, 0.0), False, "low_localization_confidence", id="localization-just-below-threshold"),
        pytest.param(1.0, True, "validated", id="localization-upper-bound"),
        pytest.param(0.0, False, "low_localization_confidence", id="localization-lower-bound"),
    ],
)
def test_localization_confidence_boundary_is_explicit(confidence, expected_allowed, expected_reason):
    """Pin the inclusive 0.8 acceptance threshold and probability endpoints."""
    decision = validate_proposed_action(**nominal_inputs(localization_confidence=confidence))

    assert decision.allowed is expected_allowed
    assert decision.reason == expected_reason

@pytest.mark.parametrize(
    "confidence",
    [pytest.param(10**10000, id="huge-integer"), pytest.param(-10**10000, id="huge-negative-integer")],
)
def test_unrepresentably_large_localization_confidence_fails_closed(confidence):
    """Huge numeric inputs must not raise or accidentally pass the safety gate."""
    decision = validate_proposed_action(**nominal_inputs(localization_confidence=confidence))
    assert decision.allowed is False
    assert decision.reason == "invalid_localization_confidence"
