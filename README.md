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
2. Run a **skill-evolve decision gate** before editing skills:
   - Update skills only for new findings/new reusable experience:
     - new contract/invariant/gate not documented,
     - new recurring failure/triage path,
     - new mandatory reproducibility command/env/artifact.
   - Do **not** update skills for:
     - wording/formatting cleanup,
     - minor local optimization,
     - one-off workaround with no reusable policy.
3. Update only the touched skill folders when the decision gate says update is needed.
4. Validate touched skills and guard change scope:

```bash
python3 /Users/zhoubot/linx-skills/scripts/check_skill_change_scope.py --base origin/main
python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
```

5. Summarize skill decision and updates in bring-up evidence.
6. Commit to `linx-skills`, repin superproject submodule, then install to Codex skills.
