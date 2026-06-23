# INTERSTELLAR · Code Intelligence

> Deep per-file analysis of every `.py` file in the repository root.
> Auto-generated · `2026-06-23 08:38 UTC` · 9 files analysed

---

## Summary

| Metric | Value |
|--------|-------|
| Files analysed | 9 |
| Total lines | 21,634 |
| Total functions | 116 |
| Total classes | 119 |
| Total safe-imports | 8 |

---

## Per-File Analysis

### `ENDURANCE.py`

| Metric | Value |
|--------|-------|
| Lines | 2,640 |
| Characters | 109,655 |
| SHA-256 prefix | `73a8735d2ff295cb` |
| Functions | 25 |
| Classes | 0 |
| Imports | 18 |
| Backend modules | 8 |

**Streamlit config:** title=`INTERSTELLAR` icon=`♾️` layout=`wide`

**Docstring:** INTERSTELLAR.py — INTERSTELLAR Control Frontend | Interstellar Science Platform v3.0.0 ═══════════════════════════════════════════════════════════════════════════════ The INTERSTELLAR Control Interfac

**Top-level functions:**
  - `_safe_import()`
  - `init_global_state()`
  - `load_background()`
  - `inject_background()`
  - `page_header()`
  - `kpi_row()`
  - `scan_line()`
  - `section_rule()`
  - `quote_banner()`
  - `tars_says()`
  - `status_badge()`
  - `_hex_to_rgb()`
  - `terminal_block()`
  - `backend_error_card()`
  - `progress_bar()`
  - `render_sidebar()`
  - `render_boot_sequence()`
  - `render_overview()`
  - `_render_gargantua_overview()`
  - `_render_plan_progress()`

**Classes:**
  - (none)

**Imports:**
  - `streamlit`
  - `os`
  - `sys`
  - `math`
  - `time`
  - `base64`
  - `hashlib`
  - `random`
  - `warnings`
  - `traceback`
  - `pathlib`
  - `typing`
  - `numpy`
  - `pandas`
  - `matplotlib`

**Safe-imported backends:**
  - `gravity_engine`
  - `relativity_calculator`
  - `planet_analyzer`
  - `wormhole_navigator`
  - `tesseract_decoder`
  - `crew_telemetry`
  - `mission_reporter`
  - `quantum_singularity`

**Constants (ALL_CAPS):**

| Name | Value |
|------|-------|
| `EARTH_POPULATION` | `3.5 Billion` |
| `BLIGHT_SEVERITY` | `CRITICAL` |
| `GARGANTUA_DIST_LY` | `10 Billion` |
| `WORMHOLE_STATUS` | `STABLE` |
| `MASTER_CSS` | `` |
| `MISSION_START_YEAR` | `2067` |
| `CURRENT_MISSION_DAY` | `730` |
| `PLAN_A_PCT` | `71.4` |
| `PLAN_B_EMBRYOS` | `5` |
| `TARS_HONESTY` | `90` |
| `TARS_HUMOUR` | `75` |


### `crew_telemetry.py`

| Metric | Value |
|--------|-------|
| Lines | 2,179 |
| Characters | 100,443 |
| SHA-256 prefix | `9fdd5e1309a959ef` |
| Functions | 13 |
| Classes | 21 |
| Imports | 20 |
| Backend modules | 0 |

**Docstring:** crew_telemetry.py — Crew Telemetry, TARS/CASE AI & Endurance Ship Systems ENDURANCE Mission Control | Interstellar Science Platform v3.0.0 ═════════════════════════════════════════════════════════════

**Top-level functions:**
  - `build_crew_registry()`
  - `build_tars()`
  - `build_case()`
  - `init_session_state()`
  - `_mpl()`
  - `_plot_crew_vitals()`
  - `_plot_physiological_profile()`
  - `_plot_tars_panel()`
  - `_plot_endurance_systems()`
  - `_plot_cryosleep()`
  - `_plot_comms()`
  - `_plot_tars_decisions()`
  - `crew_telemetry_page()`

