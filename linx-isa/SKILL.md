---
name: linx-isa
description: Linx ISA architecture and specification workflow. Use when defining ISA contracts, editing manual semantics, reviewing privilege/CSR/memory rules, or translating ISA intent into compiler/emulator/RTL requirements and tests.
---

# Linx ISA

## Overview

Use this skill for ISA-level decisions and spec-quality updates that must stay consistent across software and hardware bring-up.

## Responsibilities

- Architecture intent and constraints.
- ISA manual clarity and machine-checkable semantics.
- Contract mapping into downstream requirements.

## Non-negotiable invariants

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
python3 /Users/zhoubot/linx-isa/tools/bringup/check_linxcore_arch_contract.py --root /Users/zhoubot/linx-isa --strict
python3 /Users/zhoubot/linx-isa/tools/bringup/check_linxcore_arch_contract.py --root /Users/zhoubot/linx-isa --strict --require-mkdocs
python3 /Users/zhoubot/linx-isa/tools/bringup/check26_contract.py --root /Users/zhoubot/linx-isa
```

## Contract pages that must stay authoritative

- `docs/architecture/v0.3-architecture-contract.md`
- `docs/architecture/linxcore/overview.md`
- `docs/architecture/linxcore/microarchitecture.md`
- `docs/architecture/linxcore/interfaces.md`
- `docs/architecture/linxcore/verification-matrix.md`

## Workflow

1. Update/verify ISA source-of-truth in `isa/` and manual docs in `docs/`.
2. Cross-check ambiguity against implementation requirements.
3. Confirm architecture matrix covers all required cross-domain gate keys.
4. Coordinate with `linx-core`, `linx-qemu`, and `linx-pycircuit` before promoting architecture-visible changes.
5. Capture evidence links for changed semantics.

## Skill evolve loop (mandatory closeout)

- At closeout, decide `skill-evolve: update` or `skill-evolve: no-update`.
- Update this skill only for material reusable findings:
  - new architecture contract/invariant needed by downstream modules,
  - new mandatory docs/gate mapping requirement,
  - new recurring ambiguity pattern with a repeatable resolution workflow.
- Do not update for wording cleanup, minor optimization, or one-off editorial fixes.
- If update is needed, limit to touched docs and validate with:
  - `python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/zhoubot/linx-isa/skills/linx-skills/linx-isa`
  - `python3 /Users/zhoubot/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main`

## Included scope

This consolidated skill absorbs prior `arch-bringup` and `isa-manual` scopes.

## References

- `references/spec_alignment.md`
- `references/v0.3_contracts_and_asm.md` (v0.3 stable contracts + assembler-visible encodings; LLVM/QEMU parity checklist)
