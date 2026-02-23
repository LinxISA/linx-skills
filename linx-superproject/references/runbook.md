# Superproject Runbook

## Baseline

1. sync/init submodules
2. run layout check
3. verify clean status
4. verify pin lane uses in-repo toolchain and in-repo QEMU/Linux paths

## Minimum gate pack

- `python3 tools/bringup/check26_contract.py`
- `bash avs/compiler/linx-llvm/tests/run.sh`
- `bash avs/qemu/check_system_strict.sh`
- `bash avs/qemu/run_tests.sh --all --timeout 20`
- `LINX_SEMIHOST=0 python3 avs/qemu/run_tests.py --suite system --require-test-id 0x110F --timeout 15`

## Reliability notes

- Run `avs/qemu` gate commands sequentially unless each run gets its own output
  directory; concurrent runs can race on `avs/qemu/out`.
- If Linux `ctx_tq_irq_smoke.py` fails with `irq0_delta=0`, archive
  `/proc/interrupts` and `/proc/stat` snapshots before deciding FAIL vs BLOCKED.

## Reporting

Publish command + SHA provenance for each result.
