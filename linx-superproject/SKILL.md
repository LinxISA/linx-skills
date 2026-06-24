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
  --run-id <run-id> --case '=supernpu-tileop_api-MatMacc'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-test_MatMul'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-test_MatMacc'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TSub'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TSubs'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TAdds'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TAdd_mask'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TDiv'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TDivs'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TRem'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TRecip'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TSqrt'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TExp'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TAbs'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TCI'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TExpandCol'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TExpandRow'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TExpandScalar'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TCopyIn'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TCopyOut'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TCopy'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TCvt'
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
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TCmp'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TRowSum'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TRowMax'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TRowSumExpand'
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile pr \
  --run-id <run-id> --case '=supernpu-tileop_api-TRowMaxExpand'
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
- For SuperNPUBench manifest rows with a generic `TESTCASE`, resolve concrete
  source files from `TYPE` first and keep the filesystem's actual case in source
  manifests. `kernel/gemm/matmul TESTCASE=matmul TYPE=HIF4_HIF4` resolves
  `src/HiF4_HiF4.cpp`; `TYPE=A16W4` resolves `src/A16W4.cpp`.
- Treat SuperNPUBench `compile.all` as a machine-readable case manifest for the
  AI flow. Keep rows as concrete `make` commands with expanded values; shell
  loops or literals such as `${num_col}` and `${debug}` create benchmark-owned
  source-contract failures because the runner reads `make` rows literally.
