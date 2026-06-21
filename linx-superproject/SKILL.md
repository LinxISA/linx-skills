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
- `linx-core`: RTL/cosim/superscalar gates.
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

## Worktree Hygiene (single canonical checkout)

- For bring-up, keep a single canonical superproject folder: `/Users/zhoubot/linx-isa`.
- Avoid creating persistent `linx-isa-*` clones/worktrees under `/Users/zhoubot/`.

Audit and cleanup:

```bash
git -C /Users/zhoubot/linx-isa worktree list
git -C /Users/zhoubot/linx-isa worktree prune
```

If a worktree contains submodules, removal may require `--force`:

```bash
git -C /Users/zhoubot/linx-isa worktree remove --force <path>
git -C /Users/zhoubot/linx-isa worktree prune
```

## Skills sync policy (mandatory per bring-up cycle)

```bash
git -C /Users/zhoubot/linx-isa submodule update --init --recursive skills/linx-skills
git -C /Users/zhoubot/linx-isa/skills/linx-skills fetch origin main
git -C /Users/zhoubot/linx-isa/skills/linx-skills checkout origin/main

# Install/prune canonical skills into $CODEX_HOME/skills (defaults to $HOME/.codex/skills).
bash /Users/zhoubot/linx-isa/skills/linx-skills/scripts/install_canonical_skills.sh

python3 /Users/zhoubot/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py \
  --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main
```

- Start each superproject bring-up run from latest `skills/linx-skills`.
- Summarize skill deltas after bring-up and repin `skills/linx-skills` SHA.
- Use `$linx-skills-submodule` for safe, non-destructive skill maintenance.

## Tooling reliability (common)

- If `git fetch` fails with `LibreSSL SSL_connect: SSL_ERROR_SYSCALL`, force Git to HTTP/1.1:

```bash
git config http.version HTTP/1.1
# or per-submodule:
git -C tools/pyCircuit config http.version HTTP/1.1
```

- If `gh` GraphQL calls fail with `TLS handshake timeout` / `EOF`, retry with a larger timeout:

```bash
GH_HTTP_TIMEOUT=300 gh <command>
```

- `linx-isa` disallows merge commits; use squash merges:

```bash
gh pr merge <PR> --squash
```

## Skill evolve loop (mandatory closeout)

- Every module agent must run an explicit `update`/`no-update` decision at run closeout.
- Update skills only for material reusable findings:
  - new cross-module contract/invariant/gate,
  - new recurring triage workflow,
  - new mandatory reproducibility command/env/artifact.
- Skip skill updates for minor optimizations, wording, or one-off local workarounds.
- Require one evidence line per module in integration notes:
  - `skill-evolve: update ...` or `skill-evolve: no-update ...`.
- To avoid loops/churn, bundle material findings from a run into one skills update.

## Canonical gate commands

Retired public `0.3`/`0.4` guard scripts and historical compatibility wrappers
are not active gates. Use the canonical v0.56 checks directly:

```bash
python3 /Users/zhoubot/linx-isa/tools/isa/build_golden.py --profile v0.56 --check
python3 /Users/zhoubot/linx-isa/tools/isa/validate_spec.py --profile v0.56
python3 /Users/zhoubot/linx-isa/tools/isa/check_canonical_v056.py --root /Users/zhoubot/linx-isa
```

Keep CI/workflow names on `public-v056` surfaces.

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

Benchmark/QEMU/Linux hard-break flow:

```bash
python3 /Users/zhoubot/linx-isa/tools/bringup/run_benchmark_linux_flow.py --profile pr --dry-run
python3 /Users/zhoubot/linx-isa/tools/bringup/run_benchmark_linux_flow.py --profile pr --report-out /Users/zhoubot/linx-isa/workloads/generated/flow-pr/report.json
```

- Use this flow before TSVC, SPEC, or full benchmark work.
- Stop at the first red hard-break stage in the same lane; do not debug
  downstream Linux/rootfs/SPEC failures while ISA/compiler/QEMU/TSVC
  prerequisites are red.
- Put new benchmark artifacts under `workloads/generated/<run-id>/`, not
  ad-hoc `workloads/generated-*` sibling directories.

AI workload/QEMU/LinxCoreModel hard-break flow:

```bash
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile smoke --dry-run
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile smoke --run-id <run-id>
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile smoke \
  --run-id <run-id> --case avs-pto-parity-smoke --case avs-tile-smoke \
  --case supernpu-tileop_api
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TSub'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TSubs'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TAdds'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TAbs'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TCopyIn'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TCopyOut'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TCopy'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TReshape'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TTrans'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TPad'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TMul'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TMuls'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TMax'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TMaxs'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TAnd'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TOr'
```

- Use this flow to promote PTO and SuperNPUBench AI workloads from source
  contracts through in-repo Linx LLVM, Linx QEMU, and C++ `model/LinxCoreModel`.
- Unless `QEMU` or `QEMU_CLEAN_OUT_DIR` selects a matching clean build, the
  flow should prefer `emulator/qemu/build-linx/qemu-system-linx64`. Treat
  `emulator/qemu/build/qemu-system-linx64` as a legacy fallback that may be
  stale against current Linx direct-boot semantics.
