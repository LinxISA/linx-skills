---
name: linx-core
description: LinxCore (rtl/LinxCore) development workflow + block/BID/BROB/BISQ design decisions. Use for any LinxCore backend/bctrl work, especially block-structure (BSTART/BSTOP/EOB), BID allocation, and flush semantics.
---

# Linx Core

Canonical repo location (superproject checkout):

- `rtl/LinxCore` (submodule)

## Cross-gate closure (mandatory)

Run these before declaring LinxCore closure:

```bash
cmake -S /Users/zhoubot/linx-isa/rtl/LinxCore -B /Users/zhoubot/linx-isa/rtl/LinxCore/build
cmake --build /Users/zhoubot/linx-isa/rtl/LinxCore/build -j"$(sysctl -n hw.ncpu 2>/dev/null || nproc)"
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_stage_connectivity.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_runner_protocol.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_cosim_smoke.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_opcode_parity.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_trace_schema_and_mem.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_rob_bookkeeping.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_block_struct_pyc_flow.sh
```

Nightly escalation gates:

```bash
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_coremark_crosscheck_1000.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_cbstop_inflation_guard.sh
```

Coordination requirements:

- Architecture-visible changes must coordinate with `linx-isa`.
- pyCircuit interface-visible changes must coordinate with `linx-pycircuit`.
- Reference-model divergences must coordinate with `linx-qemu`.
- Publish evidence under `docs/bringup/gates/logs/<run-id>/<lane>/`.

## Log / trace hygiene (strict)

- Avoid generating excessive large logs.
- Do not start full-run DUT/QEMU/raw-trace capture from cycle 0 unless no narrower reproducer exists.
- First localize the suspicious `pc`, retire window, stage window, or benchmark end condition, then enable logging only around that point of interest.
- Keep captures minimal: shortest repro, smallest commit/time budget, narrowest event set, and no duplicate trace lanes when one is sufficient.
- Treat debug logs/traces under `/tmp`, `/private/tmp`, and repo-local output trees as disposable. Remove them once the needed evidence has been extracted.
- If a producer is still writing after the evidence you need is captured, stop it before rerunning or changing the setup.

## Hierarchy + compile-budget discipline (strict)

- Repeated substantial backend hardware must be expressed as `@module` families plus `spec.module_family(...).vector/map/dict(...)` and `m.array(...)`.
- `@function` is only for small pure combinational helpers. Do not instantiate modules or allocate state from `@function`.
- `@const` is required for reusable structural metadata that drives hierarchy shape or specialization reuse.
- pyCircuit now hard-fails oversized emitted hierarchy by default:
  - hottest emitted TU `<= 15000`
  - hottest emitted module `<= 40000`
  - total emitted cost `<= 700000`
- Mandatory bring-up checks when touching backend hierarchy:

```bash
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_pyc_hierarchy_discipline.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tools/generate/update_generated_linxcore.sh
```

- Practical slicing rule from LinxCore ROB bring-up:
  - do not jump straight to per-entry stateful child modules when that would create dozens of wide instance interfaces in the parent;
  - prefer recursive bank/lane slices that keep compile-once reuse but cap parent eval fanout.
  - when a parent only needs queue occupancy/readiness shape, pass packed masks (for example `valid_mask`) instead of `depth` scalar ports; per-entry scalar fanout can dominate emitted instance-cache TUs even after hierarchy splitting.
  - when a consumer only needs a queue-local scan result (for example head-wait, oldest-ready, or replay candidate), keep the scan inside the queue owner module and export only the compact result; do not feed `iq_depth * fields` metadata into a parent or sibling scan module.
  - when a consumer needs per-entry read/query services from a state owner (for example ROB commit-read or metadata lookup), attach that service to the existing owner hierarchy and export only compact query results; building a second top-level grouped consumer tree can still leave the hottest `tick/eval` shard in the parent because the parent must re-fanout every owned field into that tree.
  - before cutting a suspected hotspot, rank the parent module's `pyc.instance` sites by combined input+output count from emitted top-level MLIR; the hottest compile shard is often the widest surviving parent/child boundary, not the child whose standalone module body is largest.

## Reference-model structure discipline (strict)

- The cycle-accurate reference model must preserve the same owner boundaries called out by the LinxCore microarchitecture contract; do not collapse queue ownership, wakeup ownership, replay ownership, and stage-local state into one giant implementation file.
- Keep state-owner modules/files aligned to architectural domains:
  - queue-owned state and wakeup routing together,
  - LSU owner state together,
  - recovery/flush ownership together,
  - trace emission separate from state mutation.
