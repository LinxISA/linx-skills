# Compiler Checks

## Required

- pin-lane toolchain path check (in-repo clang/lld)
- MC + CodeGen tests for changed behavior
- AVS compile suite pass
- coverage threshold confirmation

## Recommended

- relocation/object inspection for ABI changes
- call/ret shape audit in generated assembly
- include command + lane + toolchain path in evidence logs
