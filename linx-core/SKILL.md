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
bash tools/chisel/run_chisel_tests.sh --only ROBID
bash tools/chisel/run_chisel_tests.sh --only ROBEntryStatus
bash tools/chisel/run_chisel_tests.sh --only ROBEntryBank
bash tools/chisel/run_chisel_tests.sh --only ROBFlushPrune
bash tools/chisel/run_chisel_tests.sh --only DispatchROBAllocator
bash tools/chisel/run_chisel_tests.sh --only FullBidRecoveryBridge
bash tools/chisel/run_chisel_tests.sh --only RecoveryCleanupControl
bash tools/chisel/run_chisel_tests.sh --only GPRRenameCheckpoint
bash tools/chisel/run_chisel_tests.sh --only ScalarDecodeRenameBridge
bash tools/chisel/run_chisel_tests.sh --only DecodeLoadStoreIdAssign
bash tools/chisel/run_chisel_tests.sh --only StoreSplitPayload
bash tools/chisel/run_chisel_tests.sh --only StoreDispatchQueues
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
bash tools/chisel/run_chisel_tests.sh --only ReducedCommitROB
bash tools/chisel/run_chisel_tests.sh --only LinxCoreTop
bash tools/chisel/run_chisel_rob_bookkeeping.sh --robid-only
bash tools/chisel/run_chisel_rob_bookkeeping.sh --reduced-rob
bash tools/chisel/run_chisel_reduced_rob_xcheck.sh
bash tools/chisel/run_chisel_top_xcheck.sh
bash tools/chisel/run_chisel_verilator_lint.sh
python3 tools/chisel/trace_schema_adapter.py --self-test
bash tools/chisel/run_chisel_qemu_crosscheck.sh --dry-run
```

## Chisel module agent loop

Use `rtl/LinxCore/docs/chisel/agent-loop.md` as the operational runbook for
multi-agent Chisel development. Each module packet must:

- record current `rtl/LinxCore` and `model/LinxCoreModel` SHAs before edits;
- learn behavior from LinxCoreModel C++ owner files before writing Chisel;
- update the module Markdown spec before promotion;
- keep ROB/commit/flush/BROB/QEMU cross-check infrastructure as the first proof
  surface for replacement evidence;
- run the narrow module gate plus affected cross-check gates;
- close with `skill-evolve: update ...` or `skill-evolve: no-update ...`.

Do not treat a frontend/backend Chisel module as replacement evidence merely
because its unit test passes. It needs monitored commit/stage-owner visibility
through the neutral cross-check path before it can displace pyCircuit evidence.

Toolchain facts from initial Chisel bring-up:

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
  between model `bid/gid/rid` identity and 64-bit hardware `blockBid`.
- Phase 2 `F4DecodeWindow` work must preserve LinxCoreModel `CheckMInstSize`
  instruction sizing: bit 0 clear gives 2 bytes unless header bits `[3:1]` are
  `111`, which gives 6 bytes; bit 0 set gives 4 bytes unless header bits
  `[3:1]` are `111`, which gives 8 bytes. The Chisel gate is
  `bash tools/chisel/run_chisel_tests.sh --only F4DecodeWindow`.
- F4 decode-window work must keep 8-byte window slicing sequential and
  non-compacting: a candidate that does not fit invalidates that slot and all
  later slots; do not search forward for a later instruction. Flush masks D1
  and all slot-valid bits. Slot UIDs are `(pktUid << 3) | slot`.
- Full opcode decode, register/immediate extraction, macro-boundary standalone
  behavior, and D1/D2 uop construction are deferred until the Chisel opcode
  table/decode-owner modules exist; do not bury those behaviors in the F4
  transport helper.
- Phase 2 `FrontendInstructionBuffer` work must run
  `bash tools/chisel/run_chisel_tests.sh --only FrontendInstructionBuffer`.
  The buffer is a frontend-owned FIFO for `FrontendDecodePacket` records:
  preserve FIFO order, clear occupancy on flush, keep simultaneous push/pop
  occupancy stable, and keep full-state backpressure based on pre-cycle
  occupancy.
- Chisel frontend buffers must carry `checkpointId` as packet-owned state
  alongside PC/window/packet UID. Do not reconstruct F4/D1 packet checkpoint
  identity from adjacent control wiring once a packet enters the Chisel
  frontend queue.
- Phase 2 `FrontendDecodeIngress` work must run
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeIngress`.
  This module is only the IB-to-F4 transport owner: compose
  `FrontendInstructionBuffer` with `F4DecodeWindow`, pop only on
  `decodeReady && f4.d1.valid`, preserve no same-cycle push-to-D1 bypass,
  clear/mask both children on flush, and keep opcode decode, macro-boundary
  decode, and D1/D2 uop construction in later decode-owner modules.