- For issue-side work specifically, keep `S1/S2/IQ/P1/I1/I2` responsibilities inspectable in dedicated modules/files. A monolithic scheduler file is a contract smell because it hides which stage owns routing, readiness initialization, wakeup fanout, and deallocation.
- Within that issue-side split, keep `P1/I1/I2` pick arbitration, RF-read accounting, issue-confirm gating, and issue-side wait-cause logic in an issue-owner module/file rather than leaving them split across top-level scheduler glue and queue-owner code. Queue ownership should stop at IQ residency/wakeup; issue ownership should cover pick/read/confirm behavior.
- When adding new owner tables or wake structures such as qtag wait crossbars or IQ owner tables, place them in the queue-owner module/file instead of generic top-level helpers.
- For LSU-side work, keep `LIQ/LHQ/MDB/STQ/SCB/L1D` transitions in an LSU-owner module/file and keep redirect pruning plus LSID rebasing in a recovery-owner module/file. Do not mix memory-owner progression and recovery-domain pruning into generic scheduler glue.
- For frontend-side work, keep instruction-to-uop build/decode in a decode-owner module/file, `F0..F4/D1..D3/S1/S2` movement and routing in a frontend-owner module/file, and stage-event generation in a trace-owner module/file. Do not mix uop construction, stage transport, and trace emission back into one scheduler file; that obscures which part of the model owns fetch barriers, ROB admission, and visible stage residency.
- Model architectural redirect restart as an explicit `FLS -> F0` recovery handoff, not as an implicit side effect of generic fetch iteration. In the CA reference model, recovery should publish the earliest frontend restart cycle and `F0` should honor that registered restart boundary; do not let fetch resume in the same abstract step that resolved the redirect just because the software loop can see the corrected target immediately.
- Keep redirect restart-source selection in the recovery owner too. `FLS` should resolve the legal restart source from redirect metadata and block-boundary legality (`BSTART`, `FENTRY`, `FEXIT`, `FRET.*`), then hand `F0` a concrete restart token `(target_pc, restart_seq, resume_cycle)`; do not let generic fetch code infer restart by “next surviving seq” once wrong-path/frontend occupancy exists.
- Keep architectural redirect ownership boundary-only. In the CA reference model, a non-fallthrough BRU commit is not itself an `FLS` redirect owner; treat it as pre-boundary correction metadata and let the later architectural boundary (`BSTART`/`BSTOP`/macro boundary) own the visible redirect and frontend restart.
- Model deferred BRU correction as explicit recovery-owner state, and let the later architectural boundary consume it before any boundary-local redirect target. A BRU mismatch should publish pending correction metadata when it becomes architecturally visible, but `FLS` should only resolve at the boundary, using pending BRU correction first and clearing that state once the boundary-owned redirect/restart token is issued.
- Match deferred BRU correction by block/branch epoch, not plain age. In the CA reference model, a later boundary may consume deferred BRU correction only when the correction epoch matches that boundary's block epoch; a stale correction from an older dynamic block instance must not leak across a head-`BSTART` epoch advance into the next loop iteration.
- Model recovery-target safety as a BRU-side precise trap, not a boundary fallback. If deferred BRU correction resolves to a target that lacks legal `BSTART` metadata, raise `TRAP_BRU_RECOVERY_NOT_BSTART` on the offending BRU row and retire that row with `trap_valid/trap_cause`; do not silently convert the fault into a boundary-local redirect or guessed restart sequence.
- Carry checkpoint identity through recovery-owner state and trace visibility. Deferred BRU correction, boundary redirect selection, and BRU recovery faults should preserve the checkpoint id associated with the owning row, and `FLS/CMT` trace emission should surface that checkpoint/trap metadata instead of collapsing recovery events to an unlabeled redirect cause.
- Carry live boundary kind through recovery trace visibility as well. `FLS/CMT` events that represent redirect ownership, BRU recovery faults, or rows retiring under a live branch-validation context should surface the owning branch class (`fall/cond/call/ret/direct/ind/icall`) so DFX can distinguish which architectural boundary kind drove recovery instead of reducing everything to a generic redirect cause.
- Keep checkpoint ownership split by domain: frontend owns fetch-packet checkpoint assignment, and recovery owns `flush_checkpoint_id` / redirect-checkpoint propagation. Do not synthesize backend-visible checkpoint ids from unrelated notions like block epoch once a fetch/F4 packet boundary exists; derive/store checkpoint id at packet ingress and carry the boundary row's checkpoint through redirect/fault handling.
- Model flush cleanup as registered recovery state, not same-cycle helper cleanup. In the CA reference model, boundary redirect resolution should publish `flush_pending` / `flush_checkpoint_id`-like state first, and speculative prune plus LSID/memory-owner cleanup should apply on the later recovery cycle when that pending flush becomes visible; do not prune wrong-path state in the same abstract step that retired the redirect owner just because the software scheduler can see both events at once.
- For rename-like owner state, checkpoint snapshots belong to start-marker dispatch and restore belongs to `flush_checkpoint_id`. In the CA reference model, if you do not yet model full SMAP/CMAP/freelist state, at least snapshot the owned logical-ready/rename-visible state when a start marker dispatches and restore that snapshot when the registered flush applies; do not try to reconstruct rename recovery solely from age-based wrong-path pruning after the fact.
- Keep fetch checkpoint ids and ROB-visible checkpoint ids distinct. In the hardware contract, packet/fetch checkpoint identity comes from the frontend, while start-marker/ROB checkpoint identity is derived at decode/dispatch (for example `f4_checkpoint_id + slot`) and only start markers carry that backend-visible checkpoint token. A CA model should not reuse fetch-packet checkpoint ids as if every row had a ROB checkpoint; recovery, BRU correction ownership, and commit/trace checkpoint fields should use the start-marker/ROB-visible namespace.
- BRU correction ownership uses the active start-marker checkpoint context, not the non-start BRU row's trivial checkpoint id. In the hardware contract, deferred BRU correction carries the ROB-visible checkpoint state of the current recovery context (the latest active start-marker/boundary checkpoint), even when the offending BRU row is not itself a start marker. A CA model should therefore resolve BRU correction and BRU recovery-fault checkpoint ids from the active checkpoint context, while boundary-owned redirect/flush state still uses the boundary row's own checkpoint token.
- Once that checkpoint context is live in the backend, carry it as backend-owned row state instead of reconstructing it by stream scans. In the hardware contract, BRU/recovery paths consume the checkpoint token already attached to backend-visible row state (`ROB`/issue-visible ownership). A CA model should assign recovery checkpoint context when rows enter backend ownership and let BRU correction/fault paths read that live token directly; backward scans over prior `BSTART` rows are only a bootstrap fallback, not the steady-state owner path.
- Apply the same owner rule to branch/block epoch metadata. In the hardware contract, BRU validation compares live backend `bru_epoch` against live branch state epoch, and deferred correction carries that backend-owned epoch forward. A CA model should assign row epoch when rows enter backend ownership and restore that epoch context on checkpoint flush; do not gate BRU correction or stale-correction suppression by recomputing epoch only from the committed stream once backend-owned row state exists.
- For reorder/commit work, keep `ROB/CMT` retirement, commit-visible ready-table publication, and ROB-age ordering helpers in a commit-owner module/file. Do not leave retirement and age ordering buried in the top-level scheduler once queue/front-end/LSU ownership has been split, or the model will stop reflecting which domain owns retirement semantics versus recovery semantics.

