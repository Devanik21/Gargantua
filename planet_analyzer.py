"""
planet_analyzer.py — Exoplanet Habitability & Planetary Science Engine
ENDURANCE Mission Control | Interstellar Science Platform v3.0.0
═══════════════════════════════════════════════════════════════════════════════
Scientific References:
  [1]  Schulze-Makuch et al. (2011) AsBio 11:1041  [Earth Similarity Index]
  [2]  Kopparapu et al. (2013) ApJ 765:131  [Habitable Zone boundaries]
  [3]  Seager (2013) Science 340:577  [Exoplanet atmospheres]
  [4]  Kasting, Whitmire & Reynolds (1993) Icarus 101:108  [Original HZ]
  [5]  Meadows & Barnes (2018) AsBio 18:630  [Habitability review]
  [6]  Forget & Pierrehumbert (1997) Science 278:1273  [CO₂ greenhouse]
  [7]  Kip Thorne, "The Science of Interstellar" (W.W. Norton, 2014)
  [8]  Pierrehumbert (2010) "Principles of Planetary Climate" Cambridge
  [9]  Leconte et al. (2013) Nature 504:268  [Tidally locked planets]
  [10] Turbet et al. (2016) A&A 596:A112  [Water on Proxima b]
  [11] Segura et al. (2005) AsBio 5:706  [Biosignatures]
  [12] Fujii et al. (2018) AsBio 18:739  [Spectral characterization]

Module implements:
  ┌─ PLANET DATABASE ────────────────────────────────────────────────────────┐
  │ Miller's World  — tidal-locked water world near Gargantua ISCO          │
  │ Mann's Planet   — frozen nitrogen/CO₂ world, icy surface                │
  │ Edmunds' Planet — near-habitable rocky world, Plan B target             │
  │ Earth           — reference standard (all ESI normalised to Earth=1)    │
  │ Custom planet builder — arbitrary input parameters                       │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ HABITABILITY SCORING ───────────────────────────────────────────────────┐
  │ Earth Similarity Index (ESI): radius, density, escape vel, T_surf [1]   │
  │ Interior ESI (iESI): radius, density                                     │
  │ Surface ESI (sESI): escape velocity, surface temperature                │
  │ Standard Habitability Index (SHI): 0–1 composite score                 │
  │ Biological Complexity Index (BCI): energy + liquid water + complexity   │
  │ Habitable Zone boundaries: runaway greenhouse → maximum greenhouse [2,4]│
  │ Continuous Habitable Zone (CHZ): 0.99–4.5 Gyr window                   │
  │ Tidal lock probability: spin-down timescale calculation                 │
  │ UV/X-ray radiation flux at planetary orbit                               │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ ATMOSPHERIC MODELING ──────────────────────────────────────────────────┐
  │ Hydrostatic equilibrium T(z), P(z) profiles (7-layer model)             │
  │ Scale height H = kT/(μg): composition-dependent                         │
  │ Greenhouse effect: CO₂/H₂O radiative forcing (Myhre 1998)              │
  │ Greenhouse temperature correction ΔT_greenhouse                         │
  │ Runaway greenhouse threshold: critical solar flux S_runaway             │
  │ Equilibrium temperature T_eq = T_star(R*/2D)^½(1−A)^¼                 │
  │ Effective temperature T_eff with greenhouse correction                  │
  │ Atmospheric escape: Jeans parameter Λ, thermal escape rate              │
  │ Bond albedo calculation from surface + cloud composition                │
  │ Atmospheric composition: fractional molar abundances                    │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ SPECTRAL ANALYSIS ─────────────────────────────────────────────────────┐
  │ Planetary reflectance spectrum R(λ): Lambertian + Rayleigh              │
  │ Stellar flux F_star(λ): blackbody or tabulated spectrum                 │
  │ Atmospheric absorption: H₂O, CO₂, O₃, CH₄, O₂ bands                   │
  │ Biosignature gases: O₂ 760 nm, O₃ 9.6 μm, CH₄ 7.7 μm, N₂O 17 μm     │
  │ Vegetation red edge at 700 nm (Earth-like biology proxy)                │
  │ Thermal emission: blackbody at T_surface, modulated by atmosphere       │
  │ Phase curve simulation (full-orbit reflected + thermal)                 │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ SURFACE & GEOLOGY ─────────────────────────────────────────────────────┐
  │ Surface gravity g = GM/R²; escape velocity v_esc = √(2GM/R)            │
  │ Tidal heating rate (Peale 1979) from stellar/companion tides            │
  │ Tidal locking timescale t_lock ∝ a⁶/M_star                             │
  │ Ocean coverage model: precipitation − evaporation energy balance        │
  │ Ice albedo feedback: runaway glaciation threshold                        │
  │ Plate tectonics proxy: surface age, volcanic resurfacing                │
  │ Magnetic field proxy: core solidification timescale                     │
  │ Surface pressure from mean molecular weight + column density            │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ MISSION PRIORITY SCORER ───────────────────────────────────────────────┐
  │ Composite mission score: habitability × accessibility × safety          │
  │ Risk matrix: tidal risk, radiation, temperature extremes, chemistry     │
  │ Resource assessment: water, atmosphere, usable land area                │
  │ Plan B colony suitability: embryo survivability, terraforming potential │
  │ Comparative ranking of all candidate planets                            │
  └──────────────────────────────────────────────────────────────────────────┘

"Every planetary surface is a chapter in the universe's biography of life."
                                          — Dr. Brand, NASA, 2063
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import math
import uuid
import warnings
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
import pandas as pd
import scipy.integrate as sci_int
import scipy.optimize  as sci_opt
import scipy.special   as sci_sp
import scipy.interpolate as sci_interp

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot   as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors   as mcolors
import matplotlib.ticker   as mticker
from matplotlib.colors     import LinearSegmentedColormap
from matplotlib.patches    import Circle, FancyArrowPatch

import streamlit as st

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# §1  PHYSICAL & ASTRONOMICAL CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
G_SI      = 6.674_30e-11
C_SI      = 2.997_924_58e8
K_B       = 1.380_649e-23
H_PL      = 6.626_070_15e-34
SIGMA_SB  = 5.670_374_419e-8
M_SUN     = 1.989_000e30
R_SUN     = 6.957_000e8
L_SUN     = 3.828_000e26
M_EARTH   = 5.972_000e24
R_EARTH   = 6.371_000e6
G_EARTH   = 9.806_65
M_ATMO_E  = 5.15e18          # Earth atmosphere mass [kg]
P_SURF_E  = 101_325.0        # Earth surface pressure [Pa]
T_SURF_E  = 288.0            # Earth mean surface temperature [K]
AU        = 1.495_978_707e11
LY        = 9.460_730_472e15
YEAR_S    = 3.155_760e7
AMU       = 1.660_539e-27    # atomic mass unit [kg]
N_A       = 6.022_141e23     # Avogadro number [mol⁻¹]
R_GAS     = 8.314_463        # ideal gas constant [J mol⁻¹ K⁻¹]

# Gargantua host star proxy (Thorne [7]: no star shown; use early K-dwarf)
GARG_STAR_T    = 4500.0      # K  (K2V proxy)
GARG_STAR_L    = 0.36*L_SUN  # W
GARG_STAR_R    = 0.75*R_SUN  # m
GARG_STAR_M    = 0.82*M_SUN  # kg

# ══════════════════════════════════════════════════════════════════════════════
# §2  CUSTOM COLORMAPS
# ══════════════════════════════════════════════════════════════════════════════
CMAP_HABIT = LinearSegmentedColormap.from_list("habitability",
    ["#1a0008","#3d0018","#880030","#cc4400","#ff8800",
     "#c8c000","#80d020","#20c060","#00a0d0","#2060ff"], N=512)

CMAP_SPEC = LinearSegmentedColormap.from_list("spectrum",
    ["#2020c0","#4060ff","#40a0ff","#80e0ff","#c0f0c0",
     "#ffff40","#ffa000","#ff4000","#800000"], N=512)

CMAP_PLANET = LinearSegmentedColormap.from_list("planet_surface",
    ["#000000","#080820","#0a1040","#0a2a60","#104080",
     "#1060a0","#20a0c0","#60c080","#c0d060","#e8c840"], N=256)

# ══════════════════════════════════════════════════════════════════════════════
# §3  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════
class PlanetID(Enum):
    MILLER   = "Miller's World"
    MANN     = "Mann's Planet"
    EDMUNDS  = "Edmunds' Planet"
    EARTH    = "Earth (Reference)"
    CUSTOM   = "Custom Planet"

class HabitabilityClass(Enum):
    SUPERHABITABLE = "Superhabitable  (ESI > 0.80)"
    HABITABLE      = "Potentially Habitable  (0.60–0.80)"
    MARGINALLY     = "Marginally Habitable  (0.40–0.60)"
    UNINHABITABLE  = "Uninhabitable  (0.20–0.40)"
    LETHAL         = "Lethal  (ESI < 0.20)"

class AtmosphereType(Enum):
    NONE         = "Airless"
    THIN_CO2     = "Thin CO₂ (Mars-like)"
    THICK_CO2    = "Dense CO₂ (Venus-like)"
    N2_O2        = "N₂/O₂ (Earth-like)"
    N2_DOMINATED = "N₂-dominated"
    H2_HE        = "H₂/He (gas giant)"
    WATER_VAPOUR = "Water vapour dominated"
    METHANE      = "CH₄/N₂ (Titan-like)"
    EXOTIC       = "Exotic / Unknown"

class SurfaceType(Enum):
    OCEAN        = "Global Ocean"
    ICE          = "Frozen / Ice-covered"
    ROCKY_DRY    = "Rocky / Desert"
    ROCKY_OCEAN  = "Rocky + Ocean"
    LAVA         = "Volcanic / Magma ocean"
    MIXED        = "Mixed terrain"

class TidalState(Enum):
    FREELY_ROTATING = "Freely rotating"
    SPIN_ORBIT_32   = "3:2 spin-orbit resonance"
    SPIN_ORBIT_21   = "2:1 spin-orbit resonance"
    TIDAL_LOCKED    = "Tidally locked (synchronous)"
    FORCED          = "Forced libration"

class MissionRisk(Enum):
    SAFE        = "SAFE"
    CAUTION     = "CAUTION"
    HAZARDOUS   = "HAZARDOUS"
    CRITICAL    = "CRITICAL"
    UNSURVIVABLE= "UNSURVIVABLE"

# ══════════════════════════════════════════════════════════════════════════════
# §4  ATMOSPHERIC COMPOSITION CLASS
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class AtmosphericComposition:
    """
    Molar fraction composition of a planetary atmosphere.
    Fractions must sum to ≤ 1.0 (remainder assumed trace species).
    Mean molecular weight μ computed from composition.
    """
    N2:    float = 0.0
    O2:    float = 0.0
    CO2:   float = 0.0
    H2O:   float = 0.0
    CH4:   float = 0.0
    Ar:    float = 0.0
    H2:    float = 0.0
    He:    float = 0.0
    SO2:   float = 0.0
    N2O:   float = 0.0
    O3:    float = 0.0
    NH3:   float = 0.0
    other: float = 0.0

    # Molecular weights [g/mol]
    _MW = {"N2":28.014,"O2":31.999,"CO2":44.010,"H2O":18.015,
           "CH4":16.043,"Ar":39.948,"H2":2.016,"He":4.003,
           "SO2":64.065,"N2O":44.013,"O3":47.998,"NH3":17.031,"other":30.0}

    def mean_molecular_weight(self) -> float:
        """μ = Σ xᵢ Mᵢ  [g/mol]"""
        total = 0.0
        for sp, mw in self._MW.items():
            total += getattr(self, sp) * mw
        remainder = max(0.0, 1.0 - self.total_fraction())
        total += remainder * 30.0   # default 30 g/mol for trace
        return total

    def total_fraction(self) -> float:
        return sum(getattr(self, sp) for sp in self._MW)

    def greenhouse_forcing_W_m2(self, T_ref: float = 288.0) -> float:
        """
        Approximate radiative forcing from greenhouse gases [W m⁻²].
        Uses simplified Myhre (1998) logarithmic formula for CO₂:
          ΔF_CO₂ = 5.35 × ln(C/C₀)   [W m⁻²], C₀=280 ppm baseline
        H₂O: estimated from fraction × 75 W m⁻² (Earth total GHE).
        CH₄, N₂O: simplified linear terms.
        """
        co2_ppm  = self.CO2 * 1e6
        ch4_ppb  = self.CH4 * 1e9
        n2o_ppb  = self.N2O * 1e9
        dF_co2   = 5.35 * math.log(max(co2_ppm, 1e-6)/280.0)
        dF_h2o   = self.H2O * 75.0
        dF_ch4   = 0.036 * (math.sqrt(max(ch4_ppb, 0)) - math.sqrt(722.0))
        dF_n2o   = 0.12  * (math.sqrt(max(n2o_ppb, 0)) - math.sqrt(270.0))
        return dF_co2 + dF_h2o + dF_ch4 + dF_n2o

    def biosignature_score(self) -> float:
        """
        0–1 score for spectroscopic biosignature detectability.
        Highest for O₂+O₃+CH₄ disequilibrium, also O₂+H₂O.
        """
        o2_score  = min(self.O2 / 0.21, 1.0) * 0.35
        o3_score  = min(self.O3 / 3e-6, 1.0) * 0.20
        ch4_score = min(self.CH4 / 1.7e-6, 1.0) * 0.15
        h2o_score = min(self.H2O / 0.01, 1.0) * 0.20
        n2o_score = min(self.N2O / 3.2e-7, 1.0) * 0.10
        # Chemical disequilibrium bonus (O₂+CH₄ together)
        diseq = 0.0
        if self.O2 > 0.01 and self.CH4 > 1e-6:
            diseq = 0.15
        return min(o2_score + o3_score + ch4_score + h2o_score + n2o_score + diseq, 1.0)

    def to_dict(self) -> Dict[str, float]:
        d = {}
        for sp in self._MW:
            v = getattr(self, sp)
            if v > 0:
                d[sp] = v
        return d

    @classmethod
    def earth_standard(cls) -> "AtmosphericComposition":
        return cls(N2=0.7809, O2=0.2095, Ar=0.0093, CO2=4.2e-4,
                   H2O=0.01, CH4=1.7e-6, N2O=3.2e-7, O3=3e-6)

    @classmethod
    def mars_like(cls) -> "AtmosphericComposition":
        return cls(CO2=0.953, N2=0.027, Ar=0.016, O2=0.0013, H2O=3e-4)

    @classmethod
    def venus_like(cls) -> "AtmosphericComposition":
        return cls(CO2=0.965, N2=0.035, SO2=1.5e-4, H2O=2e-5)

    @classmethod
    def titan_like(cls) -> "AtmosphericComposition":
        return cls(N2=0.984, CH4=0.014, H2=2e-4, Ar=0.0017)

    @classmethod
    def water_world(cls) -> "AtmosphericComposition":
        return cls(N2=0.60, H2O=0.38, CO2=0.015, O2=0.005)

    @classmethod
    def frozen_world(cls) -> "AtmosphericComposition":
        return cls(N2=0.95, CO2=0.048, Ar=0.002)


# ══════════════════════════════════════════════════════════════════════════════
# §5  PLANET DATACLASS — complete physical model
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class Planet:
    """
    Complete planetary physical model.
    All secondary quantities computed automatically from primary inputs.
    """
    name:           str
    planet_id:      PlanetID
    # ── Primary physical parameters ───────────────────────────────────────
    mass_earth:     float          # mass [M_earth]
    radius_earth:   float          # radius [R_earth]
    # ── Orbital parameters ────────────────────────────────────────────────
    semi_major_AU:  float          # semi-major axis [AU]
    eccentricity:   float = 0.0
    inclination_deg:float = 0.0
    # ── Thermal ───────────────────────────────────────────────────────────
    albedo_bond:    float = 0.30   # Bond albedo [0–1]
    # ── Host star ─────────────────────────────────────────────────────────
    star_T_K:       float = GARG_STAR_T
    star_L_W:       float = GARG_STAR_L
    star_M_kg:      float = GARG_STAR_M
    star_R_m:       float = GARG_STAR_R
    # ── Atmosphere ────────────────────────────────────────────────────────
    atm_type:       AtmosphereType = AtmosphereType.N2_DOMINATED
    atm_pressure_Pa:float = P_SURF_E
    composition:    AtmosphericComposition = field(
                        default_factory=AtmosphericComposition.earth_standard)
    # ── Surface ───────────────────────────────────────────────────────────
    surface_type:   SurfaceType  = SurfaceType.ROCKY_OCEAN
    ocean_fraction: float        = 0.70
    ice_fraction:   float        = 0.0
    tidal_state:    TidalState   = TidalState.FREELY_ROTATING
    rotation_period_hr: float    = 24.0
    # ── Internal ──────────────────────────────────────────────────────────
    core_fraction:  float = 0.32    # iron core radius / planet radius
    uid:            str   = field(default_factory=lambda: uuid.uuid4().hex[:8].upper())

    def __post_init__(self):
        # SI quantities
        self.M_kg     = self.mass_earth   * M_EARTH
        self.R_m      = self.radius_earth * R_EARTH
        self.a_m      = self.semi_major_AU * AU
        # Derived: gravity, escape velocity, density
        self.g_surf   = G_SI * self.M_kg / self.R_m**2          # [m/s²]
        self.v_esc    = math.sqrt(2*G_SI*self.M_kg/self.R_m)    # [m/s]
        self.rho_bulk = self.M_kg / (4/3*math.pi*self.R_m**3)   # [kg/m³]
        self.rho_earth_norm = self.rho_bulk / 5514.0             # Earth density=5514
        # Scale height [m] (using composition)
        mu_kg         = self.composition.mean_molecular_weight() * 1e-3 / N_A
        self.H_scale  = K_B * self._T_eq_no_greenhouse() / (mu_kg * self.g_surf)
        # Temperatures
        self.T_eq     = self._T_eq_no_greenhouse()
        self.T_eff    = self._T_effective()
        self.T_surf   = self.T_eff  # updated by atmosphere model
        # Orbital period (Kepler)
        if self.a_m > 0:
            self.period_s = 2*math.pi * math.sqrt(self.a_m**3/(G_SI*self.star_M_kg))
            self.S_flux   = self.star_L_W / (4*math.pi*self.a_m**2)  # [W/m²]
        else:
            self.period_s = 1.7 * 3600.0 # Fallback for Miller's World
            self.S_flux   = self.star_L_W / (4*math.pi*(10.0*AU)**2)
        self.period_yr= self.period_s / YEAR_S
        self.S_earth  = self.S_flux / 1361.0   # normalised to Earth=1

    def _T_eq_no_greenhouse(self) -> float:
        """Equilibrium temperature (no atmosphere):
           T_eq = T_star × (R_star/2a)^½ × (1−A)^¼"""
        if self.a_m <= 0:
            return 290.0 # Fallback temperature (e.g. Miller's World)
        ratio = self.star_R_m / (2.0*self.a_m)
        return self.star_T_K * math.sqrt(ratio) * (1.0-self.albedo_bond)**0.25

    def _T_effective(self) -> float:
        """Effective temperature with greenhouse correction."""
        T0  = self._T_eq_no_greenhouse()
        dF  = self.composition.greenhouse_forcing_W_m2(T0)
        # ΔT_gh from radiative forcing: ΔT = λ·ΔF, λ≈0.8 K/(W/m²)
        dT  = 0.8 * dF
        return T0 + dT

    def surface_gravity_g(self) -> float:
        """Surface gravity normalised to Earth g."""
        return self.g_surf / G_EARTH

    def escape_velocity_kms(self) -> float:
        return self.v_esc / 1000.0

    def flux_incident_W_m2(self) -> float:
        return self.S_flux

    def tidal_lock_timescale_yr(self) -> float:
        """
        Tidal locking spin-down timescale (Gladman 1996):
          t_lock ∝ a⁶ Q R M / (k₂ M_star² R_planet⁵)
        Approximate in years. Q=100 (rocky), k₂=0.3 (Love number).
        """
        Q   = 100.0; k2  = 0.3
        t_s = (Q * self.star_M_kg * self.a_m**6 * self.M_kg
               / (k2 * G_SI * self.star_M_kg**2 * self.R_m**5))
        return t_s / YEAR_S

    def is_tidally_locked(self, star_age_yr: float = 5e9) -> bool:
        return self.tidal_lock_timescale_yr() < star_age_yr


# ══════════════════════════════════════════════════════════════════════════════
# §6  CANONICAL INTERSTELLAR PLANETS
# ══════════════════════════════════════════════════════════════════════════════

def make_miller() -> Planet:
    """
    Miller's World — tidally locked ocean world orbiting Gargantua.
    Key features (Thorne [7]):
      • Massive gravitational time dilation (1h = 7yr Earth)
      • Giant standing wave / tidal bore: 1.2 km high water wall
      • Tidally locked to Gargantua — permanent day/night side
      • Intense tidal heating from Gargantua's gravity gradient
      • Shallow ocean (confirmed by crew: wading depth + waves)
      • No indigenous life (too extreme, too young post-Lazarus)
      • Orbit just outside r_ISCO of Gargantua (near-max Kerr spin)
    """
    comp = AtmosphericComposition.water_world()
    return Planet(
        name          = "Miller's World",
        planet_id     = PlanetID.MILLER,
        mass_earth    = 1.5,          # water world, slightly massive
        radius_earth  = 1.15,         # larger than Earth
        semi_major_AU = 0.0,          # orbiting Gargantua BH (not a star)
        eccentricity  = 0.0,          # circular, tidally circularized
        albedo_bond   = 0.35,         # ocean + partial clouds
        star_T_K      = 4500.0,       # host star (distant, minimal heating)
        star_L_W      = 0.36*L_SUN,
        star_M_kg     = 0.82*M_SUN,
        star_R_m      = 0.75*R_SUN,
        atm_type      = AtmosphereType.WATER_VAPOUR,
        atm_pressure_Pa = 1.8 * P_SURF_E,   # heavier atmosphere, water-rich
        composition   = comp,
        surface_type  = SurfaceType.OCEAN,
        ocean_fraction= 1.0,          # global ocean
        ice_fraction  = 0.0,          # too warm from tidal heating
        tidal_state   = TidalState.TIDAL_LOCKED,
        rotation_period_hr = 1.7,    # orbital period ≈ rotation
        core_fraction = 0.28,
    )

def make_mann() -> Planet:
    """
    Mann's Planet — frozen world with nitrogen/CO₂ ice clouds.
    Key features (Thorne [7]):
      • Cold frozen surface: mean T ~  −80°C (193 K)
      • Dense frozen N₂ atmosphere with CO₂ ice clouds
      • No liquid water — all frozen
      • Towering frozen ammonia/CO₂ cloud formations
      • Dr. Mann's false data: claimed habitable, actually lethal
      • Layered ice structures several km thick
      • Brief habitable temperature windows near equator at noon?
      • Ammonia ice: turns solid at 195 K, partially present
    """
    comp = AtmosphericComposition.frozen_world()
    return Planet(
        name          = "Mann's Planet",
        planet_id     = PlanetID.MANN,
        mass_earth    = 0.85,
        radius_earth  = 0.98,
        semi_major_AU = 1.3,          # beyond outer HZ edge
        eccentricity  = 0.07,
        albedo_bond   = 0.72,         # very high — snow + ice
        star_T_K      = 4500.0,
        star_L_W      = 0.36*L_SUN,
        star_M_kg     = 0.82*M_SUN,
        star_R_m      = 0.75*R_SUN,
        atm_type      = AtmosphereType.THIN_CO2,
        atm_pressure_Pa = 0.08 * P_SURF_E,  # thin frozen atmosphere
        composition   = comp,
        surface_type  = SurfaceType.ICE,
        ocean_fraction= 0.0,
        ice_fraction  = 0.98,
        tidal_state   = TidalState.FREELY_ROTATING,
        rotation_period_hr = 31.5,
        core_fraction = 0.30,
    )

def make_edmunds() -> Planet:
    """
    Edmunds' Planet — the best candidate, Plan B destination.
    Key features (Thorne [7]):
      • Dr. Edmunds confirmed alive (briefly) — favourable signals
      • Rocky planet with thin but breathable atmosphere
      • Surface gravity ~0.9g — comfortable for colonists
      • Temperatures survivable near equator: −20 to +35°C
      • Some liquid water exists (confirmed by Edmunds' signal)
      • Plan B embryo colony target — 5000 embryos
      • Wind storms persistent but manageable
      • Best ESI of the three candidates
    """
    comp = AtmosphericComposition(N2=0.77, O2=0.12, CO2=0.002,
                                   H2O=0.008, Ar=0.010, CH4=5e-6,
                                   N2O=1e-7, O3=1e-6, other=0.09)
    return Planet(
        name          = "Edmunds' Planet",
        planet_id     = PlanetID.EDMUNDS,
        mass_earth    = 0.92,
        radius_earth  = 0.97,
        semi_major_AU = 0.88,          # inner edge of HZ for K-star
        eccentricity  = 0.04,
        albedo_bond   = 0.28,
        star_T_K      = 4500.0,
        star_L_W      = 0.36*L_SUN,
        star_M_kg     = 0.82*M_SUN,
        star_R_m      = 0.75*R_SUN,
        atm_type      = AtmosphereType.N2_O2,
        atm_pressure_Pa = 0.75 * P_SURF_E,
        composition   = comp,
        surface_type  = SurfaceType.ROCKY_OCEAN,
        ocean_fraction= 0.42,
        ice_fraction  = 0.05,
        tidal_state   = TidalState.FREELY_ROTATING,
        rotation_period_hr = 22.4,
        core_fraction = 0.31,
    )

def make_earth() -> Planet:
    """Earth — the reference standard for all ESI calculations."""
    return Planet(
        name          = "Earth",
        planet_id     = PlanetID.EARTH,
        mass_earth    = 1.0,
        radius_earth  = 1.0,
        semi_major_AU = 1.0,
        eccentricity  = 0.017,
        albedo_bond   = 0.306,
        star_T_K      = 5778.0,
        star_L_W      = L_SUN,
        star_M_kg     = M_SUN,
        star_R_m      = R_SUN,
        atm_type      = AtmosphereType.N2_O2,
        atm_pressure_Pa = P_SURF_E,
        composition   = AtmosphericComposition.earth_standard(),
        surface_type  = SurfaceType.ROCKY_OCEAN,
        ocean_fraction= 0.71,
        ice_fraction  = 0.03,
        tidal_state   = TidalState.FREELY_ROTATING,
        rotation_period_hr = 23.93,
        core_fraction = 0.32,
    )

PLANET_REGISTRY: Dict[str, Planet] = {
    PlanetID.MILLER.value:  make_miller(),
    PlanetID.MANN.value:    make_mann(),
    PlanetID.EDMUNDS.value: make_edmunds(),
    PlanetID.EARTH.value:   make_earth(),
}


# ══════════════════════════════════════════════════════════════════════════════
# §7  HABITABILITY SCORING ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class HabitabilityScorer:
    """
    Multi-index habitability scoring system.
    Implements ESI [1], Habitable Zone analysis [2,4],
    and composite LAZARUS mission priority score.
    """

    # Earth reference values for ESI normalisation
    _REF = {
        "radius_earth":    1.0,
        "rho_norm":        1.0,   # Earth density normalised
        "v_esc_km":        11.186,
        "T_surf_K":        288.0,
    }
    # ESI weights (Schulze-Makuch 2011 [1])
    _W = {
        "radius_earth": 0.57,
        "rho_norm":     1.07,
        "v_esc_km":     0.70,
        "T_surf_K":     5.58,
    }
    _N_PARAMS = 4   # number of parameters in ESI product

    def __init__(self):
        self.earth = make_earth()

    # ── §7.1  Earth Similarity Index ─────────────────────────────────────────
    def _esi_term(self, x: float, x_ref: float, w: float) -> float:
        """
        Single ESI factor: 1 − |x−x_ref|/(x+x_ref) raised to w/n.
        Bounded [0,1].
        """
        if x + x_ref == 0:
            return 0.0
        ratio = abs(x - x_ref) / (x + x_ref)
        return (1.0 - ratio)**(w / self._N_PARAMS)

    def interior_ESI(self, p: Planet) -> float:
        """
        Interior ESI — size and density similarity to Earth [1]:
          iESI = [∏ (1−|xᵢ−xᵢ,☁|/(xᵢ+xᵢ,☁))^(wᵢ/n)]
        Parameters: radius, bulk density.
        """
        r_term   = self._esi_term(p.radius_earth, self._REF["radius_earth"],
                                   self._W["radius_earth"])
        rho_term = self._esi_term(p.rho_earth_norm, self._REF["rho_norm"],
                                   self._W["rho_norm"])
        return r_term * rho_term

    def surface_ESI(self, p: Planet) -> float:
        """
        Surface ESI — escape velocity and surface temperature similarity [1]:
        Parameters: escape velocity [km/s], mean surface temperature [K].
        """
        v_km     = p.v_esc / 1000.0
        T        = p.T_surf
        ve_term  = self._esi_term(v_km, self._REF["v_esc_km"],
                                   self._W["v_esc_km"])
        T_term   = self._esi_term(T,    self._REF["T_surf_K"],
                                   self._W["T_surf_K"])
        return ve_term * T_term

    def global_ESI(self, p: Planet) -> float:
        """
        Global ESI = (iESI × sESI)^½  [1].
        ESI = 1.0 → identical to Earth.
        ESI > 0.8 → considered Earth-like by Schulze-Makuch (2011).
        """
        return math.sqrt(self.interior_ESI(p) * self.surface_ESI(p))

    def classify(self, esi: float) -> HabitabilityClass:
        if esi >= 0.80: return HabitabilityClass.SUPERHABITABLE
        if esi >= 0.60: return HabitabilityClass.HABITABLE
        if esi >= 0.40: return HabitabilityClass.MARGINALLY
        if esi >= 0.20: return HabitabilityClass.UNINHABITABLE
        return HabitabilityClass.LETHAL

    # ── §7.2  Habitable Zone boundaries (Kopparapu 2013 [2]) ─────────────────
    def habitable_zone_AU(self, T_star: float, L_star_sol: float
                           ) -> Dict[str, float]:
        """
        Habitable Zone boundaries using Kopparapu et al. (2013) coefficients [2].
        For T_star ∈ [2600, 7200] K.
        Four boundaries:
          Recent Venus (inner, optimistic)
          Runaway Greenhouse (inner, conservative)
          Maximum Greenhouse (outer, conservative)
          Early Mars (outer, optimistic)
        S_eff = S_eff_sun + a·T' + b·T'² + c·T'³ + d·T'⁴   where T' = T_star − 5780
        d = √(L_star/S_eff) [AU]
        """
        T_prime = T_star - 5780.0

        # Kopparapu 2013 Table 3 coefficients (Sun-like to cool star)
        coeff = {
            "recent_venus":       (1.7763, 1.4335e-4, 3.3954e-9, -7.6364e-12, -1.1950e-15),
            "runaway_greenhouse": (1.0385, 1.2456e-4, 1.4612e-8, -7.6345e-12, -1.7511e-15),
            "moist_greenhouse":   (1.0146, 8.1884e-5, 1.9394e-9, -4.3618e-12, -6.8260e-16),
            "max_greenhouse":     (0.3507, 5.9578e-5, 1.6707e-9, -3.0058e-12, -5.1925e-16),
            "early_mars":         (0.3207, 5.4471e-5, 1.5275e-9, -2.1709e-12, -3.8282e-16),
        }
        hz = {}
        for name, (a0,a1,a2,a3,a4) in coeff.items():
            S_eff = a0 + a1*T_prime + a2*T_prime**2 + a3*T_prime**3 + a4*T_prime**4
            S_eff = max(S_eff, 1e-5)
            d_AU  = math.sqrt(L_star_sol / S_eff)
            hz[name] = d_AU
        hz["conservative_inner"] = hz["runaway_greenhouse"]
        hz["conservative_outer"] = hz["max_greenhouse"]
        hz["optimistic_inner"]   = hz["recent_venus"]
        hz["optimistic_outer"]   = hz["early_mars"]
        return hz

    def hz_class(self, p: Planet) -> str:
        """Classify planet as inside/outside habitable zone."""
        L_sol = p.star_L_W / L_SUN
        hz    = self.habitable_zone_AU(p.star_T_K, L_sol)
        a     = p.semi_major_AU
        if a <= 0:
            return "N/A — orbiting black hole"
        if hz["optimistic_inner"] <= a <= hz["conservative_inner"]:
            return "Inner Optimistic HZ"
        elif hz["conservative_inner"] < a <= hz["conservative_outer"]:
            return "Conservative HZ ✓"
        elif hz["conservative_outer"] < a <= hz["optimistic_outer"]:
            return "Outer Optimistic HZ"
        elif a < hz["optimistic_inner"]:
            return "Too Hot — Inside inner HZ"
        else:
            return "Too Cold — Outside outer HZ"

    # ── §7.3  Composite scores ────────────────────────────────────────────────
    def standard_habitability_index(self, p: Planet) -> float:
        """
        Standard Habitability Index (SHI) — weighted composite [5]:
          SHI = 0.25(T_score) + 0.25(water_score) + 0.25(atm_score) + 0.25(bio_score)
        Each sub-score 0–1.
        """
        # Temperature score: Gaussian centred on 295K, σ=50K
        T_score = math.exp(-0.5*((p.T_surf - 295.0)/50.0)**2)
        # Liquid water score
        T_liq   = 273.15 <= p.T_surf <= 373.15
        p_ok    = p.atm_pressure_Pa > 600.0  # triple point
        water_score = p.ocean_fraction * (1.0 if (T_liq and p_ok) else 0.0)
        # Atmosphere score
        if p.atm_type == AtmosphereType.NONE:
            atm_score = 0.0
        elif p.atm_type == AtmosphereType.N2_O2:
            atm_score = 0.9
        elif p.atm_type in (AtmosphereType.N2_DOMINATED, AtmosphereType.WATER_VAPOUR):
            atm_score = 0.5
        else:
            atm_score = 0.2
        # Biosignature score
        bio_score = p.composition.biosignature_score()
        return 0.25*(T_score + water_score + atm_score + bio_score)

    def biological_complexity_index(self, p: Planet) -> float:
        """
        BCI — proxy for potential biological complexity [5]:
          BCI = energy_availability × liquid_water × chemical_diversity
        Ranges 0–1; Earth ≈ 0.72.
        """
        # Energy from star (photosynthesis window: 400–700 nm)
        # Approximate: fraction of stellar output in PAR band
        T_s   = p.star_T_K
        par_frac = max(0.0, min(1.0, (T_s - 2500.0)/5000.0))  # rough proxy
        S_norm  = min(p.S_earth, 2.0) / 2.0
        energy  = par_frac * S_norm
        # Liquid water availability
        T_in_range = 273.15 <= p.T_surf <= 373.15
        p_in_range = p.atm_pressure_Pa > 600.0
        liquid_w = p.ocean_fraction if (T_in_range and p_in_range) else 0.0
        # Chemical complexity (N,O,C,H availability)
        chem = (min(p.composition.N2 / 0.78, 1.0) * 0.3 +
                min(p.composition.O2 / 0.21, 1.0) * 0.3 +
                min(p.composition.CO2 / 4e-4, 10.0)/10.0 * 0.2 +
                min(p.composition.H2O / 0.01, 1.0) * 0.2)
        return energy * 0.35 + liquid_w * 0.40 + chem * 0.25

    def mission_priority_score(self, p: Planet) -> Dict[str, float]:
        """
        Composite mission priority for LAZARUS/ENDURANCE missions.
        Factors: habitability (ESI, SHI, BCI), safety, accessibility,
                 Plan B suitability.
        """
        esi  = self.global_ESI(p)
        shi  = self.standard_habitability_index(p)
        bci  = self.biological_complexity_index(p)
        # Safety score (lower is safer)
        g_ratio   = p.surface_gravity_g()
        T_ok      = 1.0 - abs(p.T_surf - 295.0)/200.0
        T_ok      = max(0.0, T_ok)
        rad_ok    = max(0.0, 1.0 - p.S_earth*0.3)   # proxy for UV/X-ray
        safety    = 0.4*T_ok + 0.3*max(0,1-(g_ratio-1)**2) + 0.3*rad_ok
        # Accessibility (orbit distance proxy)
        acc       = max(0.0, 1.0 - p.semi_major_AU/3.0) if p.semi_major_AU > 0 else 0.5
        # Plan B: embryo colony suitability
        planB     = 0.4*esi + 0.3*safety + 0.3*(p.ocean_fraction*0.5 + 0.5)
        # Overall
        overall   = 0.30*esi + 0.20*shi + 0.15*bci + 0.20*safety + 0.15*acc
        return {
            "ESI":        esi,  "SHI": shi, "BCI": bci,
            "safety":     safety, "accessibility": acc,
            "plan_B_score": planB,
            "overall_priority": overall,
        }

    def full_report(self, p: Planet) -> Dict[str, Any]:
        """Generate complete habitability report for one planet."""
        scores = self.mission_priority_score(p)
        L_sol  = p.star_L_W / L_SUN
        hz     = self.habitable_zone_AU(p.star_T_K, L_sol)
        return {
            "name":                 p.name,
            "planet_id":            p.planet_id.value,
            "mass_earth":           p.mass_earth,
            "radius_earth":         p.radius_earth,
            "g_surf_ms2":           p.g_surf,
            "g_surf_earth":         p.surface_gravity_g(),
            "v_esc_kms":            p.escape_velocity_kms(),
            "rho_bulk_kgm3":        p.rho_bulk,
            "rho_norm_earth":       p.rho_earth_norm,
            "T_eq_K":               p.T_eq,
            "T_eff_K":              p.T_eff,
            "T_surf_K":             p.T_surf,
            "T_surf_C":             p.T_surf - 273.15,
            "S_flux_Wm2":           p.S_flux,
            "S_earth_norm":         p.S_earth,
            "albedo_bond":          p.albedo_bond,
            "atm_pressure_Pa":      p.atm_pressure_Pa,
            "atm_pressure_bar":     p.atm_pressure_Pa/1e5,
            "scale_height_m":       p.H_scale,
            "ocean_fraction":       p.ocean_fraction,
            "ice_fraction":         p.ice_fraction,
            "period_yr":            p.period_yr,
            "tidal_lock_yr":        p.tidal_lock_timescale_yr(),
            "tidal_locked_5Gyr":    p.is_tidally_locked(),
            "hz_class":             self.hz_class(p),
            "hz_conservative_in":   hz["conservative_inner"],
            "hz_conservative_out":  hz["conservative_outer"],
            "iESI":                 self.interior_ESI(p),
            "sESI":                 self.surface_ESI(p),
            "biosig_score":         p.composition.biosignature_score(),
            **scores,
            "habitability_class":   self.classify(scores["ESI"]).value,
        }

    def comparative_table(self, planets: Optional[List[Planet]] = None
                           ) -> pd.DataFrame:
        """Build comparative ranking DataFrame for all planets."""
        if planets is None:
            planets = list(PLANET_REGISTRY.values())
        rows = [self.full_report(p) for p in planets]
        df   = pd.DataFrame(rows)
        df   = df.sort_values("overall_priority", ascending=False)
        return df


# ══════════════════════════════════════════════════════════════════════════════
# §8  ATMOSPHERIC SCIENCE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class AtmosphericEngine:
    """
    Planetary atmosphere physics: vertical structure, spectral properties,
    escape, greenhouse, and climate modeling.
    References: Pierrehumbert [8], Seager [3], Kasting [4].
    """

    def __init__(self, planet: Planet):
        self.p = planet

    # ── §8.1  Vertical T-P profile ────────────────────────────────────────────
    def lapse_rate_K_per_km(self) -> float:
        """
        Moist adiabatic lapse rate approximation:
          Γ_d = g/c_p   (dry adiabat)
          Γ_m ≈ Γ_d × (1 − water_fraction × 0.5)  (moist correction)
        c_p from composition.
        """
        mu_g    = self.p.composition.mean_molecular_weight()  # g/mol
        c_p_si  = 1004.0 * (28.97/mu_g)   # J/(kg K), scaled from air
        gamma_d = self.p.g_surf / c_p_si * 1000.0  # K/km
        gamma_m = gamma_d * (1.0 - self.p.composition.H2O * 0.5)
        return max(gamma_m, 0.5)

    def temperature_profile(self, n_layers: int = 50
                             ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        7-layer-style vertical T–P–z profile using hydrostatic balance.
          dP/dz = −ρg = −PMg/(kT)
          T(z)  = T_surf − Γ·z  (troposphere) + stratospheric inversion
        Returns (z_km, T_K, P_Pa) arrays.
        """
        P0   = self.p.atm_pressure_Pa
        T0   = self.p.T_surf
        Gamma= self.lapse_rate_K_per_km()    # K/km
        g    = self.p.g_surf
        mu   = self.p.composition.mean_molecular_weight() * 1e-3 / N_A  # kg

        H = self.p.H_scale / 1000.0   # km
        # Tropopause height ~ 2H for Earth-like, scaled
        z_trop = 12.0 * (self.p.H_scale / 8500.0)  # km

        z_arr = np.linspace(0, 6.0*self.p.H_scale/1000.0, n_layers)
        T_arr = np.zeros(n_layers)
        P_arr = np.zeros(n_layers)

        for i, z in enumerate(z_arr):
            if z <= z_trop:
                T_arr[i] = max(T0 - Gamma*z, 50.0)
            else:
                # Simple stratosphere: isothermal + slight warming
                T_trop   = max(T0 - Gamma*z_trop, 50.0)
                T_arr[i] = T_trop + 2.0*(z - z_trop)/z_trop * 10.0
            # Hydrostatic
            P_arr[i] = P0 * math.exp(-z*1000.0 / self.p.H_scale)

        return z_arr, T_arr, P_arr

    # ── §8.2  Atmospheric escape ──────────────────────────────────────────────
    def jeans_parameter(self, species_mass_amu: float = 28.0,
                         z_exobase_km: float = None) -> float:
        """
        Jeans escape parameter λ = GMm/(kT R_exobase):
        λ > 20 → stable (negligible thermal escape)
        λ < 1  → blowoff (catastrophic escape)
        λ ~ 3–20 → Jeans escape
        """
        if z_exobase_km is None:
            z_exobase_km = 10.0 * self.p.H_scale / 1000.0
        R_exo = self.p.R_m + z_exobase_km*1000.0
        m_sp  = species_mass_amu * AMU
        T_exo = max(self.p.T_surf * 1.2, 200.0)  # exobase hotter
        return G_SI*self.p.M_kg*m_sp / (K_B*T_exo*R_exo)

    def jeans_escape_rate(self, species_mass_amu: float = 28.0
                           ) -> float:
        """
        Thermal Jeans escape rate [particles/s]:
          Φ_J = n_exo × v_th/4 × (1 + λ) × exp(−λ)
        n_exo estimated from surface density × exp(−z_exo/H).
        Units: kg/s.
        """
        lam    = self.jeans_parameter(species_mass_amu)
        if lam > 50:
            return 0.0  # negligible
        m_sp   = species_mass_amu * AMU
        T_exo  = max(self.p.T_surf * 1.2, 200.0)
        v_th   = math.sqrt(2*K_B*T_exo/m_sp)   # thermal speed [m/s]
        z_exo  = 10.0*self.p.H_scale
        n_surf = self.p.atm_pressure_Pa / (K_B*self.p.T_surf)  # [m⁻³]
        n_exo  = n_surf * math.exp(-z_exo/self.p.H_scale)
        R_exo  = self.p.R_m + z_exo
        Phi    = n_exo * v_th/4.0 * (1+lam) * math.exp(-lam)
        return Phi * m_sp * 4*math.pi*R_exo**2   # kg/s

    def atmosphere_lifetime_yr(self, species_mass_amu: float = 28.0) -> float:
        """Atmosphere mass / escape rate [yr]."""
        rate = self.jeans_escape_rate(species_mass_amu)
        if rate < 1e-30:
            return 1e20   # essentially permanent
        # Approximate atmospheric mass
        M_atm = self.p.atm_pressure_Pa * 4*math.pi*self.p.R_m**2 / self.p.g_surf
        return M_atm / (rate * YEAR_S)

    # ── §8.3  Runaway greenhouse ──────────────────────────────────────────────
    def runaway_greenhouse_flux(self) -> float:
        """
        Critical stellar flux for runaway greenhouse (Kasting 1993 [4]):
          S_runaway ≈ 1.06 × S_earth = 1440 W/m²  (for Earth-mass H₂O world)
        Scales with surface gravity: S_runaway ∝ g^½
        """
        S_base = 1440.0   # W/m²  (Earth-like)
        g_scale = math.sqrt(self.p.surface_gravity_g())
        return S_base * g_scale

    def is_runaway_greenhouse(self) -> bool:
        """Check if planet is beyond runaway greenhouse limit."""
        return self.p.S_flux > self.runaway_greenhouse_flux()

    def maximum_greenhouse_flux(self) -> float:
        """
        Outer limit: maximum greenhouse effect (CO₂ condensation stops [4]):
          S_max_GH ≈ 0.36 × S_earth = 490 W/m²  (1 M_earth)
        """
        S_base = 490.0
        g_scale = math.sqrt(self.p.surface_gravity_g())
        return S_base * g_scale

    def greenhouse_T_increment(self) -> float:
        """
        Surface temperature increment from greenhouse effect:
          T_surf = T_eq + ΔT_gh
        ΔT_gh = (climate_sensitivity × ΔF_forcing) [K]
        Earth climate sensitivity λ ≈ 0.8 K/(W/m²).
        """
        dF  = self.p.composition.greenhouse_forcing_W_m2(self.p.T_eq)
        return 0.8 * dF

    # ── §8.4  UV/X-ray flux and radiation environment ─────────────────────────
    def stellar_uv_flux_ratio(self) -> float:
        """
        UV flux normalised to Earth (280–400 nm).
        Approximate: F_UV/F_UV,earth ≈ (T_star/5780)^4 × L_star/L_sun
        K-dwarf stars have lower UV than solar.
        """
        T_ratio = (self.p.star_T_K / 5778.0)**4
        L_ratio = self.p.star_L_W / L_SUN
        d_ratio = (1.0 / max(self.p.semi_major_AU, 0.01))**2
        return T_ratio * L_ratio * d_ratio

    def surface_uv_dose_W_m2(self) -> float:
        """UV dose reaching surface (attenuated by O₃ column)."""
        uv_space = self.stellar_uv_flux_ratio() * 5.0  # ~5 W/m² on Earth
        o3_shield = min(self.p.composition.O3 / 3e-6, 1.0)
        return uv_space * (1.0 - 0.95*o3_shield)

    # ── §8.5  Climate stability metrics ──────────────────────────────────────
    def ice_albedo_feedback(self) -> float:
        """
        Ice-albedo feedback amplification factor.
        Higher ice fraction → higher albedo → colder → more ice (runaway).
        Feedback factor: f = ∂A/∂T × ∂T/∂S  (simplified)
        Returns dimensionless gain factor.
        """
        # Simplified: if ice_fraction > 0.6 → runaway glaciation likely
        if self.p.ice_fraction > 0.6:
            return 2.5   # strong positive feedback
        elif self.p.ice_fraction > 0.3:
            return 1.5
        else:
            return 1.0

    def weathering_co2_feedback(self) -> float:
        """
        Silicate weathering (carbon-silicate cycle) CO₂ stabilisation.
        On warm rocky planets: CO₂ drawn down; on cold: volcanoes supply.
        Returns stability index: >1 → negative feedback active.
        """
        if self.p.surface_type == SurfaceType.OCEAN:
            return 0.0  # water world, no silicate weathering
        if self.p.T_surf < 240:
            return 0.2  # too cold for liquid water weathering
        return 0.8 + 0.2*(self.p.T_surf - 240.0)/(50.0)


# ══════════════════════════════════════════════════════════════════════════════
# §9  SPECTRAL ANALYSIS ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class SpectralEngine:
    """
    Planetary spectroscopy: reflected light, thermal emission,
    absorption features, biosignatures.
    References: Seager [3], Segura [11], Fujii [12].
    """

    # Absorption band centres and widths [μm]
    ABSORPTION_BANDS = {
        "H2O_vis":  (0.720, 0.050),   "H2O_nir1": (0.940, 0.060),
        "H2O_nir2": (1.140, 0.080),   "H2O_nir3": (1.380, 0.100),
        "H2O_mir":  (2.700, 0.300),   "H2O_far":  (6.300, 1.000),
        "CO2_nir1": (1.600, 0.050),   "CO2_nir2": (2.010, 0.080),
        "CO2_mir":  (4.260, 0.250),   "CO2_15um": (15.00, 3.000),
        "O2_A":     (0.760, 0.005),   "O2_B":     (0.688, 0.003),
        "O3_chapp": (0.500, 0.200),   "O3_har":   (9.600, 1.500),
        "CH4_nir":  (1.670, 0.050),   "CH4_mir":  (3.310, 0.150),
        "CH4_7um":  (7.700, 1.000),   "N2O_17":   (17.00, 2.000),
        "N2O_nir":  (2.870, 0.060),
    }

    def __init__(self, planet: Planet):
        self.p = planet

    def stellar_spectrum(self, wl_um: np.ndarray) -> np.ndarray:
        """
        Stellar flux at planet [W/m²/μm] — Planck blackbody.
        """
        T     = self.p.star_T_K
        L_au2 = self.p.star_L_W / (4*math.pi*self.p.a_m**2) if self.p.a_m > 0 else 0.0
        wl_m  = wl_um * 1e-6
        x     = H_PL*C_SI / (K_B*T*wl_m)
        x     = np.clip(x, 1e-5, 700)
        B_nu  = 2*H_PL*C_SI**2/wl_m**5 / (np.exp(x)-1)
        # Normalise to incident flux
        norm = trapz(B_nu, wl_m)
        if norm > 0:
            B_nu = B_nu / norm * L_au2
        return B_nu   # W/m²/m → convert

    def rayleigh_scattering(self, wl_um: np.ndarray) -> np.ndarray:
        """
        Rayleigh scattering optical depth τ_R ∝ λ⁻⁴ × P/g × composition.
        Returns albedo contribution (0–1).
        """
        N2_frac = self.p.composition.N2
        P_rel   = self.p.atm_pressure_Pa / P_SURF_E
        tau_R   = 0.095 * P_rel * N2_frac * (0.55/wl_um)**4
        return 1.0 - np.exp(-tau_R)   # Rayleigh albedo

    def _absorption_depth(self, wl_um: np.ndarray,
                           species: str, fraction: float) -> np.ndarray:
        """Gaussian absorption feature centred at band centre."""
        if species not in self.ABSORPTION_BANDS:
            return np.zeros_like(wl_um)
        centre, width = self.ABSORPTION_BANDS[species]
        # Depth proportional to column density (log scale for realism)
        ref_frac = 1e-4
        depth = min(fraction/ref_frac * 0.5, 0.98) if fraction > 0 else 0.0
        gauss = depth * np.exp(-0.5*((wl_um-centre)/width)**2)
        return np.clip(gauss, 0, 1)

    def reflectance_spectrum(self, wl_um: np.ndarray) -> np.ndarray:
        """
        Planetary geometric albedo spectrum (0–1):
          R(λ) = A_surface(λ) × τ_window(λ) + A_Rayleigh(λ) − Σ absorption
        Includes: surface reflectance, Rayleigh scattering, H₂O/CO₂/O₂/O₃
        absorption, vegetation red edge.
        """
        c   = self.p.composition
        # Base surface albedo by type
        if self.p.surface_type == SurfaceType.OCEAN:
            A_surf = 0.06 + 0.02*np.sin(wl_um*2)   # ocean + slight variation
        elif self.p.surface_type == SurfaceType.ICE:
            A_surf = 0.75 + 0.05*np.cos(wl_um*3)
        elif self.p.surface_type == SurfaceType.ROCKY_DRY:
            A_surf = 0.25 * np.ones_like(wl_um)
        elif self.p.surface_type == SurfaceType.ROCKY_OCEAN:
            A_surf = 0.15 + 0.10*self.p.ocean_fraction * np.ones_like(wl_um)
        else:
            A_surf = 0.20 * np.ones_like(wl_um)

        # Vegetation red edge (700 nm) if biosignature_score > 0.3
        if c.biosignature_score() > 0.3:
            red_edge = 0.15 * (1.0 + np.tanh((wl_um - 0.70)*30.0)) * 0.5
            A_surf  += red_edge * (1.0 - self.p.ocean_fraction)

        # Rayleigh scattering
        ray  = self.rayleigh_scattering(wl_um)

        # Start from surface + Rayleigh
        R    = (1.0 - ray)*A_surf + ray * 0.5

        # Subtract absorption bands
        for sp, frac in [("H2O_vis", c.H2O), ("H2O_nir1", c.H2O),
                          ("H2O_nir2", c.H2O), ("H2O_nir3", c.H2O),
                          ("CO2_nir1", c.CO2), ("CO2_nir2", c.CO2),
                          ("O2_A",     c.O2),  ("O2_B",     c.O2),
                          ("O3_chapp", c.O3),
                          ("CH4_nir",  c.CH4)]:
            R -= self._absorption_depth(wl_um, sp, frac)

        R = np.clip(R, 0.0, 1.0)
        return R

    def thermal_emission_spectrum(self, wl_um: np.ndarray) -> np.ndarray:
        """
        Thermal emission from planet surface [W/m²/μm]:
          B_λ(T_surf) × emissivity(λ)
        Emissivity reduced in H₂O and CO₂ windows.
        """
        T    = self.p.T_surf
        wl_m = wl_um * 1e-6
        x    = H_PL*C_SI / (K_B*T*wl_m)
        x    = np.clip(x, 1e-5, 700)
        B    = 2*H_PL*C_SI**2/wl_m**5 / (np.exp(x)-1)
        # Emissivity (reduced in window regions)
        eps  = np.ones_like(wl_um)
        c    = self.p.composition
        for sp, frac in [("H2O_far", c.H2O), ("CO2_15um", c.CO2),
                          ("O3_har",  c.O3),  ("CH4_7um",  c.CH4),
                          ("N2O_17",  c.N2O)]:
            eps -= self._absorption_depth(wl_um, sp, frac)
        eps = np.clip(eps, 0.05, 1.0)
        return B * eps * 1e-6   # convert W/m²/m → W/m²/μm

    def combined_spectrum(self, wl_um_vis: np.ndarray,
                           wl_um_ir: np.ndarray
                           ) -> Dict[str, np.ndarray]:
        """Full spectrum: reflected (VIS) + thermal (IR)."""
        F_star = self.stellar_spectrum(wl_um_vis)
        R_vis  = self.reflectance_spectrum(wl_um_vis)
        F_refl = F_star * R_vis

        F_therm = self.thermal_emission_spectrum(wl_um_ir)
        bio_score = self.p.composition.biosignature_score()
        return {
            "wl_vis": wl_um_vis, "F_reflected": F_refl,
            "reflectance": R_vis, "F_star": F_star,
            "wl_ir": wl_um_ir, "F_thermal": F_therm,
            "biosig_score": bio_score,
        }

    def biosignature_feature_table(self) -> pd.DataFrame:
        """Table of biosignature absorption features and their detectability."""
        c   = self.p.composition
        wl_arr = np.linspace(0.3, 20.0, 2000)
        rows = []
        features = [
            ("O₂ A-band",       "O2_A",     c.O2,  0.3,  "Definitive photosynthesis marker"),
            ("O₃ 9.6 μm",       "O3_har",   c.O3,  0.01, "Stratospheric O₂ proxy"),
            ("CH₄ 7.7 μm",      "CH4_7um",  c.CH4, 1.7e-6, "Biogenic/abiotic CH₄"),
            ("N₂O 17 μm",       "N2O_17",   c.N2O, 3.2e-7, "Exclusively biogenic"),
            ("H₂O 6.3 μm",      "H2O_far",  c.H2O, 0.01,  "Liquid water indicator"),
            ("CO₂ 15 μm",       "CO2_15um", c.CO2, 4e-4,  "Atmospheric pressure probe"),
            ("O₂+CH₄ diseq",    None,        0,     0,     "Thermodynamic disequilibrium"),
        ]
        for fname, band_key, frac, earth_frac, note in features:
            if band_key is not None:
                depth = self._absorption_depth(wl_arr, band_key, frac)
                max_depth = float(np.max(depth))
            else:
                max_depth = float(c.O2 > 0.01 and c.CH4 > 1e-6)
            detectability = "STRONG" if max_depth > 0.3 else "WEAK" if max_depth > 0.05 else "ABSENT"
            ratio = frac/earth_frac if earth_frac > 0 else 0.0
            rows.append({
                "Feature": fname, "Max depth": round(max_depth, 3),
                "Detectability": detectability,
                "Planet/Earth ratio": f"{ratio:.2e}",
                "Notes": note,
            })
        return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# §10  MISSION RISK ASSESSOR
# ══════════════════════════════════════════════════════════════════════════════
class MissionRiskAssessor:
    """
    Comprehensive risk matrix for crew survival on each planet.
    Covers temperature, pressure, gravity, radiation, chemistry, tidal forces.
    """

    HUMAN_LIMITS = {
        "T_min_K":          240.0,   # minimum survivable (suited)
        "T_max_K":          330.0,   # maximum survivable (suited)
        "P_min_Pa":         6000.0,  # Armstrong limit
        "P_max_Pa":         600000.0,# 6 bar
        "g_min_earth":      0.16,    # Moon gravity (long-term tolerable)
        "g_max_earth":      2.0,     # 2g sustained limit
        "uv_max_W_m2":      20.0,    # unprotected skin limit
        "tidal_max_g_per_m":1.0,     # lethal tidal force threshold
    }

    def __init__(self, planet: Planet):
        self.p   = planet
        self.atm = AtmosphericEngine(planet)

    def temperature_risk(self) -> Tuple[MissionRisk, str]:
        T = self.p.T_surf
        L = self.HUMAN_LIMITS
        if L["T_min_K"] <= T <= L["T_max_K"]:
            return MissionRisk.SAFE, f"T={T-273:.0f}°C — within suited range"
        if T < 200 or T > 370:
            return MissionRisk.UNSURVIVABLE, f"T={T-273:.0f}°C — extreme"
        if T < L["T_min_K"]:
            return MissionRisk.HAZARDOUS, f"T={T-273:.0f}°C — suits required"
        return MissionRisk.CAUTION, f"T={T-273:.0f}°C — thermal management needed"

    def pressure_risk(self) -> Tuple[MissionRisk, str]:
        P = self.p.atm_pressure_Pa
        L = self.HUMAN_LIMITS
        if P < L["P_min_Pa"]:
            return MissionRisk.UNSURVIVABLE, f"P={P:.0f}Pa — below Armstrong limit"
        if P < 0.5*P_SURF_E:
            return MissionRisk.HAZARDOUS, f"P={P/1e3:.1f}kPa — pressure suit needed"
        if P > L["P_max_Pa"]:
            return MissionRisk.CRITICAL, f"P={P/1e5:.1f}bar — crush risk"
        if P > 2*P_SURF_E:
            return MissionRisk.CAUTION, f"P={P/1e5:.2f}bar — elevated pressure"
        return MissionRisk.SAFE, f"P={P/1e3:.1f}kPa — nominal"

    def gravity_risk(self) -> Tuple[MissionRisk, str]:
        g = self.p.surface_gravity_g()
        L = self.HUMAN_LIMITS
        if L["g_min_earth"] <= g <= L["g_max_earth"]:
            return MissionRisk.SAFE, f"g={g:.2f}g — tolerable"
        if g > 3.0 or g < 0.05:
            return MissionRisk.UNSURVIVABLE, f"g={g:.2f}g — extreme"
        if g > L["g_max_earth"]:
            return MissionRisk.HAZARDOUS, f"g={g:.2f}g — cardiovascular stress"
        return MissionRisk.CAUTION, f"g={g:.2f}g — adaptation required"

    def atmosphere_breathability(self) -> Tuple[MissionRisk, str]:
        c    = self.p.composition
        P    = self.p.atm_pressure_Pa
        o2_partial = c.O2 * P
        co2_pp = c.CO2 * P / 1000.0  # kPa
        if o2_partial < 11300 or o2_partial > 60000:
            return MissionRisk.UNSURVIVABLE, (
                f"O₂ partial pressure {o2_partial:.0f}Pa — "
                f"{'too low' if o2_partial < 11300 else 'oxygen toxicity'}")
        if co2_pp > 1.0:
            return MissionRisk.CRITICAL, f"CO₂={co2_pp:.2f}kPa — toxic"
        if c.SO2 > 1e-4 or c.NH3 > 1e-3:
            return MissionRisk.CRITICAL, "Toxic trace gases (SO₂/NH₃)"
        if c.O2 < 0.16:
            return MissionRisk.HAZARDOUS, f"Low O₂ fraction ({c.O2*100:.1f}%)"
        return MissionRisk.SAFE, f"O₂={o2_partial/1000:.1f}kPa — breathable"

    def radiation_risk(self) -> Tuple[MissionRisk, str]:
        uv = self.atm.surface_uv_dose_W_m2()
        L  = self.HUMAN_LIMITS
        if uv > L["uv_max_W_m2"] * 3:
            return MissionRisk.UNSURVIVABLE, f"UV={uv:.1f}W/m² — lethal"
        if uv > L["uv_max_W_m2"]:
            return MissionRisk.HAZARDOUS, f"UV={uv:.1f}W/m² — shielding required"
        if uv > L["uv_max_W_m2"]*0.5:
            return MissionRisk.CAUTION, f"UV={uv:.1f}W/m² — elevated"
        return MissionRisk.SAFE, f"UV={uv:.1f}W/m² — nominal"

    def tidal_risk(self) -> Tuple[MissionRisk, str]:
        """Tidal force risk (relevant for Miller near Gargantua)."""
        if self.p.planet_id.value == PlanetID.MILLER.value:
            # Miller orbits Gargantua — massive tidal force
            garg_M   = 1e8 * M_SUN
            r_miller = 9.56e11  # approximate orbit radius [m]
            tidal_g  = 2*G_SI*garg_M/(r_miller**3) / 9.81  # g/m
            if tidal_g > 1.0:
                return MissionRisk.UNSURVIVABLE, f"Tidal={tidal_g:.2e}g/m — lethal wave walls"
            return MissionRisk.CRITICAL, f"Tidal={tidal_g:.2e}g/m — extreme waves"
        return MissionRisk.SAFE, "Tidal forces negligible"

    def full_risk_matrix(self) -> pd.DataFrame:
        """Complete risk matrix for all hazard categories."""
        checks = [
            ("Temperature",      self.temperature_risk()),
            ("Pressure",         self.pressure_risk()),
            ("Gravity",          self.gravity_risk()),
            ("Atmosphere",       self.atmosphere_breathability()),
            ("Radiation/UV",     self.radiation_risk()),
            ("Tidal Forces",     self.tidal_risk()),
        ]
        risk_order = {MissionRisk.SAFE: 0, MissionRisk.CAUTION: 1,
                      MissionRisk.HAZARDOUS: 2, MissionRisk.CRITICAL: 3,
                      MissionRisk.UNSURVIVABLE: 4}
        rows = []
        for name, (risk, detail) in checks:
            rows.append({"Hazard": name, "Risk": risk.value,
                         "Detail": detail, "Risk_num": risk_order[risk]})
        df = pd.DataFrame(rows).sort_values("Risk_num", ascending=False)
        df = df.drop("Risk_num", axis=1)
        overall = max(risk_order[r] for _, (r,_) in checks)
        overall_risk = [k for k, v in risk_order.items() if v == overall][0]
        return df, overall_risk

    def survival_timeline_hours(self) -> Dict[str, float]:
        """
        Estimated unprotected survival time in various exposure scenarios.
        """
        T    = self.p.T_surf
        P    = self.p.atm_pressure_Pa
        uv   = self.atm.surface_uv_dose_W_m2()
        c    = self.p.composition

        # Temperature
        if T < 233 or T > 333:   t_temp = 0.17     # 10 min
        elif T < 253 or T > 313: t_temp = 2.0
        else:                     t_temp = 8760.0   # year+

        # Pressure
        if P < 6265:              t_pres = 0.0      # instant loss of consciousness
        elif P < 20000:           t_pres = 0.5
        else:                     t_pres = 8760.0

        # Breathability
        o2_pp = c.O2 * P
        if o2_pp < 6000:          t_o2   = 0.033    # 2 min hypoxia
        elif o2_pp < 11300:       t_o2   = 0.5
        else:                     t_o2   = 8760.0

        # UV
        if uv > 100:              t_uv   = 0.017    # 1 min
        elif uv > L_SUN*0.01:    t_uv   = 1.0
        else:                     t_uv   = 8760.0

        t_total = min(t_temp, t_pres, t_o2, t_uv)
        return {"temperature_h": t_temp, "pressure_h": t_pres,
                "o2_h": t_o2, "uv_h": t_uv,
                "total_unprotected_h": t_total,
                "limiting_factor": min(
                    [("temperature", t_temp),("pressure", t_pres),
                     ("o2", t_o2),("uv", t_uv)], key=lambda x: x[1])[0]}


# ══════════════════════════════════════════════════════════════════════════════
# §10A  ATMOSPHERIC RADIATIVE TRANSFER — 7-Layer Radiative-Convective Model
# ══════════════════════════════════════════════════════════════════════════════
class RadiativeConvectiveModel:
    """
    7-layer 1D radiative-convective equilibrium (RCE) climate model.
    Solves for the vertical temperature profile of a planetary atmosphere.

    Method:
    1. Divide atmosphere into 7 pressure layers (log-spaced)
    2. Compute optical depth τ_λ for each layer based on composition
    3. Solve two-stream Schwarzschild equations for upwelling/downwelling IR
    4. Compute radiative heating/cooling rates
    5. Convective adjustment: enforce dry/moist adiabatic lapse rate
    6. Iterate to equilibrium T(P) profile

    References:
      Manabe & Strickler (1964) J.Atmos.Sci.
      Pierrehumbert, "Principles of Planetary Climate" (2010)
    """

    def __init__(self, planet: Planet, n_layers: int = 7):
        self.p    = planet
        self.n    = n_layers
        self.g    = planet.surface_gravity()
        # Pressure grid (Pa): logarithmically spaced from surface to TOA
        P_surf    = planet.pressure_bar * 1e5
        P_toa     = P_surf * 1e-4
        self.P_edges = np.geomspace(P_surf, P_toa, self.n + 1)
        self.P_mid   = np.sqrt(self.P_edges[:-1] * self.P_edges[1:])  # Layer centers
        self.dP      = self.P_edges[:-1] - self.P_edges[1:]

    def _absorption_coefficients(self) -> Dict[str, float]:
        """Specific absorption coefficients κ_IR [m²/kg] (approximate)."""
        return {
            "CO2": 0.05,
            "H2O": 0.10,
            "CH4": 0.08,
            "N2":  0.0001,  # CIA only
            "O2":  0.0002,
            "NH3": 0.15,
        }

    def compute_optical_depths(self) -> np.ndarray:
        """
        Compute IR optical depth difference Δτ for each layer.
        Δτ_i = κ_mix · ΔP_i / g
        """
        k_dict = self._absorption_coefficients()
        k_mix = 0.0
        for gas, frac in self.p.atmosphere.items():
            k_mix += k_dict.get(gas, 0.0) * frac
        
        # Add pressure broadening: κ ∝ (P/P0)
        tau_diff = k_mix * self.dP / self.g * (self.P_mid / 1e5)**0.5
        return tau_diff

    def dry_adiabatic_lapse_rate(self) -> float:
        """Γ_d = g / c_p [K/m]. Convert to K/Pa: dT/dP = R T / (c_p P)"""
        m_mean = self.p.mean_molecular_weight() * 1e-3  # kg/mol
        c_p = 1000.0 * (28.97e-3 / m_mean)  # approximate specific heat
        return self.g / c_p

    def radiative_fluxes(self, T_layers: np.ndarray, T_surf: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Solve two-stream IR fluxes using Schwarzschild equation.
        Upwelling F_up, Downwelling F_down at layer edges.
        """
        dtau = self.compute_optical_depths()
        
        # Blackbody emission of layers (σT^4)
        B_layers = SIGMA_SB * T_layers**4
        B_surf   = SIGMA_SB * T_surf**4
        
        F_down = np.zeros(self.n + 1)
        F_up   = np.zeros(self.n + 1)
        
        # Downwelling (Top to Bottom)
        F_down[-1] = 0.0  # TOA
        for i in range(self.n - 1, -1, -1):
            trans = math.exp(-1.66 * dtau[i])  # Diffusivity factor 1.66
            F_down[i] = F_down[i+1] * trans + B_layers[i] * (1.0 - trans)
            
        # Upwelling (Bottom to Top)
        F_up[0] = B_surf
        for i in range(self.n):
            trans = math.exp(-1.66 * dtau[i])
            F_up[i+1] = F_up[i] * trans + B_layers[i] * (1.0 - trans)
            
        return F_up, F_down

    def convective_adjustment(self, T_layers: np.ndarray, T_surf: float) -> Tuple[np.ndarray, float]:
        """Enforce adiabatic lapse rate constraint (energy conserving)."""
        m_mean = self.p.mean_molecular_weight() * 1e-3
        R_spec = 8.314 / m_mean
        c_p    = 1000.0 * (28.97e-3 / m_mean)
        kappa  = R_spec / c_p  # R/c_p
        
        T_adj = T_layers.copy()
        T_s_adj = T_surf
        
        # Check consecutive layers
        for i in range(self.n - 1):
            P1, P2 = self.P_mid[i], self.P_mid[i+1]
            T1, T2 = T_adj[i], T_adj[i+1]
            # Potential temperature condition
            if T2 < T1 * (P2/P1)**kappa:
                # Mix layers conserving enthalpy (c_p T dP)
                H_tot = c_p * T1 * self.dP[i] + c_p * T2 * self.dP[i+1]
                # New temperatures follow adiabat: T2_new = T1_new * (P2/P1)^kappa
                T1_new = H_tot / (c_p * self.dP[i] + c_p * self.dP[i+1] * (P2/P1)**kappa)
                T_adj[i] = T1_new
                T_adj[i+1] = T1_new * (P2/P1)**kappa
                
        # Check surface to layer 0
        if T_adj[0] < T_s_adj * (self.P_mid[0] / self.P_edges[0])**kappa:
            T_s_adj = T_adj[0] / (self.P_mid[0] / self.P_edges[0])**kappa
            
        return T_adj, T_s_adj

    def solve_temperature_profile(self, n_iter: int = 50, dt_days: float = 0.5) -> Dict[str, np.ndarray]:
        """
        Iterate RCE model to equilibrium.
        dt_days is the pseudo-timestep for radiative relaxation.
        """
        # Initial guess: isothermal
        T_eq   = self.p.equilibrium_temperature()
        T_surf = T_eq + 30.0
        T_layers = np.ones(self.n) * T_eq
        
        c_p = 1000.0
        dt  = dt_days * 86400.0
        
        # Insolation absorbed at surface
        alb = self.p.albedo
        S_inc = self.p.stellar_flux()
        F_solar_absorbed = S_inc * (1.0 - alb) / 4.0
        
        for _ in range(n_iter):
            F_up, F_down = self.radiative_fluxes(T_layers, T_surf)
            
            # Radiative heating rates: dT/dt = -g/c_p dF_net/dP
            F_net = F_up - F_down
            dF_dP = (F_net[:-1] - F_net[1:]) / self.dP
            dT_rad = -self.g / c_p * dF_dP * dt
            
            T_layers += dT_rad
            
            # Surface balance
            F_surf_net = F_solar_absorbed + F_down[0] - F_up[0]
            # Assume arbitrary surface heat capacity equivalent to 10m ocean
            C_surf = 10.0 * 1000.0 * 4184.0 
            T_surf += F_surf_net * dt / C_surf
            
            # Convective adjustment
            T_layers, T_surf = self.convective_adjustment(T_layers, T_surf)
            
        return {
            "P_mid_Pa": self.P_mid,
            "T_layers_K": T_layers,
            "T_surf_K": T_surf,
            "OLR_W": F_up[-1],  # Outgoing Longwave Radiation
            "F_up": F_up,
            "F_down": F_down,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §10B  ATMOSPHERIC RETRIEVAL ENGINE — Spectral Biosignature Inversion
# ══════════════════════════════════════════════════════════════════════════════
class AtmosphericRetrieval:
    """
    Bayesian atmospheric retrieval engine for biosignatures.
    Simulates observation of a planetary reflectance spectrum and runs an MCMC-like
    grid search to retrieve the posterior probability of key biosignature gases.

    Retrieval targets:
      - O₂ (Oxygen A-band at 0.76 μm)
      - CH₄ (Methane bands at 1.15, 1.4, 1.6 μm)
      - O₃ (Ozone Chappuis band 0.6 μm)

    References:
      Madhusudhan & Seager (2009) ApJ 707:24
      Line et al. (2013) ApJ 775:137
    """

    def __init__(self, planet: Planet):
        self.p = planet
        # Wavelength grid for retrieval [μm]
        self.wl = np.linspace(0.4, 2.0, 300)

    def _cross_sections(self) -> Dict[str, np.ndarray]:
        """Simulated absorption cross-sections σ(λ) [arbitrary units]."""
        # Gaussian profiles for key molecular bands
        def band(wl0, width):
            return np.exp(-0.5 * ((self.wl - wl0) / width)**2)
            
        return {
            "O2":  1.0 * band(0.76, 0.01) + 0.2 * band(1.27, 0.02),
            "CH4": 0.8 * band(1.15, 0.03) + 1.2 * band(1.40, 0.04) + 1.5 * band(1.65, 0.05),
            "O3":  0.5 * band(0.60, 0.08) + 0.3 * band(0.32, 0.02),
            "H2O": 1.0 * band(0.94, 0.02) + 1.2 * band(1.13, 0.03) + 1.8 * band(1.38, 0.04) + 2.5 * band(1.88, 0.06),
            "CO2": 0.5 * band(1.60, 0.02) + 2.0 * band(2.00, 0.05),
        }

    def forward_model(self, abundances: Dict[str, float]) -> np.ndarray:
        """
        Generate synthetic reflectance spectrum given abundances.
        Uses simple Beer-Lambert transmission through 1 airmass.
        """
        sigma = self._cross_sections()
        tau = np.zeros_like(self.wl)
        
        # Column density scale factor (proportional to pressure)
        col = self.p.pressure_bar * 1.0e25  
        
        for gas, frac in abundances.items():
            if gas in sigma:
                tau += sigma[gas] * frac * col * 1e-25  # scaled cross sections
                
        # Reflectance = Albedo * exp(-2*tau) (two-way path)
        reflectance = self.p.albedo * np.exp(-2.0 * tau)
        
        # Add Rayleigh scattering slope (λ^-4)
        rayleigh = 0.05 * self.p.pressure_bar * (0.5 / self.wl)**4
        reflectance = reflectance + rayleigh
        return np.clip(reflectance, 0.0, 1.0)

    def simulate_observation(self, snr: float = 20.0) -> np.ndarray:
        """Generate synthetic observed spectrum with Gaussian noise."""
        truth = self.forward_model(self.p.atmosphere)
        noise = truth / snr * np.random.randn(len(self.wl))
        return truth + noise

    def retrieve_abundances(self, obs_spec: np.ndarray, snr: float = 20.0) -> Dict[str, Any]:
        """
        Grid search retrieval for O2 and CH4 (simulated 2D MCMC posterior).
        Computes the Bayesian evidence for the presence of biosignatures.
        """
        noise_std = np.mean(obs_spec) / snr
        
        # Grid bounds: log10(fraction)
        o2_grid  = np.logspace(-6, 0, 40)
        ch4_grid = np.logspace(-6, -2, 40)
        
        posterior = np.zeros((len(o2_grid), len(ch4_grid)))
        base_atm = {"N2": 0.8, "CO2": 0.1, "H2O": 0.01}  # Fixed background
        
        for i, o2 in enumerate(o2_grid):
            for j, ch4 in enumerate(ch4_grid):
                test_atm = base_atm.copy()
                test_atm["O2"] = o2
                test_atm["CH4"] = ch4
                
                model = self.forward_model(test_atm)
                
                # Log-likelihood: L ∝ -0.5 * chi^2
                chi2 = np.sum(((obs_spec - model) / noise_std)**2)
                posterior[i, j] = math.exp(-0.5 * chi2)
                
        # Normalise posterior
        Z = np.sum(posterior)
        posterior /= (Z + 1e-300)
        
        # Marginalize
        marg_o2  = np.sum(posterior, axis=1)
        marg_ch4 = np.sum(posterior, axis=0)
        
        # Best fit
        idx_o2, idx_ch4 = np.unravel_index(np.argmax(posterior), posterior.shape)
        
        # Equivalent width of O2-A band (0.76 μm)
        idx_A = np.where((self.wl > 0.75) & (self.wl < 0.77))[0]
        continuum = np.interp(self.wl[idx_A], [0.74, 0.78], [obs_spec[np.argmin(abs(self.wl-0.74))], obs_spec[np.argmin(abs(self.wl-0.78))]])
        ew_O2 = trapz(1.0 - obs_spec[idx_A] / continuum, self.wl[idx_A]) * 1000.0  # nm
        
        return {
            "O2_best":    o2_grid[idx_o2],
            "CH4_best":   ch4_grid[idx_ch4],
            "O2_marg":    marg_o2,
            "CH4_marg":   marg_ch4,
            "O2_grid":    o2_grid,
            "CH4_grid":   ch4_grid,
            "posterior":  posterior,
            "O2_A_band_EW_nm": max(0.0, ew_O2),
            "biosig_confidence": float(np.sum(posterior[o2_grid > 1e-3, :]) * np.sum(posterior[:, ch4_grid > 1e-5])),
        }


# ══════════════════════════════════════════════════════════════════════════════
# §10C  PLANETARY INTERIOR STRUCTURE MODEL (4-Layer)
# ══════════════════════════════════════════════════════════════════════════════
class PlanetaryInterior:
    """
    4-layer differentiated interior structure model.
    Solves the Adams-Williamson equation for hydrostatic equilibrium:
      dρ/dr = −(G M(r) ρ(r)) / (r² Φ)
    where Φ = K_S / ρ is the seismic parameter.

    Layers:
    1. Iron Core (Inner solid + Outer liquid)
    2. Silicate Mantle
    3. Silicate Crust
    4. Ocean/Ice shell (if present)

    Computes moment of inertia factor I/MR² and core pressure.
    """

    def __init__(self, planet: Planet):
        self.p = planet
        self.M_total = planet.mass_earth * 5.972e24      # kg
        self.R_total = planet.radius_earth * 6371e3      # m
        self.avg_rho = self.M_total / (4.0/3.0 * math.pi * self.R_total**3)

    def determine_layer_boundaries(self) -> Dict[str, float]:
        """
        Estimate layer boundary radii based on uncompressed density matching.
        Returns radii in metres.
        """
        # Earth baseline fractions (radius)
        # Core: 0.54 R_E, Mantle: 0.99 R_E, Crust: 1.0 R_E
        
        # Scale core size based on mean density (iron fraction proxy)
        # Higher density -> larger core. 
        # Empirical fit: r_core/R = 0.54 * (rho / 5514)^0.5
        r_c_frac = 0.54 * math.sqrt(self.avg_rho / 5514.0)
        r_c_frac = min(max(r_c_frac, 0.1), 0.85)  # bounds
        
        return {
            "R_core":   r_c_frac * self.R_total,
            "R_mantle": 0.985 * self.R_total,
            "R_crust":  self.R_total,
        }

    def _equation_of_state(self, r: float, bounds: Dict[str, float]) -> Tuple[float, float]:
        """
        Return base density ρ0 and bulk modulus K0 for layer at radius r.
        Uses Murnaghan EOS parameters [kg/m³, Pa].
        """
        if r <= bounds["R_core"]:
            # Iron core (liquid Fe-Ni)
            rho0 = 7000.0
            K0   = 130e9  
        elif r <= bounds["R_mantle"]:
            # Silicate mantle (Perovskite/Bridgmanite)
            rho0 = 4100.0
            K0   = 200e9
        else:
            # Crust (Basalt/Granite)
            rho0 = 2900.0
            K0   = 60e9
            
        return rho0, K0

    def solve_density_profile(self, n_pts: int = 500) -> Dict[str, np.ndarray]:
        """
        Integrate Adams-Williamson ODE from surface to center.
        System:
          dM/dr = 4π r² ρ
          dρ/dr = −(G M ρ²) / (K r²)
        """
        bounds = self.determine_layer_boundaries()
        r_arr = np.linspace(100.0, self.R_total, n_pts)  # avoid r=0 singularity
        
        # Initialize arrays
        rho = np.zeros(n_pts)
        M_r = np.zeros(n_pts)
        P   = np.zeros(n_pts)
        g   = np.zeros(n_pts)
        
        # Boundary condition at surface
        rho[-1], K_surf = self._equation_of_state(self.R_total, bounds)
        M_r[-1] = self.M_total
        P[-1]   = self.p.pressure_bar * 1e5
        g[-1]   = G_SI * M_r[-1] / (r_arr[-1]**2)
        
        # Integrate inward (Euler method for simplicity, suffices for qualitative)
        dr = r_arr[1] - r_arr[0]
        
        for i in range(n_pts - 1, 0, -1):
            r_i = r_arr[i]
            rho0, K0 = self._equation_of_state(r_i, bounds)
            
            # Density gradient (Adams-Williamson)
            # Add small regularisation to avoid division by zero
            Phi = K0 / rho[i]
            drho_dr = - (G_SI * M_r[i] * rho[i]) / (r_i**2 * Phi + 1e-10)
            
            # Update density
            rho[i-1] = rho[i] - drho_dr * dr
            
            # Enforce density jumps at boundaries
            rho0_next, _ = self._equation_of_state(r_arr[i-1], bounds)
            if rho0_next > rho0 + 100.0:  # Crossed boundary inward
                rho[i-1] = rho[i-1] + (rho0_next - rho0)
            
            # Update mass
            dM_dr = 4.0 * math.pi * r_i**2 * rho[i]
            M_r[i-1] = M_r[i] - dM_dr * dr
            
            # Update pressure (dP/dr = -rho g)
            g_i = G_SI * M_r[i] / (r_i**2)
            dP_dr = -rho[i] * g_i
            P[i-1] = P[i] - dP_dr * dr
            g[i-1] = G_SI * M_r[i-1] / (r_arr[i-1]**2)

        # Compute Moment of Inertia: I = (8π/3) ∫ ρ r⁴ dr
        I_val = (8.0 * math.pi / 3.0) * trapz(rho * r_arr**4, r_arr)
        # Dimensionless MoI factor: C/MR²
        I_factor = I_val / (self.M_total * self.R_total**2)

        return {
            "r_m":      r_arr,
            "r_frac":   r_arr / self.R_total,
            "rho_kgm3": rho,
            "Mass_kg":  M_r,
            "P_Pa":     P,
            "P_GPa":    P / 1e9,
            "g_ms2":    g,
            "I_factor": I_factor,
            "P_core_GPa": P[0] / 1e9,
            "R_core_km": bounds["R_core"] / 1000.0,
            "core_mass_frac": M_r[np.argmin(np.abs(r_arr - bounds["R_core"]))] / self.M_total,
        }

    def magnetic_dynamo_proxy(self) -> float:
        """
        Estimate likelihood of active core dynamo.
        Requires liquid iron core + sufficient rotation + heat flux.
        Proxy score 0-1 based on core size and rotation rate.
        """
        bounds = self.determine_layer_boundaries()
        r_c_frac = bounds["R_core"] / self.R_total
        
        # If tidally locked (Miller, maybe others), rotation is slow
        rot_omega = 2.0 * math.pi / (self.p.rotation_period_hr * 3600.0)
        earth_omega = 2.0 * math.pi / 86400.0
        
        # Rossby number proxy (inverse): higher is better for dynamo
        # Score = (core_frac / 0.54) * (omega / omega_earth)
        score = (r_c_frac / 0.54) * (rot_omega / earth_omega)**0.5
        return float(np.clip(score, 0.0, 1.0))


# ══════════════════════════════════════════════════════════════════════════════
# §11  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_session_state():

    scorer = HabitabilityScorer()
    D: Dict[str, Any] = {
        "plan_active_pid":    PlanetID.EDMUNDS.value,
        "plan_planets":       PLANET_REGISTRY,
        "plan_scorer":        scorer,
        "plan_compare_df":    None,
        "plan_atm_profile":   None,
        "plan_spectrum":      None,
        "plan_risk_matrix":   None,
        "plan_custom":        None,
        # Custom planet sliders
        "plan_c_mass":        1.0,
        "plan_c_radius":      1.0,
        "plan_c_sma":         1.0,
        "plan_c_albedo":      0.30,
        "plan_c_pressure":    1.0,
        "plan_c_T_star":      5778.0,
        "plan_c_L_star":      1.0,
        "plan_c_ocean":       0.70,
        "plan_c_ice":         0.05,
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# §12  MATPLOTLIB STYLE
# ══════════════════════════════════════════════════════════════════════════════
MPL_STYLE = {
    "figure.facecolor":  "#06090e",
    "axes.facecolor":    "#080c18",
    "axes.edgecolor":    "#14203a",
    "axes.labelcolor":   "#E8C46A",
    "axes.grid":         True,
    "grid.color":        "#0e1428",
    "grid.linestyle":    ":",
    "grid.alpha":        0.55,
    "xtick.color":       "#3a4a70",
    "ytick.color":       "#3a4a70",
    "xtick.labelsize":   6,
    "ytick.labelsize":   6,
    "axes.labelsize":    7,
    "axes.titlesize":    8,
    "axes.titlecolor":   "#E8C46A",
    "text.color":        "#E8C46A",
    "font.family":       "monospace",
    "legend.facecolor":  "#080c18",
    "legend.edgecolor":  "#14203a",
    "legend.fontsize":   6,
    "figure.dpi":        110,
    "savefig.facecolor": "#06090e",
    "axes.spines.top":   False,
    "axes.spines.right": False,
}

def _mpl():
    plt.rcParams.update(MPL_STYLE)


# ══════════════════════════════════════════════════════════════════════════════
# §13  PLOTTING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

PLANET_COLORS = {
    PlanetID.MILLER.value:  "#4FC3F7",
    PlanetID.MANN.value:    "#CE93D8",
    PlanetID.EDMUNDS.value: "#81C784",
    PlanetID.EARTH.value:   "#E8C46A",
    PlanetID.CUSTOM.value:  "#FFB74D",
}

# ── §13.1  Comparative radar/spider chart ─────────────────────────────────────
def _plot_radar(df: pd.DataFrame, planets: List[Planet]) -> plt.Figure:
    _mpl()
    metrics = ["ESI","SHI","BCI","safety","plan_B_score","overall_priority"]
    labels  = ["ESI","SHI","BCI","Safety","Plan-B","Priority"]
    N       = len(metrics)
    angles  = [2*math.pi*i/N for i in range(N)] + [0]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6),
                              subplot_kw=dict(projection="polar")
                              if False else {},
                              )
    fig.patch.set_facecolor("#06090e")

    ax1 = fig.add_subplot(121, polar=True)
    ax2 = fig.add_subplot(122)

    for p in planets:
        row = df[df["name"] == p.name]
        if row.empty:
            continue
        vals = [float(row[m].values[0]) for m in metrics]
        vals += vals[:1]
        clr  = PLANET_COLORS.get(p.planet_id.value, "#fff")
        ax1.plot(angles, vals, color=clr, lw=1.5, label=p.name, alpha=0.9)
        ax1.fill(angles, vals, color=clr, alpha=0.10)

    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(labels, fontsize=7, color="#E8C46A")
    ax1.set_ylim(0, 1); ax1.set_yticks([0.2,0.4,0.6,0.8,1.0])
    ax1.set_yticklabels(["0.2","0.4","0.6","0.8","1.0"], fontsize=5)
    ax1.set_facecolor("#06090e")
    ax1.grid(color="#1a2540", lw=0.5)
    ax1.set_title("HABITABILITY RADAR", fontsize=8, color="#E8C46A", pad=15)
    ax1.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=6)

    # Bar chart
    x   = np.arange(len(metrics))
    w   = 0.8/len(planets)
    for i, p in enumerate(planets):
        row  = df[df["name"] == p.name]
        if row.empty: continue
        vals = [float(row[m].values[0]) for m in metrics]
        clr  = PLANET_COLORS.get(p.planet_id.value, "#fff")
        ax2.bar(x + i*w, vals, w, label=p.name, color=clr, alpha=0.82)

    ax2.set_xticks(x + w*len(planets)/2)
    ax2.set_xticklabels(labels, rotation=30, ha="right", fontsize=7)
    ax2.set_ylabel("Score  [0–1]")
    ax2.set_title("COMPARATIVE SCORES")
    ax2.legend(fontsize=6)
    ax2.set_facecolor("#080c18")
    ax2.set_ylim(0, 1.05)

    plt.tight_layout()
    return fig


# ── §13.2  Habitable zone diagram ────────────────────────────────────────────
def _plot_hz_diagram(planets: List[Planet], scorer: HabitabilityScorer
                      ) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("#06090e")

    # Left: HZ diagram (luminosity vs distance)
    ax1 = axes[0]
    L_range = np.logspace(-2, 2, 200)
    T_range = np.array([5778.0*(L**0.25) for L in L_range])   # rough T-L

    for L_sol, T_star in zip(L_range, T_range):
        hz = scorer.habitable_zone_AU(T_star, L_sol)
        ax1.fill_between([hz["optimistic_inner"], hz["optimistic_outer"]],
                          [L_sol, L_sol], [L_sol*1.05, L_sol*1.05],
                          color="#1a4020", alpha=0.2)
        ax1.fill_between([hz["conservative_inner"], hz["conservative_outer"]],
                          [L_sol, L_sol], [L_sol*1.05, L_sol*1.05],
                          color="#20a040", alpha=0.2)

    # Actual planets
    for p in planets:
        if p.semi_major_AU <= 0:
            continue
        L_sol = p.star_L_W / L_SUN
        clr   = PLANET_COLORS.get(p.planet_id.value, "#fff")
        ax1.scatter(p.semi_major_AU, L_sol, color=clr, s=120,
                    zorder=5, edgecolors="#E8C46A", lw=0.5)
        ax1.annotate(p.name, (p.semi_major_AU, L_sol),
                     textcoords="offset points", xytext=(5, 4),
                     fontsize=6, color=clr)

    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xlabel("Semi-major axis  [AU]")
    ax1.set_ylabel("Stellar luminosity  [L_sun]")
    ax1.set_title("HABITABLE ZONE DIAGRAM\n(Green = conservative, Teal = optimistic)")
    ax1.set_facecolor("#060a14")

    # Right: ESI vs T_surface scatter
    ax2 = axes[1]
    T_arr  = np.linspace(180, 400, 200)
    esi_T  = []
    for T in T_arr:
        # Hypothetical ESI varying only T_surf
        v_e  = scorer._esi_term(11.186, scorer._REF["v_esc_km"], scorer._W["v_esc_km"])
        T_e  = scorer._esi_term(T, scorer._REF["T_surf_K"], scorer._W["T_surf_K"])
        r_e  = scorer._esi_term(1.0, scorer._REF["radius_earth"], scorer._W["radius_earth"])
        rho_e= scorer._esi_term(1.0, scorer._REF["rho_norm"],     scorer._W["rho_norm"])
        esi  = math.sqrt(r_e*rho_e * v_e*T_e)
        esi_T.append(esi)
    ax2.plot(T_arr - 273.15, esi_T, color="#E8C46A", lw=1.3,
             label="ESI vs T_surf (Earth mass+radius)")
    ax2.axhline(0.8, color="#81C784", lw=0.8, ls="--", label="ESI=0.8 (superhabitable)")
    ax2.axhline(0.6, color="#FFB74D", lw=0.8, ls=":", label="ESI=0.6 (habitable)")
    ax2.axvspan(-20, 50, alpha=0.08, color="#20a040",
                label="Optimal T range (-20 to 50°C)")

    for p in planets:
        if p.T_surf is None: continue
        esi  = scorer.global_ESI(p)
        clr  = PLANET_COLORS.get(p.planet_id.value, "#fff")
        ax2.scatter(p.T_surf-273.15, esi, color=clr, s=120, zorder=5,
                    edgecolors="#E8C46A", lw=0.5, label=p.name)

    ax2.set_xlabel("Surface temperature  [°C]")
    ax2.set_ylabel("ESI  (Earth Similarity Index)")
    ax2.set_title("ESI vs SURFACE TEMPERATURE")
    ax2.legend(fontsize=5.5)
    ax2.set_facecolor("#080c18")

    plt.tight_layout()
    return fig


# ── §13.3  Atmosphere vertical profile ────────────────────────────────────────
def _plot_atmosphere(planet: Planet) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    fig.patch.set_facecolor("#06090e")
    atm = AtmosphericEngine(planet)
    z_km, T_arr, P_arr = atm.temperature_profile(n_layers=80)

    ax1 = axes[0]
    ax1.plot(T_arr, z_km, color="#FF8800", lw=1.3, label="T(z)")
    ax1.axvline(273.15, color="#4FC3F7", lw=0.7, ls="--", label="273 K (0°C)")
    ax1.set_xlabel("Temperature  [K]"); ax1.set_ylabel("Altitude  [km]")
    ax1.set_title(f"TEMPERATURE PROFILE\n{planet.name}")
    ax1.legend(fontsize=6)

    ax2 = axes[1]
    ax2.semilogy(P_arr/1e3, z_km, color="#CE93D8", lw=1.3)
    ax2.set_xlabel("Pressure  [kPa]"); ax2.set_ylabel("Altitude  [km]")
    ax2.set_title("PRESSURE PROFILE")

    # Composition pie
    ax3 = axes[2]
    comp  = planet.composition
    d     = {sp: v for sp, v in comp.to_dict().items() if v > 1e-5}
    if d:
        clrs_pie = ["#4FC3F7","#81C784","#FF8800","#CE93D8","#E8C46A",
                    "#D154FF","#FFB74D","#a0a0ff"]
        labs = list(d.keys()); vals = list(d.values())
        wedges, texts, auto = ax3.pie(
            vals, labels=labs, autopct="%1.1f%%",
            colors=clrs_pie[:len(labs)], startangle=90,
            textprops={"fontsize":6, "color":"#E8C46A"})
        for at in auto: at.set_fontsize(5)
    ax3.set_title(f"ATMOSPHERIC COMPOSITION\nμ={comp.mean_molecular_weight():.2f} g/mol  "
                  f"H={planet.H_scale/1000:.1f} km")

    plt.tight_layout()
    return fig


# ── §13.4  Full spectrum figure ───────────────────────────────────────────────
def _plot_spectrum(planet: Planet) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 2, figsize=(15, 9))
    fig.patch.set_facecolor("#06090e")
    sp = SpectralEngine(planet)

    wl_vis = np.linspace(0.30, 2.50, 600)   # VIS + NIR
    wl_ir  = np.linspace(2.50, 25.0, 600)   # MIR

    data = sp.combined_spectrum(wl_vis, wl_ir)
    clr  = PLANET_COLORS.get(planet.planet_id.value, "#E8C46A")

    # Reflectance spectrum
    ax1 = axes[0, 0]
    ax1.plot(wl_vis, data["reflectance"], color=clr, lw=1.0, alpha=0.9)
    ax1.fill_between(wl_vis, data["reflectance"], 0, alpha=0.15, color=clr)
    # Mark biosignature bands
    bio_bands = [("O₂-A", 0.760), ("H₂O", 0.940), ("CO₂", 1.600),
                 ("H₂O", 1.380), ("CH₄", 1.670), ("CO₂", 2.010)]
    for name, wl in bio_bands:
        ax1.axvline(wl, color="#555", lw=0.4, ls=":")
        ax1.text(wl+0.01, 0.90, name, fontsize=4.5, color="#888", rotation=90)
    ax1.set_xlabel("Wavelength  [μm]"); ax1.set_ylabel("Geometric albedo")
    ax1.set_title(f"REFLECTANCE SPECTRUM — {planet.name}")
    ax1.set_xlim(0.3, 2.5); ax1.set_ylim(0, 1.0)

    # Thermal emission
    ax2 = axes[0, 1]
    ax2.plot(wl_ir, data["F_thermal"]*1e6, color="#FF8800", lw=1.0)
    ax2.fill_between(wl_ir, data["F_thermal"]*1e6, 0, alpha=0.15, color="#FF8800")
    ir_bands = [("CO₂", 4.26), ("H₂O", 6.3), ("CH₄", 7.7),
                ("O₃", 9.6), ("CO₂", 15.0), ("N₂O", 17.0)]
    for name, wl in ir_bands:
        ax2.axvline(wl, color="#555", lw=0.4, ls=":")
        ymax = float(np.max(data["F_thermal"]*1e6))
        ax2.text(wl+0.2, ymax*0.85, name, fontsize=4.5, color="#888", rotation=90)
    ax2.set_xlabel("Wavelength  [μm]"); ax2.set_ylabel("Thermal flux  [μW m⁻² μm⁻¹]")
    ax2.set_title(f"THERMAL EMISSION — T={planet.T_surf-273:.0f}°C")

    # Stellar + reflected comparison
    ax3 = axes[1, 0]
    F_star_norm = data["F_star"] / (data["F_star"].max()+1e-30)
    ax3.plot(wl_vis, F_star_norm, color="#FFD700", lw=0.8, alpha=0.6,
             label="Stellar (normalised)")
    ax3.plot(wl_vis, data["reflectance"], color=clr, lw=1.0,
             label=f"Planet reflectance")
    prod = F_star_norm * data["reflectance"]
    ax3.fill_between(wl_vis, prod, 0, alpha=0.2, color=clr,
                     label="Observed reflected flux")
    ax3.set_xlabel("Wavelength  [μm]"); ax3.set_ylabel("Normalised flux")
    ax3.set_title("STELLAR × ALBEDO — Observable Reflected Flux")
    ax3.legend(fontsize=6)

    # Biosignature detection table as bar chart
    ax4 = axes[1, 1]
    bio_df = sp.biosignature_feature_table()
    depths = bio_df["Max depth"].values
    names  = bio_df["Feature"].values
    det    = bio_df["Detectability"].values
    bar_colors = ["#81C784" if d=="STRONG" else "#FFB74D" if d=="WEAK"
                  else "#3a4a70" for d in det]
    bars = ax4.barh(names, depths, color=bar_colors, alpha=0.85)
    ax4.bar_label(bars, fmt="%.3f", padding=3, fontsize=6, color="#fff")
    ax4.axvline(0.30, color="#81C784", lw=0.7, ls="--", label="STRONG threshold")
    ax4.axvline(0.05, color="#FFB74D", lw=0.7, ls=":", label="WEAK threshold")
    ax4.set_xlabel("Absorption depth"); ax4.set_title("BIOSIGNATURE FEATURES")
    ax4.legend(fontsize=6)
    ax4.set_facecolor("#080c18")

    plt.tight_layout()
    return fig


# ── §13.5  Planet comparison cards + ranking ─────────────────────────────────
def _plot_comparison_overview(df: pd.DataFrame,
                               planets: List[Planet]) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.patch.set_facecolor("#06090e")
    
    # Only include planets that are present in the comparative dataframe
    df_names = df["name"].tolist() if "name" in df.columns else []
    active_planets = [p for p in planets if p.name in df_names]
    
    clrs  = [PLANET_COLORS.get(p.planet_id.value, "#fff") for p in active_planets]
    names = [p.name for p in active_planets]

    def _bar(ax, col, ylabel, title, log=False):
        vals = [float(df[df["name"]==p.name][col].values[0])
                for p in active_planets if col in df.columns]
        if not vals:
            return
        if log:
            ax.bar(names, np.abs(vals)+1e-30, color=clrs, alpha=0.85)
            ax.set_yscale("log")
        else:
            ax.bar(names, vals, color=clrs, alpha=0.85)
        for i, v in enumerate(vals):
            ax.text(i, max(vals)*0.02, f"{v:.3g}", ha="center",
                    va="bottom", fontsize=6, color="#fff")
        ax.set_ylabel(ylabel, fontsize=6)
        ax.set_title(title, fontsize=7)
        ax.tick_params(axis="x", rotation=15, labelsize=6)
        ax.set_facecolor("#080c18")

    _bar(axes[0,0], "overall_priority", "Priority score",  "OVERALL MISSION PRIORITY")
    _bar(axes[0,1], "ESI",              "ESI [0–1]",        "EARTH SIMILARITY INDEX")
    _bar(axes[0,2], "T_surf_C",         "°C",               "MEAN SURFACE TEMPERATURE")
    _bar(axes[1,0], "g_surf_earth",     "g (Earth=1)",      "SURFACE GRAVITY")
    _bar(axes[1,1], "atm_pressure_bar", "bar",              "ATMOSPHERIC PRESSURE")
    _bar(axes[1,2], "plan_B_score",     "Plan-B score",     "PLAN B COLONY SUITABILITY")

    plt.tight_layout()
    return fig


# ── §13.6  Risk matrix visualisation ─────────────────────────────────────────
def _plot_risk_matrix(risk_df: pd.DataFrame,
                       overall: MissionRisk, planet: Planet) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor("#06090e")

    risk_colors = {
        "SAFE": "#81C784", "CAUTION": "#FFD700",
        "HAZARDOUS": "#FF8800", "CRITICAL": "#D154FF",
        "UNSURVIVABLE": "#CE93D8",
    }
    risk_vals = {"SAFE":0,"CAUTION":1,"HAZARDOUS":2,"CRITICAL":3,"UNSURVIVABLE":4}

    ax1 = axes[0]
    hazards = risk_df["Hazard"].values
    risks   = risk_df["Risk"].values
    vals    = [risk_vals.get(r.split()[0], 0) for r in risks]
    bclrs   = [risk_colors.get(r.split()[0], "#fff") for r in risks]
    ax1.barh(hazards, [v+0.5 for v in vals], color=bclrs, alpha=0.85)
    ax1.set_xlim(0, 5)
    ax1.set_xticks([0.5,1.5,2.5,3.5,4.5])
    ax1.set_xticklabels(["SAFE","CAUTION","HAZARD","CRITICAL","LETHAL"],
                         fontsize=7, rotation=20)
    ax1.set_title(f"MISSION RISK MATRIX — {planet.name}\n"
                  f"Overall: {overall.value}")
    ax1.set_facecolor("#080c18")

    # Detail text
    ax2 = axes[1]
    ax2.axis("off")
    y = 0.96
    ax2.text(0.02, y, f"RISK REPORT — {planet.name}", fontsize=8,
             color="#E8C46A", transform=ax2.transAxes, fontfamily="monospace",
             fontweight="bold")
    y -= 0.08
    for _, row in risk_df.iterrows():
        risk_key = row["Risk"].split()[0]
        clr      = risk_colors.get(risk_key, "#fff")
        ax2.text(0.02, y, f"◆ {row['Hazard']:<18} [{row['Risk'][:10]}]",
                 fontsize=7, color=clr, transform=ax2.transAxes,
                 fontfamily="monospace")
        y -= 0.06
        ax2.text(0.05, y, row["Detail"],
                 fontsize=6, color="#888", transform=ax2.transAxes,
                 fontfamily="monospace")
        y -= 0.07

    # Survival timeline
    assessor = MissionRiskAssessor(planet)
    surv     = assessor.survival_timeline_hours()
    y -= 0.02
    ax2.text(0.02, y, "UNPROTECTED SURVIVAL:", fontsize=7, color="#E8C46A",
             transform=ax2.transAxes, fontfamily="monospace", fontweight="bold")
    y -= 0.07
    for k, val in surv.items():
        if k == "limiting_factor": continue
        val_s = f"{val:.2f} hr" if val < 8760 else ">1 yr"
        ax2.text(0.05, y, f"{k:<22} {val_s}",
                 fontsize=6, color="#aaa", transform=ax2.transAxes,
                 fontfamily="monospace")
        y -= 0.06
    if y > 0:
        ax2.text(0.02, y, f"Limiting factor: {surv.get('limiting_factor','—')}",
                 fontsize=7, color="#D154FF", transform=ax2.transAxes,
                 fontfamily="monospace")

    plt.tight_layout()
    return fig


# ── §13.7  Miller special — wave dynamics ────────────────────────────────────
def _plot_miller_special(miller: Planet) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#06090e")

    atm = AtmosphericEngine(miller)

    # 1. Tidal wave profile (standing wave)
    ax1 = axes[0]
    x   = np.linspace(0, 2*math.pi, 400)
    # Giant wave: two tidal bulges locked to Gargantua direction
    garg_M   = 1e8 * M_SUN
    r_miller = 9.56e11   # orbit radius [m]
    tidal_a  = 2*G_SI*garg_M*miller.R_m / r_miller**3   # tidal acceleration [m/s²]
    H_wave   = tidal_a * miller.R_m / miller.g_surf      # rough wave height [m]
    wave_h   = H_wave * (np.cos(x) + 0.3*np.cos(2*x))
    ax1.plot(x, wave_h/1000, color="#4FC3F7", lw=1.5)
    ax1.fill_between(x, wave_h/1000, 0, alpha=0.2, color="#4FC3F7")
    ax1.axhline(1.2, color="#D154FF", lw=0.8, ls="--",
                label="Film canon: 1.2 km")
    ax1.set_xlabel("Azimuthal angle [rad]")
    ax1.set_ylabel("Wave height  [km]")
    ax1.set_title(f"TIDAL STANDING WAVE PROFILE\n"
                  f"Tidal accel = {tidal_a:.2e} m/s²")
    ax1.legend(fontsize=6)

    # 2. Tidal heating vs orbital radius
    ax2 = axes[1]
    r_arr = np.linspace(miller.R_m*10, miller.R_m*100, 300)
    heat_arr = np.array([atm.p.tidal_heating_rate(0.0)
                          if False else
                          2*G_SI**2*garg_M**2*miller.M_kg*miller.R_m**5
                          / (19*1e9*100*r**6) for r in r_arr])
    ax2.semilogy(r_arr/miller.R_m, heat_arr, color="#FF8800", lw=1.2)
    ax2.axvline(r_miller/miller.R_m, color="#D154FF", lw=0.8, ls="--",
                label=f"Miller orbit")
    ax2.set_xlabel("r / R_planet"); ax2.set_ylabel("Tidal heating  [W]")
    ax2.set_title("TIDAL HEATING vs ORBIT RADIUS")
    ax2.legend(fontsize=6)

    # 3. Time dilation at Miller vs Earth calendar
    ax3 = axes[2]
    ship_hrs = np.linspace(0, 5, 100)
    earth_yr = ship_hrs * 7.0              # 1h = 7yr canon
    murph_age = MURPH_START = 10.0
    murph_ages = MURPH_START + earth_yr
    cooper_age = 35.0 + ship_hrs/8760.0   # negligible proper time
    ax3.plot(ship_hrs, murph_ages, color="#4FC3F7", lw=1.5, label="Murph (Earth)")
    ax3.plot(ship_hrs, [cooper_age]*len(ship_hrs), color="#E8C46A",
             lw=1.5, label="Cooper (ship)")
    ax3.fill_between(ship_hrs, murph_ages, cooper_age, alpha=0.15,
                     color="#D154FF", label="Age gap")
    ax3.axvline(3.22, color="#D154FF", lw=0.8, ls="--",
                label="Film: 3.22h on Miller")
    ax3.set_xlabel("Ship-hours on Miller")
    ax3.set_ylabel("Age  [yr]")
    ax3.set_title("MILLER AGE DIVERGENCE\n(1 ship-hour = 7 Earth years)")
    ax3.legend(fontsize=5.5)

    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# §14  MAIN STREAMLIT PAGE
# ══════════════════════════════════════════════════════════════════════════════
def planet_analyzer_page():
    init_session_state()
    _mpl()
    S = st.session_state

    st.markdown("""
    <div style="border-left:3px solid #81C784;padding:.55rem 1.2rem;
                margin-bottom:1.2rem;background:rgba(129,199,132,0.03);
                font-family:monospace;">
    <div style="color:#81C784;font-size:.95rem;letter-spacing:.12em;
                font-weight:600;">◓ PLANETARY SCIENCE &amp; HABITABILITY LABORATORY</div>
    <div style="color:#5a6a90;font-size:.62rem;margin-top:.2rem;">
    Miller's World · Mann's Planet · Edmunds' Planet · Custom Planet Builder  ·
    ESI · SHI · BCI · HZ Analysis · Spectroscopy · Biosignatures · Mission Risk
    </div></div>""", unsafe_allow_html=True)

    scorer  = S["plan_scorer"]
    planets = list(S["plan_planets"].values())

    (tab_overview, tab_single, tab_atm,
     tab_spectrum, tab_miller,
     tab_hz, tab_risk, tab_custom) = st.tabs([
        "▤ COMPARATIVE OVERVIEW",
        "✦ SINGLE PLANET DETAIL",
        "∿ ATMOSPHERE",
        "⌬ SPECTRUM & BIOSIG",
        "≋ MILLER'S WORLD",
        "◎ HABITABLE ZONE",
        "◬ MISSION RISK",
        "⚙ CUSTOM PLANET",
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1 — COMPARATIVE OVERVIEW
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_overview:
        if st.button("▤ COMPUTE FULL COMPARATIVE ANALYSIS",
                     width='stretch', type="primary"):
            with st.spinner("Scoring all planets..."):
                S["plan_compare_df"] = scorer.comparative_table(planets)

        df = S.get("plan_compare_df")
        if df is not None:
            # KPI row — one per planet
            pcols = st.columns(len(planets))
            for col, p in zip(pcols, planets):
                row = df[df["name"]==p.name]
                if row.empty: continue
                esi  = float(row["ESI"].values[0])
                pri  = float(row["overall_priority"].values[0])
                T_c  = float(row["T_surf_C"].values[0])
                hab  = row["habitability_class"].values[0]
                clr  = PLANET_COLORS.get(p.planet_id.value, "#E8C46A")
                esi_bar = "█" * int(esi*10) + "░"*(10-int(esi*10))
                col.markdown(
                    f'<div style="background:rgba(8,12,24,.92);'
                    f'border:1px solid {clr}44;padding:.6rem;'
                    f'border-radius:3px;font-family:monospace;'
                    f'border-top:2px solid {clr};">'
                    f'<div style="color:{clr};font-size:.65rem;font-weight:600;">'
                    f'{p.name}</div>'
                    f'<div style="color:#E8C46A;font-size:.75rem;">ESI {esi:.3f}</div>'
                    f'<div style="color:#555;font-size:.50rem;">{esi_bar}</div>'
                    f'<div style="color:#aaa;font-size:.55rem;">T={T_c:.0f}°C</div>'
                    f'<div style="color:#aaa;font-size:.55rem;">Priority={pri:.3f}</div>'
                    f'<div style="color:{clr};font-size:.50rem;">{hab[:20]}</div>'
                    f'</div>', unsafe_allow_html=True)

            st.markdown("---")
            fig1 = _plot_comparison_overview(df, planets)
            st.pyplot(fig1, width='stretch'); plt.close(fig1)

            fig2 = _plot_radar(df, planets)
            st.pyplot(fig2, width='stretch'); plt.close(fig2)

            with st.expander("◈ Full Comparative Data Table"):
                display_cols = ["name","ESI","SHI","BCI","overall_priority",
                                "T_surf_C","g_surf_earth","atm_pressure_bar",
                                "ocean_fraction","biosig_score",
                                "hz_class","habitability_class","plan_B_score"]
                st.dataframe(df[display_cols].round(4),
                             width='stretch', hide_index=True)
        else:
            st.info("Click the button above to compute the full comparative analysis.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — SINGLE PLANET DETAIL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_single:
        pid_choice = st.selectbox(
            "Select planet", [p.value for p in PlanetID if p != PlanetID.CUSTOM])
        p    = S["plan_planets"].get(pid_choice, make_earth())
        S["plan_active_pid"] = pid_choice
        rpt  = scorer.full_report(p)
        atm  = AtmosphericEngine(p)

        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            clr = PLANET_COLORS.get(pid_choice, "#E8C46A")
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.75rem;
                        border:1px solid {clr}44;border-top:2px solid {clr};
                        border-radius:3px;line-height:2.0;">
            <b style="color:{clr};font-size:.68rem;">── PHYSICAL ──</b><br>
            Mass = <b style="color:#E8C46A;">{p.mass_earth:.3f} M⊕</b>
            = <b>{p.M_kg:.3e} kg</b><br>
            Radius = <b style="color:#E8C46A;">{p.radius_earth:.3f} R⊕</b>
            = <b>{p.R_m/1e3:.0f} km</b><br>
            ρ_bulk = <b>{p.rho_bulk:.0f} kg/m³</b>
            = <b>{p.rho_earth_norm:.3f} ρ⊕</b><br>
            g_surf = <b style="color:#FF8800;">{p.g_surf:.2f} m/s²</b>
            = <b style="color:#FF8800;">{p.surface_gravity_g():.3f} g</b><br>
            v_esc = <b>{p.escape_velocity_kms():.2f} km/s</b><br>
            <b style="color:{clr};font-size:.68rem;">── ORBITAL ──</b><br>
            a = <b>{p.semi_major_AU:.3f} AU</b><br>
            e = <b>{p.eccentricity:.3f}</b><br>
            Period = <b>{p.period_yr:.3f} yr</b><br>
            S_flux = <b>{p.S_flux:.1f} W/m²</b>
            = <b>{p.S_earth:.3f} S⊕</b><br>
            <b style="color:{clr};font-size:.68rem;">── THERMAL ──</b><br>
            T_eq = <b>{p.T_eq:.1f} K</b> ({p.T_eq-273:.0f}°C)<br>
            T_eff = <b style="color:#FF8800;">{p.T_eff:.1f} K</b>
            ({p.T_eff-273:.0f}°C)<br>
            ΔT_gh = <b>{atm.greenhouse_T_increment():.1f} K</b><br>
            Albedo = <b>{p.albedo_bond:.3f}</b><br>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.75rem;
                        border:1px solid {clr}44;border-radius:3px;line-height:2.0;">
            <b style="color:{clr};font-size:.68rem;">── HABITABILITY ──</b><br>
            Global ESI = <b style="color:#E8C46A;">{rpt['ESI']:.4f}</b><br>
            Interior ESI = <b>{rpt['iESI']:.4f}</b><br>
            Surface ESI  = <b>{rpt['sESI']:.4f}</b><br>
            SHI = <b style="color:#81C784;">{rpt['SHI']:.4f}</b><br>
            BCI = <b>{rpt['BCI']:.4f}</b><br>
            Biosig score = <b style="color:#4FC3F7;">{rpt['biosig_score']:.4f}</b><br>
            HZ class = <b style="color:#CE93D8;">{rpt['hz_class']}</b><br>
            Class = <b style="color:{clr};">{rpt['habitability_class'][:28]}</b><br>
            <b style="color:{clr};font-size:.68rem;">── SCORES ──</b><br>
            Overall priority = <b style="color:#E8C46A;">{rpt['overall_priority']:.4f}</b><br>
            Plan B score = <b style="color:#81C784;">{rpt['plan_B_score']:.4f}</b><br>
            Safety = <b>{rpt['safety']:.4f}</b><br>
            <b style="color:{clr};font-size:.68rem;">── ATMOSPHERE ──</b><br>
            Pressure = <b>{p.atm_pressure_Pa/1e3:.2f} kPa</b>
            = <b>{p.atm_pressure_Pa/1e5:.3f} bar</b><br>
            Scale H = <b>{p.H_scale/1e3:.2f} km</b><br>
            μ = <b>{p.composition.mean_molecular_weight():.2f} g/mol</b><br>
            GHE forcing = <b>{p.composition.greenhouse_forcing_W_m2():.2f} W/m²</b><br>
            Runaway GH? = <b>{"YES" if atm.is_runaway_greenhouse() else "No"}</b><br>
            Tidal lock (5Gyr)? = <b>{"YES" if p.is_tidally_locked() else "No"}</b>
            </div>""", unsafe_allow_html=True)

        with c3:
            # ESI meter visual
            _mpl()
            fig_esi, ax_esi = plt.subplots(figsize=(6, 3))
            esi_val = rpt["ESI"]
            categories = ["iESI","sESI","ESI","SHI","BCI","plan_B_score"]
            vals_esi   = [rpt["iESI"],rpt["sESI"],rpt["ESI"],
                          rpt["SHI"],rpt["BCI"],rpt["plan_B_score"]]
            clrs_esi   = [CMAP_HABIT(v) for v in vals_esi]
            bars_esi   = ax_esi.bar(categories, vals_esi,
                                     color=clrs_esi, alpha=0.88)
            ax_esi.bar_label(bars_esi, fmt="%.3f", padding=3,
                              fontsize=8, color="#fff")
            ax_esi.set_ylim(0, 1.0)
            ax_esi.set_ylabel("Score  [0–1]")
            ax_esi.set_title(f"HABITABILITY SCORES — {p.name}")
            ax_esi.set_facecolor("#080c18")
            fig_esi.patch.set_facecolor("#06090e")
            st.pyplot(fig_esi, width='stretch')
            plt.close(fig_esi)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — ATMOSPHERE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_atm:
        pid2  = st.selectbox("Planet for atmosphere",
                              [p.value for p in PlanetID if p != PlanetID.CUSTOM],
                              key="atm_sel")
        p2    = S["plan_planets"].get(pid2, make_earth())
        atm2  = AtmosphericEngine(p2)

        c1, c2 = st.columns([1, 3])
        with c1:
            lapse = atm2.lapse_rate_K_per_km()
            jeans_N2 = atm2.jeans_parameter(28.0)
            jeans_H2 = atm2.jeans_parameter(2.0)
            atm_life = atm2.atmosphere_lifetime_yr()
            rgh_flux = atm2.runaway_greenhouse_flux()
            mgh_flux = atm2.maximum_greenhouse_flux()
            uv_dose  = atm2.surface_uv_dose_W_m2()
            ice_fb   = atm2.ice_albedo_feedback()
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.7rem;
                        border:1px solid rgba(129,199,132,.15);border-radius:3px;
                        line-height:2.0;">
            <b style="color:#81C784;">── LAPSE RATE ──</b><br>
            Γ = <b style="color:#E8C46A;">{lapse:.3f} K/km</b><br>
            (Earth = 6.5 K/km moist)<br>
            <b style="color:#81C784;">── ESCAPE ──</b><br>
            λ_Jeans (N₂) = <b>{jeans_N2:.2f}</b><br>
            λ_Jeans (H₂) = <b>{jeans_H2:.2f}</b><br>
            (λ>20: stable; <1: blowoff)<br>
            t_atm_life ≈ <b>{atm_life:.2e} yr</b><br>
            <b style="color:#81C784;">── CLIMATE LIMITS ──</b><br>
            S_runaway = <b style="color:#D154FF;">{rgh_flux:.0f} W/m²</b><br>
            S_max_GH  = <b>{mgh_flux:.0f} W/m²</b><br>
            Current S = <b>{p2.S_flux:.0f} W/m²</b><br>
            Runaway? <b>{"YES ⚠" if atm2.is_runaway_greenhouse() else "No ✓"}</b><br>
            <b style="color:#81C784;">── RADIATION ──</b><br>
            UV dose = <b style="color:#FF8800;">{uv_dose:.2f} W/m²</b><br>
            Ice-albedo feedback = <b>{ice_fb:.2f}×</b><br>
            CO₂ weathering idx = <b>{atm2.weathering_co2_feedback():.2f}</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            fig_a = _plot_atmosphere(p2)
            st.pyplot(fig_a, width='stretch')
            plt.close(fig_a)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 4 — SPECTRUM & BIOSIGNATURES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_spectrum:
        pid3 = st.selectbox("Planet for spectrum",
                             [p.value for p in PlanetID if p != PlanetID.CUSTOM],
                             key="spec_sel")
        p3   = S["plan_planets"].get(pid3, make_earth())
        sp3  = SpectralEngine(p3)
        fig_s = _plot_spectrum(p3)
        st.pyplot(fig_s, width='stretch'); plt.close(fig_s)
        bio_df = sp3.biosignature_feature_table()
        st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#81C784;">BIOSIGNATURE FEATURE TABLE</div>',
                    unsafe_allow_html=True)
        st.dataframe(bio_df, width='stretch', hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 5 — MILLER'S WORLD
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_miller:
        miller = S["plan_planets"][PlanetID.MILLER.value]
        fig_m  = _plot_miller_special(miller)
        st.pyplot(fig_m, width='stretch'); plt.close(fig_m)
        rpt_m  = scorer.full_report(miller)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.7rem;
                        border:1px solid rgba(79,195,247,.15);border-radius:3px;
                        line-height:2.0;">
            <b style="color:#4FC3F7;">MILLER'S WORLD — KEY PARAMETERS</b><br>
            Mass = {miller.mass_earth:.1f} M⊕ · Radius = {miller.radius_earth:.2f} R⊕<br>
            Surface gravity = {miller.surface_gravity_g():.2f} g<br>
            Global ocean = 100% coverage<br>
            Tidal state: <b>TIDALLY LOCKED to Gargantua</b><br>
            Orbital period ≈ {miller.rotation_period_hr:.1f} hr (= rotation)<br>
            ESI = {rpt_m['ESI']:.3f} · SHI = {rpt_m['SHI']:.3f}<br>
            Plan-B score = {rpt_m['plan_B_score']:.3f}<br>
            T_surf = {miller.T_eff-273:.0f}°C (tidal heating dominant)<br>
            Time dilation: 1h ship = 7yr Earth<br>
            Wave height: ~1.2 km (canon) / {2*G_SI*1e8*M_SUN*miller.R_m/(9.56e11)**3/miller.g_surf/1000:.1f} km (model)
            </div>""", unsafe_allow_html=True)
        with c2:
            risk4  = MissionRiskAssessor(miller)
            rdf4, ov4 = risk4.full_risk_matrix()
            st.dataframe(rdf4, width='stretch', hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 6 — HABITABLE ZONE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_hz:
        c1, c2 = st.columns([1, 3])
        with c1:
            T_s = st.slider("Host star T [K]", 2600, 7200, 4500, 100)
            L_s = st.slider("Host star L [L_sun]", 0.001, 10.0, 0.36, 0.01)
            hz  = scorer.habitable_zone_AU(T_s, L_s)
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.65rem;
                        border:1px solid rgba(129,199,132,.12);border-radius:3px;
                        line-height:2.0;">
            <b style="color:#81C784;">HZ BOUNDARIES</b><br>
            Recent Venus: <b>{hz['recent_venus']:.3f} AU</b><br>
            Runaway GH:   <b style="color:#D154FF;">{hz['runaway_greenhouse']:.3f} AU</b><br>
            Moist GH:     <b>{hz['moist_greenhouse']:.3f} AU</b><br>
            Max GH:       <b style="color:#4FC3F7;">{hz['max_greenhouse']:.3f} AU</b><br>
            Early Mars:   <b>{hz['early_mars']:.3f} AU</b><br>
            <br>Conservative: <b>{hz['conservative_inner']:.3f}–{hz['conservative_outer']:.3f} AU</b><br>
            Optimistic: <b>{hz['optimistic_inner']:.3f}–{hz['optimistic_outer']:.3f} AU</b>
            </div>""", unsafe_allow_html=True)
        with c2:
            fig_hz = _plot_hz_diagram(planets, scorer)
            st.pyplot(fig_hz, width='stretch'); plt.close(fig_hz)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 7 — MISSION RISK
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_risk:
        pid5 = st.selectbox("Planet for risk assessment",
                             [p.value for p in PlanetID if p != PlanetID.CUSTOM],
                             key="risk_sel")
        p5   = S["plan_planets"].get(pid5, make_earth())
        risk5= MissionRiskAssessor(p5)
        rdf5, ov5 = risk5.full_risk_matrix()
        st.markdown(f"""
        <div style="font-family:monospace;font-size:.80rem;font-weight:600;
                    color:#D154FF;margin-bottom:.5rem;">
        Overall Risk: {ov5.value}
        </div>""", unsafe_allow_html=True)
        fig_r5 = _plot_risk_matrix(rdf5, ov5, p5)
        st.pyplot(fig_r5, width='stretch'); plt.close(fig_r5)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 8 — CUSTOM PLANET BUILDER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_custom:
        st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#81C784;">BUILD YOUR OWN PLANET</div>',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            c_mass   = st.slider("Mass (M⊕)", 0.1, 10.0, 1.0, 0.05)
            c_radius = st.slider("Radius (R⊕)", 0.3, 3.0, 1.0, 0.05)
            c_sma    = st.slider("Semi-major axis (AU)", 0.1, 5.0, 1.0, 0.05)
            c_ecc    = st.slider("Eccentricity", 0.0, 0.8, 0.0, 0.01)
            c_albedo = st.slider("Bond albedo", 0.05, 0.95, 0.30, 0.01)
        with c2:
            c_T_star = st.slider("Star T_eff (K)", 2600, 7200, 5778, 100)
            c_L_star = st.slider("Star L (L_sun)", 0.001, 10.0, 1.0, 0.01)
            c_pres   = st.slider("Surface pressure (bar)", 0.001, 10.0, 1.0, 0.05)
            c_ocean  = st.slider("Ocean fraction", 0.0, 1.0, 0.7, 0.05)
            c_ice    = st.slider("Ice fraction", 0.0, 1.0, 0.05, 0.05)
        with c3:
            c_N2  = st.slider("N₂ fraction", 0.0, 1.0, 0.78, 0.01)
            c_O2  = st.slider("O₂ fraction", 0.0, 0.40, 0.21, 0.01)
            c_CO2 = st.slider("CO₂ fraction", 0.0, 0.99, 0.0004, 0.001)
            c_H2O = st.slider("H₂O fraction", 0.0, 0.50, 0.01, 0.005)
            c_CH4 = st.slider("CH₄ fraction", 0.0, 0.10, 1.7e-6, 1e-6, format="%.2e")
            c_O3  = st.slider("O₃ fraction", 0.0, 1e-4, 3e-6, 1e-7, format="%.2e")

        if st.button("⚙ ANALYSE CUSTOM PLANET",
                     width='stretch', type="primary"):
            comp_c = AtmosphericComposition(
                N2=c_N2, O2=c_O2, CO2=c_CO2, H2O=c_H2O,
                CH4=c_CH4, O3=c_O3)
            stype  = (SurfaceType.OCEAN if c_ocean > 0.8 else
                      SurfaceType.ICE   if c_ice > 0.6 else
                      SurfaceType.ROCKY_OCEAN)
            p_c    = Planet(
                name="Custom Planet", planet_id=PlanetID.CUSTOM,
                mass_earth=c_mass, radius_earth=c_radius,
                semi_major_AU=c_sma, eccentricity=c_ecc,
                albedo_bond=c_albedo,
                star_T_K=c_T_star, star_L_W=c_L_star*L_SUN,
                star_M_kg=M_SUN*(c_L_star**0.25),
                star_R_m=R_SUN*(c_L_star**0.5),
                atm_pressure_Pa=c_pres*1e5,
                composition=comp_c, surface_type=stype,
                ocean_fraction=c_ocean, ice_fraction=c_ice)
            S["plan_custom"] = p_c
            S["plan_planets"][PlanetID.CUSTOM.value] = p_c

        p_c = S.get("plan_custom")
        if p_c is not None:
            rpt_c = scorer.full_report(p_c)
            clr_c = "#FFB74D"
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:repeat(6,1fr);
                        gap:.25rem;margin:.5rem 0;">
            {"".join([
                f'<div style="background:rgba(8,12,24,.9);border:1px solid {clr_c}33;'
                f'padding:.35rem;text-align:center;border-radius:2px;font-family:monospace;">'
                f'<div style="color:#555;font-size:.50rem;">{l}</div>'
                f'<div style="color:{clr_c};font-size:.78rem;">{v}</div></div>'
                for l,v in [
                    ("ESI",    f"{rpt_c['ESI']:.3f}"),
                    ("SHI",    f"{rpt_c['SHI']:.3f}"),
                    ("BCI",    f"{rpt_c['BCI']:.3f}"),
                    ("T_surf", f"{rpt_c['T_surf_C']:.0f}°C"),
                    ("g",      f"{rpt_c['g_surf_earth']:.2f}g"),
                    ("Priority",f"{rpt_c['overall_priority']:.3f}"),
                ]
            ])}
            </div>""", unsafe_allow_html=True)

            c_col1, c_col2 = st.columns(2)
            with c_col1:
                fig_ca = _plot_atmosphere(p_c)
                st.pyplot(fig_ca, width='stretch'); plt.close(fig_ca)
            with c_col2:
                fig_cs = _plot_spectrum(p_c)
                st.pyplot(fig_cs, width='stretch'); plt.close(fig_cs)
