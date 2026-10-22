# Step-by-Step Testing Guide

This guide helps run repeatable software and simulation checks using free tools already in the repository.

## 1. Check the current commit
- Open the repository's **Actions** tab.
- Open the latest run for the commit being reviewed.
- Record the commit SHA and status. A queued or in-progress run is not a pass.

## 2. Run software checks
From a local clone, open a terminal at the repository root and use the test command documented in the repository workflow. If the Python test workflow uses pytest and dependencies are installed:
```powershell
python -m pytest
```
Save full errors and fix the first underlying failure before rerunning. Passing unit tests validates only the tested logic.

## 3. Test sensor and input failures
Check missing, stale, out-of-range and conflicting sensor values; confirm units and timestamps are validated. Expected result: the system reports uncertainty or abstains rather than silently treating invalid data as safe.

## 4. Test scenarios
Build or run documented scenarios for low visibility, localization loss, uncertain person detections, blocked routes, rising water, communication loss and emergency stop. For each scenario, record inputs, expected outcome, actual outcome and log location.

## 5. Evaluate simulation results
Record simulator/version, world, robot configuration, scenario parameters, random seed and exact command. Report only metrics supported by structured logs, with definitions, sample counts and failure counts. Clearly label every result as simulated.

## 6. Test safe escalation
Missing localization, unsafe water depth, blocked routes, communication failure or emergency-stop activation must not result in an autonomous real-world rescue command. Keep human oversight explicit.

## 7. Record the result
Create a dated report with commit SHA, commands, scenario matrix, pass/fail/not-run status, evidence links and limitations. Never describe simulation tests as proof of real-flood readiness.
