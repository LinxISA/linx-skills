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

## Chisel lane bring-up gates

For the Chisel replacement lane under `rtl/LinxCore/chisel`, use the repo-local
wrappers rather than invoking `sbt` directly. The wrappers source
`tools/chisel/chisel_env.sh`, which prefers Homebrew `openjdk@17` when
`JAVA_HOME` is unset.

Current Phase 0/0B/1/2/5-prep gate sequence:

```bash
cd /Users/zhoubot/linx-isa/rtl/LinxCore
bash tools/chisel/build_chisel.sh
bash tools/chisel/run_chisel_tests.sh --only InterfaceBundles
bash tools/chisel/run_chisel_tests.sh --only F4DecodeWindow
bash tools/chisel/run_chisel_tests.sh --only FrontendInstructionBuffer
bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeIngress
bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage
bash tools/chisel/run_chisel_tests.sh --only FrontendFetchPacketSource
bash tools/chisel/run_chisel_tests.sh --only ROBID
bash tools/chisel/run_chisel_tests.sh --only ROBEntryStatus
bash tools/chisel/run_chisel_tests.sh --only ROBEntryBank
bash tools/chisel/run_chisel_tests.sh --only ROBFlushPrune
bash tools/chisel/run_chisel_tests.sh --only DispatchROBAllocator
bash tools/chisel/run_chisel_tests.sh --only FullBidRecoveryBridge
bash tools/chisel/run_chisel_tests.sh --only RecoveryCleanupControl
bash tools/chisel/run_chisel_tests.sh --only GPRRenameCheckpoint
bash tools/chisel/run_chisel_tests.sh --only ScalarDecodeRenameBridge
bash tools/chisel/run_chisel_tests.sh --only TULinkRename
bash tools/chisel/run_chisel_tests.sh --only TULinkRelationCmap
bash tools/chisel/run_chisel_tests.sh --only TULinkRetireCommandPath
bash tools/chisel/run_chisel_tests.sh --only TULinkFlushSequencePublisher
bash tools/chisel/run_chisel_tests.sh --only TULinkLocalBlockCommitFanout
bash tools/chisel/run_chisel_tests.sh --only TULinkLocalBankArray
bash tools/chisel/run_chisel_tests.sh --only TULinkRecoveryCleanupPath
bash tools/chisel/run_chisel_tests.sh --only TULinkFlushSourceSelector
bash tools/chisel/run_chisel_tests.sh --only ScalarTURenameBridge
bash tools/chisel/run_chisel_tests.sh --only DecodeLoadStoreIdAssign
bash tools/chisel/run_chisel_tests.sh --only StoreSplitPayload
bash tools/chisel/run_chisel_tests.sh --only StoreDispatchQueues
bash tools/chisel/run_chisel_tests.sh --only StoreDispatchToSTQ
bash tools/chisel/run_chisel_tests.sh --only STQInsertProbe
bash tools/chisel/run_chisel_tests.sh --only StoreDispatchSTQPath
bash tools/chisel/run_chisel_tests.sh --only DecodeRenameQueue
bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath
bash tools/chisel/run_chisel_tests.sh --only STQFlushPrune
bash tools/chisel/run_chisel_tests.sh --only STQEntryBank
bash tools/chisel/run_chisel_tests.sh --only STQCommitQueue
bash tools/chisel/run_chisel_tests.sh --only STQCommitDrain
bash tools/chisel/run_chisel_tests.sh --only SCBCommitIngress
bash tools/chisel/run_chisel_tests.sh --only SCBCommitBridge
bash tools/chisel/run_chisel_tests.sh --only SCBEgressSelect
bash tools/chisel/run_chisel_tests.sh --only SCBLookupControl
bash tools/chisel/run_chisel_tests.sh --only SCBStateUpdate
bash tools/chisel/run_chisel_tests.sh --only SCBRowBank
bash tools/chisel/run_chisel_tests.sh --only SCBResponseDecode
bash tools/chisel/run_chisel_tests.sh --only SCBResponseBuffer
bash tools/chisel/run_chisel_tests.sh --only SCBResponseRetryQueue
bash tools/chisel/run_chisel_tests.sh --only SCBResponseRetrySelect
bash tools/chisel/run_chisel_tests.sh --only STQSCBCommitPath
bash tools/chisel/run_chisel_tests.sh --only MDBConflictDetect
bash tools/chisel/run_chisel_tests.sh --only MDBSSIT
bash tools/chisel/run_chisel_tests.sh --only MDBQueueFanout
bash tools/chisel/run_chisel_tests.sh --only LoadStoreForwarding
bash tools/chisel/run_chisel_tests.sh --only LoadForwardPipeline
bash tools/chisel/run_chisel_tests.sh --only LoadInflightQueue
bash tools/chisel/run_chisel_tests.sh --only LoadReplayWakeup
bash tools/chisel/run_chisel_tests.sh --only LoadRefillWakeup
bash tools/chisel/run_chisel_tests.sh --only CommitTrace
bash tools/chisel/run_chisel_tests.sh --only FlushControl
bash tools/chisel/run_chisel_tests.sh --only BROB
bash tools/chisel/run_chisel_tests.sh --only BrobOrderState
bash tools/chisel/run_chisel_tests.sh --only BrobStoreRangeState
bash tools/chisel/run_chisel_brob_order_state_probe.sh
bash tools/chisel/run_chisel_brob_store_range_state_probe.sh
bash tools/chisel/run_chisel_brob_store_count_publisher_probe.sh
bash tools/chisel/run_chisel_decode_load_store_id_assign_probe.sh
bash tools/chisel/run_chisel_tests.sh --only BlockScalarDoneSequencer
bash tools/chisel/run_chisel_tests.sh --only BlockMarkerLifecycle
bash tools/chisel/run_chisel_tests.sh --only BlockMarkerDecodeContextSpec
bash tools/chisel/run_chisel_tests.sh --only BlockMarkerRetireSourceSerializer
bash tools/chisel/run_chisel_tests.sh --only ReducedCommitROB
bash tools/chisel/run_chisel_tests.sh --only LinxCoreTop
bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendTraceTop
bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchTraceTop
bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute
bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendAluTraceTop
bash tools/chisel/run_chisel_tests.sh --only ReducedScalarRegisterFile
bash tools/chisel/run_chisel_tests.sh --only ReducedScalarIssueQueue
bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendRfAluTraceTop
bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop
bash tools/chisel/run_chisel_rob_bookkeeping.sh --robid-only
bash tools/chisel/run_chisel_rob_bookkeeping.sh --reduced-rob
bash tools/chisel/run_chisel_reduced_rob_xcheck.sh
bash tools/chisel/run_chisel_top_xcheck.sh
bash tools/chisel/run_chisel_trace_replay_xcheck.sh
bash tools/chisel/run_chisel_frontend_trace_top_lint.sh
bash tools/chisel/run_chisel_frontend_trace_top_xcheck.sh
bash tools/chisel/run_chisel_frontend_fetch_trace_top_xcheck.sh
bash tools/chisel/run_chisel_frontend_alu_trace_top_xcheck.sh
bash tools/chisel/run_chisel_frontend_rf_alu_trace_top_xcheck.sh
bash tools/chisel/run_chisel_frontend_fetch_rf_alu_trace_top_xcheck.sh
bash tools/chisel/build_frontend_fetch_rf_alu_qemu_fixture_elf.sh --out-dir generated/r100-live-qemu-fixture
bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh \
  --elf generated/r100-live-qemu-fixture/frontend_fetch_rf_alu_qemu_fixture.elf \
  --expected-rows 3 --capture-rows 3 --pc-lo 0x10002 --pc-hi 0x1000b \
  --max-seconds 5
bash tools/chisel/run_chisel_verilator_lint.sh
python3 tools/chisel/trace_schema_adapter.py --self-test
bash tools/chisel/run_chisel_qemu_crosscheck.sh --dry-run
bash tools/chisel/run_chisel_qemu_trace_replay_xcheck.sh --dry-run
```

For any non-dry-run comparison routed through
`tools/chisel/run_chisel_qemu_crosscheck.sh`, inspect and preserve
`<report-dir>/crosscheck_manifest.json` with the rest of the evidence bundle.
The manifest records raw traces, normalized traces, comparator reports,
selected QEMU binary, `max_commits`, `normalize_rows`, row counts, mismatch
summary, CBSTOP summary, and LinxCore/superproject git context. The wrapper
must still emit the manifest on comparator failure and then return the
comparator status.
Generated-RTL Verilator harnesses must emit commit JSONL through
`tools/chisel/commit_trace_jsonl.h` rather than open-coded per-harness JSON
strings. The helper owns QEMU-shaped architectural fields and DUT sidebands
(`valid`, `seq/cycle/slot`, `bid/gid/rid`, ROB id, and `block_bid`); harnesses
own only top-specific pin conversion. This preserves model `CommitInfo`
identity separately from the `BID_W`-bit hardware block BID and prevents
schema drift before live Chisel trace writers are added.
For QEMU trace replay, keep raw replay/normalization depth separate from the
architectural compare depth: QEMU metadata rows may be filtered before compare,
so `run_chisel_qemu_trace_replay_xcheck.sh` normalizes a wider raw window and
slices the replay input to the smallest prefix containing the requested
non-metadata commits.
Every `tools/qemu/run_qemu_commit_trace.sh --max-seconds N` invocation must be
a real wall-clock bound. The runner uses `timeout`/`gtimeout` when present and
otherwise its Python process-group fallback; a timeout returns `124` after
terminating QEMU. Do not treat a host without GNU coreutils as permission to
run an unbounded CoreMark/QEMU capture.
For PC-filtered QEMU-only preflights that are candidates for generated-RTL
promotion, exact memory-PC guards are necessary but not sufficient. The reduced
preview must also prove that the Verilator harness can reconstruct starting
architectural register state, for example through
`state_seed_audit.status="ready"` in
`tools/chisel/search_replay_liq_pc_filter_preflights.py` schema v2. If the
first non-skipped reduced row has memory/destination data but no visible source
operands, treat the PC filter as generated-RTL blocked even when QEMU-only
memory-PC guards pass; the DUT would otherwise start from reset/RF defaults
while QEMU already executed hidden predecessor state. That blocked state can be
reopened only by citing a matching raw-prefix RF seed artifact, for example
one built with `tools/chisel/build_frontend_fetch_rf_seed.py` from the
unfiltered QEMU trace and passed to generated RTL through `--rf-seed` /
`FETCH_RF_SEED`. A seeded comparator pass proves launch-state reconstruction
only; replay-LIQ replacement proof still needs nonzero eligible-store,
ResolveQ, MDB, LIQ allocation, replay-output, and row-mutation counters.
In `--elf` mode, `--replay-rows` is also the raw FIFO capture cap. The wrapper
must kill the prefix reader and fail with an empty-trace error if QEMU exits
before producing rows; do not leave agents blocked on a FIFO. Direct-boot
CoreMark-style ET_DYN images currently map load segments at `0x40000000`,
while the Linx QEMU `virt` machine defaults to 128 MiB of RAM. Use trailing
QEMU args with explicit memory for that class of replay, for example:

```bash
bash tools/chisel/run_chisel_qemu_trace_replay_xcheck.sh \
  --elf tests/benchmarks/build/coremark_real.elf \
  --max-commits 4 \
  --replay-rows 128 \
  --max-seconds 10 \
  -- -nographic -monitor none -machine virt -m 1280M \
     -kernel tests/benchmarks/build/coremark_real.elf
```

## Chisel module agent loop

Use `rtl/LinxCore/docs/chisel/agent-loop.md` as the operational runbook for
multi-agent Chisel development. Each module packet must:

- record current `rtl/LinxCore` and `model/LinxCoreModel` SHAs before edits;
- learn behavior from LinxCoreModel C++ owner files before writing Chisel;
- update the module Markdown spec before promotion;
- for scalar LSU sizing changes, keep three independent domains explicit:
  physical queue/storage capacity (`stqEntries`, `commitQueueEntries`,
  `scbEntries`, LIQ/ResolveQ/MDB depths), ROB slot-plus-wrap identity
  (`robEntries` for BID/GID/RID), and full memory-order identity
  (`lsidWidth`, normally 32). Never derive one domain from another. Add at
  least one unequal-capacity elaboration, such as 16 STQ rows with 8 ROB
  entries and a 40-bit LSID, and assert physical index/mask, ROB identity, and
  LSID widths independently;
- keep ROB/commit/flush/BROB/QEMU cross-check infrastructure as the first proof
  surface for replacement evidence;
- For BROB non-flush promotion, publish an exact per-STID `(head BID,
  prefix count)` window. An unsafe head, stale slot, hole, or exception must
  produce no authorization, and consumers must not use the youngest safe BID
  as an unsigned threshold. A store commit retained while waiting for this
  proof must carry STID, full block BID, and instruction identity, clear on the
  same accepted recovery as STQ/BROB state, and pass both the BROB rollover
  probe and `run_chisel_store_non_flush_gate_probe.sh` before promotion.
- run the narrow module gate plus affected cross-check gates;
- inspect `crosscheck_manifest.json` for every generated-RTL or QEMU/DUT
  comparison that routes through the common cross-check wrapper; R151 and later
  manifests must include `git.linxcore`, `git.linxcore_model`, `git.qemu`, and
  `git.superproject` before the run is cited as replacement evidence;
- for QEMU row replay, verify the reported `qemu-replay-raw-rows` and
  `qemu-replay-arch-rows` before treating the manifest as evidence;
- for CoreMark or other direct-boot benchmark ELF replay, pass explicit QEMU
  memory if the ELF program headers map above the default 128 MiB RAM window;
- for replay-LIQ MDB promotion, do not claim conflict record or fanout
  evidence from aggregate store-probe and ResolveQ counters. Prove a same-cycle
  store-detect/ResolveQ overlap, or a model-equivalent retained/replayed store
  probe, and require nonzero `mdb_conflict_valid`, `mdb_fanout_record_*`,
  BMDB, and SSIT counters while keeping unrelated lookup/wait-plan counters
  explicitly guarded;
- for replay-wake promotion, do not treat top-local sideband counters as proof
  that the LIQ child consumed a wake when child clear masks disagree. Inspect
  final top assignment order and tie-off helpers for the actual
  `ReducedLoadReplayLiqAllocPath.io.replayWake*` inputs before changing
  `LoadReplayWakeup` predicate logic;
- for reduced BFU body-cut work after R153, do not arm body cuts from static
  boundary geometry alone. A conditional `BSTART` can close the previous model
  body but still fall through at runtime, so cut-eligible prediction must come
  from accepted resolved body-end evidence or the local window trained by that
  evidence. Use the resolved body-end row as the same-cycle cold-cut fallback
  because `ReducedBfuGeometryPredictionLatch` is registered. Keep
  `ReducedBfuBodyCutArm` as diagnostic/oracle comparison until a real
  branch/BFU resolver replaces the external replay source. Drive local
  body-window D1 scans from registered F4/IB entry validity rather than source out-fire
  to avoid body-cut/source-advance combinational cycles;
- close with `skill-evolve: update ...` or `skill-evolve: no-update ...`.

Do not treat a frontend/backend Chisel module as replacement evidence merely
because its unit test passes. It needs monitored commit/stage-owner visibility
through the neutral cross-check path before it can displace pyCircuit evidence.

## Chisel speed loop

Use this abbreviated loop before opening the full packet ledger. It exists to
avoid repeating the long-session pattern of rereading every historical R packet,
rerunning broad status checks, and rediscovering toolchain facts.

1. Read `rtl/LinxCore/docs/chisel/integrated-development-flow.md` first, then
   only `rtl/LinxCore/docs/chisel/development-loop.md`, the assigned module
   spec, and the latest relevant rows in
   `rtl/LinxCore/docs/chisel/agent-loop.md`.
2. Record the four SHAs once: superproject, `rtl/LinxCore`,
   `model/LinxCoreModel`, and `emulator/qemu`. Do not run repeated `git status`
   checks inside the same packet unless an edit, fetch, commit, or generated
   artifact changes the state.
3. Validate the Chisel environment once with the repo wrappers. Reuse
   `tools/chisel/chisel_env.sh`; do not call raw `sbt` from ad hoc working
   directories.
4. Run gates in tiers from the integrated flow: module unit gate first,
   adjacent owner gate second, generated-RTL/QEMU cross-check third, model or
   workload promotion fourth, full closure only at promotion.
5. For QEMU/DUT failures, stop at the first divergent architectural row and
   classify ownership before editing: `chisel`, `qemu`, `model`, `compiler`,
   `adapter`, `benchmark`, or `unknown`.
6. Update the module doc, gate evidence, and ledger in the same packet. If the
   finding is reusable across modules, update this skill once; otherwise close
   with `skill-evolve: no-update`.
7. After generated-RTL/QEMU evidence is captured, prune reproducible build
   intermediates before starting another broad sweep. Preserve report JSON,
   manifests, sideband stats, and trace snippets cited by docs, but remove
   `generated/**/obj_dir`, generated Verilog trees that wrappers can recreate,
   wave dumps, and compiler temporaries (`*.tmp`, `*.o`, `*.a`, `*.d`, `*.gch`).
   If an active generated-RTL run is producing large intermediates and the loop
   pivots, terminate that run cleanly before deleting its incomplete build dir.

Prefer bounded evidence windows while debugging. Scale CoreMark or direct-boot
windows only after the narrow module gate and the previous smaller cross-check
pass. Full cross-gate closure remains mandatory before claiming LinxCore
closure, but it is not the inner edit loop.

Toolchain facts from initial Chisel bring-up:

Compatibility terminology: historical Chisel module/test names such as
`F4DecodeWindow` remain literal code identifiers. In the bring-up notes below,
an "F4 slot/window" means a D1 decode slot/view read from F4/IB state; it never
defines a separate F4 decode stage.

- Homebrew `openjdk@17` works with the wrappers.
- Homebrew `sbt` 2.0.0 works when the project uses Scala `2.13.17`.
- Chisel is pinned to `7.3.0` in `chisel/build.sbt`.
- Phase 1 common interface work must run
  `bash tools/chisel/run_chisel_tests.sh --only InterfaceBundles` before
  frontend/decode/rename/LSU/ROB agents consume the shared bundle packet.
  `InterfaceBundles` preserves the 4-wide/64-bit pyCircuit widths, 12-bit
  opcode, 4-bit instruction length fields, 6-bit reg/ptag/ROB index defaults,
  32-bit scalar LSID, `BK_*` order,
  `REG_INVALID=0x3f`, `TRAP_BRU_RECOVERY_NOT_BSTART=0x0000b001`, and the split
  between model `bid/gid/rid` identity and hardware `blockBid`. The current
  fixed 64-bit `blockBid` bundle is legacy implementation shape: new contract
  work uses `BID_W`, and a width migration must update all producers,
  consumers, traces, and fixtures coherently.
- Phase 2 `F4DecodeWindow` is a legacy module name for a D1 decode-window
  helper; it is not architectural F4. Work on it must preserve LinxCoreModel `CheckMInstSize`
  instruction sizing: bit 0 clear gives 2 bytes unless header bits `[3:1]` are
  `111`, which gives 6 bytes; bit 0 set gives 4 bytes unless header bits
  `[3:1]` are `111`, which gives 8 bytes. The Chisel gate is
  `bash tools/chisel/run_chisel_tests.sh --only F4DecodeWindow`.
- Legacy decode-window/D1 work must keep 8-byte window slicing sequential and
  non-compacting: a candidate that does not fit invalidates that slot and all
  later slots; do not search forward for a later instruction. Flush masks D1
  and all slot-valid bits. Slot UIDs are `(pktUid << 3) | slot`.
- Full opcode decode, register/immediate extraction, macro-boundary standalone
  behavior, and D1/D2 uop construction are deferred until the Chisel opcode
  table/decode-owner modules exist; do not bury those behaviors in the legacy
  `F4DecodeWindow` transport helper.
- Phase 2 `FrontendInstructionBuffer` work must run
  `bash tools/chisel/run_chisel_tests.sh --only FrontendInstructionBuffer`.
  The buffer is a frontend-owned FIFO for `FrontendDecodePacket` records:
  preserve FIFO order, clear occupancy on flush, keep simultaneous push/pop
  occupancy stable, and keep full-state backpressure based on pre-cycle
  occupancy.
- Chisel frontend buffers must carry `checkpointId` as packet-owned state
  alongside PC/window/packet UID. Do not reconstruct F4/IB-to-D1 packet checkpoint
  identity from adjacent control wiring once a packet enters the Chisel
  frontend queue.
- Phase 2 `FrontendDecodeIngress` work must run
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeIngress`.
  Architecturally this is the F4/IB-to-D1 transport boundary: F4 is the fourth
  fetch stage and the instruction-buffer boundary, not a four-slot decode
  stage. The current implementation composes
  `FrontendInstructionBuffer` with `F4DecodeWindow`, pop only on
  `decodeReady && f4.d1.valid`, preserve no same-cycle push-to-D1 bypass,
  clear/mask both children on flush, and keep opcode decode, macro-boundary
  decode, and D1/D2 uop construction in later decode-owner modules.
- Phase 2/R39/R40 `FrontendDecodeStage` work must run
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage` plus the
  affected `F4DecodeWindow`, `FrontendDecodeIngress`, and `InterfaceBundles`
  gates. This module is the first D1 decode-shape owner after F4/IB: use the
  generated pyCircuit opcode metadata mask/match table, preserve the
  most-specific-mask rule (`decode16_meta`/`decode32_meta`/`decode48_meta`/
  `decode64_meta`), emit `DecodedUop` records with slot PC/raw/len/opcode and
  UID/checkpoint identity, and expose block/load/store sideband masks. R40 adds
  `FrontendOperandDecode` as the scalar field owner behind this stage: it
  consumes generated `rdKind`/`rs1Kind`/`rs2Kind`/`immKind`, emits reg6
  architectural GPR source/destination tags in pyCircuit `srcl`/`srcr`/`srcp`
  order, and forms the common scalar immediates already covered by
  `src/common/decode.py`. Keep LSID allocation, D2 queueing, block header
  mutation, store split rewrite, T/U/SGPR/tile/vector operand classes,
  shift/source-type sidebands, and rename/ROB admission in later owners.
- Phase 5/R41 `ScalarDecodeRenameBridge` work must run
  `bash tools/chisel/run_chisel_tests.sh --only ScalarDecodeRenameBridge` plus
  affected `GPRRenameCheckpoint`, `FrontendDecodeStage`,
  `DispatchROBAllocator`, and reduced ROB bookkeeping gates. This bridge is
  the first D2 decode-to-rename staging owner: consume one `DecodedUop`, map
  scalar GPR sources through `GPRRenameCheckpoint`, optionally allocate one
  scalar GPR destination, emit a `RenamedUop`, and emit the matching
  `CommitTraceRow` allocation request for ROB/BROB allocation. Keep
  `dec_ren_q` registration, width-wide rename, automatic `isLastInBlock`
  checkpoint capture, ready-table initialization, LSID allocation, store split
  rewrite, T/U/SGPR/tile/vector rename, live top wiring, and commit side
  effects in later owners. The bridge must reject any non-scalar-GPR operand
  class or destination kind; `FrontendRegAliasClassify` is the decode owner
  that maps reg6 aliases outside the 24-entry model GPR namespace before the
  bridge sees them.
- Phase 5/R42 `DecodeRenameROBPath` work must run
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath` plus
  affected `ScalarDecodeRenameBridge`, `FrontendDecodeStage`,
  `DispatchROBAllocator`, `GPRRenameCheckpoint`, reduced ROB bookkeeping, top
  xcheck, and `run_chisel_qemu_crosscheck.sh --dry-run` gates. This path is
  the first reduced frontend/backend composition owner: connect
  `FrontendDecodeStage`, `ScalarDecodeRenameBridge`, and
  `DispatchROBAllocator`; select one decoded slot; stamp temporary backend
  identity from allocator cursors before rename; and allocate a real BROB/ROB
  row. When composing with `DispatchROBAllocator`, drive allocator
  `allocValid` from `ScalarDecodeRenameBridge.robAllocAttemptValid`, not from
  the accepted allocation event, so ROB duplicate-identity ready calculation
  sees a stable request row without feeding allocator ready back into
  allocator valid. R44 adds the registered `dec_ren_q` owner, R45 adds the
  reduced memory-order ID owner, R46 adds the renamed store payload split
  owner, and R47 connects generated store metadata plus reduced store-dispatch
  handoff; keep width-wide rename, enqueue-time ROB reservation, full
  `load_id`/`sid` payload carry, STA/STD execution, STQ mutation, automatic
  checkpoint capture, ready-table initialization,
  T/U/SGPR/tile/vector operands, full block retire, and live top-level commit
  rows in later owner packets.
- Phase 5/R43 `FrontendRegAliasClassify` / `FrontendOperandDecode` work must
  run `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage` plus
  affected `ScalarDecodeRenameBridge`, `DecodeRenameROBPath`, top xcheck,
  `run_chisel_qemu_crosscheck.sh --dry-run`, `build_chisel.sh`, and
  `run_chisel_verilator_lint.sh` gates. This owner preserves the model scalar
  reg6 alias contract: source tags `0..23` are `OperandClass.P`, `24..27` are
  `OperandClass.T`, `28..31` are `OperandClass.U`; destination tags `0..23`
  are `DestinationKind.Gpr`, tag `31` is the T queue, and tag `30` is the U
  queue. Destination aliases intentionally do not use the source T/U ranges.
  Keep T/U queue consumption, SGPR/tile/vector operands, LSID/SID allocation,
  store split, and full enqueue-time ROB reservation in later owners.
- Phase 5/R44 `DecodeRenameQueue` / `DecodeRenameROBPath` work must run
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameQueue` plus
  affected `DecodeRenameROBPath`, `ScalarDecodeRenameBridge`,
  `FrontendDecodeStage`, `DispatchROBAllocator`, reduced ROB bookkeeping, top
  xcheck, `run_chisel_qemu_crosscheck.sh --dry-run`, `build_chisel.sh`, and
  `run_chisel_verilator_lint.sh` gates. `DecodeRenameQueue` is the registered
  raw decoded-uop boundary corresponding to model `dec_ren_q`: enqueue raw
  `DecodedUop` payloads, expose queue push/pop and occupancy observability,
  clear on frontend/backend recovery cleanup in the reduced path, and pop only
  when scalar rename plus ROB allocation accept. Until an enqueue-time ROB
  reservation owner exists, stamp allocator BID/RID identity at the queue head
  before `ScalarDecodeRenameBridge`; do not stamp or reserve allocator cursors
  for multiple queued rows at enqueue because that duplicates identities. Later
  top-level frontend integration must advance D1 and consume F4/IB only on `decodeReady` /
  queue acceptance.
