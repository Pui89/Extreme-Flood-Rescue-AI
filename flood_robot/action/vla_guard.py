from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real
from typing import Any


def _is_unit_interval(value: Any) -> bool:
    """Accept only finite, non-Boolean real numbers in the closed interval [0, 1]."""
    if isinstance(value, bool) or not isinstance(value, Real):
        return False
    try:
        numeric = float(value)
    except (OverflowError, TypeError, ValueError):
        return False
    return math.isfinite(numeric) and 0.0 <= numeric <= 1.0


@dataclass
class ActionDecision:
    approved: bool
    reason: str
    action: Any = None


class VLAGuard:
    """Software guard for VLA proposals; not a standalone physical safety controller."""

    def __init__(self, min_confidence: Any = 0.70):
        if not _is_unit_interval(min_confidence):
            raise ValueError("min_confidence must be a finite number in [0, 1]")
        self.min_confidence = float(min_confidence)

    def validate(
        self,
        action: Any,
        *,
        confidence: Any,
        collision_free: Any,
        human_too_close: Any = False,
        emergency: Any = False,
    ) -> ActionDecision:
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

        if not _is_unit_interval(confidence):
            return ActionDecision(False, "invalid_confidence")

        if float(confidence) < self.min_confidence:
            return ActionDecision(False, "action_uncertainty")

        return ActionDecision(True, "approved", action)
