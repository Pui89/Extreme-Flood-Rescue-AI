# PUI89 Product Engineering Standard — Flood Rescue AI

**Product direction:** robotic disaster assessment and rescue-support coordination.  
**Status rule:** simulation and software tests do not establish real-world rescue capability.

## Product promise

Provide operators with a clearer, auditable picture of the environment and support safer mission planning across ground, surface-water, and aerial platforms. Preserve human oversight for consequential rescue decisions.

## Architecture boundaries

1. **Perception:** detect and track people, hazards, debris, water boundaries, and navigable regions using sensor-appropriate models.
2. **World state:** maintain timestamps, coordinate frames, uncertainty, sensor health, and provenance for every observation.
3. **Mission planner:** propose routes and task allocations with explicit risk and resource constraints.
4. **Fleet coordination:** account for communication delays, disconnected vehicles, conflicting observations, and lost platforms.
5. **Safety supervisor:** independently enforce safe-stop, geofence, speed, energy, communication-loss, and degraded-sensor policies.
6. **Human authority:** AI outputs are recommendations; they do not establish that a person is safe, deceased, or definitively identified.
7. **Evidence:** record scenario seed, simulator/version, model identifier, configuration, software commit, metrics, and failure traces.

## Required evaluation gates

- Establish baseline perception and navigation performance before adding larger reasoning or action models.
- Evaluate day/night, rain, fog, glare, reflections, debris, occlusion, sensor dropout, localization drift, and communication loss.
- Measure detection precision/recall, localization error where ground truth exists, route completion, time-to-safe-stop, false alarms, recovery rate, and mission-level failures.
- Inject faults systematically and verify safe behavior, including stale sensor data, conflicting sensors, malformed model outputs, low battery, blocked routes, and loss of command link.
- Use simulation for broad stress tests; clearly distinguish simulator results from field evidence.
- Do not treat generated video as physically grounded truth. Keep synthetic and simulated data labelled and separate from real-world test results.

## Release blockers

No autonomous field rescue claims without appropriate independent validation, hardware tests, operational risk assessment, and trained human supervision. Unknown or occluded people remain unknown; the system must not turn missing evidence into a confident conclusion.

## Model and license policy

Keep large weights out of Git history. Record model source/revision, checksum, license and commercial-use implications, compute requirements, and known limitations. Do not auto-download or train large models in routine CI. CI should run lightweight tests; expensive or hardware-specific evaluation must be explicitly triggered and cost-reviewed.

## Product-grade release evidence

Each release should include a reproducible scenario suite, benchmark report, safety/fault-injection results, dependency and license inventory, operator-facing limitations, installation instructions, and rollback steps.

## Current truthfulness rule

A concept, simulator demonstration, software regression test, hardware prototype, and field rescue trial are different evidence levels. Do not claim a rescue success, real-world reliability, or deployment readiness without direct evidence.
