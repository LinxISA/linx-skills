---
name: linx-workloads-bench
description: Benchmark and workload execution workflow for LinxISA. Use when building/running CoreMark, Dhrystone, PolyBench, or TSVC workloads on Linx QEMU/Linux, triaging benchmark failures, and producing reproducible performance or pass/fail reports tied to exact toolchain and runtime SHAs.
---

# Linx Workloads Bench

## Overview

Use this skill to build and run workloads in a reproducible way, with explicit artifacts and run metadata for each benchmark family.

## Workload domains

- CoreMark: `workloads/coremark/upstream/`
- Dhrystone: `workloads/dhrystone/upstream/`
- PolyBench: `workloads/third_party/PolyBenchC/`
- TSVC: run via Linx workload harness in `workloads/`

## Execution workflow

1. Select toolchain and runtime lane (`pin` or `external`).
2. Compile workloads with recorded compiler SHA/config.
3. Run on QEMU/Linux with timeout and marker checks.
4. Emit summary report per workload: build status, run status, key metrics, artifact links.

## TSVC policy

- Treat TSVC as first-class workload coverage, not optional.
- Keep compile flags and dataset config recorded with output.
- Keep failing kernels/tests listed explicitly in report.

## QEMU run expectations

- Non-zero exit or missing pass markers are failures.
- Preserve per-workload logs and command lines.
- Report both correctness status and timing/cycle data when available.

## References

- `references/workload_matrix.md`
