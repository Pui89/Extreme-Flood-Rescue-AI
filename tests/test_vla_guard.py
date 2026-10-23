import math

import pytest

from flood_robot.action.vla_guard import VLAGuard


def safe_inputs(**overrides):
    values = {
        "action": {"mode": "hold_position"},
        "confidence": 0.90,
        "collision_free": True,
        "human_too_close": False,
        "emergency": False,
    }
    values.update(overrides)
    return values


def test_valid_proposal_is_approved():
    decision = VLAGuard().validate(**safe_inputs())
    assert decision.approved is True
    assert decision.reason == "approved"
    assert decision.action == {"mode": "hold_position"}


@pytest.mark.parametrize(
    "confidence",
    [math.nan, math.inf, -math.inf, -0.01, 1.01, True, "0.90", None, 10**400],
)
def test_invalid_confidence_fails_closed(confidence):
    decision = VLAGuard().validate(**safe_inputs(confidence=confidence))
    assert decision.approved is False
    assert decision.reason == "invalid_confidence"


@pytest.mark.parametrize("confidence", [0.0, 0.69, 0.699999])
def test_low_but_valid_confidence_is_rejected(confidence):
    decision = VLAGuard().validate(**safe_inputs(confidence=confidence))
    assert decision.approved is False
    assert decision.reason == "action_uncertainty"


@pytest.mark.parametrize(
    "threshold",
    [math.nan, math.inf, -math.inf, -0.01, 1.01, True, "0.70", None, 10**400],
)
def test_invalid_threshold_is_rejected_at_construction(threshold):
    with pytest.raises(ValueError, match="min_confidence"):
        VLAGuard(min_confidence=threshold)


@pytest.mark.parametrize("flag_name", ["collision_free", "human_too_close", "emergency"])
@pytest.mark.parametrize("invalid_flag", ["false", 0, 1, None])
def test_safety_flags_must_be_actual_booleans(flag_name, invalid_flag):
    decision = VLAGuard().validate(**safe_inputs(**{flag_name: invalid_flag}))
    assert decision.approved is False
    assert decision.reason == "invalid_safety_flag"


def test_missing_action_is_rejected():
    decision = VLAGuard().validate(**safe_inputs(action=None))
    assert decision.approved is False
    assert decision.reason == "missing_action"


@pytest.mark.parametrize(
    "overrides, expected_reason",
    [
        ({"emergency": True}, "emergency_stop"),
        ({"human_too_close": True}, "human_exclusion_zone"),
        ({"collision_free": False}, "collision_check_failed"),
    ],
)
def test_existing_safety_conditions_still_block(overrides, expected_reason):
    decision = VLAGuard().validate(**safe_inputs(**overrides))
    assert decision.approved is False
    assert decision.reason == expected_reason
