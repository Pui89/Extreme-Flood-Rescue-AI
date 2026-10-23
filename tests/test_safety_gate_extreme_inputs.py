"""Edge tests for fail-closed navigation gating.

This checks a software decision function, not physical robot safety or rescue
performance.
"""
from robotics.safety_gate import NavigationState, SafetyGate


def test_wrong_state_type_fails_closed():
    assert SafetyGate().allow_motion({"localization_confidence": 1.0}) is False


def test_huge_integer_localization_confidence_fails_closed():
    state = NavigationState(
        localization_confidence=10**10000,
        obstacle_distance_m=10.0,
    )
    assert SafetyGate().allow_motion(state) is False


def test_huge_integer_obstacle_distance_fails_closed():
    state = NavigationState(
        localization_confidence=0.99,
        obstacle_distance_m=10**10000,
    )
    assert SafetyGate().allow_motion(state) is False


def test_boolean_confidence_is_not_accepted_as_numeric():
    state = NavigationState(localization_confidence=True, obstacle_distance_m=10.0)
    assert SafetyGate().allow_motion(state) is False


def test_exact_thresholds_are_inclusive():
    gate = SafetyGate(min_localization_confidence=0.7, min_obstacle_distance_m=0.5)
    state = NavigationState(localization_confidence=0.7, obstacle_distance_m=0.5)
    assert gate.allow_motion(state) is True