- Phase 2/R39/R40 `FrontendDecodeStage` work must run
  `bash tools/chisel/run_chisel_tests.sh --only FrontendDecodeStage` plus the
  affected `F4DecodeWindow`, `FrontendDecodeIngress`, and `InterfaceBundles`
  gates. This module is the first D1 decode-shape owner after F4 slots: use the
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
  top-level frontend integration must advance D1/F4 only on `decodeReady` /
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
- Do not run SBT-backed Chisel wrappers in parallel yet; a parallel ROBID test
  and ROBID bookkeeping invocation hit an SBT 2 server socket
  `Connection refused` race, while the same gates pass sequentially.
- Verilator wrappers must compile every emitted SystemVerilog file for the
  selected target, not only the named top file, because CIRCT emits instantiated
  Chisel modules as sibling `.sv` files. This applies to both the reduced ROB
  xcheck and `run_chisel_verilator_lint.sh`.
- Packet B FlushControl work must preserve LinxCoreModel `CheckOlder` branch
  order: different `stid` never compares; same-BID BID-based priority resolves
  before PE-replay special cases; same non-BID BID/RID conflicts resolve before
  generic age; PE-vs-PE age only compares within one PE.
- Packet C BROB/BID work must preserve the hardware BID contract: default BID
  is 64 bits, 128-entry slot id is `bid[6:0]`, uniqueness/age is `bid[63:7]`,
  `cmd_tag` is `bid[7:0]`, and BID flush keeps `bid <= flush_bid` while killing
  `bid > flush_bid` using full BID order.
- Commit trace work must keep the LinxCoreModel `CommitInfo` identity
  `bid/gid/rid` as 32-bit model sideband fields while preserving the hardware
  block identity separately as 64-bit `block_bid`; do not truncate the hardware
  BID into `CommitInfo.bid`.
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
  bridge is the first backend integration owner for allocation: generate the
  full hardware BID from a block cursor, allocate `BrobMetaTracker` and
  `ROBEntryBank` atomically, stamp `CommitTraceRow.blockBid`, convert the full
  BID into the ring `ROBID` sidecar for `ROBEntryBank.allocBid`, and keep RID
  allocation inside `ROBEntryBank`.
- Phase 5 `FullBidRecoveryBridge` work must run
  `bash tools/chisel/run_chisel_tests.sh --only FullBidRecoveryBridge`. This
  bridge is the first explicit recovery handoff for the two BID surfaces:
  preserve the full hardware `blockBid` for BROB/block cleanup, produce the
  ring `FlushBus.req.bid` sidecar for ROB row pruning, share the
  full-BID-to-ring-ROBID conversion with `DispatchROBAllocator`, and keep
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
  STID0; on flush, restore from checkpoint `flush.bid - 1` when valid or from
  `cmap` otherwise, prune map-queue rows by `baseOnBid` or BID/RID ordering,
  and re-apply surviving same-BID non-base entries to `smap`. Treat replay as
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
  row has both address and data ready. Keep LDQ row mutation, STQ row PC
  sidecar integration, byte forwarding, ROB nuke retirement, and final
  `FlushReq` publication in later owner packets.
