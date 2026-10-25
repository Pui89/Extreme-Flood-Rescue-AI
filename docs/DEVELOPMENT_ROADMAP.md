# PUI89 development roadmap — free-first

This roadmap is an implementation plan, not evidence that every capability is already built. Keep work local-first and avoid paid APIs, subscriptions, cloud GPUs and large model downloads unless the owner explicitly approves the cost after reviewing the license, size and hardware requirements.

## Ordered development tasks

| Priority | Task | Cost target | Acceptance evidence |
|---|---|---|---|
| 1 | Improve autonomy-supervisor tests and common interfaces | Free | Unit tests cover healthy, unsafe, missing, invalid and non-finite inputs; shared interfaces have documented contracts; test command and result are recorded |
| 2 | Improve Coconut dataset quality and establish a vision baseline | Free, local | Source/license/credit manifest; file hashes and duplicate review; corrected annotations; leakage-safe source/tree/session split; baseline precision, recall and per-class results |
| 3 | Add perception uncertainty and task-planning tests to all three projects | Free, local | Tests cover low confidence, conflicting observations, missing inputs, invalid plans, unapproved actions and safe-hold outcomes |
| 4 | Add simulated navigation and multi-robot coordination for Flood Rescue | Free tools where feasible | Reproducible scenarios for ground/boat/drone roles; route and task metrics; communication-loss and localization-failure tests; simulation-only limits stated |
| 5 | Add multimodal provenance, calibration and human-review workflow | Free, local | Each observation records source/reference, modality, timestamp and model/version; calibration is evaluated on held-out data; inconclusive/conflicting cases route to human review |

## Project-specific implementation notes

### Coconut Harvest AI
- Keep this project's implementation scoped to: coconut image dataset and vision baseline.
- Reuse the model-agnostic VLM/action-plan data contracts where appropriate.
- Keep any language model advisory: it proposes structured steps but cannot bypass the autonomy supervisor or directly command hardware.
- Do not report a metric until it has been produced by a reproducible test and its dataset/split is documented.

### Extreme Flood Rescue AI
- Keep this project's implementation scoped to: free simulation, navigation and multi-robot coordination.
- Reuse the model-agnostic VLM/action-plan data contracts where appropriate.
- Keep any language model advisory: it proposes structured steps but cannot bypass the autonomy supervisor or directly command hardware.
- Do not report a metric until it has been produced by a reproducible test and its dataset/split is documented.

### Multimodal Narcotics Screening AI
- Keep this project's implementation scoped to: data provenance, calibration and human review.
- Reuse the model-agnostic VLM/action-plan data contracts where appropriate.
- Keep any language model advisory: it proposes structured steps but cannot bypass the autonomy supervisor or directly command hardware.
- Do not report a metric until it has been produced by a reproducible test and its dataset/split is documented.


## Current status rules

- **Scaffold present:** code or documentation exists, but has not necessarily been run locally.
- **Not verified:** no reproducible test result has been supplied yet.
- **Complete:** only after acceptance evidence exists and the command, environment and results are recorded.
- Do not claim a validated physical robot, real-world rescue capability, verified 0–30 m harvesting reach, or confirmed substance identification without suitable independent evidence.

## Suggested free local test commands

Run these from the repository root:

```bash
python -m unittest discover -s tests -p "test_autonomy_supervisor.py" -v
python -m unittest discover -s tests -p "test_llm_interfaces.py" -v
```

These commands are instructions, not a claim that the tests have already passed. Dataset/model evaluation may need additional project-specific commands. No model download is required for these interface tests.
