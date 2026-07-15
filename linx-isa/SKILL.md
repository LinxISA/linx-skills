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
- `TIME` (SSR `0x0010`) is a read-only monotonic nanosecond counter modulo
  `2^64`; it is not wall-clock time.
- `BSTART.PAR` and `B.IOD` are retired spellings in v0.56.5. Their encodings
  remain reserved evidence, assemblers reject the names, and canonical decode
  never exposes them as instruction identities (`BSTART.TEPL` owns its code).

## LinxArch mandatory gates

```bash
python3 /Users/zhoubot/linx-isa/tools/bringup/check_linxcore_arch_contract.py --root /Users/zhoubot/linx-isa --strict
python3 /Users/zhoubot/linx-isa/tools/bringup/check_linxcore_arch_contract.py --root /Users/zhoubot/linx-isa --strict --require-mkdocs
python3 /Users/zhoubot/linx-isa/tools/isa/build_golden.py --profile v0.56 --check
python3 /Users/zhoubot/linx-isa/tools/isa/validate_spec.py --profile v0.56
python3 /Users/zhoubot/linx-isa/tools/isa/check_canonical_v056.py --root /Users/zhoubot/linx-isa
python3 /Users/zhoubot/linx-isa/tools/isa/gen_sail_decode.py --check
python3 /Users/zhoubot/linx-isa/tools/isa/gen_sail_status.py --check
python3 /Users/zhoubot/linx-isa/tools/isa/sail_coverage.py --check
python3 /Users/zhoubot/linx-isa/tools/bringup/check_sail_model.py --require-parser --require-c-backend
python3 /Users/zhoubot/linx-isa/docs/check_documentation.py --root /Users/zhoubot/linx-isa
```

The Sail gate is toolchain-pinned by `isa/sail/toolchain.json`; required lanes
must install that exact version and may not treat a missing parser or C backend
as success. Semantic coverage is stable ISA form-ID based and grades each form
as `decode-only`, `executable-subset`, or `architecturally-complete`; never
infer semantic completeness from mnemonic presence alone. QEMU reporter form
coverage instead uses the encoding signature `(mnemonic, length, mask,
match)`; do not report that signature coverage as stable form-ID closure.
All generated-artifact checks must compare both contents and the exact owned
file set without rewriting the worktree.

Historical compatibility wrappers are retired. Do not restore
`check_public_v03.sh`, `check_canonical_v04.py`, or `check_no_legacy_v0*.py`
paths; update callers to the canonical v0.56 checks above instead.

## Contract pages that must stay authoritative

- `docs/architecture/v0.56-architecture-contract.md`
- `docs/architecture/v0.56-workload-engine-model.md`
- `docs/architecture/v0.56-rendering-command-contract.md`
- `docs/architecture/isa-manual/src/linxisa-isa-manual.adoc`
- `isa/v0.56/linxisa-v0.56.json`
- canonical LinxCore authoring:
  - `rtl/LinxCore/docs/architecture/overview.md`
  - `rtl/LinxCore/docs/architecture/microarchitecture.md`
  - `rtl/LinxCore/docs/architecture/interfaces.md`
  - `rtl/LinxCore/docs/architecture/verification-matrix.md`
- published mirrors:
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
- `references/v0.3_contracts_and_asm.md` (archive-only historical baseline; not an active v0.56 gate source)
