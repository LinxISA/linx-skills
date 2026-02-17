# Spec Alignment

## Checkpoints

- Encoding legality and reserved space behavior
- Pseudocode side effects and exception ordering
- CSR fields and privilege transitions
- Memory ordering and restartability contracts

## Downstream alignment

For semantic changes, update expectations for:
- LLVM lowering/MC checks
- QEMU decode/execute/trap behavior
- RTL block and trap state machines
