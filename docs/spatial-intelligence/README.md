# Extreme Flood Rescue AI: Spatial Intelligence integration profile

This project now has a project-specific spatial integration profile at
`INTEGRATION_PROFILE.json`.

## Intended use
Advisory geometry for visible obstacles, structures and relative scene layout in flood scenarios.

## Planned tasks
- Visible obstacle and structure geometry
- Relative position of visible people/objects where lawful and appropriate
- Map-frame consistency checks for simulation fixtures

## Safety boundaries
- Water surface, current, submerged hazards, depth and buoyancy are not inferred by this module.
- No rescue performance or navigation safety is validated.
- Do not interpret missing point returns as free passage.

## Shared implementation dependency
The common software interfaces are being developed in the
[PUI89 Shared AI Core Spatial Intelligence PR #26](https://github.com/Pui89/PUI89-Shared-AI-Core/pull/26).
That pull request is still a draft and has not been merged. This file records
the project-specific integration contract; it does not mean the project
currently imports or executes the shared spatial module.

Before runtime integration, require lawful sensor/data provenance, calibrated
coordinate frames, synchronized timestamps, sensor-health checks, uncertainty
handling, synthetic fault tests and project-specific human-review gates.
No physical actuation is enabled.

**Current evidence status:** profile documentation added; runtime adapter,
real sensor integration, accuracy, field performance and safety validation
remain pending. No hardware or paid service is required for this documentation
stage.
