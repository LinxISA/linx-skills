# linx-skills

Linx ISA bring-up related Codex skills.

## Canonical naming scheme

- Canonical skill names use `linx-<module>` for module agents.
- One skill owns one superproject module scope.
- Deprecated aliases are removed during install sync.

## Included skills
- linx-superproject
- linx-linxcore
- linx-pycircuit
- linx-qemu
- linx-isa
- linx-lib
- linx-compiler
- linx-linux

## Module ownership map
| Skill | Module scope |
| --- | --- |
| `linx-superproject` | superproject integration and repin governance |
| `linx-linxcore` | `rtl/LinxCore` |
| `linx-pycircuit` | `tools/pyCircuit` |
| `linx-qemu` | `emulator/qemu` |
| `linx-isa` | ISA/docs architecture contracts |
| `linx-lib` | `lib/` runtime bring-up |
| `linx-compiler` | `compiler/llvm` |
| `linx-linux` | `kernel/linux` |

## LinxCore maturity collaboration policy

These skills encode strict cross-domain collaboration rules for LinxCore maturity:

- phase-based gate program (`G0..G5`) in `docs/bringup/agent_runs/manifest.yaml`,
- phase-bound waivers with explicit expiry and issue links,
- PR + nightly gate tiers with dual-lane (`pin` + `external`) closure,
- mandatory evidence pack (gate report + SHA manifest + logs/traces).

## Programmatic install/prune

Use the canonical installer to sync skills and remove deprecated aliases:

```bash
bash /Users/zhoubot/linx-skills/scripts/install_canonical_skills.sh
```
