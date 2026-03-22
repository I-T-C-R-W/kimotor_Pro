# KMotor_Pro API Specification

## Übersicht

Diese Spezifikation definiert die zentrale API-Schnittstelle für KMotor_Pro, die als Koordinationsstelle zwischen Eingabe, Verarbeitung und Ausgabe fungiert.

## API-Struktur

### Haupt-API: `kmotor_api.py`

#### Core Functions

```python
def generate_motor(config: MotorConfig) -> MotorResult:
    """
    Hauptfunktion zur Motor-Generierung.
    
    Args:
        config: MotorConfig mit allen notwendigen Parametern
        
    Returns:
        MotorResult mit Generierungsergebnis und Statistiken
        
    Raises:
        ValidationError: Bei ungültigen Konfigurationsparametern
        GeometryError: Bei Geometrie-Generierungsfehlern
        RenderError: Bei KiCad-Rendering-Fehlern
    """
    
def load_config(file_path: str) -> MotorConfig:
    """
    Lädt eine MotorConfig aus einer JSON-Datei.
    
    Args:
        file_path: Pfad zur JSON-Datei
        
    Returns:
        MotorConfig Objekt
        
    Raises:
        FileNotFoundError: Wenn Datei nicht existiert
        JSONDecodeError: Bei ungültigem JSON
        ValidationError: Bei ungültigen Konfigurationsdaten
    """
    
def save_config(config: MotorConfig, file_path: str) -> None:
    """
    Speichert eine MotorConfig in einer JSON-Datei.
    
    Args:
        config: Zu speicherndes MotorConfig Objekt
        file_path: Zielpfad für die JSON-Datei
        
    Raises:
        PermissionError: Bei fehlenden Schreibrechten
        IOError: Bei Datei-IO-Fehlern
    """
```

#### Utility Functions

```python
def validate_config(config: MotorConfig) -> MotorConfig:
    """
    Validiert und normalisiert eine MotorConfig.
    
    Args:
        config: Zu validierende MotorConfig
        
    Returns:
        Validierte und normalisierte MotorConfig
        
    Raises:
        ValidationError: Bei ungültigen Parametern
    """
    
def estimate_parameters(config: MotorConfig) -> dict:
    """
    Schätzt fehlende Parameter basierend auf gegebenen Werten.
    
    Args:
        config: MotorConfig mit teilweisen Parametern
        
    Returns:
        Dictionary mit geschätzten Parametern
    """
    
def get_supported_strategies() -> list[str]:
    """
    Gibt unterstützte Wicklungsstrategien zurück.
    
    Returns:
        Liste unterstützter Strategien
    """
    
def get_supported_magnet_shapes() -> list[str]:
    """
    Gibt unterstützte Magnetformen zurück.
    
    Returns:
        Liste unterstützter Magnetformen
    """
```

## Datenmodelle

### MotorConfig (Eingabe)

```python
@dataclass
class MotorConfig:
    # Geometrische Parameter
    outer_radius: float = 0.0      # Außenradius in mm
    inner_radius: float = 0.0      # Innenradius in mm
    slot_count: int = 0            # Anzahl der Slots
    winding_layers: int = 1        # Anzahl der Wicklungslayer
    
    # Elektrische Parameter
    voltage: float = 0.0           # Betriebsspannung in V
    current: float = 0.0           # Nennstrom in A
    turns_per_layer: int = 0       # Windungen pro Layer
    
    # Material-Parameter
    copper_thickness: float = 0.035  # Kupferdicke in mm
    isolation_thickness: float = 0.025  # Isolationsdicke in mm
    
    # Konfiguration
    winding_mode: str = 'parallel'     # 'parallel', 'radial', 'compact'
    magnet_shape: str = 'rectangular'  # 'rectangular', 'arc'
    terminal_type: str = 'pad'         # 'pad', 'via'
    
    # Optionale Parameter
    layer_count: int = 2               # Gesamtanzahl PCB-Layer
    via_diameter: float = 0.3          # Via-Durchmesser in mm
    track_width: float = 0.2           # Track-Breite in mm
    clearance: float = 0.15            # Clearance in mm
    
    def validate(self) -> None:
        """Validiert die Konfiguration"""
        # Implementierung der Validierung
        pass
        
    def normalize(self) -> 'MotorConfig':
        """Normalisiert die Konfiguration"""
        # Implementierung der Normalisierung
        pass
```