- Phase 5/R45 `DecodeLoadStoreIdAssign` / `DecodeRenameROBPath` work must run
  `bash tools/chisel/run_chisel_tests.sh --only DecodeLoadStoreIdAssign` plus
  affected `DecodeRenameROBPath`, `DecodeRenameQueue`,
  `ScalarDecodeRenameBridge`, `FrontendDecodeStage`,
  `DispatchROBAllocator`, reduced ROB bookkeeping, top xcheck,
  `run_chisel_qemu_crosscheck.sh --dry-run`, `build_chisel.sh`, and
  `run_chisel_verilator_lint.sh` gates. `DecodeLoadStoreIdAssign` is the first
  reduced STID0 memory-order ID owner after frontend decode: stamp the
  selected decoded load/store/DCZVA row with the pre-increment 32-bit `lsID`
  only when `DecodeRenameQueue` accepts the row, expose 64-bit `load_id` and
  `sid` serial-counter observability, and clear/restore counters through the
  recovery hook. This owner may expose `storeSplitIntent`, but must not clone
  STA/STD rows, rewrite PCR store sources, carry `load_id`/`sid` through common
  uop bundles, or perform width-wide same-cycle slot-order allocation. R46/R47
  consume the split intent plus opcode-derived pair/cache/PCR metadata in the
  store payload handoff; real store queue mutation remains a later owner.
- Phase 5/R46 `StoreSplitPayload` work must run
  `bash tools/chisel/run_chisel_tests.sh --only StoreSplitPayload` plus
  affected `InterfaceBundles`, `DecodeLoadStoreIdAssign`,
  `ScalarDecodeRenameBridge`, `DecodeRenameROBPath`, `DecodeRenameQueue`,
  `FrontendDecodeStage`, `DispatchROBAllocator`, reduced ROB bookkeeping, top
  xcheck, `run_chisel_qemu_crosscheck.sh --dry-run`, `build_chisel.sh`, and
  `run_chisel_verilator_lint.sh` gates. `StoreSplitPayload` consumes renamed
  store rows carrying `storeSplitIntent`, pair/cache-maintain suppression, and
  PCR metadata. Split stores must fire STA and STD atomically with shared
  `bid/gid/rid/blockBid/lsid` identity; ordinary STA payloads zero source 0;
  PCR STA payloads preserve source 0 and use store data source index 1; pair
  and cache-maintain stores remain single `ST_ALL` payloads. This owner must
  not allocate or mutate STQ/SCB/MDB state. R47 integrates it behind the
  reduced decode/rename/ROB path for payload observability only; R48 adds the
  finite STA/STD dispatch queues, while STA/STD execution and STQ residency
  remain later owners.
- Phase 5/R47 generated store metadata / reduced store-dispatch handoff work
  must run `sbt --client --error 'Test / compile'` plus affected
  `FrontendDecodeStage`, `DecodeLoadStoreIdAssign`, `StoreSplitPayload`,
  `ScalarDecodeRenameBridge`, `DecodeRenameROBPath`, `DecodeRenameQueue`,
  `InterfaceBundles`, `DispatchROBAllocator`, reduced ROB bookkeeping, top
  xcheck, `run_chisel_qemu_crosscheck.sh --dry-run`, `build_chisel.sh`, and
  `run_chisel_verilator_lint.sh` gates. Generated decode metadata now drives
  load/store-pair, PCR-store, and cache-maintain split sidebands into the
  reduced path. When connecting `StoreSplitPayload` behind scalar rename, compute
  store-dispatch readiness from the queued decoded row, not from
  `StoreSplitPayload.inReady` or the accepted renamed output. Unsplit stores
  require only STA readiness; split stores require both STA and STD readiness;
  gate `ScalarDecodeRenameBridge.outReady` with that readiness plus downstream
  renamed-output readiness. `StoreSplitPayload` consumes only the accepted
  renamed row and emits STA/STD/ST_ALL payload observability. Do not create a
  ready/valid loop through the splitter, and do not allocate or mutate
  STQ/SCB/MDB state in this reduced path.
- Phase 5/R48 `StoreDispatchQueues` / queue-backed store-dispatch handoff work
  must run `sbt --client --error 'Test / compile'` plus affected
  `StoreDispatchQueues`, `DecodeRenameROBPath`, `StoreSplitPayload`,
  `DecodeLoadStoreIdAssign`, `ScalarDecodeRenameBridge`, `DecodeRenameQueue`,
  `STQEntryBank`, `InterfaceBundles`, `DispatchROBAllocator`, reduced ROB
  bookkeeping, top xcheck, `run_chisel_qemu_crosscheck.sh --dry-run`,
  `build_chisel.sh`, and `run_chisel_verilator_lint.sh` gates.
  `StoreDispatchQueues` is the finite queue owner for the model
  `pe_iex_sta_array`/`pe_iex_std_array` dispatch boundary behind scalar
  rename. Its `staReady` and `stdReady` are capacity-only and flush-qualified;
  they must not depend on `staIn/stdIn/unsplitIn.valid` or on protocol-error
  diagnostics, because those payload-valid bits are produced by
  `StoreSplitPayload` from accepted rename output. Protocol-shape errors must
  remain observable and suppress enqueue, but not feed upstream readiness.
  Split stores enqueue STA and STD atomically or enqueue neither; unsplit
  stores enqueue only the STA-side `ST_ALL` queue. Do not compute address/data,
  allocate STQ rows, or mutate STQ/SCB/MDB state in this queue owner. Future
  store-execution packets must consume queue heads and build executed STQ
  insert requests rather than moving queue or STQ state back into rename.
- Phase 5/R49 `StoreDispatchToSTQ` request-bridge work must run
  `sbt --client --error 'Test / compile'` plus affected
  `StoreDispatchToSTQ`, `StoreDispatchQueues`, `STQEntryBank`,
  `StoreSplitPayload`, `DecodeRenameROBPath`, `InterfaceBundles`, reduced ROB
  bookkeeping, top xcheck, `run_chisel_qemu_crosscheck.sh --dry-run`,
  `build_chisel.sh`, and `run_chisel_verilator_lint.sh` gates.
  `StoreDispatchToSTQ` consumes queue heads only after explicit STA/STD
  execution results are valid and forms typed `STQStoreRequest` rows. It must
  keep address generation and store-data selection outside the bridge. When
  both executed candidates can insert, STA wins, matching the model's STA
  phase before STD phase. If a present STA candidate cannot insert but the STD
  candidate can insert, STD must be allowed to bypass; this preserves the model
  progress case where a full STQ rejects a new address allocation while still
  accepting a complementary data half merge. Do not force the R48 atomic
  rename-time split pair to enter STQ atomically. R61 makes this bridge a
  preservation owner for row-owned T/U sidecars: copy `tSeq/uSeq` and
  `tuDst*` from `StoreSplitIssuePayload` into `STQStoreRequest`; do not
  re-disable those fields in the bridge.
- Phase 5/R50 `STQInsertProbe` / `StoreDispatchSTQPath` work must run
  `sbt --client --error 'Test / compile'` plus affected `STQInsertProbe`,
  `StoreDispatchSTQPath`, `StoreDispatchToSTQ`, `StoreDispatchQueues`,
  `STQEntryBank`, `StoreSplitPayload`, `DecodeRenameROBPath`,
  `InterfaceBundles`, reduced ROB bookkeeping, top xcheck,
  `run_chisel_qemu_crosscheck.sh --dry-run`, `build_chisel.sh`, and
  `run_chisel_verilator_lint.sh` gates. `STQInsertProbe` is the shared
  read-only STQ insert-readiness predicate over the live `STQEntryBank` row
  image, and `STQEntryBank` must use the same predicate internally. Full
  queue-to-STQ composition must compute STA and STD insert readiness with
  independent probes before selecting a request; do not feed a selected-only
  `STQEntryBank.insertReady` shortcut back into both candidates. STA still
  wins when both executed candidates are ready, but a mergeable STD must be
  allowed to bypass a present STA that cannot allocate into a full STQ.
  Address generation, store-data selection, load-conflict probes, ready-table
  updates, memory trace side effects, and live top integration remain later
  owners.
- Phase 5/R51 `TULinkRename` work must run
  `sbt --client --error 'Test / compile'` plus affected `TULinkRename`,
  `FrontendDecodeStage`, `ScalarDecodeRenameBridge`, `DecodeRenameROBPath`,
  and reduced ROB bookkeeping gates. `TULinkRename` is a standalone scalar T/U
  local-register rename owner, not an extension of scalar GPR rename. Preserve
  the model `LocalRegMgr` contract for `OPD_TLINK` and `OPD_ULINK`: capture
  `tSeq`/`uSeq` from `mapQAllocPtr[0]` before destination allocation; resolve
  sources from `mapQAllocPtr[0] - (offset + 1)` using the frontend T/U
  relative tag; allocate destinations from the circular scalar local
  `allocPtr[0]`; and stall on `usedEntrySize[0] + 1 > mapSize` or
  `usedPSize[0] + 1 > pSize`. Do not use the scalar GPR first-free physical
  tag policy for T/U queues. Keep T/U release, ready-table mutation, flush
  cleanup, multi-PE/thread banking, and unified renamed-uop composition in
  later owner packets.
- Phase 5/R52 `TULinkRename` cleanup work must run
  `sbt --client --error 'Test / compile'` plus affected `TULinkRename`,
  `FlushControl`, `RecoveryCleanupControl`, `ScalarDecodeRenameBridge`, and
  reduced ROB bookkeeping gates. T/U cleanup must preserve the scalar
  `LocalRegMgr` split between marking a row retired and freeing it: plain
  `ReportRetired(seq, false)` only marks the mapQ row, direct dealloc release
  may free only the current deallocation head, and `ReportBlockCommit(bid)`
  releases only consecutive retired rows at the deallocation head with matching
  BID. Flush pruning for non-base requests must use both local mapQ sequence
  and RID ordering:
  `(flush.bid, localSeq) <= (row.bid, row.seq)` and
  `(flush.bid, flush.rid) <= (row.bid, row.rid)`. When the flushed instruction
  itself owns a T/U destination, the recovery publisher must supply the
  previous local sequence, matching model `GetPrevRegSeq`; do not infer this
  from ROB RID alone. Keep the shared ROB/LSU sequence publisher,
  relation-cmap release policy, ready-table mutation, and unified renamed-uop
  composition in later owner packets.
- Phase 5/R53 `TULinkFlushSequencePublisher` work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkFlushSequencePublisher`, `TULinkRename`,
  `RecoveryCleanupControl`, `FlushControl`, and reduced ROB bookkeeping gates.
  The publisher must treat T/U local-register cleanup as a backend PE cleanup
  sideband, not scalar stack-rename cleanup: drive commands from
  `RecoveryCleanupIntent.backendFlushValid` plus the selected ROB/LSU row
  snapshot. Non-base cleanup requires that source row to match
  `(flush.bid, flush.rid, flush.stid)` and must report/suppress
  missing or mismatched sources rather than defaulting the local sequence. Apply
  the model `GetPrevRegSeq` adjustment only for the destination class owned by
  the flushed row: T destinations decrement only `tSeq`, U destinations
  decrement only `uSeq`. Keep live row-snapshot wiring into the cleanup path,
  relation-cmap release policy, ready-table
  mutation, and multi-PE/thread banking in later owner packets.
- Phase 5/R54 `TULinkRecoveryCleanupPath` work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkRecoveryCleanupPath`, `TULinkFlushSequencePublisher`,
  `TULinkRename`, `RecoveryCleanupControl`, `FlushControl`, and reduced ROB
  bookkeeping gates. The composition must wire publisher outputs directly into
  `TULinkRename.flush*` while keeping live ROB/LSU row selection behind an
  explicit `flushSource` input. If a non-base T/U cleanup is active but the
  selected row source is missing or mismatched, treat that as a recovery
  barrier: block local T/U rename, retire, and commit for the cycle instead of
  falling through to unrelated local-register maintenance. Keep
  relation-cmap release policy, ready-table mutation, and multi-PE/thread
  banking in later owner packets.
- Phase 5/R55 `TULinkFlushSourceSelector` work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkFlushSourceSelector`, `TULinkRecoveryCleanupPath`,
  `TULinkFlushSequencePublisher`, `RecoveryCleanupControl`, `FlushControl`,
  reduced ROB bookkeeping, trace-schema self-test, and Chisel QEMU dry-run
  gates. The selector is the ROB/LSU source-selection boundary for T/U cleanup
  sidebands; it is not the live row-storage owner. Non-base cleanup candidates
  match by `(flush.bid, flush.rid, flush.stid)`, while base-on-BID cleanup does
  not require a selected row source. If ROB and LSU both match the same
  non-base cleanup row, their payloads must agree exactly; otherwise suppress
  the selected source and let the recovery barrier block local T/U rename,
  retire, and commit for the cycle. Keep relation-cmap release policy,
  ready-table mutation, and multi-PE/thread banking in later owner packets.
- Phase 5/R56 `ROBEntryBank` T/U source-sidecar work must run
  `sbt --client --error 'Test / compile'` plus affected `InterfaceBundles`,
  `ROBEntryBank`, `DispatchROBAllocator`, `DecodeRenameROBPath`,
  `TULinkFlushSourceSelector`, `TULinkRecoveryCleanupPath`,
  `TULinkFlushSequencePublisher`, `RecoveryCleanupControl`, `FlushControl`,
  reduced ROB bookkeeping, trace-schema self-test, and Chisel QEMU dry-run
  gates. The row owner must store `stid`, row-owned `tSeq/uSeq`, and
  T/U destination class at allocation, then publish `robTULinkSource` only for
  an exact non-base `(flush.bid, flush.rid, flush.stid)` match. Base-on-BID
  cleanup must publish no local sequence source. The source payload must come
  from row sidecars captured from the rename snapshot, not from
  `CommitTraceRow.identity`, row index, or default zero sequences. Flush and
  deallocation must clear the sidecars with the row. `DispatchROBAllocator`
  forwards these sidecars, and reduced `DecodeRenameROBPath` now drives them
  from `ScalarTURenameBridge` live `SPERename`-equivalent snapshots before
  T/U destination rename. Keep LSU/STQ source sidecars, selector-to-cleanup
  composition, relation-cmap release policy, ready-table mutation, and
  multi-PE/thread banking in later owner packets.
- Phase 5/R58 `STQEntryBank` LSU T/U source-sidecar work must run
  `sbt --client --error 'Test / compile'` plus affected `STQEntryBank`,
  `STQFlushPrune`, `StoreDispatchToSTQ`, `StoreDispatchSTQPath`,
  `STQInsertProbe`, `STQCommitDrain`, `STQSCBCommitPath`,
  `TULinkFlushSourceSelector`, `TULinkRecoveryCleanupPath`, reduced ROB
  bookkeeping, trace-schema self-test, and Chisel QEMU dry-run gates. The STQ
  request and row owners must carry the model `MemReqBus` `tSeq/uSeq` sidecars
  plus T/U destination ownership, then publish `lsuTULinkSource` only for an
  exact non-base `(flush.bid, flush.rid, flush.stid)` row match. Keep this
  source separate from `STQFlushPrune`, whose pruning predicate remains the
  model LSU `(bid, lsId)` recovery rule. Split-store merge must preserve the
  first row's T/U source sidecars while filling address/data readiness, matching
  `STQ::mergeStore` and `STQueueEntryInfo::init`; do not overwrite them from a
  later complementary half. `StoreDispatchToSTQ` must preserve sidecars from
  `StoreSplitIssuePayload`; the reduced backend now drives live payload
  sidecar inputs from `ScalarTURenameBridge`.
  Keep relation-cmap release policy, ready-table mutation, and
  multi-PE/thread banking in later owner packets.
- Phase 5/R59 `DecodeRenameROBPath` reduced T/U cleanup source-composition
  work must run `sbt --client --error 'Test / compile'` plus affected
  `DecodeRenameROBPath`, `TULinkRecoveryCleanupPath`,
  `TULinkFlushSourceSelector`, `DispatchROBAllocator`, `StoreDispatchSTQPath`,
  reduced ROB bookkeeping, trace-schema self-test, and Chisel QEMU dry-run
  gates. The reduced backend may instantiate `TULinkRecoveryCleanupPath` as a
  diagnostic composition point with rename, retire, and commit inputs tied
  inactive until scalar and T/U rename state are merged. Drive
  `TULinkRecoveryCleanupPath.robSource` from
  `DispatchROBAllocator.robTULinkSource` and expose an external
  `lsuTULinkSource` input for the future STQ wrapper producer. The emitted
  diagnostics must prove whether ROB and LSU candidates agree for the same
  `(bid,rid,stid)`, whether one matching source was selected, or whether
  cleanup was blocked by a missing or conflicting source. R62 moves this
  diagnostic-only owner into `ScalarTURenameBridge`; do not reintroduce a
  second independent T/U cleanup state owner in `DecodeRenameROBPath`.
- Phase 5/R60 `DecodeRenameROBPath` integrated STQ-bank LSU source work must
  run `sbt --client --error 'Test / compile'` plus affected
  `DecodeRenameROBPath`, `StoreDispatchSTQPath`, `StoreDispatchToSTQ`,
  `STQEntryBank`, `TULinkRecoveryCleanupPath`, `TULinkFlushSourceSelector`,
  `DispatchROBAllocator`, reduced ROB bookkeeping, trace-schema self-test,
  Chisel QEMU dry-run, and top xcheck gates. The reduced backend may replace
  its internal `StoreDispatchQueues` shell with `StoreDispatchSTQPath` only if
  queue flush and STQ recovery flush remain separate: frontend/decode
  maintenance may clear dispatch queues through a queue-only flush, but must
  not become an STQ row-prune event. Drive
  `TULinkRecoveryCleanupPath.lsuSource` from the live
  `StoreDispatchSTQPath.lsuTULinkSource` output, and expose enough STQ insert,
  occupancy, flush, and source diagnostics to prove the source came from the
  STQ bank. R62 moves the cleanup path under `ScalarTURenameBridge`, where the
  publisher outputs mutate live T/U rename state.
- Phase 5/R61 store-dispatch T/U sidecar carry work must run
  `sbt --client --error 'Test / compile'` plus affected `StoreSplitPayload`,
  `StoreDispatchQueues`, `StoreDispatchToSTQ`, `StoreDispatchSTQPath`,
  `DecodeRenameROBPath`, `STQEntryBank`, `TULinkRecoveryCleanupPath`,
  `TULinkFlushSourceSelector`, `DispatchROBAllocator`, reduced ROB
  bookkeeping, trace-schema self-test, Chisel QEMU dry-run, and top xcheck
  gates. `SPERename::Rename` snapshots `tSeq/uSeq` before T/U destination
  rename, `SPERename::InsertToStoreIEX` clones stores after that snapshot, and
  `MemReqBus` carries the sequence sidecars through LSU/STQ cleanup. Preserve
  those row-owned sidecars through every split/queue/bridge owner: add them to
  `StoreSplitIssuePayload`, copy them to valid STA/STD/ST_ALL payloads,
  preserve them in `StoreDispatchQueues`, and copy them into
  `STQStoreRequest`. Invalid payloads should expose disabled sidecars, and a
  false `tuDstValid` must force `DestinationKind.None`. R62 composes
  `TULinkRename` with scalar rename through `ScalarTURenameBridge`, so reduced
  `DecodeRenameROBPath` must drive live `StoreSplitPayload` and
  `DispatchROBAllocator` sidecars from that owner; do not reintroduce disabled
  producer defaults or discard sidecars in lower owners.
- Phase 5/R62 scalar/TU rename composition work must run
  `sbt --client --error 'Test / compile'` plus affected
  `ScalarTURenameBridge`, `DecodeRenameROBPath`, `ScalarDecodeRenameBridge`,
  `TULinkRename`, `TULinkRecoveryCleanupPath`, `TULinkFlushSourceSelector`,
  `StoreSplitPayload`, `StoreDispatchSTQPath`, `StoreDispatchToSTQ`,
  `STQEntryBank`, `DispatchROBAllocator`, reduced ROB bookkeeping,
  trace-schema self-test, Chisel QEMU dry-run, top xcheck, and LinxCoreModel
  SHA gates. Keep `ScalarDecodeRenameBridge` scalar-GPR-only: sanitize T/U
  operands and destinations before feeding it, reject unsupported non-P/T/U
  operands, and overlay accepted T/U source/destination physical tags onto the
  `RenamedUop` after scalar rename. Scalar acceptance must be gated by
  `TULinkRecoveryCleanupPath.ready`, and `TULinkRecoveryCleanupPath.renameValid`
  must fire only from the accepted scalar row so GPR and T/U state mutate
  atomically. Drive `StoreSplitPayload.tSeq/uSeq/tuDst*` and
  `DispatchROBAllocator.allocTSeq/allocUSeq/allocTUDst*` from the wrapper's
  pre-allocation `SPERename::Rename` snapshots and accepted T/U destination
  sidecar. Keep relation-cmap release/deallocation, old T/U physical tag
  release accounting, ready-table mutation, and multi-PE/thread banking in
  later owner packets.
- Phase 5/R63 relation-cmap retire-source work must run
  `sbt --client --error 'Test / compile'` plus affected `InterfaceBundles`,
  `TULinkRelationCmap`, `ROBEntryBank`, `DispatchROBAllocator`,
  `DecodeRenameROBPath`, reduced ROB bookkeeping, trace-schema self-test, QEMU
  dry-run, and LinxCoreModel SHA gates. Preserve the model `SPEROB` split:
  ROB deallocation publishes width-wide row-owned retire sources, while
  `TULinkRelationCmap` serializes those sources into mark-before-release
  commands for `TULinkRename.retire*`. Do not collapse the ROB deallocation
  vector into a single command before a serializer consumes it; otherwise a
  `commitWidth > 1` dealloc cycle can drop T/U release work. Retire sources
  must preserve native `bid/gid/rid`, `isLast`, `stid`, row-owned `tSeq/uSeq`,
  and T/U destination ownership as sidecars rather than reconstructing them
  from commit-trace fields. The relation-cmap command order is T pre-release
  before U pre-release, current destination mark before post-release, and
  pressure release after the fifth same-kind relation, matching
  `SPEROB::CheckRelativeReg` and `SPEROB::ReleaseFunc`. Ready-table mutation,
  old T/U physical tag release accounting, block/group commit cleanup event
  wiring, and multi-PE/thread banking remain later owner packets.
- Phase 5/R64 live relation-cmap retire wiring must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkRetireCommandPath`, `TULinkRelationCmap`, `ScalarTURenameBridge`,
  `DecodeRenameROBPath`, `ROBEntryBank`, `DispatchROBAllocator`,
  `TULinkRename`, reduced ROB bookkeeping, trace-schema self-test, and Chisel
  QEMU dry-run gates. Keep the ROB deallocation source serializer and
  relation-cmap command acceptance as separate handshakes: `sourceWindowReady`
  is full-window FIFO credit for ROB deallocation, while relation-cmap
  `commandReady` must come from actual `TULinkRename.retireAccepted`, not a
  predicted readiness condition. This preserves flush/commit priority inside
  `TULinkRename` and prevents the relation-cmap from dropping a pending
  mark/release command when maintenance wins the cycle. Preserve valid
  no-destination block-last retire sources; they can still drain older T/U
  relations even though they do not emit a current destination mark.
