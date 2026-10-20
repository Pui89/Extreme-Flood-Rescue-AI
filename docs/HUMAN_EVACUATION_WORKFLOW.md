# Human Evacuation Workflow — Flood Rescue AI

**Status:** design specification / simulation-first plan. This document does not claim a validated rescue capability or authorize real-world deployment.

## Mission

Coordinate three complementary platforms to locate people in flooded homes, assess observable urgency conservatively, provide information to trained rescuers, and support a human-led evacuation. The system must not autonomously decide that a person is medically safe, physically capable of walking, or safe to carry.

## Platform roles

### 1. Ground robot — indoor reconnaissance only within verified limits
- Inspect accessible, structurally cleared, dry or shallow-water routes only when the robot's ingress protection, traction, stability, current tolerance, and recovery method have been verified.
- Use RGB/depth camera and/or lidar for mapping, obstacle detection, and route visibility. Thermal imaging and audio are optional sensors, not proof of life or diagnosis.
- Identify possible people and report a location with confidence and sensor timestamp.
- Do not push debris, open doors against resistance, climb stairs, enter unstable structures, or approach moving water unless specifically engineered and validated.
- If water depth, current, floor condition, localization, communications, or structure safety is unknown: stop, mark the route UNKNOWN, and request human review.

### 2. Drone — external overview and location relay
- Search exterior, roof, upper windows, and accessible open areas where flight is legal and weather permits.
- Relay approximate person locations, blocked entrances, roof access, and visible hazards to the operator.
- Do not attempt to lift, carry, or physically extract a person. Do not fly into confined interiors or power lines.
- Treat thermal detections as candidate observations only; verify with another view or a human operator when possible.

### 3. Rescue boat — water-side access and evacuation support
- Approach only within the boat's rated operating conditions, load, stability, current, and crew training.
- A trained rescue team controls boarding, flotation devices, patient handling, and extraction. A small robot boat must not be assumed capable of carrying a person.
- Ground robot and drone may guide the team but must not command a boat into an unverified route.
- If conditions exceed the boat/crew's verified envelope, hold position and escalate to specialist water rescue.

## End-to-end workflow

1. **Receive incident:** operator records address/area, time, known hazards, and available communications. Never assume a building is structurally safe.
2. **Establish command:** human incident commander assigns drone, ground robot, and rescue boat roles. Define geofences, communications channel, stop command, and recovery plan.
3. **Drone survey:** create an exterior overview; mark possible people, entrances, wires, debris, current, and roof access. Every observation carries timestamp, confidence, and sensor source.
4. **Build shared map:** combine observations only when coordinates and timestamps are valid. Keep uncertain locations explicitly uncertain; do not merge conflicting detections as fact.
5. **Ground-robot route check:** attempt indoor reconnaissance only after an operator authorizes entry and all platform limits are met. Map free, blocked, unknown, and hazardous areas separately.
6. **Person candidate detection:** AI outputs POSSIBLE_PERSON, confidence, image/map location, and evidence source. It must not output a medical diagnosis. Low confidence, occlusion, or sensor disagreement becomes HUMAN_REVIEW.
7. **Conservative assistance assessment:** report observable cues only, e.g. visible movement, response to a voice prompt, apparent entrapment, or person not visible. A lack of movement is not proof of unconsciousness; thermal/audio data alone do not determine condition.
8. **Human triage:** trained rescuers decide urgency and method. If there may be immediate danger, notify the incident commander promptly; do not wait for a model confidence threshold.
9. **Select extraction plan:** 
   - Person appears able to follow instructions: rescuer gives instructions; robot may provide light, location, and a route suggestion.
   - Person's mobility/condition is unknown: treat as needing human assessment; dispatch trained rescuers and suitable flotation/medical support.
   - Person cannot move, is trapped, or is in water: trained rescue personnel choose appropriate specialist equipment and extraction technique. No improvised robotic lifting.
10. **Evacuate and confirm:** trained team moves the person to a designated safe zone and confirms handoff. AI logs only the operational status, not an unverified claim that the person is medically safe.
11. **Debrief:** preserve logs, sensor failures, route decisions, near misses, false detections, and outcomes for review.

## Required state machine

Use explicit states and log every transition:

