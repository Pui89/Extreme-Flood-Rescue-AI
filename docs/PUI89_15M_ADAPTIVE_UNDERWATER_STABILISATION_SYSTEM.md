# PUI89 15M Adaptive Underwater Stabilisation System (AUSS)

**Project:** PUI89 Extreme Flood Rescue AI  
**Status:** Proposed engineering concept / research target  
**Concept target:** up to 15 m telescopic reach  
**Validation status:** Not built, not simulated with validated fluid/structural physics, and not field-tested.

## 1. Concept summary

PUI89 proposes investigating a deployable underbody support system for an amphibious rescue platform. The user's concept is a set of long, retractable poles mounted beneath the vehicle, with a conceptual maximum extension of 15 metres. The intended research question is whether deployable supports, combined with vehicle-level hydrodynamic design and sensing, could improve stability in selected flood-rescue conditions.

The 15 m figure describes a **proposed maximum pole reach**, not a verified operating depth, safe anchoring depth, water-pressure rating, current-speed rating, or ability to withstand a dam-break surge.

The system must not be described as capable of holding a vehicle against every extreme flood. Dam-break flows can carry destructive momentum, debris and rapidly changing water levels; retreat, evacuation or non-deployment may be the only safe response.

## 2. Recommended system architecture

The concept should separate three functions rather than expecting a single pole shape to perform all of them:

1. **Telescopic support columns:** four conceptual support assemblies near the vehicle's underside corners. Their research purpose is to explore temporary stabilisation when the vehicle is stationary and suitable ground contact has been independently established.
2. **Ground-contact interface:** articulated, load-distributing feet are a candidate for suitable, surveyed ground only. A foot resting on soft sediment, an eroding riverbed, buried debris or an unknown surface is not a dependable anchor.
3. **Hydrodynamic protection:** the hull and underside should be assessed separately for drag, snagging and debris exposure. If flow-deflecting surfaces are explored, they should be a distinct, retractable hull feature—not treated as load-bearing support poles.

A fourth function is essential: **sensing and fail-safe supervision**. Deployment should be inhibited when ground contact, vehicle attitude, water/current conditions, structural load limits or communications status are unknown or outside an independently reviewed envelope.

## 3. Conceptual operating states

| State | Intended concept | Safety boundary |
|---|---|---|
| Stowed | All support elements secured in protected underbody housings | Required for normal travel and floating transit |
| Inspection | Sensors and operator assess ground, depth, current, vehicle attitude and hazards | Unknown or conflicting inputs mean no deployment |
| Controlled deployment | Supports extend only in a stationary, assessed environment | Simulation/research only until engineered and validated |
| Supported stationary work | Investigate whether supports can reduce movement during scanning or robotic-arm tasks | Never assume a support foot is anchored merely because it touches the bed |
| Abort / recovery | Stop deployment; retract or release only if the recovery path is safe | A trapped pole must not trigger an unsafe forced movement |
| Extreme-flow survival | Keep supports stowed; prioritise a safe retreat, shelter or evacuation plan | Do not attempt to anchor against an unqualified torrent |

## 4. Key engineering questions

The 15 m concept creates substantial structural and integration challenges. These must be answered by qualified mechanical, marine and structural engineers before dimensions, materials, actuator ratings or deployment speeds are selected.

- **Column strength:** combined bending, compression, buckling, torsion, fatigue and vibration across every telescopic stage.
- **Joints and locking:** load transfer, wear, corrosion, sealing, contamination and inspection of nested sections.
- **Vehicle stability:** centre of gravity, buoyancy, free-surface effects, support geometry and asymmetric loading.
- **Ground interaction:** bearing capacity, settlement, scour, pull-out, buried obstacles and uneven contact.
- **Hydrodynamic loading:** current velocity, exposed area, drag, turbulence, wave action and debris impact.
- **Snag and entrapment:** risk of poles catching cables, vegetation, vehicles, timber or rubble.
- **Power and recovery:** loss of electrical/hydraulic power, manual recovery, emergency release and safe failure position.
- **Human safety:** exclusion zones, remote supervision, rescue-team procedures and clear abort criteria.