### MotorResult (Ausgabe)

```python
@dataclass
class MotorResult:
    # Generierungsergebnis
    success: bool
    message: str
    
    # Statistiken
    stats: dict
    
    # Geometrie-Informationen
    geometry: GeometryResult
    
    # KiCad-Informationen
    pcb: PCBResult
    
    # Warnungen und Fehler
    warnings: list[str]
    errors: list[str]
    
    def to_json(self) -> str:
        """Konvertiert das Result in JSON"""
        pass
        
    def save_to_file(self, file_path: str) -> None:
        """Speichert das Result in einer Datei"""
        pass
```

### GeometryResult

```python
@dataclass
class GeometryResult:
    points: list[Point]      # Generierte Punkte
    paths: list[Path]        # Generierte Pfade
    bounds: Rectangle        # Geometrie-Grenzen
    area: float             # Gesamtfläche
    
    def export_svg(self, file_path: str) -> None:
        """Exportiert Geometrie als SVG"""
        pass
        
    def export_dxf(self, file_path: str) -> None:
        """Exportiert Geometrie als DXF"""
        pass
```

### PCBResult

```python
@dataclass
class PCBResult:
    tracks: list[Track]      # Generierte Tracks
    vias: list[Via]          # Generierte Vias
    group: Group            # PCB-Gruppe
    stats: dict            # PCB-Statistiken
    
    def export_gerber(self, directory: str) -> None:
        """Exportiert PCB als Gerber-Dateien"""
        pass
        
    def export_gcode(self, file_path: str) -> None:
        """Exportiert PCB als GCode"""
        pass
```

## Fehlerbehandlung

### Custom Exceptions

```python
class KMotorError(Exception):
    """Base exception for KMotor errors"""
    pass

class ValidationError(KMotorError):
    """Raised when configuration validation fails"""
    pass

class GeometryError(KMotorError):
    """Raised when geometry generation fails"""
    pass

class RenderError(KMotorError):
    """Raised when KiCad rendering fails"""
    pass

class FileError(KMotorError):
    """Raised when file operations fail"""
    pass
```

### Error Handling Strategy

```python
def handle_validation_error(error: ValidationError) -> MotorResult:
    """Behandelt Validierungsfehler"""
    return MotorResult(
        success=False,
        message=f"Validation failed: {error}",
        warnings=[],
        errors=[str(error)],
        stats={},
        geometry=None,
        pcb=None
    )

def handle_geometry_error(error: GeometryError) -> MotorResult:
    """Behandelt Geometrie-Fehler"""
    return MotorResult(
        success=False,
        message=f"Geometry generation failed: {error}",
        warnings=[],
        errors=[str(error)],
        stats={},
        geometry=None,
        pcb=None
    )
```

## API-Beispiele

### Beispiel 1: Einfache Motor-Generierung

```python
from kmotor_api import generate_motor, MotorConfig

# Konfiguration erstellen
config = MotorConfig(
    outer_radius=20.0,
    inner_radius=10.0,
    slot_count=12,
    winding_layers=2,
    voltage=12.0,
    current=1.0,
    winding_mode='parallel'
)

# Motor generieren
result = generate_motor(config)

if result.success:
    print(f"Motor erfolgreich generiert!")
    print(f"Track-Länge: {result.stats['total_track_length']} mm")
    print(f"Widerstand: {result.stats['total_resistance']} Ohm")
else:
    print(f"Fehler: {result.message}")
    for error in result.errors:
        print(f"  - {error}")
```

### Beispiel 2: Konfiguration aus Datei laden

```python
from kmotor_api import load_config, generate_motor

# Konfiguration aus JSON laden
config = load_config("motor_config.json")

# Motor generieren
result = generate_motor(config)

# Ergebnis speichern
if result.success:
    result.save_to_file("motor_result.json")
```

### Beispiel 3: Parameter-Schätzung

```python
from kmotor_api import estimate_parameters, MotorConfig

# Teilweise Konfiguration
partial_config = MotorConfig(
    outer_radius=25.0,
    inner_radius=15.0,
    slot_count=16,
    voltage=24.0,
    current=2.0
)

# Fehlende Parameter schätzen
estimated_params = estimate_parameters(partial_config)

# Vollständige Konfiguration erstellen
full_config = MotorConfig(
    **partial_config.__dict__,
    **estimated_params
)

# Motor generieren
result = generate_motor(full_config)
```

