# PUI89 Shared Technology Standard
Version: 1.0
Review date: 2026-11-06
Applies to: every current and future PUI89 project and the shared PUI89 AI Core.

## 1. Mission

Use high-quality, current, evidence-backed AI and engineering resources while preserving strict zero-cost development, non-Chinese provenance, security, privacy, safety, maintainability, and reproducibility.

This document is an adoption gate and research catalogue. Listing a resource does not mean it has been installed, downloaded, enabled, benchmarked, or approved for production.

## 2. Mandatory adoption gate

Before any tool, model, dataset, API, package, action, service, simulator, or hardware design is adopted, record:

- Exact project, resource name, version/revision, official source, publisher and country/origin evidence.
- Exact licence for code, model weights, tokenizer, training data, datasets, and redistribution; do not assume they share one licence.
- Total cost, usage limits, rate limits, storage, bandwidth, compute, egress, trial expiry, auto-renewal, billing triggers, and whether a payment method is required.
- Data sent to the provider, retention, telemetry, privacy, security posture, and account permissions.
- Hardware, RAM/VRAM, disk, OS, runtime, and energy requirements.
- Known vulnerabilities, maintenance status, provenance, checksums/signatures where available, and dependency chain.
- Reproducible evaluation results, limitations, failure modes, and human-oversight requirements.

Decision states:
- APPROVED: all gates verified, compatible, free for the intended use, non-Chinese origin, and evidence recorded.
- TRIAL-ONLY: isolated, synthetic-data, non-production evaluation with explicit limits.
- UNVERIFIED — DO NOT USE: any unresolved origin, licence, cost, data, security, or hardware question.
- REJECTED: violates PUI89 policy or has unacceptable risk.

No resource may be adopted merely because a website calls it "free", "open", "open source", or "open weights".

## 3. Strict zero-cost and non-Chinese policy

Prohibited without exception:
- Paid APIs, subscriptions, cloud GPUs/compute, metered services, paid datasets, paid licences, paid storage, or paid support.
- Free trials that convert to paid plans, automatic upgrades, unexpected or retrospective billing, and services requiring a payment card where avoidable.
- Chinese-origin models, model providers, tools, platforms, datasets, infrastructure, or services.
- Resources with unclear origin, ownership, licence, pricing, or data handling.
- Unreviewed model downloads, dependency installation, large downloads, or new third-party GitHub Actions.

If any billing or origin detail is unclear, stop at UNVERIFIED — DO NOT USE. Prefer local, offline, small-footprint, standard-library-first work. Do not add a dependency merely to use a fashionable tool.

## 4. Current non-Chinese AI research candidates (not yet approved for deployment)

| Candidate | Verified public facts | PUI89 disposition |
|---|---|---|
| Google DeepMind Gemma 4 | Open weights; Apache-2.0; multimodal family with E2B/E4B edge variants and larger models. Official model card and release information are linked below. | PRIORITY RESEARCH CANDIDATE. Evaluate E2B/E4B only after checking exact quantized file size, runtime, RAM/VRAM and licence files. Do not download on constrained hardware without a measured fit. |
| Meta Muse Glimmer | Meta describes a 30B open-weight agentic model under Apache-2.0, intended for local agent workflows. | RESEARCH ONLY. 30B is not a practical assumption for low-memory hardware; do not download or use cloud hosting. |
| Reflection Beam | Reflection describes open weights under Apache-2.0 for coding, reasoning and long-horizon agentic workloads. | RESEARCH ONLY until model size, exact weight licence, runtime needs, origin and reproducible benchmarks are checked. |
| OpenVLA 7B | MIT-licensed vision-language-action research model from a team including Stanford, UC Berkeley, Google DeepMind and Toyota Research Institute. Model card states limits for unseen robot embodiments. | SIMULATION-ONLY RESEARCH. No physical actuation. Check dataset/component licences and hardware before any use. |
| Physical Intelligence OpenPI / pi-family | Open robotics VLA research code and checkpoints are published by Physical Intelligence; requirements and checkpoint terms vary. | UNVERIFIED PER CHECKPOINT until exact weights, code, data licences and hardware are checked. Research in simulation only. |

Official references:
- Gemma 4 release: https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- Gemma 4 model card: https://gemma.ai/models/gemma-4/model-card/
- Gemma 4 technical/model overview: https://ai.google.dev/gemma/docs/core
- Muse Glimmer: https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model
- Reflection Beam: https://reflection.ai/blog/beam-is-available
- OpenVLA model card: https://huggingface.co/openvla/openvla-7b
- OpenVLA source: https://github.com/openvla/openvla
- OpenPI source: https://github.com/Physical-Intelligence/openpi

Open weights are not the same as a free hosted API. Model weights may be large, and code, weights, data and derivative licences may differ. No model is approved for operational decisions until PUI89 has tested it against task-specific benchmarks and safety cases.

## 5. Free/open engineering and security candidates

