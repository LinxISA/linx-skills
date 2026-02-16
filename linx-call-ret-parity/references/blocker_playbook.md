# Call/Ret Blocker Playbook

## If musttail does not lower to tail-transfer

1. Verify call site is `musttail` and ABI-compatible.
2. Confirm backend emits tail pseudo form before blockify.
3. Confirm frame lowering inserts `FEXIT` path (not `FRET.STK`) for tail blocks.
4. Confirm blockify lowers tail pseudo to `DIRECT`/`IND` (not `CALL`).

## If QEMU traps unexpectedly

1. Check trap cause:
   - 7: missing adjacent setret
   - 8: invalid setret sequence
   - 9: missing `setc.tgt` for `RET/IND/ICALL`
2. Disassemble around faulting PC.
3. Verify call header adjacency and target setup in the same block.

## If Linux cross-check fails

1. Rebuild Linux Linx objects (`switch_to.o`, `entry.o`).
2. Re-run:
   - `bash tools/ci/check_linx_callret_crossstack.sh`
3. Ensure disassembly still shows:
   - `C.BSTART IND` + `setc.tgt ra` (switch_to)
   - fused `BSTART CALL ... ra=...` (entry)
