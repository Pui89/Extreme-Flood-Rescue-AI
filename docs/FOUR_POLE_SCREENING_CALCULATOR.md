# Four-pole screening calculator

**Status: preliminary engineering aid only. Not a design tool, safety assessment, operating limit, or deployment authorisation.**

The standard-library-only script `tools/four_pole_screening.py` accepts explicitly supplied engineering values for **one pole and one simplified load case**. It reports:

- First-order steady-flow drag estimate: \(F_D = 0.5\rho C_D A v^2\).
- A crude drag-times-unsupported-length moment estimate.
- Ideal Euler-column critical-load estimate: \(P_{cr}=\pi^2EI/(KL)^2\).
- Axial demand divided by the ideal Euler estimate. This ratio is **not** a safety factor and is not a pass/fail result.

No defaults are provided for dimensions, materials, current, geometry or load. All required values must be supplied by the user or a qualified engineer. The tool does not assume four poles share load equally.

## Example invocation

The following values are **illustrative software-test inputs only**, not PUI89 design values, measured flood conditions, recommended parameters or safe limits:

```bash
python tools/four_pole_screening.py \
  --water-density-kg-m3 1000 \
  --drag-coefficient 1.0 \
  --projected-area-m2 0.1 \
  --current-velocity-m-s 2.0 \
  --elastic-modulus-pa 200000000000 \
  --second-moment-area-m4 0.000001 \
  --effective-length-factor 1.0 \
  --unsupported-length-m 2.0 \
  --axial-compressive-load-n 1000 \
  --output screening-report.json
```

The report is JSON and repeats its limitations. Invalid, missing, negative or non-finite inputs are rejected (zero is accepted only for current velocity and axial compressive load).

## What it does not establish

The equations omit turbulent/transient dam-break flow, waves, debris impact, pole-hull interaction, distributed-load structural response, telescoping-joint effects, buckling imperfections, fatigue, corrosion, ground bearing, sliding, pull-out, scour, hull load paths, stability and capsize. The calculation does not model the four-pole arrangement, a 15 m deployed member, the amphibious vehicle, passengers, rescue loads or actual flood conditions.

A low numerical demand ratio does not mean safe. A high ratio is a prompt for engineering investigation, not an automated verdict. A qualified marine/structural engineer must verify geometry, materials, boundary conditions, combined load cases, applicable standards and the complete hull/pole/ground system. Physical testing and independent review remain mandatory before any capability claim.

## Verification

Run the standard-library tests:

```bash
python -m unittest tests.test_four_pole_screening -v
```

Tests verify arithmetic, input rejection and report disclaimers only. They do not validate the equations against physical tests or certify the design.
