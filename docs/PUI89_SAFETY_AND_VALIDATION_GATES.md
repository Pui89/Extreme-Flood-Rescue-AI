# Safety and Validation Gates — Extreme Flood Rescue AI

This is an AI application and search-and-rescue robot concept. Simulated depth up to 15 m is a design target, not evidence of operating capability at that depth.

## Minimum evaluation gates
- Define each scenario's depth, current, visibility, obstacles, communication loss and sensor limitations.
- Test human/animal detection under stated conditions and record false positives, false negatives and uncertainty.
- Inject missing, stale, conflicting and implausible sensor values; test fail-safe behavior.
- Test navigation failure, blocked routes, loss of localization, communication loss and low battery.
- Record safe-stop success, collisions, route completion and detection performance by scenario, with seeds/configuration and software commit.
- Evaluate ground, boat and aerial platforms separately; do not transfer one platform's results to another.
- Do not describe simulation as field validation or promise rescue at every flood level. Deployment requires qualified rescue partners, risk assessment and relevant certification.

Action outputs remain proposals/simulation until separately authorized and safety-reviewed. No autonomous rescue or real-world validation is claimed.
