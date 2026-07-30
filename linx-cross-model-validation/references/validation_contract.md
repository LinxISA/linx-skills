# Validation Contract

## Inputs and observation

`tests/cross_model/build_elf.py` builds one test ELF. Keep deterministic input
arrays in the ELF so QEMU, gfrun, and gfsim receive identical code, addresses,
and initial bytes.

The ELF declares `cross_model_result` and `cross_model_result_size`. Resolve
both from the symbol table instead of duplicating a guest address or total size
in the manifest. Run each model in an isolated artifact directory and export
that range to the model's own `result.bin` after a passing finisher.

The finisher at `0x10009000` with value `0x5555` is a termination protocol, not
the result oracle. A natural exit, pass finisher, decode success, retire log, or
internal Tile state does not establish semantic agreement by itself.

## Golden and comparisons

Partition the exported range into typed, non-overlapping JSON manifest
segments. Generate `golden.bin` independently from the documented operation
semantics and deterministic inputs. Perform all applicable comparisons:

```text
qemu  <-> golden      qemu  <-> gfrun
gfrun <-> golden      qemu  <-> gfsim
gfsim <-> golden      gfrun <-> gfsim
```

Use exact comparison for integer and byte segments. Use floating-point
tolerance only when the manifest explicitly selects a policy such as
`fp32_ulp` and supplies its bound. Report the first mismatching segment,
byte/element offset, row/column, raw bits, and typed values.

## Artifacts

Publish runs below
`regression_results/cross_model/<run-id>/cases/<case>/`:

- `golden.bin`, `resolved_manifest.json`, `compare.json`, and `report.md`;
- one directory per model containing `result.bin`, `run.json`, `stdout.log`,
  and `stderr.log`.

Treat missing, short, long, or late result files as harness/model failures.
Classify timeout, assertion, crash, fail finisher, dump error, result mismatch,
and harness error separately. Two models failing the same way never pass.

Before running QEMU, probe the selected `qemu-system-linx64` with the `virt`
machine properties `cross-model-dump`, `cross-model-address`, and
`cross-model-size`, and reject an explicit `Property ... not found` result.
Do not rely only on `virt,help`: dynamically added instance properties may be
absent from its class-property listing. A binary without the properties cannot
publish the architectural result and is a harness/QEMU-head mismatch. Prefer
an explicit `QEMU_BIN`; otherwise use the matching QEMU checkout's `build-linx`
output.

## Checkpoints and model state

The current harness compares final architecture-visible memory. It does not
compare TileReg, ACC, GPR, instruction traces, or internal microarchitectural
state after every operation. Export Tile or ACC results through an
architecture-visible path, normally `TSTORE` or `ACCCVT` followed by `TSTORE`.

For functional localization, reserve one result segment per important
operation and export intermediate Tile results from the carrier. Those extra
stores consume modeled resources and change gfsim timing; do not use such a run
as evidence for an uninstrumented cycle count.

A non-perturbing checkpoint requires a passive observer at architectural
operation completion/retirement. It must not enqueue modeled requests, consume
ports, alter arbitration, stall retirement, or change model cycles. Retain the
final-memory comparison as the acceptance oracle even when diagnostic
checkpoint traces are available.

## ISA-version boundary

Run generated PTO ISA v0.2 cross-model ELFs with the model's default canonical
decoder. Use `--pto-v02 false` only for the repository's legacy v0.1 prebuilt
pass lists. Those lists are model-regression evidence, not the
QEMU-gfrun-gfsim result-comparison oracle.