- Phase 5/R65 relation-cmap cleanup pruning work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkRelationCmap`, `TULinkRetireCommandPath`, `DecodeRenameROBPath`,
  `TULinkRecoveryCleanupPath`, `TULinkRename`, `ROBEntryBank`,
  `DispatchROBAllocator`, reduced ROB bookkeeping, trace-schema self-test,
  Chisel QEMU dry-run, diff check, and LinxCoreModel SHA gates. Preserve the
  model cleanup split exactly: `CleanCMAP(bid)` removes all matching
  relation entries while preserving remaining order, `CleanGroupCMAP(bid,
  gid)` removes all exact `(bid,gid)` matches while preserving remaining
  order, and `FlushRelativeReg` prunes only the newest suffix of matching
  entries. For relation-cmap flush, `baseOnBid` is inclusive
  `flush.bid <= entry.bid`; non-base is strict BID-only
  `flush.bid < entry.bid` and must not add RID comparison. Apply the same
  cleanup predicates to queued ROB dealloc retire sources before they can
  enter relation-cmap, so a recovery flush cannot reintroduce pruned relation
  work. Keep ready-table side effects and live block/group commit clean event
  wiring in separate owner packets.
- Phase 5/R66 ROB block-last deallocation boundary work must run
  `sbt --client --error 'Test / compile'` plus affected `ROBEntryBank`,
  `DispatchROBAllocator`, `DecodeRenameROBPath`, `TULinkRetireCommandPath`,
  reduced ROB bookkeeping, trace-schema self-test, Chisel QEMU dry-run, diff
  check, and LinxCoreModel SHA gates. Preserve the model `SPEROB::dealloc`
  ordering: call relation release for each retired row, stop the deallocation
  window after the first block-last row, and do not expose deallocation sources
  from the next block in the same cycle. The block-last deallocation candidate
  is only a future `CleanCMAP` scheduling source; do not fire `cleanBlock*`
  from ROB commit or raw deallocation acceptance because serialized
  `TULinkRelationCmap` mark/release commands for the block-last source must be
  accepted first.
- Phase 5/R67 scalar `CleanCMAP` scheduling work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkRetireCommandPath`, `DecodeRenameROBPath`, `TULinkRelationCmap`,
  `TULinkRename`, `ROBEntryBank`, `DispatchROBAllocator`, reduced ROB
  bookkeeping, trace-schema self-test, Chisel QEMU dry-run, diff check, and
  LinxCoreModel SHA gates. Preserve the model order by latching the BID of the
  accepted block-last retire source, blocking later ROB deallocation-source
  admission while scalar block clean is pending, allowing existing
  relation-cmap mark/release commands to keep draining, and pulsing exact-BID
  `CleanCMAP` only after `pendingMark` and post-release state clear. Do not
  trigger scalar block clean directly from `deallocBlockLast*`,
  `sourceDequeued`, or ROB commit, and do not include the auto-clean pending
  latch in the retire-command `commandReady` block condition; that would
  deadlock the mark/release stream it is waiting for.
- Phase 5/R68 scalar local block-commit event work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkRetireCommandPath`, `DecodeRenameROBPath`, `TULinkRelationCmap`,
  `TULinkRename`, `ScalarTURenameBridge`, `ROBEntryBank`,
  `DispatchROBAllocator`, reduced ROB bookkeeping, trace-schema self-test,
  Chisel QEMU dry-run, diff check, and LinxCoreModel SHA gates. Preserve the
  model order `ReleaseRelative` commands, scalar `CleanCMAP`, then
  `ReportLocalRegBlockCommit`: the post-clean local block-commit event is a
  separate ready/valid boundary for the future SGPR local-register owner, not
  a T/U rename `commitValid` pulse and not an SGPR mutation inside the
  relation-cmap owner. While the local commit event is pending, block later ROB
  deallocation-source admission until the event is accepted or recovery
  prunes it, but do not feed that pending state into retire-command
  `commandReady`.
- Phase 5/R69 scalar local block-commit consumer work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkRecoveryCleanupPath`, `ScalarTURenameBridge`,
  `DecodeRenameROBPath`, `TULinkRetireCommandPath`, `TULinkRename`,
  `TULinkRelationCmap`, `ROBEntryBank`, `DispatchROBAllocator`, reduced ROB
  bookkeeping, trace-schema self-test, Chisel QEMU dry-run, diff check, and
  LinxCoreModel SHA gates. Consume the post-clean
  `ReportLocalRegBlockCommit` event in the live local-register owner:
  `TULinkRetireCommandPath` keeps the event pending, `ScalarTURenameBridge`
  forwards the handshake, and `TULinkRecoveryCleanupPath` arbitrates it behind
  external commit and recovery-flush maintenance before pulsing
  `TULinkRename.commit*` for the reduced T/U bank. Do not route this event
  through the relation-cmap scheduler, scalar GPR commit path, or generic
  top-level glue. Preserve the reduced scope until a later packet implements
  both-SGPR-hand and multi-PE fanout.
- Phase 5/R70 selected-STID local block-commit work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkRetireCommandPath`, `TULinkRecoveryCleanupPath`,
  `ScalarTURenameBridge`, `DecodeRenameROBPath`, `TULinkRename`,
  `TULinkRelationCmap`, `ROBEntryBank`, `DispatchROBAllocator`, reduced ROB
  bookkeeping, trace-schema self-test, Chisel QEMU dry-run, diff check, and
  LinxCoreModel SHA gates. Preserve the model
  `ReportLocalRegBlockCommit(bid, stid)` contract: the post-clean event must
  carry the selected STID from the block-last source, and a reduced
  local-register owner must accept only its configured local STID. Do not
  silently drop or consume a non-local STID event in the reduced bank; keep
  ready low and expose a diagnostic until a later fanout owner explicitly
  selects or instantiates the matching STID banks across both SGPR hands and
  scalar PEs.
- Phase 5/R71 selected-STID local block-commit fanout work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkLocalBlockCommitFanout`, `DecodeRenameROBPath`,
  `TULinkRecoveryCleanupPath`, `ScalarTURenameBridge`,
  `TULinkRetireCommandPath`, `TULinkRename`, `TULinkRelationCmap`,
  `ROBEntryBank`, `DispatchROBAllocator`, reduced ROB bookkeeping,
  trace-schema self-test, Chisel QEMU dry-run, diff check, and LinxCoreModel
  SHA gates. Preserve the model all-selected-PE fanout contract:
  `ReportSGPRBlockCommit(bid, stid)` selects one STID, then updates both SGPR
  hands for every scalar PE. A Chisel fanout owner must pulse downstream bank
  valid only when every selected PE bank is ready; do not let a ready subset of
  banks consume the post-clean block-commit event before the others.
- Phase 5/R72 explicit SGPR local-bank-array work must run
  `sbt --client --error 'Test / compile'` plus affected
  `TULinkLocalBankArray`, `ScalarTURenameBridge`, `DecodeRenameROBPath`,
  `TULinkLocalBlockCommitFanout`, `TULinkRecoveryCleanupPath`,
  `TULinkRetireCommandPath`, `TULinkRename`, `TULinkRelationCmap`,
  `ROBEntryBank`, `DispatchROBAllocator`, reduced ROB bookkeeping,
  trace-schema self-test, Chisel QEMU dry-run, diff check, and LinxCoreModel
  SHA gates. Preserve the model SGPR bank hierarchy:
  `sgprRenameUnit[pe][stid][hand]` is the owner shape, with T and U as the two
  hands inside each PE/STID bank group. Keep selected-STID block-commit fanout
  inside the explicit bank-array owner, not in backend glue. Later dynamic
  PE/STID routing must target that same bank-array boundary for rename,
  retire, recovery cleanup, and local block commit.
- Phase 5/R73 active SGPR bank selector plumbing must run
  `sbt --client --error 'Test / compile'` plus affected
  `ScalarTURenameBridge`, `DecodeRenameROBPath`, `TULinkLocalBankArray`,
  `TULinkRecoveryCleanupPath`, `TULinkRetireCommandPath`, `TULinkRename`,
  `TULinkRelationCmap`, `ROBEntryBank`, `DispatchROBAllocator`, reduced ROB
  bookkeeping, trace-schema self-test, Chisel QEMU dry-run, diff check, and
  LinxCoreModel SHA gates. Preserve the model `SPERename::Rename` lookup:
  active SGPR bank selection is by row-owned PE/STID at the
  `ScalarTURenameBridge`/`TULinkLocalBankArray` boundary. In the reduced
  backend, derive active STID from the queued decoded row `threadId` and keep
  PE at PE0 until decode carries a PE owner. Keep the active selector scoped
  to rename and reduced external maintenance; retired-row mark/release routing
  must use the command sidecar path described by R74, not the current
  rename-head selector.
- Phase 5/R74 retired-row SGPR retire-bank sidecar work must run
  `sbt --client --error 'Test / compile'` plus affected `InterfaceBundles`,
  `TULinkRelationCmap`, `TULinkRetireCommandPath`,
  `TULinkLocalBankArray`, `ScalarTURenameBridge`, `ROBEntryBank`,
  `DispatchROBAllocator`, `DecodeRenameROBPath`,
  `TULinkRecoveryCleanupPath`, `TULinkRename`, reduced ROB bookkeeping,
  trace-schema self-test, Chisel QEMU dry-run, diff check, and LinxCoreModel
  SHA gates. Preserve the model `SPERename::RepLocalRetired(type, peid, ...,
  tid)` and `SPEROB::ReleaseFunc` bank arguments: ROB deallocation sources
  must carry row-owned `peId/stid`, relation-cmap entries must retain those
  sidecars for later releases, and `TULinkRetireCommand` must route
  mark/release commands by command `peId/stid`. Do not derive local retire
  target banks from `ScalarTURenameBridge.activePeId/activeStid`; that selector
  belongs to the current rename head. Dynamic non-zero PE production remains a
  later packet, but the sidecar must be stored, serialized, and diagnosed now.
- Phase 5/R75 decoded/renamed scalar PE owner sidecar work must run
  `sbt --client --error 'Test / compile'` plus affected `InterfaceBundles`,
  `F4DecodeWindow`, `FrontendInstructionBuffer`, `FrontendDecodeIngress`,
  `FrontendDecodeStage`, `DecodeLoadStoreIdAssign`, `DecodeRenameQueue`,
  `ScalarDecodeRenameBridge`, `ScalarTURenameBridge`, `StoreSplitPayload`,
  `DecodeRenameROBPath`, `TULinkLocalBankArray`, `DispatchROBAllocator`,
  `ROBEntryBank`, reduced ROB bookkeeping, top xcheck, trace-schema
  self-test, Chisel QEMU dry-run, build, Verilator lint, diff check, and
  LinxCoreModel SHA gates. Preserve the model `DCTop::Work` and
  `SPERename::Rename` ownership chain: frontend packets, decoded uops, renamed
  uops, decode/rename queue rows, memory-ID outputs, and store-split payloads
  must carry row-owned `peId/threadId`; reduced `DecodeRenameROBPath` must
  drive `ScalarTURenameBridge.activePeId` and
  `DispatchROBAllocator.allocPeId` from the queued row `peId`, while active
  STID remains the queued row `threadId`. Do not reintroduce PE0 constants at
  decode, rename, ROB allocation, or store payload boundaries. Nonzero PE
  packet production and multi-PE top/bank instantiation remain later owners;
  packets that do not set `peId` still reduce to PE0 through normal zero
  defaults.
- Phase 5/R76 enqueue-time ROB reservation is the implemented contract, not an
  open design choice. Preserve the model `BCtrlUnit::Work` -> `DCTop::Work` ->
  `SPEROB::allocROB` -> `dec_ren_q` order: BROB and PE ROB identities are
  reserved before the row enters `dec_ren_q`, not at rename acceptance. In the
  C++ model, the ROB row stores the shared `SimInst` pointer, so later
  `SPERename` mutations such as `tSeq/uSeq` remain visible through that
  pointer. Chisel ROB rows store values, so `DecodeRenameROBPath` reserves the
  row before enqueue and `ROBEntryBank.renameUpdate*`, forwarded through
  `DispatchROBAllocator`, patches the accepted rename row afterward. Do not
  reintroduce queue-head ROB allocation, permanent zero T/U sidecars, or any
  allocator-valid feedback loop that lets allocator readiness depend on its own
  accepted output. Focused gates include `DecodeRenameROBPath`,
  `DispatchROBAllocator`, `ROBEntryBank`, `DecodeRenameQueue`,
  `ScalarTURenameBridge`, reduced ROB bookkeeping, top xcheck when top IO
  changes, trace-schema self-test if commit rows change, Chisel QEMU dry-run,
  build, Verilator lint, diff check, and LinxCoreModel SHA gates.
- Phase 5/R77 gate-broadening work starts from the R76 implementation and must
  run the full wrapper ladder before wider frontend/rename agents depend on the
  new allocation timing: affected R76 unit specs, reduced ROB bookkeeping,
  reduced ROB Verilator xcheck, top xcheck, trace-schema self-test, Chisel QEMU
  dry-run, `build_chisel.sh`, and Verilator lint. R77 may repair wrapper or
  trace payload issues found by those gates, but it must not redesign the
  reservation/update split without first recording a concrete first-divergence
  failure.
- Phase 5/R78 trace replay work adds the bridge between synthetic reduced
  smokes and future live QEMU/CoreMark comparison. Run
  `run_chisel_trace_replay_xcheck.sh` after changes to top-level commit export,
  `trace_schema_adapter.py`, or cross-check harness code. The gate must
  normalize a bounded external or fixture commit JSONL, replay it through
  `LinxCoreTop` under Verilator, and require zero mismatches against the
  QEMU-shaped reference stream. Treat this as replay infrastructure only; it is
  not evidence that frontend/decode/execute/LSU generated rows from an ELF.
- Phase 5/R90 QEMU trace replay work adds the bridge from archived or freshly
  collected QEMU commit JSONL into the Chisel replay harness. Run
  `run_chisel_qemu_trace_replay_xcheck.sh --dry-run`, then a bounded
  `--qemu-trace <trace.jsonl>` or `--elf <direct-boot.elf>` replay. Use
  `--max-commits` for architectural compare depth and `--replay-rows` only as
  the raw search/replay cap before metadata filtering. The bridge must report
  `qemu-replay-raw-rows`, `qemu-replay-arch-rows`, and a passing
  `crosscheck_manifest.json`. It is not full-DUT QEMU equivalence until the
  Chisel top emits live commit rows from real fetch/issue/execute/LSU/recovery.
- Phase 5/R91 live-ELF replay prefix work hardens the same bridge for
  long-running benchmark ELFs. The FIFO reader must terminate when QEMU exits
  early, and direct-boot benchmark images at high physical addresses must pass
  explicit QEMU memory. The current CoreMark prefix evidence uses
  `tests/benchmarks/build/coremark_real.elf` with `-m 1280M`, captures 128 raw
  QEMU rows, slices 5 replay rows containing 4 architectural commits, and
  requires a passing manifest with zero mismatches.
- Phase 5/R92 shared commit JSONL writer work factors generated-RTL harness
  trace emission through `tools/chisel/commit_trace_jsonl.h`. Run reduced ROB,
  top, trace replay, frontend trace, frontend fetch trace, frontend ALU, and
  frontend RF/ALU generated-RTL xchecks after changing this helper or a
  harness conversion.
  The writer must keep the QEMU architectural field spelling aligned with
  QEMU `target/linx/helper.c` / trace-manager output and keep DUT sidebands
  flat for `trace_schema_adapter.py`; it does not replace the adapter or the
  neutral comparator.
- Phase 5/R79 frontend-window trace-top work adds the first emitted Chisel top
  boundary that drives a raw `FrontendDecodePacket` window through
  `F4DecodeWindow` and `DecodeRenameROBPath` before monitored commit export.
  Run `run_chisel_tests.sh --only LinxCoreFrontendTraceTop` and
  `run_chisel_frontend_trace_top_lint.sh` after changes to that
  frontend-window-to-commit boundary. The wrapper may use an external
  completion surrogate until execute owners exist; it is not full
  QEMU/CoreMark evidence until a Verilator driver dumps DUT commit JSONL from
  live frontend/decode/execute/LSU-owned rows.
- Phase 5/R80 frontend-window trace-top xcheck work adds the first generated
  RTL comparison gate for `LinxCoreFrontendTraceTop`. Run
  `run_chisel_frontend_trace_top_xcheck.sh` after changes to the frontend
  trace-top driver, temporary completion surrogate, trace dump, or commit
  export. The gate must drive raw scalar frontend packets through
  `F4DecodeWindow` and `DecodeRenameROBPath`, use the explicit completion
  surrogate to retire allocated ROB rows, dump DUT JSONL, and require zero
  mismatches against a QEMU-shaped reference stream. Treat this as frontend
  packet to commit-row infrastructure only; it is still not CoreMark/QEMU
  architectural evidence until fetch, issue, execute, LSU, and recovery owners
  generate the retired rows and completion payloads.
- Phase 5/R94 live frontend fetch trace-top work adds the first generated RTL
  comparison gate where a Chisel source, not the testbench, creates
  `FrontendDecodePacket` rows from PC request/response handshakes. Run
  `run_chisel_tests.sh --only FrontendFetchPacketSource`,
  `run_chisel_tests.sh --only LinxCoreFrontendFetchTraceTop`, and
  `run_chisel_frontend_fetch_trace_top_xcheck.sh` after changes to the live
  frontend fetch source top, bounded memory-window fixture, source-to-F4
  handshake, temporary completion surrogate, or commit export. The fixture may
  expose one valid F4 slot per response while the reduced backend remains
  one-selected-row-per-packet. Treat this as live source-to-F4-to-ROB
  infrastructure only; it is not full QEMU/CoreMark evidence until ELF memory,
  dense packets, real execute/LSU completion, and recovery are live.
- Phase 5/R95 live frontend fetch RF-backed ALU trace-top work composes the
  live fetch source with the reduced RF-backed issue and ALU completion path.
  Run `run_chisel_tests.sh --only FrontendFetchPacketSource`,
  `run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`, and
  `run_chisel_frontend_fetch_rf_alu_trace_top_xcheck.sh` after changes to the
  live fetch source to RF/issue/ALU top, bounded memory-window fixture,
  source-to-F4 handshake, source PC advance, issue enqueue, RF source
  readiness, ALU completion, RF writeback, or commit export. Keep
  `run_chisel_frontend_fetch_trace_top_xcheck.sh` and
  `run_chisel_frontend_rf_alu_trace_top_xcheck.sh` as regressions for the two
  predecessor surfaces. Treat this as live-source RF/ALU infrastructure only;
  it is not full QEMU/CoreMark evidence until ELF memory, dense packets, full
  issue arbitration, LSU, trap/recovery, and redirect restart are live.
- Phase 5/R97 sparse ELF fetch-memory work extends the same live fetch
  RF/ALU gate with program-image input support. Run
  `python3 tools/chisel/frontend_fetch_elf_memory.py --self-test` after
  changes to ELF extraction, sparse fetch-memory format, or `FETCH_ELF`
  wrapper routing. Use
  `FETCH_ELF=<elf> bash tools/chisel/run_chisel_frontend_fetch_rf_alu_trace_top_xcheck.sh`
  to exercise ELF64 little-endian PT_LOAD extraction into
  `generated/chisel-frontend-fetch-rf-alu-trace-top-xcheck/elf.fetch.mem`.
  This proves sparse/high-address program bytes can feed the live source
  response path, but it still uses the reduced top's expected row lengths and
  fixed scalar reference rows. Do not claim QEMU/CoreMark equivalence until a
  later packet binds expected rows to a bounded QEMU/ELF prefix and removes the
  single-instruction response constraint.
- Phase 5/R98 external expected-row source work splits live fetch RF/ALU
  expected rows from the C++ harness. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_fixture_rows.py --self-test`
  after changing the default row fixture. The wrapper emits
  `generated/chisel-frontend-fetch-rf-alu-trace-top-xcheck/fixture.expected.jsonl`
  unless `FETCH_EXPECTED_ROWS=<rows.jsonl>` points at another QEMU-shaped row
  stream, then passes `--expected-rows` to the Verilator harness and sizes the
  comparator window from the expected row count. This is a row-source contract
  for reduced scalar live-fetch rows, not full QEMU/CoreMark equivalence:
  broader QEMU/ELF prefixes, dense packets, LSU, trap/recovery, and live
  full-DUT commit generation remain later owners.
- Phase 5/R99 strict QEMU trace expected-row extraction work feeds that same
  row-source boundary from an existing QEMU commit JSONL. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test` after
  changes to the extractor, and use
  `FETCH_QEMU_TRACE=<qemu.jsonl> bash tools/chisel/run_chisel_frontend_fetch_rf_alu_trace_top_xcheck.sh`
  to normalize and validate a strict sequential reduced-scalar prefix into
  `generated/chisel-frontend-fetch-rf-alu-trace-top-xcheck/qemu.expected.jsonl`.
  `FETCH_QEMU_MAX_ROWS=<n>` caps the extracted row count, while `0` means all
  normalized input rows. The extractor must reject unsupported opcodes, memory
  or trap side effects, non-scalar GPR aliases, non-sequential `next_pc`, and
  writeback/result mismatches before the Verilator harness runs. This remains
  reduced ADD/ADDI/ADDTPC/C.MOVI/C.MOVR evidence only; dense packets, LSU,
  trap/recovery, and live full-DUT commit generation remain later owners.
- Phase 5/R100 live QEMU ELF capture work binds the R99 row-source path to a
  direct-boot ELF. Build the legal-entry fixture with
  `bash tools/chisel/build_frontend_fetch_rf_alu_qemu_fixture_elf.sh --out-dir generated/r100-live-qemu-fixture`,
  then run
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --elf generated/r100-live-qemu-fixture/frontend_fetch_rf_alu_qemu_fixture.elf --expected-rows 3 --capture-rows 3 --pc-lo 0x10002 --pc-hi 0x1000b --max-seconds 5`.
  The wrapper captures bounded QEMU rows through a FIFO, validates them with
  `frontend_fetch_rf_alu_qemu_rows.py`, extracts matching bytes through
  `FETCH_ELF`, and runs the live fetch RF/ALU comparator. Use `--pc-lo` /
  `--pc-hi` to skip legal entry `BSTART` until block-header execution is live
  in the DUT. A signal-15 QEMU termination after bounded capture is expected
  only when the manifest reports `status: "pass"`. The Verilator harness must
  derive initial RF preloads from first expected source reads; do not re-add
  synthetic-only hardcoded source values.
- Phase 5/R101 reduced block-marker work lets that same legal-entry ELF run
  without scalar PC filters. Build the fixture with
  `bash tools/chisel/build_frontend_fetch_rf_alu_qemu_fixture_elf.sh --out-dir generated/r101-live-qemu-fixture`,
  then run
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --elf generated/r101-live-qemu-fixture/frontend_fetch_rf_alu_qemu_fixture.elf --expected-rows 0 --capture-rows 5 --allow-block-markers --max-seconds 5`.
  `--allow-block-markers` preserves legal `BSTART`/`BSTOP` rows as DUT-only
  skip entries: the generated-RTL harness must fetch and decode them, assert
  marker diagnostics, and require no ROB allocation or issue enqueue. The
  comparator still receives only non-skip scalar commit rows. Treat this as
  reduced marker-consume evidence, not dense packet support and not full
  `BSTART`/`BSTOP` scalar_done/BROB retirement semantics.
- Phase 5/R102 reduced dense D1-slot work lets the same live fetch RF/ALU gate
  feed natural 8-byte F4/IB windows instead of one instruction per response. The
  reduced bridge must preserve every valid D1 slot from the window in order,
  keep each slot's original slot index, and drain one slot per cycle into the
  existing serialized decode/ROB path. Build the fixture with
  `bash tools/chisel/build_frontend_fetch_rf_alu_qemu_fixture_elf.sh --out-dir generated/r102-live-qemu-fixture`,
  then run
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r102-dense-qemu-elf-xcheck --elf generated/r102-live-qemu-fixture/frontend_fetch_rf_alu_qemu_fixture.elf --expected-rows 0 --capture-rows 5 --allow-block-markers --max-seconds 5`.
  Marker-slot checks are marker-owned: a marker drain must not select a scalar
  row, push dec/ren, or allocate ROB for that marker, but it may overlap an
  older scalar row's issue enqueue in the same cycle. This is still not full
  width-wide ROB allocation or `BSTART`/`BSTOP` scalar_done/BROB retirement.
- Phase 5/R106 CoreMark ADDTPC work extends the reduced live fetch RF/ALU
  envelope with the model PC-relative constant operation. `ADDTPC` must compute
  `(pc & ~0xfff) + imm`, where frontend operand decode has already
  sign-extended `IMM20` and shifted it left by 12. Run
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`, and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r106-coremark-addtpc-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 4 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced PC-relative execute or QEMU extraction. The R106
  evidence compares three scalar rows (`C.MOVR`, `ADDTPC`, `ADDI`) with zero
  mismatches and preserves `C.BSTART` as a skip marker; the next observed
  CoreMark blocker is the 6-byte HL call marker at `pc=0x40005500`.
