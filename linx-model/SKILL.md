---
name: linx-model
description: Cycle-accurate C++ model workflow for `tools/model`, including `SimQueue` payload policy, `Module` work semantics, port-role tagging, and queue wiring assertions. Use when adding or reviewing queue-wired model code.
---

# Linx Model

Canonical repo location (superproject checkout):

- `tools/model`

AI workload final-target lane:

- The AI workload hard-break flow uses the C++ BlockISA model at
  `model/LinxCoreModel` as the final execution target.
- Canonical command:

```bash
python3 /Users/zhoubot/linx-isa/tools/bringup/run_ai_workload_flow.py --profile smoke --dry-run
/Users/zhoubot/linx-isa/model/LinxCoreModel/bin/gfsim -f <linx.elf>
```

- The smoke profile includes `avs-pto-parity-smoke`, a bounded PTO parity case
  built with `-DPTO_PARITY_TLOAD_STORE_ONLY=1`. Treat it as the fast
  QEMU-to-model PTO parity handoff proof, not as full parity closure.
- The full smoke-sized AVS PTO parity sequence remains `avs-pto-parity` in
  Tier 1. If it times out after QEMU pass, keep the fix packet in the model lane
  with the latest BROB progress instead of relaxing the final `gfsim -f <elf>`
  target.
- `avs-pto-parity-prefix-gemm-performance` is the fast Tier-1 parity prefix
  that passes through QEMU and `gfsim`; it uses fast deterministic F32/FP16
  bit-pattern seeds and stops after `PTO_PARITY_STAGE_GEMM_PERFORMANCE`.
  `avs-pto-parity-prefix-flash-attention` is the deeper Tier-1 model-green
  prefix; it stops after `PTO_PARITY_STAGE_FLASH_ATTENTION` and proves the
  current model boundary reaches the `flash_attention` digest and pass finisher
  after QEMU. `avs-pto-parity-prefix-flash-attention-softmax` is the current
  model-green softmax-prefix micro-profile; it stops after
  `PTO_PARITY_STAGE_FLASH_ATTENTION_SOFTMAX` and uses opt-in
  `PTO_ATTENTION_*` plus `PTO_FLASH_TILE_*` shape flags so the QEMU-passing ELF
  also exits naturally under plain `gfsim -f <elf>`. Treat these as prefix
  proofs/probes only. `avs-pto-parity-prefix-flash-attention-masked` is the
  next promoted micro-profile; it stops after
  `PTO_PARITY_STAGE_FLASH_ATTENTION_MASKED` and adds
  `PTO_ATTENTION_MASKED_SMOKE_*` shape flags so the QEMU-passing ELF reaches
  the `flash_attention_masked` digest and exits naturally under plain
  `gfsim -f <elf>`. `avs-pto-parity-prefix-fa-performance` reuses the same 1x
  attention micro-profile, stops after `PTO_PARITY_STAGE_FA_PERFORMANCE`, and
  reaches the `fa_performance` digest under plain `gfsim -f <elf>`.
  `avs-pto-parity-prefix-mla-attention` reuses that 1x profile, stops after
  `PTO_PARITY_STAGE_MLA_ATTENTION`, and reaches the `mla_attention` digest
  under plain `gfsim -f <elf>`. `avs-pto-parity-prefix-flash-attention-cube`
  adds the `PTO_PARITY_FLASH_CUBE_*` and `PTO_FLASH_CUBE_*` 1x controls, stops
  after `PTO_PARITY_STAGE_FLASH_ATTENTION_CUBE`, and reaches the
  `flash_attention_cube` digest under plain `gfsim -f <elf>`.
  `avs-pto-parity-prefix-flash-attention-vec` adds matching `PTO_FLASH_VEC_*`
  1x controls, stops after `PTO_PARITY_STAGE_FLASH_ATTENTION_VEC`, and reaches
  the `flash_attention_vec` digest. `avs-pto-parity-prefix-gqa` adds matching
  `PTO_PARITY_GQA_*` and `PTO_GQA_SMOKE_*` 1x controls, stops after
  `PTO_PARITY_STAGE_GQA`, and reaches the `gqa` digest under plain
  `gfsim -f <elf>`. The full `avs-pto-parity` row still owns later sparse and
  full-shape maturity; keep QEMU-passing full-shape attention timeouts in the
  model lane until the ELF exits naturally or model throughput/correctness is
  improved.