- Current SuperNPUBench Tier-0/Tier-1 direct-boot green cases are `MatMul`,
  `MatMul_e4m3`, `MatMacc`, `test_MatMul`, `test_MatMacc`, `TAdd`, `TAbs`,
  `TCI`, `TCopyIn`,
  `TCopyOut`, `TCopy`, `TCvt`, `TReshape`, `TExpandCol`, `TExpandRow`,
  `TExpandScalar`, `TTrans`, `TPad`, `TSub`, `TSubs`, `TAdd_mask`, `TAdds`,
  `TDiv`, `TDivs`, `TExp`, `TRem`, `TRecip`, `TSqrt`, `TMul`, `TMuls`, `TMax`,
  `TMaxs`, `TAnd`, `TOr`, `TCmp`, `TRowSum`, `TRowMax`, `TRowSumExpand`,
  `TRowMaxExpand`, and `kernel/control hashtable_lookup_simt`.
  `hashtable_lookup_simt` currently has two bounded `kNum=16` embedded-data
  direct smokes over the generated 2048-entry table: `LINX_HT_SCAN=1` for the
  linear-scan fallback and a no-scan MurmurHash3 initial-slot plus linear-probe
  path. The hash/probe row must stay promoted through QEMU and `gfsim` as the
  regression for C++ model `SRLW`/`SRLIW` low32, 5-bit shift, sign-extended
  result semantics. Keep only these `kNum=16` `FOR_GFSIM` rows in Tier 1; the
  `kNum=6144` SIMT rows and SIMD `NUM_COL=256/512/1024` rows are Tier 2 until
  their large/debug source contracts are adapted for Linx direct boot.
  For `kernel/control` data-object cases, keep output object paths under
  `$(OBJ_ROOT)/kernel/control/...` and give generated `.o` targets explicit
  no-op recipes after the data-object builder runs; otherwise Make may rebuild
  generated `.s` files with a host/default assembler when the AI runner
  redirects `OBJ_ROOT`.
  `MatMacc`, `test_MatMul`, `test_MatMacc`, `TAbs`, `TCI`, `TExpandCol`,
  `TExpandRow`, `TExpandScalar`, `TCopyIn`, `TCopyOut`, `TCopy`, `TCvt`,
  `TReshape`, `TTrans`, `TPad`, `TSub`, `TSubs`, `TAdd_mask`, `TAdds`, `TDiv`,
  `TDivs`, `TExp`, `TRem`, `TRecip`, `TSqrt`, `TMul`, `TMuls`, `TMax`, `TMaxs`,
  `TAnd`, `TOr`, `TCmp`, `TRowSum`, `TRowMax`, `TRowSumExpand`, and
  `TRowMaxExpand` are the first Tier-1 scalar
  arithmetic/logical/compare/unary/data-movement/reduction promotions: each uses a
  `jcore/<op>.hpp` Linx scalar/direct-copy path and a bounded integer direct-boot
  source branch, then must pass QEMU before `gfsim -f <elf>`. For `MatMacc`,
  keep direct smoke at `4x4` int64 row-major multiply-accumulate with nonzero
  initial C tile values; col-major MatMacc currently has QEMU-pass/model-fail
  evidence and belongs in the model lane before promotion. For `test_MatMul`,
  keep direct smoke at `4x4` int64 row-major MATMUL; the original
  TileLeft/TileRight/TileAcc plus TCVT float path remains deferred until the
  Linx direct-boot model lane supports that runtime contract. For
  `test_MatMacc`, keep direct smoke at `4x4` int64 row-major MATMUL+MATMACC;
  the original TileLeft/TileRight/TileAcc plus TCVT float path remains
  deferred on the same model-lane runtime contract. For `MatMul_e4m3`, keep the
  original FP8 e4m3 conversion, TileLeft/TileRight inputs, TileAcc output, and
  vector-kernel conversion contract for non-Linx builds, but use a source-local
  `4x4` int64 MATMUL direct-boot smoke under `__linx` until boxed, ACC, and FP8
  runtime support is available. Keep this smoke in both `tileop_api` and
  `other/tileop_api`; do not collapse it into the existing `MatMul` source,
  because the manifests must remain individually promotable. For `TReshape`,
  keep the bounded smoke shape aligned to the tile row-major byte contract, as
  in the current `4x8 -> 8x4` int64 case. For `TTrans`, keep the smoke square
  (`4x4` int64) unless the test source starts using distinct input/output tile
  shape parameters. For `TPad`, keep the Linx include path free of host-only
  headers such as `assert.h`; use static shape checks plus a bounded scalar
  pad loop in the direct-boot smoke instead of runtime `assert`/libc calls.
  For `TCI`, keep the smoke `8x8` int32: unboxed row-major tiles require
  `Cols * bits` to be 32-byte aligned, and unboxed col-major tiles require
  `Rows * bits` to be 32-byte aligned. For `TExpandScalar`, keep the smoke
  `4x8` int64 so row-major `Cols * bits` and col-major `Rows * bits` both
  satisfy the same unboxed tile byte-alignment rule. For `TExpandRow` and
  `TExpandCol`, use the same `4x8` int64 smoke shape and cover both row-major
  and col-major expansion paths in the direct-boot branch. For `TCvt`, keep
  the direct smoke at `16x16` int64, fill tile storage directly instead of
  using `TCOPYIN`/`TCOPYOUT` on boxed tiles, and verify row-major, col-major,
  NZ, and ZN round-trips before returning success. For `TRowSum` and
  `TRowMax`, use a `4x8` int64 direct-boot branch, keep the output tile
  `ValidCol == 1`, and cover both row-major and col-major row reductions before
  promotion. For `TRowSumExpand` and `TRowMaxExpand`, use the same `4x8` int64
  direct-boot branch, keep the full output tile shape, and fill every column in
  each row with that row's reduction value. If Clang lowers a direct-boot tile
  copy/zeroing operation to `memcpy` or `memset`, keep the helper source-local
  and freestanding under `__linx`; do not pull in host libc or relax the
  `-nostdlib` link. For `TCmp`, keep the direct smoke at `8x8` so row-major and
  col-major int32 output tiles both satisfy the unboxed 32-byte alignment rule;
  cover int64 row/col comparisons plus int32 `EQ`, and defer float/half
  direct-boot comparison until soft-float/runtime evidence exists. For
  `TAdd_mask`, use a `6x6` int64 global shape over a `4x4` tile to exercise the
  full tile plus trailing-row, trailing-column, and corner paths without
  violating the row-major unboxed 32-byte tile alignment rule. For `TDiv`, keep
  the direct smoke at `4x4` int64 and cover both row-major and col-major tiles
  with nonzero denominators; this proves scalar Linx `div` lowering through
  QEMU and `gfsim` without depending on soft-float or compiler-rt helpers. For
  `TDivs`, use the same `4x4` int64 row/col smoke with a nonzero scalar
  denominator so the case proves scalar-divisor lowering without vector-kernel
  scalar-register writes. For `TRem`, keep direct smoke at `8x8` int32 and
  cover both row-major and col-major tiles with nonzero denominators; this
  proves scalar Linx `remw` lowering through QEMU and `gfsim` without
  soft-float/compiler-rt dependencies. For `TRecip`, keep direct smoke at
  `4x4` int64, fill row-major and col-major tile storage directly, and verify
  reciprocal results before the finisher; model-only failures around the
  compiler's reciprocal lowering are commonly scalar `csel`/`psel` semantics.
  For `TSqrt`, keep direct smoke at `4x4` int64 perfect squares and use the
  bounded comparison-ladder helper in the Linx-only path; unbounded integer
  sqrt loops can expose current model loop/divergence limitations, and broader
  integer or floating-point sqrt belongs in a later model-backed promotion. For
  `TExp`, keep direct smoke at `4x4` int64 rounded-exp values and use a
  comparison-ladder helper in the Linx-only path; compiler-generated constant
  lookup tables for the same bounded values have QEMU-pass/model-timeout
  evidence, and float/half exponential belongs in a later model-backed
  promotion. Keep `other/tileop_test` and non-control `kernel/*` suites in
  Tier 2 until their larger shape/source contracts are individually promoted;
  keep `kernel/fusion*` rows in Tier 3 because they are model-oriented
  long-shape workloads.
