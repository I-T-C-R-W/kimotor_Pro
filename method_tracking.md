# Method Tracking for KMotor_Pro Refactoring

## Tracking Format
```
Methode: [Name]
Quelle: [Datei:Zeile_von-Zeile_bis]
Ziel: [Neue_Datei]
Funktion: [Kurzbeschreibung was sie macht]
Änderungen: [Imports, Namen, Dependencies]
Status: [Pending/In_Progress/Completed]
Ergebnis: [Fehler/Success - detaillierte Notizen]
```

## GUI-Methoden (kmotor_gui.py)

### kmotor_pro_gui.py Methoden

#### Methode: __init__
Quelle: kmotor_pro_gui.py:1-50
Ziel: kmotor_gui.py
Funktion: Haupt-Dialog-Initialisierung
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: _style_staticbox
Quelle: kmotor_pro_gui.py:51-60
Ziel: kmotor_gui.py
Funktion: StaticBox stylen
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: _reset_desc_font
Quelle: kmotor_pro_gui.py:61-70
Ziel: kmotor_gui.py
Funktion: Beschreibungs-Font zurücksetzen
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: __del__
Quelle: kmotor_pro_gui.py:71-80
Ziel: kmotor_gui.py
Funktion: GUI bereinigen
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_close
Quelle: kmotor_pro_gui.py:81-90
Ziel: kmotor_gui.py
Funktion: Schließen-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_cb_outline
Quelle: kmotor_pro_gui.py:91-100
Ziel: kmotor_gui.py
Funktion: Outline-Change-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_cb_mholes
Quelle: kmotor_pro_gui.py:101-110
Ziel: kmotor_gui.py
Funktion: Montage-Löcher-Change-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_cb_preset
Quelle: kmotor_pro_gui.py:111-120
Ziel: kmotor_gui.py
Funktion: Preset-Change-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_nr_layers
Quelle: kmotor_pro_gui.py:121-130
Ziel: kmotor_gui.py
Funktion: Layer-Change-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_cb_trmtype
Quelle: kmotor_pro_gui.py:131-140
Ziel: kmotor_gui.py
Funktion: Terminal-Typ-Change-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_cb_winding_mode
Quelle: kmotor_pro_gui.py:141-150
Ziel: kmotor_gui.py
Funktion: Wicklungs-Modus-Change-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_cb_magnet_shape
Quelle: kmotor_pro_gui.py:151-160
Ziel: kmotor_gui.py
Funktion: Magnet-Form-Change-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_btn_load
Quelle: kmotor_pro_gui.py:161-170
Ziel: kmotor_gui.py
Funktion: Laden-Button-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_btn_save
Quelle: kmotor_pro_gui.py:171-180
Ziel: kmotor_gui.py
Funktion: Speichern-Button-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_btn_clear
Quelle: kmotor_pro_gui.py:181-190
Ziel: kmotor_gui.py
Funktion: Löschen-Button-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_btn_generate_magnet
Quelle: kmotor_pro_gui.py:191-200
Ziel: kmotor_gui.py
Funktion: Magnet-Generieren-Button-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_btn_generate_both
Quelle: kmotor_pro_gui.py:201-210
Ziel: kmotor_gui.py
Funktion: Beides-Generieren-Button-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: on_btn_generate
Quelle: kmotor_pro_gui.py:211-220
Ziel: kmotor_gui.py
Funktion: Generieren-Button-Handler
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: _apply_pcb_preset
Quelle: kmotor_pro_gui.py:221-230
Ziel: kmotor_gui.py
Funktion: PCB-Preset anwenden
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

### kmotor_pro_action.py GUI-Methoden

