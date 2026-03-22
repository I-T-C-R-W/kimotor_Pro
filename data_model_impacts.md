# KMotor_Pro Data Model Impacts

## Übersicht

Diese Dokumentation beschreibt die Auswirkungen der neuen zentralen Datenmodelle (`kmotor_models.py`) auf die gesamte KMotor_Pro Architektur.

## Datenmodell-Übersicht

### Core Dataclasses

#### MotorConfig
```python
@dataclass
class MotorConfig:
    # Geometrische Parameter
    outer_radius: float = 0.0
    inner_radius: float = 0.0
    slot_count: int = 0
    winding_layers: int = 1
    
    # Elektrische Parameter
    voltage: float = 0.0
    current: float = 0.0
    turns_per_layer: int = 0
    
    # Material-Parameter
    copper_thickness: float = 0.035
    isolation_thickness: float = 0.025
    
    # Konfiguration
    winding_mode: str = 'parallel'
    magnet_shape: str = 'rectangular'
    terminal_type: str = 'pad'
    
    # Optionale Parameter
    layer_count: int = 2
    via_diameter: float = 0.3
    track_width: float = 0.2
    clearance: float = 0.15
```

#### MotorResult
```python
@dataclass
class MotorResult:
    success: bool
    message: str
    stats: dict
    geometry: GeometryResult
    pcb: PCBResult
    warnings: list[str]
    errors: list[str]
```

#### GeometryResult
```python
@dataclass
class GeometryResult:
    points: list[Point]
    paths: list[Path]
    bounds: Rectangle
    area: float
```

#### PCBResult
```python
@dataclass
class PCBResult:
    tracks: list[Track]
    vias: list[Via]
    group: Group
    stats: dict
```

## Auswirkungen auf Module

### 1. GUI-Module (`kmotor_gui.py`)

#### Aktuelle Situation
- Direkte Widget-Interaktion mit lokalen Variablen
- Keine zentrale Konfigurationsverwaltung
- Manuelle Parameter-Übergabe

#### Neue Architektur
```python
class MotorGUI:
    def __init__(self):
        self.config = MotorConfig()  # Zentrale Konfiguration
        
    def on_parameter_change(self, widget, value):
        # Direkte Aktualisierung der Dataclass
        field_name = self._get_field_name(widget)
        setattr(self.config, field_name, value)
        
    def get_config(self) -> MotorConfig:
        return self.config
        
    def set_config(self, config: MotorConfig):
        self.config = config
        self._update_ui_from_config()
```

#### Vorteile
- **Zentrale Konfiguration:** Ein einziges Objekt für alle Parameter
- **Typ-Sicherheit:** Dataclass-Validierung und IDE-Unterstützung
- **Einfache Serialisierung:** JSON-Export/Import durch Dataclass
- **Konsistente Validierung:** Einheitliche Validierungslogik

### 2. Solver-Module (`kmotor_solver.py`)

#### Aktuelle Situation
- Parameter werden als einzelne Argumente übergeben
- Keine klare Trennung von Eingabe- und Ausgabedaten
- Komplexe Rückgabewerte als Tupel/Dictionaries

#### Neue Architektur
```python
def solve(config: MotorConfig) -> SolverResult:
    # Eingabe: Einziges, klar definiertes Konfigurationsobjekt
    validated_config = validate_config(config)
    
    # Berechnungen mit typsicheren Daten
    parameters = calculate_parameters(validated_config)
    layout = generate_coil_layout(parameters)
    
    # Rückgabe: Strukturiertes Ergebnisobjekt
    return SolverResult(
        parameters=parameters,
        layout=layout,
        warnings=collect_warnings()
    )
```

#### Vorteile
- **Klare Schnittstelle:** Eindeutige Eingabe- und Ausgabeformate
- **Fehlertoleranz:** Strukturierte Rückgabe von Warnungen und Fehlern
- **Erweiterbarkeit:** Neue Parameter einfach hinzufügbar
- **Testbarkeit:** Einfache Mocking von Konfigurationsobjekten

### 3. Geometry-Module (`kmotor_geometry.py`)

#### Aktuelle Situation
- Geometrie-Daten als primitive Typen (Listen, Tupel)
- Keine klare Struktur für komplexe Geometrie-Informationen
- Schwierige Rückverfolgbarkeit von Geometrie-Elementen

