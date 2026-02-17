# AVS Gate Matrix

## Contract and compile

1. `python3 tools/bringup/check26_contract.py`
2. `bash avs/compiler/linx-llvm/tests/run.sh`
3. `python3 avs/compiler/linx-llvm/tests/analyze_coverage.py --out-dir <out> --fail-under 100`

## Runtime and system

1. `bash avs/qemu/check_system_strict.sh`
2. `bash avs/qemu/run_tests.sh --all --timeout <sec>`

## Required metadata per run

- command
- lane
- timestamp
- SHA manifest (`linx-isa`, `llvm`, `qemu`, `linux`, `LinxCore`, `pyCircuit`, `glibc`, `musl`)
- outcome
- artifacts

## Failure policy

Never mark gate green from narrative docs alone. Reproducible command plus SHAs are mandatory.
