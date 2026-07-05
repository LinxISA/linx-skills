---
name: linx-qemu
description: Linx emulator development workflow for submodule `emulator/qemu`. Use when implementing or debugging decode/execute behavior, trap and interrupt handling, MMU and device interactions, or AVS runtime/system regressions where emulator behavior is the likely first divergence.
---

# Linx QEMU

## Overview

Use this skill for emulator-focused work in `emulator/qemu` and for runtime failures where QEMU is the likely first divergence point.

## Target lines

Keep the active QEMU line explicit before making changes:

- Current/modern line may expose `linx64-softmmu` in the in-repo build tree.
- For current LinxISA superproject bring-up, prefer
  `/Users/zhoubot/linx-isa/emulator/qemu/build-linx/qemu-system-linx64` when
  it exists. Use `QEMU` or `QEMU_CLEAN_OUT_DIR` only when intentionally testing
  another matching build. The older `emulator/qemu/build/qemu-system-linx64`
  path can be a stale legacy fallback.
- Recovered historical lines can instead expose:
  - `linx-softmmu`
  - `linx-linux-user`
  - `linx_be-linux-user`

Do not assume the target naming surface. Read `configs/targets/` first and use
the names that actually exist in the checked-out branch.

For the merged current recovery lane, direct kernel/rootfs runs are
firmwareless by default. Preserve `-bios none` in local reproductions unless a
specific firmware blob is intentionally under test.

For direct-boot AVS and SuperNPUBench AI workload runs, set
`LINX_VIRT_TEST_FINISHER=1` unless intentionally debugging guest-side spins.
That env makes test finisher MMIO writes report pass/fail to the host instead
of relying on timeout behavior.

QEMU linux-user mode is a separate process ABI lane. Use it only when the
checked-out or recovered QEMU tree actually provides a `qemu-linx` binary; the
current canonical checked-in target list may still expose only softmmu targets.
The reusable smoke form is:

```bash
python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py \
  --mode phase-b \
  --link static \
  --runner user \
  --qemu-user /Users/zhoubot/linx-isa/emulator/qemu/build-user/qemu-linx
python3 /Users/zhoubot/linx-isa/avs/qemu/run_glibc_smoke.py \
  --runner user \
  --qemu-user /Users/zhoubot/linx-isa/emulator/qemu/build-user/qemu-linx
```

This invokes `qemu-linx -L <sysroot> <elf>` and should be treated as a fast
pre-rootfs check for ELF startup, libc syscalls, and linux-user dispatch. It
does not replace `qemu-system-linx64` kernel/initramfs or full-OS gates.

## Historical recovery lane

When the user provides a recovered full patch and says it is the authoritative
latest implementation, treat that as a separate recovery workflow rather than a
normal forward-port.

- Prefer finding an old upstream QEMU base that fits the patch over manually
  replaying selected hunks onto a newer branch.
- In this workspace, the recovered `my.patch`-style Linx tree matched best
  against an upstream `v7.0.0` base.
- If you must configure `linx-linux-user` on a non-Linux host during recovery,
  any host-policy relaxations in `configure` / `meson.build` are host bring-up
  adaptations, not ISA or emulator semantic changes.
- If the recovered tree references `pc-bios/LinxInit.bin` but the firmware blob
  is unavailable, prefer making that blob optional for local configure/build
  validation instead of pretending to have reconstructed it.

## Required gates

```bash
bash /Users/zhoubot/linx-isa/avs/qemu/check_system_strict.sh
bash /Users/zhoubot/linx-isa/avs/qemu/run_tests.sh --all --timeout 10
python3 /Users/zhoubot/linx-isa/avs/qemu/run_callret_contract.py
python3 /Users/zhoubot/linx-isa/tools/bringup/check_qemu_opcode_meta_sync.py --qemu-root /Users/zhoubot/linx-isa/emulator/qemu --allowlist /Users/zhoubot/linx-isa/docs/bringup/qemu_opcode_sync_allowlist.json --report-out /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_opcode_sync_latest.json --out-md /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_opcode_sync_latest.md
python3 /Users/zhoubot/linx-isa/tools/bringup/report_qemu_isa_coverage.py --spec /Users/zhoubot/linx-isa/isa/v0.56/linxisa-v0.56.json --qemu-meta /Users/zhoubot/linx-isa/emulator/qemu/target/linx/linx_opcode_meta_gen.h --report-out /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_isa_coverage_latest.json --out-md /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_isa_coverage_latest.md
```