- SuperNPUBench `kernel/gemm/matmul` MX cases `TYPE=A16W4` and
  `TYPE=HIF4_HIF4` currently pass source discovery/model-build smoke, then stop
  at compiler-contract with benchmark-owned evidence because their full MX path
  still depends on vector-only `template_asm.h` `Tr` constraints and
  `blkv_get_*` launch helpers. Do not classify these as compiler/QEMU/model
  bugs until the benchmark has a valid Linx direct-boot MX API contract.
- AVS Tier-0 parity smoke is `avs-pto-parity-smoke`; it passes
  `-DPTO_PARITY_TLOAD_STORE_ONLY=1` through `avs/qemu/run_tests.py
  --extra-cflag` and runs only the PTO `tload_store` digest path. The full
  smoke-sized parity sequence remains `avs-pto-parity` in Tier 1 as a
  model-lane maturity packet when it does not exit within the selected timeout.
  Non-skipped model builds configure `model/LinxCoreModel/bin/gfsim` with
  `-DOPT_LEVEL=O3 -DDISABLE_DEBUG_SYMBOLS=ON` so PR/nightly workload probes use
  the optimized bring-up binary.
  `avs-pto-parity-prefix-gemm-performance` is the fast Tier-1 model-green
  prefix boundary; it uses `PTO_PARITY_FAST_F32_SEED=1`,
  `PTO_PARITY_FAST_FP16_SEED=1`, and
  `PTO_PARITY_STOP_AFTER_STAGE=PTO_PARITY_STAGE_GEMM_PERFORMANCE` to stop after
  the GEMM prefix. `avs-pto-parity-prefix-flash-attention` is the deeper
  Tier-1 model-green prefix; it stops after
  `PTO_PARITY_STAGE_FLASH_ATTENTION` and proves source, compiler, QEMU, and
  `gfsim` through the `flash_attention` digest and pass finisher.
  `avs-pto-parity-prefix-flash-attention-softmax` is the current model-green
  softmax-prefix micro-profile; it stops after
  `PTO_PARITY_STAGE_FLASH_ATTENTION_SOFTMAX` and passes
  `PTO_ATTENTION_SMOKE_SEQ=1`, `PTO_ATTENTION_LARGE_SMOKE_SEQ=1`,
  `PTO_ATTENTION_SMOKE_QD=1`, `PTO_ATTENTION_SMOKE_VD=1`,
  `PTO_ATTENTION_SMALL_SMOKE_QD=1`, `PTO_FLASH_TILE_M=1`, and
  `PTO_FLASH_TILE_K=1` through the AVS extra-cflag hook. Keep these as prefix
  proofs/probes, not substitutes for full `avs-pto-parity` closure.
  `avs-pto-parity-prefix-flash-attention-masked` is the next model-green
  micro-profile; it stops after `PTO_PARITY_STAGE_FLASH_ATTENTION_MASKED` and
  also passes `PTO_ATTENTION_MASKED_SMOKE_SEQ=1`,
  `PTO_ATTENTION_MASKED_SMOKE_QD=1`, and
  `PTO_ATTENTION_MASKED_SMOKE_VD=1` through the AVS extra-cflag hook.
  `avs-pto-parity-prefix-fa-performance` reuses the same 1x attention
  micro-profile, stops after `PTO_PARITY_STAGE_FA_PERFORMANCE`, and proves the
  `fa_performance` digest under QEMU and `gfsim`.
  `avs-pto-parity-prefix-mla-attention` reuses that profile, stops after
  `PTO_PARITY_STAGE_MLA_ATTENTION`, and proves the `mla_attention` digest under
  QEMU and plain `gfsim -f <elf>`. Earlier full-shape softmax-prefix probes
  passed QEMU but timed out in
  `flash_attention_demo_f32` soft-float helper code; classify similar
  QEMU-passing full-shape timeouts as model-owned unless static legality
  evidence proves otherwise. Prior `tanh`/`softmax` BFU failures were model
  local-pipe lifetime and RAS speculative write-slot issues, not benchmark or
  compiler failures.
  AVS compiler-pass rows should preserve objdump disassembly, symbol, section,
  and relocation sidecars for `linx-qemu-tests.elf`; model timeout/crash rows
  should add `uart_tail`/`uart_count` breadcrumbs plus a
  `last_brob_bpc_disasm` window when the log exposes a latest BROB BPC. Use the
  UART marker to confirm source-stage progress and the BPC-to-objdump linkage
  before changing benchmark or compiler code for QEMU-passing AVS parity
  failures.
