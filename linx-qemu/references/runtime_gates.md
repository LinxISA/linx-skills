# Runtime Gates

## Minimum regression set

- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_tests.py --all --timeout 20`
- `bash /Users/zhoubot/linx-isa/avs/qemu/check_system_strict.sh`

## Musl runtime checks

- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link static`
- `python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link shared`

## Acceptance

Accept only when first-divergence root cause is fixed and strict/system gates are green.
