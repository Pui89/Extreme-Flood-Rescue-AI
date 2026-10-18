# Product brief — Flood Rescue AI

**One-line description:** A local-first, human-supervised AI decision-support prototype and simulation-first reconnaissance-robot research workflow for flood-scene evidence and hazard mapping.

## The problem
Flood response is complicated by changing water, debris, visibility, access and communication conditions. Responders need timely evidence with uncertainty visible; a model's output must not be treated as confirmation that a person is present, absent or safe.

## What the project provides today
- Application/dashboard and human-review workflow components.
- Dataset provenance, manifest, group-split and audit tools.
- Deterministic software-level workflow and safety tests.
- A documented benchmark direction for perception and simulation.

## What is not yet a product claim
Independent person-detection or flood-segmentation performance, validated water-depth estimates, safe autonomous navigation, end-to-end field robotics and real rescue outcomes have not been established. The prototype must not be used to dispatch responders or authorize live routes.

## Potential first customers and collaborators
University robotics labs, emergency-management researchers, disaster-response organizations and mapping/robotics integrators. These are audiences to interview, not confirmed customers.

## Why evaluate it
The research direction emphasizes auditable evidence, explicit uncertainty, fault handling and human review. Flood-scene segmentation and person detection are distinct tasks and must be evaluated separately.

## Demonstration plan
1. Replay recorded or simulated scenes with source and timestamp shown.
2. Demonstrate data-quality checks and uncertainty handling.
3. Report separate segmentation/person-detection results only after lawful data and held-out evaluation are available.
4. Run repeatable simulation scenarios with sensor and communication faults.
5. Review workflow requirements with qualified emergency-management experts.

## Evidence required before a pilot
- Lawful data sources and documented annotation quality.
- Separate held-out metrics and false-negative analysis for each task.
- Repeatable scenario tests, safe-stop and communications-failure results.
- Privacy, operational risk and human-factors review.
- Formal authorization and agreed acceptance criteria.

## 30 / 60 / 90-day targets
- **30 days:** finalize task definitions, data permissions and manifest audit.
- **60 days:** produce baseline results or document the blocking data gaps; run fixed-seed fault scenarios.
- **90 days:** review results with qualified research/responder stakeholders and define a controlled study. Dates are targets, not promises of completion.

## Short award pitch
Flood Rescue AI investigates how auditable AI and embodied reconnaissance could help responders interpret flood-scene evidence without hiding uncertainty. The project prioritizes task-specific benchmarks, fault-aware workflows and simulation-first evaluation before any real-world deployment. The next phase will establish evidence and requirements with qualified partners.