- Only run `gfsim` on ELFs that have already passed the QEMU stage in the same
  `workloads/generated/<run-id>/ai-bringup/report.json`.
- Do not mark model smoke/workload execution green by adding artificial `-m` or
  `--stop_cycle` limits. The final target is plain `gfsim -f <linx.elf>`;
  timeout artifacts belong to the `model` lane until the model exits naturally
  or an explicit architectural stop condition is implemented.
- Build or select the optimized bring-up binary for workload promotion:
  `cmake -S model/LinxCoreModel -B model/LinxCoreModel/build -DOPT_LEVEL=O3
  -DDISABLE_DEBUG_SYMBOLS=ON`, then build target `gfsim`. The AI runner uses
  these options by default unless `--skip-model-build` selects an existing
  binary.
- If a QEMU-passing direct-boot ELF loops in `gfsim`, record the repeated BPC,
  retired block count, ELF objdump address, and smoke log path in the fix
  packet before changing compiler or benchmark code.
- Direct-boot AVS/PTO/SuperNPUBench ELFs commonly emit UART breadcrumbs through
  MMIO `0x10000000` before they reach digest or finisher writes. Preserve both
  scalar `storeData()` and direct SPE retire observation paths when adding model
  MMIO evidence, and use `uart_tail` plus the latest BROB BPC to decide whether
  the model reached the source stage before timing out.
- If the repeated BPC is the post-test spin or a fail finisher path is skipped,
  inspect the objdump for `C.BSTART DIRECT,<target>` followed by a 32-bit
  in-body `BSTART.STD` / `FALL` descriptor and body stores. The model must
  preserve that descriptor as part of the open direct block, matching QEMU
  execution, rather than closing the block before the finisher body. Do not apply
  that preservation to compressed `C.BSTART.STD` after a direct header; PTO
  `unique_i32` proved that compressed form can be a real targetable block
  boundary.
- For scalar global-address drift after QEMU pass, check ADDTPC before LSU:
  current Linx LLVM/QEMU materialize globals as
  `ADDTPC = (current_pc & ~0xfff) + decoded_page_delta`, then `ADDI` applies the
  low 12 bits. If later loop blocks load from addresses that differ by the
  instruction-PC delta, patch the model PC-relative calculator rather than
  chasing store buffer or SCB merge paths.
- For scalar loop divergence after QEMU pass, verify the SrcR modifier contract
  before touching benchmark or compiler code: Linx LLVM and QEMU encode
  `SrcRType` as `0=.sw`, `1=.uw`, `2=.neg/.not`, `3=no modifier`.
- For scalar hash/probe divergence after QEMU pass, verify W-form logical
  right shifts before touching benchmark or compiler code. `SRLW`/`SRLIW` must
  read `SrcL[31:0]`, mask the shift amount to 5 bits, and sign-extend the
  32-bit result; `kernel/control hashtable_lookup_simt` `kNum=16` hash/probe
  proved this after QEMU passed but `gfsim` computed the wrong MurmurHash3 slot
  until the model stopped routing `SRLIW` through the generic 64-bit `SRL`.
- For scalar loop divergence involving 48-bit immediate materialization, check
  `HL.LUI`/`HL.LIS`/`HL.LIU` before chasing rename, SCB, or benchmark logic.
  Linx Sail and QEMU define `HL.LUI` and `HL.LIS` as sign-extending the decoded
  32-bit immediate to 64 bits, while `HL.LIU` zero-extends it. PTO
  `argmax_fp32` proved this through the `hl.lui -1; sll 32; srl 32` mask
  sequence: QEMU passed, but a model high-half materialization made the loop
  counter start at `-1` and never reach the pass finisher.
- For scalar/vector select divergence after QEMU pass, verify the `csel`/`psel`
  source order before changing compiler or workload code. Linx LLVM/QEMU use
  `SrcP != 0` to select `SrcR` and `SrcP == 0` to select `SrcL`.
- For 48-bit load decode failures after QEMU pass, check the decode table
  before changing compiler output. `LWU_PCR` uses selector `110` in the
  BlockISA model, matching the Linx QEMU/LLVM contract.
- For 48-bit store-immediate decode failures after QEMU pass, check the
  `store_si*` operand order before changing compiler or workload code. BlockISA
  scalar stores use `src0` as store data and `src1`/`src2` as address operands;
  `SBI/SHI/SWI/SDI.PR` and `.PO` must decode as data, base, scaled immediate,
  with PR address/writeback computed from base plus offset. PTO
  `gemm_reuse_*_fp16` proved that the old immediate-first `store_si3` ordering
  stores FP32 data as an address and reaches the fail finisher despite QEMU
  passing the same ELF.
