"""Edge tests for the implemented fail-closed action validator.

These test software decisions only; they do not validate physical robot safety
or rescue performance.
"""
from robotics.safety_gate import validate_proposed_action


def _valid_kwargs():
    return {
        "sensor_health_ok": True,
        "localization_confidence": 0.99,
        "collision_free": True,
        "authorized": True,
        "emergency_stop": False,
    }


def test_wrong_flag_type_fails_closed():
    decision = validate_proposed_action(**{**_valid_kwargs(), "sensor_health_ok": "true"})
    assert decision.allowed is False
    assert decision.reason == "invalid_sensor_health_flag"


def test_huge_integer_localization_confidence_fails_closed():
    decision = validate_proposed_action(
        **{**_valid_kwargs(), "localization_confidence": 10**10000}
    )
    assert decision.allowed is False
    assert decision.reason == "invalid_localization_confidence"


def test_boolean_confidence_is_not_accepted_as_numeric():
    decision = validate_proposed_action(
        **{**_valid_kwargs(), "localization_confidence": True}
    )
    assert decision.allowed is False
    assert decision.reason == "invalid_localization_confidence"


def test_exact_confidence_threshold_is_inclusive():
    decision = validate_proposed_action(
        **{**_valid_kwargs(), "localization_confidence": 0.8}
    )
    assert decision.allowed is True
    assert decision.reason == "validated"


def test_emergency_stop_blocks_otherwise_valid_action():
    decision = validate_proposed_action(
        **{**_valid_kwargs(), "emergency_stop": True}
    )
    assert decision.allowed is False
    assert decision.reason == "emergency_stop"