- Phase 5/R107 CoreMark HL-call work extends the reduced live fetch RF/ALU
  envelope through the first direct-call header. QEMU can emit
  `HL.BSTART.STD CALL` as a duplicate zero-advance marker row followed by the
  advancing marker row; the extractor should drop only the zero-advance marker
  artifact when it has no trap, memory, or writeback side effects. Compact
  `C.SETRET` aliases the `C.MOVI` low-opcode form when the destination is
  `ra/x10`, forces destination `x10`, uses `uimm5 << 1`, and computes
  `pc + imm`; do not route it through `ADDTPC` or generic `C.MOVI`
  semantics. Target-bearing `BSTART` forms must carry `boundaryTarget =
  pc + imm`, `F4DecodeWindow` must stop exposing later slots after a valid
  `C.BSTOP`, and the reduced live-fetch top may apply a frontend-only restart
  to the active `BSTART` target when `C.BSTOP` closes the marker-owned block.
  Run the focused gates
  `bash tools/chisel/run_chisel_tests.sh --only F4DecodeWindow`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeIngress`,
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`, and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r107-coremark-hl-call-setret-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 8 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing compact SETRET decode, target-bearing BSTART decode,
  marker-stop redirect wiring, or live-QEMU row extraction. The R107 evidence
  compares four scalar rows with zero mismatches and advances the next
  CoreMark blocker to the row after `pc=0x4000550e`.
- Phase 5/R108 CoreMark FENTRY work extends the reduced live fetch RF/ALU
  envelope through the first single-save macro prologue row. Treat this as a
  narrow reduced FENTRY shape only: map the saved GPR field to an internal RF
  read, map old SP (`x1`) to another internal RF read, mark SP (`x1`) as the
  reduced destination, write `SP - imm`, and emit the one QEMU-shaped 8-byte
  store sideband while suppressing those internal source fields in the commit
  row. The expected-row reducer must preserve FENTRY memory fields and should
  reject multi-register FENTRY until stack-template/LSU semantics are owned.
  Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r108-coremark-fentry-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 11 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced FENTRY decode, execute, memory sideband comparison, or
  QEMU extraction. The next observed 12-row CoreMark blocker is an `ADDI`
  writing architectural tag `30`, outside the reduced scalar GPR namespace.
- Phase 5/R109 CoreMark U-destination ADDI work extends the reduced live fetch
  RF/ALU envelope through that local-register destination row. Preserve the
  model alias split: destination tag `30` is `DestinationKind.U`, not a scalar
  GPR. `ScalarTURenameBridge` owns the T/U destination overlay; reduced issue
  and execute owners must gate scalar RF clear/write side effects to
  `DestinationKind.Gpr` while still emitting QEMU-shaped architectural
  `dst_reg=30` / `wb_rd=30` commit fields. The expected-row reducer may accept
  this U-destination only for the current reduced `ADDI` row and must continue
  rejecting unsupported T/U source reads. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarIssueQueue`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only ScalarTURenameBridge`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendRfAluTraceTop`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r109-coremark-u-dst-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 12 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced T/U destination handling, RF writeback gating, or
  live-QEMU row extraction. The R109 evidence compares seven scalar/macro rows
  with zero mismatches. A 13-row probe advances the next blocker to `OP_HL_LUI`
  at `pc=0x4000551a`, `insn=0x1f97000e`, `len=6`.
- Phase 5/R110 CoreMark HL.LUI work extends the reduced live fetch RF/ALU
  envelope through that T-destination immediate row. Preserve the same local
  register split as R109: destination tag `31` is `DestinationKind.T`, not a
  scalar GPR. `OP_HL_LUI` materializes the sign-extended 48-bit-format IMM32
  payload directly into the destination; frontend operand decode packs
  `Cat(pfx16[15:4], main32[31:12])` before execute receives `imm`. The
  expected-row reducer may accept this T-destination only for the current
  reduced `HL.LUI` row and must continue rejecting unsupported T/U source
  reads. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only ScalarTURenameBridge`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarIssueQueue`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r110-coremark-hl-lui-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 13 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced HL.LUI decode, execute, RF writeback gating, or
  live-QEMU row extraction. The R110 evidence compares eight scalar/macro rows
  with zero mismatches. A 14-row probe advances the next blocker to `OP_SLL`
  at `pc=0x40005520`, `insn=0x01cc7f05`, `len=4`; that row reads T/U local
  sources (`rs1=24`, `rs2=28`) and writes U destination tag `30`.
- Phase 5/R111 CoreMark SLL local-source work extends the reduced live fetch
  RF/ALU envelope through that first T/U-source row. Preserve the model/QEMU
  alias split: source tags `24..27` are T local links, source tags `28..31`
  are U local links, and they must not be read as scalar RF tags. Reduced
  issue must sample `localTReadyMask`/`localUReadyMask`, carry selected source
  `operandClass` and `relTag` sidebands, and let the live top feed operand
  data from the current reduced local-value overlay until full local-bank data
  execution exists. `OP_SLL` computes `SrcL << (SrcR & 0x3f)`. QEMU suppresses
  local T/U source fields in the commit row, so `ReducedScalarAluExecute` must
  emit source fields only for scalar `OperandClass.P` operands while still
  carrying the U destination/writeback fields. Also preserve native ROB RID
  wrap: the `SLL` row is the ninth scalar allocation in the generated 8-entry
  reduced top, so `DecodeRenameROBPath` must stamp queued `rid.wrap` from
  `DispatchROBAllocator.allocRobWrap`; a slot-only false-wrap RID makes
  `ROBEntryBank.renameUpdateReady` reject the post-rename update. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarIssueQueue`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only ROBEntryBank`,
  `bash tools/chisel/run_chisel_tests.sh --only DispatchROBAllocator`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendRfAluTraceTop`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r111-coremark-sll-tu-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 14 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced T/U source readiness/data, SLL execute semantics, ROB
  allocation RID stamping, or live-QEMU row extraction. The R111 evidence
  compares nine scalar/macro rows with zero mismatches.
- Phase 5/R112 CoreMark shift-family work extends the reduced live fetch RF/ALU
  envelope through the next same-window local shift rows. Preserve the R111
  T/U source rule, but do not assume `SLL` only writes U: the later `SLL` at
  `pc=0x4000552a` writes T destination tag `31`, and the following `OP_SRL`
  at `pc=0x4000552e` reads local T/U sources and writes T tag `31`. `OP_SRL`
  computes `SrcL >> (SrcR & 0x3f)` as a 64-bit logical shift. QEMU still
  suppresses local T/U source fields, so the reducer and Chisel completion row
  must keep scalar source fields invalid and gate scalar RF side effects to GPR
  destinations. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`, and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r112-coremark-sll-srl-tu-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 17 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced shift-family execute semantics, T/U destination
  admission, or live-QEMU row extraction. The R112 evidence compares twelve
  scalar/macro rows with zero mismatches. An 18-row probe advances the next
  blocker to `OP_OR` at `pc=0x40005532`, `insn=0x078e3f05`, `len=4`; that row
  reads local U0/T0 and writes U0.
- Phase 5/R113 CoreMark OR/C.LDI work extends the reduced live fetch RF/ALU
  envelope through `OP_OR` at `pc=0x40005532` and a narrow `C.LDI` row at
  `pc=0x40005536`. `OP_OR` reads local U0/T0, writes U0, suppresses local
  source fields in the QEMU-shaped row, and keeps scalar RF side effects gated
  to GPR destinations. The current `C.LDI` support is intentionally limited to
  the observed zero-load prefix row: scalar source x4, T destination tag `31`,
  8-byte load sideband, `mem_rdata=0`, and result zero. Do not generalize this
  into a load/LSU implementation without adding a real data-memory source. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`, and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r113-coremark-or-c-ldi-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 19 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced OR semantics, the C.LDI zero-load sideband, T/U local
  destination admission, or live-QEMU row extraction. The R113 evidence compares
  fourteen scalar/macro rows with zero mismatches. A 21-row extraction probe
  advances the next blocker to `OP_C_ADD` at `pc=0x4000553c`, `insn=0xe608`,
  `len=2`, after a supported same-window `SLL` at `pc=0x40005538`.
- Phase 5/R114 CoreMark C.ADD work extends the reduced live fetch RF/ALU
  envelope through compressed local-source add at `pc=0x4000553c`,
  `insn=0xe608`, `len=2`. LinxCoreModel `block16.decode` owns the compressed
  arithmetic contract: `@C_ARITH` reads `SrcL`/`SrcR` from bits `[10:6]` and
  `[15:11]` and writes implicit destination tag `31`. Current QEMU commit JSONL
  emits this exact row as a no-writeback local trace gap, so the reduced
  expected-row extractor may synthesize only this C.ADD implicit T writeback
  from the QEMU PC/instruction stream plus local T/U history. If QEMU emits a
  writeback for C.ADD, require destination tag `31`; do not generalize this into
  arbitrary QEMU trace patching without new LinxCoreModel and live-QEMU
  evidence. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`, and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r114-coremark-c-add-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 21 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing compressed arithmetic extraction, local T/U destination
  admission, or reduced ALU C.ADD semantics. The R114 evidence compares sixteen
  scalar/macro rows with zero mismatches. A 22-row probe advances the next
  blocker to `OP_SRA` at `pc=0x4000553e`, `insn=0x01ec6f85`, `len=4`; that row
  reads local T0/U2, writes T tag `31`, and currently produces result `1`.
- Phase 5/R115 CoreMark SRA/SLLI work extends the reduced live fetch RF/ALU
  envelope through `OP_SRA` at `pc=0x4000553e` and the same dense-packet
  `OP_SLLI` at `pc=0x40005542`. LinxCoreModel `block32.decode` maps `SRA` to
  `@shift` and `SLLI` to `@shift_i`; `SRA` uses signed 64-bit arithmetic right
  shift by `SrcR & 0x3f`, while `SLLI` uses `shamt_20_25`. The generated
  Chisel opcode table currently marks shift-immediate rows as `ImmNONE`, so
  `FrontendOperandDecode` must explicitly carry `shamt_20_25` for
  `OP_SLLI`/`OP_SRLI`/`OP_SRAI`. The reduced live top must also keep same-packet
  local T/U consumers ordered behind pending local producers; a previous
  per-source ready block created a ready/output combinational cycle through
  `DecodeRenameROBPath`, so keep the coarse acyclic local-producer stall until
  a real local-bank scheduler carries per-entry dependency versions. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r115-coremark-sra-slli-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 23 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing shift-immediate operand decode, reduced SRA/SLLI semantics,
  local T/U producer ordering, or live-QEMU row extraction. The R115 evidence
  compares eighteen scalar/macro rows with zero mismatches. A 24-row probe
  advances the next frontier to mixed local/scalar `C.ADD` at `pc=0x40005546`,
  `insn=0x2608`, `len=2`: compressed `SrcL` is T0, compressed `SrcR` is scalar
  x4, QEMU emits the scalar source field, and current QEMU emits no
  destination/writeback.
- Phase 5/R116 CoreMark mixed-source dense-packet work extends the reduced
  live fetch RF/ALU envelope through the full 8-byte packet beginning at
  `pc=0x40005546`: mixed local/scalar `C.ADD` (`insn=0x2608`) synthesizes the
  implicit T writeback while preserving QEMU's scalar `src1`, the following
  `ADDI` (`insn=0x018c0115`) reads encoded `SrcL=T0` with QEMU's local source
  field suppressed and writes scalar x2, and `C.MOVR` (`insn=0x2806`) moves
  scalar x0 to x5. Expected-row extraction must validate each encoded source
  independently as either a suppressed local T/U source or a visible scalar GPR
  source; do not keep opcode-wide assumptions such as "all C.ADD sources are
  local" or "all ADDI src0 fields are scalar." Also avoid promoting a live
  CoreMark gate that stops inside an 8-byte dense fetch window: a 24-row capture
  reaches the mixed C.ADD but fails the dense-packet boundary check, while the
  26-row gate captures the whole packet. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test` and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r116-coremark-c-add-mixed-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 26 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing encoded source validation, C.ADD trace-gap synthesis,
  local-source ADDI extraction, or dense-packet capture rules. The R116 evidence
  compares twenty-one scalar/macro rows with zero mismatches. A 27-row probe
  still passes and shows the next raw row as a zero-advance `C.BSTART` artifact
  at `pc=0x4000554e`, `insn=0x0004`, which the current marker-skip logic drops.
- Phase 5/R117 CoreMark C.MOVR/C.LDI/C.SETC work extends the reduced live fetch
  RF/ALU envelope through the marker at `pc=0x4000554e` and the packet ending
  at `C.BSTART.STD.FALL` (`pc=0x4000555a`). `C.MOVR` may write T destination
  alias `31`; `C.LDI` must validate its encoded base as scalar or suppressed
  local T/U and must use signed bits `[15:11] << 3` as a byte offset, so
  `FrontendOperandDecode` overrides generic `ImmSIMM5_11_S5` for `OP_C_LDI`.
  `C.SETC_NE` (`key=0x36`) is a no-writeback compare row: the observed
  CoreMark row has suppressed local `SrcL=T0`, visible scalar `SrcR=x5`, and
  no destination/writeback. The reduced `DecodeRenameROBPath` must feed
  marker/block-retire scalar commit feedback into scalar rename mapQ release,
  and its T/U retire serializer must drain terminal responses
  (`accepted|miss|releaseMismatch|unsupported`) so stale retire commands do
  not deadlock later local-source packets. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`, and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r117-coremark-c-movr-c-ldi-setc-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 34 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing C.MOVR T-destination admission, C.LDI immediate/base
  extraction, C.SETC_NE no-writeback handling, scalar block-retire feedback, or
  T/U retire command terminal-response handling. The R117 evidence compares
  twenty-five scalar/macro rows with zero mismatches. The next frontier starts
  at `pc=0x4000555c`, `insn=0x13808315`, likely `ADDTPC`.
- Phase 5/R118 CoreMark SDI store-immediate work extends the reduced live fetch
  RF/ALU envelope through `OP_SDI` at `pc=0x4000556a`. The model/QEMU ordinary
  store-immediate contract is: encoded `SrcL`/`src0` is store data, encoded
  `SrcR`/`src1` is address base, decoded `simm12_7_s5_25_7` is scaled left by
  3 for doubleword stores, and non-PCR stores use store-data source index 0.
  Commit rows must remain no-writeback and carry one 8-byte store sideband;
  scalar P sources are visible while local T/U bases are consumed internally and
  suppressed to match QEMU. Do not promote live CoreMark captures that cut
  inside a dense F4/IB window: 41 rows cuts inside the SDI/ADDI two-slot packet, 43
  rows cuts inside the following three-slot branch packet, and the promoted R118
  gate uses `--capture-rows 42`. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`, and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r118-coremark-sdi-42-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 42 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced SDI classification, store-immediate address/data
  sidebands, no-writeback store handling, or dense-packet capture rules. The
  R118 evidence compares thirty-one scalar/macro rows with zero mismatches. The
  next frontier is the dense packet beginning at `pc=0x40005572` and ending at
  the redirecting marker at `pc=0x40005574`.
- Phase 5/R119 CoreMark conditional-BSTART work extends the reduced live fetch
  RF/ALU envelope through the loop edge at `pc=0x40005574` and one fall-through
  iteration. `OP_C_SETC_NE` now publishes a validity-masked branch-decision
  sideband; the live top latches that decision until the following marker
  boundary; and `DecodeRenameROBPath` must stall marker-only conditional
  boundaries until the decision is valid. A false decision allocates the
  fallthrough marker block, while a true decision redirects to the active
  conditional target and suppresses new marker allocation. The live harness must
  collect commit rows while dense slots drain; otherwise ROB retire pulses can
  disappear before the later compare phase. Do not promote the 48-row probe
  because it cuts inside the post-redirect dense window; the promoted R119 gate
  uses `--capture-rows 50`. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r119-coremark-cond-bstart-50-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 50 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing conditional marker readiness, branch-decision sidebands,
  marker redirect/fallthrough allocation, or dense-drain commit buffering. The
  R119 evidence compares thirty-six scalar/macro rows with zero mismatches.
- Phase 5/R120 CoreMark repeated-loop work extends the reduced live fetch
  RF/ALU envelope through repeated conditional-loop body trips. If a visible
  target-body scalar row allocates a BROB block while no marker-owned block is
  active, `DecodeRenameROBPath` must seed active block state from that scalar
  allocation and keep it until a matching block-last sideband or later marker
  boundary closes it. The reduced live RF/ALU top may bypass store-dispatch
  residency only because the ALU execute path already emits the compared
  QEMU-shaped store sideband and this top does not yet connect STA/STD
  execution or STQ commit/free feedback. Do not enable that bypass in full LSU
  or backend integration paths. Run
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r120-coremark-scalar-block-store-bypass-128-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 128 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing scalar-created block lifecycle, marker block cleanup,
  store-dispatch readiness/bypass, or the reduced live RF/ALU store-sideband
  comparison boundary. The R120 evidence compares eighty-eight scalar/macro
  rows with zero mismatches.
- Phase 5/R121 CoreMark LDI/C.SETC_EQ work extends the reduced live fetch
  RF/ALU envelope through the repeated-loop 256-row capture. `OP_LDI` is a
  reduced zero-load bridge only for the current prefix: validate one 8-byte
  non-store memory sideband at `src0 + (simm12 << 3)` and do not treat it as a
  real LSU/data-memory implementation. `OP_C_SETC_EQ` shares the no-writeback
  compare-row shape with `C.SETC_NE` but publishes equality on the reduced
  branch-decision sideband. Bounded live-QEMU captures may end inside an
  8-byte F4/IB window; in that case the frontend fetch RF/ALU harness may accept a
  DUT dense-packet superset only for the final captured expected row while
  still comparing every committed row in the captured prefix. If that final
  packet contains post-prefix slots, stop after the compared prefix instead of
  draining those extra slots into backend state and requiring full top idle.
  Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`, and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r121-coremark-ldi-setceq-tail-256-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 256 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced LDI/SETC_EQ handling or bounded-capture tail-prefix
  policy. The R121 evidence compares one hundred seventy-three scalar/macro
  rows with zero mismatches.
- Phase 5/R122 CoreMark read-only load-lookup work replaces the previous
  zero-only `C.LDI`/`LDI` shortcut with an explicit reduced lookup bridge:
  `ReducedScalarAluExecute` publishes `loadLookupValid/loadLookupAddr`, the
  live RF/ALU top exposes `loadLookupData`, and the Verilator harness reads
  eight little-endian bytes from the same sparse ELF memory image used for
  instruction fetch. Missing bytes return zero. This is read-only harness
  evidence, not an LSU/cache/store-forwarding implementation, and stores must
  not mutate or depend on this image until a later packet adds explicit memory
  mutation or connects the real LSU/STQ path. R122 also admits `OP_SETC_LTU`
  as a no-writeback unsigned branch sideband and lets the QEMU row reducer
  accept the observed local-alias `ADDI` to T, `C.MOVR` from local T0, and
  `LDI` to U shapes. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r122-coremark-prefix-before-redirect-marker-470-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 470 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced read-only load lookup, SETC_LTU branch sidebands, or
  local-alias QEMU row reduction. The R122 evidence compares 315 normalized
  rows with zero mismatches. A 486-row probe exposed the redirecting
  `C.BSTART` allocation policy at `pc=0x400055d4`; settle marker policy before
  claiming larger windows, and do not promote the following `OP_SD` indexed
  store without store memory mutation or LSU/STQ ownership.
- Phase 5/R123 CoreMark direct-active marker-boundary work extends the reduced
  live fetch RF/ALU envelope through the redirecting marker at `pc=0x400055d4`.
  Preserve the model block-kind split: an active `Direct` or `Call` marker
  block redirects unconditionally to its recorded active target at the next
  marker boundary and suppresses allocation of that boundary marker; an active
  `Cond` marker block uses the SETC result directly, where false allocates
  fallthrough and true redirects. The live RF/ALU Verilator harness must also
  collect both slots of a legal two-row commit window in slot order before
  comparing rows. Run
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r123-coremark-redirect-marker-486-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 486 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing active marker-boundary redirect policy, live RF/ALU commit-window
  collection, or CoreMark marker handling. The R123 evidence compares 323
  normalized rows with zero mismatches. The next frontier is `OP_SD` at
  `pc=0x400055f2`; do not promote it without explicit store memory mutation or
  a real LSU/STQ path.
- Phase 5/R124 CoreMark indexed-store work extends the reduced live fetch
  RF/ALU envelope through the `OP_SD` row at `pc=0x400055f2` and a 544-row
  capture. Preserve the model source mapping exactly:
  `src0=SrcD`/bits `[31:27]` is the store payload, `src1=SrcL`/`rs1` is the
  address base, and `src2=SrcR`/`rs2` is the scaled index. The reduced execute
  owner emits a no-writeback 8-byte store sideband with
  `addr = srcData(1) + (srcData(2) << 3)` and `wdata = srcData(0)`. The current
  QEMU row schema still has only `src0` and `src1`, so the completion row
  projects visible base/index as QEMU sources while keeping the payload-first
  model order internally. Admit `OP_SD` only where that projection is valid or
  where a future packet extends the trace schema or routes through LSU/STQ. The
  live RF/ALU harness may mutate the sparse memory image only after the
  expected committed 8-byte store row matches the DUT row; this is a
  program-order reduced-load bridge, not store forwarding, cache state, or a
  real STQ. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r124-coremark-op-sd-544-probe-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 544 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing `OP_SD` source mapping, reduced store sidebands, sparse memory
  mutation, or live RF/ALU load lookup. The R124 evidence compares 357
  normalized rows with zero mismatches. The next packet should run a larger
  bounded CoreMark probe to identify the next unsupported or mismatching row.
- Phase 5/R253 reduced-store STQ pressure work fixes the opt-in
  `--reduced-store-dispatch-stq` CoreMark path after the R247-R252 failures.
  Reusable triage rules: do not match `ReducedStoreCommitFreeOwner` by physical
  ROB sideband; match committed store rows to STQ rows by model
  `CommitTrace.identity` (`bid/gid/rid`) plus STID. If a committed store is
  observed before the split-store path has inserted a ready `ST_ALL` row, buffer
  that committed-store identity and mark the STQ row when it later becomes
  resident and markable. Split-store rows may bypass local T/U source sequence
  lookup at `ScalarTURenameBridge` while preserving the sidecars for store/STQ
  owners; otherwise reduced OP_SD/SDI paths can falsely underflow the local
  sequence before full T/U store execution exists. Run
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only ScalarTURenameBridge`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedStoreCommitFreeOwner`,
  and the reduced-store QEMU ELF wrapper after changing these contracts. R253
  evidence: 240 raw CoreMark QEMU rows compare 162 normalized rows with zero
  mismatches, and a direct replay of the 726-row R252 expected stream emits 495
  architectural rows with zero neutral-comparator mismatches.
- Phase 5/R259 reduced-store overlay visibility work fixes the next
  no-harness-mutation load failure after R258. Reusable triage rule:
  store-visible load data in a reduced memory overlay must include
  ROB-committed or `storeCommitQ`-equivalent store fragments before SCB
  acceptance. LinxCoreModel `STQ::lookupForLoad` can use committed
  `storeCommitQ` state before `STQ::commit` drains that store into SCB, so an
  overlay fed only by `SCBRowBank.acceptedMask` can be too late. Preserve the
  R253 model-identity mark/free rule, and keep SCB accepted `last` fragments as
  the STQ free source; the commit-row feed is a reduced load-visibility bridge,
  not a new free owner. R262 adds the lane-order companion rule: same-cycle
  reduced overlay store request lanes must be presented old-to-young because
  `ReducedStoreMemoryOverlay` applies lanes sequentially and later lanes
  overwrite overlapping bytes. Current SCB accepted fragments selected from
  registered `STQCommitQueue` state are older than current ROB commit-row
  bypass fragments, so route SCB accepted lanes before current commit-row lanes
  while preserving R259 visibility and keeping SCB accepted `last` as the only
  STQ free source. Run
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`
  plus a `FETCH_DISABLE_STORE_MEMORY_MUTATION=1` reduced-store replay after
  changing this path. The R259 2048-row replay compares 1467 rows with zero
  mismatches in
  `generated/r259-reduced-store-overlay-commit-row-2048-trace-xcheck/report/crosscheck_manifest.json`.
- Phase 5/R125 CoreMark SUBI/C.AND/C.SDI work extends the reduced live fetch
  RF/ALU envelope through a 1024-row CoreMark capture. Preserve the reduced
  row-source contracts: `OP_SUBI` computes `src0 - uimm12`; 32-bit `OP_ADD`
  may validate each encoded source independently as visible scalar or
  suppressed local T/U; compressed local `OP_C_AND` shares the `OP_C_ADD`
  implicit T-destination contract and may synthesize the missing QEMU
  destination/writeback only for this local arithmetic trace-gap shape; and
  `OP_C_SDI` is a no-writeback 8-byte store with address from the encoded
  compressed base plus signed bits `[15:11] << 3` and payload from T0. The live
  RF/ALU harness may mutate sparse memory only after the expected committed
  `C.SDI` store row matches the DUT row, matching the R124 committed-store
  bridge policy and still not claiming LSU/STQ/cache/store-forwarding
  ownership. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r125-coremark-1024-frontier-probe-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 1024 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing reduced SUBI/C.AND/C.SDI semantics, encoded local/scalar ADD
  row reduction, compressed local trace-gap synthesis, or committed sparse
  memory mutation. The R125 evidence compares 665 normalized rows with zero
  mismatches.
