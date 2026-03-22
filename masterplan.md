# KMotor_Pro Refactoring Masterplan

## Übersicht

Dieser Masterplan basiert auf der Analyse aller Helper-Dateien und definiert den systematischen Ablauf der Refaktorisierung. Er dient als zentrales Tracking-Tool und Leitfaden für die gesamte Umsetzung.

## Analyse der Helper-Dateien

### Key Insights aus den Dokumenten

**1. Ausgangsbasis (refactoring_status.md)**
- Alle neuen Module bereits vorhanden (14/14)
- 186 Methoden müssen aus 4 alten Dateien extrahiert werden
- Anti-Loop Rules etabliert
- Git-Status: `refactor-ai` Branch mit Commit `865cc3c`

**2. Methoden-Tracking (method_tracking.md)**
- **186 Methoden** aus 4 alten Dateien
- **kmotor_pro_action.py**: 131 Methoden (GUI, Logik, Geometrie, Rendering, Konfiguration)
- **kmotor_pro_gui.py**: 34 Methoden (reine GUI)
- **kmotor_pro_solver.py**: 3 Methoden (Solver-Strategien)
- **kmotor_pro_linalg.py**: 18 Methoden (mathematische Funktionen)

**3. Datenfluss-Design (dataflow_design.md)**
- **Zentrale Rolle**: `MotorConfig.json` als Eingabedatei
- **API-Schnittstelle**: `kmotor_api.py` als Koordinationsstelle
- **Klare Trennung**: GUI → API → Solver → Geometry → Renderer

**4. API-Spezifikation (api_specification.md)**
- **Hauptfunktion**: `generate_motor(config: MotorConfig) -> MotorResult`
- **Dataclasses**: `MotorConfig`, `MotorResult`, `GeometryResult`, `PCBResult`
- **Fehlerbehandlung**: Strukturierte Exceptions und Results

**5. Dataclass-Auswirkungen (data_model_impacts.md)**
- **Typ-Sicherheit**: Dataclasses gewährleisten korrekte Datentypen
- **Konsistenz**: Einheitliche Datenstrukturen über alle Module
- **Serialisierung**: Einfache JSON-Import/Export

## Masterplan-Struktur

### Phase 1: Vorbereitung (Tag 1)
**Ziel**: Setup und erste Methoden-Extraktion

#### Schritt 1.1: Setup und Validierung
- [ ] **Status-Check**: Alle neuen Module vorhanden ✓
- [ ] **Import-Test**: Basis-Imports funktionieren
- [ ] **Dataclass-Test**: `kmotor_models.py` funktioniert
- [ ] **API-Test**: `kmotor_api.py` Struktur validieren

#### Schritt 1.2: Erste GUI-Extraktion
- [ ] **Methode 1**: `kmotor_pro_gui.py.__init__` → `kmotor_gui.py`
- [ ] **Methode 2**: `kmotor_pro_gui.py._style_staticbox` → `kmotor_gui.py`
- [ ] **Methode 3**: `kmotor_pro_gui.py._reset_desc_font` → `kmotor_gui.py`
- [ ] **Methode 4**: `kmotor_pro_gui.py.__del__` → `kmotor_gui.py`
- [ ] **Methode 5**: `kmotor_pro_gui.py.on_close` → `kmotor_gui.py`

**Tracking**: Jede Methode in `method_tracking.md` als `In_Progress` markieren

#### Schritt 1.3: Validierung der ersten Phase
- [ ] **Import-Check**: Keine Cross-Dependencies
- [ ] **Funktions-Test**: GUI-Methoden arbeiten korrekt
- [ ] **Dokumentation**: Methoden-Tracking aktualisieren

### Phase 2: GUI-Modul (Tag 2)
**Ziel**: Komplette GUI-Extraktion

#### Schritt 2.1: kmotor_pro_gui.py vollständig extrahieren
- [ ] **Alle 34 Methoden** aus `kmotor_pro_gui.py` in `kmotor_gui.py` verschieben
- [ ] **Import-Struktur** bereinigen
- [ ] **Cross-Dependencies** entfernen

#### Schritt 2.2: GUI-Methoden aus kmotor_pro_action.py extrahieren
- [ ] **16 GUI-Methoden** aus `kmotor_pro_action.py` in `kmotor_gui.py` verschieben
- [ ] **Referenzen** in `kmotor_pro_action.py` entfernen
- [ ] **Event-Handler** neu verbinden

#### Schritt 2.3: GUI-Integration testen
- [ ] **Dialog-Initialisierung** funktioniert
- [ ] **Event-Handler** reagieren korrekt
- [ ] **Parameter-Übergabe** an API funktioniert

### Phase 3: Geschäftslogik (Tag 3-4)
**Ziel**: Solver-Logik extrahieren