#### Methode: __init__
Quelle: kmotor_pro_action.py:1-100
Ziel: kmotor_gui.py
Funktion: Haupt-Dialog-Initialisierung
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_close
Quelle: kmotor_pro_action.py:1000-1010
Ziel: kmotor_gui.py
Funktion: Dialog-Schließen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_btn_clear
Quelle: kmotor_pro_action.py:1100-1110
Ziel: kmotor_gui.py
Funktion: Eingaben löschen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_btn_generate
Quelle: kmotor_pro_action.py:1200-1210
Ziel: kmotor_gui.py
Funktion: Motor generieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_btn_generate_magnet
Quelle: kmotor_pro_action.py:1300-1310
Ziel: kmotor_gui.py
Funktion: Magnet-PCB generieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_btn_generate_both
Quelle: kmotor_pro_action.py:1400-1410
Ziel: kmotor_gui.py
Funktion: Beides generieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_btn_save
Quelle: kmotor_pro_action.py:1500-1510
Ziel: kmotor_gui.py
Funktion: Konfiguration speichern
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_btn_load
Quelle: kmotor_pro_action.py:1600-1610
Ziel: kmotor_gui.py
Funktion: Konfiguration laden
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_cb_preset
Quelle: kmotor_pro_action.py:1700-1710
Ziel: kmotor_gui.py
Funktion: PCB-Preset auswählen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_cb_outline
Quelle: kmotor_pro_action.py:1800-1810
Ziel: kmotor_gui.py
Funktion: Outline-Typ ändern
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_cb_trmtype
Quelle: kmotor_pro_action.py:1900-1910
Ziel: kmotor_gui.py
Funktion: Terminal-Typ ändern
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_cb_winding_mode
Quelle: kmotor_pro_action.py:2000-2010
Ziel: kmotor_gui.py
Funktion: Wicklungs-Modus ändern
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_cb_magnet_shape
Quelle: kmotor_pro_action.py:2100-2110
Ziel: kmotor_gui.py
Funktion: Magnet-Form ändern
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_cb_mholes
Quelle: kmotor_pro_action.py:2200-2210
Ziel: kmotor_gui.py
Funktion: Montage-Löcher ändern
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: on_nr_layers
Quelle: kmotor_pro_action.py:2300-2310
Ziel: kmotor_gui.py
Funktion: Layer-Anzahl ändern
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _apply_config_to_gui
Quelle: kmotor_pro_action.py:2400-2410
Ziel: kmotor_gui.py
Funktion: Konfiguration auf GUI übertragen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

## Geschäftslogik (kmotor_solver.py)

### kmotor_pro_solver.py Methoden

#### Methode: parallel
Quelle: kmotor_pro_solver.py:1-20
Ziel: kmotor_solver.py
Funktion: Parallele Strategie
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: radial
Quelle: kmotor_pro_solver.py:21-40
Ziel: kmotor_solver.py
Funktion: Radiale Strategie
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: compact
Quelle: kmotor_pro_solver.py:41-60
Ziel: kmotor_solver.py
Funktion: Kompakte Strategie
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

### kmotor_pro_action.py Geschäftslogik-Methoden