**Classes:**
  - `CrewID`
  - `CrewStatus`
  - `SystemStatus`
  - `MissionPhase`
  - `RobotMode`
  - `AlertLevel`
  - `CrewMember`
  - `AIRobot`
  - `ShipModule`
  - `LifeSupportSystem`
  - `PropulsionSystem`
  - `PowerSystem`
  - `EnduranceSpacecraft`
  - `CryosleepPod`
  - `CryosleepManager`
  - `Message`
  - `CommunicationsRelay`
  - `PhysiologySimulator`
  - `EpigeneticRadiationModel`
  - `CircadianRhythmModel`
  - `MicrogravityPhysiology`

**Imports:**
  - `__future__`
  - `hashlib`
  - `math`
  - `random`
  - `time`
  - `uuid`
  - `warnings`
  - `dataclasses`
  - `enum`
  - `typing`
  - `numpy`
  - `pandas`
  - `scipy.signal`
  - `scipy.integrate`
  - `matplotlib`

**Safe-imported backends:**
  - (none)

**Constants (ALL_CAPS):**

| Name | Value |
|------|-------|
| `G_SI` | `6.674` |
| `C_SI` | `2.997` |
| `M_SUN` | `1.989` |
| `YEAR_S` | `3.155` |
| `DAY_S` | `86` |
| `HOUR_S` | `3` |
| `GARG_DIST_LY` | `10.0` |
| `ENDURANCE_MASS_KG` | `5.00` |
| `ENDURANCE_RADIUS_M` | `40.0` |
| `ENDURANCE_RPM` | `5.0` |
| `ENDURANCE_MODULES` | `16` |
| `ENDURANCE_CREW_MODS` | `12` |
| `ENDURANCE_DOCK_MODS` | `4` |
| `ENDURANCE_FUEL_KG` | `3.0` |
| `ENDURANCE_ISP` | `9000.0` |


### `gravity_engine.py`

| Metric | Value |
|--------|-------|
| Lines | 3,036 |
| Characters | 131,094 |
| SHA-256 prefix | `58e6609c8f2baf0c` |
| Functions | 15 |
| Classes | 14 |
| Imports | 20 |
| Backend modules | 0 |

**Docstring:** gravity_engine.py — Gargantua Black Hole Physics & Gravitational Wave Engine ENDURANCE Mission Control | Interstellar Science Platform v3.0.0 ══════════════════════════════════════════════════════════

**Top-level functions:**
  - `geo_mass()`
  - `schw_rad()`
  - `geo_time()`
  - `init_session_state()`
  - `_mpl()`
  - `_plot_disk_panel()`
  - `_plot_bh_anatomy()`
  - `_plot_gw_waveform()`
  - `_plot_radial_profile()`
  - `_plot_tidal()`
  - `_plot_miller()`
  - `_plot_gw_catalog()`
  - `_plot_penrose()`
  - `_plot_hawking()`
  - `gravity_engine_page()`

**Classes:**
  - `BHType`
  - `OrbitClass`
  - `TidalClass`
  - `GWStatus`
  - `KerrBlackHole`
  - `NovikovThorneAccretionDisk`
  - `HawkingRadiationCalculator`
  - `KerrGeodesicLensing`
  - `GWEvent`
  - `GravitationalWaveEngine`
  - `PenroseCarterDiagram`
  - `KerrNewmanPhysics`
  - `QuasiNormalModes`
  - `PhotonRingRenderer`

**Imports:**
  - `__future__`
  - `hashlib`
  - `math`
  - `time`
  - `uuid`
  - `warnings`
  - `dataclasses`
  - `enum`
  - `typing`
  - `numpy`
  - `pandas`
  - `scipy.integrate`
  - `scipy.optimize`
  - `scipy.signal`
  - `scipy.fft`

**Safe-imported backends:**
  - (none)

**Constants (ALL_CAPS):**

