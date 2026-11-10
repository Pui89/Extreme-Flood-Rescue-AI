# Extreme Flood Rescue AI — Perception Accuracy Upgrade v0.1

**Status:** Requirements specified; no new model, sensor integration or rescue capability is validated.

Shared contract: [PUI89 Perception and Accuracy Standard](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/main/docs/perception/PUI89_PERCEPTION_AND_ACCURACY_STANDARD_V0.1.md).

## Priority perception tasks

1. Detect and segment people, animals, boats, vehicles, buildings, floating debris and rescue equipment.
2. Distinguish a person/animal from floating debris; preserve ambiguous classes as unknown and request human review.
3. Track rescue targets across video frames with timestamps, identity continuity, last-seen position and visibility state.
4. Segment water, road, shoreline, building and visible waterline boundaries.
5. Estimate water depth only from calibrated depth/level sensors or a validated measurement method. RGB colour, wheel height or a single photograph is not a depth measurement.
6. Estimate current direction/speed only from repeated observations and suitable measurement evidence; distinguish observed drift from inferred current.
7. Detect submerged hazards only with appropriate sensors such as sonar or validated depth sensing; camera non-detection does not mean underwater clearance.
8. Map landing/approach zones, overhead hazards, power lines and unstable debris where visible.
9. Monitor sensor obstruction, water ingress indicators, timestamp drift and degraded communications.

## Difficult-condition matrix

Night, rain, glare, reflections, muddy water, waves, motion blur, partial submersion, occlusion by debris, crowded scenes, low camera angle, aerial viewpoint, intermittent communication and missing sensor streams.

## Evaluation

Report per-class detection/segmentation metrics, rescue-target tracking continuity, waterline localization error, measured depth error against independent references, false-negative hazard rate and sensor-degradation detection. Separate aerial, shore, surface and underwater sensor domains. Group splits by incident/location/recording session to avoid leakage.

## Water World State

Maintain observed water boundary, measured depth with method/time, estimated flow with uncertainty, obstacle map, target last-seen position, sensor-health state and explicit unknown regions. Expire stale observations; never present old water depth as current.

**Safety boundary:** a detected person is not a confirmed rescue assessment; no navigation, propulsion, lifting or rescue action is authorized by perception alone. Human-supervised operation and validated physical limits remain required.
