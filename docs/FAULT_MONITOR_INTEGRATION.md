# Fault monitor integration guide

Free, local-first software for accepting fault reports, suggesting conservative responses, and keeping a bounded in-memory event list. No third-party runtime dependencies are added.

## What it covers

Software, sensor, power, network, security, physical, environmental, data, and unknown faults—when application code explicitly reports them. Critical faults recommend inhibiting hazardous actions, alerting an operator, and requiring human review. Security-critical faults recommend isolating the affected component; physical threats require human emergency procedures.

## Test locally

```bash
python -m pip install pytest
PYTHONPATH=apps python -m pytest tests/test_fault_monitor.py -q
```

## Example

```python
from pui89_safety.fault_monitor import Domain, FaultMonitor, FaultReport, Severity
monitor = FaultMonitor()
event = monitor.report(FaultReport(
    code="SENSOR_UNAVAILABLE", domain=Domain.SENSOR,
    severity=Severity.CRITICAL, message="Required sensor heartbeat expired",
    source="sensor_monitor",
))
print(event["decision"])
```

## Limits and safe use

This is not antivirus/EDR, network intrusion detection, a gunshot/person/tamper detector, or a hardware safety controller. It does not switch off motors or electrical power. Connect it to project-specific monitoring and independently engineered safety circuits only after qualified review. Physical threats require human emergency procedures, not autonomous pursuit or confrontation. Abrupt power loss is not safe for every robot, boat, drone, slope, or suspended load. Do not log credentials, personal data, or sensitive case evidence. Persistent audit storage, alerts, malware protection, backup/restore, and hardware control must be separately implemented and tested.
