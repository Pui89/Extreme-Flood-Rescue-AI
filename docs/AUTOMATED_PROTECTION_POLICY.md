# Document automated protection policy for flood rescue

## Automated protection and fail-safe policy

This is the project's safety contract for software and future hardware integration. It is **not proof of a physically safe rescue robot**.

### Required automated checks
- Reject missing, malformed, stale, or implausible readings; unknown terrain, unknown water conditions, and conflicting sensors must not be treated as safe.
- Check platform-specific limits for water depth, current, slope, tilt, payload, battery reserve, obstacle clearance, localization confidence, and communications before movement.
- On emergency stop, watchdog timeout, sensor timeout, loss of localization/comms, battery or propulsion fault, unstable ground, or limit violation, inhibit new motion and enter the configured safe state.
- Treat ground robot, boat, and drone as different platforms with separate operating envelopes. A 0–15 m scenario slider is simulation-only and must never be interpreted as a physical rating.
- Require operator review before resuming after a safety stop; do not automatically restart movement into unknown water or a blocked route.
- Log the hazard trigger, supplied readings, selected safe state, and recovery decision for replay and review.

### Rescue-specific boundaries
- A person/animal detection is an uncertain perception result, not proof of identity, condition, or safe access.
- Route planning must account for submerged obstacles, current, debris, unstable structures/banks, and escape/recovery options; depth alone is insufficient.
- Do not send a platform into a scenario beyond its evidence-backed operating envelope. Simulation success is not evidence of field rescue capability.
- Physical safeguards still required: independent emergency stop where applicable, watchdog and motor inhibit, sealed electronics validated for the intended conditions, buoyancy/stability testing for water platforms, and controlled hardware-in-the-loop/field testing.

### Release gate
Tests must include missing and stale data, sensor disagreement, emergency stop, communications loss, low battery, propulsion fault, blocked route, and recovery behavior. Record results; keep physical capability and safety status **not validated** until documented evidence supports the specific platform and conditions.
