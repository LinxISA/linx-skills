---
name: linx-avs-runtime-gates
description: AVS execution and gate-triage workflow for LinxISA. Use when running compile/runtime/system suites, diagnosing regressions in QEMU/Linux/libc integration, validating mnemonic coverage, or producing reproducible gate evidence with explicit commands and SHAs.
---

# Linx AVS Runtime Gates

## Overview

Use this skill to run AVS as the operational truth source and produce reproducible pass/fail evidence for compiler, emulator, and runtime bring-up.

## Canonical gate set

- Contract gate: `tools/bringup/check26_contract.py`
- Compile gate: `avs/compiler/linx-llvm/tests/run.sh`
- Mnemonic coverage: `avs/compiler/linx-llvm/tests/analyze_coverage.py`
- Runtime suites: `avs/qemu/run_tests.sh --all`
- Strict runtime system gate: `avs/qemu/check_system_strict.sh`

## Execution order (runtime-first stabilization)

1. Run compile and coverage gates.
2. Run strict system gate.
3. Run full runtime suites.
4. Run Linux and libc runtime gates from their domain skills.

## Reproducibility contract

For every gate run, capture:
- command line,
- lane (`pin` or `external`),
- full SHA manifest,
- timestamp,
- outcome,
- artifact/log paths.

Treat this artifact as source-of-truth and render status docs from it.

## Common regressions

- Path resolution bug in `avs/qemu/run_tests.py` (`REPO_ROOT` synthesis).
- Green docs drift from live reruns.
- Runtime trap loops that require Linux/QEMU symbolication.

## Acceptance criteria

- `check26` passes.
- AVS compile suites pass.
- Mnemonic coverage is `100.0%` for `linx64` and `linx32`.
- `avs/qemu/run_tests.sh --all` runs all suites without root/path failures.

## References

- `references/gate_matrix.md`
