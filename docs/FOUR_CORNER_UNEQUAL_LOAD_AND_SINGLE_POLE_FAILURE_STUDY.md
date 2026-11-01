# Four-corner unequal-load and single-pole-failure study

**Status: CONCEPT / ANALYTICAL STUDY PLAN / NOT DESIGNED / NOT TESTED.** This document defines the next engineering questions for the proposed four independently monitored retractable poles. It does not calculate a safe operating envelope, establish load ratings, or authorise deployment.

## 1. Why equal load sharing must not be assumed

Four poles do not automatically carry one quarter of the total load each. Real reactions depend on hull geometry, pole spacing, attachment stiffness, pole extension, ground elevation and stiffness, contact-pad behaviour, preload, hull flexibility, current direction, vehicle attitude and transient events.

A simple division of total load by four is therefore not an acceptable design assumption. Even a symmetric vehicle can experience strongly asymmetric reactions when one foot contacts soft sediment, one pole is longer, or flow acts off-centre.

The existing `tools/four_pole_screening.py` evaluates one simplified pole/load case. It is not a four-support structural solver. Do not combine four independent outputs and call the result a system safety assessment.

## 2. Required four-corner load-case matrix

Identify corners consistently in the vehicle coordinate system (for example, front-left, front-right, rear-left, rear-right). The labels are bookkeeping only; the final coordinate convention must be defined on a dimensioned hull drawing.

| Case | Condition to investigate | Questions and required evidence |
|---|---|---|
| LC-01 | Symmetric vertical support | What are the actual reactions from a validated hull/pole/ground stiffness model? |
| LC-02 | Front-biased vertical load | Does trim change, and can the front attachments and hull carry the resulting reactions? |
| LC-03 | Side-biased vertical load | What roll moment and cross-hull load path develop? |
| LC-04 | Diagonal support / uneven ground | Can the hull twist, unload a foot, or overload the opposite diagonal? |
| LC-05 | One soft or settling foot | How do reactions redistribute as one support loses stiffness or sinks? |
| LC-06 | One foot loses contact | Is the remaining support geometry stable, or does the craft tip/slide before recovery? |
| LC-07 | One pole jammed at partial extension | Can the vehicle remain in a safe state without forcing the other poles to compensate? |
| LC-08 | One pole bent or structurally degraded | Can the pole be isolated and released without sudden load transfer? |
| LC-09 | Off-centre steady current | What combined lateral force, yaw, roll and bending loads reach each pole and attachment? |
| LC-10 | Transient flow / wave / debris event | What dynamic analysis and controlled test evidence are needed? The simple steady-flow calculator is insufficient. |

For each case record the applied load vector, its point of application, current direction and velocity history where relevant, vehicle mass and centre of gravity, buoyancy distribution, pole geometry, support conditions, uncertainty bounds, model version and reviewer.

## 3. Single-pole failure is a system-level event

A failed, jammed, detached or suddenly unloaded pole can cause a rapid change in support geometry. The remaining three poles must **not** be assumed to accept the missing reaction safely. Depending on the configuration, the craft may rotate, slide, pitch, roll, twist, capsize or overload another attachment.

At minimum, analyse each of the four possible single-pole-loss cases separately:

- front-left unavailable;
- front-right unavailable;
- rear-left unavailable;
- rear-right unavailable.

Also analyse non-structural failures that can have similar consequences: false position feedback, incorrect load-sensor readings, power loss, actuator runaway, a pole that cannot retract, a foot trapped by debris, and a communication or controller fault.

A single-pole-loss analysis must report whether the remaining support arrangement has a stable equilibrium, whether any support reaction becomes tensile or otherwise physically impossible for the selected foot, the predicted motion before intervention, the peak loads during redistribution, and the available recovery or release path. If these cannot be established, the safe design response is to prohibit deployment in that condition.

## 4. Minimum model before numerical conclusions

A credible four-support model needs, at minimum:

1. A dimensioned hull coordinate system and pole attachment locations.
2. Vehicle mass, centre of gravity, buoyancy and relevant inertia data.
3. Pole section, material properties, telescoping overlap, joint details, imperfections and boundary conditions.
4. Attachment and hull stiffness, including local reinforcement and global hull flexibility.
5. Ground contact model: surveyed elevation, bearing stiffness/capacity, friction, settlement, scour and uncertainty.
6. Environmental load cases, including direction, spatial distribution, transients and debris hazards.
7. Sensor error, latency, actuator limits, power-loss behaviour and emergency release dynamics.
8. Independent review of assumptions, equations, numerical method, mesh/convergence where applicable, and sensitivity.

The model must solve equilibrium and compatibility together. It must not impose equal reactions by default. Contact loss, sliding, uplift, pole buckling, joint limits and nonlinear ground response may require nonlinear analysis. Dynamic events require an appropriate time-dependent model.

## 5. Safety logic to investigate

The concept should default to **poles stowed and mechanically retained** during travel and whenever conditions are unknown. Any future deployment interlock would need verified vehicle speed, depth, current, obstacle clearance, ground survey, pole health, sensor validity, attachment condition and explicit human authorisation.

A detected mismatch, overload, unexpected movement, sensor disagreement, loss of communications or power should enter a pre-analysed safe state. Do not assume automatic retraction is always safest: retracting one loaded pole can itself trigger instability. The recovery sequence must be derived from validated failure analysis and include a controlled release option where feasible.

Do not deploy long poles in fast current, dam-break flow, debris fields, near people, or over unknown ground on the basis of this software study. The proposed up-to-15 m extension remains a concept envelope only.

## 6. Required outputs for every analysed case

Publish a machine-readable record and an engineer-readable report containing:

- case identifier and configuration revision;
- input values, units, provenance and uncertainty;
- assumptions and excluded physics;
- reaction and load distribution for all four poles;
- hull, attachment, pole, joint and ground demand results;
- predicted attitude and stability margins, with method and limitations;
- failure sequence and time-to-critical-state where dynamic analysis supports it;
- sensitivity to uncertain inputs;
- independent reviewer, review date and unresolved actions.

Never publish a single green/red status without the underlying loads, criteria, uncertainty and reviewer approval. No allowable stress, buckling margin, stability threshold or operating limit is supplied by this document.

## 7. Staged validation gate

1. Freeze requirements and coordinate conventions; obtain a dimensioned concept drawing.
2. Obtain independent marine, structural and geotechnical review of the load paths and ground-contact concept.
3. Build and verify a four-support analytical model against hand-checkable limiting cases.
4. Run unequal-load, contact-loss and each single-pole-failure case with sensitivity analysis.
5. Conduct dry, instrumented component and attachment tests only after engineering review.
6. Progress to unmanned, low-energy controlled-water tests with exclusion zones and independent emergency recovery.
7. Expand environmental conditions only after each prior gate is accepted and recorded.

**No step in this plan validates a 15 m pole, dam-break resistance, extreme-current station-keeping, passenger safety or operational rescue capability.** Those claims require measured physical evidence and independent engineering approval.

## 8. Relationship to the preliminary calculator

The preliminary calculator remains a one-pole screening aid for simplified steady-flow drag and ideal Euler-column buckling. Its results are not safety factors. This study does not silently extend that tool into a four-pole solver. Any future software implementation must preserve the distinction between illustrative calculations, verified analytical models, physical test results and field evidence.