- Phase 5 `LoadStoreForwarding` work must run
  `bash tools/chisel/run_chisel_tests.sh --only LoadStoreForwarding`. This
  module is the first scalar store-to-load byte selector behind
  `STQ::lookupForLoad`: build the clipped 64-byte load mask, filter same-line
  scalar stores older than or equal to the load's allocation snapshot, select
  the nearest older store per byte, forward only data-ready selected bytes, and
  report a wait/replay mask when the selected store for any requested byte is
  not data-ready. It may merge forwarded bytes over cache data, but it must not
  mutate STQ rows, LDQ wait-store state, MDB state, DCache/SCB state, recovery
  publication, or memory-event trace. Later LIQ/LHQ/STQ integration may
  pipeline the E2 CAM, E3 merge, and E4 wakeup stages, but must preserve this
  per-byte nearest-store result.
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
  `youngestStoreId` snapshot, launch only non-wait-store `Wait` rows through
  `LoadForwardPipeline`, apply E4 outcomes back to row state, publish LHQ
  records only for E4 hits, hold `StoreDataNotReady` rows as wait-store
  replays, and hold incomplete bytes as `L1DcMiss`/`missPending`. Keep precise
  `FlushBus` pruning, L1/L2 refill queues, ready-table updates, consumer
  bypass routing, a separate ResolveQ/LHQ queue, and memory-event trace in
  later owner packets.
- Phase 5 `LoadReplayWakeup` work must run
  `bash tools/chisel/run_chisel_tests.sh --only LoadReplayWakeup` and the
  affected `LoadInflightQueue` gate. This module is the first store-unit/SCB
  replay wakeup sidecar for resident LIQ rows: store-unit wakeups clear
  wait-store diagnostics by store identity plus PC, store-unit data merges only
  into same-line `L1DcMiss`/`L2Wait` rows when the store is no newer than the
  row's allocation snapshot, and SCB data merges into working same-line rows
  except `Repick`. Completion is a recomputed requested-byte mask fully covered
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
  Verilator harness, writes nested Chisel commit JSONL including an invalid
  fixed-width slot, normalizes through `trace_schema_adapter.py`, and requires
  zero mismatches against the QEMU-shaped reference trace.
- `run_chisel_top_xcheck.sh` is the first top-level generated-RTL trace proof
  for the Chisel lane: it emits a dedicated 8-entry, two-wide `LinxCoreTop`
  xcheck configuration, builds the same Verilator harness against top-level IO,
  asserts clean commit monitor outputs, and requires zero mismatches against the
  QEMU-shaped reference trace. The default top still emits `CoreParams()`.

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
- Checkpoint capture copies the current speculative map into the slot indexed
  by `bid.val` and updates `renamePtr`. In the model call path, `SPERename`
  captures this checkpoint for `inst->isLastInBlock`.
- Commit walks the map queue for matching BID in queue order, releases the old
  committed physical tag for each architectural destination, updates `cmap`,
  and clears committed rows. Same-architecture multiple writes in one block must
  release the overwritten intermediate physical tag as well as the pre-block
  committed tag.
- Flush computes `restoreBid = flush.bid - 1`. If `restoreBid <= renamePtr`,
  restore `smap` from the valid checkpoint for that BID, or from `cmap` if the
  checkpoint is invalid, then set `renamePtr = restoreBid`.
- Flush pruning uses `baseOnBid` to remove rows at or younger than `flush.bid`;
  otherwise it removes rows at or younger than the `(flush.bid, flush.rid)`
  pair. Surviving rows in the same BID must be re-applied to `smap` in map
  queue order after the checkpoint/cmap restore.
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
- Use F4-provided instruction length to select the 16/32/48/64-bit rule domain;
  do not let a wider table match a shorter F4 slot.
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
