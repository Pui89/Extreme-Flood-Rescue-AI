# AI Agent Review and Support Plan

## Purpose
Provide repeatable, low-cost review for the Flood Rescue AI prototype and simulation work. The agent produces evidence-backed findings and recommendations; it does not autonomously navigate a real rescue robot or direct people into hazardous water.

## Automated review stages
1. **Repository health:** run tests, check required configuration and report failures with links.
2. **Input validation:** check missing, stale, out-of-range, or inconsistent sensor values; validate units and timestamps.
3. **Scenario testing:** test low visibility, localization loss, uncertain person detections, blocked routes, rising water, communication loss, and emergency stop.
4. **Simulation reproducibility:** record simulator/version, world, robot configuration, seed, scenario parameters, and command for every run.
5. **Metrics:** when simulations produce structured logs, report detection precision/recall, false alarms, route completion, time, minimum clearance, and failure counts as applicable. State denominators and scenario coverage.
6. **Human escalation:** uncertain or conflicting evidence must produce an alert or abstention, not a confident rescue instruction.

## Evidence labels
- **PASS:** a defined automated check ran and passed.
- **FAIL:** a defined check ran and failed.
- **NOT RUN:** simulator, model, scenario, or logs were unavailable.
- **HUMAN REVIEW REQUIRED:** result needs qualified interpretation.
- Distinguish simulated results from real-world results in every report.

## Suggested report
A dated Markdown report should contain commit SHA, tests, simulator and scenario details, inputs, outputs, failures, metric definitions, evidence links, and limitations. Do not fabricate performance figures.

## Cost and permissions
Prefer free/open-source simulation and existing GitHub Actions. No paid API, external upload, or new cloud service is required. Use least-privilege workflow permissions; do not let the agent deploy code to robot hardware.

## First priorities
- Add unit tests for invalid/stale sensor readings and unsafe route states.
- Create a small, documented simulation scenario matrix with expected safe outcomes.
- Save machine-readable scenario logs and generate a benchmark report.
- Make emergency-stop and human-review paths explicit in the logic.

## Limitations
Simulation and unit tests do not prove safe performance in real floods. No unvalidated model should be used as the sole basis for rescue decisions.