---
name: linx-isa
description: Linx ISA architecture and specification workflow. Use when defining ISA contracts, editing manual semantics, reviewing privilege/CSR/memory rules, or translating ISA intent into compiler/emulator/RTL requirements and tests.
---

# Linx ISA

## Overview

Use this skill for ISA-level decisions and spec-quality updates in `~/linx-isa` that must stay consistent across software and hardware bring-up.

## Responsibilities

- Architecture intent and constraints.
- ISA manual clarity and machine-checkable semantics.
- Contract mapping into downstream requirements.

## Non-negotiable invariants

- **Coverage merge threshold:** Do not merge coverage-only PRs unless the net `implemented_forms` increase is **≥ 5%** of `total_forms`, unless the user explicitly asks to merge earlier.

- Block-structured control-flow contract is explicit.
- Safety rule on control-flow targets is enforced.
- Template and decoupled block semantics are unambiguous.
- Trap/privilege and memory-model behavior is precise.
- `EBREAK` default behavior is architectural breakpoint trap; semihost handling
  is opt-in (`LINX_SEMIHOST=1`) and must not be implicit.
- `BI=1` trap return contract explicitly restores second-layer block state
  (`EBARG/BSTATE`, including `TQ/UQ` queues and continuation PCs).

## LinxArch mandatory gates

```bash
python3 ~/linx-isa/tools/isa/build_golden.py --profile v0.4 --check
python3 ~/linx-isa/tools/isa/validate_spec.py --profile v0.4
python3 ~/linx-isa/tools/bringup/check_sail_model.py
python3 ~/linx-isa/tools/isa/check_canonical_v04.py --root ~/linx-isa
python3 ~/linx-isa/tools/bringup/check_linxcore_arch_contract.py --root ~/linx-isa --strict --require-mkdocs
```

## Contract pages that must stay authoritative

- `docs/architecture/v0.4-architecture-contract.md`
- `docs/architecture/isa-manual/src/linxisa-isa-manual.adoc`
- `docs/architecture/v0.4-hardening-policy.md`
- `docs/architecture/v0.4-workload-engine-model.md`
- `docs/architecture/v0.4-rendering-kernel-authoring.md`
- `docs/architecture/v0.4-rendering-pto-contract.md`
- `docs/architecture/v0.4-rendering-command-contract.md`
- `docs/architecture/linxcore/overview.md`
- `docs/architecture/linxcore/microarchitecture.md`
- `docs/architecture/linxcore/interfaces.md`
- `docs/architecture/linxcore/verification-matrix.md`

`docs/architecture/v0.4-draft/README.md` is archival context only and must not be treated as the active source of truth.

## Workflow

1. Update/verify ISA source-of-truth in `isa/` and manual docs in `docs/`.
2. Cross-check ambiguity against implementation requirements.
3. Before surfacing a design question, re-read the relevant manual/state files and recent working memory so already-settled points are not re-asked as if unresolved.
4. For any control-flow, trap-state, or save/restore ambiguity, first classify which layer is being described: block/header stream vs body/kernel stream, and top-level architectural state vs second-layer `BSTATE`/`EBSTATE` state. Do not treat those layers as interchangeable.
5. Confirm architecture matrix covers all required cross-domain gate keys.
6. Coordinate with downstream compiler/emulator/RTL/pyCircuit owners before promoting architecture-visible changes; when using skills, route emulator/pyCircuit alignment through `linx-ide` and RTL/microarchitecture alignment through `linxcore`.
7. Capture evidence links for changed semantics.

## Skill evolve loop (mandatory closeout)

- At closeout, decide `skill-evolve: update` or `skill-evolve: no-update`.
- Update this skill only for material reusable findings:
  - new architecture contract/invariant needed by downstream modules,
  - new mandatory docs/gate mapping requirement,
  - new recurring ambiguity pattern with a repeatable resolution workflow.
- Do not update for wording cleanup, minor optimization, or one-off editorial fixes.
- If update is needed, limit to touched docs and validate with:
  - `QUICK_VALIDATE=$(find ~/.codex ~/.openclaw /home/zhoubot -path '*/skill-creator/scripts/quick_validate.py' 2>/dev/null | head -n1); test -n "$QUICK_VALIDATE" && python3 "$QUICK_VALIDATE" ~/linx-isa/skills/linx-skills/linx-isa`
  - `python3 ~/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py --repo-root ~/linx-isa/skills/linx-skills --base origin/main`

## Included scope

This consolidated skill absorbs prior `arch-bringup` and `isa-manual` scopes.

## References

- `references/spec_alignment.md`
- `references/v0.3_contracts_and_asm.md` (v0.3 stable contracts + assembler-visible encodings; LLVM/QEMU parity checklist)
- `../linx-ide/references/v0.3_qemu_trap_contracts.md` (QEMU/pyCircuit-facing runtime and trap-alignment reference)
