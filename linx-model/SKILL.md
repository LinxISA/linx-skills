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
- Only run `gfsim` on ELFs that have already passed the QEMU stage in the same
  `workloads/generated/<run-id>/ai-bringup/report.json`.
- Do not mark model smoke/workload execution green by adding artificial `-m` or
  `--stop_cycle` limits. The final target is plain `gfsim -f <linx.elf>`;
  timeout artifacts belong to the `model` lane until the model exits naturally
  or an explicit architectural stop condition is implemented.
- If a QEMU-passing direct-boot ELF loops in `gfsim`, record the repeated BPC,
  retired block count, ELF objdump address, and smoke log path in the fix
  packet before changing compiler or benchmark code.
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
  - `skill-evolve: update linx-model (direct-block, ADDTPC page-base, decode, store-immediate PR/PO, LDQ, BFU nuke, compressed-header, and HL immediate contracts)`
