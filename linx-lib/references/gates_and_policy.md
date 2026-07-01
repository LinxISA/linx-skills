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

## Allocator bisection policy

Keep `MALLOC_IMPL=mallocng` as the default maintained phase-b musl allocator.
Use `MALLOC_IMPL=oldmalloc` only as a targeted bisection lane when mallocng
metadata assertions, allocator-list corruption, or allocator-adjacent SPEC
faults appear.

For SPEC allocator bisection:

```bash
MALLOC_IMPL=oldmalloc MODE=phase-b bash /Users/zhoubot/linx-isa/lib/musl/tools/linx/build_linx64_musl.sh
bash /Users/zhoubot/linx-isa/tools/build_linx_llvm_cpp_runtimes.sh --profile spec --mode phase-b
LINX_SPEC_LINK_MODE=default bash /Users/zhoubot/linx-isa/tools/spec2017/build_int_rate_linx.sh \
  --mode phase-b --force-static --bench <bench> --emit-manifest <manifest.json>
```

Then rerun the same QEMU matrix shape and compare failure class, heartbeat
progress, trap registers, and OOM counters. A switch from mallocng metadata
assertions to oldmalloc `live-timeout` is evidence for allocator metadata,
codegen, or VM-path triage; it is not SPEC correctness closure and must not
promote oldmalloc to the default baseline.