- Phase 5/R126 CoreMark PCR-return and byte-store work extends the reduced
  live fetch RF/ALU envelope through a 1415-row CoreMark capture. Preserve the
  reduced row-source contracts: 32-bit PCR load immediates are unshifted signed
  bits `[31:15]`; 48-bit `HL.*.PCR` loads use unshifted
  `Cat(pfx16[15:4], main32[31:15])`; `BSTART` immediates remain shifted
  branch targets; `C.SETC.TGT`/`SETC.TGT` publish a live dynamic target;
  `FRET.STK` is a no-writeback scalar redirect row whose `next_pc` must be
  compared; and `DecodeRenameROBPath` must clear active marker target state on
  execute-owned scalar redirects so the return target body seeds a fresh
  scalar-created block. Ranged `FENTRY` save addresses use the encoded save
  count, `ADDW` sign-extends the low-32-bit sum, and `SBI` emits a
  no-writeback 1-byte store at `base + unscaled_split_imm`. The comparator
  must treat side-effect-free macro/template rows as metadata only when they
  are sequential; non-sequential rows such as `FRET.STK` stay in the compare
  stream. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r126-coremark-fret-scalar-redirect-1415-qemu-elf-xcheck-pass --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 1415 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing PCR load immediates, SETC target/FRET redirect handling,
  scalar-redirect active-block lifecycle, ranged FENTRY, ADDW/SBI semantics, or
  macro/template metadata filtering. The R126 evidence compares 927 normalized
  rows with zero mismatches.
- Phase 5/R174 block-marker lifecycle work makes active block context
  STID-indexed instead of global. Preserve the model ownership shape:
  `BRQ::stashH[stid]`, `BRQ::brq[stid]`, `BCtrlUnit::currentBID[stid]`,
  `BlockROB::current/next[stid]`, and `DCTop::lastHeader[stid]` are per
  scalar thread. In Chisel, `BlockMarkerLifecycle` must use `markerStid` for
  decode-time marker-only rows, `retiredMarker.stid` for serialized retired
  marker sources, `activeQueryStid` for scalar row BID reuse/diagnostics,
  `scalarBlockStartStid` for scalar-created active blocks, and
  `scalarRedirectStid` for execute-owned redirect cleanup. A scalar redirect
  must clear only the redirecting STID lane; ROB block-last cleanup matches the
  exact `(STID,BID)` lane because BID slots are per-STID, not global. Run
  `bash tools/chisel/run_chisel_tests.sh --only BlockMarkerLifecycleSpec`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPathSpec`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTopSpec`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r174-stid-marker-lifecycle-6000-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 6000 --allow-block-markers --allow-block-loop-reentry --max-seconds 16 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing marker active-state lane selection, scalar redirect cleanup,
  scalar-created block seeding, or retired-marker lifecycle STID routing.
- Phase 5/R175 marker-row ROB-admission shell lets unskipped `BSTART`/`BSTOP`
  rows rename-update their reserved ROB row, stay off the reduced scalar
  issue/ALU path, and complete internally through the ROB completion port.
  Preserve the boundary: this is not the full live marker lifecycle switch.
  Full marker-row replacement still needs a decode/retire split, or equivalent
  proof, so following scalar rows receive the new boundary BID before the
  marker row retires while retire-time scalar-done/redirect semantics do not
  double-close the same block. The live CoreMark top remains in
  `skipBlockMarkers=true` mode until that split is implemented. Run
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPathSpec`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTopSpec`,
  `bash tools/chisel/run_chisel_tests.sh --only DispatchROBAllocatorSpec`,
  `bash tools/chisel/run_chisel_tests.sh --only ROBEntryBankSpec`, and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r175-marker-row-completion-shell-6000-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 6000 --allow-block-markers --allow-block-loop-reentry --max-seconds 16 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing marker-row rename consumption, internal marker completion,
  external completion arbitration, or the live marker-skip regression surface.
- Phase 5/R176/R177/R178/R179/R180 marker decode context splits following-row BID assignment from
  retire-time marker effects. `BlockMarkerDecodeContext` is the decode-time
  owner: decoded `BSTART` rows must use the allocator's new BID even when
  an older active context exists, following scalar rows must reuse that new BID,
  decoded `BSTOP` rows must reuse and clear the active BID, and
  flush/redirect/ROB block-last cleanup must stay STID-scoped. R177 wires this
  owner into `DecodeRenameROBPath` only behind `useMarkerDecodeContext=true`;
  R178 adds `LinxCoreFrontendFetchRfAluMarkerRowsTraceTop` as the named
  non-default top wrapper with `skipBlockMarkers=false` and
  `useMarkerDecodeContext=true`; R179 adds
  `run_chisel_frontend_fetch_rf_alu_marker_rows_smoke.sh` as the first
  generated-RTL proof that the wrapper admits a CoreMark `C.BSTART` marker row
  and makes the following scalar row reuse that marker's selected BID.
  R180 adds `--marker-rows` to
  `run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh`: the wrapper emits the
  marker-row top, passes `--admit-marker-rows` to the generated-RTL driver,
  admits legal markers into ROB, validates marker-shaped commits, filters those
  marker commits from the scalar comparator stream, and keeps the existing QEMU
  scalar reference format unchanged. The first proof admits one marker row,
  filters one marker commit, compares the following three scalar rows, and
  passes with zero mismatches; the default top regression on the same prefix
  stays in skip mode with zero admitted marker rows. R192 extends marker-row
  mode through the 128-row repeated-loop CoreMark window: while an admitted
  marker drain barrier holds dense slots, backend decode inputs must be
  invalidated; a retired redirect boundary can complete the previous active BID
  and still own a marker-only BROB entry that needs its own later scalar-done
  pulse; and redirect cleanup must not cancel an already pending
  `BlockScalarDoneSequencer` retire/free pulse. R194 extends the filtered
  marker-row comparator through a 512-row CoreMark capture and fixes a
  generated-RTL harness tail-prefix rule: when a bounded expected stream ends on
  an admitted marker row, the driver must keep draining marker-shaped commits
  until those expected marker rows are filtered, while still failing on any
  scalar commit past the captured prefix. The proof admits and filters 161
  marker commits and compares 337 scalar/macro rows with zero mismatches.
  Preserve the separate `decodeValid` candidate decision and `decodeFire` state
  update; collapsing them creates allocator-ready feedback through
  `allocUsesExistingBlock`. Do not wire the live top out of
  `skipBlockMarkers=true` until the filtered marker-row comparator scales
  beyond the first CoreMark prefix and checks stop, redirect, and cleanup
  lifecycle side effects. Run
  `bash tools/chisel/run_chisel_tests.sh --only BlockMarkerDecodeContextSpec`,
  `bash tools/chisel/run_chisel_tests.sh --only BlockMarkerLifecycleSpec`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPathSpec`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTopSpec`,
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_marker_rows_smoke.sh`,
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r180-marker-row-filtered-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 3 --capture-rows 16 --allow-block-markers --marker-rows --max-seconds 10 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`,
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r180-default-skip-regression-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 3 --capture-rows 16 --allow-block-markers --max-seconds 10 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`,
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r192-marker-row-brob-retire-drain-128-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 128 --allow-block-markers --allow-block-loop-reentry --marker-rows --max-seconds 16 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`,
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r192-default-skip-regression-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 3 --capture-rows 16 --allow-block-markers --max-seconds 10 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`,
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r194-marker-row-scale-512-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 512 --allow-block-markers --allow-block-loop-reentry --marker-rows --max-seconds 20 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r178-marker-row-harness-prep-6000-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 6000 --allow-block-markers --allow-block-loop-reentry --max-seconds 16 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing decode-time marker active context, selected block-BID choice,
  marker lifecycle split wiring, the opt-in backend path, or marker-row harness
  migration.
- Phase 5/R127 CoreMark return-block cleanup work extends the reduced live
  fetch RF/ALU envelope through a 1461-row CoreMark capture. Preserve these
  reusable contracts: emitted `LinxCoreFrontendFetchRfAluTraceTop` uses a
  32-entry scalar mapQ for this gate; local-overlay backpressure must be gated
  by whether the dec/ren head actually uses T/U local sources; `FRET.STK`
  redirects to explicit SETC target first and active-marker target second;
  scalar execute redirects flush backend issue/execute/rename/ROB/report state
  and full-BID BROB block state, while marker redirects remain frontend
  restarts; scalar redirects must complete the active BROB block before
  clearing active marker context; `FRET.STK` has no visible operands; `FENTRY`
  uses an implicit top-owned SP shadow, clears visible source 1, and suppresses
  ranged save store data in the reduced trace; reduced issue pick must not
  re-cancel an already selected row because later diagnostic readiness drops;
  BROB `Flushed` slots are non-live and allocatable; conditional marker-only
  state with no target or no possible branch producer falls through; and a
  marker allocation that would reuse the active slot must pre-retire that
  active BID. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarIssueQueue`,
  `bash tools/chisel/run_chisel_tests.sh --only BROB`,
  `bash tools/chisel/run_chisel_tests.sh --only DispatchROBAllocator`,
  `bash tools/chisel/run_chisel_tests.sh --only DecodeRenameROBPath`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r127-brob-flushed-reuse-1461-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 1461 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing scalar redirect cleanup, BROB allocation readiness, FRET/FENTRY
  macro shape, local-overlay gating, issue selected-readiness, marker
  fallthrough/pre-retire policy, or backend redirect cleanup. The R127 evidence
  compares 966 normalized rows with zero mismatches.
- Phase 5/R136 CoreMark LDI-local-T work extends the reduced live fetch RF/ALU
  envelope through a 1620-row capture. Preserve the `FRET.STK` hidden SP
  restore: on the condition-false RA-load path the visible commit row writes
  only `x10/ra`, but architectural `x1/sp` is restored to
  `stackPointerData + imm`; reduced tops without a real macro-retire owner
  should keep an SP shadow and source later architectural `x1` reads from it
  rather than adding an ad-hoc second RF write. The same packet admits
  32-bit `OP_LDI` to local `x31/T0` while keeping scalar RF writeback limited
  to scalar GPR destinations. Run
  `python3 tools/chisel/frontend_fetch_rf_alu_qemu_rows.py --self-test`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `bash tools/chisel/run_chisel_tests.sh --only LinxCoreFrontendFetchRfAluTraceTop`,
  and
  `bash tools/chisel/run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh --build-dir generated/r136-ldi-t-dst-1620-qemu-elf-xcheck --elf tests/benchmarks/build/coremark_real.elf --expected-rows 0 --capture-rows 1620 --allow-block-markers --max-seconds 8 -- -nographic -monitor none -machine virt -m 1280M -kernel tests/benchmarks/build/coremark_real.elf`
  after changing FRET.STK RA-load return, SP-shadow sourcing, local T/U
  destination admission, reduced LDI load lookup, or bounded final dense-window
  handling. An in-flight FRET.STK must sample its SETC condition in E1 and
  carry that sample through W1/W2; a younger marker may then clear the shared
  block-condition latch without changing the older return. With live first-pass
  LIQ enabled, ordinary loads transfer lookup ownership to LIQ, but the
  synthetic FRET RA load must remain direct-execute eligible and retain direct
  sparse-memory lookup. Select the RA load for an explicit condition-false
  return, or when the condition is absent and neither SETC nor active-marker
  target exists; otherwise a live target owns the redirect. The R136 evidence compares 1094 normalized rows with zero
  mismatches; a QEMU-only 1660-row probe reaches `OP_CSEL` at `pc=0x40005d32`.
  R137 classifies that frontier as a model/QEMU source-order divergence, not a
  reduced RTL implementation target: Sail and LinxCoreModel select `SrcL` when
  `SrcP != 0`, while current QEMU selects `SrcR`. Do not add reduced Chisel
  `OP_CSEL` support by copying QEMU until the architecture/model/QEMU contract
  is resolved.
- Phase 5/R81 reduced scalar ALU completion work adds the first generated RTL
  comparison gate where a Chisel execute owner, not an external surrogate,
  marks a frontend-decoded ROB row complete with nonzero source, destination,
  and writeback data. Run `run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `run_chisel_tests.sh --only LinxCoreFrontendAluTraceTop`, and
  `run_chisel_frontend_alu_trace_top_xcheck.sh` after changes to scalar ALU
  execute completion, `completeRow` payload wiring through
  `DecodeRenameROBPath`/`DispatchROBAllocator`/`ROBEntryBank`, or the frontend
  ALU trace-top driver. Keep the old `run_chisel_frontend_trace_top_xcheck.sh`
  as the R80 surrogate regression gate. Treat `operandData` on the ALU trace
  top as temporary harness input; the next replacement evidence must move
  operand sourcing into RF/ready-table/issue owners rather than adding more
  top-level fixture values.
- Phase 5/R82 reduced scalar RF-backed ALU source work replaces the R81
  top-level per-uop `operandData` fixture with persistent physical RF state for
  dependent scalar rows. Run `run_chisel_tests.sh --only
  ReducedScalarRegisterFile`, `run_chisel_tests.sh --only
  ReducedScalarAluExecute`, `run_chisel_tests.sh --only
  LinxCoreFrontendRfAluTraceTop`, and
  `run_chisel_frontend_rf_alu_trace_top_xcheck.sh` after changes to scalar RF
  operand sourcing, ALU physical-destination writeback metadata, or the shared
  frontend ALU trace-top driver. Keep `run_chisel_frontend_alu_trace_top_xcheck.sh`
  as the R81 operand-fixture regression and
  `run_chisel_frontend_trace_top_xcheck.sh` as the R80 surrogate regression.
  Treat `rfAllReadReady` in the R82 top as diagnostic only; do not feed an
  accepted-output readiness bit back into `ScalarDecodeRenameBridge.outReady`
  until an issue/ready-table owner exposes pre-accept source readiness.
- Phase 5/R83 reduced scalar issue-queue work inserts
  `ReducedScalarIssueQueue` between `DecodeRenameROBPath` and
  `ReducedScalarAluExecute` in the RF-backed ALU trace top. Run
  `run_chisel_tests.sh --only ReducedScalarIssueQueue`,
  `run_chisel_tests.sh --only LinxCoreFrontendRfAluTraceTop`, and
  `run_chisel_frontend_rf_alu_trace_top_xcheck.sh` after changes to scalar
  issue enqueue/dequeue, RF source-readiness gating, the RF-backed top, or the
  shared frontend ALU trace-top driver. Keep
  `run_chisel_frontend_alu_trace_top_xcheck.sh` as the R81 operand-fixture
  regression and `run_chisel_frontend_trace_top_xcheck.sh` as the R80
  surrogate regression. In the reduced lane, `ScalarDecodeRenameBridge`
  acceptance must remain driven by downstream issue-queue capacity; RF
  physical source readiness gates only queue-head issue.
- Phase 5/R84 reduced issue release work makes the RF-backed scalar issue
  queue keep selected rows resident as issued entries until the ALU returns a
  model-derived release identity. Run `run_chisel_tests.sh --only
  ReducedScalarIssueQueue`, `run_chisel_tests.sh --only ReducedScalarAluExecute`,
  `run_chisel_tests.sh --only LinxCoreFrontendRfAluTraceTop`, and
  `run_chisel_frontend_rf_alu_trace_top_xcheck.sh` after changes to issued
  residency, release identity, ALU W2 release, or top-level issue diagnostics.
  In this reduced lane, execute acceptance marks the FIFO head issued; it must
  not remove the row. Removal waits for a later `(bid, rid, stid)` release,
  including unsupported reduced opcodes that still reached W2. The R84 queue
  remains a head-only FIFO surrogate and does not replace full model
  `IssueState` age select, P1/I1/I2 timing, cancel, replay, or bypass behavior.
- Do not run SBT-backed Chisel wrappers in parallel yet; a parallel ROBID test
  and ROBID bookkeeping invocation hit an SBT 2 server socket
  `Connection refused` race, while the same gates pass sequentially.
- Verilator wrappers must compile every emitted SystemVerilog file for the
  selected target, not only the named top file, because CIRCT emits instantiated
  Chisel modules as sibling `.sv` files. This applies to both the reduced ROB
  xcheck and `run_chisel_verilator_lint.sh`.
- `LinxCoreFrontendFetchRfAluTraceTop` is already close to the JVM constructor
  method-size limit. For dormant owner packets, prefer module-local diagnostics
  and defer top integration unless an external wrapper consumes the signals or
  an existing owner can absorb the logic without growing the top constructor.
  Do not add a new batch of top-level diagnostic IO, width assertions, or
  standalone dormant owner instances casually. If a focused top gate fails with
  `Method too large`, first remove or compact the new top fanout/instance
  before changing replay logic.
- When a dormant source-return or replay cluster already has several direct
  children in `LinxCoreFrontendFetchRfAluTraceTop`, a constructor-relief packet
  may replace that cluster with one composite owner. Keep future raw request,
  identity, response, and sideband inputs at the composite IO boundary and tie
  them off in the top helper; tying them false inside the composite can let
  FIRRTL eliminate the child owner during module-level elaboration and hide the
  boundary that future packets need to promote.
- Replay-LIQ local STQ snapshot source-return must preserve the accepted query
  identity. Once a query issues for a selected row, response matching must use
  a token or queued owner captured from that accepted `cID/eID` rather than the
  current launch selector, query issue must be gated by token capacity, and the
  token may clear only at the ordered response consumption boundary.
- Queue owners that feed a downstream matcher must keep head visibility
  independent of downstream ready when that ready is derived from the matcher
  consuming the head. Empty-slot bypass may expose a new head in the same
  cycle, but only storage/count updates should depend on dequeue ready;
  otherwise FIRRTL can report a response-valid/dequeue-ready combinational
  cycle during path elaboration.
- Live-control policy owners that may later drive both request issue and sink
  readiness must take request-capacity inputs from pre-cycle resident state
  (for example `!requestQueue.full`), not same-cycle `enqueueReady` values that
  may depend on a policy-controlled sink/dequeue. Same-cycle drain can make room
  for storage, but it must not open a new policy request arm through a
  request/sink/dequeue/queue-ready combinational loop. When the policy output
  is muxed into a composite path, apply the same rule at the path request-control
  boundary; an unselected `enqueueReady` mux branch can still leave a FIRRTL
  dependency cycle if the selected sink arm controls the queue dequeue.
- Replay-LIQ local STQ snapshot response drains must not infer stale from a
  simple nonmatch. A nonmatching FIFO head may belong to a later token once
  multi-token query ownership exists. Only explicit row-state evidence
  equivalent to the model `entry.fsm != MTC_LDQ_REPICK` check may authorize a
  stale-head drop, and stale drops must not clear the accepted query token.
- Packet B FlushControl work must preserve LinxCoreModel `CheckOlder` branch
  order: different `stid` never compares; same-BID BID-based priority resolves
  before PE-replay special cases; same non-BID BID/RID conflicts resolve before
  generic age; PE-vs-PE age only compares within one PE.
- Packet C BROB/BID work must preserve the hardware BID contract:
  each STID has a default 256-entry BROB ring,
  `BID_W = ceil(log2(BROB_ENTRIES))`, and default BID is 8 bits. Shared block
  identity is `(STID,BID)`; STID is separate, while wrap, generation, and age
  stay in per-STID BROB-owned state. `(cmd_stid,cmd_tag) = (stid,bid)`. Flush
  uses an STID-qualified BROB younger-entry kill mask or equivalent ring
  context; unsigned BID magnitude is never an age comparison.
- Chisel BROB order state must own independent allocation-tail, commit-head,
  and bounded live-count registers per STID. Allocation advances only the tail;
  exact completed-head retirement advances only the head; accepted recovery
  validates and truncates tail/count without moving the head. Model
  `MISS_PRED_FLUSH` reports the first killed block and restores inclusively;
  retained-target scalar nuke/inner/fast flush restores to the target
  successor. Metadata pruning must consume the same owner head/count and use
  bounded modular distance, including windows spanning implementation BID
  rollover; raw unsigned BID magnitude is not an age test.
- Scalar/engine completion is persistent BROB metadata, not retirement
  authority. A younger completed block waits behind the exact resident head.
  Shared retirement must arbitrate eligible STID heads fairly and hold the
  selected full `(STID,BID)` irrevocably under backpressure. Metadata free,
  commit-head advance, live-count decrement, downstream block-commit enqueue,
  and public retire fire must share one handshake. Keep non-flush, store-range,
  replay, and configurable multi-block-retire claims separate until those
  owners exist.
- Scalar LSID/load-ID/store-ID counters are independent per STID and advance
  only at the accepted decode boundary. Scoped recovery mutates only the exact
  STID lane; reset/restart is the explicit all-lane clear. Keep these
  per-instruction identities separate from BROB aggregate block ranges.
- BROB block store ranges own a separate cursor and next store ID per STID.
  Assign a stable start to the exact resident cursor row, stop on an unknown
  count or identity hole, and advance only through consecutive count-certain
  rows using the owner head/live-count window. Scalar-done may freeze an
  accumulated scalar count; template/tile counts require an authoritative
  explicit producer. Accepted suffix recovery restores the first killed
  row's saved start when assigned. Range assignment is not non-flush proof and
  must never authorize STQ commitment or SCB admission.
- Treat scalar and explicit block store-count publication as retained owner
  traffic, not advisory pulses. Admit explicit CTU/tile payloads only for an
  exact identity inside the selected STID's owner head/live-count window;
  preserve them under sink backpressure and cancel them only with the accepted
  recovery that kills their full BID. Keep scalar closure independently
  resident because it is not backpressurable.
- On count-source collision, an explicit value wins only for the same exact
  `(STID,full BID)`; different blocks serialize scalar-first while explicit
  stays pending. An agreeing frozen-count repeat is idempotent; a conflicting
  explicit value is an integration error and must not rewrite the row. Do not
  retire the exact BROB head until normal completion and range count certainty
  are both true.
- Audit model call sites before promoting a declared mechanism. Current model
  DCTop/Decoder/GenCoder accumulation and `deliveryStoreID` are active, while
  `BlockROB::setStoreCount` and DCTop `calcLSCnt` have no active caller. Use
  dormant code as design intent only, and document the real Chisel producer
  boundary instead of claiming inactive model flow as behavioral evidence.
- Public allocator readiness/fire, resident ROB allocation valid, BROB
  allocation valid, and cursor advance must come from one recovery-qualified
  admission decision. An accepted recovery cycle must not let a child ROB row
  allocate while the public allocator reports no fire. Generated proof must
  include simultaneous allocation/recovery and verify that neither child owner
  mutates until coherent admission resumes.
- Commit trace work must keep the LinxCoreModel `CommitInfo` identity
  `bid/gid/rid` as 32-bit model sideband fields while preserving the
  hardware block identity separately as `(stid, BID_W-bit block_bid)`; do not
  merge the model and hardware identity domains.
- Fixed-width Chisel commit trace dumps may include invalid slots, but
  `tools/chisel/trace_schema_adapter.py` must filter `valid: 0` rows before
  sequence numbering and QEMU comparison.
- Reduced ROB harness work must preserve the LinxCoreModel commit walk: retire
  only contiguous completed rows from the head, stop on the first invalid or
  incomplete head, reject duplicate live `(bid,gid,rid)` identities, and emit
  `CommitTraceRow` rows in commit slot order. Full flush rebasing, deallocation,
  rename cleanup, LSU/STQ side effects, and precise trap ownership remain
  deferred to integrated ROB/CMT.
- Phase 5 integrated ROB/CMT work must run
  `bash tools/chisel/run_chisel_tests.sh --only ROBEntryStatus` before
  changing ROB entry-bank state. Preserve the LinxCoreModel `PROBStatus` order:
  `Free=0`, `Allocated=1`, `Renamed=2`, `Issued=3`, `Completed=4`,
  `Retired=5`, `Fault=6`, `NeedFlush=7`. Commit consumes only `Completed`
  rows and changes them to `Retired`; deallocation consumes only `Retired`
  rows and changes them to `Free`. Do not collapse the two walks into one
  status transition.
- Phase 5 `ROBEntryBank` work must run
  `bash tools/chisel/run_chisel_tests.sh --only ROBEntryBank`. The entry bank
  preserves separate `allocPtr`, `commitPtr`, and `deallocPtr` walks:
  allocation creates `Allocated` rows and increments resident/outstanding
  counts, completion marks eligible rows `Completed`, commit emits monitored
  contiguous completed-head rows and changes them to `Retired`, and deallocation
  frees only later-visible `Retired` rows. Retired rows remain resident and
  reject duplicate `(bid,gid,rid)` identities until deallocation clears them.
  Full flush rebasing, rename cleanup, LSU/STQ side effects, precise traps, and
  restart ownership remain future integrated ROB/CMT work; keep
  `ReducedCommitROB` as the reduced trace harness.
- Phase 5 `ROBFlushPrune` work must run
  `bash tools/chisel/run_chisel_tests.sh --only ROBFlushPrune`. The selector
  preserves the prune part of LinxCoreModel `SPEROB::flush`: scan from
  `deallocPtr`, match rows by `flush.bid <= row.bid` for base-on-BID requests
  or `(flush.bid, flush.rid) <= (row.bid, row.rid)` otherwise, start pruning at
  the first matching valid row, and prune every later valid row in scan order.
  Resident decrement counts every pruned valid row; outstanding decrement counts
  only `ROBEntryStatus.osdActive` rows. Keep pointer rebasing, row mutation,
  rename cleanup, LSU/STQ cleanup, precise traps, and restart ownership in the
  integrated ROB/CMT owner, not in this selector and not in `ReducedCommitROB`.
- When `ROBEntryBank` consumes `ROBFlushPrune`, an applied flush owns the bank
  cycle: suppress allocation, completion, commit, and deallocation; clear every
  row in `flushPruneMask`; decrement resident and outstanding counts with the
  selector outputs; rebase `allocPtr` to the first pruned row; and rebase
  `commitPtr` when the selector reports a pruned-before-commit row or the flush
  leaves no outstanding work.
- `ROBEntryBank` flush comparison must use native row BID/RID sidecars, not
  `CommitTraceRow.identity` sidebands. `allocBid` is supplied by the
  backend/BROB owner and stored in `rowBid`; RID is allocated locally from the
  bank allocation pointer and stored in `rowRid`. `CommitTraceRow.identity`
  remains the trace and duplicate-detection sideband.
- Phase 5 `DispatchROBAllocator` work must run
  `bash tools/chisel/run_chisel_tests.sh --only DispatchROBAllocator`. This
  bridge is the first backend integration owner for allocation: allocate a
  `BID_W`-bit BID from the BROB tail, allocate `BrobMetaTracker` and
  `ROBEntryBank` atomically, stamp `CommitTraceRow.blockBid`, carry separate
  BROB ring/wrap context wherever age is required, and keep RID allocation
  inside `ROBEntryBank`.
- Phase 5 `FullBidRecoveryBridge` work must run
  `bash tools/chisel/run_chisel_tests.sh --only FullBidRecoveryBridge`. This
  legacy-named bridge is an implementation migration point, not authority for
  a widened BID. It must preserve the `BID_W`-bit `blockBid`, accept
  BROB-qualified kill/order context for block cleanup, produce the typed
  `FlushBus.req.bid` sidecar for ROB row pruning, and keep
  rename restore, LSU/STQ cleanup, frontend redirect, PE replay fanout, and
  BROB pointer restoration in later cleanup owners.
- Phase 5 `RecoveryCleanupControl` work must run
  `bash tools/chisel/run_chisel_tests.sh --only RecoveryCleanupControl`. This
  module is the first registered cleanup-intent boundary after recovery
  selection: classify global flush, global replay, and PE-scoped replay; expose
  BCTRL, rename, backend, frontend, LSU/STQ, tile, PE fanout, and ROB prune
  intent bits; and keep actual consumer mutation in owner packets such as
  `GPRRenameCheckpoint`, `STQFlushPrune`, frontend restart payload owners, and
  BROB pointer restoration instead of `ROBFlushPrune` or generic top-level
  glue.
- Phase 5 `GPRRenameCheckpoint` work must run
  `bash tools/chisel/run_chisel_tests.sh --only GPRRenameCheckpoint`. This
  module is the first scalar rename-map consumer of
  `RecoveryCleanupControl.intent`: own scalar `smap`/`cmap`, per-BID
  checkpoints, `renamePtr`, free physical GPR mask, and finite map queue for
  STID0. Its current `flush.bid - 1` restore is a legacy reduced behavior; new
  work must use the selected STID's BROB-qualified predecessor/generation
  context, falling back to `cmap` when invalid. Prune map-queue rows by
  `baseOnBid` or BID/RID ordering and re-apply surviving same-BID non-base
  entries to `smap`. Treat replay as
  observed-only here; ClockHands, T/U operands, SGPR, multithread, and full
  dispatch/commit wiring remain later owners.
- Phase 5 `STQFlushPrune` work must run
  `bash tools/chisel/run_chisel_tests.sh --only STQFlushPrune`. This module is
  the first concrete LSU/STQ consumer of `RecoveryCleanupControl.intent.flush`:
  mirror `FlushBus::match(MemReqBus)` including `stid`, optional PE/thread
  scoping, BID-only matching, group matching with the model BID fast path, and
  default BID+LSID matching; free only valid `STQ_WAIT` rows; and leave full
  STQ RAM mutation, `storeCommitQ`, SCB/MDB, memory queues, and LSID rebasing
  to the later LSU/STQ owner.
- Phase 5 `STQEntryBank` work must run
  `bash tools/chisel/run_chisel_tests.sh --only STQEntryBank`. This module is
  the first STQ row-state owner: allocate first-free store rows, merge
  complementary `ST_ADDR`/`ST_DATA` halves into `ST_ALL`, track resident
  `size` and WAIT/outstanding `osdSize`, mark local ready WAIT rows as
  `STQ_COMMIT`, free committed rows only by explicit single-index or multi-row
  mask command, and apply `STQFlushPrune.freeMask` to clear matched WAIT rows.
  Multi-row committed free is the bank-side target for `STQCommitQueue` issue
  lanes: accepted committed rows decrement resident `size` once per row, and
  WAIT/outstanding `osdSize` is unchanged. Keep `storeCommitQ` ordering,
  memory-side request acceptance, SCB/MDB handoff, data-array banking, load
  forwarding, and LSID rebasing in later LSU owners.
- Phase 5 `STQCommitQueue` work must run
  `bash tools/chisel/run_chisel_tests.sh --only STQCommitQueue`. This module
  is the first `storeCommitQ` ordering owner after `STQEntryBank` marks rows
  committed: keep committed row indices sorted by `(bid, lsId)` using
  wrap-aware `ROBID` order, issue up to the configured commit width, skip
  downstream-stalled rows while preserving them in the queue, and compact issued
  rows. Drive `STQEntryBank.commitFreeMask` only after memory-side issue
  succeeds. Keep SCB/MDB handoff, cacheline split handling, TTrans/tile side
  effects, BSB window slide, data-array banking, and load forwarding in later
  LSU owners.
- Phase 5 `STQCommitDrain` work must run
  `bash tools/chisel/run_chisel_tests.sh --only STQCommitDrain`. This module is
  the first memory-side committed-store drain boundary after `STQCommitQueue`:
  compute row readiness from committed STQ row sidecars plus downstream
  single- or split-segment acceptance, emit one or two scalar memory request
  descriptors using the model `AddrCrossCacheline` / `GetCrossReq` split
  contract, preserve queue skip-around-stall behavior, and expose a standalone
  issue/free mask only for early bring-up and debug. In the full STQ-to-SCB
  composition, `SCBRowBank.commitFreeMask` is the final `STQEntryBank` free
  source. Keep SCB/MDB storage, CHI completion, TTrans/tile side effects, BSB
  window slide, data-array banking, and load forwarding in later LSU owners.
- Phase 5 `SCBCommitIngress` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBCommitIngress`. This module
  is the first scalar SCB ingress owner after `STQCommitDrain`: coalesce
  committed store fragments into 64-byte cacheline entries in lane order, merge
  little-endian byte data by `addr[5:0]` and `size`, publish post-merge
  line-valid wakeups, and report blocked fragments when no matching line or
  free entry exists. Keep SCB capacity feedback into `STQCommitDrain`, DCache
  lookup/update, SCB eviction, L2/CHI request/response handling, MDB conflict
  prediction, and store-to-load forwarding in later LSU owner packets.