## LinxTrace v1 container (strict)

- Canonical trace artifact is a single uncompressed `*.linxtrace` (JSONL).
- First non-empty record must be `{"type":"META", ...}` (in-band META).
- Legacy split artifacts are forbidden: `*.linxtrace.jsonl`, `*.linxtrace.meta.json`, `*.gz`.
- Do not turn LinxTrace/raw-event generation into an unbounded full-run logger by default.
  Prefer bounded commit windows or explicit terminal conditions, and only expand the window after a smaller capture proved insufficient.
- Keep LinxTrace authoring on the pyc probe path.
  Do not introduce trace-only pipeline state, edge detectors, sequence counters, or block-event sidecars into the functional LinxCore hardware just to make pipeview look correct.
  If the trace needs reconstruction, do it in TB/raw-trace/build steps unless the stage owner already exposes the needed state as a natural probe.
- Preserve probe-only child hierarchy with compiler keep metadata, not parent debug-port fanout.
  If a child exists only to emit `dbg__*` probes for ProbeRegistry/LinxTrace, keep the instance alive via pyCircuit's keep path (`pyc.debug_keep` + dead-instance pruning) instead of forwarding every probe leaf into the parent just to defeat DCE.
- Probe-only DFX boundaries should be packed for compile budget.
  `debug_occ` helper modules do not need to preserve functional-hardware port granularity; if parent/child fanout becomes a hotspot, pack per-lane/per-stage probe payloads into wide buses and unpack inside the probe module.
