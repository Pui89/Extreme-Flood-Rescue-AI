# Engineering Assurance and Verification Plan

**Status:** engineering process document for a simulation-oriented research prototype.  
**Basis:** project-defined engineering assurance practices for requirements traceability, hazard tracking, verification, validation, and evidence-based release decisions.

## 1. Purpose and system boundary

This plan defines traceable requirements, hazards, verification evidence, and release gates for Flood Rescue AI and its proposed ground/boat/drone reconnaissance concept.

**Current scope:** software workflow, dataset provenance and manifest utilities, group-aware split/audit tools, API/dashboard, and deterministic demonstrations/tests.  
**Not established:** reliable real-world person detection, validated water-depth estimation, safe live-flood navigation, physical rescue, or an integrated field-tested robot.

AI outputs are hypotheses for trained responders. They must not independently dispatch a robot, declare a person safe, or confirm a rescue.

## 2. Requirements and verification matrix

| ID | Requirement | Verification | Acceptance evidence | Current status |
|---|---|---|---|---|
| FR-REQ-001 | Missing, malformed, stale, or non-finite sensor inputs are rejected or marked unavailable. | Unit/regression tests | Tests cover invalid values, timestamps, missing fields, sensor-quality boundaries. | Must be confirmed by CI. |
| FR-REQ-002 | A route is not labelled safe merely because an input flag says collision-free. | Code inspection and scenario tests | Documented geometry/constraints are checked or route is marked unverified. | Re-check all route paths. |
| FR-REQ-003 | Uncertain person detections remain unconfirmed and require human review. | Workflow tests | Evidence, uncertainty, and review status remain distinct. | Intended policy; verify each path. |
| FR-REQ-004 | Communication loss, stale telemetry, or critical sensor disagreement causes a conservative state. | Fault-injection simulation | Repeatable safe-state transition with reason logged. | Incomplete until demonstrated. |
| FR-REQ-005 | Related scenes/near-duplicates do not leak across data splits. | Manifest audit and split tests | Group key, dataset version, source rights, and split audit recorded. | Tools exist; each dataset needs audit. |
| FR-REQ-006 | Model metrics are reproducible on independent held-out data. | Benchmark rerun/report audit | Dataset/model versions, metric definitions, environment, failures published. | Real-world detector benchmark not established. |
| FR-REQ-007 | Rescue outcome is confirmed by an authorised responder, not inferred from lost contact or an AI score. | Acceptance review | Confirmed, unconfirmed, failed, and unknown states separated. | Physical rescue not demonstrated. |
| FR-REQ-008 | VLA proposal guard rejects malformed flags, missing actions, and confidence values outside finite [0, 1]. | Unit/regression tests | Cases cover strings/numbers used as flags, null actions, NaN/infinity, and confidence boundaries. | Gap identified; implementation and tests not yet verified. |

## 3. Initial hazard log

| Hazard | Potential consequence | Required control before operational use |
|---|---|---|
| Missed/false person detection | Delayed aid or unsafe prioritisation | Held-out evaluation, false-negative analysis, human confirmation |
| Incorrect water depth/current estimate | Vehicle enters dangerous water | Calibrated sensors and independent ground truth; mark unknown if unavailable |
| Unsafe route around current, debris, wires, or unstable structures | Injury, entrapment, robot loss | Conservative geofencing, verified vehicle limits, collision checks, responder approval |
| Communication/power loss | Robot becomes unobservable or stranded | Fault-injection tests, safe-stop/recovery policy, independent emergency controls |
| Stale/conflicting sensors | Incorrect map or action | Timestamp/health checks, conflict handling, uncertainty propagation |
| False rescue-success report | Search stops prematurely | Explicit outcome confirmation and audit trail |
| Data leakage or unlicensed data | Inflated metrics or rights violation | Provenance/licence audit and group-aware split |

This initial hazard log is not a completed formal safety analysis. Add owners, severity/likelihood ratings, mitigations, and closure evidence before field trials.

## 4. Verification, validation, and release gates

1. **Software:** regression tests pass, including malformed inputs, sensor loss, and fail-closed paths.
2. **Data:** lawful source, licence, annotation protocol, group-aware splits, and audit results are recorded.
3. **Perception:** evaluate person detection separately from flood-scene segmentation; report held-out precision/recall, false negatives, latency, uncertainty, and failures.
4. **Simulation:** fixed-seed scenarios cover obstacles, water/current assumptions, degraded visibility, GPS drift, communication loss, and emergency stop.
5. **Integration:** verify coordinate frames, time sync, vehicle limits, geofencing, collision checking, and recovery in simulation and hardware-in-the-loop before field work.
6. **Field:** require rescue-agency authorisation, qualified safety review, supervised trials, and independently recorded outcomes. No AI-only operational authority.

Verification checks requirements; validation checks suitability for intended use. Passing CI is evidence about tested software only, not a safe route or successful rescue.

## 5. Specific follow-up: VLA proposal guard

On 2026-10-23, inspection of `flood_robot/action/vla_guard.py` found that confidence is only compared with the configured minimum, rather than validated as a finite number in [0, 1]. As a result, NaN can evade the less-than comparison, and values above 1 can be treated as sufficiently confident. The current truthiness checks also allow a string such as `"false"` for `collision_free` to behave as true. A missing `action=None` is not explicitly rejected.

**Required software fix:** validate the minimum-confidence threshold at construction; require confidence to be a finite numeric value in [0, 1]; require all safety flags to be actual Boolean values; reject a missing action; and add regression tests for these cases.

**Status:** identified, not implemented or tested in this update. The connected GitHub tool blocked the attempted code write, so no claim is made that the guard is fixed. This software guard is not a certified safety controller and must not be treated as sufficient for physical actuation.

## 6. Evidence and change control

Record commit, environment, command, dataset/model version, seed, scenario parameters, raw output, metric definitions, and limitations for each result. Separate simulation from real-world results. Safety-related changes require regression tests and human review.

## 7. Cost and licensing

Prefer local execution and free/open-source tools. Check dependency and dataset licences. Do not add paid APIs, hosted inference, cloud GPUs, subscriptions, or billing-triggering workflows without explicit approval.

## 8. Review boundary

This project-level plan supports disciplined engineering and evidence tracking. It does not replace independent safety, legal, privacy, domain-expert, or operational review.
