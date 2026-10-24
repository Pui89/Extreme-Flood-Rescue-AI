# Flood Rescue AI — Robot Build Sequence

**Purpose:** turn the repository's existing software prototype and robot concept into a testable, human-supervised rescue-robot research platform.

**Current boundary:** this plan does not claim a physical robot, trained flood-victim detector, validated flood-depth estimate, safe autonomous navigation, waterproofing, or field rescue capability. Do not use a prototype for emergency response.

## Target system

The long-term concept is a modular reconnaissance platform with a sealed central electronics bay, wide stable base, high-mounted RGB camera, optional thermal camera, water-level sensing, lights, communications, and a removable observation/supply module. A ground rover, tethered test boat, drone, and quadruped are different platforms; do not combine them into one physical build until each subsystem has a justified, separately tested role.

```text
Recorded / simulated observations
          |
          v
Input validation + timestamp + sensor-health checks
          |
          v
Separate perception tasks
(person candidates | flood-scene segmentation | obstacles)
          |
          v
Uncertainty-aware map and route proposal
          |
          v
Deterministic safety supervisor
(STOP / SAFE HOLD / REQUEST HUMAN REVIEW)
          |
          v
Human operator dashboard + auditable event log
          |
          v
Simulation adapter first; hardware interface only after review
```

## Free-first build stages

### Stage 0 — Establish the software baseline

- Use the existing local simulation, decision-support agent, safety supervisor, and automated tests.
- Record the exact Git commit, Python version, commands, test count, and failures for each run.
- Keep all scenarios synthetic unless source, permission, licence, privacy restrictions, and labels have been reviewed.
- Do not download large model weights or install a new robotics stack without checking disk/RAM requirements first.

**Acceptance gate:** existing tests run reproducibly; outputs explicitly label synthetic observations; unknown or malformed inputs cannot become a confident rescue claim.

### Stage 1 — Repeatable flood scenarios

Create fixed-seed scenarios for: clear route, blocked route, possible-person marker, stale camera frame, missing water reading, contradictory sensors, low battery, localization loss, communication loss, and emergency stop.

For each scenario, save the input, expected safe response, actual response, pass/fail, and event log. Test failures as carefully as nominal paths.

**Acceptance gate:** every injected critical fault leads to STOP, SAFE HOLD, or human review as specified; no test can command a physical actuator.

### Stage 2 — Perception evidence

Treat these as separate tasks with separate datasets and metrics:

- **Person detection:** independently licensed, labelled person imagery; report precision, recall, false negatives, and per-condition failures.
- **Flood-scene segmentation:** evaluate only classes actually present in the selected dataset; report per-class IoU/Dice and confusion.
- **Water depth:** require calibrated depth/range sensing or another independently validated measurement method. RGB appearance alone is not a trustworthy depth measurement.
- **Obstacle detection:** document sensor modality, blind spots, and uncertainty.

Freeze a test split grouped by event/video/location before training. Keep model outputs advisory and never describe synthetic markers as AI detections.

**Acceptance gate:** publish reproducible held-out results with dataset/version, licence, split counts, model/checkpoint hash, machine, latency, and failure analysis. If no verified data is ready, report “not evaluated.”

### Stage 3 — Simulation navigation

Only after Stage 1 passes, evaluate a compatible local simulator and navigation stack. Verify installation cost, licences, laptop resources, coordinate frames, collision checking, unknown-space handling, and emergency-stop behavior. Start with dry, low-risk scenarios; add simulated water constraints only when their meaning is explicit.

**Acceptance gate:** repeatable route tests and fault-injection results exist; unknown terrain is not silently treated as traversable; communications loss produces a safe response.

### Stage 4 — Controlled sensor bench

Only if suitable equipment is already available: test one camera and one calibrated water-level sensor on a desk or dry bench. Record timestamps, missing readings, calibration, and environmental limits. No purchases are required for software stages.

**Acceptance gate:** sensor readings are traceable and fault states are tested. Bench results do not prove waterproofing or flood performance.

### Stage 5 — Physical platform feasibility

Do not build or test in live floodwater. Before any physical prototype, complete a hazard review covering buoyancy/stability, ingress protection, battery isolation, propulsion entanglement, tether/recovery, emergency stop, communications loss, and bystander risk. Use qualified supervision and a controlled pool/pond only after an independent review. Never carry or manipulate a person as an initial test.

**Acceptance gate:** written review, manual recovery method, independent stop, safe test area, and documented staged trials are in place. A physical trial is not permission for emergency deployment.

## Free-first and safety rules

- No paid APIs, cloud GPUs, subscriptions, or hosted inference are required by this plan.
- Software tooling may be free; physical sensors, enclosures, batteries, radios, and test facilities may cost money. Ask before spending.
- Never automatically merge code or connect prototype AI output directly to motors, propulsion, or manipulators.
- Keep private location/rescue data out of public commits and logs.
- Report only checks actually run; keep software tests, simulation results, bench measurements, and field evidence distinct.

## Immediate next action

Run the existing local simulation and tests from the repository root, capture the actual output, then add one deterministic fault scenario at a time. Do not start model training until lawful task-specific data and a frozen evaluation split are ready.
