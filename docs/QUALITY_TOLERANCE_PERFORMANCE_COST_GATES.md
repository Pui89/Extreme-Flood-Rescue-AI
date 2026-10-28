# Quality, tolerance, performance, safety and cost gates

**Status:** proposed acceptance plan for software/simulation development. This is not a validated rescue robot or proof of flood survivability.

## 1. Define tolerances from the operating envelope

For each simulated sensor and control input, document units, timestamp/freshness, calibration, valid range, uncertainty and failure behavior. Track localization uncertainty, water depth/level uncertainty, current/flow uncertainty, obstacle clearance, braking/stop distance, communication latency, battery reserve and payload. Do not set universal thresholds without vehicle, sensor and environment data. Define an operating envelope and refuse actions outside it.

## 2. Safe behavior around workers, people and animals

- The AI planner may suggest routes; a deterministic safety supervisor enforces geofences, speed/clearance limits, vehicle limits and stop conditions.
- Missing, stale, contradictory or implausible sensor data; loss of communication; low battery; unstable platform; excessive current; unknown depth; or breached limits => transition to a predefined safe state and report why.
- Never treat a person/animal detector as infallible. Unknown/occluded objects in the path require slowing/stopping and human review, not a blind approach.
- Keep a risk-assessed stand-off distance from people, workers, animals, debris, power infrastructure and unstable structures. Do not chase, trap, injure or deliberately disturb wildlife, including monkeys.
- No autonomous passenger carrying, water entry, deployment around live electrical hazards or real rescue operation until professionally risk-assessed, physically validated and authorized. A software emergency-stop simulation is not a hardware E-stop.
- Define recovery and communication-loss behavior in advance; do not resume motion automatically after a safety stop without a deliberate, safe restart.

## 3. Performance metrics

Report separately:
- perception: per-class precision/recall, false negatives/positives and uncertainty/abstention;
- localization/navigation: position error, path deviation, obstacle-clearance minimum and stop distance;
- mission simulation: task completion, route duration, intervention count and simulated contact/near-miss events;
- resilience: safe-state entry time, communication recovery, battery reserve at stop and fault-recovery success;
- robustness: tests across visibility, rain/fog assumptions, occlusion, debris, moving water parameters, sensor drift, packet delay/loss and conflicting observations;
- resource use: CPU/RAM, frame or step latency, energy model assumptions and runtime.

Record scenario seed/configuration, units, number of trials, software commit and failures. Report simulation-only metrics as simulation-only. Depth up to 15 m is a scenario parameter/design challenge, not an operating claim.

## 4. Tolerance and fault injection

Test depth bias, current estimate error, localization drift, blocked sensor, stale GPS/position, lost network, delayed command, low battery, obstacle appearing, uncertain person/animal classification and corrupted state. Every unsafe/unknown case must yield a defined safe response, a reason code and reproducible report. Simulate first; real water testing requires qualified engineering review, retrieval plan, tethering/containment where appropriate and an independently approved test plan.

## 5. Cost and maintainability

- Prefer existing Python standard-library tooling and small deterministic simulation fixtures.
- No paid APIs, cloud GPUs, automatic model downloads, recurring scheduled jobs or new dependencies by default.
- Evaluate hardware, waterproofing, corrosion protection, batteries, communications, maintenance, retrieval, training and replacement parts—not only the AI software.
- Track compute and memory before considering local VLM/VLA models. Do not download model weights until licence, file size, RAM/VRAM and local-storage checks are recorded.
- Use modular sensors, readable logs, replaceable parts and manual recovery.

## 6. Release gates

1. Software and malformed-input tests pass.
2. Fault-injection simulation demonstrates the specified safe states.
3. Performance reports are reproducible and include failed scenarios.
4. A competent reviewer approves the operating envelope and hazard analysis.
5. Instrumented, controlled hardware tests verify braking, sealing, stability, communications and recovery.
6. Independent validation and authorized pilot demonstrate the specific rescue task before operational claims.

No single software score proves rescue readiness, human safety, animal safety or flood survivability.
