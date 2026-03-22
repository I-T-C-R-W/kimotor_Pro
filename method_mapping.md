# Method Mapping from Old Files (1.41) to New Modules

## Analyse der alten Dateien

**Gesamt: 186 Methoden aus 4 alten Dateien**

### kmotor_pro_action.py (131 Methoden)
**Haupt-Plugin-Klasse mit GUI, Logik und Rendering gemischt**

#### GUI-Methoden (gehören in kmotor_gui.py)
- `__init__` - Haupt-Dialog-Initialisierung
- `on_close` - Dialog-Schließen
- `on_btn_clear` - Eingaben löschen
- `on_btn_generate` - Motor generieren
- `on_btn_generate_magnet` - Magnet-PCB generieren
- `on_btn_generate_both` - Beides generieren
- `on_btn_save` - Konfiguration speichern
- `on_btn_load` - Konfiguration laden
- `on_cb_preset` - PCB-Preset auswählen
- `on_cb_outline` - Outline-Typ ändern
- `on_cb_trmtype` - Terminal-Typ ändern
- `on_cb_winding_mode` - Wicklungs-Modus ändern
- `on_cb_magnet_shape` - Magnet-Form ändern
- `on_cb_mholes` - Montage-Löcher ändern
- `on_nr_layers` - Layer-Anzahl ändern
- `_apply_config_to_gui` - Konfiguration auf GUI übertragen

#### Geschäftslogik (gehört in kmotor_solver.py)
- `get_parameters` - Parameter extrahieren
- `_effective_winding_layers` - Effektive Wicklungs-Layer berechnen
- `_winding_pitch_mm` - Wicklungs-Pitch berechnen
- `_estimate_turns_per_layer` - Windungen pro Layer schätzen
- `validate_parameters` - Parameter validieren
- `get_magnet_parameters` - Magnet-Parameter extrahieren
- `validate_magnet_parameters` - Magnet-Parameter validieren
- `_update_magnet_summary` - Magnet-Zusammenfassung aktualisieren
- `estimate_motor_constants` - Motor-Konstanten schätzen
- `estimate_winding_factor` - Wicklungsfaktor schätzen
- `estimate_performance_stats` - Leistungs-Statistik schätzen
- `estimate_model_warnings` - Modell-Warnungen schätzen
- `get_effective_coil_strategy` - Effektive Spulen-Strategie ermitteln
- `generate_magnet_pcb` - Magnet-PCB generieren
- `generate` - Haupt-Generierungsfunktion
- `coil_tracker` - Spulen-Tracker
- `mpt_point` - MPT-Punkt berechnen
- `do_coils` - Spulen erstellen
- `build_slot_anchors` - Slot-Anker bauen
- `build_slot_center_via` - Slot-Mitte-Via bauen
- `collect` - Sammel-Funktion
- `discrete_centerline_radii` - Diskrete Mittellinien-Radius berechnen
- `add_through_via` - Durchkontaktierung hinzufügen
- `add_custom_through_via` - Custom Durchkontaktierung hinzufügen
- `add_support_hole` - Stützloch hinzufügen
- `get_support_hole_width` - Stützloch-Breite berechnen
- `get_selected_terminal_od_iu` - Terminal-OD berechnen
- `estimate_safe_inner_fill_radius` - Sicherer Innen-Füll-Radius schätzen
- `hole_collides` - Loch-Kollision prüfen
- `do_professional_routing` - Professionelles Routing
- `add_ring_path` - Ring-Pfad hinzufügen
- `get_slot_start` - Slot-Start berechnen
- `segs_intersect` - Segment-Schnittpunkt prüfen
- `orient` - Orientierung berechnen
- `do_outline` - Outline erstellen
- `do_mounting_holes` - Montage-Löcher erstellen
- `do_thermal_zones` - Thermische Zonen erstellen
- `do_silkscreen` - Silkscreen erstellen
- `calculate_stats_breakdown` - Statistik-Details berechnen
- `calculate_stats` - Statistik berechnen

