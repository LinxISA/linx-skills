# Topology Policy

## Root-only LinxISA map

Only `/Users/zhoubot/linx-isa/.gitmodules` may contain LinxISA repo URLs.

Allowed URL forms:
- `https://github.com/LinxISA/<repo>.git`
- `git@github.com:LinxISA/<repo>.git`

## Non-root block rule

Any non-root `.gitmodules` containing `LinxISA/` links is a policy failure.

## Dual-lane governance

- Pin lane: superproject submodule SHAs.
- External lane: active external trees.

Publish side-by-side lane outcomes with full SHA manifests.

## Promotion gate

Promote external lane to pin lane only after required gates pass in integration and baseline contexts.

## Canonical submodule set

- `compiler/llvm`
- `emulator/qemu`
- `kernel/linux`
- `rtl/LinxCore`
- `tools/pyCircuit`
- `lib/glibc`
- `lib/musl`
