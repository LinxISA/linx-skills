# glibc Gates

## G1a (partial)

- configure succeeds
- `csu/subdir_lib` succeeds
- core startup objects available

## G1b (required next)

- shared `libc.so` build completes
- evidence emitted separately from G1a

## Reporting rules

- never collapse G1a and G1b into one status
- glibc promotion is blocked if Linux runtime baseline is unstable

## Cross-stack alignment

- relocation IDs align with Linux UAPI + musl
- signal/ucontext/setjmp behavior consistent with ABI contract