#### Geometrie-Methoden (gehört in kmotor_geometry.py)
- `_point_xy` - Punkt-Koordinaten berechnen
- `_as_point` - Als Punkt konvertieren
- `_radial_vector` - Radial-Vektor berechnen
- `_tangent_vector` - Tangential-Vektor berechnen
- `_point_radius` - Punkt-Radius berechnen
- `_nearest_point_distance` - Nächste Punkt-Distanz berechnen
- `_get_outline_outer_radius` - Outline-Außen-Radius berechnen
- `_get_outline_corners` - Outline-Ecken berechnen
- `_get_outline_bounds` - Outline-Grenzen berechnen
- `_clip_segment_to_outline_box` - Segment an Outline-Box clippen
- `_rotate_xy` - XY rotieren
- `_rotate_about_xy` - XY um Punkt rotieren
- `_offset_xy` - XY verschieben
- `_get_board_span` - Board-Span berechnen
- `_get_magnet_board_origin` - Magnet-Board-Orig berechnen
- `_get_pcb_text_position` - PCB-Text-Position berechnen
- `_get_bottom_right_info_anchor` - Info-Anker berechnen
- `_get_terminal_label_position` - Terminal-Label-Position berechnen
- `_outline_poly_points` - Outline-Polygon-Punkte berechnen
- `to_xy` - Zu XY konvertieren
- `as_inset_point` - Als Insets-Punkt berechnen
- `_angle_diff` - Winkel-Differenz berechnen
- `_angle_delta` - Winkel-Delta berechnen
- `_nearest_magnet_angle_delta` - Nächste Magnet-Winkel-Delta berechnen

#### KiCad-Rendering (gehört in kmotor_kicad.py)
- `_add_silk_segment` - Silk-Segment hinzufügen
- `_add_silk_circle` - Silk-Kreis hinzufügen
- `_add_silk_circle_at` - Silk-Kreis an Position hinzufügen
- `_add_edge_cuts_circle_at` - Edge-Cuts-Kreis hinzufügen
- `_clear_generated_corner_holes` - Ecken-Löcher löschen
- `_add_npth_hole_at` - NPTH-Loch hinzufügen
- `_add_silk_arc_ticks` - Silk-Arc-Ticks hinzufügen
- `_add_local_tick_fan` - Lokalen Tick-Fan hinzufügen
- `_add_linear_hole_scale` - Lineare Loch-Skala hinzufügen
- `add_rotated_line_block` - Rotierten Linien-Block hinzufügen
- `_iter_outer_mount_points` - Äußere Montage-Punkte iterieren
- `_add_silk_cross_guides` - Silk-Kreuz-Hilfen hinzufügen
- `_add_silk_slot_frames` - Silk-Slot-Frames hinzufügen
- `_add_silk_hole_scales` - Silk-Loch-Skalen hinzufügen
- `_add_silk_text` - Silk-Text hinzufügen
- `_add_grouped_silk_segment` - Gruppiertes Silk-Segment hinzufügen
- `_add_grouped_segment` - Gruppiertes Segment hinzufügen
- `_add_grouped_silk_circle` - Gruppierten Silk-Kreis hinzufügen
- `_add_grouped_circle` - Gruppierten Kreis hinzufügen
- `_add_grouped_edge_circle` - Gruppierten Edge-Kreis hinzufügen
- `_get_magnet_aux_layer` - Magnet-Aux-Layer holen
- `_add_grouped_rect_outline` - Gruppiertes Rechteck-Outline hinzufügen
- `_clear_magnet_group` - Magnet-Gruppe löschen
- `_create_magnet_group` - Magnet-Gruppe erstellen
- `_add_mounting_hole_fp_at` - Montage-Löcher-FP hinzufügen
- `_iter_corner_points_for_origin` - Eckpunkte für Origin iterieren
- `_add_linear_hole_scale_at` - Lineare Loch-Skala an Position hinzufügen
- `_build_offset_outline` - Offset-Outline bauen
- `_build_offset_mounting_holes` - Offset-Montage-Löcher bauen
- `_build_magnet_markers` - Magnet-Marker bauen
- `init_path` - Pfad initialisieren
- `init_nets` - Netze initialisieren
- `udpate_lset` - LSet aktualisieren
- `fillet` - Fase berechnen