Coverage and opcode-sync gates must target the live v0.56 catalog. Treat any
`isa/v0.3` or `isa/v0.4` coverage command as archive-only unless explicitly
running a historical comparison.

## Incremental build policy

- Prefer a fresh out-of-tree local build when the checked-in `build/` tree
  drifts across upstream Meson option schema changes.
- Current recovered QEMU uses `configure` passthrough options rather than the
  older `--with-git-submodules=ignore` form. A known-good local rebuild form is:

```bash
mkdir -p /tmp/linx-qemu-local-build
cd /tmp/linx-qemu-local-build
/Users/zhoubot/linx-isa/emulator/qemu/configure \
  --target-list=linx64-softmmu \
  --enable-plugins \
  --disable-docs \
  --disable-werror \
  --disable-install-blobs
ninja qemu-system-linx64
```

- Reuse that build directory for incremental semantic/debug iterations once it
  configures successfully.

## Workflow

1. Reproduce with the smallest AVS case.
2. If the failure is in AVS compile or object generation, first decide whether
   the blocker belongs to the compiler surface rather than QEMU semantics.
   In particular, old Linx AVS cases that still use `%tpcrel_hi/%tpcrel_lo`,
   unfused symbolic `BSTART CALL`, or legacy block-attribute syntax should not
   be treated as emulator regressions until the in-repo `clang` integrated
   assembler accepts them.
3. For Linux userspace/runtime failures, try the linux-user process smoke first
   if `qemu-linx` exists. A user-mode pass narrows later failures to
   kernel/rootfs/system integration; a user-mode fail keeps the first
   divergence in ELF startup, syscall, or linux-user QEMU dispatch.
4. Capture the first wrong architectural event (`pc`, opcode, trap/irq cause, memory side-effect).
5. Only if needed, add targeted QEMU tracing around the suspicious PC or first wrong event; do not start tracing from reset/boot by default.
6. Compare against ISA semantics and expected Linux/runtime behavior.
7. If the first divergence only appears on positive direct-call or call/ret
   runtime cases using 64-bit `L.BSTART.*` headers, verify whether the raw
   immediate decode is still in halfword units before `linx_pcrel_target()`
   shifts it into a byte offset.
8. Patch decode/execute or exception path and add a focused regression.
9. Re-run runtime and system strict gates.

For recovered historical lines, insert one extra step before implementation:

1. Pick and validate the old base first.
2. Apply the recovered patch whole if possible.
3. Only then start conflict resolution or branch-local build adaptation.

## Trace policy

- Do not generate full-run QEMU traces from the beginning of execution unless no narrower reproducer exists.
- First localize the suspicious `pc`/opcode/window from AVS output, guest state, or a smaller repro, then enable trace only near that window.
- For hosted user-fault bring-up, prefer the opt-in `LINX_FAULT_TRACE=1`
  path before adding new trace code. Narrow it with
  `LINX_FAULT_TRACE_PC_LO`/`LINX_FAULT_TRACE_PC_HI` or
  `LINX_FAULT_TRACE_COUNT_LO`/`LINX_FAULT_TRACE_COUNT_HI`, and cap output with
  `LINX_FAULT_TRACE_LIMIT` when possible.
- For wrong runtime instruction bytes, pair a narrow TLB-fill trace with
  PC-watch virtual and physical byte dumps before changing decode. A reusable
  shape is `LINX_TLB_FILL_TRACE_VA=<va>`,
  `LINX_DEBUG_PC_WATCH=<pc>`,
  `LINX_DEBUG_PC_WATCH_DUMP_CODE_BYTES=<n>`, and
  `LINX_DEBUG_PC_WATCH_DUMP_PHYS=1`. If virtual bytes and physical bytes agree
  but disagree with the ELF file offset that should back that VA, treat QEMU as
  following the installed PTE and route the blocker to Linux file
  mapping/page-cache/VMA triage.
