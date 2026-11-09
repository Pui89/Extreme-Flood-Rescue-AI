# PUI89 Shared AI Core schema snapshot — v0.1.0

These JSON Schema files are a read-only compatibility snapshot copied from
[PUI89/PUI89-Shared-AI-Core](https://github.com/Pui89/PUI89-Shared-AI-Core),
source commit `d7c16d0aee589349cd70b86bffaae531415c00cd` (main, 2026-11-09).

Why the snapshot exists: this project is public while the Shared AI Core is
private. GitHub Actions' default repository token cannot check out a private
repository from a different repository. The snapshot lets public CI validate
against the published contract version without exposing credentials or making
the Core repository public.

The snapshot contains schemas only, not shared implementation code. Do not
edit these files independently. To adopt a new contract version, update the
snapshot from the Core through a reviewed pull request and record its source
commit. These schemas use JSON Schema Draft 2020-12; the Core's lightweight
Python validator supports only its documented subset and is not a full
Draft 2020-12 validator.

This snapshot does not grant physical actuation authority. ActionProposal
remains advisory-only and requires human approval.