#### Methode: get_parameters
Quelle: kmotor_pro_action.py:3000-3050
Ziel: kmotor_solver.py
Funktion: Parameter extrahieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _effective_winding_layers
Quelle: kmotor_pro_action.py:3100-3150
Ziel: kmotor_solver.py
Funktion: Effektive Wicklungs-Layer berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _winding_pitch_mm
Quelle: kmotor_pro_action.py:3200-3250
Ziel: kmotor_solver.py
Funktion: Wicklungs-Pitch berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _estimate_turns_per_layer
Quelle: kmotor_pro_action.py:3300-3350
Ziel: kmotor_solver.py
Funktion: Windungen pro Layer schätzen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: validate_parameters
Quelle: kmotor_pro_action.py:3400-3450
Ziel: kmotor_solver.py
Funktion: Parameter validieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: get_magnet_parameters
Quelle: kmotor_pro_action.py:3500-3550
Ziel: kmotor_solver.py
Funktion: Magnet-Parameter extrahieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: validate_magnet_parameters
Quelle: kmotor_pro_action.py:3600-3650
Ziel: kmotor_solver.py
Funktion: Magnet-Parameter validieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _update_magnet_summary
Quelle: kmotor_pro_action.py:3700-3750
Ziel: kmotor_solver.py
Funktion: Magnet-Zusammenfassung aktualisieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: estimate_motor_constants
Quelle: kmotor_pro_action.py:3800-3850
Ziel: kmotor_solver.py
Funktion: Motor-Konstanten schätzen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: estimate_winding_factor
Quelle: kmotor_pro_action.py:3900-3950
Ziel: kmotor_solver.py
Funktion: Wicklungsfaktor schätzen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: estimate_performance_stats
Quelle: kmotor_pro_action.py:4000-4050
Ziel: kmotor_solver.py
Funktion: Leistungs-Statistik schätzen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: estimate_model_warnings
Quelle: kmotor_pro_action.py:4100-4150
Ziel: kmotor_solver.py
Funktion: Modell-Warnungen schätzen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: get_effective_coil_strategy
Quelle: kmotor_pro_action.py:4200-4250
Ziel: kmotor_solver.py
Funktion: Effektive Spulen-Strategie ermitteln
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: generate_magnet_pcb
Quelle: kmotor_pro_action.py:4300-4350
Ziel: kmotor_solver.py
Funktion: Magnet-PCB generieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: generate
Quelle: kmotor_pro_action.py:4400-4450
Ziel: kmotor_solver.py
Funktion: Haupt-Generierungsfunktion
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: coil_tracker
Quelle: kmotor_pro_action.py:4500-4550
Ziel: kmotor_solver.py
Funktion: Spulen-Tracker
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: mpt_point
Quelle: kmotor_pro_action.py:4600-4650
Ziel: kmotor_solver.py
Funktion: MPT-Punkt berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: do_coils
Quelle: kmotor_pro_action.py:4700-4750
Ziel: kmotor_solver.py
Funktion: Spulen erstellen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: build_slot_anchors
Quelle: kmotor_pro_action.py:4800-4850
Ziel: kmotor_solver.py
Funktion: Slot-Anker bauen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: build_slot_center_via
Quelle: kmotor_pro_action.py:4900-4950
Ziel: kmotor_solver.py
Funktion: Slot-Mitte-Via bauen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: collect
Quelle: kmotor_pro_action.py:5000-5050
Ziel: kmotor_solver.py
Funktion: Sammel-Funktion
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: discrete_centerline_radii
Quelle: kmotor_pro_action.py:5100-5150
Ziel: kmotor_solver.py
Funktion: Diskrete Mittellinien-Radius berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: add_through_via
Quelle: kmotor_pro_action.py:5200-5250
Ziel: kmotor_solver.py
Funktion: Durchkontaktierung hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: add_custom_through_via
Quelle: kmotor_pro_action.py:5300-5350
Ziel: kmotor_solver.py
Funktion: Custom Durchkontaktierung hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: add_support_hole
Quelle: kmotor_pro_action.py:5400-5450
Ziel: kmotor_solver.py
Funktion: Stützloch hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: get_support_hole_width
Quelle: kmotor_pro_action.py:5500-5550
Ziel: kmotor_solver.py
Funktion: Stützloch-Breite berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: get_selected_terminal_od_iu
Quelle: kmotor_pro_action.py:5600-5650
Ziel: kmotor_solver.py
Funktion: Terminal-OD berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: estimate_safe_inner_fill_radius
Quelle: kmotor_pro_action.py:5700-5750
Ziel: kmotor_solver.py
Funktion: Sicherer Innen-Füll-Radius schätzen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: hole_collides
Quelle: kmotor_pro_action.py:5800-5850
Ziel: kmotor_solver.py
Funktion: Loch-Kollision prüfen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: do_professional_routing
Quelle: kmotor_pro_action.py:5900-5950
Ziel: kmotor_solver.py
Funktion: Professionelles Routing
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: add_ring_path
Quelle: kmotor_pro_action.py:6000-6050
Ziel: kmotor_solver.py
Funktion: Ring-Pfad hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: get_slot_start
Quelle: kmotor_pro_action.py:6100-6150
Ziel: kmotor_solver.py
Funktion: Slot-Start berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: segs_intersect
Quelle: kmotor_pro_action.py:6200-6250
Ziel: kmotor_solver.py
Funktion: Segment-Schnittpunkt prüfen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: orient
Quelle: kmotor_pro_action.py:6300-6350
Ziel: kmotor_solver.py
Funktion: Orientierung berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: do_outline
Quelle: kmotor_pro_action.py:6400-6450
Ziel: kmotor_solver.py
Funktion: Outline erstellen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: do_mounting_holes
Quelle: kmotor_pro_action.py:6500-6550
Ziel: kmotor_solver.py
Funktion: Montage-Löcher erstellen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: do_thermal_zones
Quelle: kmotor_pro_action.py:6600-6650
Ziel: kmotor_solver.py
Funktion: Thermische Zonen erstellen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: do_silkscreen
Quelle: kmotor_pro_action.py:6700-6750
Ziel: kmotor_solver.py
Funktion: Silkscreen erstellen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: calculate_stats_breakdown
Quelle: kmotor_pro_action.py:6800-6850
Ziel: kmotor_solver.py
Funktion: Statistik-Details berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: calculate_stats
Quelle: kmotor_pro_action.py:6900-6950
Ziel: kmotor_solver.py
Funktion: Statistik berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

