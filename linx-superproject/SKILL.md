---
name: linx-superproject
description: LinxISA superproject governance and cross-repo execution workflow. Use when managing submodule topology, dual-lane pin/external sync, AVS gate reproducibility, SHA manifest reporting, or workload matrix publication across llvm/qemu/linux/LinxCore/pyCircuit/glibc/musl.
---

# Linx Superproject

## Overview

Use this skill for root-level coordination in `/Users/zhoubot/linx-isa`: topology rules, lane sync, gate truth, and cross-stack reporting.

## Core policy (mandatory)

- Keep LinxISA links in root `.gitmodules` only.
- Keep no inter-leaf LinxISA submodule links.
- Keep a single in-repo source of truth; do not route work to external trees
  such as `/Users/zhoubot/qemu` or `/Users/zhoubot/linux`.
- Keep required submodules in sync:
  - `compiler/llvm`
  - `emulator/qemu`
  - `kernel/linux`
  - `rtl/LinxCore`
  - `tools/pyCircuit`
  - `lib/glibc`
  - `lib/musl`
  - `workloads/pto_kernels`
  - `skills/linx-skills`

## LinxCore maturity collaboration contract

- Canonical governance files:
  - `docs/bringup/agent_runs/manifest.yaml`
  - `docs/bringup/agent_runs/waivers.yaml`
  - `docs/bringup/gates/latest.json`
- Active phase is controlled by `manifest.phase_policy.active_phase` (G0..G5).
- Waivers are phase-bound and must include owner, issue, phase, and `expires_utc`.
- Required non-waived gates must pass in both `pin` and `external` lanes.
- Evidence pack per run must include:
  - canonical gate report row,
  - SHA manifest,
  - gate logs,
  - multi-agent summary JSON.

## Owner map for collaboration

- `arch`: architecture docs and contract lint gates.
- `linxcore`: RTL/cosim/superscalar gates.
- `testbench`: ROB/replay/verification gates.
- `pycircuit`: pyCircuit flow and interface-contract gates.
- `trace`: LinxTrace schema/compatibility/viewer-sync gates.
- `integration`: strict closure, performance floor, dual-lane parity.

## Canonical sync commands

```bash
git submodule sync --recursive
git submodule update --init --recursive
bash tools/ci/check_repo_layout.sh
```

## Canonical gate commands

PR tier strict closure:

```bash
LINX_GATE_TIER=pr RUN_EXTENDED_CROSS_GATES=1 \
bash /Users/zhoubot/linx-isa/tools/regression/strict_cross_repo.sh
```

Nightly tier strict closure:

```bash
LINX_GATE_TIER=nightly RUN_EXTENDED_CROSS_GATES=1 RUN_PERF_FLOOR_GATES=1 \
bash /Users/zhoubot/linx-isa/tools/regression/strict_cross_repo.sh
```

Dual-lane runtime convergence:

```bash
LINX_GATE_TIER=pr RUN_EXTENDED_CROSS_GATES=1 \
bash /Users/zhoubot/linx-isa/tools/bringup/run_runtime_convergence.sh --lane pin --run-id <run-id-pin>
LINX_GATE_TIER=pr RUN_EXTENDED_CROSS_GATES=1 \
bash /Users/zhoubot/linx-isa/tools/bringup/run_runtime_convergence.sh --lane external --run-id <run-id-ext>
```

## Dual-lane governance

- Pin lane: superproject submodule SHAs.
- External lane: active external trees.
- For pin-lane bring-up, prefer in-repo toolchain binaries from
  `compiler/llvm/build-linxisa-clang/bin`.
- Run same gate matrix on both lanes and publish side-by-side outcomes.

## Transcript lessons (2026-02-23)

- Treat `ebreak` as architectural breakpoint by default; semihost behavior must
  be explicit opt-in (`LINX_SEMIHOST=1`).
- Do not run `avs/qemu` suites in parallel against the same `avs/qemu/out`
  directory; shared build outputs can produce false undefined-symbol failures.
- Keep Linux timer diagnostics separate from parser failures: if `ctx_tq` fails
  with `irq0_delta=0`, capture `/proc/interrupts` and `/proc/stat` evidence
  before changing checklist status.
- Checklist status must be run-id backed, absolute-date stamped, and path-clean
  (no external tree evidence links).

## Gate truth contract

Always record for each gate:
- command,
- lane,
- SHA manifest,
- timestamp,
- pass/fail,
- artifact links.

Treat markdown status pages as generated views, not source-of-truth.

## Repin workflow discipline

1. Land module change with module-owned gates green.
2. Update submodule SHA in superproject.
3. Re-run PR strict closure with extended cross gates.
4. Merge repin only with green required gates and complete evidence.

## Included scope

This consolidated skill owns:
- AVS gate orchestration,
- submodule topology cleanup,
- workload matrix publishing (including TSVC).

## References

- `references/runbook.md`
- `../linx-isa/references/v0.3_contracts_and_asm.md` (ISA v0.3 stable contracts)
- `../linx-compiler/references/v0.3_codegen_and_asm_contracts.md` (LLVM parity focus)
- `../linx-ide/references/v0.3_qemu_trap_contracts.md` (QEMU parity focus)
