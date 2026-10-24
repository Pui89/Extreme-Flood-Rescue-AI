# Flood Rescue AI — Extreme-Flood Product Readiness

## Target
The simulator may explore flood-depth scenarios from **0–15 m**. This is a scenario parameter, not a physical robot rating. Water depth alone does not represent risk; current velocity, debris, waves, slope failure, access, communications and recovery must be modelled separately.

## Mission architecture
1. Drone/remote sensing performs initial reconnaissance when conditions permit.
2. Perception proposes people/animal locations and obstacles, with confidence and reviewable evidence.
3. Mapping records blocked routes, uncertainty and time/source of each observation.
4. A mission supervisor chooses among observe, request human review, safe hold, retreat or request a suitable craft.
5. A ground robot remains in safe hold at the demo's conservative depth boundary; the simulator must not imply safe operation in fast torrents.
6. Every mission log records scenario seed, depth, current, debris, sensor status, communication state, decision and reason.

## Test matrix
- Depth: 0–2 m, 2–6 m, 6–10 m, 10–15 m.
- Current: calm, moderate, strong and unknown (use documented numeric ranges once a hydrodynamic model is selected).
- Hazards: floating debris, boulders, submerged obstacles, bridge loss, sudden rise, poor visibility.
- System faults: camera loss, stale location, low battery, network loss, contradictory sensors, invalid depth estimate.
- Outcomes: safe hold, retreat, relay location, request human assistance; never assume entry is safe just because the simulated depth is below a threshold.

## Evaluation
Use scene/video-separated train and test splits. Report person/animal detection precision and recall, false alarms per scene, localization error when ground truth exists, route-planning success, safe-stop latency, communication-loss response and scenario completion. Report failures and confidence intervals where feasible; no fabricated results.

## Data source and licence register
Before use, record dataset name, exact source URL, licence/terms, attribution, task fit, data size, checksum, allowed commercial use, and split policy. FloodNet/LADI are candidates for aerial flood scene understanding; verify each source's current terms and whether its labels match the intended task. Water segmentation is not the same as detecting trapped people. Do not automatically download datasets.

## Release gates
- **Gate A — simulation:** deterministic scenario seeds and automated tests for all safe-hold/fault paths.
- **Gate B — perception:** licensed test set with scene-level separation and published metrics.
- **Gate C — integration:** fault injection for sensor, battery and communications failures; human override remains available.
- **Gate D — field:** expert-led, controlled trials and independent safety review before any physical rescue claim.

## Commercially credible first product
Start with human-reviewed flood mapping, aerial reconnaissance support and incident reporting—not an unvalidated robot advertised as rescuing people in 15 m water. No physical flood rating, rescue performance or life-saving claim is established by simulation alone.