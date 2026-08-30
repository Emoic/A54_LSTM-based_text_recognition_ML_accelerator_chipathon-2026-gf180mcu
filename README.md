# A54 A-block wrapper

This directory contains a separate physical-design wrapper for the existing
`lstm16x_top` RTL.  The LSTM implementation is unchanged.  The new top-level
module, `A54_A`, exposes exactly the internal pad-cell terminals specified by
the organizer's latest `A54_A.def` template.

Physical requirements:

- origin: `(0, 0)`
- die/PR boundary: `1110 um x 1110 um`
- DEF template: `organizer_def/A54/project_defs/A/A54_A.def`
- final top cell: `A54_A`
- external pad assignments: 22 entries in `info.yaml`
- internal pad-cell interface terminals: 125, exactly matching the DEF template

The response pads are configured as outputs (`OE=1`, `IE=0`) with weak pulls
disabled.  Clock, reset, command-valid, and command-data pads are configured as
inputs with weak pulls disabled.

The signoff-complete implementation is in the LibreLane run
`synthesis/runs/A54_A_wrapper_clean5`. Its final DEF contains the same die area,
pin names, pin uses, pin directions, and absolute pin geometries as the organizer
template. The submitted GDS also contains one top-level boundary shape on layer
0/0 from `(0, 0)` to `(1110, 1110) um`.

The organizer DEF's VDD and VSS terminals consist of multiple separate Metal2
port shapes. The compatible seed connects those shapes to continuous edge buses
and then to the generated core power grid. This preserves every organizer pin
shape while making the complete VDD and VSS networks connected for IR analysis.

Run the wrapper RTL test from this directory:

```sh
iverilog -g2012 -o tb_A54_A.vvp tb/tb_A54_A.sv rtl/A54_A.v rtl/core/*.v
vvp tb_A54_A.vvp
```

The expected final line is `WRAPPER PASS: signature=a8`.

## Final clean5 signoff results

- detailed-route DRC: 0
- Magic DRC: 0
- Netgen LVS: circuits match uniquely; all reported mismatch counts are 0
- KLayout-versus-Magic stream-out XOR: 0 differences
- final-route antenna: 0 violating nets and 0 violating pins
- setup and hold: WNS/TNS and violation counts are 0 in all nine reported corners
- maximum slew, capacitance, and fanout violations: 0 in all nine corners
- standard-cell utilization: 66.1547%
- sequential cells / functional clock sinks: 3042 / 3042
- VDD worst IR drop: 0.134545 V (2.69% of 5 V)
- VSS worst ground rise: 0.164650 V (3.29% of 5 V)

Raw reports are included under `verification/` in the submission package. The
GF180 LibreLane configuration used here does not provide a separate KLayout DRC
runset; the available signoff physical deck is Magic DRC, while stream-out
equivalence is independently checked by KLayout-versus-Magic XOR.