#### Neue Architektur
```python
def generate(solver_result: SolverResult) -> GeometryResult:
    # Typsichere Eingabeverarbeitung
    parameters = solver_result.parameters
    layout = solver_result.layout
    
    # Strukturierte Geometrie-Generierung
    points = generate_points(parameters)
    paths = generate_paths(points, layout)
    bounds = calculate_bounds(points)
    
    return GeometryResult(
        points=points,
        paths=paths,
        bounds=bounds,
        area=calculate_area(paths)
    )
```

#### Vorteile
- **Strukturierte Geometrie:** Klare Organisation von Punkten, Pfaden und Metadaten
- **Wiederverwendbarkeit:** Geometrie kann unabhängig von KiCad genutzt werden
- **Export-Fähigkeit:** Einfache Konvertierung zu SVG/DXF durch strukturierte Daten
- **Validierung:** Geometrie kann leicht auf Konsistenz geprüft werden

### 4. Renderer-Module (`kmotor_kicad.py`)

#### Aktuelle Situation
- Direkte KiCad-Objekterzeugung aus primitiven Daten
- Keine Trennung von Geometrie und Rendering-Logik
- Schwierige Testbarkeit der Rendering-Funktionen

#### Neue Architektur
```python
def render(geometry_result: GeometryResult) -> PCBResult:
    # Typsichere Geometrie-Verarbeitung
    points = geometry_result.points
    paths = geometry_result.paths
    
    # Strukturierte KiCad-Objekterzeugung
    tracks = create_tracks_from_paths(paths)
    vias = create_vias_from_points(points)
    group = create_group(tracks + vias)
    
    return PCBResult(
        tracks=tracks,
        vias=vias,
        group=group,
        stats=calculate_pcb_stats(tracks, vias)
    )
```

#### Vorteile
- **Trennung von Anliegen:** Geometrie vs. KiCad-Rendering
- **Testbarkeit:** Rendering kann mit Mock-Geometrie getestet werden
- **Flexibilität:** Unterschiedliche Renderer für verschiedene Ausgabeformate
- **Konsistenz:** Einheitliche PCB-Ergebnisstruktur

## Abhängigkeits-Änderungen

### Vor der Refaktorisierung
```
GUI → (viele Einzelparameter) → Solver
Solver → (primitive Daten) → Geometry  
Geometry → (primitive Daten) → Renderer
```

### Nach der Refaktorisierung
```
GUI → MotorConfig → API → Solver → SolverResult → Geometry → GeometryResult → Renderer → PCBResult
```

### Neue Abhängigkeiten

#### Module, die `kmotor_models.py` benötigen
- **Alle Module** importieren die Dataclasses
- **API-Modul** als zentrale Schnittstelle
- **GUI-Modul** für Konfigurationsverwaltung
- **Solver-Modul** für Eingabe/Ausgabe
- **Geometry-Modul** für strukturierte Daten
- **Renderer-Modul** für PCB-Ergebnisse

#### Entfallende Cross-Dependencies
- **Keine direkten GUI-Solver-Abhängigkeiten**
- **Keine direkten Geometry-Renderer-Abhängigkeiten**
- **Keine primitiven Daten-Übergaben zwischen Modulen**

## API-Änderungen

### Methoden-Signaturen

#### Vorher
```python
def generate_motor(
    outer_radius, inner_radius, slot_count, winding_layers,
    voltage, current, turns_per_layer, copper_thickness,
    isolation_thickness, winding_mode, magnet_shape, terminal_type
):
    # Komplexe Parameterliste
    pass
```

#### Nachher
```python
def generate_motor(config: MotorConfig) -> MotorResult:
    # Eindeutige, typsichere Schnittstelle
    pass
```

### Fehlerbehandlung

#### Vorher
```python
def some_function():
    if error_condition:
        raise Exception("Error message")
    # Keine strukturierte Fehler-Rückgabe
```

#### Nachher
```python
def some_function(config: MotorConfig) -> MotorResult:
    if error_condition:
        return MotorResult(
            success=False,
            message="Error description",
            errors=["Detailed error info"],
            warnings=[],
            stats={},
            geometry=None,
            pcb=None
        )
```

## Serialisierung und Persistenz

### JSON-Export/Import

#### Konfiguration speichern
```python
import json

def save_config(config: MotorConfig, file_path: str):
    with open(file_path, 'w') as f:
        json.dump(config.__dict__, f, indent=2)

def load_config(file_path: str) -> MotorConfig:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return MotorConfig(**data)
```

