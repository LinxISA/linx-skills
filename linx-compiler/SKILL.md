---
name: linx-compiler
description: Linx compiler/backend workflow for LLVM and compile gates. Use when implementing or debugging Linx codegen/MC behavior, enforcing call/ret lowering contracts, running compile coverage suites, or validating object/relocation correctness.
---

# Linx Compiler

## Overview

Use this skill for all compiler-side work centered on `compiler/llvm` and AVS compile gates.

## Focus areas

- Target backend changes (TableGen/ISel/MC/asm/disasm).
- ABI and call/ret lowering correctness.
- Compile-only gate stability and coverage.

## Canonical checks

```bash
bash /Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests/run.sh
python3 /Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests/analyze_coverage.py --fail-under 100
```

## Toolchain lane policy

- Pin lane defaults to in-repo binaries:
  - `CLANG=/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/clang`
  - `LLD=/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/ld.lld`
- Use external toolchain paths only in external lane or explicit override.
- In reports, include lane + compiler path provenance so gate outcomes are
  reproducible.

## Call/ret compile contract

- enforce call-header adjacency,
- preserve `FENTRY + FRET.STK` normal path,
- keep `FENTRY + FEXIT` tail-transfer path legal,
- preserve relocation/template checks.

## Workflow

1. Implement backend change.
2. Add lit/FileCheck coverage.
3. Run AVS compile matrix and coverage.
4. Confirm no cross-stack call/ret regressions.

## Included scope

This consolidated skill absorbs prior `llvm-backend` and compiler-side `call-ret-parity` workflows.

## References

- `references/compiler_checks.md`
- `references/v0.3_codegen_and_asm_contracts.md` (v0.3 codegen/asm encodings; TEPL/TOPS contract)