## Geometrie-Methoden (kmotor_geometry.py)

### kmotor_pro_action.py Geometrie-Methoden

#### Methode: _point_xy
Quelle: kmotor_pro_action.py:7000-7050
Ziel: kmotor_geometry.py
Funktion: Punkt-Koordinaten berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _as_point
Quelle: kmotor_pro_action.py:7100-7150
Ziel: kmotor_geometry.py
Funktion: Als Punkt konvertieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _radial_vector
Quelle: kmotor_pro_action.py:7200-7250
Ziel: kmotor_geometry.py
Funktion: Radial-Vektor berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _tangent_vector
Quelle: kmotor_pro_action.py:7300-7350
Ziel: kmotor_geometry.py
Funktion: Tangential-Vektor berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _point_radius
Quelle: kmotor_pro_action.py:7400-7450
Ziel: kmotor_geometry.py
Funktion: Punkt-Radius berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _nearest_point_distance
Quelle: kmotor_pro_action.py:7500-7550
Ziel: kmotor_geometry.py
Funktion: Nächste Punkt-Distanz berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _get_outline_outer_radius
Quelle: kmotor_pro_action.py:7600-7650
Ziel: kmotor_geometry.py
Funktion: Outline-Außen-Radius berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _get_outline_corners
Quelle: kmotor_pro_action.py:7700-7750
Ziel: kmotor_geometry.py
Funktion: Outline-Ecken berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _get_outline_bounds
Quelle: kmotor_pro_action.py:7800-7850
Ziel: kmotor_geometry.py
Funktion: Outline-Grenzen berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _clip_segment_to_outline_box
Quelle: kmotor_pro_action.py:7900-7950
Ziel: kmotor_geometry.py
Funktion: Segment an Outline-Box clippen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _rotate_xy
Quelle: kmotor_pro_action.py:8000-8050
Ziel: kmotor_geometry.py
Funktion: XY rotieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _rotate_about_xy
Quelle: kmotor_pro_action.py:8100-8150
Ziel: kmotor_geometry.py
Funktion: XY um Punkt rotieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _offset_xy
Quelle: kmotor_pro_action.py:8200-8250
Ziel: kmotor_geometry.py
Funktion: XY verschieben
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _get_board_span
Quelle: kmotor_pro_action.py:8300-8350
Ziel: kmotor_geometry.py
Funktion: Board-Span berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _get_magnet_board_origin
Quelle: kmotor_pro_action.py:8400-8450
Ziel: kmotor_geometry.py
Funktion: Magnet-Board-Orig berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _get_pcb_text_position
Quelle: kmotor_pro_action.py:8500-8550
Ziel: kmotor_geometry.py
Funktion: PCB-Text-Position berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _get_bottom_right_info_anchor
Quelle: kmotor_pro_action.py:8600-8650
Ziel: kmotor_geometry.py
Funktion: Info-Anker berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _get_terminal_label_position
Quelle: kmotor_pro_action.py:8700-8750
Ziel: kmotor_geometry.py
Funktion: Terminal-Label-Position berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _outline_poly_points
Quelle: kmotor_pro_action.py:8800-8850
Ziel: kmotor_geometry.py
Funktion: Outline-Polygon-Punkte berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: to_xy
Quelle: kmotor_pro_action.py:8900-8950
Ziel: kmotor_geometry.py
Funktion: Zu XY konvertieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: as_inset_point
Quelle: kmotor_pro_action.py:9000-9050
Ziel: kmotor_geometry.py
Funktion: Als Insets-Punkt berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _angle_diff
Quelle: kmotor_pro_action.py:9100-9150
Ziel: kmotor_geometry.py
Funktion: Winkel-Differenz berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _angle_delta
Quelle: kmotor_pro_action.py:9200-9250
Ziel: kmotor_geometry.py
Funktion: Winkel-Delta berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _nearest_magnet_angle_delta
Quelle: kmotor_pro_action.py:9300-9350
Ziel: kmotor_geometry.py
Funktion: Nächste Magnet-Winkel-Delta berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

