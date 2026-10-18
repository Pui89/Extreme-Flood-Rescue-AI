# Commercial and award-readiness roadmap — Flood Rescue AI

**Updated:** 18 October 2026  
**Stage:** human-supervised AI application and simulation-oriented workflow prototype; not a field-validated rescue robot.

## Product goal
Develop a local-first decision-support application and simulation-first reconnaissance-robot workflow to help trained responders review possible people, flood extent, debris, blocked access and uncertainty. A detection is not proof that someone is safe; a proposed route is not proof that it is safe.

## Evidence already recorded
- Python CI passed on Python 3.10, 3.11 and 3.12: https://github.com/Pui89/Flood-Rescue-AI/actions/runs/39096446071
- Dataset manifest/provenance, group-splitting and audit tools, deterministic workflow/safety tests, application/dashboard components and a benchmark protocol are present.

## Not yet proven
- Representative, licence-cleared data for each intended task.
- Independent held-out accuracy for person detection or flood-scene segmentation.
- Validated water-depth estimates, route safety, robust navigation, ROS 2/Nav2/Gazebo end-to-end performance or physical rescue.
- Operational approval, customer demand, certification or commercial effectiveness.

## Product ladder
1. **Decision-support demo:** replay permitted recorded or simulated scenes; display timestamps, uncertainty, data quality and human review.
2. **Benchmark package:** evaluate flood/water/road segmentation separately from person detection; document source, split, metrics and geographic limits.
3. **Simulation demo:** fixed-seed scenarios for water, debris, blocked routes, visibility loss, communication loss and safe stops.
4. **Research/responder partnership:** tabletop evaluation with authorized experts; no operational reliance on unvalidated predictions.
5. **Commercial/public-sector pilot:** only after legal/privacy review, independent safety evaluation, training and incident procedures.

## Immediate priorities
- [ ] Audit dataset licences, provenance, permitted use, class definitions, duplicates and label quality.
- [ ] Keep flood-scene segmentation separate from person detection; FloodNet scene labels alone do not establish a person-detection dataset.
- [ ] Define each task and metric before training; obtain lawful person-detection data if needed.
- [ ] Test missing, stale and conflicting sensors, uncertainty, communication loss and fail-closed decisions.
- [ ] Run fixed-seed scenarios; report failures, false negatives, latency and route failures.
- [ ] Evaluate a baseline only after data rights and splits pass audit.
- [ ] Integrate ROS 2/Nav2/Gazebo only where a reproducible integration and scenario can be maintained.

## Minimum acceptance gates
| Gate | Required evidence |
|---|---|
| Data | Sources, permissions, labels, group splits and audit |
| Perception | Separate held-out results for each task and class, including false negatives |
| Mapping | Ground-truth reference and mapping error |
| Resilience | Tested response to sensor faults, stale data and communication loss |
| Simulation | Repeatable scenarios, route outcomes and failure logs |
| Deployment | Operator procedures, privacy, maintenance and independent safety review |

## Commercial positioning
**Value proposition to test:** a low-cost, auditable research and training platform for flood-scene reconnaissance and human-reviewed hazard mapping.

Potential audiences include university robotics labs, emergency-management agencies, disaster-response NGOs and mapping/robotics integrators. These are prospects to interview, not confirmed partners.

Do not market this prototype as a rescue service or promise victim detection, safe navigation, lives saved or superiority without independent evidence and operational authorization. Pricing must account for deployment, ruggedization, communications, training, maintenance and liability.

## Award application evidence pack
- Defined problem and intended user.
- Demo with simulated/recorded scenes and visible uncertainty.
- Data rights, privacy and evaluation protocol.
- Baseline metrics, false-negative analysis and failure cases.
- Simulation fault-injection and safe-stop report.
- Risk register and human-in-the-loop operating model.
- Measurable milestones, budget and partner support only when obtained.

## Cost, safety and integrity
- Free/open-source-first and local-first; no paid APIs, cloud GPUs or subscriptions without explicit approval.
- Never treat a scene label or synthetic observation as a confirmed person detection.
- Do not rely on this prototype for live emergency dispatch or route authorization.
- Never claim rescue outcomes, certification, customers or comparative performance without evidence.
- This is a plan, not proof checklist items are complete. Record commit, environment, scenario, result and failures after each verified run.