| Name | Value |
|------|-------|
| `G_SI` | `6.674` |
| `C_SI` | `2.997` |
| `HBAR` | `1.054` |
| `H_PL` | `6.626` |
| `K_B` | `1.380` |
| `SIGMA_SB` | `5.670` |
| `M_SUN` | `1.989` |
| `M_EARTH` | `5.972` |
| `R_SUN` | `6.957` |
| `R_EARTH` | `6.371` |
| `MPC` | `3.085` |
| `GPC` | `3.085` |
| `YEAR_S` | `3.155` |
| `DAY_S` | `86` |
| `HOUR_S` | `3` |


### `mission_reporter.py`

| Metric | Value |
|--------|-------|
| Lines | 1,808 |
| Characters | 83,184 |
| SHA-256 prefix | `2e52c9f4fafe0e32` |
| Functions | 10 |
| Classes | 18 |
| Imports | 16 |
| Backend modules | 0 |

**Docstring:** mission_reporter.py — Mission Reporting, Lazarus Archive & Plan A/B Engine ENDURANCE Mission Control | Interstellar Science Platform v3.0.0 ════════════════════════════════════════════════════════════

**Top-level functions:**
  - `build_lazarus_archive()`
  - `init_session_state()`
  - `_mpl()`
  - `_plot_lazarus_overview()`
  - `_plot_plan_ab()`
  - `_plot_blight()`
  - `_plot_achievements()`
  - `_plot_data_drives()`
  - `_plot_mission_timeline()`
  - `mission_reporter_page()`

**Classes:**
  - `ProbeStatus`
  - `PlanStatus`
  - `AchievementTier`
  - `DataDriveStatus`
  - `LazarusProbe`
  - `PlanAStatus`
  - `EmbryoProfile`
  - `EmbryoBank`
  - `PlanBStatus`
  - `BlightSpreadModel`
  - `Achievement`
  - `MissionScorer`
  - `DataDrive`
  - `DataDriveManager`
  - `MissionReporter`
  - `PlanBGeneticOptimizer`
  - `BlightSIRModel`
  - `LazarusSignalAnalyzer`

**Imports:**
  - `__future__`
  - `hashlib,`
  - `dataclasses`
  - `enum`
  - `typing`
  - `numpy`
  - `pandas`
  - `scipy.optimize`
  - `scipy.integrate`
  - `matplotlib`
  - `matplotlib.pyplot`
  - `matplotlib.gridspec`
  - `matplotlib.patches`
  - `matplotlib.ticker`
  - `matplotlib.colors`

**Safe-imported backends:**
  - (none)

**Constants (ALL_CAPS):**

| Name | Value |
|------|-------|
| `G_SI` | `6.674` |
| `C_SI` | `2.997` |
| `M_SUN` | `1.989` |
| `YEAR_S` | `3.155` |
| `DAY_S` | `86` |
| `EARTH_POP_2067` | `3.5` |
| `BLIGHT_ONSET_YR` | `2049` |
| `MISSION_START_YR` | `2067` |
| `COLONY_CAP` | `100` |
| `EMBRYO_COUNT` | `5` |


### `planet_analyzer.py`

| Metric | Value |
|--------|-------|
| Lines | 2,706 |
| Characters | 118,807 |
| SHA-256 prefix | `bfbdfa55c1d436dc` |
| Functions | 14 |
| Classes | 15 |
| Imports | 20 |
| Backend modules | 0 |

**Docstring:** planet_analyzer.py — Exoplanet Habitability & Planetary Science Engine ENDURANCE Mission Control | Interstellar Science Platform v3.0.0 ════════════════════════════════════════════════════════════════

**Top-level functions:**
  - `make_miller()`
  - `make_mann()`
  - `make_edmunds()`
  - `make_earth()`
  - `init_session_state()`
  - `_mpl()`
  - `_plot_radar()`
  - `_plot_hz_diagram()`
  - `_plot_atmosphere()`
  - `_plot_spectrum()`
  - `_plot_comparison_overview()`
  - `_plot_risk_matrix()`
  - `_plot_miller_special()`
  - `planet_analyzer_page()`

