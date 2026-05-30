---
name: linx-qemu
description: Linx emulator development workflow for submodule `emulator/qemu`. Use when implementing or debugging decode/execute behavior, trap and interrupt handling, MMU and device interactions, or AVS runtime/system regressions where emulator behavior is the likely first divergence.
---

# Linx QEMU

## Overview

Use this skill for emulator-focused work in `emulator/qemu` and for runtime failures where QEMU is the likely first divergence point.

## Target lines

Keep the active QEMU line explicit before making changes:

- Current/modern line may expose `linx64-softmmu` in the in-repo build tree.
- Recovered historical lines can instead expose:
  - `linx-softmmu`
  - `linx-linux-user`
  - `linx_be-linux-user`

Do not assume the target naming surface. Read `configs/targets/` first and use
the names that actually exist in the checked-out branch.

## Historical recovery lane

When the user provides a recovered full patch and says it is the authoritative
latest implementation, treat that as a separate recovery workflow rather than a
normal forward-port.

- Prefer finding an old upstream QEMU base that fits the patch over manually
  replaying selected hunks onto a newer branch.
- In this workspace, the recovered `my.patch`-style Linx tree matched best
  against an upstream `v7.0.0` base.
- If you must configure `linx-linux-user` on a non-Linux host during recovery,
  any host-policy relaxations in `configure` / `meson.build` are host bring-up
  adaptations, not ISA or emulator semantic changes.
- If the recovered tree references `pc-bios/LinxInit.bin` but the firmware blob
  is unavailable, prefer making that blob optional for local configure/build
  validation instead of pretending to have reconstructed it.

## Required gates

```bash
bash /Users/zhoubot/linx-isa/avs/qemu/check_system_strict.sh
bash /Users/zhoubot/linx-isa/avs/qemu/run_tests.sh --all --timeout 10
python3 /Users/zhoubot/linx-isa/avs/qemu/run_callret_contract.py
python3 /Users/zhoubot/linx-isa/tools/bringup/check_qemu_opcode_meta_sync.py --qemu-root /Users/zhoubot/linx-isa/emulator/qemu --allowlist /Users/zhoubot/linx-isa/docs/bringup/qemu_opcode_sync_allowlist.json --report-out /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_opcode_sync_latest.json --out-md /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_opcode_sync_latest.md
python3 /Users/zhoubot/linx-isa/tools/bringup/report_qemu_isa_coverage.py --spec /Users/zhoubot/linx-isa/isa/v0.56/linxisa-v0.56.json --report-out /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_isa_coverage_latest.json --out-md /Users/zhoubot/linx-isa/docs/bringup/gates/qemu_isa_coverage_latest.md
```

Coverage and opcode-sync gates must target the live v0.56 catalog. Treat any
`isa/v0.3` or `isa/v0.4` coverage command as archive-only unless explicitly
running a historical comparison.

## Incremental build policy

- Reuse one local QEMU build directory across iterations; do not `rm -rf` the
  build tree between ordinary bring-up edits.
- After the initial configure, prefer plain incremental rebuilds:

```bash
mkdir -p /tmp/linx-qemu-local-build
cd /tmp/linx-qemu-local-build
/Users/zhoubot/linx-isa/emulator/qemu/configure --with-git-submodules=ignore --target-list=linx64-softmmu --enable-plugins --disable-docs --disable-werror
ninja -C /tmp/linx-qemu-local-build qemu-system-linx64
```

- Use `run_qemu_build_clean.sh` only when you need a reproducible clean-lane
  proof or when the local incremental tree is suspected to be poisoned.

## Firmwareless boot contract

- For direct-kernel Linx runtime harnesses (`-kernel` + initramfs / direct boot),
  treat `-bios none` as mandatory unless the runner is explicitly using a
  known `...bios-none` binary wrapper.
- If a runtime/control lane reports
  `Unable to load the LINX firmware "LinxInit.bin"`, fix the harness command
  line first; do not treat that as a guest runtime regression.
- Keep control lanes aligned with bring-up lanes. If SPEC/TSVC/runtime-smoke
  runners use firmwareless boot, their control/smoke variants must do the same
  before you compare outcomes.
- If a corrected firmwareless lane still produces only repeated
  `Trace-XX ... [0000000000000000/0000000000000000/00000000/ff000000]`, treat
  that as the canonical zero-PC collapse signal. Do not spend more time on the
  wrapper once that signature appears; move directly to first-divergence state
  triage.

## Workflow

1. Reproduce with the smallest AVS case.
2. If the failure is in AVS compile or object generation, first decide whether
   the blocker belongs to the compiler surface rather than QEMU semantics.
   In particular, old Linx AVS cases that still use `%tpcrel_hi/%tpcrel_lo`,
   unfused symbolic `BSTART CALL`, or legacy block-attribute syntax should not
   be treated as emulator regressions until the in-repo `clang` integrated
   assembler accepts them.
3. Capture the first wrong architectural event (`pc`, opcode, trap/irq cause, memory side-effect).
4. Only if needed, add targeted QEMU tracing around the suspicious PC or first wrong event; do not start tracing from reset/boot by default.
5. Compare against ISA semantics and expected Linux/runtime behavior.
6. If the first divergence only appears on positive direct-call or call/ret
   runtime cases using 64-bit `L.BSTART.*` headers, verify whether the raw
   immediate decode is still in halfword units before `linx_pcrel_target()`
   shifts it into a byte offset.
7. If a firmwareless Linux/initramfs lane still shows zero guest-visible output
   after the harness is corrected, split the problem with a trivial static
   initramfs control payload before blaming SPEC/TSVC/benchmark logic.
8. When Linux task switching is involved, verify that the QEMU ACR1
   `0x1f40..0x1f5f` CSR window is a live architectural view of current block
   state, not just trap-shadow storage. The named EBARG slots (`LRA`, `TQ/UQ`,
   `LB/LC`, `EXTCTX_*`, `TPLFLAGS`) must stay spec-shaped, while emulator-only
   spill data belongs in hidden extension slots.
9. Patch decode/execute or exception path and add a focused regression.
10. Re-run runtime and system strict gates.

For recovered historical lines, insert one extra step before implementation:

1. Pick and validate the old base first.
2. Apply the recovered patch whole if possible.
3. Only then start conflict resolution or branch-local build adaptation.

## Trace policy

- Do not generate full-run QEMU traces from the beginning of execution unless no narrower reproducer exists.
- First localize the suspicious `pc`/opcode/window from AVS output, guest state, or a smaller repro, then enable trace only near that window.
- Keep trace scope minimal: shortest repro, narrowest event set, shortest instruction window, and one lane at a time.
- Treat QEMU traces as disposable debugging artifacts. Remove large trace/log outputs immediately after extracting the needed evidence.
- Clean temporary QEMU traces from `/tmp`, `/private/tmp`, and repo-local output trees before closeout when they are no longer needed.

## Collaboration rules

- When QEMU diverges from LinxCore/pyCircuit traces, act as reference owner and publish first mismatch evidence.
- Keep timer IRQ policy explicit in strict runs (`LINX_EMU_DISABLE_TIMER_IRQ=0` by default).
- Coordinate trap/MMU semantic updates with `linx-isa` before declaring closure.
- If a QEMU AVS case is blocked by current compiler asm-surface compatibility
  rather than emulator semantics, mark or skip that case explicitly in the AVS
  harness instead of counting it as a QEMU execution failure.

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