#### Ergebnisse speichern
```python
def save_result(result: MotorResult, file_path: str):
    # Custom JSON encoder für komplexe Objekte
    with open(file_path, 'w') as f:
        json.dump(result.to_dict(), f, indent=2)
```

### Interoperabilität

#### Andere Anwendungen
```python
# Externe Anwendung kann MotorConfig.json laden
import json

def load_external_config(file_path: str) -> MotorConfig:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return MotorConfig(**data)

# Und direkt mit KMotor_Pro API verwenden
result = generate_motor(load_external_config("external_config.json"))
```

## Performance-Implikationen

### Vorteile
- **Reduzierte Kopieroperationen:** Dataclasses sind effizient
- **Bessere Caching-Möglichkeiten:** Strukturierte Daten leichter zu cachen
- **Optimierte Validierung:** Einmalige Validierung der gesamten Konfiguration

### Nachteile
- **Leichter Overhead:** Dataclass-Objekte vs. primitive Typen
- **Speicherbedarf:** Zusätzliche Metadaten in Dataclasses

### Optimierungsstrategien
```python
# Frozen Dataclasses für unveränderliche Konfigurationen
@dataclass(frozen=True)
class MotorConfig:
    # ...

# Slots für reduzierten Speicherbedarf
@dataclass
class Point:
    __slots__ = ['x', 'y']
    x: float
    y: float
```

## Migration-Strategie

### Phase 1: Dataclass-Integration
1. **Bestehende Parameter** in Dataclasses umwandeln
2. **Backward-Compatibility** durch Wrapper-Funktionen sicherstellen
3. **Unit-Tests** für neue Dataclass-Struktur schreiben

### Phase 2: Modul-Übergänge
1. **GUI-Module** auf MotorConfig umstellen
2. **Solver-Module** auf strukturierte Rückgaben umstellen
3. **Geometry-Module** auf typsichere Daten umstellen
4. **Renderer-Module** auf PCBResult umstellen

### Phase 3: API-Vereinheitlichung
1. **Alle API-Funktionen** auf neue Dataclass-Schnittstellen umstellen
2. **Alte Schnittstellen** deprecaten und entfernen
3. **Dokumentation** der neuen Architektur aktualisieren

## Teststrategie

### Unit-Tests für Dataclasses
```python
def test_motor_config_validation():
    # Teste Validierung von MotorConfig
    config = MotorConfig(outer_radius=-1.0)  # Ungültiger Wert
    with pytest.raises(ValidationError):
        config.validate()

def test_geometry_result_export():
    # Teste Export-Funktionalität
    geometry = GeometryResult(points=[], paths=[], bounds=Rectangle(0,0,10,10), area=100)
    geometry.export_svg("test.svg")
    assert os.path.exists("test.svg")
```

### Integration-Tests
```python
def test_complete_workflow():
    # Teste kompletten Workflow mit Dataclasses
    config = MotorConfig(
        outer_radius=20.0,
        inner_radius=10.0,
        slot_count=12
    )
    
    result = generate_motor(config)
    
    assert result.success
    assert result.geometry is not None
    assert result.pcb is not None
    assert len(result.warnings) >= 0
```

## Zusammenfassung

Die Einführung zentraler Dataclasses hat tiefgreifende Auswirkungen auf die gesamte KMotor_Pro Architektur:

### Vorteile
- **Typ-Sicherheit:** Dataclasses gewährleisten korrekte Datentypen
- **Konsistenz:** Einheitliche Datenstrukturen über alle Module
- **Wartbarkeit:** Klare Schnittstellen und Trennung von Anliegen
- **Erweiterbarkeit:** Einfaches Hinzufügen neuer Parameter und Funktionen
- **Interoperabilität:** Einfache Integration mit anderen Anwendungen

### Herausforderungen
- **Migration-Aufwand:** Umstellung bestehender Code auf neue Strukturen
- **Lernkurve:** Entwickler müssen Dataclass-Konzepte verstehen
- **Performance-Überwachung:** Neue Datenstrukturen auf Performance prüfen

### Nächste Schritte
1. **Dataclass-Implementation** in `kmotor_models.py` finalisieren
2. **API-Schnittstellen** auf neue Dataclass-Struktur umstellen
3. **Module-spezifische** Anpassungen planen und implementieren
4. **Test-Strategie** für neue Architektur entwickeln