- SEARCHING: collecting observations; no person confirmed.
- POSSIBLE_PERSON: model candidate; human verification required.
- HUMAN_REVIEW: uncertain, conflicting, occluded, stale, or out-of-distribution input.
- LOCATION_REPORTED: candidate location sent to operator with timestamp and confidence.
- ROUTE_CHECK: evaluating map, water, current, obstacles, localization, communications, and platform limits.
- ROUTE_BLOCKED: hazard or limit violation; no autonomous entry.
- RESCUER_REQUIRED: extraction or assessment requires trained people.
- EVACUATION_IN_PROGRESS: human team has accepted responsibility; robot provides approved support only.
- SAFE_HANDOFF_REPORTED: operator confirms transfer to the designated team/zone; this is not a medical clearance.
- STOPPED: emergency stop, loss of localization/communications, invalid sensor data, or safety interlock.

Any safety-critical unknown must fail safe: stop movement, preserve last known location, notify the operator if communications remain available, and wait for human review. Emergency-stop behavior must be independent of the AI perception model.

## Water-depth scenarios (1 m through 6 m)

Depth is not inferred reliably from a single ordinary RGB image. Use measured depth sensors, surveyed water levels, terrain/elevation data, or other validated sources where available. Attach uncertainty and source/time to every depth estimate.

For each 1 m, 2 m, 3 m, 4 m, 5 m, and 6 m scenario:
- The default ground-robot decision is **NO ENTRY / UNKNOWN** unless that exact robot is engineered and tested for the condition.
- A boat or underwater platform may be considered only within its own documented design and operating envelope.
- Test current speed, hidden drop-offs, debris, submerged obstacles, sensor visibility, communications loss, and recovery failure separately; depth alone is not a sufficient safety variable.
- Never describe simulated success as real-world water-rescue capability.

## Free/open-source simulation and software plan

Prefer local software and public datasets; no paid APIs, hosted inference, cloud GPUs, or paid data services are required by this plan.

- **ROS 2 + Gazebo Sim:** robot, sensors, indoor/outdoor scene, and controlled fault scenarios.
- **Nav2:** ground-robot mapping/navigation baseline, with blocked/unknown areas excluded from safe routes.
- **OpenCV / PyTorch:** local perception experiments and reproducible evaluation.
- **RViz:** operator visualization of map, candidate locations, confidence, timestamps, and route status.
- **Public flood imagery:** use FloodNet for aerial flood-scene understanding and water/road/building labels. It does not supply exact 1–6 m depth ground truth. Record each dataset's licence, provenance, split, and intended task before use.

Open-source software does not guarantee zero hardware, electricity, storage, or internet costs. Keep all computation local to avoid cloud charges; review licence obligations before redistribution.

## Simulation test matrix

Run scenarios with repeatable seeds and logs:
- day/night, rain, glare, reflections, turbidity, occlusion, and camera failure;
- water depth from 1 m to 6 m as labelled environmental scenarios, plus unknown depth;
- slow/fast current, debris, hidden steps/drop-offs, blocked doors, stairs, and unstable-looking structures;
- false person detections, missed detections, multiple people, partial visibility, and thermal/audio disagreement;
- stale timestamps, invalid transforms, localization drift, GPS loss, low battery, network loss, and robot immobilization;
- boat overload/unsafe approach as a simulated **reject/stop** case;
- operator stop request at every workflow stage.

Report per-task precision/recall, person-localization error, false alarms, time-to-alert, route-blocking success, unsafe-entry attempts, stop response, communication-loss behavior, and recovery success. Report denominators and test conditions. Do not combine simulation and field metrics.

## Go/no-go gates

1. Dataset licence/provenance and leakage-safe splits reviewed.
2. Unit tests pass for state transitions, stale data, uncertainty, and fail-safe stop.
3. Simulation scenarios and results reproducible.
4. Human-factors review confirms that alerts are understandable and uncertainty is visible.
5. Hardware-specific environmental, electrical, structural, flotation, and communications tests completed by qualified people before any real deployment.
6. A qualified rescue organization approves operational procedures and training.

**Current limitation:** this document is a design plan. It does not prove that the repository currently implements all these components, that a model detects people reliably, or that any robot can enter floodwater or extract a person.