- For PCR store failures after QEMU pass, preserve the decode operand contract:
  `SB/SH/SW/SD.PCR` carries the PC-relative address immediate in `src0` and the
  store data in `src1`. Address calculation must use `pc + src0`, while common
  store-data paths must select `src1` only for PCR stores and keep `src0` for
  ordinary stores. `pto-kernel-unique_i32` proved this by passing QEMU, then
  tripping the model text-store assertion on `hl.sw.pcr` until PCR stores used
  a dedicated store-data source selector.
- For LSU crashes in non-atomic load execution, do not require `src1`.
  `src1`/`dataVld` is mandatory for atomic memory operations; ordinary loads
  may execute with no right-hand source operand.
- For BSTART recovery after direct-block body execution, preserve the owning
  start-header `hid` when converting in-body `BSTART` / `BEND` markers to last
  markers. BRQ/RAS lookup may need that relation to recover the original open
  block.
- For BFU nuke handling, do not consume queued BE nuke records while a direct
  `be_bfu_nuke` is pending. If a direct or queued nuke targets an FB older than
  the BRQ front, consume it as stale; a missing non-stale active nuke header is
  still a model error.
- For BFU delivery crashes after QEMU pass, check F4 no-valid-FB handling
  before changing workload or compiler code. `Pipe::GetFirstValidFBIdx()`
  returns `-1U` when the pipe has no resident fetch bundle, so
  `BFU::DeliverStall` must bounds-check that sentinel before indexing
  `pipe[F4].fb[global_idx]`; `pto-kernel-hash_table_insert_fp32` proved this
  path by passing QEMU and then SIGBUSing in model `DeliverStall`.
- For BFU/BHC miss-queue stalls after QEMU pass, preserve the
  `MissQEntry(va_cl, pa_cl, stid, is_pf, enqueue_time)` constructor order.
  Demand misses must enqueue `(fb->stid, false)` and prefetch misses must
  enqueue `(pfi->stid, true)`. Swapping `stid` and `is_pf` can make STID0
  prefetch entries look like STID1 demand entries, escaping STID0 flushes and
  consuming demand miss capacity during long soft-float loops.
- For BFU local-fetch crashes or F1 local-pipe stalls after QEMU pass, audit
  stale local selection before changing compiler output. `select_info` must be
  cleared when the selected local pipe no longer exists, its F2 slot is invalid,
  it is not ready, or its F2 FB is null. Before `LocalPipeStall()` reserves new
  local pipes, release occupied local pipes whose F0/F2/F3 stages are all
  invalid and reset the static predictor pipe for the remembered STID. Full
  `avs-pto-parity` proved this by moving from a BFU `tanh` SIGSEGV and a
  `softmax` local-pipe stall to sustained execution through
  `flash_attention_softmax`.
- For RAS crashes in call-heavy soft-float loops after QEMU pass, check the
  speculative write-slot hazard before changing benchmark or compiler code.
  `RAS::handleCall()` writes at `spec_wptr`; if that slot is valid, F1 must
  stall before prediction instead of asserting on `!spec_table[spec_wptr].vld`.
  `avs-pto-parity-prefix-flash-attention` proved this by moving from a
  `bfu_ras.cpp:52` assertion in `softmax_inplace` to a final-green
  `flash_attention` prefix.
- For queued BE nuke records that name a later local split, first look for the
  exact `(fbid, fbid_local)` in BRQ. If it is absent but the same global `fbid`
  has an older resident local split, use that resident FB only to find the
  owning nuke header. If no resident header matches, consume the queued record
  as stale instead of aborting; the requested local split is no longer active in
  BFU. Exact-resident FBs that lack a valid nuke header remain model errors.
- When mapping a queued nuke body PC back to its owning header, compare against
  the decoded header size (`spInfo->hsize`) before falling back to the fixed
  bundle step. Compressed `C.BSTART` headers can have their first body
  instruction two bytes after the header, and a fixed `MIN_BUNDLE_SIZE` match
  can miss the valid owner.
