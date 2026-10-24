# Robot protection and safety case (simulation-first)

## Goal

Reduce foreseeable robot hazards through layered protection, fail-closed decisions, independent emergency stopping, and repeatable fault tests. These are established safety-engineering practices; **they are not yet proven on a physical PUI89 robot**. This repository currently evaluates supplied status values and does not read sensors or stop motors.

## Software interlocks added

The terrain-aware gate now requires explicit values for:

- emergency-stop status;
- safety-monitor health;
- battery health;
- propulsion/drive health;
- localization and communications;
- fresh sensor data, flood depth/current limits, terrain slope, bank stability, debris clearance, and structure clearance.

A missing status causes `safe_hold`. An active emergency stop, unhealthy safety monitor, low/unsafe battery status, propulsion fault, unavailable localization/communications, stale data, or exceeded configured depth/current limit also causes `safe_hold`. Malformed status values are rejected. These are software decisions only; they do not actuate hardware.

## Protective design requirements before any physical robot

1. **Independent emergency stop:** a physical, reachable stop device and an independent hardware path that removes hazardous drive/propulsion energy as appropriate to the platform. Do not rely on a Python process, network link, AI model, or screen button as the only stop.
2. **Watchdog and fail-safe state:** loss of controller heartbeat, software crash, stale command, or safety-monitor fault must transition to a defined safe state. Verify the actual hardware response, including stopping distance and residual motion.
3. **Speed and operating envelope:** enforce platform-specific speed, slope, current, depth, tilt, payload, and recovery limits derived from engineering analysis and controlled tests. Missing limits must block operation. The 0–15 m range is a simulation range, not a ground robot capability claim.
4. **Collision and exclusion zones:** independent collision checking, conservative clearance, geofencing/keep-out zones, and a stop on unknown/unobserved route cells. Do not let a generative model bypass these controls.
5. **Power protection:** monitor battery state, voltage sag, temperature, and a tested reserve for retreat/recovery. If the reserve cannot be verified, stop mission expansion and request human review.
6. **Flood-specific protection:** sealed/electrically protected enclosures, verified buoyancy and stability where relevant, corrosion-resistant connectors, tether/float/recovery strategy where appropriate, and sensor checks for water ingress. Ratings must be supported by supplier data and controlled tests; visual design alone is not proof.
7. **Communications and localization:** test link loss, delayed/out-of-order commands, GNSS denial, map mismatch, and localization jumps. The response must be deterministic and observable.
8. **Human control:** provide clear status, stop reason, and a recovery path. Require authorized human confirmation before entering uncertain/high-consequence areas or attempting a rescue.
9. **Audit and cybersecurity:** record timestamped inputs, software/configuration versions, stop reason, and operator action; authenticate commands and prevent replay/unauthorized control. Avoid storing unnecessary personal data.
10. **Verification before release:** unit tests, fault injection, hardware-in-the-loop tests, independent review, then controlled trials in low-risk environments with explicit abort criteria. Test each platform independently.

## Evidence ladder

| Level | Evidence required | What it supports |
|---|---|---|
| 1. Software unit tests | Reproducible tests for missing, stale, invalid and fault inputs | Tested logic only |
| 2. Scenario simulation | Repeatable hazard cases and safe-stop decisions | Simulated behavior only |
| 3. Physics-backed simulation | Validated environment/vehicle model, independent collision checker and fault injection | Model-dependent evidence |
| 4. Hardware-in-the-loop | Real controller/sensors with simulated environment and measured stop behavior | Integration evidence within tested conditions |
| 5. Controlled physical tests | Instrumented tests, risk controls, abort plan and independent review | Evidence only for the tested configuration and envelope |
| 6. Operational validation | Relevant authority approval, field trials, maintenance/training and monitored deployments | Deployment-specific evidence |

Do not call the robot “proven safe,” “field-ready,” or “15 m capable” until the relevant evidence exists. Passing software tests is necessary but insufficient.

## Current status

- Implemented in software gate: explicit emergency-stop, safety-monitor, battery and propulsion status checks; fail-closed handling for missing/malformed statuses.
- Tests added: missing interlock status, active emergency stop, unhealthy monitor, battery fault, propulsion fault, malformed status.
- Not implemented/verified by this change: physical emergency-stop circuit, watchdog connected to hardware, real battery or propulsion telemetry, waterproofing, buoyancy, braking/stop distance, sensor fusion, collision hardware, or field tests.
- Cost: standard-library Python and repository documentation only; no paid API, cloud GPU, new package or model download.

