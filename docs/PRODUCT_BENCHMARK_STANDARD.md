# Flood Rescue AI — Product Benchmark Standard

Company-wide benchmark rules: [PUI89 Product Quality and Benchmark Standard](https://github.com/Pui89/Pui89.github.io/blob/main/PRODUCT_QUALITY_AND_BENCHMARK_STANDARD.md).

## Relevant comparison set

Compare the same scenario and task: simulation-based reconnaissance, hazard mapping, or navigation support. Candidate groups include a no-autonomy/operator baseline, classical navigation/planning baselines, relevant open-source robotics stacks, and documented commercial systems only where evidence and conditions are comparable. Record each candidate's source, version, licence, sensors, hardware, simulation assumptions, and whether it was actually tested.

## Core metrics

- Mission/task completion rate across a predeclared scenario set.
- Path length and completion time, with identical start/goal and environment.
- Collision count, minimum obstacle clearance, recovery events and failed runs.
- Localization and hazard-map error against documented ground truth.
- Robustness to sensor dropout, localization drift, blocked routes and communication loss.
- Human interventions and time to detect/recover from failures.
- Compute load and end-to-end latency on named hardware.

## Fair protocol

Use versioned scenarios, repeated runs, fixed random seeds where supported, the same map/start/goal/obstacle configuration, and declared failure definitions. Report number of runs, distributions, failures and limitations. Simulated water, terrain, sensors and vehicle dynamics are assumptions, not field facts.

## Safety boundary

This is a research and rescue-support concept. Passing software tests or simulation does not establish flood navigation, amphibious mobility, evacuation capability, or physical rescue safety. Do not use the system for real emergency response without qualified partners, appropriate hardware and independent safety validation.

## Zero-spend constraint

Use simulation and existing hardware only. No paid cloud simulation, datasets, equipment, or services without explicit approval. If the needed scenario or sensor is unavailable for free, document the gap and defer the claim.
