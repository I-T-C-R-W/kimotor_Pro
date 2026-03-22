# KMotor_Pro Refactoring Dataflow Design

## Übersicht

Dieses Dokument beschreibt den Datenfluss vor und nach der Refaktorisierung, mit Fokus auf die zentrale Rolle von `MotorConfig.json` und die API-Schnittstelle.

## Zentrale Konzepte

### MotorConfig.json
- **Zentrale Eingabedatei** für alle Konfigurationsparameter
- **Datenmodell:** `kmotor_models.py` mit Dataclasses
- **Eingabepfade:**
  - GUI-Eingabe → MotorConfig.json
  - API-Aufruf → MotorConfig.json  
  - Direkte JSON-Datei
- **Ausgabepfade:**
  - Speichern als JSON
  - Laden aus JSON
  - Interoperabilität mit anderen Apps

### API-Schnittstelle
- **Zentrale Schnittstelle:** `kmotor_api.py`
- **Funktion:** Koordination zwischen Eingabe, Verarbeitung und Ausgabe
- **Methoden:**
  - `generate_motor(config: MotorConfig) -> Result`
  - `load_config(file_path: str) -> MotorConfig`
  - `save_config(config: MotorConfig, file_path: str)`

## Datenfluss vor der Refaktorisierung

```
GUI (kmotor_pro_gui.py)
    ↓
Plugin-Klasse (kmotor_pro_action.py)
    ↓
Direkte Methodenaufrufe
    ↓
KiCad-Rendering (pcbnew)
```

**Probleme:**
- Starke Kopplung zwischen GUI und Logik
- Keine klare Trennung von Verantwortlichkeiten
- Schwer testbar und wiederverwendbar

## Datenfluss nach der Refaktorisierung

### Phase 1: Eingabe und Validierung
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│      GUI        │    │       API        │    │  JSON-Datei     │
│ kmotor_gui.py   │    │ kmotor_api.py    │    │ MotorConfig.json│
└─────────┬───────┘    └─────────┬────────┘    └─────────┬───────┘
          │                      │                       │
          └──────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   MotorConfig.json      │
                    │    (zentrale Config)    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   kmotor_models.py      │
                    │   (Dataclasses)         │
                    └─────────────────────────┘
```

### Phase 2: Verarbeitung
```
┌─────────────────┐
│   kmotor_api.py │  ← Zentrale Schnittstelle
│   (API)         │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ kmotor_solver.py│  ← Geschäftslogik + Berechnungen
│   (Solver)      │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│kmotor_geometry.py│  ← Geometrie-Generation
│  (Geometry)     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ kmotor_kicad.py │  ← KiCad-Rendering
│   (Renderer)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   KiCad-PCB     │
└─────────────────┘
```

### Phase 3: Ausgabe
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   KiCad-PCB     │    │     SVG         │    │     DXF         │
│ kmotor_kicad.py │    │ kmotor_export.py│    │ kmotor_export.py│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Modul-Interaktionen

### kmotor_api.py (Zentrale Koordination)
```python
def generate_motor(config: MotorConfig) -> MotorResult:
    # 1. Validierung der Konfiguration
    validated_config = validate_config(config)
    
    # 2. Solver-Aufruf
    solver_result = kmotor_solver.solve(validated_config)
    
    # 3. Geometrie-Generation
    geometry_result = kmotor_geometry.generate(solver_result)
    
    # 4. Rendering
    pcb_result = kmotor_kicad.render(geometry_result)
    
    return pcb_result
```

### kmotor_solver.py (Geschäftslogik)
```python
def solve(config: MotorConfig) -> SolverResult:
    # Parameterberechnung
    parameters = calculate_parameters(config)
    
    # Spulen-Layout
    coil_layout = generate_coil_layout(parameters)
    
    # Validierung
    validate_layout(coil_layout)
    
    return SolverResult(parameters=parameters, layout=coil_layout)
