# Frontier AI Technology and Free-First Upgrade Plan

## Goal
Build a credible simulation-first AI rescue research platform. Prioritize free/open-source software, reproducible tests and conservative safety behavior. Simulation results must not be presented as real-world rescue validation.

## Priority order

### P0 — Scenario and safety specification
- Define explicit scenarios for water depth, current, visibility, debris, communications loss, battery/power faults and uncertain human/animal detection.
- Treat the 0–6 m range and more extreme depths as simulated scenario parameters, not proof that a robot can operate or rescue at those depths.
- Define stop conditions, human oversight and failure recovery before autonomous behaviors.

### P1 — Deterministic safety and fault tests
- Test stale/lost sensor data, low battery, blocked path, lost communications, uncertain detection and invalid navigation goals.
- Ensure critical or unknown faults produce conservative stop/alert/manual-review recommendations.
- Software fault reports do not actuate a real emergency stop unless separately integrated and validated with hardware.

### P2 — Agentic mission-planning prototype
- Create a bounded workflow that proposes a mission plan, checks constraints, runs simulation scenarios and reports failures.
- Keep the planner separate from low-level robot control.
- Require human approval for consequential actions; never let a language model directly command physical actuators.
- Keep baseline checks runnable without a hosted model, API key or network access.

### P3 — Open robotics simulation
- Evaluate ROS 2 and Gazebo as the first simulation path.
- Add navigation, mapping and sensor simulation incrementally; record versions, setup instructions and limitations.
- Investigate heavier GPU-accelerated simulation only if hardware capacity, storage and license are suitable; do not assume the current laptop can run every simulator.

### P4 — Perception and evaluation
- Build a documented scenario set for people/animals, water, obstacles and visibility.
- Report detection quality, false negatives, latency and scenario coverage only after reproducible tests.
- Separate simulated perception results from field-test results.

## Acceptance criteria
- Scenario tests are repeatable and record configuration and outcomes.
- Critical fault cases have explicit expected behavior.
- No unverified claims of carrying people, operating at extreme depth, autonomous rescue or field readiness.
- README labels simulation-only, prototype, planned and physically validated capabilities accurately.

## Free-first tool policy
Prefer Python, pytest, ROS 2, Gazebo and compatible open-source tools. Keep initial checks lightweight and local. Check licenses, supported platforms and hardware requirements before adding dependencies. No paid API, cloud GPU or subscription without explicit approval.

## Current status
This document is a plan, not evidence that all listed stages are implemented or passed. Current simulation coverage, rescue performance and physical hardware capability remain unverified unless supported by recorded tests.