- Visible backend stages must come from real owner stage state, not transient probe overlap or commit-edge reconstruction.
  In particular, `W1/W2` must not be synthesized from retire-side bookkeeping; top-level commit probes should emit only `CMT`.
- Keep block structure in the main trace contract: `uop` rows plus `block` rows, with `BLOCK_EVT` preserved as auxiliary lifecycle context.

Generate + lint + open (LinxCore-side builder flow):

```bash
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tools/linxcoresight/run_linxtrace.sh <program.memh> [max_commits]
python3 /Users/zhoubot/linx-isa/rtl/LinxCore/tools/linxcoresight/lint_linxtrace.py <trace.linxtrace>
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tools/linxcoresight/open_linxcoresight.sh <trace.linxtrace>
```
## Block/BID design decisions (strict)

These are confirmed in #linx-core (2026-02-24) and must be preserved by future changes:

1) **BID is generated by BROB**
- BID is the BROB entry identity.
- Default sizing: BROB is parameterized; **default entries = 128**.

2) **BID encoding**
- Keep 64-bit BID.
- `slot_id = BID[6:0]` (for 128 entries)
- `uniq = BID[63:7]` (debug uniqueness / age ordering)
- So: `BID = (uniq << 7) | slot_id`

3) **Tag routing**
- **cmd_tag = BID[7:0]**
- Rationale: PE response tags must route to the correct BROB entry; avoid any unrelated tag sources (e.g. cycles).

4) **Block completion**
- `complete = scalar_done && (needs_engine ? engine_done : 1)`
- `needs_engine` should be set when the block actually issues engine commands.

5) **BSTART / BSTOP semantics**
- `BSTART` uop in ROB carries the **new BID** (it belongs to the new block).
- `scalar_done` is triggered at **BSTART retire + BSTOP retire**.
  - On BSTART retire: mark scalar_done for the *old active bid* (implicit end).
  - On BSTOP retire: mark scalar_done for the current active bid (explicit end).

6) **Flush semantics (BID-based)**
- On a flush/redirect, the system reports the **current block BID** (the block where the flush is generated).
- All blocks **younger than this BID** must be cleared.
- Because slot ids wrap, comparisons must use full 64-bit BID ordering.
- Rule: **keep `bid <= flush_bid`, kill `bid > flush_bid`**.
- This applies to **all modules that carry/queue BID** (at minimum: BROB + BISQ + any other bid-carrying queues).

## PR checklist for BID/block changes

- [ ] Confirm `cmd_tag == bid[7:0]` through backend->bctrl->PE and response routing.
- [ ] Confirm flush path provides `flush_bid` and every bid-carrying module kills `bid > flush_bid`.
- [ ] Confirm BROB keeps `bid <= flush_bid` (including current block) and handles wrap via uniq bits.
- [ ] Update docs/skills when new edge cases are discovered.

## Issue Queue + speculative ready + load-miss cancel (strict)

Confirmed in #linx-core (2026-02-24). This section is the checklist to avoid forgetting.

### Ready table vs speculative ready

- `ready_table[P-ptag]` is **1-bit per P-ptag** and is **non-spec ready**:
  - must only be set when the value is guaranteed **not** to be cancelled.
  - used by uops after enqueue to query readiness.
- `issq` must track **speculative readiness** per operand, with an `is_spec` marker.

### Pick/issue/commit model

- Wakeup must **not** affect pick in the same cycle (timing constraint):
  - wakeup @ cycle N → pick can only observe it at cycle N+1.
- `issq` entries must not be deallocated while cancellable.
  - Implement an `inflight` lock bit:
    - P1: `pick` sets `inflight=1` (entry remains valid).
    - Cancel: clears `inflight=0` (entry stays valid).
    - **Dealloc point is I2**: only clear `valid` when the uop is confirmed non-cancellable.
- Age/oldest-ready ordering must be preserved across `inflight`:
  - inflight entries are simply ineligible; their age does not change.

### Load speculative wakeup + forward + miss

- Load produces **spec-wakeup at LD_E1** (no data).
- Load returns **data only at LD_E4**.
- Consumers that become ready only via load spec-wakeup:
  - must not request RF read ports in I1 for that src;
  - must obtain data via **E4→consumer-I2 forward**, reusing the bypass network (match by P-ptag).

### ld_gen_vec

- `ld_gen_vec` is a **bitset** (not onehot), representing load pipeline stages E1–E4.
- It must propagate along dependency chains.
- Load pipeline advances `ld_gen_vec` via bit-shift as it moves through stages.

