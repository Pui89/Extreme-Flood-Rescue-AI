# Product Quality Roadmap — Flood Rescue AI

**Priority:** Equal top priority across all PUI89 projects.  
**Current evidence level:** software decision-support prototype; no validated real-world rescue capability.

## Release gates

1. **Scenario provenance:** version the lawful real or synthetic dataset, scenario generator, simulator version, configuration, random seed, and ground-truth source. Keep synthetic/simulation evidence distinct from field evidence.
2. **Perception and navigation baselines:** measure per-condition precision/recall, localization error where ground truth exists, route completion, route risk, and mission failures before claiming improvements.
3. **Fault injection:** test stale/conflicting sensors, localization drift, water-depth boundary values, blocked routes, low battery, lost communications, invalid model outputs, process crashes, and partial fleet failure.
4. **Fail-safe behavior:** unsafe or unknown state must trigger a verified safe stop/hold or operator escalation appropriate to the platform. Test time-to-safe-stop, manual override, recovery and audit trace.
5. **Human authority:** AI recommendations do not determine a person's identity, condition, or fate. No unsupervised hazardous rescue action without separately validated controls and operating approval.

## Milestones

- [ ] Maintain a versioned scenario and test-case inventory.
- [ ] Establish reproducible perception and navigation baselines.
- [ ] Add boundary and fault-injection tests for each safety-critical input.
- [ ] Run simulation stress tests across visibility, water, debris, sensor dropout and communications conditions.
- [ ] Publish metrics, failures, scenario seeds, environment, and reproducible commands.
- [ ] Document operator procedures, limitations, rollback, hardware-specific tests, and safety review.

## Resource policy

Keep default CI lightweight and free-first. Do not automatically download large models or launch expensive simulations in routine CI. Any optional cloud, hardware, dataset, or model expense must be reviewed before use.

## Honest status rule

Unit tests and simulation cannot establish waterproofing, physical reliability, victim detection in the field, or successful rescue. State exactly which software tests, simulations, and hardware trials have actually been completed.
