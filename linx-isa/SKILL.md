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

## Workflow

1. Update/verify ISA source-of-truth in `isa/` and manual docs in `docs/`.
2. Cross-check ambiguity against implementation requirements.
3. Confirm test plan coverage in compile/runtime gates.
4. Capture evidence links for changed semantics.

## Included scope

This consolidated skill absorbs prior `arch-bringup` and `isa-manual` scopes.

## References

- `references/spec_alignment.md`
- `references/v0.3_contracts_and_asm.md` (v0.3 stable contracts + assembler-visible encodings; LLVM/QEMU parity checklist)
