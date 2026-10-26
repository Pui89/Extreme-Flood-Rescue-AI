# Simulation-only platform-envelope gate

## Purpose

`scripts/platform_envelope_gate.py` is a small, standard-library-only decision gate for deterministic flood-scenario tests. It checks explicit scenario depth/current against declared limits and checks required status flags. Missing, malformed, stale, conflicting, unreviewed, or out-of-limit conditions produce `SAFE_HOLD`.

It does **not** model fluid dynamics, establish a real platform's safe operating envelope, certify equipment, or control hardware.

## Run the tests

From the repository root, with Python installed:

```powershell
python -m unittest tests.test_platform_envelope_gate -v
```

No model, package download, network connection, paid API, or GPU is required.

## Input contract

The scenario must include:

- `depth_m`, `current_mps`: finite, non-negative numeric values
- `sensor_data_fresh`, `sensors_valid`, `communications_available`
- `safety_monitor_healthy`, `emergency_stop_active`
- `recovery_path_available`

The envelope must include:

- `platform_type`
- `max_depth_m`, `max_current_mps`
- `limits_reviewed`: explicit boolean
- `evidence_reference`: non-empty traceability reference

The test fixture's values are examples only, not recommended engineering limits. Real values must not be guessed or copied across different vehicle types.

## Decision meanings

- `SAFE_HOLD`: a required input is missing/invalid, a required health condition is not met, limits have not been reviewed, or the scenario exceeds a declared limit.
- `SIMULATION_ONLY_GATE_PASS`: the supplied scenario passes these limited software checks only. It is not a physical safety approval or permission to deploy.

## Still required before stronger claims

1. Define platform-specific limits from qualified engineering analysis and controlled evidence.
2. Model current, waves, debris, water ingress, buoyancy/stability, sensor degradation and recovery conditions in an appropriate simulator.
3. Add reproducible scenario fixtures and test failures, stale/conflicting readings, boundary values and operator acknowledgement.
4. Keep software tests, simulation results, hardware-in-the-loop tests and field tests reported separately.
5. Have qualified reviewers approve any real-world safety case. This script cannot replace independent safety controls or a physical emergency-stop chain.
