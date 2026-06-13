# INTERSTELLAR · Feature Map

> Auto-generated · Last updated: 2026-06-13 14:40 UTC
> Source of truth: `ENDURANCE.py` + `README.md` — never edit manually

---

## Navigation Pages

| Icon | Page Label | Route Key |
|------|-----------|-----------|
| ✦ | MISSION OVERVIEW | `overview` |
| ⬡ | GRAVITY ENGINE | `gravity` |
| ⏱ | RELATIVITY CALC | `relativity` |
| 🪐 | PLANET SCANNER | `planets` |
| ⟳ | WORMHOLE NAVIGATOR | `wormhole` |
| ◈ | TESSERACT DECODER | `tesseract` |
| ⛨ | CREW TELEMETRY | `crew` |
| ▤ | MISSION REPORTER | `mission` |
| ⚛ | QUANTUM SINGULARITY | `quantum` |
| ℹ | SYSTEM STATUS | `system` |
| Phase | Gargantua Orbit | `#4FC3F7` |
| Active Crew | 4 (Cooper, Brand, Romilly, Doyle) | `#81C784` |
| TARS | Operational — Mode: NAV | `#E8C46A` |
| CASE | Operational — Mode: SCI | `#E8C46A` |
| Hull Integrity | 98.7% | `#81C784` |
| Fuel Remaining | 67.3% — 201,900 kg | `#FF8800` |
| Δv Remaining | 4.2 km/s | `#FF8800` |
| Life Support | O₂: 380kg · H₂O: 1,640L | `#81C784` |
| Power | 38.2 kW (surplus: 6.8) | `#81C784` |
| Comms Lag | 79 min one-way | `#CE93D8` |
| Probes launched | 12 | `#E8C46A` |
| Active signals | 1 | `#81C784` |
| Confirmed OK | 1 | `#E8C46A` |
| Confirmed bad | 4 | `#D154FF` |
| Data falsified | 1 | `#CE93D8` |
| Silent | 5 | `#555` |
| Unknown | 1 | `#4FC3F7` |

---

## Backend Modules (Safe-Imported)

  - `gravity_engine`
  - `relativity_calculator`
  - `planet_analyzer`
  - `wormhole_navigator`
  - `tesseract_decoder`
  - `crew_telemetry`
  - `mission_reporter`
  - `quantum_singularity`

---

## Module Registry

| File | Description |
|------|-------------|
| `ENDURANCE.py` | Mission Control Frontend |
| `gravity_engine.py` | Module I   — Kerr BH Physics |
| `relativity_calculator.py` | Module II  — SR/GR Engine |
| `planet_analyzer.py` | Module III — Habitability |
| `wormhole_navigator.py` | Module IV  — Wormhole Physics |
| `tesseract_decoder.py` | Module V   — Gravity Signals |
| `crew_telemetry.py` | Module VI  — Ship & Crew |
| `mission_reporter.py` | Module VII — Mission Intel |
| `quantum_singularity.py` | Module VIII— Planck/LQG/BKL |

---

## Mission Constants

| Constant | Value |
|----------|-------|
| `PLAN_A_PCT` | 71.4% |
| `PLAN_B_EMBRYOS` | 5000 |
| `TARS_HONESTY` | 90% |
| `TARS_HUMOUR` | 75% |
| `MISSION_START_YEAR` | 2067 |
| `CURRENT_MISSION_DAY` | 730 |
| `BLIGHT_SEVERITY` | CRITICAL |
| `WORMHOLE_STATUS` | STABLE |
| `EARTH_POPULATION` | 3.5 Billion |

---

## Frontend Section Map (§ markers in ENDURANCE.py)

| Section | Description |
|---------|-------------|
| §1 | BACKEND IMPORTS — safe import with fallback UI |
| §2 | CONSTANTS & MISSION DATA |
| §3 | MASTER CSS — dark space theme |
| §4 | SESSION STATE INITIALISATION |
| §5 | BACKGROUND IMAGE LOADER |
| §6 | UTILITY COMPONENTS |
| §7 | SIDEBAR |
| §8 | BOOT SEQUENCE |
| §9 | OVERVIEW PAGE — Mission dashboard |
| §10 | SYSTEM STATUS PAGE |
| §11 | BACKEND PAGE WRAPPERS — safe rendering with error handling |
| §12 | GLOBAL MATPLOTLIB STYLE (applied before every backend) |
| §13 | INTERSTELLAR INTRO CRAWL (one-time welcome) |
| §14 | MAIN ROUTER |
| §15 | ENTRY POINT |

---

*Total codebase: 21,573 lines · 9 Python files · 8 science backends*
