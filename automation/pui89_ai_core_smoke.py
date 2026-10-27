"""PUI89 shared AI-core smoke checks; standard-library only.

This is an interface/safety prototype, not a perception model or robot controller.
Run: python automation/pui89_ai_core_smoke.py --report reports/pui89-ai-core-smoke.json
"""
from __future__ import annotations

import argparse
import json
import math
import time
import unittest
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Observation:
    source: str
    value: Any
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class WorldState:
    observations: dict[str, Observation] = field(default_factory=dict)
    uncertainty_flags: list[str] = field(default_factory=list)

    def update(self, key: str, observation: Observation) -> None:
        if not key.strip():
            raise ValueError("state key must not be empty")
        if not math.isfinite(observation.confidence) or not 0.0 <= observation.confidence <= 1.0:
            raise ValueError("confidence must be finite and between 0 and 1")
        self.observations[key] = observation
        if observation.confidence < 0.5:
            flag = f"low_confidence:{key}"
            if flag not in self.uncertainty_flags:
                self.uncertainty_flags.append(flag)


@dataclass
class ActionProposal:
    action: str
    confidence: float
    requires_human_approval: bool = False
    simulated_only: bool = True


def authorize_action(proposal: ActionProposal, *, state_known: bool, approval: bool = False) -> tuple[bool, str]:
    """Fail closed; this function never executes an action."""
    if not proposal.action.strip():
        return False, "empty_action"
    if not math.isfinite(proposal.confidence) or not 0.0 <= proposal.confidence <= 1.0:
        return False, "invalid_confidence"
    if not state_known:
        return False, "unknown_world_state"
    if proposal.confidence < 0.75:
        return False, "confidence_below_threshold"
    if proposal.requires_human_approval and not approval:
        return False, "human_approval_required"
    if not proposal.simulated_only:
        return False, "physical_action_blocked_in_smoke_test"
    return True, "proposal_accepted_for_simulation"


def make_failure_report(case_id: str, expected: Any, actual: Any, severity: str = "error") -> dict[str, Any]:
    return {
        "case_id": case_id,
        "severity": severity,
        "expected": expected,
        "actual": actual,
        "status": "pass" if expected == actual else "fail",
    }


class SharedCoreContractTests(unittest.TestCase):
    def test_world_state_tracks_observation(self):
        state = WorldState()
        obs = Observation(source="mock_sensor", value="target_candidate", confidence=0.9)
        state.update("target", obs)
        self.assertEqual(state.observations["target"].value, "target_candidate")
        self.assertEqual(state.uncertainty_flags, [])

    def test_low_confidence_is_explicitly_flagged(self):
        state = WorldState()
        state.update("target", Observation(source="mock_sensor", value=None, confidence=0.2))
        self.assertIn("low_confidence:target", state.uncertainty_flags)

    def test_invalid_confidence_rejected(self):
        state = WorldState()
        with self.assertRaises(ValueError):
            state.update("target", Observation(source="mock_sensor", value="x", confidence=float("nan")))

    def test_unknown_state_fails_closed(self):
        ok, reason = authorize_action(ActionProposal("move", 0.99), state_known=False)
        self.assertFalse(ok)
        self.assertEqual(reason, "unknown_world_state")

    def test_low_confidence_action_rejected(self):
        ok, reason = authorize_action(ActionProposal("inspect", 0.4), state_known=True)
        self.assertFalse(ok)
        self.assertEqual(reason, "confidence_below_threshold")

    def test_human_approval_required(self):
        proposal = ActionProposal("high_impact_action", 0.95, requires_human_approval=True)
        ok, reason = authorize_action(proposal, state_known=True, approval=False)
        self.assertFalse(ok)
        self.assertEqual(reason, "human_approval_required")

    def test_physical_action_blocked(self):
        proposal = ActionProposal("actuator_command", 0.99, simulated_only=False)
        ok, reason = authorize_action(proposal, state_known=True)
        self.assertFalse(ok)
        self.assertEqual(reason, "physical_action_blocked_in_smoke_test")

    def test_simulated_proposal_can_pass_gate(self):
        ok, reason = authorize_action(ActionProposal("observe", 0.9), state_known=True)
        self.assertTrue(ok)
        self.assertEqual(reason, "proposal_accepted_for_simulation")

    def test_failure_report_is_machine_readable(self):
        report = make_failure_report("uncertainty-001", "fail", "fail")
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["case_id"], "uncertainty-001")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="reports/pui89-ai-core-smoke.json")
    args = parser.parse_args()
    started = time.perf_counter()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SharedCoreContractTests)
    result = unittest.TestResult()
    suite.run(result)
    elapsed = round(time.perf_counter() - started, 6)
    failures = [
        {"test": test.id(), "traceback": trace}
        for test, trace in result.failures + result.errors
    ]
    payload = {
        "schema_version": "1.0",
        "suite": "pui89-shared-ai-core-contract-smoke",
        "status": "pass" if result.wasSuccessful() else "fail",
        "tests_run": result.testsRun,
        "failures": failures,
        "duration_seconds": elapsed,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope_note": "Interface and safety-gate smoke checks only; no model accuracy or robot performance is measured.",
    }
    output = Path(args.report)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
