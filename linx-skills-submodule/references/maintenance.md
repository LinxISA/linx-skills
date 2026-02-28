# Safe Maintenance Checklist

## Before bring-up

- pull latest `skills/linx-skills` from `origin/main`,
- run canonical install sync into `$CODEX_HOME/skills`,
- capture starting submodule SHA.

## During bring-up

- update only touched skill folders,
- keep module ownership explicit in skill text,
- avoid broad rename/delete operations.

## Before commit

- run `check_skill_change_scope.py`,
- run `quick_validate.py` for touched skills,
- summarize changed skills + reason + gate impact.

## After commit

- push `linx-skills` PR,
- repin superproject submodule SHA,
- run canonical install sync again.
