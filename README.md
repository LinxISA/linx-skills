# linx-skills

Linx ISA bring-up related Codex skills.

## Included skills
- linx-arch-bringup
- linx-avs-runtime-gates
- linx-call-ret-parity
- linx-glibc-bringup
- linx-isa-emulator
- linx-isa-manual
- linx-konata-renderer-debug
- linx-konata-trace-gen
- linx-konata-trace-validate
- linx-linux-bringup
- linx-llvm-backend
- linx-mlir-pycircuit
- linx-musl-bringup
- linx-rtl-development
- linx-superproject-governance
- linx-workloads-bench

## Linx Superproject Coverage
| Superproject area | Skill coverage |
| --- | --- |
| Superproject governance (`linx-isa`, submodules, dual-lane) | `linx-superproject-governance` |
| `avs/` runtime/compile/system gates | `linx-avs-runtime-gates` |
| `compiler/llvm` | `linx-llvm-backend`, `linx-call-ret-parity` |
| `emulator/qemu` | `linx-isa-emulator`, `linx-call-ret-parity` |
| `kernel/linux` | `linx-linux-bringup`, `linx-call-ret-parity` |
| `rtl/LinxCore` | `linx-rtl-development`, `linx-konata-trace-gen`, `linx-konata-trace-validate`, `linx-konata-renderer-debug` |
| `tools/pyCircuit` | `linx-mlir-pycircuit` |
| `lib/glibc` | `linx-glibc-bringup`, `linx-call-ret-parity` |
| `lib/musl` | `linx-musl-bringup`, `linx-call-ret-parity` |
| `workloads/` (CoreMark/Dhrystone/PolyBench/TSVC) | `linx-workloads-bench` |
| `isa/` and `docs/` | `linx-isa-manual`, `linx-arch-bringup` |

## Konata Bundle
- `linx-konata-trace-gen`: generate LinxCore Konata v0005 traces and artifact bundles.
- `linx-konata-trace-validate`: validate trace stage/record/UID integrity before UI debugging.
- `linx-konata-renderer-debug`: triage Konata parser/renderer/theme/open-path issues after validation passes.