### Miss-pending suppression

- LSU provides `miss_pending` (derived from E4 miss detection) that stays asserted until LIQ restarts the load after refill and the load returns via the hit path.
- While `miss_pending==1`, issue queues must suppress picking entries whose `src.ld_gen_vec` contains `LD_E4`.

### Config hook (optional)

- Keep a top-level `CoreCfg` hook for an alternative implementation that delays miss visibility to E5 (would require extending `ld_gen_vec` to 5 bits). Default is the E4 scheme above.

## Pipeline + wakeup timing (strict)

- Pipeline stages used in discussions: `P1 → I1 → I2 → E1 → W1`.
- Latency-to-wakeup mapping (initial):
  - `lat=1 → wakeup@P1`
  - `lat=2 → wakeup@I2`
  - `lat=3 → wakeup@E1`
  - `lat=4 → wakeup@W1`
- Timing constraint: wakeup at cycle N can only affect pick at cycle N+1 (no same-cycle wake→pick loops).

## IQ naming + physical layout (strict)

- External naming must follow golden `uop_kind` mapping (`issq_alu/bru/agu/std/fsu/sys/cmd/...`).
- Physical IQs may be merged/split, but must preserve original `uop_kind` for trace/perf.
- Current physical split decision:
  - `alu_iq0` (ALU-only)
  - `shared_iq1` (ALU + SYS + FSU)
- Enqueue ports are parameterized. Default: **each physical IQ has 2 enq ports**.
- ALU uops may be dynamically distributed between `alu_iq0` and `shared_iq1`:
  - prefer filling `alu_iq0` first, then spill to `shared_iq1`.

## Regfile ports + arbitration (strict)

- Read ports may contend (area saving):
  - default `int_rf_rports = 3` (parameterized).
  - I1 does global read-port arbitration; failure cancels the in-flight attempt (entry remains valid; `inflight` clears).
  - Arbitration policy: **oldest-first**.
  - Oldest key uses ROB age (`rid + wrap`), compared relative to ROB head.
- Write ports must not contend (performance):
  - each IQ picker/issue port corresponds to a pipeline and a dedicated RF write port.
  - **STD has read ports but no write port**.

## T/U point-to-point wakeup (strict)

- P-ptags: global broadcast wakeup.
- T/U queue semantics: point-to-point wakeup via `qtag = (phys_issq_id, entry_id)`.
  - `phys_issq_id` is a physical IQ enum (`IQ_ALU0/IQ_SHARED1/IQ_BRU/IQ_AGU/IQ_STD/IQ_CMD/...`) derived via `spec` templates at JIT.
  - `entry_id` width is derived per IQ (`clog2(entries)`); packed to a uniform max width for the qtag wire.

## Load spec-ready + forward (strict)

- `ready_table` is used to **initialize** src readiness at enqueue.
- After enqueue, src readiness is maintained in the issq entry; E4 hit must use the wakeup path to update existing entries.
- Merge rule: `src_ready = src_ready_nonspec || src_ready_spec`.
  - nonspec once set never clears.
  - spec may be suppressed by miss_pending gating.
- Load behavior:
  - spec-wakeup at **LD_E1** (no data).
  - data only at **LD_E4**; consumer receives it via **E4→consumer-I2 forward**, reusing bypass (match by P-ptag).
  - For load-spec srcs, I1 must not request RF read ports.

## LIQ/LHQ + load/store ids (strict)

- Decode allocates mem-order ids with D1 apply / D2 grant, in slot order (slot0→slot3) to define same-cycle ordering.
- Replace `ldq` naming with:
  - `LIQ` (Load Inflight Queue) — load pipeline + miss/restart/repick.
  - `LHQ` (Load Hit Queue) — stores resolved load info for load/store address conflict checks.
- Default LIQ depth: 32 (parameterized).
- LHQ stores byte-granular overlap metadata:
  - 64B cacheline window + 64-bit byte mask.
  - LHQ updates on load **E4 hit**.
- Separate id domains:
  - `LID` (load_id) is LIQ slot+wrap.
  - `SID` (store_id / stq_id) is STQ slot+wrap.
- Cross-domain ordering snapshots:
  - each load(LID) records `youngest_sid_at_alloc` (SID+wrap).
  - each store(SID) records `youngest_lid_at_alloc` (LID+wrap).
- Store split: STA(AGU) + STD share the same SID.

## SCB (Store Coalescing Buffer) → DCache / CHI (strict)

Confirmed in #linx-core (2026-02-25).

