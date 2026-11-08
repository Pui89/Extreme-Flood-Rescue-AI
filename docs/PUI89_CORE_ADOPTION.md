# PUI89 Shared AI Core — Extreme Flood Rescue AI Adapter

**Status:** Integration plan; documentation only.  
**Platform contract:** [PUI89 Evidence-to-Action Intelligence Platform](https://github.com/Pui89/Pui89.github.io/blob/main/docs/PUI89_EVIDENCE_TO_ACTION_PLATFORM.md)

## Purpose

Represent flood observations, changing environmental state, rescue proposals and failure conditions using shared PUI89 evidence contracts. This guide does not claim a physically validated rescue platform.

## Domain observations

Record water level/depth, current estimate, obstacles, weather/context, communication status, victim/animal reports and sensor health with units, source, timestamp, location reference, quality and uncertainty. Distinguish direct sensor readings, operator reports, map data, synthetic scenarios and model-derived estimates.

## World-state requirements

Maintain versioned snapshots with evidence links and freshness limits. Preserve contradictory readings. Mark inaccessible, stale or missing sensor values as unknown. Do not interpolate a safety-critical value without explicitly recording the method and uncertainty.

## Proposal and safety rules

- Route, approach, deployment and rescue recommendations are proposals for authorised human mission review.
- HOLD when current/depth/obstacle information is stale or conflicting, communication is degraded, victim location is uncertain, or operating limits cannot be verified.
- BLOCK operation outside the validated operating envelope.
- Simulated buoyancy, navigation, current resistance, reach or rescue success is not real-world validation.
- No propulsion, wheel, pole, winch, lift or deployment command may be issued by the shared core.
- Rescue operations require trained human command and emergency procedures.

## Evaluation gates

1. Validate shared observation, world-state, proposal and failure-report schemas.
2. Test missing/stale/conflicting water and current observations.
3. Test communication loss, sensor failure, map mismatch and recovery proposals.
4. Evaluate scenario coverage across urban, rural and other explicitly defined environments.
5. Report simulated results separately from field trials; identify simulator and scenario versions.
6. Verify that unknown critical conditions result in HOLD/BLOCK and human review.
7. Record false-safe cases as critical failures.

## Required report

Include scenario IDs, simulator/version, environmental assumptions, test command, repetitions, pass/fail counts, failure artifacts and reviewer. No claim of 15 m capability, flood-current resistance or rescue effectiveness without appropriate physical evidence.

## Implementation boundary

This document is an adoption plan. Runtime integration, field validation, buoyancy, navigation and physical safety are not established by adding this file.
