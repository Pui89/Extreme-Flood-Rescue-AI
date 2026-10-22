# System Fault and Hardware Safety Playbook

**Status: design guidance only.** This playbook does not certify a boat, ground robot, drone, or rescue system. Water operations, lifting, propulsion, batteries, and aircraft require hardware-specific risk assessment and qualified review.

## Safety priority

Protect rescuers and the public first. When the vehicle's safe state is uncertain, suspend the mission, notify the operator, and use the recovery plan. Do not make a dangerous situation worse in an attempt to complete a rescue.

## Fault response matrix

| Fault or situation | Required response to design and test |
|---|---|
| AI model crash, invalid detection, or uncertain person alert | Stop AI-dependent mission decisions; show uncertainty and require human review. Never treat an unverified detection as a confirmed victim. |
| Camera, thermal, depth, LiDAR, sonar, IMU, GPS, or encoder failure | Mark affected sensing unavailable; stop motion if safe navigation cannot be confirmed. |
| Localization drift, map mismatch, blocked route, or unknown water depth/current | Do not enter the uncertain route; hold/retreat only using a verified safe procedure, otherwise request recovery. |
| Remote link or operator heartbeat lost | Execute the vehicle-specific loss-of-link behaviour; do not continue hazardous navigation. A drone, boat, and ground robot need different safe responses. |
| Low battery, voltage sag, overheating, or power fault | Abort mission and return/land/shore only if the verified route and reserve permit; otherwise signal recovery. |
| Main computer or control process freezes | Independent watchdog and hardware safety mechanisms should disable hazardous propulsion/manipulation or enter a pre-engineered safe state. Validate per platform. |
| Propeller, wheel, track, winch, arm, or steering jam; collision; entrapment; capsize/tip | Disable rescue manipulation and use the platform-specific stop/hold response; alert operator and follow a recovery procedure. |
| Water ingress, damaged insulation, short circuit, smoke, swelling battery, or unusual heat | Keep people clear; isolate energy only if safe and designed for it; do not touch wet or exposed electrical equipment. Request qualified recovery. |
| Emergency stop, guard/interlock, or safety-monitor fault | Keep hazardous functions inhibited until inspected and intentionally reset; reset must not automatically restart motion. |
| Wind, waves, current, lightning, poor visibility, unstable bank, or unsafe depth | Abort or constrain the mission according to pre-defined operating limits; never improvise beyond validated limits. |
| Storage, calibration, configuration, map, or logging failure | Block autonomous mission start if the missing item is safety-critical; alert operator and fall back to manual recovery. |
| Unknown fault or update | Suspend autonomous rescue and re-test affected functions before field use. |

## Hardware and electrical design checklist

- Define a safe state separately for ground vehicle, boat, and drone. “Cut all power” is not universally safe: propulsion loss, a falling load, or an uncontrolled aircraft may create additional hazards.
- Provide suitable physical emergency-stop/manual override and independent actuator/propulsion controls, designed for the specific platform and reviewed by qualified specialists.
- Select battery management, fusing, wiring, connectors, isolation, grounding, enclosure and ingress protection, thermal management, and corrosion protection for the actual electrical design.
- Prevent unexpected restart after power recovery, communication recovery, or watchdog reset.
- Guard propellers, wheels/tracks, winches, arms, and pinch points; define safe handling, lockout/isolation, lifting, towing, and retrieval procedures.
- Test loss of link, water ingress detection, sensor failures, low battery, watchdog action, and emergency stop in simulation and controlled non-hazardous tests before field deployment.
- Never test near flood victims or rescuers until the platform has passed documented, supervised safety validation.

## Recovery and verification

For each fault, record detection, safe response, operator alert, recovery method, reset authority, test conditions, expected and actual results, and evidence. Test combined faults as well as single failures. Label untested cases **NOT TESTED**. No generic software can guarantee safety for every possible hardware or environmental situation.

## Current project boundary

This repository's software checks and simulation plans do not prove physical rescue capability, waterproofing, electrical safety, or platform-specific fail-safe operation. A qualified robotics, electrical, marine, or aviation safety review is required for the relevant hardware before field use.
