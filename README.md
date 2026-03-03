# KiMotor Fork - State Report

Dieses Repo ist ein Fork mit umfangreichen Anpassungen an Routing, GUI und Validierung.

<img width="1552" height="1787" alt="test57" src="https://github.com/user-attachments/assets/868c92da-4f4e-4a39-ba0a-b7de5e4b57b5" />


- Robustere Schema-/Phasenlogik:
  - `1P`, `3P`, `3P+N` mit Fallback-Handling.
  - saubere Zuordnung der Terminalanzahl (`n_term`).
- Eingabevalidierung vor Generierung:
  - `n_slots > 0`
  - `n_loops > 0`
  - Slot/Phasen-Kompatibilität (mindestens Phasenanzahl, teilbar ohne Rest).
- Routing-Refactor:
  - zentrale Via-Helferfunktionen statt mehrfach dupliziertem Code.
  - deterministischere Coil-Ankerlogik (slot-basierte Anker).
  - Ringverteilung symmetrisiert und auf sinnvolle Anzahl Ebenen begrenzt.
- Support-Vias / Support-TH:
  - Support-Modi `0 / 2 / 4`.
  - eigener Support-TH-Durchmesser.
  - Kollisionsprüfung für zusätzliche Stützlöcher.
- Optionale innere GND-Füllung:
  - per Checkbox ein-/ausschaltbar.
- Status-Handling:
  - Statusfeld in GUI (`Ready / Running / Finished / Failed`).
  - Fehlerfälle im Ablauf werden im Status + Dialog gemeldet.
- Statistik erweitert:
  - Gesamtwerte + Aufschlüsselung (Total / Phase / Coil / Ring).
  - Temperaturabhängige Widerstände.
- 1P/3P Routing-Stand:
  - `3P` aktuell stabiler Zielstand.
  - `1P` stark verbessert (direktere Verbindung statt unnötiger Innenring-Topologie).

## Neu hinzugefügte / zentral genutzte Funktionen

In `kimotor_action.py`:

- `set_status(...)`
- `add_through_via(...)`
- `add_custom_through_via(...)`
- `add_support_hole(...)`
- `hole_collides(...)`
- `build_slot_anchors(...)`
- `build_slot_center_via(...)`
- `calculate_stats_breakdown(...)`
- Wrapper `calculate_stats(...)`

## GUI-Erweiterungen

In `kimotor_gui.py`:

- Status-Panel mit Textausgabe.
- Checkbox: `Fill inner area with GND`.
- Support-Via/Support-TH Einstellungen.
- Erweiterte Stats-Anzeigen (Total, Coil, Ring).

## Bekannte offene Baustelle

- `3P+N` Terminal-/Neutral-Topologie ist noch nicht final:
  - N-Positionierung und Endrouting benötigen noch eine dedizierte, vollständig deterministische Topologie-Tabelle.
  - `1P` + `3P` haben aktuell höhere Priorität und gelten als deutlich stabiler.

## Hinweis

Für schnelle lokale Prüfung nach Änderungen:

```bash
python3 -m py_compile kimotor_action.py kimotor_gui.py
```
