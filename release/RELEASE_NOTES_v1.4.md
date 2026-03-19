# KMotor_Pro v1.4

Second stable `KMotor_Pro` milestone for KiCad 9.

## Included

- deterministic stator PCB generation
- secondary Magnet PCB workflow with shared mechanics
- `Generate`, `Generate Magnet PCB`, and `Generate Both`
- fabrication presets for JLCPCB and PCBWay
- winding mode stats for `PCB` and `Wire`
- total copper length and turns-per-layer estimate
- derived motor constants:
  - `Ke est`
  - `Kt est`
  - `Kv est`
- derived operating estimates:
  - winding factor
  - no-load RPM @ 12V
  - stall current
  - stall torque
- deterministic center-via placement fixes for tested low-height edge cases
- `Compact` coil mode controls and `maxSpec layout` workflow

## Notes

- `Compact` is currently a stable workflow/UI mode; its dedicated final geometry solver is still being expanded.
- `3P` remains the primary stable target.
- `1P` is usable and improved.
- `3P+N` still needs a final dedicated neutral-routing topology.
