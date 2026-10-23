import math

import pytest

from flood_robot.action.vla_guard import VLAGuard


@pytest.mark.parametrize(
    "confidence",
    [math.nan, math.inf, -math.inf, -0.1, 1.01, True, "0.9", None, [], {}, 10**400],
)
def test_rejects_invalid_confidence(confidence):
    decision = VLAGuard().validate(
        {"move": "forward"}, confidence=confidence, collision_free=True
    )
    assert not decision.approved
    assert decision.reason == "invalid_confidence"


@pytest.mark.parametrize("collision_free", ["false", 1, None, 0])
def test_rejects_malformed_collision_flag(collision_free):
    decision = VLAGuard().validate(
        {"move": "forward"}, confidence=0.99, collision_free=collision_free
    )
    assert not decision.approved
    assert decision.reason == "invalid_safety_flag"


def test_rejects_missing_action():
    decision = VLAGuard().validate(None, confidence=0.99, collision_free=True)
    assert not decision.approved
    assert decision.reason == "missing_action"


@pytest.mark.parametrize(
    "threshold", [math.nan, math.inf, -0.1, 1.01, True, "0.7", None, 10**400]
)
def test_rejects_invalid_confidence_threshold(threshold):
    with pytest.raises(ValueError):
        VLAGuard(min_confidence=threshold)


def test_approves_valid_action():
    action = {"move": "forward"}
    decision = VLAGuard().validate(action, confidence=0.99, collision_free=True)
    assert decision.approved
    assert decision.action == action


@pytest.mark.parametrize("flag", ["human_too_close", "emergency"])
@pytest.mark.parametrize("value", ["false", 0, 1, None])
def test_rejects_malformed_human_and_emergency_flags(flag, value):
    decision = VLAGuard().validate(
        {"move": "forward"},
        confidence=0.99,
        collision_free=True,
        **{flag: value},
    )
    assert not decision.approved
    assert decision.reason == "invalid_safety_flag"


@pytest.mark.parametrize(
    ("flag", "reason"),
    [("human_too_close", "human_exclusion_zone"), ("emergency", "emergency_stop")],
)
def test_human_exclusion_and_emergency_stop_override_high_confidence(flag, reason):
    decision = VLAGuard().validate(
        {"move": "forward"},
        confidence=0.99,
        collision_free=True,
        **{flag: True},
    )
    assert not decision.approved
    assert decision.reason == reason
