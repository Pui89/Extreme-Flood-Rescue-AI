# Four-pole deployable stabiliser — engineering feasibility study

**Status: CONCEPT / NOT DESIGNED / NOT TESTED.** This document converts the proposed four long retractable poles beneath the amphibious rescue raft into a reviewable engineering study. It does not establish that the vehicle can resist a dam-break wave, fast current, or any specified flood condition.

## 1. Design intent

The concept has **four independently monitored telescoping poles**, arranged near the four hull corners and stowed in protected underside housings during travel. The intended research question is whether a controlled deployment could provide temporary station-keeping or reduce drift/roll in a specifically surveyed, low-energy environment.

The user's proposed maximum pole length is **up to 15 m**. Treat 15 m as a concept envelope to investigate, not a selected member length, a guaranteed extension, or a safe operating depth. The required extension depends on water depth, hull freeboard, ground clearance, sediment, obstacles, and the actual stabilisation method.

## 2. Critical distinction: stabilisers are not automatically anchors

A pole touching the riverbed is not necessarily an anchor. It may slide, penetrate unpredictably, buckle, bend, snag debris, or transfer a damaging overturning load into the hull.

The four poles must therefore be studied in separate modes:

| Mode | Intended use | Initial engineering position |
|---|---|---|
| Stowed transit | All poles retracted and mechanically retained | Default state for travel and current exposure |
| Shallow-water support | Carefully controlled contact with verified firm ground | Research only; low-energy, unmanned tests first |
| Station-keeping | Temporary resistance to small, measured environmental loads | Requires surveyed substrate and validated load path |
| Deep/fast-current flood | Poles extended into unknown water/ground | **Prohibited by default**; no evidence that this is safe |
| Emergency release | Retract, release, or isolate a jammed/damaged pole | Must be designed and tested before any water trial |

Do not deploy long poles while moving through fast current, debris, trees, cables, buildings, culverts, or unknown submerged obstacles. A pole snag can abruptly stop one corner, yaw or capsize the craft, or injure people nearby.

## 3. Four-corner arrangement

The preliminary layout is one pole near each corner, with the following design questions still open:

- Is each pole vertical, angled, or articulated?
- Does it terminate in a replaceable broad foot, a non-penetrating pad, or a specialised seabed interface?
- Can the four poles carry load independently, or are they mechanically linked?
- Can the hull remain stable if one pole fails, jams, or contacts a different ground height?
- How are lateral loads, bending moments, torsion and asymmetric ground reactions transferred into reinforced hull structure?
- Can a pole be isolated and safely released without destabilising the craft?

A broad foot may reduce local bearing pressure but can increase hydrodynamic drag and snag risk. A pointed foot may penetrate soft sediment but can disappear into weak ground and become difficult to recover. Neither interface is selected.

## 4. Minimum engineering calculations

No dimensions, material grades, wall thicknesses, extension speeds, actuator forces, or load ratings should be published until the following inputs are measured or justified.

### 4.1 Current-induced force

For a first-order screening estimate:

\[
F_D = \tfrac{1}{2}\rho C_D A v^2
\]

where:

- \(\rho\) = water density for the actual water condition;
- \(C_D\) = drag coefficient for the real pole/foot geometry and orientation;
- \(A\) = projected area exposed to flow;
- \(v\) = local current velocity relative to the pole.

This simplified relation does not represent turbulent dam-break fronts, debris impact, rapidly changing flow, vortices, wave action, or interaction between four poles and the hull. Those cases need appropriate specialist analysis and controlled validation.

### 4.2 Bending moment and hull load path

For each pole, determine the distributed hydrodynamic and contact loads and calculate the resulting shear force and bending moment along its full deployed length. The hull attachment, housing, locking mechanism and local hull reinforcement must be checked for the combined load cases, including one-pole snag and asymmetric loading.

### 4.3 Slender-member buckling

A preliminary idealised Euler screening equation is:

\[
P_{cr} = \frac{\pi^2 E I}{(K L)^2}
\]

