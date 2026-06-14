# Runtime Gates

## Minimum regression set

- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_tests.py --all --timeout 20`
- `bash /Users/zhoubot/linx-isa/avs/qemu/check_system_strict.sh`

## Musl runtime checks

- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link static`
- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link shared`

## Linux-user process smoke

When a local/recovered Linx linux-user QEMU exists, validate userspace ABI
bring-up before full-system rootfs work with:

- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link static --runner user --qemu-user /Users/zhoubot/linx-isa/emulator/qemu/build-user/qemu-linx`
- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_glibc_smoke.py --runner user --qemu-user /Users/zhoubot/linx-isa/emulator/qemu/build-user/qemu-linx`

This path runs `qemu-linx -L <sysroot> <elf>` and checks the same smoke pass
markers. It is a pre-rootfs gate, not a replacement for `qemu-system-linx64`
kernel/initramfs validation.

## Acceptance

Accept only when first-divergence root cause is fixed and strict/system gates are green.
