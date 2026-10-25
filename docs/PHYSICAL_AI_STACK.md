# Physical AI stack — Extreme Flood Rescue AI

## Planned architecture

1. **Vision-language model (VLM):** summarize recorded/simulated scenes and propose candidate people, animals, obstacles or uncertainties for review. It is not a certified life-safety detector.
2. **Task/action LLM:** turn an approved search objective into a structured high-level plan, such as inspect a simulated sector or request a human review.
3. **World state:** represent known/unknown water depth, current hazards, obstacle map, robot status, communication state and time-stamped detections.
4. **Navigation and multi-agent planner:** assign simulated search sectors to ground, surface and aerial platforms; avoid assuming every platform is safe at every water depth.
5. **Failure recovery:** explicitly test lost communications, localization failure, sensor disagreement, blocked routes and low-confidence detections.
6. **Autonomy supervisor:** retain the existing supervisor as an independent gate. The LLM cannot bypass it.
7. **Evidence and evaluation:** report simulation conditions, route success, detection recall, false alarms, recovery outcomes and failure cases.

## Safe starter action vocabulary

Use high-level allowlisted actions such as `inspect_sector`, `update_hazard_map`, `request_human_review`, `replan_route`, and `hold_position`. These are plan labels only, not commands to real motors, boats or drones.

## Current implementation status

- `pui89_autonomy/llm_interfaces.py` provides dependency-free data contracts and validators for vision findings and action plans.
- It does **not** load or run a VLM/LLM, connect to an API, operate a simulator, or control a rescue vehicle.
- Flood depths including 6 m or 15 m are design/simulation scenarios, not proven real-world operating limits.
- Rescue decisions require trained human oversight and independent hardware safety systems.

## Next steps

1. Build reproducible simulated scenarios and baseline perception/navigation metrics.
2. Test plans for unknown depth, current, obstacles, lost localization and communications loss.
3. Add a local model adapter only after checking model license, hardware fit, download size and reproducible evaluation.
4. Keep real vehicle actions disabled until independent engineering safety validation.
