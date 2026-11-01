#!/usr/bin/env python3
"""Preliminary, user-input-only screening calculations for one proposed pole.

This tool is not a design code, structural analysis, safety assessment, or
operational interlock. It never decides that a pole or vehicle is safe.
"""
from __future__ import annotations

import argparse
import json
import math
from typing import Any


DISCLAIMER = (
    "SCREENING ONLY: simplified steady-flow drag and ideal Euler-column "
    "equations. Not a design approval, safe-load rating, flood-current model, "
    "or permission to deploy. Obtain qualified independent engineering review."
)


def _positive_finite(name: str, value: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be finite and greater than zero")
    return number


def calculate_screening(
    *,
    water_density_kg_m3: float,
    drag_coefficient: float,
    projected_area_m2: float,
    current_velocity_m_s: float,
    elastic_modulus_pa: float,
    second_moment_area_m4: float,
    effective_length_factor: float,
    unsupported_length_m: float,
    axial_compressive_load_n: float,
) -> dict[str, Any]:
    """Calculate separate first-order drag, moment and ideal Euler screens.

    All inputs describe one engineer-defined pole/load case. No four-pole load
    sharing is assumed. The returned ratio is demand / ideal Euler critical
    load, not a safety factor and not a pass/fail result.
    """
    positive = {
        "water_density_kg_m3": water_density_kg_m3,
        "drag_coefficient": drag_coefficient,
        "projected_area_m2": projected_area_m2,
        "elastic_modulus_pa": elastic_modulus_pa,
        "second_moment_area_m4": second_moment_area_m4,
        "effective_length_factor": effective_length_factor,
        "unsupported_length_m": unsupported_length_m,
    }
    values = {name: _positive_finite(name, value) for name, value in positive.items()}

    try:
        velocity = float(current_velocity_m_s)
    except (TypeError, ValueError) as exc:
        raise ValueError("current_velocity_m_s must be a finite number >= 0") from exc
    if not math.isfinite(velocity) or velocity < 0:
        raise ValueError("current_velocity_m_s must be finite and >= 0")

    try:
        axial_load = float(axial_compressive_load_n)
    except (TypeError, ValueError) as exc:
        raise ValueError("axial_compressive_load_n must be a finite number >= 0") from exc
    if not math.isfinite(axial_load) or axial_load < 0:
        raise ValueError("axial_compressive_load_n must be finite and >= 0")

    drag_n = (
        0.5
        * values["water_density_kg_m3"]
        * values["drag_coefficient"]
        * values["projected_area_m2"]
        * velocity**2
    )
    length = values["unsupported_length_m"]
    bending_moment_nm = drag_n * length
    euler_critical_load_n = (
        math.pi**2
        * values["elastic_modulus_pa"]
        * values["second_moment_area_m4"]
        / (values["effective_length_factor"] * length) ** 2
    )
    demand_ratio = (
        axial_load / euler_critical_load_n if euler_critical_load_n > 0 else None
    )

    return {
        "status": "SCREENING_RESULT_ONLY_NO_SAFETY_VERDICT",
        "disclaimer": DISCLAIMER,
        "scope": "one user-defined pole and one simplified load case; no load sharing assumed",
        "inputs": {
            **values,
            "current_velocity_m_s": velocity,
            "axial_compressive_load_n": axial_load,
        },
        "results": {
            "steady_flow_drag_estimate_n": drag_n,
            "drag_times_unsupported_length_moment_estimate_nm": bending_moment_nm,
            "ideal_euler_critical_load_estimate_n": euler_critical_load_n,
            "axial_demand_divided_by_ideal_euler_load": demand_ratio,
        },
        "limitations": [
            "Drag equation omits turbulence, waves, debris impact, transient dam-break fronts and pole-hull interaction.",
            "Moment is a crude drag-times-length screen, not a distributed-load structural solution.",
            "Euler equation assumes an ideal column; telescoping joints, imperfections, bending, corrosion, fatigue and dynamic effects are not represented.",
            "No material, section, joint, hull attachment, ground bearing, sliding, pull-out, scour, stability or capsize verification is performed.",
            "No sharing or equalisation of load between four poles is assumed.",
            "A numerical result cannot establish a safe operating envelope or authorise deployment.",
        ],
        "required_next_step": "Independent qualified engineering review using verified geometry, material data, boundary conditions, load combinations and applicable standards.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preliminary four-pole concept screening; not a safety assessment."
    )
    parser.add_argument("--water-density-kg-m3", type=float, required=True)
    parser.add_argument("--drag-coefficient", type=float, required=True)
    parser.add_argument("--projected-area-m2", type=float, required=True)
    parser.add_argument("--current-velocity-m-s", type=float, required=True)
    parser.add_argument("--elastic-modulus-pa", type=float, required=True)
    parser.add_argument("--second-moment-area-m4", type=float, required=True)
    parser.add_argument("--effective-length-factor", type=float, required=True)
    parser.add_argument("--unsupported-length-m", type=float, required=True)
    parser.add_argument("--axial-compressive-load-n", type=float, required=True)
    parser.add_argument("--output", help="Optional path for a JSON report; stdout if omitted.")
    args = parser.parse_args()

    try:
        report = calculate_screening(
            water_density_kg_m3=args.water_density_kg_m3,
            drag_coefficient=args.drag_coefficient,
            projected_area_m2=args.projected_area_m2,
            current_velocity_m_s=args.current_velocity_m_s,
            elastic_modulus_pa=args.elastic_modulus_pa,
            second_moment_area_m4=args.second_moment_area_m4,
            effective_length_factor=args.effective_length_factor,
            unsupported_length_m=args.unsupported_length_m,
            axial_compressive_load_n=args.axial_compressive_load_n,
        )
    except ValueError as exc:
        parser.error(str(exc))

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
