# Runtime Triage

## Quick commands

```bash
llvm-addr2line -e /Users/zhoubot/linux/build-linx-fixed/vmlinux <pc>
llvm-objdump -d /Users/zhoubot/linux/build-linx-fixed/vmlinux | rg -n "<symbol>|<pc>"
```

## Exit condition

Both smoke and full boot pass without repeated trap loops.