## Integration mit anderen Modulen

### Modul-Dependencies

```python
# kmotor_api.py imports
from kmotor_models import MotorConfig, MotorResult
from kmotor_solver import solve
from kmotor_geometry import generate as geometry_generate
from kmotor_kicad import render as kicad_render
```

### API-Workflow

```python
def generate_motor_workflow(config: MotorConfig) -> MotorResult:
    """Kompletter Generierungs-Workflow"""
    
    # 1. Validierung
    validated_config = validate_config(config)
    
    # 2. Solver-Aufruf
    solver_result = solve(validated_config)
    
    # 3. Geometrie-Generation
    geometry_result = geometry_generate(solver_result)
    
    # 4. KiCad-Rendering
    pcb_result = kicad_render(geometry_result)
    
    # 5. Ergebnis zusammenstellen
    return MotorResult(
        success=True,
        message="Motor successfully generated",
        stats=calculate_stats(solver_result, geometry_result, pcb_result),
        geometry=geometry_result,
        pcb=pcb_result,
        warnings=solver_result.warnings,
        errors=[]
    )
```

## Performance-Anforderungen

### Performance-Ziele

- **Generierungszeit:** < 30 Sekunden für komplexe Designs (≥300 Slots)
- **Speicherverbrauch:** < 500 MB für große Designs
- **API-Antwortzeit:** < 1 Sekunde für einfache Validierungen

### Optimierungsstrategien

```python
# Caching für häufige Berechnungen
@lru_cache(maxsize=128)
def cached_geometry_calculation(params: tuple) -> GeometryResult:
    # Berechnung mit Caching
    pass

# Batch-Verarbeitung für mehrere Motoren
def batch_generate_motors(configs: list[MotorConfig]) -> list[MotorResult]:
    """Generiert mehrere Motoren gleichzeitig"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(generate_motor, configs))
    return results
```

## Test-API

### Test-Funktionen

```python
def test_api() -> bool:
    """Testet die gesamte API-Funktionalität"""
    try:
        # Test-Konfiguration
        test_config = MotorConfig(
            outer_radius=15.0,
            inner_radius=8.0,
            slot_count=8,
            winding_layers=1,
            voltage=5.0,
            current=0.5
        )
        
        # API-Test
        result = generate_motor(test_config)
        
        # Validierung
        assert result.success, "Motor generation should succeed"
        assert result.geometry is not None, "Geometry should be generated"
        assert result.pcb is not None, "PCB should be generated"
        
        return True
        
    except Exception as e:
        print(f"API test failed: {e}")
        return False

def benchmark_api() -> dict:
    """Benchmark der API-Performance"""
    import time
    
    test_configs = [
        MotorConfig(outer_radius=10.0, inner_radius=5.0, slot_count=i*10)
        for i in range(1, 11)
    ]
    
    times = []
    for config in test_configs:
        start_time = time.time()
        generate_motor(config)
        end_time = time.time()
        times.append(end_time - start_time)
    
    return {
        "slot_counts": [config.slot_count for config in test_configs],
        "times": times,
        "average_time": sum(times) / len(times)
    }
```

## Dokumentation und Support

### API-Dokumentation

- **Inline-Dokumentation:** Jede Funktion hat ausführliche Docstrings
- **Beispiele:** Praxisnahe Code-Beispiele für alle Hauptfunktionen
- **Fehlerbehandlung:** Klare Fehlermeldungen und Handhabungsstrategien

### Support-Funktionen

```python
def get_api_version() -> str:
    """Gibt die API-Version zurück"""
    return "1.0.0"

def get_supported_formats() -> dict:
    """Gibt unterstützte Dateiformate zurück"""
    return {
        "input": ["json"],
        "output": ["json", "svg", "dxf", "gerber", "gcode"]
    }

def get_system_info() -> dict:
    """Gibt Systeminformationen zurück"""
    import platform
    import sys
    
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "api_version": get_api_version()
    }
```

## Nächste Schritte

1. **API-Implementation** in `kmotor_api.py` basierend auf dieser Spezifikation
2. **Unit-Tests** für alle API-Funktionen
3. **Integration-Tests** mit den anderen Modulen
4. **Performance-Optimierung** basierend auf Benchmark-Ergebnissen
5. **Dokumentation** für Endbenutzer und Entwickler