- Phase 5 `SCBCommitBridge` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBCommitBridge`. This module
  is the first model-aligned capacity-feedback owner between `STQCommitDrain`
  descriptors and `SCBCommitIngress`: gate every descriptor with the
  conservative model `SCBuffer::full()` rule (`freeCount >= requestCount`),
  stall even structural same-line hits while that model batch gate is closed,
  and produce final `STQEntryBank.commitFreeMask` bits only from accepted
  descriptors with `last=1`. Keep SCB eviction, DCache/L2/CHI request/response
  handling, MDB conflict prediction, store-to-load forwarding, and full
  STQ-to-SCB composition in later LSU owner packets.
- Phase 5 `SCBEgressSelect` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBEgressSelect`. This module
  is the first SCB egress-selection owner after `SCBCommitBridge`: use
  `SCBEntryState` to mirror model `S_EMPTY/S_VALID/S_LOOKUP/S_MISS`, consider
  only valid rows for lookup issue, prefer full valid rows, and use a
  deterministic first-valid not-full fallback for the model's random eviction
  path. Keep DCache lookup/update, L2/CHI request/response state, SCB row free,
  MDB conflict prediction, store-to-load forwarding, and full STQ-to-SCB
  composition in later LSU owner packets.
- Phase 5 `SCBLookupControl` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBLookupControl`. This module
  is the first abstract DCache/L2 outcome owner after `SCBEgressSelect`:
  writable DCache hits emit byte-update and SCB-free intent, tag hits without
  write permission emit upgrade ownership requests, tag misses emit write
  ownership requests, and transaction tags use `(entryIndex << 2) | 2`.
  Keep actual DCache RAM mutation, registered SCB row mutation,
  WriteResp/UpgradeResp matching, MDB conflict prediction, store-to-load
  forwarding, and full STQ-to-SCB composition in later LSU owner packets.
- Phase 5 `SCBStateUpdate` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBStateUpdate`. This module
  is the first SCB row-state transition owner after `SCBLookupControl`:
  same-cycle accepted hit/miss masks are legal for a current `S_VALID` row or
  a response-returned `S_LOOKUP` retry row, writable hits clear rows,
  non-writable lookups move rows to `S_MISS`, and decoded WriteResp/UpgradeResp
  targets must name valid `S_MISS` rows before returning to `S_LOOKUP`.
  Accepted-only lookup starts still require `S_VALID`; a bare accepted mask on
  `S_LOOKUP` is illegal. Keep registered row-bank storage, raw response
  transaction-id decode, ingress/egress arbitration, DCache RAM mutation,
  L2/CHI queues, MDB conflict prediction, store-to-load forwarding, and full
  STQ-to-SCB composition in later LSU owner packets.
- Phase 5 `SCBRowBank` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBRowBank`. This module is
  the first registered SCB composition owner: own one row image, keep the model
  batch gate based on pre-cycle free count, stage accepted committed-store
  ingress before egress lookup payload generation, give response-returned
  `S_LOOKUP` rows priority over ordinary valid-row eviction, and keep
  `S_LOOKUP`/`S_MISS` rows closed to same-line store coalescing. Own the
  accepted-response handshake into `SCBResponseRetryQueue` so raw response
  dequeue, `S_MISS`-to-`S_LOOKUP` state update, and ordered retry enqueue share
  one accept boundary. Keep L2/CHI response queues, DCache RAM mutation, MDB
  conflict prediction, store-to-load forwarding, BSB window-slide side effects,
  and memory-event trace in later LSU owner packets.
- Phase 5 `STQSCBCommitPath` work must run
  `bash tools/chisel/run_chisel_tests.sh --only STQSCBCommitPath`. This module
  is the first full STQ-to-SCB composition owner: wire `STQEntryBank`,
  `STQCommitDrain`, and `SCBRowBank` so accepted `SCBRowBank` `last` fragments
  are the only committed-row free source back into the STQ bank; gate drain
  issue with the registered SCB pre-cycle model-batch condition; suppress drain
  issue during STQ flush-prune cycles; and treat `STQCommitDrain.commitFreeMask`
  as debug-only in the full composition. Keep L2/CHI response queues, DCache
  RAM mutation, MDB conflict prediction, store-to-load forwarding, BSB
  window-slide side effects, and memory-event trace in later owner packets.
- Phase 5 `SCBResponseDecode` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBResponseDecode`. This module
  is the raw SCB WriteResp/UpgradeResp tag owner: accept only response
  transaction ids encoded as `(entryIndex << 2) | 2`, reject absent or
  ambiguous response types, reject out-of-range decoded indices, and suppress
  stale responses to rows that are not valid `S_MISS`. Keep L2/CHI response
  queue arbitration, DCache RAM mutation, MDB conflict prediction,
  store-to-load forwarding, BSB window-slide side effects, and memory-event
  trace in later LSU owner packets.
- Phase 5 `SCBResponseBuffer` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBResponseBuffer` plus
  affected `SCBResponseDecode`, `SCBRowBank`, and `STQSCBCommitPath` gates.
  This module is the raw L2/CHI response FIFO boundary in front of
  `SCBResponseDecode`: preserve FIFO order and ready/valid backpressure,
  expose only the head to decode, and dequeue a head only after decode reports
  a legal valid-`S_MISS` target and the downstream response retry queue can
  accept the target row id. Keep DCache RAM mutation, MDB conflict prediction,
  store-to-load forwarding, BSB window-slide side effects, and memory-event
  trace in later LSU owner packets.
- Phase 5 `SCBResponseRetryQueue` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBResponseRetryQueue` plus
  affected `SCBResponseRetrySelect`, `SCBRowBank`, `SCBResponseDecode`,
  `SCBResponseBuffer`, and `STQSCBCommitPath` gates. This module is the exact
  LinxCoreModel `SCBuffer::resp_list` row-id FIFO owner: push each accepted
  WriteResp/UpgradeResp target row after legal decode, expose only the oldest
  retry head to selection, support same-cycle pop/push, and backpressure raw
  response dequeue when full. Keep DCache RAM mutation, MDB conflict
  prediction, store-to-load forwarding, BSB window-slide side effects, and
  memory-event trace in later LSU owner packets.
- Phase 5 `SCBResponseRetrySelect` work must run
  `bash tools/chisel/run_chisel_tests.sh --only SCBResponseRetrySelect` plus
  affected `SCBResponseRetryQueue`, `SCBRowBank`, `SCBStateUpdate`,
  `SCBEgressSelect`, and `STQSCBCommitPath` gates. This module consumes the
  queued `resp_list` head: only the oldest queued row may retry before ordinary
  `S_VALID` row eviction, a stale or non-`S_LOOKUP` head blocks ordinary egress
  and reports an error, and the ordinary egress selector remains responsible
  only for full-line priority and deterministic not-full fallback. Keep DCache
  RAM mutation, MDB conflict prediction, store-to-load forwarding, BSB
  window-slide side effects, and memory-event trace in later LSU owner packets.
- Phase 5 `MDBConflictDetect` work must run
  `bash tools/chisel/run_chisel_tests.sh --only MDBConflictDetect`. This module
  is the first store-arrival conflict classifier behind model `detect_su_lu_q`:
  scalar conflicts require address overlap plus
  `LessEqual(store.bid, store.lsID, load.bid, load.lsID)`, resolved active LDQ
  rows and `ResolveQ` rows are flush candidates, unresolved active rows are
  only marked wait-store for `ST_ADDR`, tile load/store conflicts are
  suppressed until the tile owner exists, and the selected resolved conflict is
  the oldest load by `(bid, lsID)`. Same-BID pairs classify as inner flush;
  cross-BID pairs classify as load-attributed nuke flush. Keep the MDB SSIT
  table, `lookup_lu_mdb_q`, `lookup_mdb_lu_q`, `lookup_mdb_su_q`,
  `record_lu_mdb_q`, `delete_lu_mdb_q`, store wakeup, byte forwarding, BCTRL
  `bmdb`, IEX-local MDB, ROB nuke retirement, and final `FlushReq`
  publication in later owner packets.
- Phase 5 `MDBSSIT` work must run
  `bash tools/chisel/run_chisel_tests.sh --only MDBSSIT`. This module is the
  first state owner for the model MDB Store Set ID Table: apply lookup, delete,
  and record commands in `MDB::Work` order; suppress only the first lookup on
  the recorded nuke BID; require both confidence and weight gates before a
  lookup stalls; reinforce same-store conflicts by raising confidence and
  saturating weight; replace different-store conflicts only when confidence is
  low or the new store is closer by `(bid offset, lsID offset)`; otherwise
  decrement confidence. Delete releases an entry only when weight is already
  zero, otherwise it decays weight and reports when the row drops below the
  stall threshold. Chisel must initialize first-insert `lsID_off`
  deterministically even though the C++ miss path leaves it implicit, and it
  must report finite-table overflow rather than silently inventing replacement.
  Keep lookup/record/delete queue wrappers, `StoreUnit::mdbCheck` wakeup, LDQ
  `updateMDBInfo`, BCTRL `bmdb`, IEX-local MDB, byte forwarding, ROB nuke
  retirement, and final `FlushReq` publication in later owner packets.
- Phase 5 `MDBQueueFanout` work must run
  `bash tools/chisel/run_chisel_tests.sh --only MDBQueueFanout`. This module
  is the first queue-boundary owner around `MDBSSIT`: own finite
  `lookup_lu_mdb_q`, `delete_lu_mdb_q`, `record_lu_mdb_q`,
  `lookup_mdb_lu_q`, and `lookup_mdb_su_q` equivalents; fan each lookup result
  atomically to both LU and SU outputs; and freeze delete/record phases behind
  a pending lookup when finite output backpressure prevents that atomic fanout.
  Accepted records may publish BMDB report intent, but BCTRL/IEX MDB table
  mutation remains outside this queue owner. The store-side MDB wakeup path
  must scan the STQ row view in row order, ignore tile rows, match the
  predicted store by `(bid, pc)`, and emit wakeup only when the first matching
  row has both address and data ready. Keep LDQ row mutation, MDB consumption
  of STQ PC sidecars, byte forwarding, ROB nuke retirement, and final
  `FlushReq` publication in later owner packets.
- Phase 5 `LoadStoreForwarding` work must run
  `bash tools/chisel/run_chisel_tests.sh --only LoadStoreForwarding`. This
  module is the first scalar store-to-load byte selector behind
  `STQ::lookupForLoad`: build the clipped 64-byte load mask, filter same-line
  scalar stores older than or equal to the load's `(BID, LSID)` allocation
  snapshot, select the nearest older store per byte using model `(BID, LSID)`
  order, forward only data-ready selected bytes, and report a wait/replay mask
  when the selected store for any requested byte is not data-ready. Do not use
  ROBID/BID-only ordering here; R264 found same-BID stores must compare LSID
  through `STQCommitQueue.lessEqualBidLs` to match `STQ::lookupForLoad`. It
  may merge forwarded bytes over cache data, but it must not
  mutate STQ rows, LDQ wait-store state, MDB state, DCache/SCB state, recovery
  publication, or memory-event trace. Later LIQ/LHQ/STQ integration may
  pipeline the E2 CAM, E3 merge, and E4 wakeup stages, but must preserve this
  per-byte nearest-store result.
- Phase 5 `ReducedStoreResidentForward` work must run
  `bash tools/chisel/run_chisel_tests.sh --only ReducedStoreResidentForward`
  plus the affected `LoadStoreForwarding`, `ReducedScalarAluExecute`, and
  `LinxCoreFrontendFetchRfAluTraceTop` gates. This module is the reduced-top
  adapter from resident `StoreDispatchSTQPath` rows into `LoadStoreForwarding`:
  convert raw load LSID with the same reduced `ROBID` shape as
  `StoreDispatchToSTQ`, apply ready resident store bytes after
  `ReducedStoreMemoryOverlay`, and expose forward/wait/eligible diagnostics
  plus the selected wait-store `(storeId, storeLsId, pc)` identity. Ready
  resident hits may feed execute. Wait-hit loads must hold execute rather than
  retiring committed-overlay pass-through data; cross-line resident cases still
  pass through the committed-overlay load data. Until LIQ/LDQ replay control
  exists, keep LDQ wait-store mutation, replay wakeup consumption, cross-line
  resident forwarding, MDB publication, and memory-event trace in later owner
  packets.
- Phase 5 `ResidentStoreReplayWakeup` work must run
  `bash tools/chisel/run_chisel_tests.sh --only ResidentStoreReplayWakeup`
  plus the affected `ReducedStoreResidentForward`, `LoadReplayWakeup`, and
  `LinxCoreFrontendFetchRfAluTraceTop` gates. This module is the producer-side
  bridge from resident STQ wait-store diagnostics to the generic
  `LoadReplayWakeupRequest`: select the `waitStore.storeIndex` row, require the
  row to still match `(storeId, storeLsId, pc)`, require scalar
  address/data-ready non-cross-line state, and publish source=`StoreUnit`,
  line address, byte-valid mask, and line-positioned store data. Do not invent
  a second replay-wakeup shape for reduced-top work. In the integrated reduced
  top, feed this producer from a registered wait-store key, not directly from
  the live forwarder: once the store data becomes ready, the live forwarder no
  longer reports a wait, so the key must already be held by the load-side
  replay owner. Until LIQ/LDQ integration exists, this producer must not
  relaunch a load or wake consumers.
- Phase 5 `ReducedLoadWaitReplaySlot` work must run
  `bash tools/chisel/run_chisel_tests.sh --only ReducedLoadWaitReplaySlot`
  plus `ResidentStoreReplayWakeup`, `LoadReplayWakeup`,
  `ReducedScalarAluExecute`, `ReducedStoreResidentForward`, and
  `LinxCoreFrontendFetchRfAluTraceTop` gates. This reduced-top diagnostic
  bridge captures the held E-stage load and selected wait-store key while
  `ReducedStoreResidentForward` reports a wait hit, feeds the registered key
  back to `ResidentStoreReplayWakeup`, and consumes the typed wakeup through
  the existing `LoadReplayWakeup` wait-store matcher. It may clear only its
  own diagnostic slot. It must not relaunch the load, wake dependents, mutate
  full LIQ/LDQ state, or bypass `LoadReplayWakeup` with ad hoc BID/LSID/PC
  matching.
- Phase 5 `LoadForwardPipeline` work must run
  `bash tools/chisel/run_chisel_tests.sh --only LoadForwardPipeline`. This
  module is the first registered E2/E3/E4 wrapper around
  `LoadStoreForwarding`: instantiate the selector in E2, register masks and
  merged data to E3, form final byte-valid state in E4, classify
  store-data-not-ready, data-incomplete, source-wait, and return-port-wait
  outcomes, and assert wakeup only when data is complete, source responses have
  returned, no wait-store byte remains, and the return slot is ready. Keep
  LIQ/LHQ/LDQ row mutation, STQ/SCB/MDB mutation, ready-table updates,
  issue-wakeup fanout, response queues, and memory-event trace in later owner
  packets.
- Phase 5 `LoadInflightQueue` work must run
  `bash tools/chisel/run_chisel_tests.sh --only LoadInflightQueue`. This
  module is the first registered LIQ/LHQ row owner around the forwarding
  pipeline: allocate slot-plus-wrap `LID`s with the load's
  `(youngestStoreId, youngestStoreLsId)` snapshot, launch only non-wait-store
  `Wait` rows through `LoadForwardPipeline`, apply E4 outcomes back to row
  state, publish LHQ
  records only for E4 hits, hold `StoreDataNotReady` rows as wait-store
  replays, and hold incomplete bytes as `L1DcMiss`/`missPending`. Keep precise
  `FlushBus` pruning, L1/L2 refill queues, ready-table updates, consumer
  bypass routing, a separate ResolveQ/LHQ queue, and memory-event trace in
  later owner packets.
- Phase 5 `LoadReplayWakeup` work must run
  `bash tools/chisel/run_chisel_tests.sh --only LoadReplayWakeup` and the
  affected `LoadInflightQueue` gate. This module is the first store-unit/SCB
  replay wakeup sidecar for resident LIQ rows: store-unit wakeups clear
  wait-store diagnostics by `(storeId, storeLsId, pc)`, store-unit data merges
  only into same-line `L1DcMiss`/`L2Wait` rows when `(storeId, storeLsId)` is no
  newer than the row's `(youngestStoreId, youngestStoreLsId)` allocation
  snapshot, and SCB data merges into working same-line rows except `Repick`.
  Completion is a recomputed requested-byte mask fully covered
  by the merged valid mask. Completed rows return to `Wait` for relaunch; keep
  L1 refill, ready-table updates, consumer bypass routing, ResolveQ/LHQ queue
  movement, precise flush, and trace emission in later owner packets.
- Phase 5 `LoadRefillWakeup` work must run
  `bash tools/chisel/run_chisel_tests.sh --only LoadRefillWakeup` and the
  affected `LoadInflightQueue`/`LoadReplayWakeup` gates. This module is the
  first read-refill wakeup sidecar for resident LIQ rows: accept only read
  refill packets, wake working same-line scalar rows that have not already
  recorded `l1Hit`, set a local `l1Hit` sideband, and store full-line data plus
  a full valid mask in the row. `LoadInflightQueue` launch must use row-owned
  `lineData`/`validMask` when present so refill- and replay-completed rows
  relaunch through `LoadForwardPipeline` without an external base-data replay
  input. Keep miss queue/prefetch-set ownership, full L1D/LDQ data-buffer
  ownership, L2/CHI response queues, ready-table updates, consumer bypass,
  precise flush, ResolveQ/LHQ movement, and trace emission in later packets.
- `run_chisel_reduced_rob_xcheck.sh` is the first live generated-RTL trace
  proof for the Chisel lane: it emits `ReducedCommitROB` SystemVerilog, builds a
  Verilator harness, writes Chisel commit JSONL through the shared writer
  including an invalid fixed-width slot, normalizes through
  `trace_schema_adapter.py`, and requires zero mismatches against the
  QEMU-shaped reference trace.
- `run_chisel_top_xcheck.sh` is the first top-level generated-RTL trace proof
  for the Chisel lane: it emits a dedicated 8-entry, two-wide `LinxCoreTop`
  xcheck configuration, builds the same Verilator harness against top-level IO,
  asserts clean commit monitor outputs, and requires zero mismatches against the
  QEMU-shaped reference trace. The default top still emits `CoreParams()`.
