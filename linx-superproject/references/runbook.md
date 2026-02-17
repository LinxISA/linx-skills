# Superproject Runbook

## Baseline

1. sync/init submodules
2. run layout check
3. verify clean status

## Minimum gate pack

- `python3 tools/bringup/check26_contract.py`
- `bash avs/compiler/linx-llvm/tests/run.sh`
- `bash avs/qemu/check_system_strict.sh`
- `bash avs/qemu/run_tests.sh --all --timeout 20`

## Reporting

Publish command + SHA provenance for each result.