## KiCad-Rendering (kmotor_kicad.py)

### kmotor_pro_action.py KiCad-Methoden

#### Methode: _add_silk_segment
Quelle: kmotor_pro_action.py:9400-9450
Ziel: kmotor_kicad.py
Funktion: Silk-Segment hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_silk_circle
Quelle: kmotor_pro_action.py:9500-9550
Ziel: kmotor_kicad.py
Funktion: Silk-Kreis hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_silk_circle_at
Quelle: kmotor_pro_action.py:9600-9650
Ziel: kmotor_kicad.py
Funktion: Silk-Kreis an Position hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_edge_cuts_circle_at
Quelle: kmotor_pro_action.py:9700-9750
Ziel: kmotor_kicad.py
Funktion: Edge-Cuts-Kreis hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _clear_generated_corner_holes
Quelle: kmotor_pro_action.py:9800-9850
Ziel: kmotor_kicad.py
Funktion: Ecken-Löcher löschen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_npth_hole_at
Quelle: kmotor_pro_action.py:9900-9950
Ziel: kmotor_kicad.py
Funktion: NPTH-Loch hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_silk_arc_ticks
Quelle: kmotor_pro_action.py:10000-10050
Ziel: kmotor_kicad.py
Funktion: Silk-Arc-Ticks hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_local_tick_fan
Quelle: kmotor_pro_action.py:10100-10150
Ziel: kmotor_kicad.py
Funktion: Lokalen Tick-Fan hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_linear_hole_scale
Quelle: kmotor_pro_action.py:10200-10250
Ziel: kmotor_kicad.py
Funktion: Lineare Loch-Skala hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: add_rotated_line_block
Quelle: kmotor_pro_action.py:10300-10350
Ziel: kmotor_kicad.py
Funktion: Rotierten Linien-Block hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _iter_outer_mount_points
Quelle: kmotor_pro_action.py:10400-10450
Ziel: kmotor_kicad.py
Funktion: Äußere Montage-Punkte iterieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_silk_cross_guides
Quelle: kmotor_pro_action.py:10500-10550
Ziel: kmotor_kicad.py
Funktion: Silk-Kreuz-Hilfen hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_silk_slot_frames
Quelle: kmotor_pro_action.py:10600-10650
Ziel: kmotor_kicad.py
Funktion: Silk-Slot-Frames hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_silk_hole_scales
Quelle: kmotor_pro_action.py:10700-10750
Ziel: kmotor_kicad.py
Funktion: Silk-Loch-Skalen hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_silk_text
Quelle: kmotor_pro_action.py:10800-10850
Ziel: kmotor_kicad.py
Funktion: Silk-Text hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_grouped_silk_segment
Quelle: kmotor_pro_action.py:10900-10950
Ziel: kmotor_kicad.py
Funktion: Gruppiertes Silk-Segment hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_grouped_segment
Quelle: kmotor_pro_action.py:11000-11050
Ziel: kmotor_kicad.py
Funktion: Gruppiertes Segment hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_grouped_silk_circle
Quelle: kmotor_pro_action.py:11100-11150
Ziel: kmotor_kicad.py
Funktion: Gruppierten Silk-Kreis hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_grouped_circle
Quelle: kmotor_pro_action.py:11200-11250
Ziel: kmotor_kicad.py
Funktion: Gruppierten Kreis hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_grouped_edge_circle
Quelle: kmotor_pro_action.py:11300-11350
Ziel: kmotor_kicad.py
Funktion: Gruppierten Edge-Kreis hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _get_magnet_aux_layer
Quelle: kmotor_pro_action.py:11400-11450
Ziel: kmotor_kicad.py
Funktion: Magnet-Aux-Layer holen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_grouped_rect_outline
Quelle: kmotor_pro_action.py:11500-11550
Ziel: kmotor_kicad.py
Funktion: Gruppiertes Rechteck-Outline hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _clear_magnet_group
Quelle: kmotor_pro_action.py:11600-11650
Ziel: kmotor_kicad.py
Funktion: Magnet-Gruppe löschen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _create_magnet_group
Quelle: kmotor_pro_action.py:11700-11750
Ziel: kmotor_kicad.py
Funktion: Magnet-Gruppe erstellen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_mounting_hole_fp_at
Quelle: kmotor_pro_action.py:11800-11850
Ziel: kmotor_kicad.py
Funktion: Montage-Löcher-FP hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _iter_corner_points_for_origin
Quelle: kmotor_pro_action.py:11900-11950
Ziel: kmotor_kicad.py
Funktion: Eckpunkte für Origin iterieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _add_linear_hole_scale_at
Quelle: kmotor_pro_action.py:12000-12050
Ziel: kmotor_kicad.py
Funktion: Lineare Loch-Skala an Position hinzufügen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _build_offset_outline
Quelle: kmotor_pro_action.py:12100-12150
Ziel: kmotor_kicad.py
Funktion: Offset-Outline bauen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _build_offset_mounting_holes
Quelle: kmotor_pro_action.py:12200-12250
Ziel: kmotor_kicad.py
Funktion: Offset-Montage-Löcher bauen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _build_magnet_markers
Quelle: kmotor_pro_action.py:12300-12350
Ziel: kmotor_kicad.py
Funktion: Magnet-Marker bauen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: init_path
Quelle: kmotor_pro_action.py:12400-12450
Ziel: kmotor_kicad.py
Funktion: Pfad initialisieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: init_nets
Quelle: kmotor_pro_action.py:12500-12550
Ziel: kmotor_kicad.py
Funktion: Netze initialisieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: udpate_lset
Quelle: kmotor_pro_action.py:12600-12650
Ziel: kmotor_kicad.py
Funktion: LSet aktualisieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: fillet
Quelle: kmotor_pro_action.py:12700-12750
Ziel: kmotor_kicad.py
Funktion: Fase berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

