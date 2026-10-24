# Terrain-aware flood safety gate

## Purpose

`pui89_autonomy/flood_hazard.py` is a dependency-free, software-only route-hazard gate for repeatable tests and simulation. It evaluates supplied values for platform, water depth/current, slope, bank stability, debris/structure clearance, localization, communications, and sensor freshness.

It does **not** acquire sensors, estimate current or depth from imagery, control hardware, or validate real-world safety.

## Decision states

- `proceed_simulation`: supplied inputs passed configured software checks only; not a field authorization.
- `human_review`: conflicting sensor inputs need review.
- `safe_hold`: required input missing/invalid/stale, communications/localization unavailable, depth/current exceeds a configured limit, or ground-robot depth is at least 5.5 m.
- `replan_handoff`: route edge/bank, debris, structure clearance or configured slope makes the current route unsuitable.

Unknown required values fail safe. Do not use visual appearance alone to infer flood depth, current, foundation strength, or structural safety. A building that remains standing is not automatically safe to approach or enter.

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

The 5.5 m safe-hold rule applies to the **ground robot**. Boat and drone operation requires separate platform-specific limits and validation. Configured thresholds must come from documented engineering evidence; this module does not invent universal safe depth/current/slope values. A `proceed_simulation` result is only a software test state and never proof that a physical route is safe.