```

### kmotor_geometry.py (Geometrie)
```python
def generate(solver_result: SolverResult) -> GeometryResult:
    # Punkt-Generierung
    points = generate_points(solver_result.parameters)
    
    # Pfad-Generierung
    paths = generate_paths(points, solver_result.layout)
    
    # Geometrie-Validierung
    validate_geometry(paths)
    
    return GeometryResult(points=points, paths=paths)
```

### kmotor_kicad.py (Rendering)
```python
def render(geometry_result: GeometryResult) -> PCBResult:
    # KiCad-Objekte erzeugen
    tracks = create_tracks(geometry_result.paths)
    vias = create_vias(geometry_result.points)
    
    # PCB-Gruppen erstellen
    group = create_group(tracks + vias)
    
    # PCB aktualisieren
    update_pcb(tracks, vias, group)
    
    return PCBResult(tracks=tracks, vias=vias, group=group)
```

## Datenklassen (kmotor_models.py)

### Core Dataclasses
```python
@dataclass
class MotorConfig:
    # Geometrische Parameter
    outer_radius: float
    inner_radius: float
    slot_count: int
    winding_layers: int
    
    # Elektrische Parameter
    voltage: float
    current: float
    turns_per_layer: int
    
    # Material-Parameter
    copper_thickness: float
    isolation_thickness: float
    
    # Konfiguration
    winding_mode: str  # 'parallel', 'radial', 'compact'
    magnet_shape: str  # 'rectangular', 'arc'
    terminal_type: str # 'pad', 'via'
```

### Result Dataclasses
```python
@dataclass
class SolverResult:
    parameters: dict
    layout: CoilLayout
    warnings: list[str]

@dataclass
class GeometryResult:
    points: list[Point]
    paths: list[Path]
    bounds: Rectangle

@dataclass
class PCBResult:
    tracks: list[Track]
    vias: list[Via]
    group: Group
    stats: dict
```

## Migration-Strategie

### Schritt 1: API-First Implementation
1. **kmotor_api.py** vollständig implementieren
2. **kmotor_models.py** Dataclasses finalisieren
3. **Test-Schnittstelle** für API bereitstellen

### Schritt 2: Modulweise Migration
1. **kmotor_solver.py** aus `kmotor_pro_action.py` extrahieren
2. **kmotor_geometry.py** aus `kmotor_pro_action.py` extrahieren
3. **kmotor_kicad.py** aus `kmotor_pro_action.py` extrahieren
4. **kmotor_gui.py** aus `kmotor_pro_gui.py` extrahieren

### Schritt 3: Integration und Testing
1. **API-Testing** mit verschiedenen MotorConfig.json Dateien
2. **Integration-Testing** der gesamten Pipeline
3. **Regression-Testing** gegen bestehende Designs

## Vorteile der neuen Architektur

### 1. Trennung von Verantwortlichkeiten
- **GUI:** Nur Eingabe und Anzeige
- **API:** Koordination und Schnittstelle
- **Solver:** Geschäftslogik
- **Geometry:** Mathematische Berechnungen
- **Renderer:** KiCad-Integration

### 2. Wiederverwendbarkeit
- **MotorConfig.json** kann von anderen Apps genutzt werden
- **API** kann für automatisierte Workflows verwendet werden
- **Module** können unabhängig getestet werden

### 3. Erweiterbarkeit
- **Neue Exportformate** (SVG, DXF) leicht hinzufügbar
- **Neue Solver-Strategien** durch Strategy-Pattern
- **Neue Geometrie-Formen** durch Factory-Pattern

### 4. Testbarkeit
- **Unit-Tests** für jedes Modul separat
- **Integration-Tests** der gesamten Pipeline
- **Mock-Tests** für KiCad-Abhängigkeiten

## Nächste Schritte

1. **Dataflow-Dokumentation** in diesem Dokument vervollständigen
2. **API-Spezifikation** detailliert ausarbeiten
3. **Erste Methode** aus `kmotor_pro_gui.py` in `kmotor_gui.py` verschieben
4. **Test-Workflow** für die neue Architektur aufbauen