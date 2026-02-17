# Workload Matrix

## Families

- CoreMark
- Dhrystone
- PolyBench
- TSVC

## Required per-workload report fields

- source location and revision
- compile command and compiler SHA
- runtime command and QEMU/Linux SHA
- pass/fail markers
- timeout status
- optional performance counters

## TSVC requirement

TSVC is mandatory workload coverage for matrix completeness.

## Failure handling

Keep one log per workload/test and include first failing marker or trap signature.
