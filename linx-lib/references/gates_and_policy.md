# Gates and Policy

## Required artifacts

- `out/libc/glibc/logs/summary.txt`
- `out/libc/musl/logs/phase-b-summary.txt`
- `avs/qemu/out/musl-smoke/summary_static.json`
- `avs/qemu/out/musl-smoke/summary_shared.json`

## Green rule

Libc runtime is green only when required static/shared tests pass per policy.
For musl PR/runtime closure, the required static and shared summaries must be
produced by `run_musl_smoke.py --sample all`; the no-sample default is only a
lightweight local repro.
