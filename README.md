# linx-skills

Linx ISA bring-up related Codex skills.

## Included skills
- linx-superproject
- linxcore
- linx-isa
- linx-lib
- linx-compiler
- linx-linux
- linx-ide

## Consolidation Map
| New consolidated skill | Absorbed scope |
| --- | --- |
| `linx-superproject` | submodule topology, dual-lane governance, AVS matrix orchestration, workload/TSVC reporting |
| `linxcore` | LinxCore RTL + block/BID semantics + cross-gate closure checklist |
| `linx-isa` | architecture bring-up + ISA manual/spec alignment |
| `linx-lib` | glibc bring-up + musl bring-up + libc runtime policy |
| `linx-compiler` | LLVM backend + compiler-side call/ret conformance |
| `linx-linux` | Linux boot/runtime bring-up + kernel-facing call/ret checks |
| `linx-ide` | emulator workflow + pyCircuit MLIR + RTL observability + Konata tooling |

## LinxCore maturity collaboration policy

These skills encode strict cross-domain collaboration rules for LinxCore maturity:

- phase-based gate program (`G0..G5`) in `docs/bringup/agent_runs/manifest.yaml`,
- phase-bound waivers with explicit expiry and issue links,
- PR + nightly gate tiers with dual-lane (`pin` + `external`) closure,
- mandatory evidence pack (gate report + SHA manifest + logs/traces).