- STQ may contain flushable (speculative) stores.
- SCB must only contain stores guaranteed **not** to be flushed.
  - This is controlled by a **non-flush pointer** (strong: excludes branch flush + exceptions/interrupts/traps).
- SCB coalesces by **physical cacheline** (paddr line base).
- Memory model: **TSO**
  - store drain must preserve program order.

### CHI completion

- Fence/store-drain completion is defined by receiving **WriteResp** (not just request acceptance).
- Use **CHI TxnID** to match WriteResp to SCB entries.
- Default parameters (parameterized):
  - `scb_entries = 16`
  - `scb_outstanding = 8` (TxnID width = 3)

### Coalescing + ordering constraints

- Do not merge additional writes into an SCB entry that has already issued a CHI request and is awaiting WriteResp.
- If the same cacheline is written again while an outstanding entry exists, allocate a **separate** SCB entry (queue), and drain in SID order.
- Drain arbitration: **oldest SID first**.

## Store→load forwarding (strict)

- Forwarding compares address + 64B byte mask.
- For a load(LID), only consider older stores with `SID <= youngest_sid_at_alloc(LID)`.
- If multiple overlap, select the **nearest older per byte** store (most recent SID for each byte within that range).

### Reference implementation to benchmark against (XiangShan)

We explicitly benchmarked these rules against XiangShan's LSQ forwarding design (2026-02-25) and the approach matches:

- Byte-granular forwarding implemented as per-byte data+valid arrays.
- Address CAM produces per-entry hit masks.
- Ring-buffer wrap handled by splitting the candidate range into two masks (same-flag / different-flag), i.e. `needForward(0/1)`.
- If addr matches but data is not valid, raise a replay-style condition (`dataInvalid` in XiangShan).

Useful XiangShan source references:
- `XiangShan/src/main/scala/xiangshan/mem/lsqueue/StoreQueueData.scala`
  - `SQAddrModule`: addr CAM + mask-aware hit
  - `SQData8Module/SQDataModule`: per-byte youngest-store selection + forward mask/data generation
- `XiangShan/src/main/scala/xiangshan/mem/Bundles.scala`
  - `LoadForwardQueryIO`: forwardMask/forwardData + `dataInvalid`

For LinxCore, the equivalent behavior is:
- E2 completes STQ forwarding query (addr CAM + older-range mask + per-byte youngest selection).
- E3 selects cache vs store-forward data and performs merge by byte mask.
- E4 registers the final data and triggers wakeup/ready-table update (hit).
- If store-forward selected but store-data not ready, treat as miss_kind=STORE_DATA_NOT_READY and repick after STQ data-ready.

### STQ data array implementation decisions (strict)

Confirmed in #linx-core (2026-02-25):

- STQ data array is **banked** and **2-cycle write**:
  - default `stq_data_banks = 2` (parameterized).
  - write ordering: **mask first, then data** (2 cycles).
  - `stq_data_ready(sid)` is asserted only after **mask+data** are both written.
- With 2 banks, split the 64B cacheline window by byte lanes:
  - bank0 covers bytes 0..31, bank1 covers bytes 32..63.

## Load/store conflict → nuke flush (strict)

- Address conflict triggers a **nuke** attributed to the load.
- LSU reports the load RID; ROB sets `entry.nuke=1` on that ROB entry.
- Nuke triggers only when the nuke-marked load becomes ROB head:
  - do not retire that entry;
  - redirect PC = that load's PC.
- `nuke_pending` freezes IFU (stop fetching new younger uops), but commit_redirect (older BRU flush) still applies.
  - BRU flush may clear younger ROB entries (and their nuke marks).
- Implementation: ROB maintains an `oldest_nuke` record (not full-table OR scan) and validates nuke reports only for still-valid RIDs.
- For block domain: on nuke flush, compute `flush_bid = rob_head.block_bid` and flush younger blocks by BID (`bid > flush_bid`).

## Deferred BRU correction payload (strict)

- Deferred BRU correction must carry both:
  - the branch target, and
  - `actual_take` / correction-take state.
- Do not model deferred BRU correction as target-only metadata.
- Boundary-authoritative recovery may need to restart at:
  - the carried branch target when `actual_take=1`, or
  - the boundary fallthrough when `actual_take=0`.
- A CA reference model that records only the target cannot represent the
  spec-required `pred_taken=1, actual_take=0` recovery case correctly.

## Live branch-validation context (strict)

- Backend BRU validation context must be seeded only by boundary forms that
  carry BRU-visible prediction semantics:
  - conditional boundaries, and
  - return boundaries.