#### Schritt 3.1: kmotor_pro_solver.py extrahieren
- [ ] **3 Solver-Methoden** (`parallel`, `radial`, `compact`) in `kmotor_solver.py`
- [ ] **Strategy-Pattern** implementieren

#### Schritt 3.2: Geschäftslogik aus kmotor_pro_action.py extrahieren
- [ ] **60 Geschäftslogik-Methoden** in `kmotor_solver.py` verschieben
- [ ] **Parameter-Validierung** implementieren
- [ ] **Fehlerbehandlung** strukturieren

#### Schritt 3.3: Solver-Integration testen
- [ ] **API-Schnittstelle** funktioniert
- [ ] **Parameter-Validierung** korrekt
- [ ] **Fehler-Rückgabe** strukturiert

### Phase 4: Geometrie-Modul (Tag 5)
**Ziel**: Geometrie-Logik extrahieren

#### Schritt 4.1: Geometrie-Methoden aus kmotor_pro_action.py extrahieren
- [ ] **25 Geometrie-Methoden** in `kmotor_geometry.py` verschieben
- [ ] **Punkt-Generierung** implementieren
- [ ] **Pfad-Generierung** implementieren

#### Schritt 4.2: Geometrie-Integration testen
- [ ] **Solver → Geometry** Schnittstelle funktioniert
- [ ] **Geometrie-Validierung** korrekt
- [ ] **Export-Funktionen** (SVG, DXF) funktionieren

### Phase 5: Mathematik-Modul (Tag 6)
**Ziel**: Mathematische Funktionen extrahieren

#### Schritt 5.1: kmotor_pro_linalg.py extrahieren
- [ ] **18 mathematische Methoden** in `kmotor_solvermath.py` verschieben
- [ ] **Vektor-Operationen** implementieren
- [ ] **Geometrie-Berechnungen** implementieren

#### Schritt 5.2: Mathematik-Integration testen
- [ ] **Geometry → Math** Schnittstelle funktioniert
- [ ] **Berechnungs-Genauigkeit** korrekt
- [ ] **Performance** akzeptabel

### Phase 6: Renderer-Modul (Tag 7-8)
**Ziel**: KiCad-Rendering extrahieren

#### Schritt 6.1: KiCad-Methoden aus kmotor_pro_action.py extrahieren
- [ ] **40 KiCad-Methoden** in `kmotor_kicad.py` verschieben
- [ ] **Track-Erzeugung** implementieren
- [ ] **Via-Erzeugung** implementieren
- [ ] **Group-Erzeugung** implementieren

#### Schritt 6.2: Renderer-Integration testen
- [ ] **Geometry → Renderer** Schnittstelle funktioniert
- [ ] **KiCad-Objekte** korrekt erzeugt
- [ ] **PCB-Gruppen** korrekt erstellt

### Phase 7: Konfiguration (Tag 9)
**Ziel**: Persistenz-Logik extrahieren

#### Schritt 7.1: Konfigurations-Methoden aus kmotor_pro_action.py extrahieren
- [ ] **13 Konfigurations-Methoden** in `kmotor_persist.py` verschieben
- [ ] **JSON-Import/Export** implementieren
- [ ] **Preset-Management** implementieren

#### Schritt 7.2: Konfigurations-Integration testen
- [ ] **MotorConfig.json** korrekt laden/speichern
- [ ] **Preset-Funktionen** funktionieren
- [ ] **Fehler-Logging** korrekt

### Phase 8: Integration & Testing (Tag 10-12)
**Ziel**: Komplette Integration und Testing

#### Schritt 8.1: End-to-End Testing
- [ ] **Komplette Pipeline** testen: GUI → API → Solver → Geometry → Renderer
- [ ] **Fehler-Szenarien** testen
- [ ] **Performance-Tests** durchführen

#### Schritt 8.2: Regression Testing
- [ ] **Bestehende Designs** mit neuer Architektur generieren
- [ ] **Ergebnis-Vergleich** mit alter Version
- [ ] **Kompatibilität** sicherstellen

#### Schritt 8.3: Dokumentation abschließen
- [ ] **method_tracking.md** vollständig aktualisieren
- [ ] **dataflow_design.md** finalisieren
- [ ] **api_specification.md** finalisieren

## Daily Tracking-System

### Täglicher Ablauf

#### Morning Standup (15 Minuten)
1. **Status-Update**: Was wurde gestern abgeschlossen?
2. **Ziel-Setzung**: Was soll heute erreicht werden?
3. **Blocker-Check**: Gibt es Hindernisse?

#### Midday Check (10 Minuten)
1. **Fortschritts-Check**: Läuft alles nach Plan?
2. **Problemlösung**: Gibt es unerwartete Herausforderungen?
3. **Anpassungen**: Muss der Plan angepasst werden?

