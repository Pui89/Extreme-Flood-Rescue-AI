# Flood Rescue AI — Failure and Security Response Matrix

## Purpose and status

This document records conservative failure-response requirements for design, simulation, and future verification. It is **not** proof that these responses are implemented in hardware or validated in the field. Follow applicable law, workplace procedures, and qualified safety/security guidance during any real deployment.

## Response matrix

| Failure or threat | Required safe response | Current evidence boundary |
|---|---|---|
| AI/perception service crashes or observations are invalid | Stop advancing based on uncertain perception; preserve last known state; request operator review. | Current simulation uses synthetic observations; live AI crash handling is not demonstrated. |
| Camera, thermal sensor, LiDAR, GNSS, IMU, or localization is lost/stale | Mark affected area unknown; stop or switch only to a separately validated fallback mode. | Design requirement; real sensors and localization are not validated. |
| Communication link or operator heartbeat is lost | Trigger safe stop in the simulation; physical system must use a tested, vehicle-specific stop/hold behavior. | Communication-loss safe stop is represented in the synthetic grid simulation only. |
| Battery, power, motor, water ingress, or overheating fault | Stop mission progression; report fault; use validated recovery/return procedure only if independently safe. | Simulation does not model vehicle power, water ingress, or physical dynamics. |
| Route is blocked, water depth/current is unknown, or localization disagrees | Do not mark unknown cells safe; replan only with verified inputs; hold if no safe route exists. | Grid path planning exists; flood physics and water-depth sensing are not demonstrated. |
| Possible-person observation is uncertain or model misses a person | Label as unverified; request human review; never claim a rescue or person confirmation from synthetic markers. | Synthetic possible-person markers only; no real detection metrics. |
| Malware, unauthorized command, or suspected remote compromise | Isolate compromised links; reject unauthenticated commands; preserve logs; require trusted recovery and operator authorization. | Response policy only; no security certification or penetration testing. |
| Theft, collision, projectile damage, fire, or other physical attack/damage | Stop mission; do not approach or retaliate; prioritize human safety and notify responsible responders through available safe channels. | Physical protection, threat sensing, and emergency procedures are not implemented or validated. |
| Reboot, clock skew, corrupt mission log, or inconsistent state | Do not resume automatically; verify logs and localization, then require authorized operator confirmation. | Recovery-state validation remains a requirement. |

## Common principles

1. **Fail closed:** missing, stale, contradictory, or invalid inputs must not be interpreted as proof of safety or as a positive/negative classification.
2. **Human oversight:** uncertain or high-impact decisions require authorized human review.
3. **Separate safety controls:** software checks are not substitutes for independent, appropriately engineered emergency stops, brakes, interlocks, and safe power isolation.
4. **Security incidents:** do not retaliate or execute untrusted instructions. Isolate affected systems where safe, preserve logs and hashes, use trusted recovery media/backups, and follow the organization's incident process.
5. **Evidence:** each test record should include scenario ID, software version/commit, environment, input, expected response, actual response, pass/fail, and reviewer.
6. **No invented validation:** mark items as `REQUIREMENT`, `SIMULATED`, `TESTED`, or `FIELD-VALIDATED` only when the evidence supports that status.

## Verification plan

- Convert each applicable row into a repeatable unit or simulation test.
- Test normal, boundary, malformed-input, failure-injection, recovery, and repeated-run behavior.
- Require safe-stop and recovery tests to pass before considering hardware integration.
- Do not describe the project as physically safe, certified, or operational based only on software tests.

