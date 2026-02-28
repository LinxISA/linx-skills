---
name: linx-skills-submodule
description: Safe workflow for evolving the `skills/linx-skills` submodule during Linx bring-up. Use when pulling latest skills, making targeted skill updates, summarizing skill deltas, validating scope, committing to linx-skills, and installing into Codex skills.
---

# Linx Skills Submodule

## Overview

Use this skill for controlled, incremental evolution of skills during superproject bring-up.

## Canonical loop

1. Pull latest `skills/linx-skills` from `origin/main`.
2. Install canonical skills to `$CODEX_HOME/skills`.
3. Run the evolve decision gate (`update` vs `no-update`).
4. Update only the skills touched by current bring-up work when decision is `update`.
5. Validate touched skills and run scope guard.
6. Summarize what changed and why.
7. Commit to `linx-skills` and repin in `linx-isa`.

## Commands

```bash
git -C /Users/zhoubot/linx-isa submodule update --init --recursive skills/linx-skills
git -C /Users/zhoubot/linx-isa/skills/linx-skills fetch origin main
git -C /Users/zhoubot/linx-isa/skills/linx-skills checkout origin/main
bash /Users/zhoubot/linx-isa/tools/bringup/sync_canonical_skills.sh
python3 /Users/zhoubot/linx-skills/scripts/check_skill_change_scope.py --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main
python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
```

## Anti-destruction policy

- Do not delete skill folders unless explicitly approved.
- Keep edits narrow to touched skills and policy files.
- Use `check_skill_change_scope.py` before commit.
- If a deletion is truly required, list each allowed removal explicitly.

## Evidence requirements

- Summarize changed skill folders, rationale, and impacted bring-up gates.
- Include pre/post validation output in bring-up notes.
- Record the final `linx-skills` SHA used for superproject repin.

## Skill evolve decision gate (mandatory)

- Decision is `update` only when at least one material item exists:
  - new contract/invariant/gate absent from current skill docs,
  - new recurring failure pattern that changed the triage workflow,
  - new mandatory reproducibility command/env/artifact path.
- Decision is `no-update` for:
  - formatting/wording cleanup only,
  - minor optimization without new policy,
  - one-off workaround not reusable by future agents.
- To avoid update loops/churn:
  - at most one skill-evolve commit per agent run unless a second material finding appears,
  - do not create follow-up skill-only churn PRs for style-only edits.
- Always record one explicit closeout line in evidence:
  - `skill-evolve: update <skills...> (<reason>)` or
  - `skill-evolve: no-update (<reason>)`.

## References

- `references/maintenance.md`