- For SPEC userspace-trap PC-watch packets, require the runner's
  `qemu_debug_env` JSON field in the evidence so the exact heartbeat,
  fault-trace, and PC-watch knobs are reproducible. Keep watch sets minimal:
  broad multi-window PC-watch can perturb row timing enough to change a
  userspace trap into a kernel live-timeout. `LINX_DEBUG_PC_WATCH_RING=1` is
  useful when the terminal fault is on a watched PC, but signal paths can still
  end without `LINX_PC_WATCH_RING` output; in that case use printed
  `linx_pc_watch:` / `LINX_PC_WATCH_REGS` hit lines as authoritative evidence
  and narrow the next repro toward the producer/caller path instead of widening
  the trace.
- For SPEC live-timeout throughput triage, use the SPEC runner switch
  `--qemu-tlb-stats` or `LINX_SPEC_QEMU_TLB_STATS=1` before enabling full
  `LINX_TLB_TRACE=1`. The switch sets `LINX_QEMU_TLB_STATS=1`; QEMU appends
  `tlbi_iall`, `tlbi_ia`, `tlbi_iv`, `tlbi_iav`, and last-invalidation
  PC/BPC/operand/ACR fields to `LINX_HEARTBEAT` without enabling the
  experimental MMU cache. The SPEC runner records these fields under
  `heartbeat_tlb_invalidation` and prints compact `tlbi=` liveness tags. Use
  this to separate startup/fault-path invalidation pressure from steady-state
  benchmark execution before changing QEMU TLB behavior.
- For SPEC demand page-walk attribution, use `LINX_QEMU_TLB_FILL_STATS=1`
  before enabling full `LINX_QEMU_TLB_FILL_TRACE=1`. The fill-stats path adds
  `tlbf_total`, fetch/load/store/probe/ok/fault counts, user/kernel/other
  MMU-index splits, and last-fill PC/BPC/VA/PA/access/MMU/prot/cause/ACR
  fields to `LINX_HEARTBEAT`; the SPEC runner records them under
  `heartbeat_tlb_fill` and prints compact `tlbf=` liveness tags in matrix
  markdown. Use full fill traces only after the aggregate counters identify a
  row/window worth narrowing.
- For SPEC page-walk cache experiments, do not treat QEMU's `tlb_set_page`
  `size` argument as multi-page lookup coverage. Upstream cputlb still
  materializes one `TARGET_PAGE_SIZE` entry and uses larger sizes only for
  invalidation bookkeeping. If Linx large block mappings are the target, keep
  the generic soft-TLB page-granular and test the opt-in block-aware page-walk
  result cache via the SPEC runner switches `--qemu-mmu-cache` and
  `--qemu-mmu-cache-stats` (or their `LINX_QEMU_MMU_CACHE=1` /
  `LINX_QEMU_MMU_CACHE_STATS=1` env equivalents); use the runner's
  `heartbeat_mmu_cache` / `mmuc=` fields to prove hit/miss/fill behavior before
  promoting it. On 2026-07-05, focused `505.mcf_r` train improved from
  `41000000005` to `45000000003` bounded instructions in 180s with
  `mmuc_hit=122234545`, while strict `999.specrand_ir` passed with the new
  switches; keep the cache opt-in until all-row train evidence is green.
- For long live-timeout rows where aggregate fill volume is high but full fill
  trace output would be too large, add `LINX_QEMU_TLB_FILL_HOT=1` alongside
  `LINX_QEMU_TLB_FILL_STATS=1`. QEMU emits `LINX_TLB_FILL_HOT` heartbeat
  companion lines with a small hot-page sketch; the SPEC runner records
  `heartbeat_tlb_fill_hot` and prints compact `tlbf-hot=` tags with the
  hottest page/access/MMU tuple and eviction pressure.