**Classes:**
  - `PlanetID`
  - `HabitabilityClass`
  - `AtmosphereType`
  - `SurfaceType`
  - `TidalState`
  - `MissionRisk`
  - `AtmosphericComposition`
  - `Planet`
  - `HabitabilityScorer`
  - `AtmosphericEngine`
  - `SpectralEngine`
  - `MissionRiskAssessor`
  - `RadiativeConvectiveModel`
  - `AtmosphericRetrieval`
  - `PlanetaryInterior`

**Imports:**
  - `__future__`
  - `math`
  - `uuid`
  - `warnings`
  - `copy`
  - `dataclasses`
  - `enum`
  - `typing`
  - `numpy`
  - `pandas`
  - `scipy.integrate`
  - `scipy.optimize`
  - `scipy.special`
  - `scipy.interpolate`
  - `matplotlib`

**Safe-imported backends:**
  - (none)

**Constants (ALL_CAPS):**

| Name | Value |
|------|-------|
| `G_SI` | `6.674` |
| `C_SI` | `2.997` |
| `K_B` | `1.380` |
| `H_PL` | `6.626` |
| `SIGMA_SB` | `5.670` |
| `M_SUN` | `1.989` |
| `R_SUN` | `6.957` |
| `L_SUN` | `3.828` |
| `M_EARTH` | `5.972` |
| `R_EARTH` | `6.371` |
| `G_EARTH` | `9.806` |
| `M_ATMO_E` | `5.15` |
| `P_SURF_E` | `101` |
| `T_SURF_E` | `288.0` |
| `YEAR_S` | `3.155` |


### `quantum_singularity.py`

| Metric | Value |
|--------|-------|
| Lines | 2,200 |
| Characters | 105,215 |
| SHA-256 prefix | `19916f64cc0ebbd7` |
| Functions | 12 |
| Classes | 12 |
| Imports | 20 |
| Backend modules | 0 |

**Docstring:** quantum_singularity.py — Quantum Gravity, Singularity Physics & Bulk Dimensional Engine ENDURANCE Mission Control | Interstellar Science Platform v3.0.0 ═══════════════════════════════════════════════

**Top-level functions:**
  - `_fig_style()`
  - `_make_fig()`
  - `_render_planck_foam_tab()`
  - `_render_lqg_tab()`
  - `_render_bkl_tab()`
  - `_render_page_curve_tab()`
  - `_render_unruh_tab()`
  - `_render_chaos_tab()`
  - `_render_holography_tab()`
  - `_render_cooper_tab()`
  - `_render_qs_overview()`
  - `quantum_singularity_page()`

**Classes:**
  - `PlanckState`
  - `KasnerEpoch`
  - `PageCurveState`
  - `SYKParams`
  - `PlanckFoamEngine`
  - `LQGEngine`
  - `BKLEngine`
  - `PageCurveEngine`
  - `UnruhVacuumEngine`
  - `QuantumChaosEngine`
  - `HolographyEngine`
  - `CooperCrossingEngine`

**Imports:**
  - `__future__`
  - `math`
  - `warnings`
  - `hashlib`
  - `dataclasses`
  - `enum`
  - `typing`
  - `numpy`
  - `pandas`
  - `scipy.integrate`
  - `scipy.optimize`
  - `scipy.special`
  - `scipy.stats`
  - `scipy.linalg`
  - `matplotlib`

**Safe-imported backends:**
  - (none)

**Constants (ALL_CAPS):**