- PTO catalog smoke promotion currently covers `pto-kernel-tload_store`,
  `pto-kernel-gemm`, `pto-kernel-gemm_basic`, `pto-kernel-gemm_demo`,
  `pto-kernel-gemm_performance`, `pto-kernel-mamulb`,
  `pto-kernel-tmatmul_acc`, `pto-kernel-relu_fp32`, and
  `pto-kernel-add_custom` in Tier 1, plus Tier-2 layout cases
  `pto-kernel-flatten_fp32`, `pto-kernel-reshape_fp32`,
  `pto-kernel-squeeze_fp32`, `pto-kernel-unsqueeze_fp32`,
  `pto-kernel-concat_fp32`, `pto-kernel-split_fp32`,
  `pto-kernel-stack_fp32`, `pto-kernel-permute_nhwc_nchw_fp32`, and
  `pto-kernel-transpose_large_fp32`, and Tier-2 indexing cases
  `pto-kernel-slice_fp32`, `pto-kernel-gather_fp32`,
  `pto-kernel-scatter_fp32`, `pto-kernel-where_fp32`,
  `pto-kernel-argmax_fp32`, `pto-kernel-unique_i32`,
  `pto-kernel-hash_table_insert_fp32`,
  `pto-kernel-hash_table_lookup_fp32`, and
  `pto-kernel-unsorted_segment_sum_fp32`. Use `--tier 2` with `--profile pr` when targeting
  the Tier-2 cases directly. The AI flow
  generates explicit per-case harnesses, compiles each matching source with
  `-DPTO_QEMU_SMOKE=1`, emits standalone Linx ELFs plus objdump/raw-bin
  artifacts, then runs each ELF in QEMU and only then `gfsim -f <elf>`.
  `pto-kernel-add_custom` is promoted with a harness-local freestanding
  `__addsf3` helper scoped to the positive integer-valued smoke inputs seeded
  by the oracle. Its oracle-side `f32_bits_from_u32` must keep the exact
  small-value table for the current smoke range; without that table, `gfsim`
  can time out in harness-only bit-scan conversion loops even though QEMU
  passes. Keep the table local to `add_custom`; do not move it into shared GEMM
  copy harnesses without rerunning `pto-kernel-gemm_basic` and
  `pto-kernel-gemm_demo`, because the generated `.rodata` access pattern is
  part of the model evidence. `pto-kernel-unsorted_segment_sum_fp32` uses the
  same scoped helper for positive integer-valued smoke additions. Do not
  generalize either helper into a compiler-rt substitute.
  `pto-kernel-gemm_basic`, `pto-kernel-gemm_demo`, and
  `pto-kernel-gemm_performance` are promoted only through their
  `PTO_QEMU_SMOKE` float bit-pattern copy-oracle branches; `gemm_performance`
  keeps `repeat_tiles=3` and verifies the final repeat through a precomputed
  expected-bit table, avoiding model-side oracle arithmetic as the success
  criterion. Do not count these as full float TMATMUL/TCVT/TMULS coverage. Keep
  every other non-promoted `pto_kernel` catalog entry source/compile/static
  until it has an ABI-specific harness, oracle, and QEMU-to-model evidence.
