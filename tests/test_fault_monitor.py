import pytest
from pui89_safety.fault_monitor import Domain, FaultMonitor, FaultReport, Response, Severity, decide_response


def test_critical_sensor_fault_inhibits_hazardous_actions():
    d = decide_response(FaultReport("CAMERA_LOST", Domain.SENSOR, Severity.CRITICAL, "Camera unavailable"))
    assert d.inhibit_hazardous_actions and d.alert_operator and d.require_human_review_before_resume
    assert d.response is Response.STOP_MISSION_AND_ALERT


def test_critical_security_fault_isolates_component():
    d = decide_response(FaultReport("INTEGRITY_FAIL", Domain.SECURITY, Severity.CRITICAL, "Integrity failed"))
    assert d.response is Response.ISOLATE_COMPROMISED_COMPONENT and d.inhibit_hazardous_actions


def test_physical_threat_requires_human_emergency_procedure():
    d = decide_response(FaultReport("THREAT", Domain.PHYSICAL, Severity.CRITICAL, "Threat reported"))
    assert d.response is Response.HUMAN_EMERGENCY_PROCEDURE


def test_warning_limits_operation():
    d = decide_response(FaultReport("LOW_BATTERY", Domain.POWER, Severity.WARNING, "Reserve low"))
    assert d.response is Response.LIMIT_OPERATION and d.inhibit_hazardous_actions


def test_info_keeps_monitoring():
    d = decide_response(FaultReport("HEARTBEAT_OK", Domain.SOFTWARE, Severity.INFO, "Heartbeat"))
    assert d.response is Response.CONTINUE_WITH_MONITORING and not d.alert_operator


def test_sensitive_details_are_not_logged():
    m = FaultMonitor()
    e = m.report(FaultReport("BAD_CMD", Domain.SECURITY, Severity.CRITICAL, "Rejected", details={"password":"secret"}))
    assert "details" not in e and "secret" not in str(m.snapshot())


def test_event_history_is_bounded():
    m = FaultMonitor(max_events=2)
    for i in range(3): m.report(FaultReport(f"E{i}", Domain.SOFTWARE, Severity.INFO, "event"))
    assert [e["code"] for e in m.snapshot()] == ["E1", "E2"]


def test_invalid_input_rejected():
    with pytest.raises(ValueError): FaultMonitor().report(FaultReport("", Domain.UNKNOWN, Severity.CRITICAL, "bad"))
    with pytest.raises(ValueError): FaultMonitor(max_events=0)

@pytest.mark.parametrize(
    ("code", "domain", "message"),
    [
        ("AI_PROCESS_CRASH", Domain.SOFTWARE, "AI process stopped unexpectedly"),
        ("CAMERA_OR_SENSOR_LOST", Domain.SENSOR, "Required sensor heartbeat expired"),
        ("ELECTRICAL_FAULT", Domain.POWER, "Power subsystem reported a fault"),
        ("NETWORK_LINK_LOST", Domain.NETWORK, "Required control link was lost"),
        ("MALWARE_OR_INTEGRITY_ALERT", Domain.SECURITY, "Security monitor reported a critical integrity concern"),
        ("TAMPERING_OR_THEFT_ALERT", Domain.PHYSICAL, "Tamper or physical-security alarm reported"),
        ("UNSAFE_ENVIRONMENT", Domain.ENVIRONMENT, "Operating environment is outside verified limits"),
        ("INPUT_DATA_CORRUPT", Domain.DATA, "Input data failed integrity checks"),
        ("UNCLASSIFIED_CRITICAL_FAULT", Domain.UNKNOWN, "A critical fault could not be classified"),
    ],
)
def test_critical_fault_scenarios_require_conservative_response(code, domain, message):
    """A reported critical failure must never recommend continuing hazardous autonomy."""
    decision = decide_response(FaultReport(code, domain, Severity.CRITICAL, message))
    assert decision.inhibit_hazardous_actions
    assert decision.alert_operator
    assert decision.require_human_review_before_resume
    assert decision.response is not Response.CONTINUE_WITH_MONITORING


def test_network_warning_limits_operation_and_alerts_operator():
    decision = decide_response(
        FaultReport("NETWORK_DEGRADED", Domain.NETWORK, Severity.WARNING, "Control link is unstable")
    )
    assert decision.response is Response.LIMIT_OPERATION
    assert decision.alert_operator
    assert decision.require_human_review_before_resume


def test_returned_events_and_snapshots_are_defensive_copies():
    monitor = FaultMonitor()
    event = monitor.report(FaultReport(
        "INTEGRITY_FAIL", Domain.SECURITY, Severity.CRITICAL, "Integrity check failed"
    ))
    event["decision"]["response"] = "tampered"
    snapshot = monitor.snapshot()
    snapshot[0]["decision"]["response"] = "tampered-again"
    assert monitor.snapshot()[0]["decision"]["response"] == Response.ISOLATE_COMPROMISED_COMPONENT.value


def test_blank_or_whitespace_report_fields_are_rejected():
    monitor = FaultMonitor()
    with pytest.raises(ValueError):
        monitor.report(FaultReport("   ", Domain.UNKNOWN, Severity.CRITICAL, "message"))
    with pytest.raises(ValueError):
        monitor.report(FaultReport("FAULT", Domain.UNKNOWN, Severity.CRITICAL, "   "))