- Direct-boot AI workload QEMU runs require `LINX_VIRT_TEST_FINISHER=1` so
  SuperNPUBench and AVS pass/fail MMIO writes become host-visible exits instead
  of long-running guest spins.
- Treat `workloads/generated/<run-id>/ai-bringup/report.json` as the
  machine-readable source of truth; `summary.md` is a generated human view.
- `--case <text>` is a substring selector. Use quoted exact selectors such as
  `--case '=supernpu-tileop_api-TSub'` when a case name is a prefix of another
  case, for example `TSub` versus `TSubs`.
- SuperNPUBench `PLAT=linx` cases are linked as direct-boot Linx ELFs with
  `_start` first at `0x10000`; preserve the generated linker script, objdump,
  raw bin, and compile logs as triage artifacts.
- Current SuperNPUBench Tier-0/Tier-1 direct-boot green cases are `MatMul`,
  `TAdd`, `TAbs`, `TCopyIn`, `TCopyOut`, `TCopy`, `TReshape`, `TTrans`,
  `TPad`, `TSub`, `TSubs`, `TAdds`, `TMul`, `TMuls`, `TMax`, `TMaxs`,
  `TAnd`, and `TOr`. `TAbs`, `TCopyIn`, `TCopyOut`, `TCopy`, `TReshape`,
  `TTrans`, `TPad`, `TSub`, `TSubs`, `TAdds`, `TMul`, `TMuls`, `TMax`,
  `TMaxs`, `TAnd`, and `TOr` are the first Tier-1 scalar
  arithmetic/logical/unary/data-movement promotions: each uses a
  `jcore/<op>.hpp` Linx scalar/direct-copy path and a bounded int64 direct-boot
  source branch, then must pass QEMU before `gfsim -f <elf>`. For `TReshape`,
  keep the bounded smoke shape aligned to the tile row-major byte contract, as
  in the current `4x8 -> 8x4` int64 case. For `TTrans`, keep the smoke square
  (`4x4` int64) unless the test source starts using distinct input/output tile
  shape parameters. For `TPad`, keep the Linx include path free of host-only
  headers such as `assert.h`; use static shape checks plus a bounded scalar
  pad loop in the direct-boot smoke instead of runtime `assert`/libc calls.
- AVS Tier-0 parity smoke is `avs-pto-parity-smoke`; it passes
  `-DPTO_PARITY_TLOAD_STORE_ONLY=1` through `avs/qemu/run_tests.py
  --extra-cflag` and runs only the PTO `tload_store` digest path. The full
  smoke-sized parity sequence remains `avs-pto-parity` in Tier 1 as a
  model-lane maturity packet when it does not exit within the selected timeout.
- AVS Tier-0 tile smoke uses the compile-smoke source override during QEMU
  execution to prove the PTO/QEMU/model handoff before the full tile runtime
  source is green. Keep these case-level smokes separate from model-build smoke.
- Model-build smoke must use the generated tiny ELF under `cases/_model/`
  unless `--model-smoke-elf` is explicitly provided; do not reuse an arbitrary
  QEMU-passing workload ELF as the global `gfsim` availability check.
- `--model-build-timeout` covers CMake configure/build only; `--model-timeout`
  covers `gfsim -f <elf>` smoke and workload execution.
- Use a targeted smoke selection such as `--case avs-pto-parity-smoke --case
  avs-tile-smoke --case supernpu-tileop_api` when you need a fast
  source-to-model green proof. Keep long full-parity ELFs in the PR/nightly
  report as model-lane maturity packets unless they naturally exit within the
  selected model timeout.
- First failing hard-break stage owns the fix lane:
  `benchmark`, `compiler`, `emulator`, `model`, or `docs-skills`.
- In SuperNPUBench compile logs, classify missing `*_Impl` tile API coverage,
  unsupported Linx tile runtime contracts (`__vbuf__`, `blkv_get_*`, boxed
  layout static asserts), and host-libc/soft-float direct-boot dependencies as
  `benchmark`; reserve `compiler` for true LLVM/backend/MC/link legality bugs
  after the workload source contract is valid for Linx direct boot.
- Failed cases emit bounded agent fix packets under
  `workloads/generated/<run-id>/ai-bringup/fix-packets/`.

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
- In recovery-forward-port runs, treat compiler/assembler compatibility
  failures as module-domain first, and do not use stale Linux/QEMU artifacts as
  closure evidence before rebuilding them with the refreshed in-repo toolchain.
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
5. If the module PR merged by squash/rebase and rewrote the submodule SHA,
   follow immediately with a gitlink-only superproject repoint so `main`
   references the merged upstream SHA rather than the earlier topic-branch tip.

## Included scope

This consolidated skill owns:
- AVS gate orchestration,
- submodule topology cleanup,
- workload matrix publishing (including TSVC).

## References

- `references/runbook.md`
- `../linx-isa/references/v0.3_contracts_and_asm.md` (archive-only historical baseline)
- `../linx-compiler/references/v0.3_codegen_and_asm_contracts.md` (archive-only historical baseline)
- `../linx-qemu/references/runtime_gates.md` (QEMU parity focus)
