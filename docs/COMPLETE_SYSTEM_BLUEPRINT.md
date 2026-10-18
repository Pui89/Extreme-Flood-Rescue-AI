# Complete System Blueprint — Flood Rescue AI

**Scope:** human-supervised search-and-rescue decision support and simulation-first mobile robot. This is a system blueprint, not a claim of field-ready rescue capability.

## System architecture

```text
RGB / thermal / depth / LiDAR / water-level / map inputs
  -> timestamp, sensor-health and quality checks
  -> separate perception tasks: person detection, flood segmentation, obstacle detection
  -> coordinate transform and uncertainty-aware hazard map
  -> traversability / route proposal
  -> mission-risk gate and human coordinator review
  -> simulation navigation adapter (ROS 2 / Gazebo / Nav2, when installed)
  -> STOP / retreat / request-help states
  -> event log and reproducible evaluation report
```

## Component contracts

1. **Input validation:** record timestamp, sensor source, coordinate frame and calibration. Reject stale or malformed observations.
2. **Person detection:** use a separately trained/evaluated person detector. FloodNet is useful for post-flood scene understanding/segmentation but does not supply a person-detection guarantee. Dataset labels and intended use must match the task.
3. **Flood/hazard segmentation:** distinguish floodwater, roads, buildings, debris and other available classes. Do not infer water depth from RGB alone unless a separately validated method and supporting measurements exist.
4. **Mapping:** transform observations into a map only when calibration/pose are valid. Mark unknown space as unknown rather than safe.
5. **Planning:** propose routes only through verified traversable areas; add configurable clearance, water-depth, slope and communications constraints where actual sensors support them.
6. **Safety supervisor:** default to STOP or request human review on unknown terrain, sensor conflict, loss of communications, stale pose, low confidence or emergency stop. No autonomous entry into hazardous water is authorized by this software blueprint.
7. **Audit:** record source IDs, model versions, route rationale, uncertainty, human decision and outcome. A lost signal must never be logged as a successful rescue.

## Free-first development profile

- Start with recorded data and simulation; do not require paid APIs, cloud GPUs or paid notebooks.
- ROS 2 Jazzy + Gazebo Harmonic is an official documented combination for a compatible Ubuntu 24.04 setup. Nav2's guide covers transforms, robot description, odometry, sensors, mapping/localization, footprint and navigation plugins: https://docs.nav2.org/jazzy/configuration_and_development/first_time_robot_setup_guide/gazebo/
- FloodNet official source describes a 2,343-image aerial post-flood dataset with scene-understanding labels and a permissive Community Data License Agreement; preserve its documented split and cite the paper: https://github.com/BinaLab/FloodNet-Supervised_v1.0
- Keep raw data and weights outside Git unless redistribution rights are verified.

## Acceptance gates

- [ ] Separate data specifications and evaluation protocols for person detection, flood segmentation and obstacle detection.
- [ ] Dataset source, licence, attribution, label basis, duplicate group and split are auditable.
- [ ] Test data is held out by scene/video/location where possible; report class-level precision/recall, false negatives, latency and failure examples.
- [ ] Map tests cover invalid coordinate transforms, missing pose, unknown cells and stale sensor timestamps.
- [ ] Simulation scenarios cover blocked routes, fast-changing water hazards, obstacle encounters, battery/communication loss, sensor dropouts, STOP and recovery.
- [ ] No robot enters real floodwater based solely on model output; field trials require rescue-authority approval, trained supervision and independent safety review.

## Current boundary

The existing repository has software-level safety and audit checks plus dataset preparation tools. This blueprint does not prove real-world person-detection accuracy, flood-depth estimation, autonomous navigation or a completed rescue. Every acceptance gate must be labelled **PASS**, **FAIL**, or **NOT RUN** with a reproducible evidence link.