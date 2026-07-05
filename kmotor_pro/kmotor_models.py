from dataclasses import dataclass, field
from typing import List, Optional

# --- 1. TOPOLOGY (Die mathematische DNA) ---
@dataclass
class TopologyConfig:
    scheme: str = "3P"          # "1P", "3P", "3P+N"
    phases: int = 3
    slots: int = 6
    pole_pairs: int = 30        # Wurde bisher in Magnet definiert, gehört aber zur Topologie

# --- 2. MECHANICS / STATOR (Der physische Träger) ---
@dataclass
class StatorMechanicsConfig:
    outline_type: str = "Circle" # "None", "Circle", "Square", "Hexagon", "Octagon"
    shaft_bore_dia_mm: float = 10.0      # m_ctrlDbore
    outer_dia_mm: float = 100.0          # m_ctrlDout
    corner_fillet_mm: float = 3.1        # m_ctrlFilletRadius
    annular_width_mm: float = 5.0        # m_ctrlWmnt
    
    # Mounting Holes (Inner & Outer)
    mount_size: str = "M3"               # "None", "M2", "M3", etc.
    mount_out_count: int = 6             # m_mhOut
    mount_out_dia_mm: float = 90.0       # m_mhOutR
    mount_in_count: int = 0              # m_mhIn
    mount_in_dia_mm: float = 20.0        # m_mhInR
    
    # Corner Alignment Holes (Für Quadrate)
    corner_hole_count: int = 4
    corner_hole_dia_mm: float = 3.2
    corner_hole_offset_mm: float = 10.0

# --- 3. COIL LAYOUT (Die Kupferspiralen im Slot) ---
@dataclass
class CoilLayoutConfig:
    winding_mode: str = "PCB"            # "PCB", "Wire"
    strategy: str = "Radial"             # "Parallel", "Radial", "Compact"
    max_spec_layout: bool = False
    turns_per_layer: int = 12            # m_ctrlLoops
    
    # Radiale Ausdehnung der Spule im Slot
    inner_dia_mm: float = 26.0           # m_ctrlDin
    outer_dia_mm: float = 85.0           # m_ctrlDend
    
    # Leitungsgeometrie
    track_width_mm: float = 0.134
    track_spacing_mm: float = 0.150
    track_fillet_mm: float = 0.0         # r_fill
    wire_dia_mm: Optional[float] = 0.50  # Nur bei WindingMode "Wire"

# --- 4. STACK & PCB FABRICATION (Z-Achse und Fertigung) ---
@dataclass
class StackPcbConfig:
    layers: int = 2
    copper_weight: str = "1 oz / 35um"
    
    # Vias für die Spulen
    via_dia_mm: float = 0.45
    via_drill_mm: float = 0.30
    
    # Support Vias (Verankerung)
    support_via_mode: int = 2            # 0, 2, 4
    support_hole_dia_mm: float = 0.8
    
    # Sammelschienen (Rings)
    ring_width_mm: float = 0.80
    ring_spacing_mm: float = 0.25
    
    # Kupferfüllung (Thermal / GND)
    fill_inner_gnd: bool = True
    inner_gnd_dia_mm: float = 0.0        # 0.0 = Auto-Kalkulation
    fill_outer_gnd: bool = True

# --- 5. ROTOR & MAGNETS (Das Gegenstück) ---
@dataclass
class RotorMagnetConfig:
    shape: str = "Round"                 # "Round", "Rect"
    ring_dia_mm: float = 90.0
    rotation_offset_deg: float = 0.0
    
    # Dimensionen
    dia_mm: Optional[float] = 8.0        # Für Shape = Round
    width_mm: Optional[float] = 10.0     # Für Shape = Rect
    height_mm: Optional[float] = 5.0     # Für Shape = Rect
    length_mm: Optional[float] = 0.0     # Z-Höhe des Magneten (z.B. für 3D Simulation)
    
    # Abstände und Feld
    gap_mm: float = 0.5                  # Mechanischer Luftspalt
    keepout_mm: float = 0.0              # Toleranzabstand
    b_gap_est_tesla: float = 0.60        # Geschätztes B-Feld

# --- 6. PERIPHERALS (Terminals & Silkscreen) ---
@dataclass
class PeripheralsConfig:
    # Terminals (Phasenanschlüsse)
    term_type: str = "THT"               # "THT", "SMD", "None"
    term_size: str = "1.0"
    term_offset_mm: float = 3.0          # dterm (Abstand zum innersten Ring)
    
    # Silkscreen Optionen
    silk_cross_guides: bool = False
    silk_slot_frames: bool = False
    silk_degree_scale: bool = False
    silk_hole_scales: bool = False
    corner_scale_step_deg: float = 1.0
    corner_scale_span_deg: float = 5.0

# --- MASTER CONFIG (Das aggregierte JSON Objekt) ---
@dataclass
class MotorInputConfig:
    version: str = "1.5.0"
    topology: TopologyConfig = field(default_factory=TopologyConfig)
    mechanics: StatorMechanicsConfig = field(default_factory=StatorMechanicsConfig)
    coil: CoilLayoutConfig = field(default_factory=CoilLayoutConfig)
    stack: StackPcbConfig = field(default_factory=StackPcbConfig)
    rotor: RotorMagnetConfig = field(default_factory=RotorMagnetConfig)
    peripherals: PeripheralsConfig = field(default_factory=PeripheralsConfig)

    # Hier kommen später zwei winzige Helper-Funktionen rein:
    # def to_json(self) -> str: ...
    # @classmethod def from_json(cls, json_str: str) -> 'MotorInputConfig': ...