| Name | Value |
|------|-------|
| `G_SI` | `6.674` |
| `C_SI` | `2.997` |
| `HBAR_SI` | `1.054` |
| `H_SI` | `6.626` |
| `KB_SI` | `1.380` |
| `E_CHARGE` | `1.602` |
| `M_E_SI` | `9.109` |
| `M_SUN` | `1.989` |
| `ALPHA_EM` | `7.297` |
| `SIGMA_SB` | `5.670` |
| `GAMMA_BI` | `0.2375` |
| `A_MIN_LQG` | `4.0` |
| `RHO_CRIT_LQC` | `0.4088` |
| `GARG_MASS_MSUN` | `1.0` |
| `GARG_SPIN` | `0.9999` |


### `relativity_calculator.py`

| Metric | Value |
|--------|-------|
| Lines | 2,801 |
| Characters | 124,072 |
| SHA-256 prefix | `bb53f69695e0bc36` |
| Functions | 9 |
| Classes | 13 |
| Imports | 18 |
| Backend modules | 0 |

**Docstring:** relativity_calculator.py — Special & General Relativity Engine ENDURANCE Mission Control | Interstellar Science Platform v3.0.0 ════════════════════════════════════════════════════════════════════════

**Top-level functions:**
  - `init_session_state()`
  - `_mpl()`
  - `_plot_sr_dashboard()`
  - `_plot_spacetime_diagram()`
  - `_plot_gr_profile()`
  - `_plot_mission_timeline()`
  - `_plot_geodesic()`
  - `_plot_twin_summary()`
  - `relativity_calculator_page()`

**Classes:**
  - `IntervalType`
  - `FrameType`
  - `MissionPhase`
  - `ClockType`
  - `SpecialRelativity`
  - `GeneralRelativity`
  - `MissionLeg`
  - `PersonTimeline`
  - `CooperMurphTimeEngine`
  - `SpacetimeDiagramBuilder`
  - `InterstellarMissionIntegrator`
  - `GWMemoryCalculator`
  - `PostNewtonianBinary`

**Imports:**
  - `__future__`
  - `math`
  - `time`
  - `uuid`
  - `warnings`
  - `dataclasses`
  - `enum`
  - `typing`
  - `numpy`
  - `pandas`
  - `scipy.integrate`
  - `scipy.optimize`
  - `matplotlib`
  - `matplotlib.pyplot`
  - `matplotlib.gridspec`

**Safe-imported backends:**
  - (none)

**Constants (ALL_CAPS):**

| Name | Value |
|------|-------|
| `C_SI` | `2.997` |
| `G_SI` | `6.674` |
| `HBAR` | `1.054` |
| `H_PL` | `6.626` |
| `K_B` | `1.380` |
| `M_SUN` | `1.989` |
| `M_EARTH` | `5.972` |
| `M_ELECTRON` | `9.109` |
| `M_PROTON` | `1.672` |
| `R_EARTH` | `6.371` |
| `MPC` | `3.085` |
| `YEAR_S` | `3.155` |
| `DAY_S` | `86` |
| `HOUR_S` | `3` |
| `GARG_MASS_SOLAR` | `1.00` |


### `tesseract_decoder.py`

| Metric | Value |
|--------|-------|
| Lines | 2,176 |
| Characters | 96,998 |
| SHA-256 prefix | `b6e5d2f3b2bd7512` |
| Functions | 9 |
| Classes | 13 |
| Imports | 20 |
| Backend modules | 0 |

**Docstring:** tesseract_decoder.py — Tesseract Physics, Gravity Signal & Quantum Data Engine ENDURANCE Mission Control | Interstellar Science Platform v3.0.0 ════════════════════════════════════════════════════════

**Top-level functions:**
  - `init_session_state()`
  - `_mpl()`
  - `_plot_tesseract()`
  - `_plot_encoding()`
  - `_plot_wdw()`
  - `_plot_tars_crystal()`
  - `_plot_bulk_channel()`
  - `_plot_coordinate_decode()`
  - `tesseract_decoder_page()`

**Classes:**
  - `EncodingScheme`
  - `DecoderState`
  - `MessageType`
  - `BulkDimension`
  - `TesseractGeometry`
  - `GravitySignalEncoder`
  - `GravitySignalDecoder`
  - `MurphyEquationSolver`
  - `TARSDataCrystal`
  - `BulkCommunicationChannel`
  - `HolographicEntanglement`
  - `BulkGeodesicDeviation`
  - `QuasicrystalGeometry`

