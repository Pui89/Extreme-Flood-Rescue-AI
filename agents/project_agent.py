"""Safety-first decision-support agent for Flood Rescue AI.

Recommendations only: no navigation, rescue, or actuator commands are executed.
Standard-library only; inputs are measurements supplied by the calling system.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class AgentDecision:
    project: str
    status: str
    recommendation: str
    reasons: tuple[str, ...]
    requires_human_approval: bool = True
    actuator_command: None = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["reasons"] = list(self.reasons)
        return result


def run_agent(observation: dict[str, Any]) -> AgentDecision:
    """Review a reconnaissance observation.

    Optional keys: sensor_ok, localization_ok, water_depth_m, route_clear,
    person_detected, detection_confidence (0..1), human_approved.
    """
    if not isinstance(observation, dict):
        raise TypeError("observation must be a dictionary")
    if observation.get("sensor_ok") is False:
        return AgentDecision("flood-rescue", "STOP", "STOP_AND_CHECK_SENSORS",
                             ("Sensor health check failed.",))
    if observation.get("localization_ok") is not True:
        return AgentDecision("flood-rescue", "NEED_DATA", "HOLD_AND_RELOCALIZE",
                             ("Reliable localization is not confirmed.",))
    depth = observation.get("water_depth_m")
    if not isinstance(depth, (int, float)) or isinstance(depth, bool) or depth < 0:
        return AgentDecision("flood-rescue", "NEED_DATA", "REQUEST_VALID_WATER_DEPTH",
                             ("A non-negative water-depth measurement is required.",))
    if observation.get("route_clear") is not True:
        return AgentDecision("flood-rescue", "STOP", "DO_NOT_ENTER_ROUTE",
                             ("Route safety has not been confirmed; the agent will not authorize entry.",))
    if observation.get("person_detected", False):
        confidence = observation.get("detection_confidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
            return AgentDecision("flood-rescue", "NEED_DATA", "REQUEST_VALID_DETECTION_CONFIDENCE",
                                 ("Person-detection confidence is missing or invalid.",))
        if confidence >= 0.50:
            return AgentDecision("flood-rescue", "URGENT_REVIEW", "ALERT_HUMAN_RESCUE_OPERATOR",
                                 ("Possible person detected; this is not a confirmed victim identification.",))
    if observation.get("human_approved") is not True:
        return AgentDecision("flood-rescue", "AWAITING_APPROVAL", "REQUEST_OPERATOR_REVIEW",
                             ("Basic supplied checks passed; an operator must review the route and context.",))
    return AgentDecision("flood-rescue", "READY_FOR_EXTERNAL_PLANNER",
                         "PASS_REVIEW_GATE_ONLY",
                         ("Review gate passed; no route is planned or executed by this module.",))


