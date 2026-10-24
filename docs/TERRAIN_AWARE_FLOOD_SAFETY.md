# Terrain-aware flood safety gate

## Purpose

`pui89_autonomy/flood_hazard.py` is a dependency-free, software-only route-hazard gate for repeatable tests and simulation. It evaluates supplied values for platform, water depth/current, slope, bank stability, debris/structure clearance, localization, communications, sensor freshness, emergency-stop status, safety-monitor health, battery status, and propulsion/drive health.

It does **not** acquire sensors, estimate current or depth from imagery, control hardware, or validate real-world safety.

## Decision states

- `proceed_simulation`: supplied inputs passed configured software checks only; not a field authorization.
- `human_review`: conflicting sensor inputs need review.
- `safe_hold`: required input missing/invalid/stale, communications/localization unavailable, a required platform depth limit is not configured, or depth/current exceeds an explicitly configured limit.
- `replan_handoff`: route edge/bank, debris, structure clearance or configured slope makes the current route unsuitable.

Unknown required values fail safe. The software gate requires explicit emergency-stop, safety-monitor, battery and propulsion status; an active emergency stop or reported fault leads to `safe_hold`. This does not physically stop a robot because the module does not control hardware. Do not use visual appearance alone to infer flood depth, current, foundation strength, or structural safety. A building that remains standing is not automatically safe to approach or enter.

See [Robot protection and safety case](ROBOT_PROTECTION_AND_SAFETY_CASE.md) for layered protective design, independent hardware stop/watchdog requirements, and the evidence ladder. The protective design practices are requirements—not proof that a physical robot is safe.

## Run tests (Python standard library only)

```bat
python -m unittest discover -s tests -p "test_flood_hazard.py" -v
python -m unittest discover -s tests -p "test_autonomy_supervisor.py" -v
python -m unittest discover -s tests -p "test_flood_rescue_sim.py" -v
```

The tests are committed but have not been run on the user's computer by this change. Run locally or inspect the PR's CI results before treating them as verified.

## Audit record

Each decision returns a structured in-memory `audit_record` with timestamp, supplied inputs, decision state, reasons, evidence type, and `physical_safety_validated: false`. This is not persistent storage and does not prove input authenticity. The caller must save it if durable records are required and must avoid logging unnecessary personal data.

## Platform boundaries

The simulation scenario range is **0–15 m**; it is not a physical capability rating. There is no universal hard-coded 5.5 m cutoff in this gate. Ground and boat decisions require an explicit platform depth limit; current and slope limits should also be configured from documented platform-specific engineering evidence. Drone operation requires its own relevant limits and validation. A `proceed_simulation` result is only a software test state and never proof that a physical route is safe.
