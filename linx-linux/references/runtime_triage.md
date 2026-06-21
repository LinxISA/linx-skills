# Runtime Triage

## Quick commands

```bash
llvm-addr2line -e /Users/zhoubot/linx-isa/kernel/linux/build-linx-fixed/vmlinux <pc>
llvm-objdump -d /Users/zhoubot/linx-isa/kernel/linux/build-linx-fixed/vmlinux | rg -n "<symbol>|<pc>"
LINX_CPU_DUMP_DEBUG=1 /Users/zhoubot/linx-isa/emulator/qemu/build/qemu-system-linx64 ...
```

## Hosted user-fault breadcrumbs

- When musl fork/exec/stdio smoke reaches userspace and then traps, preserve
  the kernel-side `LINX_USER_TRAP` and `LINX_REBOOT` debug UART breadcrumbs
  until the same sample passes without QEMU fault tracing.
- Pair those breadcrumbs with QEMU `LINX_FAULT_TRACE=1` filters around the
  first wrong user PC or instruction-count window. Do not widen Linux logging
  before checking whether the QEMU trace already identifies the bad target,
  fault address, or trap delivery state.

## Early-boot boundary walk

- When smoke stops before userspace, move the boundary with single-character
  UART markers through:
  - `setup_arch()`
  - `paging_init()`
  - `free_area_init()`
  - `setup_per_cpu_areas()`
  - `start_kernel()`
- Rebuild only `vmlinux`, then rerun smoke with:

```bash
TIMEOUT=20 LINX_DISABLE_TIMER_IRQ=1 SKIP_BUILD=1 \
QEMU=/Users/zhoubot/linx-isa/emulator/qemu/build/qemu-system-linx64 \
python3 /Users/zhoubot/linx-isa/kernel/linux/tools/linxisa/initramfs/smoke.py
```

- Treat each newly reached marker as proof that everything before it returned;
  do not keep reworking earlier subsystems once the trace boundary has moved.

## Command line corruption vs parser failure

- If boot stalls around `parse_args("Booting kernel", ...)`, dump the first
  bytes of `static_command_line` both right after `setup_command_line()` and
  again just before `parse_args()`.
- Classification:
  - bytes already wrong at both points: `/chosen/bootargs` import is wrong;
    fix the DT property read/copy path first.
  - bytes correct before parse but bad later: investigate overwrite between
    `setup_command_line()` and `parse_args()`.
  - bytes correct and parser markers stop on one option: debug that specific
    parameter handler or unknown-option fallback.
- For Linx bring-up, prefer the generic flat-DT accessor for string properties
  such as `/chosen/bootargs` if a custom property walker returns corrupted
  string data.

## Log-buffer false blocker

- If the trace reaches `random_init_early()` and then dies before the next
  `start_kernel()` marker, isolate `setup_log_buf(0)` before changing unrelated
  init code.
- On Linx bring-up, the non-early printk ring-buffer growth path can be a
  temporary blocker by itself; keeping the built-in log buffer is an acceptable
  short-term bring-up step while moving the boundary forward.

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
