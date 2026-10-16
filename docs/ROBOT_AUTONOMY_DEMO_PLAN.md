# Flood Rescue AI — Robot Demonstration Plan

> **Status:** Proposed simulation/prototype plan. This is not proof of a physically built, amphibious, or field-validated rescue robot. Do not deploy an unvalidated robot in floodwater or a live emergency.

## Mission: reconnaissance before human entry

The robot is intended to perform bounded, hazardous-area reconnaissance so responders can make better-informed decisions before entering an area. Initial development should be simulation-first and use recorded or synthetic scenarios.

## Concept platform

- Rugged tracked or wheeled ground robot for dry ground and shallow, controlled test environments.
- RGB camera; optional thermal camera for night-time search experiments.
- Depth sensor or LiDAR for local mapping and obstacle detection.
- Water-contact, tilt, battery, and communications-health monitoring as appropriate to the prototype.
- On-device computer running the local AI application.
- Remote operator interface, physical emergency stop, and a fail-safe stop state.

An amphibious platform is a separate, substantially harder design and is **not assumed** by this plan.

## Demonstration workflow

1. **Receive mission boundary:** operator sets a simulated or controlled test area.
2. **Explore:** robot follows a bounded route and stops when localization or obstacle sensing is unreliable.
3. **Observe:** capture timestamped images and sensor readings.
4. **Detect and map:** flag possible people, water-covered paths, debris, blocked access, and other visible hazards only where supported by evaluated models.
5. **Represent uncertainty:** mark occluded areas and missing data as unknown; never report 'no person present' just because a detector did not find someone.
6. **Plan candidate route:** use the map and explicit obstacle constraints to suggest a route; a separate safety layer checks motion commands.
7. **Escalate:** send evidence, coordinates (when valid), sensor health, and candidate route to a trained rescue coordinator.
8. **Human confirmation:** rescue personnel decide whether and how to act.
9. **Verify:** record a rescue status only when confirmed by a responder or reliable follow-up evidence.

## What it can do instead of a person — in a bounded task

| Hazardous or repetitive task | Robot contribution | Human remains responsible for |
|---|---|---|
| First look into an unsafe street or building approach | Remote reconnaissance from a safe launch point | Deciding whether entry is safe and authorized |
| Repeatedly surveying an area | Repeatable image and sensor collection | Interpreting uncertain evidence |
| Marking visible debris and blocked routes | Draft a hazard map with timestamps | Confirming map accuracy and route suitability |
| Searching camera views for possible people | Flag candidate detections for review | Confirming a person is present and coordinating rescue |
| Reporting observations | Send a structured situation report | Dispatch, rescue, medical care, and incident command |

## Free, local-first milestones

- **M0 — Recorded-data replay:** run the AI application against sample images; label all sample/synthetic inputs.
- **M1 — 2D simulation:** simulate a robot, obstacles, flood zones, possible-person detections, and a map. Demonstrate safe stopping and route replanning.
- **M2 — Scenario evaluation:** measure person-detection recall, false alarms, map error, route completion, stop latency, and behavior during sensor/communications loss.
- **M3 — Controlled robot test:** use a physical platform only on dry, level, private test ground with an emergency stop and an observer.
- **M4 — Supervised pilot:** proceed only with rescue-agency approval, independent safety testing, suitable environmental protection, and trained operators.

## Safety requirements

- No autonomous entry into fast-flowing water, electrically hazardous areas, unstable structures, or unknown-depth water.
- Loss of communications, low battery, sensor conflict, or localization failure must trigger a defined safe state.
- A camera detection is a lead, not confirmation that a person has been found or rescued.
- The robot must not obstruct emergency vehicles or responders.
- Do not make operational claims from a simulation, concept image, or untested model.

## Demo acceptance criteria

- The robot avoids known obstacles in simulation and stops when a safety condition is triggered.
- A simulated communications failure results in stop/return behavior defined by the scenario.
- Candidate people and hazards include timestamps and uncertainty.
- Unknown or unobserved areas remain explicitly unknown.
- Results are reproducible and distinguish synthetic, recorded, and live data.

## Current vs proposed

**Current:** this repository describes a flood-rescue AI application and a human-supervised workflow. Existing application capabilities should be verified by running the code and tests.

**Proposed:** autonomous mobility, live camera/thermal/LiDAR integration, real-time mapping, route execution, and field rescue operations remain engineering and validation work unless separately demonstrated with evidence.