- Do not treat every redirecting `BSTART*` form as a conditional-validation
  context. `CALL` / `DIRECT` / `IND` / `ICALL` boundaries are not BRU
  mismatch-validation owners.
- For conditional boundaries, seed `pred_take` from frontend direction policy:
  - backward target (`target < pc`) => predicted taken
  - forward target (`target >= pc`) => predicted not-taken
- For return boundaries, seed `pred_take = 0`.
- Keep the full live boundary kind taxonomy in backend-owned context
  (`FALL/COND/CALL/RET/DIRECT/IND/ICALL` or the local equivalent).
- Do not collapse live boundary context to only `cond/ret/none` in the CA
  model. BRU mismatch validation is a subset rule over that full taxonomy,
  not the only branch-context state the backend owns.

## Dynamic boundary target ownership (strict)

- `RET` / `IND` / `ICALL` recovery must be driven by live backend-owned target
  state, not only by a committed-row `next_pc` surrogate.
- In the CA reference model:
  - `SETC.TGT` / `C.SETC.TGT` publish the dynamic target owner state for the
    current block;
  - `FRET.*` may publish row-local dynamic target state directly;
  - boundary rows (`BSTOP` / equivalent block terminators) may snapshot only
    already-live dynamic target owner state.
- Do not let a boundary row manufacture dynamic-target ownership from a generic
  committed-row redirect fallback when no live `setc.tgt` owner exists.
- If a `RET` / `IND` / `ICALL` boundary resolves without live dynamic-target
  owner state, model a precise boundary-owner trap rather than silently using a
  guessed restart.
- If live dynamic-target state resolves to a non-block start, model a precise
  boundary-owner bad-target trap on that same row.
- Keep this target owner state checkpoint-restorable with the rest of the live
  recovery/rename-owned backend context.

## Call-header return-target ownership (strict)

- Treat `CALL` start markers as a distinct backend-owned header contract, not
  just as a branch-kind label.
- The CA reference model must support both legal call-header shapes:
  - fused returning call headers that already publish `ra` / return-target state
    on the call-start row, and
  - adjacent `CALL` start marker + `SETRET/C.SETRET/HL.SETRET` materialization.
- For the adjacent form, keep a one-row call-header adjacency window alive
  across the call-start boundary so the immediately following `SETRET` can bind
  to that header.
- `SETRET` outside that immediate adjacency window is a precise strict-mode
  contract fault on the `SETRET` row itself.
- `CALL` headers without adjacent `SETRET` remain legal as non-returning call
  headers; do not trap the header row just because it lacks return-target state.
- `SETRET/C.SETRET` materializes an explicit return label for later return
  consumption; do not apply `RET/IND/ICALL` block-start legality checks at
  call-header materialization time. Enforce target legality when the dynamic
  return target is actually consumed.
- Call-header return-target owner state and open-header adjacency state must be
  checkpoint-restorable with the rest of the backend recovery context.
- Keep producer-side target setup state separate from boundary-consumer target
  ownership in the CA model.
  `SETC.TGT` / equivalent setup rows publish a live target source, but once a
  `RET/IND/ICALL` boundary row enters backend ownership, capture its consumed
  target (and source row identity if tracked) on the boundary row itself.
  Later mutations of live producer state must not rewrite an already-owned
  boundary target.
- Keep return-consumer metadata distinct from generic `ret` branch kind.
  `FRET.RA`, `FRET.STK`, and `BSTART.RET` consuming `SETC.TGT` are different
  backend ownership paths and should be preserved in CA owner state and trace
  metadata (for example on `FLS/CMT`) instead of collapsing to only
  `branch_kind=ret`.
- Keep precise return-target fault causes distinct on `FLS` as well.
  When the recovery owner raises precise `RET/IND/ICALL` target faults
  (for example missing dynamic target state or a non-`BSTART` target), the CA
  trace should surface the exact architectural fault class on the `FLS` row and
  preserve the live `return_kind`; do not collapse these rows into a generic
  BRU-recovery fault once return-consumer ownership is already modeled.
- Preserve precise trap payloads on `FLS/CMT`, not only the trap class.
  If the CA model already carries precise recovery traps with `traparg0`
  (for example boundary source PC on BRU/RET target faults), keep that payload
  visible in stage-trace events and `linxtrace` output so DFX can identify the
  exact failing owner row without having to fall back to commit JSONL only.
