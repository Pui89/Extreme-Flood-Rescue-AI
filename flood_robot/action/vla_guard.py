from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass
class ActionDecision:
    approved: bool
    reason: str
    action: Any = None


class VLAGuard:
    """Safety boundary between LeRobot/VLA policies and robot actuators."""

    def __init__(self, min_confidence=0.70):
        if (
            isinstance(min_confidence, bool)
            or not isinstance(min_confidence, (int, float))
            or not math.isfinite(min_confidence)
            or not 0.0 <= min_confidence <= 1.0
        ):
            raise ValueError("min_confidence must be a finite number in [0, 1]")
        self.min_confidence = float(min_confidence)

    def validate(
        self,
        action,
        *,
        confidence,
        collision_free,
        human_too_close=False,
        emergency=False,
    ):
        # Safety flags must be actual booleans. Strings such as "false" are
        # ambiguous and must never be interpreted as permission to move.
        if any(
            type(flag) is not bool
            for flag in (collision_free, human_too_close, emergency)
        ):
            return ActionDecision(False, "invalid_safety_flag")

        if emergency:
            return ActionDecision(False, "emergency_stop")
        if human_too_close:
            return ActionDecision(False, "human_exclusion_zone")
        if not collision_free:
            return ActionDecision(False, "collision_check_failed")

        if action is None:
            return ActionDecision(False, "missing_action")

        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not math.isfinite(confidence)
            or not 0.0 <= confidence <= 1.0
        ):
            return ActionDecision(False, "invalid_confidence")

        if confidence < self.min_confidence:
            return ActionDecision(False, "action_uncertainty")

        return ActionDecision(True, "approved", action)