where \(E\) is elastic modulus, \(I\) is the relevant second moment of area, \(K\) is an effective-length factor, and \(L\) is unsupported length. A telescoping, jointed, imperfect member exposed to bending, impact, corrosion and dynamic loads is not an ideal Euler column. The equation is a warning-screen, not a design approval.

### 4.4 Ground bearing and pull-out

The ground interface must be assessed for bearing failure, sliding, pull-out, scour, liquefaction/softening, erosion and changing bed levels. Do not assume that a riverbed, road surface, mud, rubble or submerged soil can support a pole reaction. Unknown substrate means no anchoring claim.

### 4.5 Stability and capsize

Recalculate displacement, freeboard, centre of gravity, righting response and roll/pitch stability for every permitted pole state and payload configuration. Include a single pole jammed, a pole suddenly released, unequal contact heights, asymmetric passenger/supply loads, and a pole snagged by debris. A four-pole system can make stability worse if it locks the hull to a moving obstruction.

## 5. Required failure controls

The control design should include, at minimum:

- Independent position and extension feedback for all four poles.
- Load or strain sensing at each pole or attachment, with sensor plausibility checks.
- Mechanical travel stops and positive stow locks.
- A no-deploy interlock when speed, current, debris, depth, ground confidence, or sensor health is outside a validated envelope.
- A safe response to power loss, communication loss, sensor disagreement, jam, overload and unexpected contact.
- A physically independent emergency release/recovery strategy; software commands alone are not sufficient.
- Human authorisation before deployment and before any change in pole load-bearing state.
- Event logs recording commands, sensor health, estimated loads, overrides and release events.

The safe default for unknown conditions is **poles stowed, propulsion/route decision returned to the vehicle's independently validated safety policy, and human review**. Do not assume that extending poles is always the safest action.

## 6. Staged verification plan

1. **Requirements capture:** define intended use, prohibited environments, maximum concept extension, hull geometry, pole spacing, payload cases and operator roles.
2. **Independent engineering review:** obtain qualified marine, structural and mechanical review of materials, joints, load paths, corrosion, fatigue and release design.
3. **Analytical screening:** evaluate current drag, bending, buckling, bearing, stability and single-failure cases using documented inputs and uncertainty ranges.
4. **Dry bench tests:** test each telescoping mechanism, lock, position sensor, overload response, power-loss state and emergency release with no people or animals aboard.
5. **Instrumented static tests:** use a controlled test fixture and known loads to compare measured strain/deflection with the reviewed model.
6. **Unmanned controlled-water tests:** only after independent sign-off, in still water with a recovery system, exclusion zone, abort criteria and qualified supervision.
7. **Progressive environmental tests:** increase complexity only through documented review gates. No dam-break, flood-current, debris-field or occupied-raft trial is implied by this plan.

Every result must identify the tested pole configuration, material, extension, hull attachment, load case, instrumentation, calibration, uncertainty, failures and reviewer. A successful bench test does not validate flood operation.

## 7. Evidence required before any capability claim

| Claim | Minimum evidence |
|---|---|
| Pole extends to a stated length | Measured full-scale mechanism test, including tolerance and loaded deflection |
| Pole supports a stated load | Reviewed calculations plus calibrated structural tests for the complete load path |
| Pole holds position in current | Controlled water test with measured flow, substrate, geometry and load |
| Four poles improve stability | Comparative hull stability tests across symmetric and asymmetric cases |
| Safe emergency release | Repeated instrumented fault-injection tests, including power loss and jam |
| Suitable for rescue use | Independent system-level safety case and supervised trials with applicable approvals |

## 8. Current boundary

- Four poles are a user-proposed concept, not a built subsystem.
- Up to 15 m is a study envelope, not a verified pole specification or a 15 m flood operating capability.
- No current-speed, anchoring, holding-force, payload or passenger rating is established.
- The existing 0–15 m flood scenario range remains a software/design simulation target; this surface craft is not thereby rated for deep submergence.
- Do not use the poles as a substitute for hull buoyancy, propulsion, steering, a safe operating envelope, rescue-team judgement or a recovery plan.

**Decision gate:** keep the four-pole mechanism at concept stage until geometry, intended operating mode, load cases, substrate assumptions, independent review and controlled test evidence are available.
