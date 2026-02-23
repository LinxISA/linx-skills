# Runtime Triage

## Quick commands

```bash
llvm-addr2line -e /Users/zhoubot/linx-isa/kernel/linux/build-linx-fixed/vmlinux <pc>
llvm-objdump -d /Users/zhoubot/linx-isa/kernel/linux/build-linx-fixed/vmlinux | rg -n "<symbol>|<pc>"
LINX_CPU_DUMP_DEBUG=1 /Users/zhoubot/linx-isa/emulator/qemu/build/qemu-system-linx64 ...
```

## Timer false-fail triage

- If `ctx_tq_irq_test` reports `mismatch=0` but `irq0_delta=0`, first collect:
  - `cat /proc/interrupts`
  - `cat /proc/stat`
- Classification:
  - parser/open/read error: fix userspace parser and re-run.
  - counters always zero with timer-on: keep FAIL/BLOCKED and file kernel/qemu
    evidence instead of forcing PASS.
  - counters increase and mismatch stays zero: mark PASS with run-id evidence.

## Exit condition

Both smoke and full boot pass without repeated trap loops.
