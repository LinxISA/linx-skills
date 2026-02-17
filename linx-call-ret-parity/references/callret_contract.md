# Call/Ret Contract (Linx64)

## Required forms

- Normal return: `FENTRY ... FRET.STK`
- Tail transfer: `FENTRY ... FEXIT` then direct/indirect transfer
- Return blocks: `BSTART.RET` + `setc.tgt ra`
- Call header: adjacent `BSTART.CALL` + `SETRET/C.SETRET`
- Return label is explicit from setret; it is not assumed to be fall-through.

## Contract violations (strict mode)

- Missing adjacent setret for call headers
- setret emitted in invalid sequence (outside call header use)
- `RET`/`IND`/`ICALL` without `setc.tgt`
- Dynamic target that is not a legal block start

## Setret widths

- `c.setret`: short forward range.
- `setret`: larger forward range.
- `hl.setret`: wide signed range; use when smaller forms cannot encode the return label.

## Cross-stack anchors

- `/Users/zhoubot/linux/arch/linx/kernel/switch_to.S`
- `/Users/zhoubot/linux/arch/linx/kernel/entry.S`