#### Konfiguration (gehört in kmotor_persist.py)
- `eda_angle` - EDA-Winkel berechnen
- `init_persist` - Persistenz initialisieren
- `_item_token` - Item-Token berechnen
- `_tag_generated_zone` - Zone markieren
- `_is_generated_zone` - Zone prüfen
- `_cleanup_generated_zones` - Generierte Zonen löschen
- `_apply_pcb_preset` - PCB-Preset anwenden
- `set_status` - Status setzen
- `_format_exception` - Exception formatieren
- `_log_exception` - Exception loggen
- `_safe_ui_yield` - Safe UI Yield
- `_safe_refresh_board` - Safe Board Refresh
- `_run_action` - Action ausführen

### kmotor_pro_gui.py (34 Methoden)
**Reine GUI-Methoden (gehören in kmotor_gui.py)**

#### GUI-Methoden
- `__init__` - GUI-Initialisierung
- `_style_staticbox` - StaticBox stylen
- `_reset_desc_font` - Beschreibungs-Font zurücksetzen
- `__del__` - GUI bereinigen
- `on_close` - Schließen-Handler
- `on_cb_outline` - Outline-Change-Handler
- `on_cb_mholes` - Montage-Löcher-Change-Handler
- `on_cb_preset` - Preset-Change-Handler
- `on_nr_layers` - Layer-Change-Handler
- `on_cb_trmtype` - Terminal-Typ-Change-Handler
- `on_cb_winding_mode` - Wicklungs-Modus-Change-Handler
- `on_cb_magnet_shape` - Magnet-Form-Change-Handler
- `on_btn_load` - Laden-Button-Handler
- `on_btn_save` - Speichern-Button-Handler
- `on_btn_clear` - Löschen-Button-Handler
- `on_btn_generate_magnet` - Magnet-Generieren-Button-Handler
- `on_btn_generate_both` - Beides-Generieren-Button-Handler
- `on_btn_generate` - Generieren-Button-Handler
- `_apply_pcb_preset` - PCB-Preset anwenden

### kmotor_pro_solver.py (3 Methoden)
**Solver-Strategien (gehören in kmotor_solver.py)**

#### Solver-Methoden
- `parallel` - Parallele Strategie
- `radial` - Radiale Strategie
- `compact` - Kompakte Strategie

### kmotor_pro_linalg.py (18 Methoden)
**Mathematische Funktionen (gehören in kmotor_solvermath.py)**

#### Mathematische Methoden
- `vec` - Vektor-Funktion
- `line_vec` - Linien-Vektor
- `line` - Linien-Funktion
- `circle_to_polygon` - Kreis zu Polygon
- `line_points` - Linien-Punkte
- `line_offset` - Linien-Offset
- `circle_line_tg` - Kreis-Linie-Tangente
- `circle_line_sec` - Kreis-Linie-Sekante
- `circle_circle_tg` - Kreis-Kreis-Tangente
- `track_arc_trim` - Track-Arc-Trim
- `circle_arc_mid` - Kreis-Arc-Mitte
- `line_line_intersect` - Linie-Linie-Schnitt
- `circle_line_intersect` - Kreis-Linie-Schnitt
- `circle_circle_intersect` - Kreis-Kreis-Schnitt
- `line_line_center` - Linie-Linie-Mitte
- `line_arc_center` - Linie-Arc-Mitte
- `normalize` - Normalisieren
- `tangent` - Tangente berechnen

## Zusammenfassung der Zuordnung

| Alte Datei | Neue Module | Methodenanzahl |
|------------|-------------|----------------|
| kmotor_pro_action.py | kmotor_gui.py | ~20 Methoden |
| kmotor_pro_action.py | kmotor_solver.py | ~60 Methoden |
| kmotor_pro_action.py | kmotor_geometry.py | ~25 Methoden |
| kmotor_pro_action.py | kmotor_kicad.py | ~20 Methoden |
| kmotor_pro_action.py | kmotor_persist.py | ~6 Methoden |
| kmotor_pro_gui.py | kmotor_gui.py | 34 Methoden |
| kmotor_pro_solver.py | kmotor_solver.py | 3 Methoden |
| kmotor_pro_linalg.py | kmotor_solvermath.py | 18 Methoden |

**Gesamt: 186 Methoden müssen in die neuen Module verschoben werden**