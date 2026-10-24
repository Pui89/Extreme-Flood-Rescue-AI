# Extreme-Flood Mission Architecture — 0–15 m Scenario Target

## Purpose

Design a coordinated AI-assisted rescue system for extreme flood disasters, including scenarios whose simulated water-depth input reaches 15 m. The design target is to help responders search, assess hazards, communicate, deliver suitable supplies where feasible, and plan recovery. It is not a claim that the current repository or any existing prototype can physically operate at 15 m.

## Core principle: one mission coordinator, platform-specific limits

The system may coordinate several distinct platform classes. Each must have its own verified operating envelope and independent safety controls:

1. **Aerial reconnaissance (drone):** survey accessible airspace, map visible hazards, relay imagery, and mark possible people or animals for human review. Wind, rain, visibility, battery, airspace rules, and communication range can make a flight unsafe.
2. **Surface craft:** assess only when current, waves, debris, snagging, stability, payload, flotation, propulsion, communications, and recovery capability are within verified limits. A surface craft is not a deep-submergence vehicle.
3. **Ground / amphibious platform:** travel only where traction, slope, ground bearing, water depth/current, buoyancy, tilt, obstacle clearance, and retrieval capability are verified. It must not assume submerged streets are traversable.
4. **Submersible / underwater vehicle (future, separate design):** a 15 m underwater mission requires a pressure-rated and tested hull/enclosure, penetrators and seals, depth sensing, buoyancy and trim control, tether or validated communications, navigation suitable for low visibility, and a recovery plan. This is a different engineering platform, not a mode that can simply be enabled on an ordinary ground robot.
5. **Human response team:** remains responsible for operational decisions and rescue actions. The AI supports decisions; it must not represent uncertain detections as confirmed survivors or autonomously expose people to hazards.

## Mission stages

1. **Observe:** collect time-stamped imagery and sensor data; check sensor health, calibration, freshness, and consistency.
2. **Map and estimate:** estimate water surface/depth where data supports it, current and debris hazards where measurable, terrain/structure risks, and uncertainty. Mark unknowns explicitly.
3. **Select a suitable platform:** compare mission needs with the verified envelope of each available platform. Do not infer capability from the scenario's depth number alone.
4. **Plan a conservative task:** choose a route and task with a return/recovery path, communications plan, battery reserve, and human oversight. Prefer remote observation when physical access is uncertain.
5. **Gate before movement:** require healthy safety monitor, emergency-stop chain, fresh sensors, valid localization, communications, energy reserve, and all platform-specific limits to pass.
6. **Monitor continuously:** re-check hazards during operation. If any critical signal becomes missing, stale, implausible, conflicting, or outside its validated range, inhibit new motion and enter the platform's predefined safe state.
7. **Recover and review:** after a safety stop, require operator review and a documented recovery procedure; do not automatically resume into unknown conditions. Record the event for replay.

## Depth scenarios

Use 0–15 m as a scenario parameter for software tests, interface design, and hazard-response exercises. A depth value is not a rating of power, pressure resistance, buoyancy, waterproofing, stability, or rescue capacity.

- **0–shallow water:** still require checks for current, holes, drains, debris, contamination, slippery ground, and sensor reliability.
- **Increasing / uncertain depth:** use uncertainty-aware planning; do not extrapolate beyond measured and validated conditions.
- **Extreme-depth scenario up to 15 m:** default to remote/aerial reconnaissance and human-led platform selection. Underwater exploration is permitted only as a future submersible-specific task with documented pressure/depth certification, communication/navigation design, and recovery testing. Unknown limits mean no deployment.
- **Any depth with dangerous current, debris, unstable structures, failed communications, or no recovery path:** hold, retreat only if that retreat is itself verified safe, or request human intervention according to the platform's approved safety case.

## Software interfaces to implement and test

Keep software modular and platform-neutral at the mission layer:

- SensorHealth: source, timestamp, calibration/validity, status, and uncertainty.
- EnvironmentEstimate: estimated depth/current/obstacles/terrain plus confidence and unknown flags.
- PlatformEnvelope: platform type and evidence-backed limits; unknown limits fail closed.
- MissionRequest: goal, priority, people/animals as possible detections, time and energy constraints.
- SafetyGate: allow / limited operation / safe hold / operator review, with explicit reason codes.
- RecoveryPlan: last safe waypoint, communication fallback, recovery method, and operator contact.
- EventRecord: timestamp, inputs, limits used, decision, reason, and subsequent operator action.

Do not allow perception outputs to bypass the safety gate. Do not allow a visual demo, simulated sensor, or caller-supplied boolean to masquerade as a connected physical emergency-stop circuit or live hardware status.

## Minimum verification scenarios

Automate tests for:
- missing, stale, malformed, out-of-range, and mutually conflicting sensor readings;
- a 15 m scenario with no certified platform envelope (must hold);
- a suitable platform whose certified envelope excludes the requested conditions (must hold);
- current/debris/structure risk despite an otherwise acceptable depth;
- emergency stop, watchdog timeout, low reserve, propulsion fault, localization loss, and communications loss;
- route blocked or recovery path unavailable;
- uncertain person/animal detections and false positives;
- safe stop, operator acknowledgement, and no automatic restart;
- event-log completeness and deterministic replay.

Report simulation tests, software tests, hardware-in-the-loop tests, and field tests separately. Passing one category does not imply passing another.

## Physical validation still required

Before any real rescue claim, qualified engineers must define the actual platform and requirements, analyze hazards, test pressure/sealing/flotation/stability/propulsion/energy/communications/navigation under controlled conditions, verify independent emergency-stop and motor-inhibit behavior, validate detection performance, and conduct staged tests with a documented recovery plan. Human-carrying or direct person-rescue capability requires separate load, stability, entrapment, and rescue-system validation; it must not be inferred from supply delivery or simulation.

## Current status

**Design proposal only.** This document specifies an architecture and verification plan. It does not establish that all modules are implemented, that tests have passed, or that a robot is physically capable of a 15 m mission.
