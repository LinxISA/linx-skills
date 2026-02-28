---
name: linx-lib
description: Linx libc bring-up workflow across glibc and musl. Use when building or debugging libc ports, enforcing static/shared runtime split policy, aligning ABI/relocation behavior with Linux and toolchain, or reporting staged gate outcomes (G1/M1-M3/R1-R2).
---

# Linx Lib

## Overview

Use this skill for combined libc bring-up and runtime policy across `lib/glibc` and `lib/musl`.

## Gate ladder

- glibc:
  - `G1a` configure + `csu/subdir_lib`
  - `G1b` shared `libc.so` gate
- musl:
  - `M1/M2/M3` build gates
  - `R1/R2` runtime gates

## Canonical commands

```bash
bash /Users/zhoubot/linx-isa/lib/glibc/tools/linx/build_linx64_glibc.sh
MODE=phase-b /Users/zhoubot/linx-isa/lib/musl/tools/linx/build_linx64_musl.sh
python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link static
python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link shared
```

## Runtime policy

- Static and shared outcomes are first-class and separate.
- No aggregate green if one mode fails.
- Preserve mode-level logs and summaries.

## Alignment checks

- ABI/register conventions align with Linux UAPI.
- Relocation IDs/contracts align across libc + linker + kernel.
- signal/ucontext/setjmp behavior is cross-stack consistent.

## Skill evolve loop (mandatory closeout)

- At closeout, decide `skill-evolve: update` or `skill-evolve: no-update`.
- Update this skill only for material reusable findings:
  - new libc/runtime contract required by gates,
  - new mandatory build/runtime command/env for reproducible results,
  - new recurring triage flow for static/shared divergences.
- Do not update for minor optimization, wording cleanup, or one-off local workaround.
- If update is needed, validate with:
  - `python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/zhoubot/linx-isa/skills/linx-skills/linx-lib`
  - `python3 /Users/zhoubot/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main`

## Included scope

This consolidated skill absorbs prior `glibc-bringup`, `musl-bringup`, and libc-focused call/ret runtime checks.

## References

- `references/gates_and_policy.md`