**Imports:**
  - `__future__`
  - `hashlib`
  - `math`
  - `struct`
  - `time`
  - `uuid`
  - `warnings`
  - `dataclasses`
  - `enum`
  - `typing`
  - `numpy`
  - `pandas`
  - `scipy.integrate`
  - `scipy.optimize`
  - `scipy.fft`

**Safe-imported backends:**
  - (none)

**Constants (ALL_CAPS):**

| Name | Value |
|------|-------|
| `COOPER_MSG_BINARY` | `01001110010001000011001011000010` |
| `G_SI` | `6.674` |
| `C_SI` | `2.997` |
| `HBAR` | `1.054` |
| `H_PL` | `6.626` |
| `K_B` | `1.380` |
| `M_PLANCK` | `2.176` |
| `L_PLANCK` | `1.616` |
| `T_PLANCK` | `5.391` |
| `E_PLANCK` | `1.956` |
| `M_SUN` | `1.989` |
| `YEAR_S` | `3.155` |
| `HOUR_S` | `3` |
| `GARG_MASS_KG` | `1.0` |
| `GARG_RS` | `2.0` |


### `wormhole_navigator.py`

| Metric | Value |
|--------|-------|
| Lines | 2,088 |
| Characters | 93,273 |
| SHA-256 prefix | `ea8d69a33e426597` |
| Functions | 9 |
| Classes | 13 |
| Imports | 20 |
| Backend modules | 0 |

**Docstring:** wormhole_navigator.py — Wormhole Physics & Interstellar Navigation Engine ENDURANCE Mission Control | Interstellar Science Platform v3.0.0 ═════════════════════════════════════════════════════════════

**Top-level functions:**
  - `init_session_state()`
  - `_mpl()`
  - `_plot_embedding()`
  - `_plot_exotic_traversal()`
  - `_plot_mission_trajectory()`
  - `_plot_gravity_assist()`
  - `_plot_saturn_wormhole()`
  - `_plot_shape_comparison()`
  - `wormhole_navigator_page()`

**Classes:**
  - `ShapeFunction`
  - `RedshiftFunction`
  - `TraversalStatus`
  - `ManeuverType`
  - `WormholeGeometry`
  - `ExoticMatterPhysics`
  - `WormholeTraversalCalculator`
  - `OrbitalMechanics`
  - `TrajectoryLeg`
  - `MissionTrajectoryPlanner`
  - `MorrisThorneGeodesics`
  - `FlammsParaboloid`
  - `EnergyConditionAnalyzer`

**Imports:**
  - `__future__`
  - `math`
  - `uuid`
  - `warnings`
  - `dataclasses`
  - `enum`
  - `typing`
  - `numpy`
  - `pandas`
  - `scipy.integrate`
  - `scipy.optimize`
  - `scipy.special`
  - `matplotlib`
  - `matplotlib.pyplot`
  - `matplotlib.gridspec`

**Safe-imported backends:**
  - (none)

**Constants (ALL_CAPS):**

| Name | Value |
|------|-------|
| `G_SI` | `6.674` |
| `C_SI` | `2.997` |
| `HBAR` | `1.054` |
| `K_B` | `1.380` |
| `M_SUN` | `1.989` |
| `L_SUN` | `3.828` |
| `M_EARTH` | `5.972` |
| `M_JUPITER` | `1.898` |
| `M_SAT` | `5.683` |
| `R_EARTH` | `6.371` |
| `R_SAT` | `6.033` |
| `YEAR_S` | `3.155` |
| `DAY_S` | `86` |
| `HOUR_S` | `3` |
| `GARG_MASS_SOLAR` | `1.00` |


---

*INTERSTELLAR Code Intelligence · run #1 · 2026-06-23 08:38:02 UTC*
