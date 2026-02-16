# Call/Ret Test Matrix

## Compiler-only

- `avs/compiler/linx-llvm/tests/c/33_callret_direct.c`
- `avs/compiler/linx-llvm/tests/c/34_callret_nested.c`
- `avs/compiler/linx-llvm/tests/c/35_callret_recursive.c`
- `avs/compiler/linx-llvm/tests/c/36_callret_indirect.c`
- `avs/compiler/linx-llvm/tests/c/37_callret_tail_musttail.c`

## LLVM lit

- `llvm/test/CodeGen/LinxISA/callret-fentry-fret.ll`
- `llvm/test/CodeGen/LinxISA/tailcall-fexit-musttail.ll`
- `llvm/test/MC/LinxISA/call-header-adjacency.s`

## QEMU runtime

- `python3 avs/qemu/run_tests.py --suite callret`
- `python3 avs/qemu/run_callret_contract.py`

## Linux+musl runtime

- `python3 avs/qemu/run_musl_smoke.py --link both --sample callret`

## Linux cross-check

- `bash tools/ci/check_linx_callret_crossstack.sh`