- `pto-kernel-gemm_reuse_a_fp16`, `pto-kernel-gemm_reuse_b_fp16`, and
  `pto-kernel-gemm_reuse_ab_fp16` have direct-boot FP16 storage harnesses with
  harness-local positive-integer `__mulsf3`/`__addsf3` shims. They are promoted
  at the default `PTO_QEMU_SMOKE=1` 16x16x16 shape and pass source, compiler,
  QEMU, and `gfsim -f <elf>` when the AI flow uses `--model-timeout 600`.
  Earlier model-fail packets around these cases were closed by the BlockISA
  `store_si3` PR/PO decode fix plus LSU/local-link wakeup fixes; do not regress
  them by replacing the workload with a smaller shape. The PTO sources expose
  `PTO_QEMU_SMOKE_DIM` only as a controlled future probe hook.
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
- For model-lane scalar/vector select mismatches after QEMU pass, verify the
  `csel`/`psel` contract before changing benchmark or compiler code:
  `SrcP != 0` selects `SrcR`; `SrcP == 0` selects `SrcL`, matching
  Linx LLVM/QEMU.
- In SuperNPUBench compile logs, classify missing `*_Impl` tile API coverage,
  unsupported Linx tile runtime contracts (`__vbuf__`, `blkv_get_*`, `Tr` asm
  constraints, boxed layout static asserts, MATMUL unboxed/ACC static asserts), and
  host-libc/soft-float direct-boot dependencies as `benchmark`; reserve
  `compiler` for true LLVM/backend/MC/link legality bugs after the workload
  source contract is valid for Linx direct boot.
- If a SuperNPUBench `make` command exits successfully but the AI flow cannot
  find the expected ELF, inspect the compile log before assigning compiler
  ownership. Stale data-object assembly paths that still target `linx64v5`, or
  source manifests that still require missing benchmark-only headers such as
  `benchmark.h`, are benchmark/source-contract failures.
- For SuperNPUBench data-object cases, keep generated data/object packaging in
  the benchmark lane until it uses the current `COMPILER_DIR` with
  `linx64-linx-none-elf`, writes object artifacts under the run's `OBJ_ROOT`,
  links `EXTRA_OBJ_FILES`, and ignores regenerated `.data`/`.bin` inputs. Only
  after that packaging is valid should `Tr`/`blkv_get_*` errors be treated as
  the next unsupported Linx tile runtime contract.
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