Evaluate these official projects first; do not install them automatically:
- OSV-Scanner: local dependency vulnerability and licence checks; official documentation https://google.github.io/osv-scanner/
- Gitleaks: open-source secret scanner; source https://github.com/gitleaks/gitleaks
- OpenSSF Scorecard: checks repository security practices; https://scorecard.dev/ and https://github.com/ossf/scorecard
- GitHub native Dependabot and supply-chain features: verify current plan/visibility limits before enabling; https://github.com/security/advanced-security/software-supply-chain
- OWASP Dependency-Check / Dependency-Track: open-source dependency risk tools; verify deployment and maintenance requirements; https://owasp.org/www-project-dependency-check/ and https://owasp.org/www-project-dependency-track/

Security automation must use pinned, reviewed action versions or locally verified binaries; least-privilege workflow permissions; no untrusted pull-request secrets; no automatic write permissions; and no paid scanner tier. Check action publisher, source, licence, release integrity and transitive dependencies before enabling.

## 6. Robotics, simulation and digital-twin candidates

- ROS 2 and Gazebo: prefer simulation-first development and documented interfaces; verify the supported ROS/Gazebo distribution and licences before integration.
- NVIDIA Isaac Lab: framework is published under BSD-3-Clause; GPU requirements and the Isaac Sim/Omniverse terms must be checked separately. Official source: https://developer.nvidia.com/isaac/lab
- NVIDIA Isaac Sim: NVIDIA describes it as free/open source under Apache-2.0 while also documenting additional software/materials terms and separate paid redistribution/cloud costs. Do not use cloud services or redistribution features that can incur charges. Official source: https://developer.nvidia.com/isaac/sim

Do not install heavy simulators on constrained machines. Keep robot, car and motorcycle control interfaces in mock/simulation mode. No direct hardware actuation, road deployment, rescue deployment, or safety-critical control from an unvalidated AI model.

## 7. Shared PUI89 AI Core requirements

All projects should reuse one consistent, versioned contract design rather than creating incompatible duplicates:
- WorldState: timestamp, source, coordinate/frame context, observed facts, uncertainty and freshness.
- Observation: sensor/source identity, payload reference, calibration, quality, provenance and missing-data flags.
- ActionProposal: proposed action, preconditions, risk, confidence, expiry and required approvals; proposal is not an execution command.
- FailureReport: failure class, severity, evidence, affected component, containment and recovery state.

Cross-cutting capabilities:
- Evidence Integrity and provenance.
- Uncertainty propagation and calibration.
- Conflicting/missing/noisy evidence handling.
- Human review and explicit approval for consequential actions.
- Safety gates, emergency stop, safe-state behavior and fail-closed defaults.
- Benchmark registry, reproducible tests, regression tests and machine-readable reports.
- Change, deterioration and predictive-maintenance tracking.
- Cybersecurity, secrets protection, dependency provenance, backup and recovery.
- Clear status labels: implemented, tested, passed, failed, proposed, blocked, unverified.

## 8. Project-specific application map

| PUI89 project | Priority applications |
|---|---|
| Coconut Harvest AI | Multimodal perception; maturity classification; uncertainty-aware detection; arm/gripper simulation; worker/animal safety; orchard/environment robustness; predictive maintenance. |
| Flood Rescue AI | Multisensor world-state; terrain/water/current simulation; resilient navigation; communications-loss handling; flotation/stability and rescue-safety modelling; human-authorized proposals only. |
| Multimodal Narcotics Screening AI | RGB and approved sensor evidence fusion; provenance and calibration; uncertainty and human review; false-positive/false-negative benchmarks; privacy and audit trail; no autonomous enforcement. |
| Homeguard AI Nomad | Sensor fusion for heat, water, humidity, smoke, electrical and structural signals; anomaly/change detection; explainable alerts; offline-first operation; privacy and false-alarm controls. |
| PUI89 AI Robot Car | Perception, world-state tracking, agent planning, simulation, predictive maintenance, cybersecurity and driver/human override; no road deployment from unvalidated AI. |
| PUI89 AI Robot Motorcycle | Rider-centric perception, stability and hazard modelling, simulation-only control proposals, fault detection, battery/electrical protection and human override; no road deployment from unvalidated AI. |

## 9. Evidence and release gates

A feature is not complete because a document describes it. For each capability record:
1. Source code or configuration path.
2. Test/benchmark name and version.
3. Test command and environment.
4. Expected and actual result.
5. Evidence artifact or log reference.
6. Known limitations and unresolved risks.
7. Reviewer and date.

Release gates: resource provenance/licence/cost review; security review; unit and integration tests; negative/fault-injection tests; simulation evaluation; performance and resource-budget checks; human safety review; and documented rollback/recovery.

## 10. Adoption workflow

1. Discover candidates from official non-Chinese sources.
2. Verify origin, code/weights/data licences, cost and privacy independently.
3. Check hardware fit before downloads or installation.
4. Compare against a simple PUI89 baseline using fixed datasets and benchmarks.
5. Record findings and limitations.
6. Propose a small isolated change; do not silently add dependencies or services.
7. Run tests and review security implications.
8. Approve per project only when evidence supports the decision.
9. Recheck versions, licences, pricing and vulnerabilities before upgrades.

Last reviewed: 2026-11-06. Re-verify all external facts before adoption; pricing, licences, model availability and hardware requirements can change.