- `run_chisel_trace_replay_xcheck.sh` is the first external-row replay proof
  for the top-level Chisel cross-check path: it normalizes an input or fixture
  commit JSONL, drives those rows through `LinxCoreTop` with the Verilator
  harness, writes DUT and QEMU-shaped reference streams, and requires zero
  mismatches through the neutral comparator.
- `run_chisel_qemu_trace_replay_xcheck.sh` is the first QEMU-row replay proof
  for the Chisel cross-check path: it collects or consumes QEMU JSONL,
  normalizes a wider raw window, slices a metadata-aware prefix with the
  requested number of architectural rows, replays that prefix through
  `LinxCoreTop`, and requires a passing manifest through the same neutral
  comparator. For `--elf` replay, `--replay-rows` bounds live FIFO capture;
  high-address benchmark ELFs such as the current CoreMark build require
  trailing QEMU memory args, for example `-m 1280M`.
- `run_chisel_frontend_trace_top_lint.sh` is the first generated-RTL proof for
  the raw frontend-window to integrated decode/rename/ROB commit boundary: it
  emits `LinxCoreFrontendTraceTop`, compiles every sibling SystemVerilog module
  that CIRCT emits for that target, and lints the result with Verilator.
- `run_chisel_frontend_trace_top_xcheck.sh` is the first generated-RTL
  comparison proof for that boundary: it emits `LinxCoreFrontendTraceTop`,
  builds the dedicated frontend trace-top Verilator harness, drives scalar
  frontend packets, dumps DUT commit JSONL, normalizes through
  `trace_schema_adapter.py`, and requires zero mismatches against the
  QEMU-shaped reference trace.
- `run_chisel_frontend_fetch_trace_top_xcheck.sh` is the first generated-RTL
  comparison proof for the live frontend source boundary: it emits
  `LinxCoreFrontendFetchTraceTop`, builds the dedicated Verilator harness,
  drives PC request/response handshakes with a bounded memory-window fixture,
  dumps DUT commit JSONL through the shared writer, normalizes through
  `trace_schema_adapter.py`, and requires zero mismatches against the
  QEMU-shaped reference trace.
- `run_chisel_frontend_fetch_rf_alu_trace_top_xcheck.sh` is the generated-RTL
  comparison proof for the current highest-fidelity reduced scalar path: it
  emits `LinxCoreFrontendFetchRfAluTraceTop`, drives live fetch PC
  request/response handshakes into F4 from binary or sparse ELF fetch-memory
  bytes, reduced decode/rename/ROB, RF-backed issue, and ALU execute, dumps
  DUT commit JSONL through the shared writer, normalizes through
  `trace_schema_adapter.py`, and requires zero mismatches against the
  QEMU-shaped reference trace.
- `run_chisel_frontend_fetch_rf_alu_qemu_elf_xcheck.sh` is the reduced
  live-QEMU proof for that path: it captures a bounded commit prefix from a
  direct-boot ELF, validates the strict scalar subset or preserves legal block
  markers as skip rows, pairs it with the ELF fetch bytes, and preserves the
  common comparator manifest. Treat it as reduced live fetch RF/ALU evidence
  only until width-wide ROB allocation, LSU, trap/recovery, and real full-DUT
  commit generation are live.
- `run_chisel_frontend_alu_trace_top_xcheck.sh` is the first generated-RTL
  comparison proof where frontend-decoded scalar rows complete through a
  Chisel execute owner. It emits `LinxCoreFrontendAluTraceTop`, builds the
  dedicated ALU trace-top Verilator harness, holds fixture operand data stable
  until execute accepts the renamed uop, dumps DUT commit JSONL with nonzero
  writeback fields, normalizes through `trace_schema_adapter.py`, and requires
  zero mismatches against the QEMU-shaped reference trace.

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
- For issue-side work specifically, keep `S1/S2/S3/IQ/P0/P1/I1/I2` responsibilities inspectable in dedicated modules/files. A monolithic scheduler file is a contract smell because it hides which stage owns routing, readiness initialization, wakeup fanout, and deallocation.
- Within that issue-side split, keep `P1/I1/I2` pick arbitration, RF-read accounting, issue-confirm gating, and issue-side wait-cause logic in an issue-owner module/file rather than leaving them split across top-level scheduler glue and queue-owner code. Queue ownership should stop at IQ residency/wakeup; issue ownership should cover pick/read/confirm behavior.
- I2 deallocates only a non-speculative, non-cancellable transfer. A uop with
  live load-dependence state remains valid+inflight in IQ until every producer
  load resolves hit at E5; miss/replay cancels the pipe copy, clears inflight,
  and leaves the resident row for repick.
- Preserve the ARM-style stage names in architecture-facing work: `S1` captures
  dispatch payload, `S2` allocates/writes IQ state, and `S3` is the resident,
  valid, pickable IQ boundary. `P0` is optional preselection and `P1` is final
  pick. Do not skip `S3` merely because the current implementation folds it
  into IQ residency.
- Treat `E*` and `W*` as overlaid coordinates, not one serial chain. `E1/E2/E3`
  name absolute cycles after I2; `W1/W2/W3` name actual
  data-bypass/result/writeback age for the selected operation latency, with W1
  as the first real data age. Earlier speculative wakeup stays separately
  E-qualified. `W*` must never be reused for ROB retirement, trace preparation,
  or commit.
- When adding new owner tables or wake structures such as qtag wait crossbars or IQ owner tables, place them in the queue-owner module/file instead of generic top-level helpers.
- For LSU-side work, keep `LIQ/LHQ/MDB/STQ/SCB/L1D` transitions in an LSU-owner module/file and keep redirect pruning plus LSID rebasing in a recovery-owner module/file. Do not mix memory-owner progression and recovery-domain pruning into generic scheduler glue.
- For frontend-side work, keep instruction-to-uop build/decode in a decode-owner module/file, `F0/F1..F4/IB/D1..D3/S1..S3` movement and routing in a frontend-owner module/file, and stage-event generation in a trace-owner module/file. F0 is canonical thread/PC control. F1-F4 are the four fetch stages; F4 owns final lightweight predecode/prediction and aliases IB, never four decode slots. Internal serial `IB -> F4` and `F4DecodeWindow` names are migration aliases. Do not mix uop construction, stage transport, and trace emission back into one scheduler file; that obscures which part of the model owns fetch barriers, ROB admission, and visible stage residency.
- Template parents are marked at F4 but must pass D1/D2 before D3 atomically
  reserves one `(STID,BID)`, child ROB rows, and a final template trace/commit
  row. CTU fills child rows in order; children reuse the parent BID and retire
  before the final row. Flush removes filled/unfilled reservations by STID and
  checkpoint. Do not use a ROB-head direct-write CTU path as canonical evidence.
- Preserve the ARM-style retirement coordinates: R0 captures resolve, R1 forms the precise decision, R2 publishes CMT and FLS coherently, R3 performs registered recovery processing, and R4 publishes restart state to F0. Do not move CMT to R3 or conflate the R2 flush broadcast with the R4 restart.
- Model architectural redirect restart as the registered `R2 FLS -> R3 recovery -> R4 restart -> F0` sequence, not as an implicit side effect of generic fetch iteration. F0 must honor the R4 restart boundary; do not let fetch resume in the same abstract step that resolved the redirect just because the software loop can see the corrected target immediately.
- Keep redirect restart-source selection in the recovery owner too. The R1/R2 path resolves the legal restart source from redirect metadata and block-boundary legality (`BSTART`, `FENTRY`, `FEXIT`, `FRET.*`); R4 then hands F0 a concrete restart token `(target_pc, restart_seq, resume_cycle)`. Do not let generic fetch code infer restart by “next surviving seq” once wrong-path/frontend occupancy exists.
- Keep architectural redirect ownership boundary-only. In the CA reference model, a non-fallthrough BRU commit is not itself an `FLS` redirect owner; treat it as pre-boundary correction metadata and let the later architectural boundary (`BSTART`/`BSTOP`/macro boundary) own the visible redirect and frontend restart.
- Model deferred BRU correction as explicit recovery-owner state, and let the later architectural boundary consume it before any boundary-local redirect target. A BRU mismatch should publish pending correction metadata when it becomes architecturally visible, but `FLS` should only resolve at the boundary, using pending BRU correction first and clearing that state once the boundary-owned redirect/restart token is issued.
- Match deferred BRU correction by block/branch epoch, not plain age. In the CA reference model, a later boundary may consume deferred BRU correction only when the correction epoch matches that boundary's block epoch; a stale correction from an older dynamic block instance must not leak across a head-`BSTART` epoch advance into the next loop iteration.
- Model recovery-target safety as a BRU-side precise trap, not a boundary fallback. If deferred BRU correction resolves to a target that lacks legal block-start metadata (`BSTART*` or a valid template start), report architectural `E_BLOCK(EC_CFI)` with `CFI_BAD_TARGET`, source PC/TPC in `TRAPARG0`, and `ECSTATE.BI=0`. `TRAP_BRU_RECOVERY_NOT_BSTART (0xB001)` is legacy internal diagnostics only and must be mapped before trap export; do not silently convert the fault into a boundary-local redirect or guessed restart sequence.
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
- LinxTrace v1 is a single-STID compatibility schema and retains its legacy
  64-bit `block_bid` container. Do not reinterpret high bits as canonical
  uniqueness. Multi-STID promotion requires a v2 major with separate
  `{stid, BID_W-bit block_bid, block_uid}` across producer, linter, viewer,
  fixtures, and comparator.
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

These are the canonical LinxCore contract and must be preserved by future changes:

1) **BID is generated by BROB**
- Each STID owns an independent BROB ring; scalar frontend `thread_id` aliases
  STID, while PE/engine-local TID remains a subordinate qualifier.
- BID is the entry identity within that STID's BROB.
- Default sizing: `N_STID=1`; **BROB entries per STID = 256** (power of two,
  at least 2). Multi-STID is a supported target configuration and requires
  STID-bearing shared interfaces. `STID_W=max(1,ceil(log2(N_STID)))`.

2) **BID encoding**
- `BID_W = ceil(log2(BROB_ENTRIES))`.
- BID is the complete per-STID BROB slot identity. For each default 256-entry
  ring, BID is 8 bits. Shared block identity is `(STID,BID)`; STID is never
  packed above BID.
- A conventional internal BROB pointer may use `{wrap, bid}` and therefore
  `BID_W + 1` bits, but wrap/generation/age is not part of BID.
- A globally unique `block_uid` may exist for DFX only; it must not widen BID
  or participate in architectural routing.

3) **Tag routing**
- **`(cmd_stid, cmd_tag) = (STID, BID)`** when the engine tag width covers
  `BID_W`; responses echo both fields.
- Rationale: PE response tags must route to the correct BROB entry; avoid any unrelated tag sources (e.g. cycles).
- If a long-latency engine needs protection across slot reuse, carry a
  separate echoed transaction epoch/tag. Do not pack that epoch into BID.
- The default permits one outstanding top-level command per `(STID,BID)` and
  one aggregated non-scalar-done response. Multiple same-block commands require
  a separate transaction ID plus expected-response accounting.
- Command valid is independent of ready and payload holds until fire. Response
  lanes likewise hold until fire; a collector must accept or independently
  backpressure simultaneous responses without priority-mux loss. Preserve the
  full trapno/TRAPARG0/BI envelope.

4) **Block completion**
- `complete = scalar_done && (needs_engine ? engine_done : 1)`
- `needs_engine` should be set when the block actually issues engine commands.
- Scalar boundary completion is separate from non-scalar engine completion;
  one event must not set both bits.

5) **BSTART / BSTOP semantics**
- `BSTART` uop in ROB carries the **new `(STID,BID)`** (it belongs to the new block).
- `scalar_done` is triggered at **BSTART retire + BSTOP retire**.
  - On BSTART retire: mark scalar_done for the *old active `(STID,BID)`* (implicit end).
  - On BSTOP retire: mark scalar_done for the current `(STID,BID)` (explicit end).

6) **Flush semantics (BID-based)**
- On a flush/redirect, the system reports the **current `(flush_stid,
  flush_bid)`**. Only that STID's younger blocks are cleared.
- Because slot ids wrap, unsigned BID comparison is invalid.
- The selected STID's BROB computes the younger set from its
  head/tail/occupancy/wrap state and publishes STID plus `brob_kill_mask`, or
  exactly equivalent ring-qualified context.
- A migration-era wider cleanup transport must first resolve its canonical
  `BID_W` slot against that exact selected-STID live window. The unique internal
  `{wrap,bid}` pointer is the pivot. Wider upper bits are diagnostic only.
  Cleanup interfaces must keep these identities physically separate: every
  field named or specified as BID is exactly `BID_W`, while any internal
  `{wrap,bid}` pointer travels in a distinct field under an explicit valid
  qualifier. Do not widen a BID field to carry generation, and do not compare a
  canonical BID slot as an unsigned age.
  Distribute the resolved pivot or kill mask to every BROB, rename, ROB, LSU,
  and queued-cleanup consumer; never let one owner use the resolved pointer
  while another uses the raw transport. A missing or ambiguous live match must
  suppress all cleanup mutations together.
- Rule: keep the flush-owning entry and older entries; kill the ring interval
  from successor(`flush_bid`) to the pre-flush tail.
- This applies to **all modules that carry/queue `(STID,BID)`** (at minimum:
  BROB, BISQ, engine queues, memory rows, and cleanup paths).
- A `(STID,BID)` slot may not be reused until all row, command, response, and cleanup
  ownership for its previous occupant has drained, unless a separate echoed
  transaction identity rejects stale responses.

7) **Recovery producer ownership**
- Give each independent BCC, IEX, PE, and LSU recovery family its own finite
  retained lane. A lane accepts only a complete typed event, holds identity and
  payload stable until central acceptance, and exposes backpressure to its
  trigger owner.
- Treat source indices as provenance contracts. Append new producer banks after
  existing external lanes, and keep the canonical scalar-LSU lane final unless
  every cause-mask, payload-owner, sidecar, probe, and consumer is migrated in
  one reviewed change.
- Select STID/scope once in a shared retained-source boundary before age or
  resident-owner lookup. An invalid STID must issue no lookup, publish no
  source, and release no retained report. Canonical and reduced compositions
  may own different queues, but must instantiate the same scope-selection and
  exact-promotion policy rather than duplicating it in top-level wiring.
- When allocation requires a speculative side lookup such as MDB prediction,
  join side-queue credit into allocation readiness and issue the lookup from
  the exact accepted allocation payload. The resident row and lookup must
  accept atomically; never allocate first and reconstruct or pulse the lookup
  later. Assert acceptance equality at the integration boundary.
- For store-side conflict probes, expose a stable pre-permit insertion intent
  so MDB sink readiness can gate address-bearing STQ acceptance without a
  ready/payload combinational cycle. If reduced timing requires later ResolveQ
  replay, retain every committed probe in a finite FIFO and include FIFO credit
  in admission; never overwrite an accepted probe with the latest store.
  Data-only fragments may bypass this address-side gate.
- When several producers mutate one resident queue, arbitrate complete native
  mutation requests and preserve each producer's qualification policy. MDB
  lookup/timeout requests may target pre-launch `Wait` rows without unrelated
  SCB-return proof, while source-return mutations keep their stricter row-state
  and ordering checks. A retained producer must not dequeue until the selected
  native write accepts. Feed owner-generated wakeups back into the resident
  queue; if wake sources collide, define priority and retain the displaced
  source rather than leaving a wakeup as diagnostics only.
- Derive IEX IQ-watchdog replay identity from the selected STID's authoritative
  full BROB commit pointer and valid/incomplete oldest state. Increment the full
  pointer with rollover; never increment a canonical BID slot and invent wrap.
- Tied-off reduced shells prove integration shape only. Do not claim live BCC,
  IEX, or PE recovery until the actual trigger owner drives the raw event port
  and generated RTL proves positive activation.

## PR checklist for BID/block changes

- [ ] Confirm `BID_W == ceil(log2(BROB_ENTRIES))` per STID through backend, BCTRL, PE, response, trace, and test interfaces.
- [ ] Confirm `(cmd_stid,cmd_tag) == (stid,bid)` through backend->bctrl->PE and response routing, or document a physically STID-dedicated lane plus the separate echoed transaction tag.
- [ ] Confirm flush path provides `(flush_stid,flush_bid)` plus that ring's qualified kill context and every `(STID,BID)`-carrying module applies the same younger set.
- [ ] Confirm canonical BID resolution is performed once per accepted cleanup,
  all state owners consume the same resolved pivot/kill set, and zero-match
  recovery mutates no owner.
- [ ] Confirm cleanup BID fields are exactly `BID_W`; any wrap-qualified
  implementation pointer is a separate valid-qualified field and cannot replace
  architectural `(STID,BID)` identity.
- [ ] Confirm wrap-boundary tests prove that unsigned BID magnitude is never used as age.
- [ ] Confirm two STIDs can use the same BID without alias and one-ring flush does not touch the other.
- [ ] Confirm stale/duplicate responses cannot match or over-complete a reused `(STID,BID)` slot.
- [ ] Confirm recovery source indices and provenance widths include every
  retained lane without renumbering existing payload owners.
- [ ] Confirm IQ-watchdog recovery uses the owner-selected full BROB commit
  pointer successor and suppresses absent, completed, or out-of-range STID state.
- [ ] Update docs/skills when new edge cases are discovered.

## Scalar GPR rename checkpoint cleanup (strict)

Confirmed from `tools/model/model/bctrl/spe/GPRRename.cpp` and
`SPERename.cpp`. Use this section when implementing or reviewing Chisel scalar
GPR rename cleanup.

- The model scalar GPR owner has **24 architectural GPRs**. Wider architectural
  tag surfaces in dispatch/decode must be classified by the decode alias owner
  that handles invalid/T/U/SGPR aliases; do not silently treat those aliases as
  scalar GPRs.
- `ScalarDecodeRenameBridge` is the first Chisel consumer that enforces this
  boundary. It accepts only scalar GPR tags `0..23` for `OperandClass.P` /
  `DestinationKind.Gpr`, rejects any source class other than `P` and any
  destination kind other than `Gpr` until their owners exist, and reports the
  rejection instead of allocating a scalar physical tag.
- Reset state is identity for `smap` and `cmap`, with physical tags above the
  identity GPR range marked free.
- Checkpoint capture copies the current speculative map into the live
  `(STID,BID)` slot and records the matching BROB generation/ring context. In
  the model call path, `SPERename` captures this checkpoint for
  `inst->isLastInBlock`.
- Commit walks the map queue for matching BID in queue order, releases the old
  committed physical tag for each architectural destination, updates `cmap`,
  and clears committed rows. Same-architecture multiple writes in one block must
  release the overwritten intermediate physical tag as well as the pre-block
  committed tag.
- Flush restores from the selected STID's BROB-qualified predecessor
  checkpoint, or from `cmap` if that checkpoint is invalid. The legacy model
  computes this as predecessor of its full `{wrap,val}` ROBID; target hardware
  must not implement it as unsigned narrow `flush.bid - 1` without ring/
  generation context.
- For block-stop redirects that preserve the just-finished block, scalar GPR
  cleanup uses the BROB successor/predecessor context that selects the
  just-finished block's committed checkpoint, not a raw numeric BID
  subtraction. Selecting the checkpoint before the block can lose adjacent
  `C.SETRET` / source maps after mapQ commit.
- Default skip-marker marker-only redirects are frontend restarts, not
  backend/rename cleanup events. When `skipBlockMarkers=true`, a marker stop
  redirect has no valid marker retire source; do not synthesize scalar GPR
  cleanup from `robMarkerRetireSource` or equivalent invalid metadata. Execute
  redirects still own backend cleanup, and admitted marker-row mode may use
  marker-retire metadata after the marker row has actually entered and retired
  through the backend. The R243 reduced-store CoreMark failure proved this by
  losing the x10 physical mapping before an `FENTRY` save store.
- Until exact `isLastInBlock` checkpoint capture is owned in Chisel, the
  reduced in-order marker-row path refreshes the scalar GPR checkpoint after
  each accepted row with the post-rename map. Do not remove that approximation
  without rerunning the 1024-row admitted-marker CoreMark QEMU/DUT gate.
- Flush pruning uses `baseOnBid` to remove rows at or younger than `flush.bid`;
  otherwise it removes rows at or younger than the `(flush.bid, flush.rid)`
  pair. Surviving rows must be re-applied to `smap` in BID/RID order after the
  checkpoint/cmap restore, including older surviving rows from wrapped BIDs
  when no valid checkpoint exists. Do not rebuild only from `cmap` or only from
  same-BID survivors; that loses speculative mappings that are still older than
  the cleanup point.
- `renameReplayValid` is not a scalar GPR map mutation in the first Chisel
  owner. Keep it observable for integration, and leave SGPR, ClockHands, T/U
  operands, multithread map banks, and full dispatch/commit wiring to explicit
  later packets.
- Focused gates for changes touching this owner:
  `bash tools/chisel/run_chisel_tests.sh --only GPRRenameCheckpoint`,
  `bash tools/chisel/run_chisel_tests.sh --only ScalarDecodeRenameBridge`,
  `bash tools/chisel/run_chisel_tests.sh --only RecoveryCleanupControl`,
  `bash tools/chisel/run_chisel_tests.sh --only FullBidRecoveryBridge`,
  `bash tools/chisel/run_chisel_tests.sh --only ROBID`, and
  `bash tools/chisel/run_chisel_rob_bookkeeping.sh --reduced-rob`.

## Frontend opcode and operand decode (strict)

Confirmed from `rtl/LinxCore/src/common/opcode_meta_gen.py`,
`decode16.py`, `decode32.py`, `decode48.py`, `decode64.py`,
`model/LinxCoreModel/model/bctrl/spe/Decoder.cpp`,
`model/LinxCoreModel/isa/ISACommon/GPR.h`,
`model/LinxCoreModel/isa/ISACommon/DecodeUtiles.h`,
`model/LinxCoreModel/isa/MInst.cpp`, and
`model/LinxCoreModel/isa/codec/decodefiles/block16.decode`.

- Chisel opcode classification must be generated from the pyCircuit opcode
  metadata catalog, not from ad-hoc low-bit slices of the raw instruction.
- The rule selection contract is **most-specific mask wins**: among matching
  rules for the current instruction length, choose the rule with the largest
  `mask.bit_count()`. Equal specificity keeps source/catalog order.
- Use the F4/IB entry length carried into D1 to select the 16/32/48/64-bit rule
  domain; do not let a wider table match a shorter D1 slot.
- `FrontendDecodeStage` owns opcode catalog ID, basic dispatch target,
  block-boundary/stop, load, and store sideband masks.
- The generated Chisel table must carry the pyCircuit operand-shape metadata
  (`rdKind`, `rs1Kind`, `rs2Kind`, `immKind`) alongside opcode/category
  metadata; future decode packets should extend that source table rather than
  duplicating ad-hoc opcode lists.
- `FrontendOperandDecode` owns only scalar architectural field extraction and
  reg6 alias classification:
  generic 16/32/48 GPR fields, fixed-destination compressed scalar forms,
  indexed-store `srcp`, macro source fields, and common scalar immediates
  (`UIMM12`, `SIMM12_*`, `SIMM17`, `SIMM25`, compressed 5/12-bit immediates,
  `FENTRY_UIMM_HI`, `IMM20`, and `HL.LUI` `IMM32`). `FrontendRegAliasClassify`
  emits source tags `0..23` as `OperandClass.P`, `24..27` as `OperandClass.T`,
  `28..31` as `OperandClass.U`; destination tags `0..23` as
  `DestinationKind.Gpr`, tag `31` as `DestinationKind.T`, and tag `30` as
  `DestinationKind.U`.
- `FrontendOperandDecode` does not own LSID allocation, D2 queueing, block
  header mutation, store split rewrite, physical rename, ROB admission,
  T/U queue consumption, SGPR/tile/vector operand classes,
  shift/source-type sidebands (`srcr_type`, `shamt`), or full PCR/HL payload
  interpretation.
- Regenerate the Chisel table with
  `python3 tools/chisel/gen_frontend_decode_table.py` after pyCircuit opcode
  metadata changes, then run `bash tools/chisel/run_chisel_tests.sh --only
  FrontendDecodeStage`.
- Focused gates for changes touching this owner:
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage`,
  `bash tools/chisel/run_chisel_tests.sh --only F4DecodeWindow`,
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeIngress`, and
  `bash tools/chisel/run_chisel_tests.sh --only InterfaceBundles`. If reg6
  alias classification changed, also run `ScalarDecodeRenameBridge`,
  `DecodeRenameROBPath`, top xcheck, QEMU dry-run cross-check, `build_chisel.sh`,
  and Verilator lint.

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
- Scalar decode stamps the current LSID snapshot on every valid row before
  only load/store/DCZVA rows increment the LSID counter. ResolveQ retire
  watermarks must therefore come from a ROB commit memory-order sidecar that
  preserves this all-row pre-increment LSID, not only from committed memory
  rows. After a commit batch, publish the most advanced cumulative
  `(STID,BID,LSID)` frontier per affected STID (first uncommitted position or
  equivalent tail frontier); ResolveQ removes only rows strictly older by that
  STID's BROB-ring age plus LSID. One frontier may coalesce multiple commits,
  but frontiers never compare across STIDs. Keep the sidecar out of
  `CommitTraceRow` unless the architectural trace schema intentionally grows.
