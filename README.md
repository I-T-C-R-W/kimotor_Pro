# KiMotor Fork - State Report for my PRO Version
<img width="1892" height="809" alt="test87" src="https://github.com/user-attachments/assets/69f7b5d3-c293-4eb2-ab20-4f6bca2c1897" />
<img width="1928" height="1692" alt="test90" src="https://github.com/user-attachments/assets/4295ef36-de36-431a-a911-b2a1f343552b" />


Dieses Repo ist ein Fork mit umfangreichen Anpassungen an Routing,Funktionen, GUI und Validierung.

- Robustere Schema-/Phasenlogik:
  - `1P`, `3P`, (`3P+N`) mit Fallback-Handling.
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
- Fehler werden abgefangen und Müll wird gelöscht 
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
- Via Diameter Settings
- Ring Diameter Settings
- Space Diameter Setings
- Support-Via/Support-TH Einstellungen.
- Erweiterte Stats-Anzeigen (Total, Coil, Ring).

## Bekannte offene Baustelle

- `3P+N` Terminal-/Neutral-Topologie ist noch nicht final:
  - N-Positionierung und Endrouting benötigen noch eine dedizierte, vollständig deterministische Topologie-Tabelle.

  - `1P` + `3P` sind aber stabil und nahezu immer fehlerfrei,
  Bekannte Fehler :
   - bei engen Settings leider manchmal das TH Terminal etwas überlappend 
   - der VIA Pin in der Coil ist bei hohen Settings selten mal etwas daneben - daher immer prüfen ! 

## Stable-Stand (Branch = `work`)

- `KiMotor Pro` liegt im Branch `work` jetzt als relativ stabiler Arbeitsstand vor.
- Die harten GUI-Probleme (Layout/Bedienbarkeit) wurden im aktuellen Stand weitgehend behoben.

## TODO (nächste Schritte)
- in der Gui :   spaltenskalierung anpassen, startpreset anpassen - Ergebniss aus spalte 3 evt unter 1 und 2 verschieben oder direkt unter die Parametereinstellungen

- `PCB preset` bleibt aktuell absichtlich im Code enthalten (kompatibilitätsrelevant),
  ist in der GUI jedoch ohne aktive Funktion ausgeblendet.
- Später optional: echte Preset-Profile für Hersteller/Stacks (z. B. `PCBWay` und `JLCPCB`, jeweils Basic/Extended).
