# PUI89 Shared Engineering Standard — Flood Rescue AI

**Purpose:** make development repeatable, low-cost, reviewable, and evidence-led. This document records a working standard; it does not claim new tests or simulation results have been run.

## Operating rules

1. **Free-first:** prefer open-source tools and GitHub Actions within available free quotas. Do not add paid APIs, hosted GPUs, subscriptions, or services that can incur charges without explicit approval.
2. **Inspect before changing:** reuse existing agents, safety guards, simulation demos, validation matrices, and tests instead of creating duplicates.
3. **Small, reviewable changes:** isolate changes, add regression tests, and use a pull request when practical.
4. **Evidence over claims:** distinguish software tests, synthetic scenarios, simulation results, and physical field trials. They are not interchangeable.
5. **Reproducibility:** record scenario/configuration, software version, random seed where applicable, test conditions, outputs, failures, and command used.

## Project-specific priority: repeatable simulation evidence

1. Define a small versioned set of scenarios for varying water depth, visibility/rain, obstacle density, communications loss, localization failure, and safe-hold behavior.
2. Clearly label synthetic people/animals and simulated sensor outputs. They are not real detections.
3. Test each subsystem separately: perception input handling, route planning, localization status, hazard checks, operator alerts, and fail-safe transitions.
4. Measure success rate, route completion, collision/clearance violations, stop/hold response, false alerts where ground truth exists, and runtime. State sample counts and test conditions.
5. Test adverse cases and failures, not only successful demonstrations.
6. Keep simulation evidence separate from real-world claims; do not claim waterproofing, safe flood operation, victim detection, or rescue capability without appropriate validation.

## Shared quality gates

- Run the existing lightweight unit tests and CI workflow.
- Keep operator authority and manual recovery explicit for hazardous actions.
- A fail-safe requirement in documentation is not proof of a functioning hardware safety mechanism.
- Avoid unnecessary model downloads or cloud compute before the evaluation design is stable.
- Record failures and limitations alongside successful results.

## Definition of done

A change is complete only when its code/docs are reviewed, relevant automated checks have actually run, the result is reported accurately, and any remaining limitation is explicit. If a check has not run, mark it **not verified**.

## Immediate next action

Use the existing validation matrix to choose a small, repeatable simulation test suite. Run and record the exact cases before expanding the simulation or adding more concept imagery.
