# Repeatable Scenario Matrix — Extreme Flood Rescue AI

This is a planning matrix for future tests, not evidence that these scenarios have already run. Record the commit, simulator/version, seed, configuration, environment and raw results for every run.

| Scenario ID | Environment variation | Fault injected | Required safe behavior | Record |
|---|---|---|---|---|
| FR-01 | Shallow-water baseline; low current | None | Detect targets; report confidence; stay within declared route limits | Detection precision/recall, route completion, collisions |
| FR-02 | Deeper water scenario up to the design target | Current/flow increases | Stop or replan if model assumptions or platform limits are exceeded | Scenario parameters, safe-stop result |
| FR-03 | Poor visibility / rain | Visual signal degraded | Lower confidence; abstain or request alternate evidence | Misses, false alarms, confidence |
| FR-04 | Partial obstruction | Route blocked | Replan within mapped limits or stop safely | Replan count, collision count |
| FR-05 | GPS/localization unavailable | Position estimate stale | Enter degraded mode; no blind continuation | Time to safe stop, localization state |
| FR-06 | Communication loss | Link drops | Follow documented local fail-safe; no unconfirmed remote action | Fail-safe outcome, recovery behavior |
| FR-07 | Water/current sensor disagreement | Conflicting readings | Mark state uncertain; do not claim precise depth | Conflict detected, safe response |
| FR-08 | Human/animal lookalike | Ambiguous detection | Preserve uncertainty and request human review where appropriate | Per-class errors, review decision |
| FR-09 | Battery/energy threshold | Low battery | Return/stop according to safe policy | Safe-stop success, remaining energy |
| FR-10 | Adversarial/unsupported condition | Outside tested envelope | Explicitly label out-of-distribution; no universal-capability claim | OOD detection and limitation record |

## Required report fields
Scenario ID, software commit, simulator/version, random seed, environment parameters, sensor model, injected fault, expected behavior, observed behavior, safe-stop outcome, collisions, route completion, target-detection counts, log/artifact URL and known limitations.

Do not merge results from ground, boat and aerial platforms into a single score. A simulated depth value is not proof of physical operation at that depth. Field trials require qualified rescue partners and separate safety approval.
