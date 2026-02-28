# linx-skills

Linx ISA bring-up related Codex skills.

## Canonical naming scheme

- Canonical skill names use `linx-<module>` for module agents.
- One skill owns one superproject module scope.
- Deprecated aliases are removed during install sync.

## Included skills
- linx-superproject
- linx-core
- linx-pycircuit
- linx-qemu
- linx-isa
- linx-lib
- linx-compiler
- linx-linux

## Managed utility skills
- linx-skills-submodule

## Module ownership map
| Skill | Module scope |
| --- | --- |
| `linx-superproject` | superproject integration and repin governance |
| `linx-core` | `rtl/LinxCore` |
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

## Safe skill-evolution workflow

For bring-up evolution without destructive churn:

1. Pull latest `skills/linx-skills` in superproject before bring-up work.
2. Update only the touched skill folders.
3. Validate touched skills and guard change scope:

```bash
python3 /Users/zhoubot/linx-skills/scripts/check_skill_change_scope.py --base origin/main
python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
```

4. Summarize skill updates in bring-up evidence.
5. Commit to `linx-skills`, repin superproject submodule, then install to Codex skills.
