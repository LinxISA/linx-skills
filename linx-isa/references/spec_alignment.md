# Spec Alignment

## Checkpoints

- Encoding legality and reserved space behavior
- Pseudocode side effects and exception ordering
- CSR fields and privilege transitions
- Memory ordering and restartability contracts
- `EBREAK` contract clarity: default `SW_BREAKPOINT`, semihost only under
  explicit enable.
- `BI=1` restore clarity: required `EBARG/BSTATE` fields and queue semantics
  (`t/u` queues vs continuation PCs) are fully enumerated.

## Downstream alignment

For semantic changes, update expectations for:
- LLVM lowering/MC checks
- QEMU decode/execute/trap behavior
- RTL block and trap state machines
- Linux trap-return and context-switch restoration points
