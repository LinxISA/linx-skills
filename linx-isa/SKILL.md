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
- `BSTART.PAR` and `B.IOD` are retired spellings in v0.57. Their encodings
  remain reserved evidence, assemblers reject the names, and canonical decode
  never exposes them as instruction identities (`BSTART.TEPL` owns its code).
- v0.57 is the sole active ISA release. Do not revive legacy forms; active
  specification, generator, compiler, and emulator gates use only v0.57.
- v0.57 TPREFETCH is encoded adjacent to TLOAD/TSTORE and is destination-free:
  model it as TLOAD addressing/attributes with no destination queue publication.
- v0.57 TMA selectors are the contiguous PTO tile-memory family 0..8. Keep PTO
  tile op selector tables dense and reject holes or aliases unless the golden
  manifest explicitly reserves them.
- CUBE block/template names are unique architectural identities in v0.57. Do
  not reuse a CUBE mnemonic, template key, or generated block-template entry for
  two distinct forms.
- v0.57 scalar CAS/DMA forms are active ISA deltas; they must be present in the
  golden catalog, generated codec tables, manual fragments, compiler MC
  coverage, and QEMU decode metadata before closure.
- v0.57 PTO ISA mapping has 111 PTO dialect operations. PTOAS and ISA manifest
  checks must agree on the 111-entry map; missing PTO entries are blockers, and
  legacy selector spellings are rejected rather than normalized.
- Before changing a form with a variable selector, enumerate its raw words
  against every generic selector space at the same instruction length. If one
  raw word has multiple architectural meanings, freeze the ISA/assembler
  contract first; decoder priority or a single-component decoder change is not
  a valid repair.
- Before concatenating adjacent encoded fields into one logical operand, audit
  the form's introduction history and exact sub-instruction boundaries. A
  compound form that embeds independently relocatable operations keeps their
  operand roles, PC bases, and side effects unless an explicit architecture
  decision redefines it. Require metamorphic raw tests that vary each field
  independently; field adjacency or equal aggregate width is not evidence of
  concatenation.

## LinxArch mandatory gates

```bash
python3 /Users/zhoubot/linx-isa/tools/bringup/check_linxcore_arch_contract.py --root /Users/zhoubot/linx-isa --strict
python3 /Users/zhoubot/linx-isa/tools/bringup/check_linxcore_arch_contract.py --root /Users/zhoubot/linx-isa --strict --require-mkdocs
python3 /Users/zhoubot/linx-isa/tools/isa/build_golden.py --profile v0.57 --check
python3 /Users/zhoubot/linx-isa/tools/isa/validate_spec.py --profile v0.57
python3 /Users/zhoubot/linx-isa/tools/isa/check_canonical_v057.py --root /Users/zhoubot/linx-isa
python3 /Users/zhoubot/linx-isa/tools/isa/check_pto_v057_manifest.py --root /Users/zhoubot/linx-isa
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

Historical compatibility wrappers are retired. Update every caller to the
canonical v0.57 checks above instead of restoring versioned wrappers.

## Contract pages that must stay authoritative

- `docs/architecture/v0.57-architecture-contract.md`
- `docs/architecture/v0.57-encoding-decisions.md`
- `docs/architecture/isa-manual/src/linxisa-isa-manual.adoc`
- `isa/v0.57/linxisa-v0.57.json`
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