- Preserve boundary target-owner identity on `FLS/CMT` for dynamic control
  consumers.
  When a `RET/IND/ICALL` boundary consumes target state published by an earlier
  owner row (`SETC.TGT`, `FRET.*`, or equivalent), keep that owner-row identity
  visible in CA trace metadata instead of collapsing everything onto the
  boundary row alone. DFX needs to correlate the consuming boundary with the
  producer row that supplied the dynamic target.
- Apply the same owner discipline to returning call headers.
  If a `CALL` header gets its return label from adjacent `SETRET/C.SETRET` or a
  fused returning form, keep the materializing owner-row identity in CA owner
  state, restore it with checkpoints, and expose it on `CMT` for the call
  header. The call boundary row and the target-materializing row are not always
  the same instruction.
- Preserve attempted owner-row identity on precise call-header faults too.
  A strict-mode `SETRET/C.SETRET/HL.SETRET` adjacency fault is still an
  attempted return-label materialization, so `FLS/CMT` metadata should identify
  the faulting `SETRET` row as the target-owner row instead of dropping owner
  identity just because materialization failed.
- Preserve call-header materialization kind on `FLS/CMT`, not only owner row.
  Returning call headers reached by a fused call form and returning call
  headers materialized by adjacent `SETRET/C.SETRET/HL.SETRET` are different
  backend ownership paths. Keep an explicit materialization kind in CA owner
  state and surface it in trace so DFX does not have to infer it indirectly
  from row identity alone.
- Keep call-return materialization alive as return-source owner state until
  `RET` consumes it.
  Do not treat fused-call or adjacent-`SETRET` materialization as a short-lived
  call-header-only annotation. The backend CA model should preserve the live
  return-label source (owner row and materialization kind) across later
  boundaries/checkpoint restore so `FRET.RA` recovery and validation can use the
  real source metadata instead of falling back to row-local surrogates.
- If `SETC.TGT` copies a live call-return label into dynamic-target state,
  preserve the exact fused-vs-adjacent materialization kind through later
  `RET`/`IND`/`ICALL` consumers, not only a coarse source class.
  Once a dynamic boundary consumes target state derived from live return-label
  ownership, `FLS/CMT` should still be able to distinguish `fused_call` from
  `adjacent_setret` on the consuming boundary row; do not collapse that path to
  generic `call_return_*` source metadata only.
- Preserve explicit dynamic-target producer kind alongside owner-row identity.
  For dynamic control consumers, `uopN` as the target owner is not sufficient
  DFX metadata by itself. Keep whether the target was produced by `SETC.TGT`,
  `FRET.RA`, or `FRET.STK` in live CA owner state and on `FLS/CMT`, especially
  for `IND`/`ICALL` rows where consumer-side `return_kind` may be absent.
- Model `SETC.TGT in the same block` as an epoch-owned recovery contract, not
  just a boolean presence check.
  If a dynamic boundary consumes target state whose setup epoch does not match
  the boundary block epoch, raise a precise stale-setup fault distinct from
  `dynamic_target_missing`; do not collapse owner-state mismatch into generic
  absence.
- Preserve both target setup epoch and consuming boundary epoch on `FLS/CMT`
  for stale dynamic-target faults.
  Once stale dynamic-target recovery is modeled precisely, the CA trace should
  expose the setup-vs-boundary epoch mismatch directly instead of leaving DFX
  with only a coarse `dynamic_target_stale_*` class string.
- If `SETC.TGT` copies a live return label, preserve the original source-owner
  row and source epoch separately from the copied setup epoch.
  In the CA model, a stale return-derived target is not the same thing as a
  stale architectural target setup. Keep the copied `SETC.TGT` owner/setup
  epoch and the original return-label source owner/epoch as distinct live owner
  state, and surface both on `FLS/CMT`.

## When merging LinxCore PRs

After merging to `LinxISA/LinxCore`, bump the superproject gitlink:

- In the LinxISA superproject checkout, update the `rtl/LinxCore` submodule pointer on `main`, PR + merge.

## Skill evolve loop (mandatory closeout)

- At closeout, decide `skill-evolve: update` or `skill-evolve: no-update`.
- Update this skill only if the run produced material reusable findings:
  - new block/BID/ROB/flush invariant,
  - new mandatory LinxCore gate/evidence requirement,
  - new recurring debug path that changes triage order.
- Do not update this skill for minor tuning, wording cleanup, or one-off local fixes.
- If updating, keep scope narrow and validate with:
  - `python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/zhoubot/linx-isa/skills/linx-skills/linx-core`
  - `python3 /Users/zhoubot/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main`