#### Evening Review (15 Minuten)
1. **Ergebnis-Dokumentation**: Was wurde tatsächlich erreicht?
2. **Fehler-Logging**: Welche Probleme gab es und wie wurden sie gelöst?
3. **Plan-Update**: Was muss morgen priorisiert werden?

### Tracking-Tools

#### method_tracking.md als zentrales Tool
- **Status-Flags**: `Pending` → `In_Progress` → `Completed`
- **Fehler-Logging**: Detaillierte Notizen zu Problemen und Lösungen
- **Zeit-Tracking**: Aufwand für jede Methode dokumentieren

#### Helper-Dateien als Referenz
- **dataflow_design.md**: Datenfluss-Verständnis
- **api_specification.md**: Schnittstellen-Verständnis
- **data_model_impacts.md**: Dataclass-Verständnis

## Meilensteine und Checkpoints

### Milestone 1: GUI-Modul (Tag 2)
- [ ] **Alle 50 GUI-Methoden** extrahiert
- [ ] **GUI funktioniert** ohne Cross-Dependencies
- [ ] **Event-Handler** korrekt verbunden

### Milestone 2: Core Logic (Tag 4)
- [ ] **Solver-Logik** vollständig extrahiert
- [ ] **API-Schnittstelle** funktioniert
- [ ] **Parameter-Validierung** implementiert

### Milestone 3: Geometry & Math (Tag 6)
- [ ] **Geometrie-Logik** extrahiert
- [ ] **Mathematische Funktionen** extrahiert
- [ ] **Geometrie-Generation** funktioniert

### Milestone 4: Renderer (Tag 8)
- [ ] **KiCad-Rendering** extrahiert
- [ ] **PCB-Erzeugung** funktioniert
- [ ] **Gruppen-Erzeugung** funktioniert

### Milestone 5: Integration (Tag 12)
- [ ] **Komplette Pipeline** funktioniert
- [ ] **End-to-End Tests** bestanden
- [ ] **Regression Tests** bestanden

## Risikomanagement

### Hohe Risiken

#### 1. Cross-Dependencies
**Risiko**: Versteckte Abhängigkeiten zwischen Modulen
**Mitigation**: Systematisches Import-Testing nach jeder Phase
**Checkpoint**: Täglicher Import-Check

#### 2. Datenverlust
**Risiko**: Methoden verlieren wichtige Logik beim Verschieben
**Mitigation**: Detaillierte Dokumentation in method_tracking.md
**Checkpoint**: Jede Methode vor/nach dem Verschieben testen

#### 3. Performance-Regression
**Risiko**: Neue Architektur ist langsamer als alte
**Mitigation**: Performance-Benchmarks in jeder Phase
**Checkpoint**: Tägliche Performance-Tests

### Mittlere Risiken

#### 1. Fehlende Methoden
**Risiko**: Methoden werden beim Zählen übersehen
**Mitigation**: Systematische Durchsicht aller alten Dateien
**Checkpoint**: Abschluss-Check nach jeder Phase

#### 2. Falsche Zuordnung
**Risiko**: Methoden werden in falsche Module verschoben
**Mitigation**: Klare Kriterien für Modul-Zuordnung
**Checkpoint**: Peer-Review der Zuordnungen

## Erfolgskriterien

### Technische Kriterien
- [ ] **Keine Cross-Dependencies** zwischen Modulen
- [ ] **Alle 186 Methoden** korrekt zugeordnet
- [ ] **API-Schnittstelle** funktioniert einwandfrei
- [ ] **Performance** mindestens gleich gut wie vorher

### Qualitätskriterien
- [ ] **Code-Qualität**: Keine Duplikationen, klare Trennung
- [ ] **Testbarkeit**: Jedes Modul einzeln testbar
- [ ] **Dokumentation**: Alle Änderungen dokumentiert
- [ ] **Wartbarkeit**: Neue Entwickler können Module verstehen

### Funktionskriterien
- [ ] **Komplette Funktionalität** erhalten
- [ ] **Keine Regressionen** in bestehenden Designs
- [ ] **Erweiterbarkeit** für zukünftige Features
- [ ] **Interoperabilität** mit anderen Anwendungen

## Nächste Schritte

1. **Phase 1 starten**: Beginne mit Setup und Validierung
2. **Erste Methode extrahieren**: `kmotor_pro_gui.py.__init__`
3. **method_tracking.md aktualisieren**: Status auf `In_Progress` setzen
4. **Daily Standup einrichten**: Regelmäßige Fortschrittskontrolle

**Wichtig**: Jeder Schritt muss dokumentiert und getestet werden, bevor der nächste begonnen wird!