- For SPEC rows or post-start profiles where `helper_linx_tlb_iv` is hot, add
  `LINX_QEMU_TLB_INV_HOT=1` or the SPEC runner switch `--qemu-tlb-inv-hot`
  alongside `--qemu-tlb-stats` before changing QEMU cputlb behavior. QEMU emits
  `LINX_TLB_INV_HOT` heartbeat companion lines keyed by invalidation op and
  source PC, with last BPC/operand/page/ACR plus per-heartbeat deltas. The SPEC
  runner records `heartbeat_tlb_inv_hot` and prints compact `tlbi-hot=` tags.
  If the hot source is in Linx Linux `update_mmu_cache_range()` or
  `ptep_set_wrprotect()`, route the next speed loop to Linux flush frequency or
  batching before retrying QEMU MMU-index narrowing.
- For SPEC frame-template attribution, use `LINX_QEMU_FRAME_STATS=1` or the
  SPEC runner's `--qemu-frame-stats` before enabling full `LINX_FENTRY_TRACE`
  / `LINX_FRET_STK_TRACE`. QEMU appends `fr_` counters to `LINX_HEARTBEAT`,
  and the SPEC runner records them under `heartbeat_frame_stats`. Use this to
  rule frame fallback stores or return-cache misses in/out before reopening
  frame-store, restore-load, or BSTART return-target experiments.
- When aggregate `fr_` counters show frame-template traffic but do not identify
  the hot shape, add `LINX_QEMU_FRAME_SHAPE_HOT=1` or the SPEC runner switch
  `--qemu-frame-shape-hot`. QEMU emits `LINX_FRAME_SHAPE_HOT` companion lines
  with the hottest frame kind, register range, register count, stack size,
  count/delta, and eviction pressure; the SPEC runners record
  `heartbeat_frame_shape_hot` and matrix markdown prints `frame-hot=` tags. On
  2026-07-05, focused `541.leela_r` train showed the dominant shape was a
  one-register stack-32 `FENTRY`/`FRET.STK` pair, so future template-helper
  speed prototypes should specialize concrete shapes like that before adding
  broader frame-helper machinery.
- For one-register frame-template speed experiments, use
  `LINX_QEMU_FRAME_SINGLE_REG_FAST=1` or the SPEC runner switch
  `--qemu-frame-single-reg-fast`. The path is default-off, applies only to
  valid one-register `FENTRY`/`FRET.STK` shapes, and keeps frame trace modes on
  the generic implementation. Pair it with `--qemu-frame-stats` so
  `fr_single_fast_fentry` and `fr_single_fast_fret_stk` prove usage. On
  2026-07-05, focused `541.leela_r` train improved from `5500000007` to
  `5900000001` bounded instructions in the fine-heartbeat 45s shape while
  strict `999.specrand_ir` and call/ret contract gates passed. The same day,
  clean-build train-all evidence under
  `workloads/generated/specint-train-all-frame-single-fast-clean-qemu-20260705-r1/`
  kept `999.specrand_ir` passing and all other rows live-progressing, but the
  timeout-normalized result was mixed: `520`, `523`, `525`, and `541` improved,
  `531` was roughly flat, and `500`, `505`, and `557` regressed versus the
  prior clean ledger. Keep it opt-in/default-off and use it only for focused
  one-register frame-shape experiments until row-specific regressions are
  understood.
- For SPEC frame restore-load experiments, keep
  `LINX_QEMU_FRAME_RESTORE_HOST_LOAD=1` / `LINX_FRAME_RESTORE_HOST_LOAD=1`
  opt-in and normally drive it through the SPEC runner's
  `--qemu-frame-restore-host-load` or
  `LINX_SPEC_QEMU_FRAME_RESTORE_HOST_LOAD=1`. The fast path uses a
  same-page, non-faulting host-pointer hit probe for restore slots and falls
  back to the existing faulting load on misses. Use it only with
  `--qemu-frame-stats` so `fr_restore_host` and `fr_restore_fallback` prove
  whether the run actually used the path. As of 2026-07-04 it improved a
  focused `531.deepsjeng_r` train sample but did not close the all-row train
  gate and does not replace the data-memory/TLB lane for `505`.
- For SPEC frame-template dispatch experiments, keep
  `LINX_QEMU_TEMPLATE_CHAIN=1` opt-in until an all-row train comparison proves
  it. The 2026-07-04 focused `523.xalancbmk_r` probe with
  `LINX_QEMU_MMU_CACHE=1` improved the 120-second count from 16B to 22B
  instructions while preserving call/ret and 999 sentinels, but broad promotion
  still needs train-all evidence. Use it as a dispatch/helper-exit probe after
  frame/TB stats or a post-start host profile points at template helper exits,
  `tb_lookup`, `qht_lookup_custom`, or `pthread_jit_write_protect_np`.
