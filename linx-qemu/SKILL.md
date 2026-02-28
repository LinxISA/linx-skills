---
name: linx-qemu
description: Linx emulator development workflow for submodule `emulator/qemu`. Use when implementing or debugging decode/execute behavior, trap and interrupt handling, MMU and device interactions, or AVS runtime/system regressions where emulator behavior is the likely first divergence.
---

# Linx QEMU

## Overview

Use this skill for emulator-focused work in `emulator/qemu` and for runtime failures where QEMU is the likely first divergence point.

## Required gates

```bash
bash /Users/zhoubot/linx-isa/avs/qemu/check_system_strict.sh
bash /Users/zhoubot/linx-isa/avs/qemu/run_tests.sh --all --timeout 10
python3 /Users/zhoubot/linx-isa/tools/bringup/check_qemu_opcode_meta_sync.py --qemu-root /Users/zhoubot/linx-isa/emulator/qemu --allowlist /Users/zhoubot/linx-isa/docs/bringup/qemu_opcode_sync_allowlist.json --report-out /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_opcode_sync_latest.json --out-md /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_opcode_sync_latest.md
python3 /Users/zhoubot/linx-isa/tools/bringup/report_qemu_isa_coverage.py --spec /Users/zhoubot/linx-isa/isa/v0.3/linxisa-v0.3.json --qemu-meta /Users/zhoubot/linx-isa/emulator/qemu/target/linx/linx_opcode_meta_gen.h --report-out /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_isa_coverage_latest.json --out-md /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_isa_coverage_latest.md
```

## Workflow

1. Reproduce with the smallest AVS case.
2. Capture the first wrong architectural event (`pc`, opcode, trap/irq cause, memory side-effect).
3. Compare against ISA semantics and expected Linux/runtime behavior.
4. Patch decode/execute or exception path and add a focused regression.
5. Re-run runtime and system strict gates.

## Collaboration rules

- When QEMU diverges from LinxCore/pyCircuit traces, act as reference owner and publish first mismatch evidence.
- Keep timer IRQ policy explicit in strict runs (`LINX_EMU_DISABLE_TIMER_IRQ=0` by default).
- Coordinate trap/MMU semantic updates with `linx-isa` before declaring closure.

## Skill evolve loop (mandatory closeout)

- At closeout, decide `skill-evolve: update` or `skill-evolve: no-update`.
- Update this skill only for material reusable findings:
  - new emulator semantic rule that must stay aligned with LinxArch,
  - new required runtime gate/command/env for reproducibility,
  - new recurring first-divergence triage sequence.
- Do not update for minor optimization, wording cleanup, or one-off local workaround.
- If update is needed, keep scope narrow and validate with:
  - `python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/zhoubot/linx-isa/skills/linx-skills/linx-qemu`
  - `python3 /Users/zhoubot/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main`

## References

- `references/runtime_gates.md`
