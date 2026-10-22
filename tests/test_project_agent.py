from agents.project_agent import run_agent


def test_missing_localization_holds():
    assert run_agent({}).recommendation == "HOLD_AND_RELOCALIZE"


def test_unclear_route_stops():
    d = run_agent({"localization_ok": True, "water_depth_m": .2, "route_clear": False})
    assert d.status == "STOP"
    assert d.actuator_command is None


def test_possible_person_alerts_operator():
    d = run_agent({"localization_ok": True, "water_depth_m": .1, "route_clear": True,
                   "person_detected": True, "detection_confidence": .8})
    assert d.recommendation == "ALERT_HUMAN_RESCUE_OPERATOR"


def test_invalid_depth_requests_data():
    assert run_agent({"localization_ok": True, "water_depth_m": -1}).status == "NEED_DATA"
