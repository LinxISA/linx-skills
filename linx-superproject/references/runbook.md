# Superproject Runbook

## Baseline

1. sync/init submodules
2. run layout check
3. verify clean status
4. verify pin lane uses in-repo toolchain and in-repo QEMU/Linux paths
5. verify every gitlink against `docs/bringup/component-lock.v0.58.json`
6. for ISA closure, treat v0.58 as the sole active profile and its release
   manifest plus exact PTO lock as the conformance record

## Minimum gate pack

- `bash tools/ci/check_repo_layout.sh`
- `python3 tools/ci/check_component_lock.py --root .`
- `python3 tools/isa/build_golden.py --profile v0.58 --check`
- `python3 tools/isa/validate_spec.py --profile v0.58`
- `python3 tools/isa/check_canonical_v058.py --root .`
- `python3 tools/isa/check_pto_v058_manifest.py --root .`
- `make -C tools/Linx-TileOP-API check`
- `python3 workloads/pto_kernels/scripts/check_supernpu_v058.py`
- `python3 docs/check_documentation.py --root .`

The v0.58 gate pack must preserve the four-engine `VEC`/`TLSU`/`CUBE`/`SFU`
classification, treat TEPL only as the unchanged encoded carrier, accept
active TFMA, reject permanently deleted spellings, and prove the common PTO
subset against the exact locked release. Standalone SuperNPUBench and archived
v0.57 AVS Tile/PTO parity sources are not active gate evidence.

## Reliability notes

- Run `avs/qemu` gate commands sequentially unless each run gets its own output
  directory; concurrent runs can race on `avs/qemu/out`.
- If Linux `ctx_tq_irq_smoke.py` fails with `irq0_delta=0`, archive
  `/proc/interrupts` and `/proc/stat` snapshots before deciding FAIL vs BLOCKED.
- For bounded all-row SPECint gates, use `tools/bringup/run_specint_fast_gate.py`
  without a routine `--transports` override. The wrapper keeps all supported
  rows in `test-all`/`train-all`, but splits large payload rows such as
  `525.x264_r` into `*-large-9p` shards so the gate records benchmark liveness
  instead of the known oversized-initramfs VFS-root panic. Pass
  `--transports initramfs` only when intentionally reproducing transport
  behavior.

## Reporting

Publish command + SHA provenance for each result.

## Incremental post-SPEC C workload pack

After a current-SHA SPEC diagnostic run, do not invoke the whole
`full-benchmarks` stage just to collect the remaining C workload evidence. That
stage repeats SPEC build/attestation and long nightly rows. Run the incremental
pack below, with all QEMU executions serialized:

1. Run `workloads/run_benchmarks.py` for CoreMark and Dhrystone through
   `tools/bringup/run_c_benchmark_matrix.py`. Require `requested_gate=runtime`,
   `runtime_all_pass=true`, and both rows to be `RUN_PASS`; a successful build
   is not runtime evidence.
2. PolyBench is an optional Linux/QEMU runtime smoke, not a numerical oracle.
   Use the phase-b musl static lane (`LINX_SPEC_FORCE_STATIC=1`) and pass
   `--cflag=-DMINI_DATASET` to `workloads/run_polybench.py`. Upstream defaults
   to `LARGE_DATASET`, which measures emulator throughput instead of providing
   a minimal bring-up proof. Require both `gemm` and `jacobi-2d` to run, exit
   zero, and have child Linux reports with `result.ok=true`.
3. Milepost is optional and requires an explicit external source corpus whose
   `$CTUNING_ROOT/program` contains `milepost-codelet-*` sources. The in-repo
   `workloads/ctuning` directory is the runner, not the corpus. For the five-row
   sentinel require `selected_codelets=5`, `passed=5`, `failed=0`, `skipped=0`,
   and `all_pass=true`; generated `out/` objects and skipped rows are never
   coverage evidence.

For SPEC train diagnostics, report `live-timeout` separately from traps,
panics, and silent stalls. A heartbeat/site-changing timeout proves liveness,
not workload completion. Preserve the passing strict-output/hash sentinel and
the clean QEMU/kernel provenance in the machine-readable packet.

## TSVC differential sentinel

Before paying for the full 151-kernel batched TSVC gate, use a four-kernel
OFF-vs-AUTO differential sentinel over `s000`, `s2712`, `s311`, and `s332`.
These rows cover a basic loop, predicated elemental operation, reduction, and
early-exit control flow. Run OFF first, then AUTO serially against a clean
current-HEAD QEMU; pass the OFF stdout to AUTO with
`--compare-baseline-log`, `--fail-on-checksum-mismatch`, and
`--strict-fail-under 4`.

Accept only when both commands exit zero, each observes four kernels, AUTO
reports `vectorized=4`, and the checksum report has `ok=true`, no missing rows,
and zero mismatches. Record current LLVM/Clang/LLD and QEMU SHA provenance.
This is a cheap compiler/QEMU transformation oracle, not a replacement for the
required full batched TSVC gate.
