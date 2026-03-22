# REFACTOR_SPEC.md

## 🎯 GOAL

Refactor `kimotor_action.py` into a modular, deterministic, and scalable architecture.

The system must support:

* large slot counts (>=300)
* multiple coil types (PCB, wire)
* future physics extensions
* headless execution (CLI / automation)

---

## 🧱 CORE PRINCIPLES (MANDATORY)

1. **Separation of Concerns**

   * GUI, logic, geometry, and rendering MUST be strictly separated

2. **Deterministic Behavior**

   * Same input (MotorConfig) MUST produce identical output

3. **Move, NOT Rewrite**

   * Existing logic should be preserved
   * Only reorganize and minimally adapt

4. **Single Source of Truth**

   * All parameters MUST come from `MotorConfig`

---

## 🚫 HARD RULES (DO NOT VIOLATE)

* `kmotor_solver.py` MUST NOT import `pcbnew`
* `kmotor_solver.py` MUST NOT depend on GUI
* `kmotor_geometry.py` MUST NOT depend on KiCad or GUI
* `kmotor_gui.py` MUST NOT contain calculations
* `kmotor_kicad.py` MUST NOT contain business logic
* NO hidden global state
* NO duplicated calculations

---

## 🧩 TARGET FILE STRUCTURE

```
kmotor/
  kmotor_gui.py
  kmotor_gui_previewer.py
  kmotor_api.py
  kmotor_solver.py
  kmotor_geometry.py
  kmotor_solvermath.py
  kmotor_kicad.py
  kmotor_models.py
  kmotor_persist.py
```

---

## 📦 MODULE RESPONSIBILITIES

### kmotor_models.py

Defines all core data structures

* MotorConfig (ALL input parameters)
* Coil, Slot, Geometry primitives
* Result containers

---

### kmotor_api.py

Central orchestration layer

* Entry point: `generate_motor(config)`
* Selects strategy (PCB / wire)
* Calls solver → geometry → renderer

---

### kmotor_solver.py

Core logic (NO geometry rendering, NO KiCad)

* slot distribution
* phase assignment
* winding logic
* topology handling (1P / 3P / future)

---

### kmotor_geometry.py

Pure geometry generation

* points
* paths
* coil shapes

Output must be abstract (no KiCad types)

---

### kmotor_solvermath.py

Mathematics + physics (pure functions)

* rotations
* intersections
* magnetic / electrical models (future)

---

### kmotor_kicad.py

Renderer only

* converts geometry → pcbnew objects
* no calculations
* no decision logic

---

### kmotor_gui.py

User interface only

* collects input
* creates MotorConfig
* calls API
* displays result

---

### kmotor_gui_previewer.py

Lightweight preview system

* schematic visualization
* no real geometry
* context-sensitive UI help

---

### kmotor_persist.py

Config storage

* save/load presets
* JSON or similar

---

## 🔄 SYSTEM PIPELINE

```
MotorConfig
    ↓
kmotor_api
    ↓
kmotor_solver
    ↓
kmotor_geometry
    ↓
kmotor_kicad
```

---

## ⚙️ IMPLEMENTATION PHASES

### Phase 1 – Extraction (NO behavior change)

* create all modules
* move existing code into correct files
* ensure system still runs

---

### Phase 2 – Decoupling

* remove all cross-dependencies
* enforce HARD RULES
* clean imports

---

### Phase 3 – Stabilization

* introduce floating point tolerances
* remove iterative geometry errors
* ensure deterministic output

---

### Phase 4 – Performance

* introduce NumPy vectorization
* eliminate redundant calculations
* support large slot counts

---

### Phase 5 – Extension

* physics models
* export (SVG/DXF)
* strategy system (PCB vs wire)

---

## 🧠 DESIGN PATTERNS

* Strategy Pattern → coil / topology handling
* Factory Pattern → generator selection
* Functional Core → solver + math
* Imperative Shell → GUI + API

---

## ✅ SUCCESS CRITERIA

Refactor is complete when:

* solver runs without GUI
* solver runs without KiCad
* geometry is reusable for export
* system handles >=300 slots reliably
* no duplicated logic remains

---

## ⚠️ NON-GOALS

* no UI redesign (except separation)
* no physics rewrite during refactor
* no feature expansion during Phase 1–2

---

## 🔒 FINAL RULE

If a change introduces coupling between modules → REJECT IT