- For SPEC TCG dispatch/cache-pressure attribution, use
  `LINX_QEMU_TB_STATS=1` or the SPEC runner's `--qemu-tb-stats` before changing
  TCG `tb-size`, cache policy, or dispatch behavior. QEMU appends `tbs_`
  counters to `LINX_HEARTBEAT`, and the SPEC runner records them under
  `heartbeat_tb_stats`. Use this after host profiles implicate
  `cpu_tb_exec`, `pthread_jit_write_protect_np`, or TB lookup/codegen pressure.
  The 2026-07-03 focused `505.mcf_r` probe had `tbs_flush=0`, stable
  miss/generation counts, and only about 36 MiB of roughly 1 GiB code-buffer
  use, so larger TB cache was rejected; route similar evidence toward per-TB
  dispatch/JIT transition and soft-MMU lookup work instead. A simple
  per-thread TLS guard around `qemu_thread_jit_execute()` /
  `qemu_thread_jit_write()` was also rejected on 2026-07-03: it preserved 999
  correctness but lowered the comparable no-stats 505 count to about 30B
  instructions in 120s, below the clean 34B baseline.
- If a post-`LINX_SPEC_START` SPEC profile shows `helper_linx_tlb_iv` hot,
  first quantify Linux-side `local_flush_tlb_page()` sources before changing
  QEMU cputlb semantics. In the 2026-07-04 `531.deepsjeng_r` profile,
  `helper_linx_tlb_iv` was the second largest active QEMU frame after
  `probe_access_internal`; a naive uncommitted experiment that narrowed
  `TLB.IV`/`TLB.IAV` to an address-derived QEMU MMU-index map preserved the
  999 sentinel but was neutral on focused 531. Do not retry address-derived
  MMU-index narrowing without new evidence; inspect Linx Linux
  `update_mmu_cache_range`, `ptep_set_wrprotect`, and fault/vmalloc
  `local_flush_tlb_page()` call volume first.
- For host-side SPEC profiling, prefer
  `tools/spec2017/profile_qemu_after_spec_start.py` over manual `pgrep` or
  parent-process sampling. The wrapper waits for `LINX_SPEC_START` in the
  generated `qemu.log`, then samples only a descendant whose executable
  basename is `qemu-system-linx64`, avoiding false samples of Python runner
  commands that merely contain a `--qemu` argument.
- Keep trace scope minimal: shortest repro, narrowest event set, shortest instruction window, and one lane at a time.
- Treat QEMU traces as disposable debugging artifacts. Remove large trace/log outputs immediately after extracting the needed evidence.
- Clean temporary QEMU traces from `/tmp`, `/private/tmp`, and repo-local output trees before closeout when they are no longer needed.

## Collaboration rules

- When QEMU diverges from LinxCore/pyCircuit traces, act as reference owner and publish first mismatch evidence.
- Keep timer IRQ policy explicit in strict runs (`LINX_EMU_DISABLE_TIMER_IRQ=0` by default).
- Coordinate trap/MMU semantic updates with `linx-isa` before declaring closure.
- If a QEMU AVS case is blocked by current compiler asm-surface compatibility
  rather than emulator semantics, mark or skip that case explicitly in the AVS
  harness instead of counting it as a QEMU execution failure.

## Skill evolve loop (mandatory closeout)

- At closeout, decide `skill-evolve: update` or `skill-evolve: no-update`.
- Update this skill only for material reusable findings:
  - new emulator semantic rule that must stay aligned with LinxArch,
  - new required runtime gate/command/env for reproducibility,
  - new recurring first-divergence triage sequence.
- Do not update for minor optimization, wording cleanup, or one-off local workaround.
- If update is needed, keep scope narrow and validate with:
  - `python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/zhoubot/linx-isa/skills/linx-skills/linx-qemu`
  - `python3 /Users/zhoubot/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main`

## References

- `references/runtime_gates.md`
