# Amphibious Rescue-Raft Robot Concept

**Status:** concept specification for software architecture and future simulation. This document does not describe a built, tested, certified or operational rescue vessel.

## 1. Mission concept

A low-profile, raft- or rescue-boat-shaped amphibious robotic platform intended to support responders during floods. The platform is designed around two distinct mobility configurations:

- **Land mode:** retractable wheels are deployed beneath the hull for controlled movement on suitable, load-bearing ground.
- **Floating mode:** the wheels fold or retract into protected recesses beneath the hull, while buoyancy and a dedicated marine propulsion system provide movement in water.

The transition is conditional on verified platform state and operator authorization. It must not be triggered by a single water-depth reading.

## 2. Physical layout

- **Hull:** buoyant, compartmentalized, load-bearing raft/boat hull with protected wheel bays.
- **Retractable wheels:** four or more protected wheels, with mechanical locks and position feedback. The design must prevent accidental deployment, retraction or snagging.
- **Water propulsion:** guarded electric thrusters or waterjets may be evaluated. Final selection requires thrust, efficiency, debris-ingestion, guarding, maintenance and emergency-stop analysis.
- **Steering:** differential thrust or a separately validated rudder/steering arrangement, with manual override.
- **Rescue deck:** low, non-slip deck, perimeter handholds, controlled boarding point and responder-accessible tie-downs.
- **People:** provision for assisted boarding and secure seating/restraint positions. No passenger capacity is specified until stability and load tests justify it.
- **Animals:** a separate washable, ventilated and restrained compartment, with layout reviewed for animal welfare and responder access.
- **Supplies:** secured, separated storage for first-aid equipment, drinking water, flotation aids and communications gear. Payload mass and distribution must be monitored.

## 3. Operating modes

| Mode | Configuration | Intended context | Mandatory hold conditions |
|---|---|---|---|
| Land travel | Wheels deployed; marine propulsion inhibited unless separately designed for use | Firm, surveyed ground and suitable access routes | Soft/unstable ground, excessive slope, wheel fault, unknown traction or unsafe load |
| Transition to water | Controlled wheel retraction and hull/propulsion checks | Only at an assessed launch/transition area | Conflicting sensors, wheel-lock fault, water ingress, unstable load, low battery or no operator approval |
| Floating navigation | Wheels fully retracted and locked; marine propulsion enabled | Water conditions within the craft's validated envelope | Current/wave/debris limits exceeded, propulsion fault, loss of communications, low reserve buoyancy or uncertain state |
| Recovery / emergency | Safe hold, stop or recovery procedure selected by trained operator | Fault, lost link, unsafe environment or mission abort | No autonomous continuation through an unknown hazard |

The platform must verify wheel position, mechanical lock state, hull condition, propulsion readiness, battery reserve, payload distribution and operator authorization before changing modes.

## 4. Strong-current research and simulation

The project will study fast-flowing water as a **bounded research and simulation problem**, not assume the craft can withstand arbitrary currents.

Simulation parameters should include:

- Current speed, direction and spatial variation.
- Water depth, waves and changing water level.
- Floating debris, submerged obstacles and snag hazards.
- Visibility, rain and sensor degradation.
- Hull mass, displacement, payload position and centre of gravity.
- Propulsion thrust, steering authority, battery reserve and communications quality.
- Launch/recovery access, safe zones, abort conditions and human operator decisions.

Candidate measurements for future simulator and controlled test work:

- Position/heading tracking error and route completion.
- Cross-track drift and ability to hold or regain a safe route.
- Propulsion saturation and remaining control authority.
- Collision, snag and near-miss events.
- Safe-hold/abort response under sensor, communications or propulsion faults.
- Stability indicators, freeboard and payload-shift response where a validated physics model is available.

Do not publish current-speed, wave-height, payload, passenger, animal-weight, speed, endurance or depth ratings without reproducible evidence for the actual hull and configuration.

## 5. AI and control architecture

Proposed information flow:

`RGB / thermal / depth / IMU / GNSS / water-level / current / wheel-state / propulsion telemetry`
→ sensor-health, timestamp and uncertainty checks
→ terrain/water classification and hazard map
→ world-state estimate
→ platform-envelope and payload checks
→ proposed land / transition / float mode
→ independent deterministic safety gate
→ human authorization
→ low-level vehicle controller
→ telemetry, event and failure report.

AI may assist with scene understanding, possible person/animal detection, hazard mapping and route recommendations. It must not bypass the independent safety gate, emergency stop, mechanical interlocks or human authorization.

Missing, stale, malformed or conflicting sensor observations must lead to a safe hold or human review. A simulation-ready result is not permission to actuate physical hardware.

## 6. Validation gates

1. **Requirements and calculations:** define intended operating envelope; calculate displacement, reserve buoyancy, freeboard, centre of gravity and stability for empty, nominal and asymmetric payloads.
2. **Mechanism bench tests:** test wheel deployment/retraction, locks, position sensing, ingress protection, snag protection and failure recovery without people or animals aboard.
3. **Propulsion bench tests:** test guarded propulsion, steering, thermal limits, emergency stop, manual override and lost-link behavior on a controlled test stand.
4. **Unmanned still-water tests:** use ballast, tethering, an exclusion zone and qualified supervision. Measure leakage, trim, freeboard, roll/pitch, turning, stopping and recovery.
5. **Controlled current tests:** proceed only after independent review, with qualified marine/rescue supervision, a separate safety craft, defined abort criteria and recovery arrangements.
6. **Payload and rescue trials:** define people/animal/supply limits only after stability calculations and staged supervised trials; comply with applicable regulations and rescue-agency requirements.

## 7. Explicit capability boundaries

- The wider project's **0–15 m flood range is a scenario-design/simulation target**. It is not a 15 m submergence rating or a claim that this surface craft can operate in 15 m water.
- Strong-current operation is a research objective. No current-speed rating or fast-current capability is established.
- The raft/boat hull, retractable wheels, flotation, propulsion, passenger/animal layout and rescue functions remain conceptual until built and separately validated.
- No passenger capacity, animal capacity, payload mass, speed or endurance is claimed.
- Software tests and synthetic simulations do not prove buoyancy, stability, water resistance, navigation, rescue performance or physical safety.

**Design principle:** a safe hold, abort or human-review decision is preferable to continuing when the water, craft state or operating envelope is uncertain.