Long slender columns can experience large lateral loads and instability. Extending them into fast-moving water may increase drag and overturning moments rather than improve stability. Therefore, the poles must never be assumed to resist dam-break flow simply because they are long or reach the riverbed.

## 5. Required sensing and fail-safe logic

Candidate inputs for a future research/simulation interface:

- Pole extension and lock-state feedback.
- Per-column load and strain estimates.
- Vehicle roll, pitch and acceleration.
- Water depth and current estimates, with timestamp and quality metadata.
- Ground-contact confidence and ground-condition classification.
- Obstacle/debris proximity.
- Power, actuator and communication health.

**Fail-closed rule:** missing, stale, contradictory, uncalibrated or out-of-envelope data must prevent a new deployment proposal and produce a simulated SAFE_HOLD / REVIEW_REQUIRED state. Software status is not a certified physical emergency stop.

No automatic deployment in live flood conditions is authorised by this concept document.

## 6. Simulation and verification roadmap

The first phase should use the existing standard-library PUI89 test infrastructure and clearly labelled synthetic inputs. It must not claim physical fidelity.

### Phase A — requirements and analytical review
- Define vehicle mass properties, buoyancy assumptions and support geometry as unknown parameters until measured or justified.
- Define the environmental variables and uncertainty ranges.
- Create a hazard analysis for deployment, support failure, snagging, loss of power and failed retraction.
- Obtain qualified review before choosing pole dimensions or structural ratings.

### Phase B — deterministic software scenarios
- Stowed-state checks and invalid-command rejection.
- Missing/stale current, depth, attitude and pole-position inputs.
- Conflicting load sensors and asymmetric support contact.
- Overload, extension-limit, lock-state and actuator-fault scenarios.
- Communication/power loss and emergency abort paths.
- Confirm conservative hold/review behaviour and complete failure reports.

### Phase C — physics-based simulation selection
Only after the requirements are reviewed, evaluate a suitable structural and fluid simulation approach. Record software version, solver assumptions, mesh/convergence evidence, boundary conditions, material data, uncertainty and independent review. A dry-terrain Gazebo scene or a rule-based Python test is not a substitute for validated computational fluid dynamics or structural analysis.

### Phase D — controlled prototype research
Physical testing would require qualified engineering oversight, a controlled test facility, load instrumentation, independent safety review and staged low-energy tests. No field deployment in floodwater should be inferred from a bench or tank test.

## 7. Metrics to report — only when measured

- Maximum tested extension and configuration.
- Measured column strain, deflection and load by stage.
- Vehicle roll/pitch and displacement under defined conditions.
- Ground settlement and support-foot slip.
- Current velocity, water depth and debris conditions.
- Deployment/retraction time and fault recovery outcome.
- Test repetitions, failures, uncertainty and instrumentation calibration.

Do not publish a current-speed rating, pressure rating, 15 m depth capability, survivability percentage or rescue-performance figure until the corresponding test or validated analysis exists.

## 8. Cost, data and autonomy boundaries

- No paid API, cloud GPU, hosted inference or subscription is required for the initial documentation and standard-library software checks.
- No model weights or large simulator packages are downloaded automatically.
- No personal or operational rescue data is uploaded by this concept.
- No physical actuator, vehicle, pole or rescue equipment is controlled by the software.
- All proposed actions remain simulation-only and subject to human review.

## 9. Public-facing description

**PUI89 15M Adaptive Underwater Stabilisation System (AUSS)** is a proposed research concept exploring four retractable underbody support columns with up to 15 m conceptual reach for an amphibious extreme-flood rescue platform. The concept investigates temporary stabilisation on suitable, assessed ground, coordinated with hydrodynamic hull design, environmental sensing and fail-safe supervision. The 15 m reach and all flood-resistance functions remain unvalidated research targets; the system is not claimed to anchor a vehicle against dam-break torrents or operate safely in every flood condition.

## 10. Immediate next gate

Before implementation beyond documentation and synthetic tests, define whether the 15 m requirement means total pole extension from the chassis or a target depth below the waterline, and specify whether the primary function is ground-contact support or non-contact flow stabilisation. These are different mechanical systems and should not be combined into one unverified claim.
