import math

import pytest

from robotics.safety_gate import validate_proposed_action


def safe_inputs(**overrides):
    values = {
        "sensor_health_ok": True,
        "localization_confidence": 0.95,
        "collision_free": True,
        "authorized": True,
        "emergency_stop": False,
    }
    values.update(overrides)
    return values


def test_valid_proposal_is_allowed():
    decision = validate_proposed_action(**safe_inputs())
    assert decision.allowed is True
    assert decision.reason == "validated"


@pytest.mark.parametrize(
    "confidence",
    [math.nan, math.inf, -math.inf, -0.01, 1.01, True, "0.95", None],
)
def test_invalid_confidence_fails_closed(confidence):
    decision = validate_proposed_action(
        **safe_inputs(localization_confidence=confidence)
    )
    assert decision.allowed is False
    assert decision.reason == "invalid_localization_confidence"


@pytest.mark.parametrize("confidence", [0.0, 0.79, 0.799999])
def test_low_but_valid_confidence_fails_closed(confidence):
    decision = validate_proposed_action(
        **safe_inputs(localization_confidence=confidence)
    )
    assert decision.allowed is False
    assert decision.reason == "low_localization_confidence"


@pytest.mark.parametrize(
    "overrides, expected_reason",
    [
        ({"emergency_stop": True}, "emergency_stop"),
        ({"sensor_health_ok": False}, "sensor_health"),
        ({"collision_free": False}, "collision_risk"),
        ({"authorized": False}, "operator_or_policy_not_authorized"),
    ],
)
def test_existing_safety_conditions_still_block(overrides, expected_reason):
    decision = validate_proposed_action(**safe_inputs(**overrides))
    assert decision.allowed is False
    assert decision.reason == expected_reason