- Direct-boot SuperNPUBench ELFs use the test finisher MMIO address
  `0x10009000`; `0x5555` is pass, while `0x3333` and `0x7777` are non-pass
  terminal statuses. A final-green `gfsim` run should exit naturally and leave
  a `linx_test_finisher write addr=0x10009000 ... pass` line in its log.
- Classify QEMU-passing ELF load/decode/runtime failures as `model` until
  digest or trace evidence proves the compiler or emulator produced the first
  wrong architectural event.

## Module work contract (strict)

- `Work()` is the one-cycle evaluation phase. A module reads current visible queue heads, performs combinational logic, and optionally enqueues results to output queues.
- Default rule: read at most one item per input queue and at most one item per inner queue per cycle unless the module spec explicitly requires multi-consume behavior.
- If a decision only needs to inspect data, use `Front()` and do not pop.
- Only consume when the module actually fires. Use `Read()` to transfer ownership/value out of the queue, or `Pop()` only after an intentional `Front()`-based decision.
- Do not mutate sibling-module state directly inside `Work()`. Cross-module communication must happen through `SimQueue`.
- `Xfer()` is not a substitute for datapath logic. Keep functional data motion in `Work()` and reserve `Xfer()` for phase-boundary bookkeeping if needed.

## Queue role discipline (strict)

- Parent modules own the real queue storage and pass only non-owning queue pointers to children.
- Distinguish three queue roles in module code:
  - `INPUT`: boundary queues driven from outside the module.
  - `OUTPUT`: boundary queues written by the module.
  - `INNER`: module-local/private queues used for internal pipelining or local observation.
- Do not overload `inputs_` to represent internal queues. If a module needs private readable queues, add a separate `inners_` container plus `AddInner()` / `Inner()` helpers before implementing the module logic.
- Do not wire one queue pointer into inconsistent roles in the same module without an explicit comment and assertion.

## Port binding macros (required pattern)

When writing module implementation files, bind queues through role-tagged macros or equivalent helper wrappers. The point is to make queue role visible in code review and fail fast on wiring mistakes.

```cpp
#define INPUT(name, idx) \
  auto* name [[maybe_unused]] = this->Input(idx); \
  LINX_MODEL_ASSERT(name != nullptr)

#define OUTPUT(name, idx) \
  auto* name [[maybe_unused]] = this->Output(idx); \
  LINX_MODEL_ASSERT(name != nullptr)

#define INNER(name, idx) \
  auto* name [[maybe_unused]] = this->Inner(idx); \
  LINX_MODEL_ASSERT(name != nullptr)
```

- If the framework already provides equivalent helpers, reuse them.
- If not, add the smallest helper layer needed before writing datapath code.
- Avoid raw repeated indexing such as `inputs_[0]` / `outputs_[1]` throughout `Work()`.

## Wiring and assertion rules (mandatory)

- In `Build()` / `BuildSelf()`, assert every queue pointer immediately after registration and connection.
- Assert expected port counts for modules with fixed interfaces.
- Prefer compile-time type equality on queue payloads when wiring templates across helpers.
- For `unique_ptr` payloads, ownership moves exactly once through `Write(std::move(...))` and `Read()`. Do not access the moved-from handle afterwards.
- For `shared_ptr` payloads, use sharing intentionally for observer/fanout cases; do not switch to `shared_ptr` just to avoid fixing ownership design.
- Use value payloads for flags, small integers, enums, and narrow tags.

## Work template

```cpp
void WorkSelf() override {
  INPUT(in0, 0);
  OUTPUT(out0, 0);
  // INNER(pipe0, 0);

  const bool fire = !in0->Empty() && !out0->Full();
  if (!fire) {
    return;
  }

  const auto& peek = in0->Front();
  if (!Accept(peek)) {
    return;
  }

  auto item = in0->Read();
  auto result = Combine(std::move(item));
  out0->Write(std::move(result));
}
```

- For value payloads, the same pattern applies with plain values:

```cpp
void WorkSelf() override {
  INPUT(flag_in, 0);
  OUTPUT(flag_out, 0);

  if (flag_in->Empty() || flag_out->Full()) {
    return;
  }

  const bool flag = flag_in->Read();
  flag_out->Write(!flag);
}
```

## Closeout line

- When this skill causes a material update, record:
  - `skill-evolve: update linx-model (direct-block, ADDTPC page-base, W-form shifts, decode, store-immediate PR/PO, LDQ, BFU nuke, BHC miss queue, BFU local-pipe lifetime, compressed-header, and HL immediate contracts)`
