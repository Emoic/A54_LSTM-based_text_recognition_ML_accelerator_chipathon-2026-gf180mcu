DESIGN DELIVERY PACKAGE

Design: lstm16x_top
Process: GF180MCU
Reference run: lstm16x_22pin_clean4
Macro size: 1000 um x 1000 um
Top-level pins: 22, including VDD and VSS

PRIMARY STREAM FILE

deliverables/gds/lstm16x_top.gds
SHA-256: 9E77C643DD84006B0489780E924753E96B2FFC90AEB7481CD408DA7CC3D7EC4A
Size: 22,794,068 bytes

DIRECTORY CONTENTS

deliverables/
  Final GDS, DEF, LEF, ODB, Magic layout, extracted SPICE,
  gate-level netlists, SDC, SDF, SPEF, Liberty models, metrics,
  and a rendered layout image from the reference run.

source/rtl/
  RTL source files.

source/constraints/
  Flow configuration, timing constraints, and pin-order file.

verification/functional/
  Golden model, test vectors, and RTL testbenches.

verification/signoff/
  Original Magic DRC, Netgen LVS, KLayout-versus-Magic XOR,
  antenna, power-grid, illegal-overlap, and run-metrics outputs.

verification/timing/
  Post-route timing summary and reports for nine corners.

verification/em/
  Independent post-route IR-drop and current-density analysis.

run_metadata/
  Resolved flow configuration and original flow logs.

INTEGRATION BOUNDARY

This package contains a digital core macro. A foundry or MPW submission must
still follow the target shuttle's official naming, layer, seal-ring, density,
waiver, and submission-checklist requirements. Pad-ring integration, ESD
protection, package limits, and board-level voltage translation are outside
this macro and must be completed at the full-chip integration stage.
