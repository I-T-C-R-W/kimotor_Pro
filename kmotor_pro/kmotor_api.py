# kmotor_api.py
# Central orchestration layer for KMotor_Pro
# Generated during Phase 1 refactoring

# Entry point: generate_motor(config)
# Selects strategy (PCB / wire)
# Calls solver → geometry → renderer