- ResolveQ precise flush producers are also MemReq-shaped: for scalar
  redirects, drive queue pruning from the redirecting row's all-row LSID
  snapshot converted to the reduced `ROBID` shape, not from ROB RID and not from
  a disabled LSID. Marker-only cleanup without a real LSID should stay on the
  conservative hard-clear path until a recovery owner provides a valid LSID.
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
- Store-unit replay wakeup has two separate LIQ effects:
  - clear wait-store when the blocked row's stored store identity and PC match.
  - merge data into `L1DcMiss`/`L2Wait` rows only when same-line and
    `SID <= youngest_sid_at_alloc`.
- SCB replay wakeup merges same-line byte-valid data into working LIQ rows
  except `Repick`; when merged bytes cover the requested load mask, return the
  row to `Wait` for the next launch rather than directly publishing an LHQ hit.
- L1 refill wakeup is a separate owner from store/SCB replay wakeup:
  - accept only read refill packets.
  - match working same-line scalar LIQ rows that have not already recorded
    `l1Hit`.
  - return the row to `Wait`, set local `l1Hit`, and store full-line data plus
    full valid mask for the next launch.
  - keep miss queue, prefetch set, full L1D/LDQ data buffer, ready-table,
    bypass, precise flush, ResolveQ/LHQ, and trace ownership separate.
- LIQ launch should use row-owned `lineData`/`validMask` when present before
  falling back to external base data; this is what lets replay/refill-completed
  rows relaunch through the normal load-forward pipeline.

## SCB (Store Coalescing Buffer) → DCache / CHI (strict)

Confirmed in #linx-core (2026-02-25).

- STQ may contain flushable (speculative) stores.
- SCB must only contain stores guaranteed **not** to be flushed.
  - This is controlled by a **non-flush pointer** (strong: excludes branch flush + exceptions/interrupts/traps).
- Scalar STQ `Wait -> Commit` has two model-derived non-flush proofs. Preserve
  both when adapting the LSU:
  - completed, exception-free blocks inside the exact per-STID strong
    non-flush head/count prefix;
  - a ready resident scalar row in the exact oldest ROB `(STID, BID)` block
    whose wrap-qualified LSID is strictly older than the ROB/PE oldest-LSID
    snapshot.
- The oldest-LSID proof scans resident STQ rows directly. It must not depend on
  first observing a matching ROB store-commit identity because ROB retirement
  and delayed STA/STD merge can cross. If a later commit-LSID proof is retained,
  latch it through row absence and clear it on accepted recovery.
- Do not repair a full, all-ready STQ by merely aliasing STQ depth to ROB depth
  or enlarging the queue. First inspect resident scalar early-safe eligibility,
  exact BID/STID matching, LSID wrap, and recovery stall. Tile/template rows
  cannot reuse the scalar predicate; they need explicit issued/non-flush proof.
- Treat `ScalarLsuParams` as the live Chisel physical-sizing owner. STQ rows,
  commit FIFO, commit issue lanes, SCB rows, forwarding snapshots, wait-store
  indices, and MDB store vectors use their respective configured capacities;
  BID/GID/RID remain ROB-sized. A compatibility default that makes sizes equal
  is not proof: run the unequal-capacity module and reduced-top gates.
- LSID is a full-width per-STID memory-order identity, not an STQ or ROB index.
  A transitional `ROBID`-shaped LSID projection may not become the golden
  interface or decide ordering without the full `lsidWidth` value beside it.
- Use `CoreParams.lsidWidth`/`InterfaceParams.lsidWidth` as the Chisel owner.
  Same-block age uses `LSIDOrder` modulo serial arithmetic; plain unsigned
  comparison is forbidden, and exactly half-range separation is ambiguous.
  The finite live memory window must remain below half of the LSID domain.
- R670 carries full LSID through store dispatch, split merge, STQ residency,
  scalar early-safe commit, commit FIFO, split drain, SCB admission, and the
  committed-memory overlay. Its ROBID projection is temporary and now exists
  only for physical compatibility and legacy diagnostics. Do not remove the
  full field or use the projection for ordering logic; remove remaining
  projection consumers before deleting the projection itself.
- Memory identity is STID-scoped. Split STA/STD merge identity must include
  `(STID, BID, full LSID)`; equal BID/LSID values from different STIDs never
  merge or compare. Every cache-line fragment and reduced-top commit bypass
  must retain the originating BID and full LSID metadata.
- R671 carries `lsIdFullValid/lsIdFull` through `FullBidFlushReq`, producer
  retention, recovery arbitration/class merge, full-BID/ring bridges, and
  `RecoveryCleanupIntent.flush`. Scalar redirect sources must capture the
  execute row's full all-row LSID before publication; do not reconstruct it
  from RID, BID, or the legacy LSID projection.
- Typed STQ recovery uses full LSID only after STID/PE/thread and flush-mode
  scope checks. BID-only suffix recovery needs no LSID. Non-BID store pruning
  must conservatively refuse missing full-LSID authority and exactly
  half-range ambiguity; it may not fall back to `FlushReq.lsId`.
- Before R672-A, LIQ/ResolveQ/MDB recovery sources left `lsIdFullValid` clear.
  Keep required/missing/ambiguous STQ diagnostics for any still-unconverted
  source; never hide missing authority by re-enabling projected STQ pruning or
  passing a zero placeholder to the authoritative matcher.
- R672-A promotes the canonical scalar-load owner: load allocation, LIQ/LHQ,
  ResolveQ, MDB conflict/fanout/SSIT/wait/delete/recovery, and return queue/W1/W2
  payloads carry explicit full-LSID validity/value. Same-BID cleanup,
  group cleanup, retirement, conflict selection, and SSIT distance use
  `LSIDOrder`; cross-BID age remains ROB/BROB-ring-owned. MDB may identify a
  wait target before its local store index resolves, but it must not mutate LIQ
  until the predicted store's full LSID is valid. Do not widen BID/GID/RID or
  reconstruct missing full authority.
- R672-B promotes the reduced replay snapshot request/token/response graph and
  reduced forwarding order.
  Ordinary live capture and wait-store relaunch must first carry the load's
  authority through `ReducedLoadReplayCandidate`, relaunch FIFO, and LIQ
  allocation. Request FIFO rows, the accepted-query token, response FIFO rows,
  response apply, and row-mutation wait metadata retain parameterized full-LSID
  validity/value. Selective request/token/response pruning must use
  `STQFlushPrune.matchesFlush`; same-BID missing authority retains state. The
  projection-only matcher is deleted and must not be reintroduced.
- Forwarding uses BID/BROB order across blocks. Within one BID, candidate
  eligibility, nearest-store selection per byte, and final wait-store choice
  require valid parameterized full LSIDs and use `LSIDOrder`. Missing authority
  and exactly half-range ambiguity fail closed and must remain observable; do
  not fall back to the projection. The selected not-ready store retains full
  authority through E3/E4 and any reduced resident wait-slot/replay-wakeup
  bridge into canonical LIQ wait, timeout-delete, and recovery state. Replay
  matching requires exact full LSID whenever the stored wait key marks it
  valid.
- Cluster/entry IDs and ROBID-shaped LSID fields in the snapshot graph are
  physical routing or compatibility sidecars. They must not authorize Linx
  memory-order recovery or substitute for full-LSID authority.
- R673 makes cacheable scalar load misses retained canonical state.
  `loadMissQueueEntries` is independent of LIQ, ROB, STQ, LRET, and LSID width.
  Reserve worst-case miss capacity at accepted launch and release it at every
  E4 outcome; an E4 data miss must transfer atomically into `LoadMissQueue` and
  may never rely on a one-cycle lower-memory pulse.
- Coalesce one miss entry per aligned cache line, but identify the lower-memory
  transaction by miss slot plus generation and line address. Preserve
  first-miss FIFO issue order and hold every request field stable under
  backpressure. Line address alone is not response authority after flush or
  reuse.
- Every coalesced dependent retains LIQ slot/generation plus
  PE/STID/TID/BID/GID/RID/full-LSID authority. Typed recovery prunes dependents
  with `LoadQueueFlushMatch`. Cancel an unissued entry only after its last
  dependent is removed; retain an issued empty entry as an orphan until its
  exact response drains. A stale generation or wrong-line response must not
  wake LIQ or free a current entry.
- Only a valid read response with exact slot, generation, and line authority
  may retire a miss entry. Invalid-ID, non-read, stale, duplicate, and
  wrong-line responses are diagnostics and cannot mutate live state. Qualify
  the E4-to-miss transfer and its drop assertion with non-flush residency so a
  coincident accepted recovery is not misreported as data loss.
- The miss queue is for upstream-classified cacheable scalar normal memory.
  Device/MMIO, tile, cache-maintenance, and other side-effecting classes need
  dedicated non-coalescing owners. Do not import ARM barrier, exclusive,
  acquire/release, or exception-level behavior into this mechanism.
- R674 makes refill publication a bounded retained transport rather than a
  combinational priority mux. `loadRefillQueueEntries` is independent of LIQ,
  miss, ROB, STQ, return, and LSID sizing. Exact miss and external refill
  sources have independent ready/valid ingress and may both fire; preserve
  miss-then-external same-cycle FIFO order and one-packet-per-cycle LIQ egress.
- Compute ingress readiness from post-dequeue capacity so a full transport can
  replace its consumed head without a bubble. If only one slot opens, miss
  ingress wins and external ingress remains backpressured. Hold head payload
  and provenance stable until output fire.
- A valid exact read response may free a miss entry only in the same event that
  its refill packet enters retained transport. Malformed responses need no
  refill credit. Hard flush clears buffered refills; typed precise recovery
  freezes transport for that cycle and preserves physical line data for
  surviving Linx loads. Legal dual ingress is not a protocol error.
- For a scalar load that crosses one cache line, retain one architectural Linx
  identity and make every phase consumer use the active aligned line and
  phase-local byte mask: forwarding, store/SCB wakeup, miss coalescing, refill
  matching, and lower-memory request generation. Do not implement only final
  data assembly while those owners still observe the first line.
- A completed first phase is private LIQ state. It may not publish ResolveQ,
  LRET, writeback, or wakeup. Publish exactly one result only after all line
  phases are complete, using the original address, size, destination, and
  full-LSID identity. Sequential versus parallel phase launch is a performance
  policy, not an architectural difference.
- Hard Linx recovery clears every phase. Typed precise recovery prunes by the
  existing full row identity; a nonmatching survivor may retain a phase that
  completed before recovery, but it must not adopt a phase transition produced
  by a coincident canceled E4 cycle. Add generated-RTL proof for that exact
  first-phase recovery collision.
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
- RTL egress selection must consider only model-valid SCB rows, prefer full
  cachelines, and replace the model's random not-full eviction with a
  deterministic choice before issuing a lookup descriptor.
- DCache lookup control must preserve the model split between writable hit and
  tag hit: writable hit updates/free locally; tag hit without write permission
  sends an upgrade request; tag miss sends a write request; miss rows remain
  resident until a later WriteResp/UpgradeResp returns them to lookup.
- SCB row-state update must preserve the model lookup/response lifecycle:
  selected `S_VALID` rows can move to `S_LOOKUP`, same-cycle writable hits
  clear rows, same-cycle or registered non-writable lookups move rows to
  `S_MISS`, and WriteResp/UpgradeResp decode may return only valid `S_MISS`
  rows to `S_LOOKUP`; report illegal response targets rather than silently
  freeing or reusing the row.
- Raw SCB response decode must preserve the model tag namespace: a legal
  WriteResp/UpgradeResp transaction id is `(entryIndex << 2) | 2`, the decoded
  index must name an implemented SCB row, and the target row must be valid
  `S_MISS` before `SCBStateUpdate` may return it to `S_LOOKUP`. Wrong type,
  wrong low-bit tag, out-of-range index, and stale non-`S_MISS` targets are
  errors, not implicit drops or frees.
- Raw SCB response buffering must preserve the model response-queue boundary:
  keep FIFO order and backpressure in front of `SCBResponseDecode`, present
  only the FIFO head to decode, and retain illegal or stale heads so decode
  continues to report the failing target instead of silently dropping it.
- SCB response retry ordering must preserve the model `resp_list` FIFO:
  accepted WriteResp/UpgradeResp row ids enqueue in response-return order, raw
  response consumption, `S_MISS`-to-`S_LOOKUP` state update, and retry enqueue
  share the accepted-response handshake, and only the queued head may retry
  before ordinary valid-row eviction. Retry rows are legal state-update finish
  targets only when paired with hit/free or miss masks; accepted-only lookup
  starts still require `S_VALID`. A stale or non-`S_LOOKUP` queued head is an
  error and must block ordinary egress instead of silently falling through.
- Registered SCB row-bank composition must use pre-cycle free count for the
  model batch admission gate. Same-cycle writable-hit frees do not admit new
  committed-store fragments in that cycle, but accepted ingress may be visible
  in the same-cycle lookup payload. `S_LOOKUP` and `S_MISS` rows are never
  merge targets; same-line stores must allocate a separate row when free space
  exists.
- Full STQ-to-SCB composition must drive `STQEntryBank.commitFreeMask` only
  from accepted `SCBRowBank` descriptors with `last=1`. The standalone
  `STQCommitDrain.commitFreeMask` is issue/debug observability in that path,
  not a bank mutation source. Drain issue must stay closed when the registered
  SCB model-batch gate is closed or when `STQEntryBank` is applying a
  flush-prune cycle.
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

- Store-arrival scalar conflict detection uses address overlap and
  `LessEqual(store.bid, store.lsID, load.bid, load.lsID)`; tile load/store
  conflicts are currently suppressed until a tile-specific owner exists.
- Among resolved active LDQ rows plus `ResolveQ`, select the oldest conflicting
  load by `(bid, lsID)` for MDB recording and recovery classification.
- Unresolved active LDQ rows are marked wait-store only for `ST_ADDR` probes.
- Cross-BID address conflict triggers a **nuke** attributed to the load;
  same-BID address conflict is an inner flush, not a nuke.
- LSU reports the load RID; ROB sets `entry.nuke=1` on that ROB entry.
- Nuke triggers only when the nuke-marked load becomes ROB head:
  - do not retire that entry;
  - redirect PC = that load's PC.
- `nuke_pending` freezes IFU (stop fetching new younger uops), but commit_redirect (older BRU flush) still applies.
  - BRU flush may clear younger ROB entries (and their nuke marks).
- Implementation: ROB maintains an `oldest_nuke` record (not full-table OR scan) and validates nuke reports only for still-valid RIDs.
- For block domain: on nuke flush, compute
  `flush_bid = rob_head.block_bid` and ask BROB for the ring-qualified younger
  kill set. Never approximate that set with `bid > flush_bid`.

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

## Scalar LSU-to-IEX load-return queues (strict)

- Model final scalar load return as a retained queue boundary, not a
  combinational LSU-to-ROB/RF/wakeup pulse. Preserve PE/STID/TID plus
  BID/GID/RID/load-LSID through queue admission and registered E4/W1/W2
  residency.
- Keep one independently sized queue per `(STID, return pipe)`. Queue depth,
  STID count, return-pipe count, and ROB identity capacity are separate
  parameters; never infer an identity width from queue capacity.
- Split admission into STID-local pre-credit and exact selected-pipe
  acceptance when pipe choice depends on consumer capacity. Feeding final
  target readiness into pipe selection creates a combinational cycle. A
  published return must still be accepted atomically by exactly one final
  lane.
- Canonicalize stored pipe identity from the accepted queue target. Do not
  trust a duplicate payload pipe field that can disagree with lane selection.
- If E3/E4 is registered after launch, reserve the exact selected lane at
  launch. Enforce `resident + reserved <= lane depth`, permit same-cycle drain
  credit only for that lane, and release one reservation on every terminal E4
  result whether it hits, misses, replays, or is otherwise blocked.
- Treat E4 hit insertion into ResolveQ and LRET as one atomic publication.
  Neither sink may observe the return alone, and the LIQ row may clear only
  after both sinks accept the same payload.
- Recovery must suppress flush-coincident E4 publication and release or prune
  pipeline reservations in the same action that kills or rewinds the LIQ row.
  Include both resident queue entries and reservations in LSU quiescence.
- When a row gains lane identity or another parameterized field, thread the
  full row shape through every mutation, preview, bridge, and helper bundle.
  Default helper widths are not evidence that a non-default configuration is
  preserved.
- Do not bypass an empty return queue directly into IEX. Permit same-cycle
  dequeue/enqueue at a full lane, but keep enqueue and later drain as distinct
  registered phases.
- Use fair shared-port drain across nonempty STID/pipe lanes and retain a head
  under IEX E4 backpressure.
- Apply accepted typed Linx recovery by compacting only matching queue entries;
  preserve older and independent entries in FIFO order. Reserve global hard
  clear for reset/start/restart or genuinely unscoped fatal recovery.
- W2 is the atomic side-effect point: required ROB resolve, RF writeback, and
  wakeup readiness must all be satisfied before its resident slot clears.
- Once LRET drains into registered IEX stages, carry the complete scoped entry
  through every W1/W2 lane. Validate the exact ROB row before dequeue: hold a
  missing row, and consume a present `NeedFlush` row without side effects.
- Size canonical W1/W2 residency by return-pipe count. Permit same-cycle W2
  completion, W1 advance, and new W1 insertion only when each source and
  destination slot has one unambiguous owner; use fair shared ingress when one
  queue drain can target several W1 lanes.
- When multiple W2 lanes share physical sinks, arbitrate them fairly and
  advance fairness only on the atomic resolve/RF/wakeup completion fire. A
  blocked selected lane must retain its payload and arbitration ownership.
- Preserve the complete slot-plus-wrap RID through W2 and revalidate it at the
  ROB completion side-effect point. Admission-time lookup is not completion
  authority; never reduce canonical completion identity to a slot value.
- If another completion source has priority, withhold scalar resolve-ready so
  W2 holds and retries when the sources target different rows. Never emit both
  completion sources in one cycle or clear W2 merely because it was a
  candidate. Treat same-row candidates as duplicate producer ownership unless
  both sources carry enough exact identity and side-effect evidence to prove a
  separate idempotent policy.
- Keep physical GPR data and non-speculative P-tag readiness in one canonical
  owner. A write request or port grant reserves bandwidth only; it must not
  mutate data or readiness until exact W2 resolve, required RF writeback, and
  required wakeup all fire atomically with ROB completion.
- Drive resident issue-queue global-P wakeup from that same committed RF fire,
  not from write request/grant and not only by polling the newly registered
  ready mask one edge later. Update matching valid, non-issued P source
  next-state readiness with the ready table on the accepted edge; wakeup at N
  is pick-visible at N+1 and must never affect selection at N.
- Treat finite scalar RF read ports as an explicit physical Chisel enhancement,
  not as behavior copied from LinxCoreModel: the current model services every
  scalar read request and has no scalar read denial. Preserve architectural
  equivalence by granting a uop's required reads atomically, cancelling only
  the losing `inflight` attempt, retaining the resident row, and proving later
  retry through generated RTL plus commit comparison.
- In a banked shared IQ, first form the oldest selectable candidate independently
  for each represented STID. Compare wrap-qualified RID age only between rows
  with the same STID; choose among different STIDs with advancing round-robin
  state. Apply the same rule at bank-local pick, global I1 admission, and
  shared I2 output arbitration. Advance fairness only when the selected
  transaction advances.
- Treat unresolved control as an admission frontier, not merely an arbiter
  preference. A younger same-STID row must not enter I1 while an older control
  row is resident. For Linx, BRU rows and redirecting `FRET.STK` own this
  frontier; retain exact `(STID, BID, RID)` across IQ release until central
  recovery accepts cleanup. Do not globally flush older issue/store ownership
  to close the release-to-recovery gap.
- Preserve store completion order across issue banks: a store may enter I1 only
  when no older resident store exists in the same STID. Loads and non-memory
  work may still bypass under normal dependency/MDB policy, and unrelated STIDs
  remain independent. This protects FIFO STA/STD consumers without importing
  ARM memory-order or barrier semantics.
- Keep total scalar issue capacity, scalar bank count, physical read ports,
  write ports, and execution width as independent parameters with explicit
  divisibility/minimum constraints. A live two-bank ALU/spill slice is not
  evidence that the complete BRU/AGU/STD/CMD physical queue layout or
  two-write-port S1/S2 dispatch is implemented.
- Parameterize physical GPR capacity and write-port count independently of the
  Linx architectural P-register namespace. One port serializes all producers;
  multiple ports may accept independent tags in one cycle. Serialize same-tag
  requests with deterministic priority and reject duplicate committed owners.
- Keep Linx T/U local-link data and qtag wakeup outside the global P ready
  table. Until the point-to-point sink is integrated, reject a T/U W2 request
  with an explicit backend contract error and no ROB/RF/wakeup evidence; do
  not silently deadlock it or substitute a global P-tag write.
- Once all live consumers instantiate the canonical GPR owner directly,
  delete compatibility RF wrappers, tests, and file-level pages. Keep history
  in git and update current architecture evidence so no second state owner can
  return through a stale integration path.
- During typed precise recovery, suppress stage movement and side effects,
  prune matching W1/W2 entries, and preserve unrelated lanes. Do not replace
  scoped recovery with a global stage clear.
- Exported `pending`, `empty`, and top-level quiescence must aggregate the
  retained queue, in-flight reservations, and every registered W1/W2 stage.
  Queue-empty alone is not load-return completion evidence.
- Generated-RTL proof must cover selected-lane backpressure with independent
  credit, full-lane simultaneous dequeue/enqueue, ROBID-wrap pruning,
  prune-cycle mutation suppression, resident fullness without a request, and
  scope/payload identity on drain. Completion integration proof must also wrap
  and reuse a ROB slot, reject the stale pre-wrap RID, accept the current
  generation, hold scalar W2 under legal different-row contention, and classify
  same-row contention as duplicate producer ownership. Physical-state proof
  must also cover request hold with no early mutation, each public sink allow,
  same-tag and independent-tag contention, actual one-port and multi-port
  configurations, and an unsupported T/U negative case.
- Banked-issue proof must force simultaneous bank-local picks, nonzero I1
  contention and cancellation, retained-row retry, multiple resident I2 rows,
  same-STID oldest selection, and cross-STID fairness without cross-lane RID
  comparison. CoreMark through a commit-only top is no-regression evidence,
  not natural bank-contention activation; cite top-visible nonzero fabric
  counters only when the RF/issue composition generated them.
- Extend banked-issue proof with a younger same-STID control row held through
  exact release, unrelated-STID progress, retained external redirect identity,
  and younger-store retry after the oldest store releases. A full-path run that
  exposes a later LSU owner deadlock is evidence for the next packet, not
  permission to weaken these issue frontiers.
- Reuse these ISA-neutral queue, credit, arbitration, residency, and pruning
  mechanisms. Reject ARM exception levels, condition flags, exclusive
  monitors, barrier encodings, acquire/release opcode policy, and ARM-specific
  return state.

## When merging LinxCore PRs

After merging to `LinxISA/LinxCore`, bump the superproject gitlink:

- In the LinxISA superproject checkout, update the `rtl/LinxCore` submodule pointer on `main`, PR + merge.

## Scalar GGPR mapQ capacity triage

- LinxCoreModel sizes scalar GGPR rename with independent model knobs:
  `ggpr_count = 128` and `ggpr_mapq_depth = 256` in `configs/core.toml`.
- Do not tie Chisel scalar GPR mapQ capacity to local T/U `mapQDepth`.
  Local T/U `mapQDepth` controls compact ROBID sequence plumbing; scalar
  `gprMapQDepth` controls GGPR rename pressure.
- If a marker-row/CoreMark gate stops with `decodeBlockedByRename=1`,
  nonzero `gprFree`, and `gprMapQFree=0`, check scalar `gprMapQDepth` against
  LinxCoreModel before debugging ROB/BID ordering.
- The known R195 symptom was `pc=0x4000557a`, `gprFree=63`,
  `gprMapQFree=0` in the 1024-row admitted-marker CoreMark probe. R196 split
  `gprMapQDepth = 256` from local T/U `mapQDepth = 32`.
- A naive 256-depth `GPRRenameCheckpoint` can become a Verilator front-end
  bottleneck. R198 split the largest per-architecture replay and commit scans
  into helper modules (`GPRRenameReplaySurvivorSelect` and
  `GPRRenameCommitArchSelect`), which makes the 256-depth marker-row top reach
  Verilator build and DUT comparison. Do not inline those scans back into the
  parent checkpoint without rerunning the model-sized marker-row smoke and
  1024-row gate.
- R202 closed the post-R198 stale source-value failure as scalar GPR checkpoint
  restore, not RF readiness. If a marker-row/CoreMark gate shows an architectural
  source using an older physical tag while the arch last-writer diagnostic has a
  newer tag, inspect block-stop cleanup BID selection and checkpoint refresh
  before changing RF, forwarding, or `gprMapQDepth`.
- The passing R202 baseline is
  `generated/r202-marker-stop-restore-qemu-elf-xcheck`: 1024 raw QEMU rows,
  953 expected rows, 288 admitted marker commits filtered, 665 compared rows,
  and zero mismatches.

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