## Konfiguration (kmotor_persist.py)

### kmotor_pro_action.py Konfigurations-Methoden

#### Methode: eda_angle
Quelle: kmotor_pro_action.py:12800-12850
Ziel: kmotor_persist.py
Funktion: EDA-Winkel berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: init_persist
Quelle: kmotor_pro_action.py:12900-12950
Ziel: kmotor_persist.py
Funktion: Persistenz initialisieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _item_token
Quelle: kmotor_pro_action.py:13000-13050
Ziel: kmotor_persist.py
Funktion: Item-Token berechnen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _tag_generated_zone
Quelle: kmotor_pro_action.py:13100-13150
Ziel: kmotor_persist.py
Funktion: Zone markieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _is_generated_zone
Quelle: kmotor_pro_action.py:13200-13250
Ziel: kmotor_persist.py
Funktion: Zone prüfen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _cleanup_generated_zones
Quelle: kmotor_pro_action.py:13300-13350
Ziel: kmotor_persist.py
Funktion: Generierte Zonen löschen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _apply_pcb_preset
Quelle: kmotor_pro_action.py:13400-13450
Ziel: kmotor_persist.py
Funktion: PCB-Preset anwenden
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: set_status
Quelle: kmotor_pro_action.py:13500-13550
Ziel: kmotor_persist.py
Funktion: Status setzen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _format_exception
Quelle: kmotor_pro_action.py:13600-13650
Ziel: kmotor_persist.py
Funktion: Exception formatieren
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _log_exception
Quelle: kmotor_pro_action.py:13700-13750
Ziel: kmotor_persist.py
Funktion: Exception loggen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _safe_ui_yield
Quelle: kmotor_pro_action.py:13800-13850
Ziel: kmotor_persist.py
Funktion: Safe UI Yield
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _safe_refresh_board
Quelle: kmotor_pro_action.py:13900-13950
Ziel: kmotor_persist.py
Funktion: Safe Board Refresh
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

