# Flood Rescue AI — Fault-Injection Scenario Matrix

**Status:** proposed verification cases for a software/simulation prototype.  
**Purpose:** define repeatable tests for conservative behavior when sensing, mapping, navigation, or communications degrade. This document is a test plan, not evidence that the scenarios have already been executed or that the system is safe for field use.

## Test rules

- Run deterministic software tests or simulation only; do not test in live floodwater.
- Record commit, environment, scenario parameters, random seed, logs, and test result.
- Use **PASS**, **FAIL**, or **NOT RUN**. Never mark a scenario passed because the expected behavior is only described here.
- A stop or review state must be explicit and auditable. Missing data must not be silently replaced with a safe assumption.
- Do not connect these test cases to physical actuator authority. Any future hardware work needs independent controls and qualified safety review.

## Required fault scenarios

| ID | Injected condition | Expected conservative behavior | Evidence to record | Status |
|---|---|---|---|---|
| FR-FAULT-001 | Required sensor field missing | Mark input unavailable; stop route approval or request human review | Input, validation error, final state, audit reason | NOT RUN |
| FR-FAULT-002 | Sensor timestamp older than configured freshness limit | Reject as stale; do not treat it as current evidence | Timestamp, freshness threshold, final state | NOT RUN |
| FR-FAULT-003 | NaN, infinity, malformed coordinate, or impossible range | Reject invalid measurement; no route marked verified | Payload, rejection reason, test output | NOT RUN |
| FR-FAULT-004 | Two critical sensors disagree beyond a defined threshold | Preserve disagreement and uncertainty; request human review or STOP | Both readings, threshold, selected state and reason | NOT RUN |
| FR-FAULT-005 | Route crosses unknown/unmapped cells | Route remains unverified; do not describe unknown terrain as safe | Map fixture, route output, unknown-cell handling | NOT RUN |
| FR-FAULT-006 | Obstacle blocks the proposed path | Re-plan only with a validated checker; otherwise stop and escalate | Map, candidate route, collision-check evidence | NOT RUN |
| FR-FAULT-007 | Communication heartbeat is lost | Enter documented safe state and log communications fault | Heartbeat trace, timeout, state transition, recovery policy | NOT RUN |
| FR-FAULT-008 | Position/transform is absent, invalid, or inconsistent | Reject localization-dependent route/action | Frame IDs, transform input, rejection reason | NOT RUN |
| FR-FAULT-009 | Person detection confidence is low or evidence conflicts | Keep person status unconfirmed; require authorized human review | Detection evidence, uncertainty, review state | NOT RUN |
| FR-FAULT-010 | Outcome telemetry is lost after a proposed rescue | Do not report a person rescued or safe; mark outcome UNKNOWN / unconfirmed | Last valid event, missing evidence, final incident status | NOT RUN |
| FR-FAULT-011 | Recovery/reconnection occurs after a fault | Require fresh validated inputs and explicit state transition before resuming a simulation | Recovery trace and gate conditions | NOT RUN |
| FR-FAULT-012 | Repeated fault or timeout during recovery | Remain stopped or escalate; do not loop indefinitely in an assumed-safe state | Retry count, timeout, final state and log | NOT RUN |

## Test record template

Copy one record per scenario and execution.

- Scenario ID:
- Repository commit:
- Test code / simulator version:
- Environment:
- Fixed random seed:
- Injected fault and parameters:
- Expected result:
- Observed result:
- Log / artifact location:
- Result: **PASS / FAIL / NOT RUN**
- Deviations and failure analysis:
- Reviewer and date (UTC):

## Exit criteria before claiming software-level fault handling

1. Every applicable scenario has an automated regression test or a documented reason it cannot yet be automated.
2. The test demonstrates the observed state and the reason for that state, not merely that no exception was raised.
3. Unknown, stale, missing, and conflicting inputs cannot be reported as verified-safe evidence.
4. Rescue outcome remains unconfirmed unless an authorized responder or an independently defined evidence source confirms it.
5. All failures are recorded and corrected; CI is rerun after changes.
6. Documentation distinguishes software tests, simulation results, hardware-in-the-loop results, and field validation.

## Explicit non-claims

This matrix does not establish reliable person detection, flood-depth estimation, route safety, autonomous navigation, or successful rescue. Passing these cases would show only that the tested software paths behaved as specified in the recorded environment.
