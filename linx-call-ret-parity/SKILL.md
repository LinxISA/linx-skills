---
name: linx-call-ret-parity
description: Call/ret contract closure across Linx compiler, emulator, kernel, and libc/runtime gates. Use when debugging return-path control flow, enforcing call-header adjacency, validating setc.tgt requirements, or triaging runtime traps caused by call/ret contract drift.
---

# Linx Call/Ret Parity

## Overview

Use this skill when the task is to make Linx call/ret behavior precise and consistent across compiler, emulator, kernel references, and test gates.

## Normative contract

- Normal function shape: `FENTRY + FRET.STK`.
- Tail-transfer shape: `FENTRY + FEXIT` followed by legal block transfer.
- `BSTART.RET` requires `setc.tgt ra`.
- `RET`/`IND`/`ICALL` dynamic targets must be explicit (`setc.tgt`) and block-legal.
- Call headers are fused and adjacent: `BSTART.CALL` + immediate `SETRET/C.SETRET`.

Reference:
- `references/callret_contract.md`

## Workflow

1. Lock docs first:
  - `/Users/zhoubot/linx-isa/docs/reference/linxisa-call-ret-contract.md`
  - `/Users/zhoubot/linx-isa/docs/reference/linxisa-assembly-agent-guide.md`
  - `/Users/zhoubot/linx-isa/docs/bringup/LINX_ASM_ABI_UNWIND_CONTEXT_CHECKLIST.md`
2. Enforce compiler behavior:
  - musttail-first lowering
  - fused call header semantics
  - direct/indirect tail-transfer lowering after `FEXIT`
3. Enforce QEMU strict traps for contract violations.
4. Run compile/runtime matrices and negative trap checks.
5. Run Linux cross-stack audit script and confirm kernel-side pattern parity.

## Required checks

- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_tests.py --suite callret`
- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_callret_contract.py`
- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link static --sample callret`
- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link shared --sample callret`
- `bash /Users/zhoubot/linx-isa/tools/ci/check_linx_callret_crossstack.sh`
- `bash /Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests/run.sh`
- `python3 /Users/zhoubot/linux/tools/linxisa/initramfs/smoke.py`
- `python3 /Users/zhoubot/linux/tools/linxisa/initramfs/full_boot.py`

## Runtime-first policy

- Treat freestanding call/ret pass as necessary but not sufficient.
- Keep static and shared Linux+musl call/ret runtime as separate required outcomes.
- If one mode fails, keep global call/ret runtime status red and preserve mode-specific logs.
- For repeated block-trap loops, symbolicate Linux PC and cross-check QEMU target legality enforcement.

## References

- `references/callret_contract.md`
- `references/test_matrix.md`
- `references/blocker_playbook.md`
- `references/crossstack_skills.md`
