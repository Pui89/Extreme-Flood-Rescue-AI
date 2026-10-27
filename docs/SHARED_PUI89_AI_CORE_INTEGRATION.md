# Shared PUI89 AI Core — Extreme Flood Rescue adapter

**Status:** simulation-first integration contract. Passing synthetic checks is not flood-physics evidence, rescue validation, or proof of operation at 15 m.

## Shared contract

Use the existing standard-library autonomy lab, world-state tracker, and reproducible report builder as Phase 1. Each scenario should include a stable ID, seed label, simulated time, sensor observations, hazards, expected mode/action, and explicit fault injection. Results should capture actual mode/action, guard trace, failure codes, step latency, configuration/code hashes, and limitations.

Sensor observations should carry timestamps, freshness, quality/confidence, source, and explicit missing/unknown states. The world-state must not replace a missing reading with a guessed value.

## Required fault-injection cases

- Depth, current, localisation, camera, or range sensor absent, stale, malformed, out of range, or mutually inconsistent.
- Communication loss between operator and vehicle or between simulated platforms.
- Water depth/current outside the configured and reviewed operating envelope.
- Human/animal detection uncertain, occluded, or contradictory across sensors.
- Map/localisation confidence degraded or obstacle state unknown.
- Emergency stop requested during navigation, target approach, or simulated assistance.
- Scenario configuration missing required limits or containing invalid numeric values.

## Expected conservative behavior

If a required sensor/limit is missing, stale, conflicting, or invalid, the simulated action must be SAFE_HOLD or STOPPED according to the existing supervisor contract. No target approach or simulated rescue action should proceed on unknown safety conditions. Log the first failing gate and all relevant fault codes. Do not describe a software safe-stop as a certified physical emergency stop.

## Evidence and metrics

Report scenario count, pass/fail count, each injected fault, safe-hold/stop outcome, false-safe transitions, decision latency, configuration hash, and all NOT RUN cases. Water depth up to 15 m is a scenario input/design challenge only; it does not validate buoyancy, pressure resistance, currents, communications, passenger support, or rescue performance.

## Run order

1. Run python tools/pui89_master_verify.py.
2. Run the existing autonomy-lab tests and simulation/scenarios.json runner.
3. Run platform-envelope and fault-injection tests; retain JSON/CSV outputs.
4. Consider ROS 2/Gazebo only after deterministic tests pass and a separate licence, install-size, RAM/VRAM, and maintenance review.

**Cost boundary:** Phase 1 needs no paid API, cloud GPU, automatic download, or hardware connection.