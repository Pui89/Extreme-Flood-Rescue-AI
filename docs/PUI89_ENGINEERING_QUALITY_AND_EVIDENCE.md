# PUI89 Engineering Quality and Evidence System — Extreme Flood Rescue AI

**Reviewed:** 25 October 2026  
**Purpose:** a lightweight, free-first release gate shared across PUI89 projects. This is a process standard, not a claim of validated rescue capability.

## Non-negotiable evidence rules

1. **No evidence, no claim.** Use *verified*, *failed*, *not measured*, or *blocked* with a named artifact, test, scenario, and date.
2. **Separate software, simulation, model, and physical evidence.** Passing CI or a synthetic scenario does not establish field rescue performance or physical safety.
3. **Reproducibility before performance claims.** Record code revision, environment, command, scenario configuration, trial count, metrics, failures, and report path.
4. **No fabricated numbers.** Label synthetic fixtures and simulated water-depth scenarios explicitly.
5. **Free-first.** Prefer local tools and standard-library checks. Do not require paid APIs, hosted GPUs, subscriptions, or model downloads for basic checks. Warn before resource-heavy downloads.
6. **Safe, reversible workflow.** Work on a branch and open a reviewable pull request. Do not auto-merge or silently modify the default branch.
7. **Human oversight.** Uncertain or unsafe conditions should trigger hold, replan, or operator review; software policy alone does not stop physical hardware.

## Project release gates

| Gate | Required evidence | Current status |
|---|---|---|
| Scenario reproducibility | Versioned scenario config, fixed seeds where applicable, repeatable run command and retained output | **Partially established; expand scenario coverage** |
| Water and environment envelope | Explicitly simulated depth, current, debris, visibility and terrain assumptions | **0–15 m is simulation-only; not a physical operating envelope** |
| Sensor degradation | Missing, stale, contradictory and low-quality observations tested | **Must be demonstrated per path** |
| Communications and platform faults | Lost link, stale telemetry, power/fault flags and recovery/hold behavior | **Expand repeatable regression coverage** |
| Safety decision workflow | Unsafe/unknown states block unsafe proposals; operator approval and audit record are testable | Software behavior must be verified by named tests; no hardware claim |
| Rescue effectiveness | Representative labelled scenarios, false alarms/misses, latency, route/safety outcomes and repeated trials | **Not measured as real-world rescue effectiveness** |
| Physical capability | Instrumented trials, platform-specific operating envelope, independent safety review | **Not validated** |

## Standard evidence record

For each meaningful test or experiment, record:

- **ID / requirement:** stable identifier and expected behavior.
- **Revision and environment:** commit SHA, OS, dependencies, hardware if relevant.
- **Command and inputs:** exact command, scenario version, seed, simulated depth/conditions and sensor-fault settings.
- **Result:** pass/fail/blocked/not measured; actual counts and metrics only when observed.
- **Failures and uncertainty:** missed detections, false alarms, unsafe proposals, holds, timeouts and recovery outcomes.
- **Artifact:** durable report path or CI run URL.
- **Limitations and next action:** what the result does not establish.

## Operating loop

1. Select one requirement from [the validation matrix](VALIDATION_MATRIX.md) and [reproducible benchmark plan](REPRODUCIBLE_BENCHMARKS.md).
2. Make the smallest safe change on a dedicated branch.
3. Run the narrow scenario test first; then the repository regression suite when feasible.
4. Inspect logs and generated reports; a successful process exit alone is not proof that expected behavior occurred.
5. Update the matrix with observed evidence and limitations.
6. Open a pull request with scope, commands run, results, and unrun checks; review before merging.

## Immediate priority

Add repeatable scenario tests for rising water, debris, sensor loss/staleness, communications loss, and safe-hold/recovery. State clearly which parts are synthetic simulation. The 0–15 m design target must not be presented as a validated depth rating.

## Completion criteria

This system is operational only when a reviewer can trace **requirement → implementation → test → observed result → artifact → limitation**. This document does not certify operational safety, field performance, or physical rescue capability.
