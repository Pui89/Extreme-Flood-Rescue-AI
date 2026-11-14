# Extreme Flood Rescue AI — Issue label taxonomy

This file defines the recommended labels for consistent triage. It does not create GitHub labels automatically. Repository labels must be created and verified separately before templates or automation depend on them.

## Recommended labels

### Type
- `type:bug`
- `type:feature`
- `type:research`
- `type:documentation`

### Priority
- `priority:critical`
- `priority:high`
- `priority:normal`
- `priority:low`

### Status
- `status:needs-triage`
- `status:blocked`
- `status:in-progress`
- `status:needs-evidence`
- `status:ready-for-review`

### Evidence maturity
- `evidence:concept`
- `evidence:synthetic`
- `evidence:simulated`
- `evidence:bench-tested`
- `evidence:field-validated`
- `evidence:independently-verified`

### Risk
- `risk:safety`
- `risk:security`
- `risk:privacy`
- `risk:licensing`

## Triage rules
1. Apply labels only after a human reviews the issue.
2. Use the highest justified priority; do not infer urgency from unsupported claims.
3. Mark evidence maturity according to the strongest directly linked evidence, not the intended roadmap.
4. Safety, security, privacy, and licensing concerns require explicit review.
5. Do not close an issue solely because evidence is incomplete; request the missing evidence.

## Product boundary
This taxonomy is workflow guidance, not a certification, safety case, field validation, or proof that a capability exists.