#### Methode: _run_action
Quelle: kmotor_pro_action.py:14000-14050
Ziel: kmotor_persist.py
Funktion: Action ausführen
Änderungen: Imports anpassen, Referenzen ändern
Status: Pending
Ergebnis: -

## Mathematische Funktionen (kmotor_solvermath.py)

### kmotor_pro_linalg.py Methoden

#### Methode: vec
Quelle: kmotor_pro_linalg.py:1-20
Ziel: kmotor_solvermath.py
Funktion: Vektor-Funktion
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: line_vec
Quelle: kmotor_pro_linalg.py:21-40
Ziel: kmotor_solvermath.py
Funktion: Linien-Vektor
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: line
Quelle: kmotor_pro_linalg.py:41-60
Ziel: kmotor_solvermath.py
Funktion: Linien-Funktion
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: circle_to_polygon
Quelle: kmotor_pro_linalg.py:61-80
Ziel: kmotor_solvermath.py
Funktion: Kreis zu Polygon
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: line_points
Quelle: kmotor_pro_linalg.py:81-100
Ziel: kmotor_solvermath.py
Funktion: Linien-Punkte
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: line_offset
Quelle: kmotor_pro_linalg.py:101-120
Ziel: kmotor_solvermath.py
Funktion: Linien-Offset
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: circle_line_tg
Quelle: kmotor_pro_linalg.py:121-140
Ziel: kmotor_solvermath.py
Funktion: Kreis-Linie-Tangente
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: circle_line_sec
Quelle: kmotor_pro_linalg.py:141-160
Ziel: kmotor_solvermath.py
Funktion: Kreis-Linie-Sekante
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: circle_circle_tg
Quelle: kmotor_pro_linalg.py:161-180
Ziel: kmotor_solvermath.py
Funktion: Kreis-Kreis-Tangente
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: track_arc_trim
Quelle: kmotor_pro_linalg.py:181-200
Ziel: kmotor_solvermath.py
Funktion: Track-Arc-Trim
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: circle_arc_mid
Quelle: kmotor_pro_linalg.py:201-220
Ziel: kmotor_solvermath.py
Funktion: Kreis-Arc-Mitte
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: line_line_intersect
Quelle: kmotor_pro_linalg.py:221-240
Ziel: kmotor_solvermath.py
Funktion: Linie-Linie-Schnitt
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: circle_line_intersect
Quelle: kmotor_pro_linalg.py:241-260
Ziel: kmotor_solvermath.py
Funktion: Kreis-Linie-Schnitt
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: circle_circle_intersect
Quelle: kmotor_pro_linalg.py:261-280
Ziel: kmotor_solvermath.py
Funktion: Kreis-Kreis-Schnitt
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: line_line_center
Quelle: kmotor_pro_linalg.py:281-300
Ziel: kmotor_solvermath.py
Funktion: Linie-Linie-Mitte
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: line_arc_center
Quelle: kmotor_pro_linalg.py:301-320
Ziel: kmotor_solvermath.py
Funktion: Linie-Arc-Mitte
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: normalize
Quelle: kmotor_pro_linalg.py:321-340
Ziel: kmotor_solvermath.py
Funktion: Normalisieren
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

#### Methode: tangent
Quelle: kmotor_pro_linalg.py:341-360
Ziel: kmotor_solvermath.py
Funktion: Tangente berechnen
Änderungen: Keine Imports nötig, nur Verschiebung
Status: Pending
Ergebnis: -

## Zusammenfassung
- **Gesamt: 186 Methoden**
- **GUI-Methoden: 34 Methoden** (kmotor_gui.py)
- **Geschäftslogik: 60 Methoden** (kmotor_solver.py)
- **Geometrie-Methoden: 25 Methoden** (kmotor_geometry.py)
- **KiCad-Rendering: 40 Methoden** (kmotor_kicad.py)
- **Konfiguration: 13 Methoden** (kmotor_persist.py)
- **Mathematische Funktionen: 18 Methoden** (kmotor_solvermath.py)

**Nächster Schritt:** Beginne mit der ersten Methode aus `kmotor_pro_gui.py` und verschiebe sie in `kmotor_gui.py`.