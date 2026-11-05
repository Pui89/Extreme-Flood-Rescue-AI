# PUI89 Total Resilience & Intelligence Standard

Applies to every current and future PUI89 project. Zero-cost/local-first by default; no paid services without explicit owner approval.

## THINK · DO · FIND
- THINK: identify hazards, score likelihood and impact, track uncertainty, compare safer options, recommend priorities.
- DO: run automated checks, enforce release gates, preserve evidence, and use safe-state behavior when safety conditions fail.
- FIND: discover vulnerabilities, failure modes, missing evidence, suitable free/open tools, relevant standards, and funding/research opportunities.

## Mandatory protection domains
Every project must maintain a risk register covering:
1. Cybersecurity: unauthorized access, credential exposure, malware, ransomware, malicious dependencies, prompt injection, data/model poisoning, unsafe commands.
2. Water/environment: rain, immersion, humidity, condensation, dust, mud, corrosion, temperature, vibration, impact, tampering.
3. Fire/heat/electrical: overheating, short circuit, overcurrent, overvoltage, reverse polarity, battery damage, power loss, thermal runaway.
4. Communications/positioning: network or signal loss, GPS denial, stale messages, sensor disconnection, interference, timestamp faults.
5. AI/data integrity: hallucinations, false predictions, bias, out-of-distribution inputs, uncertainty, calibration, missing/conflicting evidence, privacy, provenance.
6. Mechanical/operational safety: jams, overload, instability, collision, unintended motion, actuator limits, emergency stop, safe shutdown.
7. Human/mission/recovery: misuse, accidental activation, human review, mission abort, degraded operation, backups, incident response, recovery.

## Mandatory rules
- Every protection is NOT_VERIFIED until supported by suitable tests and recorded evidence.
- Software checks cannot establish physical water, fire, impact, or ingress resistance.
- IP67/IP68, flame ratings, temperature/load limits and safety claims are targets until the assembled equipment is appropriately tested.
- Never claim waterproof, fireproof, floodproof, hack-proof, or deployment-safe without evidence.
- AI must never override independent hardware safety interlocks. Emergency stops, motor limits, fuses/BMS and safe-state mechanisms require separate design and validation.
- Consequential screening/safety decisions must expose uncertainty and require qualified human review.
- Apply least privilege, input validation, secret protection, dependency/model-licence review, audit records, backup/restore and incident response.
- No paid service or hidden usage charge. Prefer existing free GitHub capabilities and standard-library checks.

## Automated gates
This repository's PUI89 workflow checks that the standard and machine-readable risk profile exist and declare all protection domains. Existing security workflows remain responsible for their existing scans; avoid duplication.

Before release, review tests/simulation evidence, unresolved high risks, safe failure behavior, hardware/environmental validation for physical claims, human approval/operating limits, and recovery/rollback readiness.

A passing policy workflow validates declarations only. It does not certify physical resistance, cybersecurity, AI accuracy, or deployment safety.

## Evidence record
For each material risk record: hazard, affected component, likelihood, impact, mitigation, test method, result, evidence location, date/version, reviewer, and status (NOT_TESTED, PASS, FAIL, or NOT_APPLICABLE with rationale).

## New-project inheritance
Every new PUI89 repository must copy this standard, add .github/pui89-resilience.json with project-specific hazards, and include .github/workflows/pui89-resilience.yml before its first release. Shared PUI89 AI Core should consume compatible risk/evidence reports across projects.
