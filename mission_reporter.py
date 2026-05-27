"""
mission_reporter.py — Mission Reporting, Lazarus Archive & Plan A/B Engine
ENDURANCE Mission Control | Interstellar Science Platform v3.0.0
═══════════════════════════════════════════════════════════════════════════════
Scientific References:
  [1]  Kip Thorne, "The Science of Interstellar" (W.W. Norton, 2014)
  [2]  NASA Human Research Program — Long Duration Mission Standards
  [3]  Shannon (1948) Bell Syst.Tech.J. 27:379  [Information theory]
  [4]  Bekenstein (1973) PRD 7:2333  [Black hole information]
  [5]  Film canon: Interstellar (2014) Dir. Christopher Nolan  [7]
  [6]  Thorne mission notes: Lazarus probe specifications

Module implements:
  ┌─ LAZARUS MISSION ARCHIVE ───────────────────────────────────────────────┐
  │ 12 probe missions: full manifest, status, data quality, coordinates     │
  │ Lazarus agents: Miller, Mann, Edmunds, Wolf, Kipp, Edmunds, Gargantua  │
  │ Signal quality index per probe: SNR, data completeness, timestamp       │
  │ Planetary survey data: habitability score, environment, suitability     │
  │ Mission priority ranking from NASA gravity observatory                  │
  │ Data integrity validation: checksums, transmission errors              │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ PLAN A ENGINE ─────────────────────────────────────────────────────────┐
  │ Gravity equation progress tracker: 42 coefficients status              │
  │ Colony ship readiness: 100,000+ people, launch sequencing              │
  │ Earth population countdown: blight spread rate model                   │
  │ Quantum gravity data integration: TARS crystal coefficient import      │
  │ Murphy's breakthrough timeline: Earth-side equation solving            │
  │ Colony lift-off delta-v and energy requirements                        │
  │ Station mass budget: Lagrange point parking orbit, transfer burns      │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ PLAN B ENGINE ─────────────────────────────────────────────────────────┐
  │ Embryo bank: 5,000 embryo profiles, genetic diversity index            │
  │ Colony viability assessment: minimum viable population theory          │
  │ Resource allocation: water/food/shelter for 3-generation bootstrap     │
  │ Artificial uterine system: gestation timeline and energy budget        │
  │ Genetic diversity: Founder's Effect mitigation strategy                │
  │ Terraforming timeline: atmosphere modification milestones              │
  │ First-generation survival probability model                            │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ NASA MISSION SCORING ──────────────────────────────────────────────────┐
  │ Achievement system: mission milestones with points                     │
  │ Overall mission success score (0–100)                                  │
  │ Risk-adjusted success probability                                      │
  │ Crew performance metrics                                               │
  │ Data quality index: bits collected per mission day                     │
  │ Legacy score: impact on human survival probability                     │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ DATA DRIVE MANAGEMENT ─────────────────────────────────────────────────┐
  │ Drive submission log: SHA-256 hash + timestamp + bit count             │
  │ TARS crystal archive: quantum data packages with verification          │
  │ NASA transmission queue: priority-ordered data packets                 │
  │ Compression ratio analysis: lossless vs lossy for mission data         │
  │ Data provenance chain: full audit trail from sensor to NASA            │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ BLIGHT SPREAD MODEL ───────────────────────────────────────────────────┐
  │ Crop failure progression: wheat → okra → corn timeline                 │
  │ Population carrying capacity vs food production                        │
  │ Food scarcity index: calories available per person per day             │
  │ Time-to-extinction estimate from current blight spread rate            │
  │ Colony urgency score: mission deadline calculator                      │
  └──────────────────────────────────────────────────────────────────────────┘

"Do not go gentle into that good night. Rage, rage against the dying of the light."
                       — Dylan Thomas; Prof. Brand's farewell, 2067
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations
import hashlib, math, time, uuid, warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import scipy.optimize as sci_opt
import scipy.integrate as sci_int
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot     as plt
import matplotlib.gridspec   as gridspec
import matplotlib.patches    as mpatches
import matplotlib.ticker     as mticker
import matplotlib.colors     as mcolors
from matplotlib.colors       import LinearSegmentedColormap
from matplotlib.patches      import FancyBboxPatch, Circle, FancyArrowPatch
import streamlit as st
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# §1  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
G_SI      = 6.674_30e-11
C_SI      = 2.997_924_58e8
M_SUN     = 1.989_000e30
AU        = 1.495_978_707e11
LY        = 9.460_730_472e15
YEAR_S    = 3.155_760e7
DAY_S     = 86_400.0
EARTH_POP_2067   = 3.5e9       # population at mission start (~2067)
BLIGHT_ONSET_YR  = 2049        # year blight began spreading
MISSION_START_YR = 2067
COLONY_CAP       = 100_000     # plan A colony ship capacity
EMBRYO_COUNT     = 5_000       # plan B embryo bank

# ══════════════════════════════════════════════════════════════════════════════
# §2  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════
class ProbeStatus(Enum):
    ACTIVE        = "ACTIVE — transmitting"
    SILENT        = "SILENT — no signal"
    CONFIRMED_OK  = "CONFIRMED HABITABLE"
    CONFIRMED_BAD = "CONFIRMED UNINHABITABLE"
    FALSIFIED     = "DATA FALSIFIED"
    DESTROYED     = "DESTROYED"
    UNKNOWN       = "UNKNOWN"

class PlanStatus(Enum):
    NOT_STARTED   = "Not started"
    IN_PROGRESS   = "In progress"
    BLOCKED       = "Blocked"
    COMPLETE      = "Complete"
    ABANDONED     = "Abandoned"

class AchievementTier(Enum):
    BRONZE   = "Bronze"
    SILVER   = "Silver"
    GOLD     = "Gold"
    PLATINUM = "Platinum"
    LEGEND   = "Legend — Humanity Saved"

class DataDriveStatus(Enum):
    PENDING     = "Pending transmission"
    TRANSMITTED = "Transmitted to NASA"
    VERIFIED    = "Verified — SHA match"
    CORRUPTED   = "Corrupted — checksum fail"
    ARCHIVED    = "Archived in crystal"

# ══════════════════════════════════════════════════════════════════════════════
# §3  LAZARUS MISSION ARCHIVE
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class LazarusProbe:
    probe_id:         int
    agent_name:       str
    planet_name:      str
    launch_year:      int
    arrival_year:     int
    status:           ProbeStatus
    signal_snr_db:    float        # signal quality [dB]
    data_completeness:float        # 0–1
    habitability_score: float      # 0–1 (agent's reported score)
    actual_score:     float        # 0–1 (true score — may differ from report)
    coordinates_sent: bool = False
    last_signal_year: int  = 0
    notes:            str  = ""
    planet_temp_C:    float = 0.0
    planet_pressure_bar: float = 1.0
    planet_water:     bool = False
    agent_alive:      bool = False
    data_falsified:   bool = False
    uid: str = field(default_factory=lambda: uuid.uuid4().hex[:8].upper())

    @property
    def signal_quality_label(self) -> str:
        if self.signal_snr_db > 20:  return "EXCELLENT"
        if self.signal_snr_db > 10:  return "GOOD"
        if self.signal_snr_db > 0:   return "MARGINAL"
        return "LOST"

    @property
    def mission_duration_yr(self) -> int:
        return self.arrival_year - self.launch_year

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ID":             self.probe_id,
            "Agent":          self.agent_name,
            "Planet":         self.planet_name,
            "Launch":         self.launch_year,
            "Arrival":        self.arrival_year,
            "Status":         self.status.value,
            "SNR (dB)":       self.signal_snr_db,
            "Data %":         round(self.data_completeness*100, 1),
            "Reported ESI":   round(self.habitability_score, 3),
            "Actual ESI":     round(self.actual_score, 3),
            "Falsified":      self.data_falsified,
            "Agent alive":    self.agent_alive,
            "Water":          self.planet_water,
            "T_surf (°C)":    self.planet_temp_C,
            "Pressure (bar)": self.planet_pressure_bar,
            "Notes":          self.notes[:50],
        }


def build_lazarus_archive() -> List[LazarusProbe]:
    """
    12 Lazarus probes — canonical Interstellar film manifest [5,1].
    Missions 1–10: initial wave. Missions 11–12: second wave (Mann planet etc.)
    """
    probes = [
        LazarusProbe(1, "Dr. Lazarus-1 (Wolf)", "Wolf 1061c",
                     2047, 2054, ProbeStatus.SILENT, -5.2, 0.12, 0.45, 0.22,
                     planet_temp_C=-85, planet_pressure_bar=0.04,
                     notes="Signal lost 2 years after landing. Thin atmosphere."),
        LazarusProbe(2, "Dr. Lazarus-2 (Pantagruel)", "Pantagruel b",
                     2048, 2055, ProbeStatus.SILENT, -12.1, 0.05, 0.30, 0.18,
                     planet_temp_C=-120, planet_pressure_bar=0.001,
                     notes="No signal after insertion burn. Impact suspected."),
        LazarusProbe(3, "Dr. Lazarus-3 (Kipp)", "Kipp System IV",
                     2049, 2057, ProbeStatus.CONFIRMED_BAD, 8.4, 0.65, 0.40, 0.21,
                     planet_temp_C=52, planet_pressure_bar=3.2,
                     notes="Dense CO₂, pressure lethal. Agent Kipp survived 4yr."),
        LazarusProbe(4, "Dr. Lazarus-4 (Laura)", "HD 40307g",
                     2049, 2058, ProbeStatus.SILENT, -3.1, 0.08, 0.55, 0.35,
                     planet_temp_C=18, planet_pressure_bar=1.1, planet_water=True,
                     notes="Promising signal for 6 months, then lost. Water detected."),
        LazarusProbe(5, "Dr. Lazarus-5 (Doyle)", "Gliese 667Cc",
                     2050, 2058, ProbeStatus.CONFIRMED_BAD, 14.2, 0.78, 0.38, 0.28,
                     planet_temp_C=-15, planet_pressure_bar=0.8,
                     notes="Tidally locked. Day side too hot, night too cold."),
        LazarusProbe(6, "Dr. Miller", "Miller's World",
                     2051, 2059, ProbeStatus.ACTIVE, 22.5, 0.91, 0.72, 0.68,
                     coordinates_sent=True, last_signal_year=2059,
                     planet_temp_C=28, planet_pressure_bar=1.8, planet_water=True,
                     agent_alive=False,
                     notes="Signal active. Massive tidal wave event. Global ocean. 1h=7yr."),
        LazarusProbe(7, "Dr. Mann", "Mann's Planet",
                     2052, 2061, ProbeStatus.FALSIFIED, 18.9, 0.85, 0.87, 0.12,
                     coordinates_sent=True, last_signal_year=2063,
                     planet_temp_C=-73, planet_pressure_bar=0.08,
                     agent_alive=True, data_falsified=True,
                     notes="⚠ DATA FALSIFIED. Mann survived by sending false habitability data."),
        LazarusProbe(8, "Dr. Edmunds", "Edmunds' Planet",
                     2052, 2062, ProbeStatus.CONFIRMED_OK, 25.1, 0.94, 0.88, 0.85,
                     coordinates_sent=True, last_signal_year=2062,
                     planet_temp_C=12, planet_pressure_bar=0.75, planet_water=True,
                     agent_alive=False,
                     notes="Best data. Edmunds died in wind storm. Planet confirmed habitable."),
        LazarusProbe(9, "Dr. Lazarus-9 (Chen)", "Tau Ceti e",
                     2053, 2062, ProbeStatus.SILENT, -8.7, 0.02, 0.25, 0.15,
                     planet_temp_C=-200, planet_pressure_bar=0.0,
                     notes="No atmosphere. Frozen. Signal lost pre-landing."),
        LazarusProbe(10, "Dr. Lazarus-10 (Amelia)", "Kepler-186f",
                     2054, 2063, ProbeStatus.UNKNOWN, 2.1, 0.30, 0.60, 0.42,
                     planet_temp_C=-25, planet_pressure_bar=0.5,
                     notes="Weak signal. Atmospheric data ambiguous. Water ice possible."),
        LazarusProbe(11, "Dr. Lazarus-11 (Rye)", "Proxima Centauri b",
                     2055, 2059, ProbeStatus.CONFIRMED_BAD, 11.2, 0.55, 0.35, 0.20,
                     planet_temp_C=-40, planet_pressure_bar=0.2,
                     notes="Tidally locked. Stellar flares decimated atmosphere."),
        LazarusProbe(12, "Dr. Lazarus-12 (Torres)", "TRAPPIST-1e",
                     2056, 2063, ProbeStatus.SILENT, -15.0, 0.03, 0.70, 0.50,
                     planet_temp_C=5, planet_pressure_bar=1.0, planet_water=True,
                     notes="Promising. Signal lost during orbital insertion."),
    ]
    return probes


# ══════════════════════════════════════════════════════════════════════════════
# §4  PLAN A ENGINE
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class PlanAStatus:
    """
    Plan A: solve Murphy's gravitational equation → lift humanity off Earth.
    Requires all 42 equation coefficients from Gargantua's singularity.
    Colony ships: 100,000 people per ship, ~10 ships needed.
    """
    coefficients_known:  int   = 0
    coefficients_total:  int   = 42
    tars_contribution:   int   = 0    # coefficients from TARS crystal
    murph_contribution:  int   = 0    # coefficients from Murph's Earth-side work
    brand_contribution:  int   = 12   # Prof. Brand's 40 years of work
    plan_status:         PlanStatus = PlanStatus.IN_PROGRESS
    colony_ships_ready:  int   = 0
    colony_ships_total:  int   = 10
    people_per_ship:     int   = COLONY_CAP
    lift_off_dv_kms:     float = 9.5   # Δv to orbit [km/s]
    station_orbit_km:    float = 400.0
    transfer_orbit_AU:   float = 1.0   # destination
    years_to_build:      float = 5.0   # manufacturing time
    breakthrough_year:   Optional[int] = None

    def __post_init__(self):
        self.coefficients_known = (self.tars_contribution +
                                   self.murph_contribution +
                                   self.brand_contribution)
        self.coefficients_known = min(self.coefficients_known,
                                      self.coefficients_total)

    @property
    def fraction_complete(self) -> float:
        return self.coefficients_known / self.coefficients_total

    @property
    def solved(self) -> bool:
        return self.coefficients_known >= self.coefficients_total

    def colony_capacity(self) -> int:
        return self.colony_ships_ready * self.people_per_ship

    def lift_energy_J(self) -> float:
        """Energy to lift 100,000 people to orbit."""
        m_total = self.people_per_ship * 100  # ~100 kg/person
        dv      = self.lift_off_dv_kms * 1e3
        return 0.5 * m_total * dv**2

    def summary(self) -> Dict[str, Any]:
        return {
            "equation_pct":       round(self.fraction_complete*100, 2),
            "coefficients_known": self.coefficients_known,
            "coefficients_total": self.coefficients_total,
            "tars_coefficients":  self.tars_contribution,
            "murph_coefficients": self.murph_contribution,
            "brand_legacy":       self.brand_contribution,
            "solved":             self.solved,
            "plan_status":        self.plan_status.value,
            "colony_ships_ready": self.colony_ships_ready,
            "total_capacity":     self.colony_capacity(),
            "lift_dv_kms":        self.lift_off_dv_kms,
            "lift_energy_J":      self.lift_energy_J(),
            "breakthrough_year":  self.breakthrough_year,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §5  PLAN B ENGINE
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class EmbryoProfile:
    embryo_id:    int
    genetic_code: str          # SHA-256 prefix (simulated)
    sex:          str          # "M" / "F"
    genetic_diversity_idx: float  # 0–1 (1 = maximally diverse)
    disease_resistance:   float
    radiation_tolerance:  float
    cognitive_potential:  float
    physical_potential:   float
    viability_pct:        float   # cryopreservation viability

    def fitness_score(self) -> float:
        return np.mean([self.disease_resistance, self.radiation_tolerance,
                        self.cognitive_potential, self.physical_potential,
                        self.viability_pct/100])


class EmbryoBank:
    """5,000 frozen embryo bank — Plan B genetic seed vault."""

    def __init__(self, n_embryos: int = EMBRYO_COUNT):
        self.n        = n_embryos
        self.embryos  = self._generate_bank(n_embryos)
        self.cryo_temp_C   = -196.0   # liquid nitrogen
        self.viability_avg = np.mean([e.viability_pct for e in self.embryos])
        self.diversity_idx = self._compute_diversity()

    def _generate_bank(self, n: int) -> List[EmbryoProfile]:
        np.random.seed(2067)
        embryos = []
        for i in range(n):
            code = hashlib.sha256(str(i).encode()).hexdigest()[:12]
            sex  = "F" if i % 2 else "M"
            embryos.append(EmbryoProfile(
                embryo_id=i, genetic_code=code, sex=sex,
                genetic_diversity_idx = float(np.random.beta(8, 2)),
                disease_resistance    = float(np.random.beta(6, 2)),
                radiation_tolerance   = float(np.random.beta(5, 3)),
                cognitive_potential   = float(np.random.beta(7, 2)),
                physical_potential    = float(np.random.beta(6, 2)),
                viability_pct         = float(np.random.normal(94, 3)),
            ))
        return embryos

    def _compute_diversity(self) -> float:
        """Shannon diversity index from genetic codes."""
        codes = [e.genetic_code[:4] for e in self.embryos]
        unique, counts = np.unique(codes, return_counts=True)
        p = counts/len(codes)
        return float(-np.sum(p*np.log2(p+1e-10)) / np.log2(len(unique)+1))

    def fitness_distribution(self) -> np.ndarray:
        return np.array([e.fitness_score() for e in self.embryos])

    def top_embryos(self, n: int = 20) -> pd.DataFrame:
        sorted_e = sorted(self.embryos, key=lambda e: e.fitness_score(), reverse=True)
        rows = [{
            "ID": e.embryo_id, "Code": e.genetic_code, "Sex": e.sex,
            "Diversity": round(e.genetic_diversity_idx, 3),
            "Disease Res.": round(e.disease_resistance, 3),
            "Rad. Tol.":  round(e.radiation_tolerance, 3),
            "Cognitive":  round(e.cognitive_potential, 3),
            "Physical":   round(e.physical_potential, 3),
            "Viability%": round(e.viability_pct, 1),
            "Fitness":    round(e.fitness_score(), 3),
        } for e in sorted_e[:n]]
        return pd.DataFrame(rows)

    def summary(self) -> Dict[str, Any]:
        fit = self.fitness_distribution()
        return {
            "total_embryos":    self.n,
            "male_count":       sum(1 for e in self.embryos if e.sex=="M"),
            "female_count":     sum(1 for e in self.embryos if e.sex=="F"),
            "avg_viability_pct": round(self.viability_avg, 2),
            "diversity_index":  round(self.diversity_idx, 4),
            "avg_fitness":      round(float(fit.mean()), 4),
            "min_fitness":      round(float(fit.min()), 4),
            "max_fitness":      round(float(fit.max()), 4),
            "cryo_temp_C":      self.cryo_temp_C,
        }


@dataclass
class PlanBStatus:
    """
    Plan B: seed Edmunds' planet with embryo bank — restart humanity.
    Prof. Brand (Sr.) always knew Plan A was impossible — deliberately withheld.
    Amelia Brand executes Plan B after Gargantua slingshot.
    """
    embryo_bank:        EmbryoBank = field(default_factory=EmbryoBank)
    plan_status:        PlanStatus = PlanStatus.IN_PROGRESS
    destination_planet: str        = "Edmunds' Planet"
    landing_year:       Optional[int] = None
    first_birth_year:   Optional[int] = None
    mvp_threshold:      int  = 160       # minimum viable population
    gen1_survival_pct:  float = 0.78    # first generation survival probability
    terraforming_years: int   = 50       # years to breathable atmosphere
    colony_ready_year:  Optional[int] = None
    brand_present:      bool  = True     # Dr. Brand survived to execute Plan B

    def viable_embryos(self) -> int:
        """Number of embryos expected to survive cryopreservation."""
        return int(self.embryo_bank.n * self.embryo_bank.viability_avg/100)

    def gen1_population(self) -> int:
        return int(self.viable_embryos() * self.gen1_survival_pct)

    def gen2_population(self) -> int:
        return int(self.gen1_population() * 2.2)   # reproduction rate

    def exceeds_mvp(self) -> bool:
        return self.gen1_population() >= self.mvp_threshold

    def genetic_bottleneck_risk(self) -> float:
        """
        Founder's Effect severity: inbreeding coefficient after n generations.
        F ≈ 1/(2N_e) per generation where N_e = effective population.
        Risk score 0–1 (higher = more bottleneck).
        """
        Ne = self.gen1_population() * self.embryo_bank.diversity_idx
        F  = 1.0/(2*max(Ne, 1)) * 10   # after 10 generations
        return float(np.clip(F, 0, 1))

    def summary(self) -> Dict[str, Any]:
        return {
            "destination":      self.destination_planet,
            "plan_status":      self.plan_status.value,
            "embryo_count":     self.embryo_bank.n,
            "viable_embryos":   self.viable_embryos(),
            "gen1_population":  self.gen1_population(),
            "gen2_population":  self.gen2_population(),
            "mvp_threshold":    self.mvp_threshold,
            "exceeds_mvp":      self.exceeds_mvp(),
            "bottleneck_risk":  round(self.genetic_bottleneck_risk(), 4),
            "gen1_survival_%":  self.gen1_survival_pct*100,
            "terraforming_yr":  self.terraforming_years,
            "brand_present":    self.brand_present,
            "landing_year":     self.landing_year,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §6  BLIGHT SPREAD MODEL
# ══════════════════════════════════════════════════════════════════════════════
class BlightSpreadModel:
    """
    Models the global agricultural collapse (Blight) that drives the mission.
    Logistic spread model with crop-specific extinction timelines.
    """
    CROPS = {
        "Wheat":   {"onset_yr": 2049, "K": 0.35, "severity": 0.85},
        "Corn":    {"onset_yr": 2053, "K": 0.28, "severity": 0.92},
        "Rice":    {"onset_yr": 2056, "K": 0.22, "severity": 0.78},
        "Soy":     {"onset_yr": 2058, "K": 0.18, "severity": 0.88},
        "Okra":    {"onset_yr": 2060, "K": 0.40, "severity": 0.70},
        "Potato":  {"onset_yr": 2061, "K": 0.30, "severity": 0.75},
        "Cassava": {"onset_yr": 2063, "K": 0.25, "severity": 0.65},
    }

    def blight_fraction(self, crop: str, year: float) -> float:
        """Fraction of crop destroyed by given year (logistic model)."""
        if crop not in self.CROPS:
            return 0.0
        p      = self.CROPS[crop]
        t0     = p["onset_yr"]; K = p["K"]; sev = p["severity"]
        t_rel  = max(0.0, year - t0)
        # Logistic growth of blight spread
        frac   = sev / (1 + math.exp(-K*(t_rel - 10.0)))
        return float(np.clip(frac, 0, sev))

    def food_production_index(self, year: float) -> float:
        """
        Global food production index (1.0 = pre-blight baseline).
        Weighted average over all crops.
        """
        weights = {"Wheat":0.25,"Corn":0.25,"Rice":0.20,
                   "Soy":0.10,"Okra":0.05,"Potato":0.10,"Cassava":0.05}
        total = 0.0
        for crop, w in weights.items():
            loss  = self.blight_fraction(crop, year)
            total += w * (1.0 - loss)
        return float(np.clip(total, 0, 1))

    def calories_per_person_per_day(self, year: float) -> float:
        """Calories available globally, per person per day."""
        fpi   = self.food_production_index(year)
        base  = 2200.0  # pre-blight baseline
        return base * fpi * 0.85   # 85% distribution efficiency

    def carrying_capacity(self, year: float) -> float:
        """Earth human carrying capacity at given food production."""
        cal   = self.calories_per_person_per_day(year)
        frac  = cal / 2200.0
        return EARTH_POP_2067 * frac * 0.80   # 80% survival per deficiency level

    def extinction_year(self) -> float:
        """Year when carrying capacity drops to zero."""
        try:
            yr = sci_opt.brentq(
                lambda y: self.carrying_capacity(y), 2060, 2200,
                xtol=0.1)
            return yr
        except Exception:
            return 2140.0

    def population_projection(self, yr_start: float = 2060,
                               yr_end: float = 2120,
                               n: int = 120) -> pd.DataFrame:
        """Year-by-year population projection under blight."""
        years = np.linspace(yr_start, yr_end, n)
        pop   = np.array([self.carrying_capacity(y) for y in years])
        fpi   = np.array([self.food_production_index(y) for y in years])
        cal   = np.array([self.calories_per_person_per_day(y) for y in years])
        return pd.DataFrame({
            "year": years,
            "population": pop,
            "food_production_index": fpi,
            "cal_per_person_day": cal,
            "mission_urgency": 1.0 - pop/EARTH_POP_2067,
        })

    def crop_timeline(self, yr_start: float = 2048,
                       yr_end: float = 2100, n: int = 200) -> pd.DataFrame:
        years = np.linspace(yr_start, yr_end, n)
        rows = {"year": years}
        for crop in self.CROPS:
            rows[crop] = [self.blight_fraction(crop, y) for y in years]
        return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# §7  MISSION ACHIEVEMENT SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class Achievement:
    name:        str
    description: str
    points:      int
    tier:        AchievementTier
    unlocked:    bool  = False
    unlock_date: float = 0.0
    uid: str = field(default_factory=lambda: uuid.uuid4().hex[:6].upper())

    def unlock(self):
        self.unlocked   = True
        self.unlock_date= time.time()


ACHIEVEMENT_CATALOGUE: List[Dict] = [
    {"name": "Departure",       "desc": "Endurance clears Earth orbit",
     "pts": 50,  "tier": AchievementTier.BRONZE},
    {"name": "Ringed Giant",    "desc": "Saturn flyby successful",
     "pts": 100, "tier": AchievementTier.BRONZE},
    {"name": "Through The Eye", "desc": "Wormhole transit complete",
     "pts": 250, "tier": AchievementTier.SILVER},
    {"name": "First Contact",   "desc": "First planet survey complete",
     "pts": 150, "tier": AchievementTier.SILVER},
    {"name": "The Wave",        "desc": "Miller's World surface operations",
     "pts": 200, "tier": AchievementTier.SILVER},
    {"name": "Truth Revealed",  "desc": "Mann's deception uncovered",
     "pts": 100, "tier": AchievementTier.BRONZE},
    {"name": "Slingshot",       "desc": "Gargantua gravity assist complete",
     "pts": 400, "tier": AchievementTier.GOLD},
    {"name": "Into The Dark",   "desc": "Cooper enters Gargantua",
     "pts": 500, "tier": AchievementTier.GOLD},
    {"name": "42 Coefficients", "desc": "Murphy's equation solved",
     "pts": 1000,"tier": AchievementTier.PLATINUM},
    {"name": "Love Transcends", "desc": "TARS data transmitted via watch-hand",
     "pts": 750, "tier": AchievementTier.PLATINUM},
    {"name": "Plan B Executed", "desc": "Embryo bank delivered to Edmunds",
     "pts": 800, "tier": AchievementTier.PLATINUM},
    {"name": "Humanity Endures","desc": "Colony established — species survives",
     "pts": 5000,"tier": AchievementTier.LEGEND},
]


class MissionScorer:
    def __init__(self):
        self.achievements = [
            Achievement(a["name"], a["desc"], a["pts"], a["tier"])
            for a in ACHIEVEMENT_CATALOGUE
        ]
        self.bonus_log: List[Dict] = []

    def unlock(self, name: str) -> Optional[Achievement]:
        for a in self.achievements:
            if a.name == name and not a.unlocked:
                a.unlock()
                return a
        return None

    def total_points(self) -> int:
        return sum(a.points for a in self.achievements if a.unlocked)

    def max_points(self) -> int:
        return sum(a.points for a in self.achievements)

    def success_score(self) -> float:
        return self.total_points() / max(self.max_points(), 1)

    def tier_summary(self) -> Dict[str, int]:
        d = {t.value: 0 for t in AchievementTier}
        for a in self.achievements:
            if a.unlocked:
                d[a.tier.value] += 1
        return d

    def achievements_df(self) -> pd.DataFrame:
        rows = [{
            "Achievement":  a.name,
            "Description":  a.description,
            "Points":       a.points,
            "Tier":         a.tier.value,
            "Unlocked":     a.unlocked,
            "When":         time.strftime('%H:%M:%S', time.localtime(a.unlock_date))
                            if a.unlocked else "—",
        } for a in self.achievements]
        return pd.DataFrame(rows)

    def risk_adjusted_probability(self, unlocked_count: int) -> float:
        """
        Probability of mission success given number of milestones reached.
        Simple Bayesian update: each milestone reduces uncertainty.
        """
        n_total = len(self.achievements)
        prior   = 0.15    # 15% prior probability (it's a long shot)
        update  = 0.07    # each milestone adds ~7% probability
        return float(np.clip(prior + unlocked_count*update, 0, 0.99))


# ══════════════════════════════════════════════════════════════════════════════
# §8  DATA DRIVE MANAGER
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class DataDrive:
    drive_id:     str   = field(default_factory=lambda: "DD-"+uuid.uuid4().hex[:6].upper())
    source:       str   = "ENDURANCE"
    destination:  str   = "NASA_GRAVITY_OBS"
    content_desc: str   = "Mission telemetry"
    size_bits:    int   = 0
    status:       DataDriveStatus = DataDriveStatus.PENDING
    sha256_hash:  str   = ""
    timestamp:    float = field(default_factory=time.time)
    compression_ratio: float = 1.0
    is_tars_crystal:   bool  = False
    murphy_coeffs:     int   = 0   # number of equation coefficients
    verified:     bool  = False

    def __post_init__(self):
        if not self.sha256_hash:
            payload = f"{self.drive_id}{self.content_desc}{self.size_bits}"
            self.sha256_hash = hashlib.sha256(payload.encode()).hexdigest()

    def verify(self) -> bool:
        payload = f"{self.drive_id}{self.content_desc}{self.size_bits}"
        expected = hashlib.sha256(payload.encode()).hexdigest()
        self.verified = (expected == self.sha256_hash)
        if self.verified:
            self.status = DataDriveStatus.VERIFIED
        else:
            self.status = DataDriveStatus.CORRUPTED
        return self.verified

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Drive ID":     self.drive_id,
            "Source":       self.source,
            "Destination":  self.destination,
            "Content":      self.content_desc[:40],
            "Size (Mbits)": round(self.size_bits/1e6, 2),
            "Compressed x": round(self.compression_ratio, 2),
            "Status":       self.status.value,
            "SHA-256":      self.sha256_hash[:16]+"...",
            "TARS Crystal": self.is_tars_crystal,
            "Murphy Coeffs":self.murphy_coeffs,
            "Verified":     self.verified,
        }


class DataDriveManager:
    def __init__(self):
        self.drives: List[DataDrive] = []
        self._seed_drives()

    def _seed_drives(self):
        """Pre-populate with canonical mission data drives."""
        drives_spec = [
            ("ENDURANCE", "NASA_GRAVITY_OBS", "Mission telemetry Day 0–730",
             8e9, False, 0),
            ("MILLER_SURVEY", "NASA_GRAVITY_OBS", "Miller World surface scans",
             2.5e9, False, 0),
            ("MANN_SURVEY", "NASA_GRAVITY_OBS", "Mann Planet survey (corrupted)",
             1.2e9, False, 0),
            ("TARS_SINGULARITY", "MURPH_EARTH", "TARS quantum gravity crystal — 42 coefficients",
             4.8e11, True, 42),
            ("EDMUNDS_SURVEY", "NASA_GRAVITY_OBS", "Edmunds Planet confirmed habitable",
             3.6e9, False, 0),
        ]
        for src, dst, desc, bits, crystal, coeffs in drives_spec:
            d = DataDrive(source=src, destination=dst, content_desc=desc,
                          size_bits=int(bits), is_tars_crystal=crystal,
                          murphy_coeffs=coeffs)
            if crystal:
                d.status = DataDriveStatus.TRANSMITTED
            d.verify()
            self.drives.append(d)

    def submit_drive(self, content: str, size_bits: int,
                     source: str = "ENDURANCE",
                     destination: str = "NASA",
                     is_tars: bool = False,
                     coeffs: int = 0) -> DataDrive:
        d = DataDrive(source=source, destination=destination,
                      content_desc=content, size_bits=size_bits,
                      is_tars_crystal=is_tars, murphy_coeffs=coeffs)
        d.verify()
        d.status = DataDriveStatus.TRANSMITTED
        self.drives.append(d)
        return d

    def total_data_bits(self) -> int:
        return sum(d.size_bits for d in self.drives)

    def tars_crystal_drives(self) -> List[DataDrive]:
        return [d for d in self.drives if d.is_tars_crystal]

    def drives_df(self) -> pd.DataFrame:
        return pd.DataFrame([d.to_dict() for d in self.drives])

    def integrity_report(self) -> Dict[str, Any]:
        total   = len(self.drives)
        verified= sum(1 for d in self.drives if d.verified)
        corrupt = sum(1 for d in self.drives if d.status==DataDriveStatus.CORRUPTED)
        crystal = len(self.tars_crystal_drives())
        return {
            "total_drives":     total,
            "verified":         verified,
            "corrupted":        corrupt,
            "tars_crystals":    crystal,
            "integrity_pct":    round(verified/max(total,1)*100, 2),
            "total_bits":       self.total_data_bits(),
            "total_GB":         round(self.total_data_bits()/8e9, 3),
            "total_murphy_coeffs": sum(d.murphy_coeffs for d in self.drives),
        }


# ══════════════════════════════════════════════════════════════════════════════
# §9  MISSION REPORTER MASTER CLASS
# ══════════════════════════════════════════════════════════════════════════════
class MissionReporter:
    """
    Master mission reporting: integrates all sub-systems into
    unified mission status report, NASA transmission, and
    historical archive generation.
    """

    def __init__(self):
        self.lazarus    = build_lazarus_archive()
        self.plan_a     = PlanAStatus(tars_contribution=30, murph_contribution=0,
                                       brand_contribution=12)
        self.plan_b     = PlanBStatus()
        self.blight     = BlightSpreadModel()
        self.scorer     = MissionScorer()
        self.drives     = DataDriveManager()
        self.report_log: List[Dict] = []
        self._seed_achievements()

    def _seed_achievements(self):
        for name in ["Departure","Ringed Giant","Through The Eye",
                     "First Contact","The Wave","Truth Revealed"]:
            self.scorer.unlock(name)

    def lazarus_df(self) -> pd.DataFrame:
        return pd.DataFrame([p.to_dict() for p in self.lazarus])

    def best_candidates(self, n: int = 3) -> List[LazarusProbe]:
        eligible = [p for p in self.lazarus
                    if p.status not in (ProbeStatus.CONFIRMED_BAD,
                                         ProbeStatus.DESTROYED,
                                         ProbeStatus.FALSIFIED)]
        return sorted(eligible, key=lambda p: p.actual_score, reverse=True)[:n]

    def generate_nasa_report(self) -> Dict[str, Any]:
        blight_ext  = self.blight.extinction_year()
        urgency     = 1.0 - self.blight.carrying_capacity(
                          MISSION_START_YR + 30) / EARTH_POP_2067
        return {
            "report_id":        "LAZARUS-ENDURANCE-FINAL",
            "timestamp":        time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "mission_day":      730,
            "plan_a":           self.plan_a.summary(),
            "plan_b":           self.plan_b.summary(),
            "blight_extinction_year": round(blight_ext, 1),
            "mission_urgency":  round(urgency, 4),
            "lazarus_complete": len(self.lazarus),
            "best_planet":      self.best_candidates(1)[0].planet_name,
            "total_score":      self.scorer.total_points(),
            "success_prob":     round(self.scorer.risk_adjusted_probability(
                                       sum(1 for a in self.scorer.achievements if a.unlocked)), 4),
            "data_integrity":   self.drives.integrity_report(),
            "embryo_summary":   self.plan_b.embryo_bank.summary(),
        }

    def mission_timeline(self) -> pd.DataFrame:
        """Full canonical mission timeline with Earth time."""
        events = [
            (2049, "Blight begins spreading",           "EARTH",     "CRITICAL"),
            (2063, "NASA Gravity Observatory discovers wormhole", "EARTH", "DISCOVERY"),
            (2063, "Endurance crew assembled",          "EARTH",     "MISSION"),
            (2065, "Endurance launches",                "EARTH",     "MISSION"),
            (2067, "Saturn arrival; wormhole transit",  "SATURN",    "MISSION"),
            (2067, "Gargantua system entry",            "GARGANTUA", "MISSION"),
            (2090, "Miller World survey (3hr ship = 23yr Earth)", "MILLER", "SURVEY"),
            (2090, "Mann Planet survey — Mann's betrayal revealed","MANN", "CRITICAL"),
            (2091, "Gargantua slingshot; TARS enters singularity","GARGANTUA","MISSION"),
            (2091, "Cooper enters tesseract; transmits quantum data","TESSERACT","DISCOVERY"),
            (2091, "Murph solves Murphy's Equation — Plan A complete","EARTH","BREAKTHROUGH"),
            (2092, "Colony ships begin launch sequence",  "EARTH",   "PLAN_A"),
            (2092, "Brand lands on Edmunds — Plan B begun","EDMUNDS","PLAN_B"),
            (2157, "First Plan B generation reaches adulthood","EDMUNDS","COLONY"),
        ]
        rows = []
        for yr, evt, loc, cat in events:
            rows.append({"Year": yr, "Event": evt, "Location": loc, "Category": cat})
        return pd.DataFrame(rows)
        return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# §9A  NSGA-II MULTI-OBJECTIVE EMBRYO OPTIMIZER (Plan B Genetic Diversity)
# ══════════════════════════════════════════════════════════════════════════════
class PlanBGeneticOptimizer:
    """
    Simulates the selection of the initial 5,000 fertilized embryos for Plan B.
    Uses the NSGA-II (Non-dominated Sorting Genetic Algorithm II) concept
    to optimize a multi-objective problem:
      Objective 1: Maximize genetic diversity (minimize inbreeding).
      Objective 2: Maximize environmental adaptability (e.g., radiation resistance).
      Objective 3: Maximize critical skill predispositions (e.g., engineering).
      
    For the simulation, we use a surrogate model representing the Pareto front
    of embryo batches.
    """
    
    def __init__(self, target_population: int = 5000):
        self.pop_size = target_population
        
    def generate_pareto_front(self, n_points: int = 100) -> Dict[str, np.ndarray]:
        """
        Generates a synthetic 3D Pareto front for embryo batch selection.
        Trade-off: High diversity vs High specific adaptability.
        """
        # Generate random points on a 3D spherical shell quadrant (Pareto surface)
        u = np.random.rand(n_points)
        v = np.random.rand(n_points)
        
        theta = 0.5 * math.pi * u
        phi = 0.5 * math.pi * v
        
        # Base scores (normalized 0 to 1)
        diversity = np.sin(theta) * np.cos(phi)
        adaptability = np.sin(theta) * np.sin(phi)
        skills = np.cos(theta)
        
        # Add some noise and scale
        diversity = 70.0 + 30.0 * diversity + np.random.randn(n_points) * 1.5
        adaptability = 60.0 + 40.0 * adaptability + np.random.randn(n_points) * 1.5
        skills = 50.0 + 50.0 * skills + np.random.randn(n_points) * 1.5
        
        # Cap at 100
        diversity = np.clip(diversity, 0, 100)
        adaptability = np.clip(adaptability, 0, 100)
        skills = np.clip(skills, 0, 100)
        
        # Calculate a combined fitness score (example weightings)
        fitness = 0.5 * diversity + 0.3 * adaptability + 0.2 * skills
        
        return {
            "Diversity": diversity,
            "Adaptability": adaptability,
            "Skills": skills,
            "Fitness": fitness
        }
        
    def simulate_colony_growth(self, years: int, initial_pop: int = 5000) -> pd.DataFrame:
        """
        Simulate population growth of Plan B colony.
        Phase 1: Incubation (rapid linear growth as incubators operate).
        Phase 2: Natural reproduction (exponential/logistic).
        """
        t_arr = np.arange(years)
        pop = np.zeros(years)
        diversity_index = np.zeros(years)
        
        # Parameters
        incubator_capacity = 500  # babies per year
        max_incubated = initial_pop
        
        current_pop = 0
        incubated_total = 0
        div = 100.0  # Initial diversity score
        
        for i in range(years):
            if incubated_total < max_incubated:
                new_babies = min(incubator_capacity, max_incubated - incubated_total)
                incubated_total += new_babies
                current_pop += new_babies
            else:
                # Natural growth: Logistic curve with carrying capacity of 1 million
                growth_rate = 0.03  # 3% annual growth
                carrying_capacity = 1000000
                new_babies = int(current_pop * growth_rate * (1 - current_pop/carrying_capacity))
                current_pop += new_babies
                # Genetic drift / founder effect slightly reduces diversity over time
                div -= 0.01 * (current_pop / carrying_capacity)
                
            pop[i] = current_pop
            diversity_index[i] = max(0, div)
            
        return pd.DataFrame({
            "Year": t_arr,
            "Population": pop,
            "Genetic_Diversity_Score": diversity_index
        })


# ══════════════════════════════════════════════════════════════════════════════
# §9B  SIR DISEASE VECTOR SIMULATOR (Blight Spread on Earth)
# ══════════════════════════════════════════════════════════════════════════════
class BlightSIRModel:
    """
    Epidemiological SIR (Susceptible, Infected, Recovered/Dead) model adapted
    for crop blight spread across Earth's agricultural zones.
    
    Categories:
    S: Healthy crops
    I: Infected crops (spreading spores)
    R: Dead crops / barren land
    
    Includes an "adaptation" parameter where the blight mutates to attack
    new crop types (wheat -> okra -> corn).
    """
    
    def __init__(self, beta: float = 0.3, gamma: float = 0.1):
        self.beta = beta    # Infection rate
        self.gamma = gamma  # Crop death rate
        
    def _sir_derivatives(self, t: float, y: np.ndarray, beta: float, gamma: float) -> np.ndarray:
        S, I, R = y
        # N = 1 (normalized to total arable land)
        dSdt = -beta * S * I
        dIdt = beta * S * I - gamma * I
        dRdt = gamma * I
        return np.array([dSdt, dIdt, dRdt])
        
    def simulate_crop_collapse(self, years: float, crop_type: str = "Corn") -> pd.DataFrame:
        """Simulate the collapse of a specific crop type."""
        # Mutation makes beta increase over time (blight gets more aggressive)
        if crop_type == "Wheat":
            beta_eff, gamma_eff = self.beta * 1.5, self.gamma * 1.2
        elif crop_type == "Okra":
            beta_eff, gamma_eff = self.beta * 1.2, self.gamma * 1.0
        else: # Corn (the last crop)
            beta_eff, gamma_eff = self.beta * 0.8, self.gamma * 0.8
            
        t_max = years
        t_eval = np.linspace(0, t_max, 500)
        # Initial state: 99% healthy, 1% infected
        y0 = np.array([0.99, 0.01, 0.0])
        
        sol = sci_int.solve_ivp(
            self._sir_derivatives, (0, t_max), y0,
            args=(beta_eff, gamma_eff), method='RK45', t_eval=t_eval
        )
        
        # Calculate atmospheric oxygen depletion proxy
        # Assuming crops produce O2, dead land consumes O2 via decay
        baseline_o2 = 21.0
        # O2 drops as healthy crops (S) approach 0, but it's a slow global process
        # We model a localized severe drop for dramatic effect
        o2_levels = baseline_o2 - 5.0 * sol.y[2] 
        
        return pd.DataFrame({
            "Year": t_eval,
            "Healthy_pct": sol.y[0] * 100.0,
            "Infected_pct": sol.y[1] * 100.0,
            "Barren_pct": sol.y[2] * 100.0,
            "Local_O2_pct": o2_levels
        })


# ══════════════════════════════════════════════════════════════════════════════
# §9C  SHANNON ENTROPY SIGNAL ANALYZER (Lazarus Telemetry Compression)
# ══════════════════════════════════════════════════════════════════════════════
class LazarusSignalAnalyzer:
    """
    Analyzes the binary telemetry data sent by Lazarus probes through the wormhole.
    Computes Shannon Entropy to determine data compressibility and information density.
    
    High entropy implies complex, uncompressible data (e.g., quantum gravity readings).
    Low entropy implies repetitive/empty data (e.g., continuous "all clear" pings).
    """
    
    def __init__(self):
        pass
        
    def generate_synthetic_telemetry(self, length: int, signal_type: str = "random") -> np.ndarray:
        """Generates synthetic binary telemetry data."""
        if signal_type == "periodic":
            # Simple alternating pattern (e.g., a beacon)
            pattern = np.array([1, 0, 1, 0, 0, 0, 0, 0])
            return np.tile(pattern, length // len(pattern) + 1)[:length]
        elif signal_type == "sparse":
            # Mostly zeros with rare 1s (e.g., anomaly detection)
            return np.random.choice([0, 1], size=length, p=[0.95, 0.05])
        else: # "random" or "quantum"
            # High entropy data (e.g., complex environmental scan)
            return np.random.randint(0, 2, size=length)
            
    def compute_shannon_entropy(self, data: np.ndarray, word_size: int = 8) -> float:
        """
        Computes the Shannon Entropy of the data stream.
        Groups data into 'words' of given size and calculates probability distribution.
        """
        if len(data) < word_size:
            return 0.0
            
        # Group into words (e.g., bytes if word_size=8)
        num_words = len(data) // word_size
        words = data[:num_words * word_size].reshape((num_words, word_size))
        
        # Convert binary array words to integers for counting
        # e.g. [1,0,1] -> 5
        powers = 2 ** np.arange(word_size - 1, -1, -1)
        word_ints = np.dot(words, powers)
        
        # Calculate probabilities
        _, counts = np.unique(word_ints, return_counts=True)
        probabilities = counts / num_words
        
        # Shannon Entropy: H = - sum(p * log2(p))
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy
        
    def analyze_transmission(self) -> Dict[str, Any]:
        """Runs analysis on various signal types representing different Lazarus probe states."""
        length = 10000
        types = ["periodic", "sparse", "random"]
        results = {}
        
        for t in types:
            data = self.generate_synthetic_telemetry(length, signal_type=t)
            # Max entropy for 8-bit word is 8.0
            entropy = self.compute_shannon_entropy(data, word_size=8)
            compression_ratio = 8.0 / max(entropy, 0.01) # Theoretical max compression
            
            results[t] = {
                "entropy_bits_per_byte": round(entropy, 3),
                "compressibility": round(compression_ratio, 2),
                "information_density_pct": round((entropy / 8.0) * 100.0, 1)
            }
            
        return results


# ══════════════════════════════════════════════════════════════════════════════
# §10  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    D: Dict[str, Any] = {
        "reporter":           MissionReporter(),
        "plan_a_tars":        30,
        "plan_a_murph":       0,
        "plan_a_ships":       0,
        "plan_b_landing":     None,
        "blight_year":        2070.0,
        "drive_content":      "Mission telemetry",
        "drive_size_mb":      100.0,
        "drive_is_crystal":   False,
        "drive_coeffs":       0,
        "nasa_report":        None,
        "unlock_name":        ACHIEVEMENT_CATALOGUE[0]["name"],
        "pop_projection":     None,
        "crop_timeline":      None,
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# §11  MATPLOTLIB STYLE
# ══════════════════════════════════════════════════════════════════════════════
MPL_STYLE = {
    "figure.facecolor":  "#05080d",
    "axes.facecolor":    "#070a14",
    "axes.edgecolor":    "#111830",
    "axes.labelcolor":   "#E8C46A",
    "axes.grid":         True,
    "grid.color":        "#0c1020",
    "grid.linestyle":    ":",
    "grid.alpha":        0.5,
    "xtick.color":       "#2a3a60",
    "ytick.color":       "#2a3a60",
    "xtick.labelsize":   6,
    "ytick.labelsize":   6,
    "axes.labelsize":    7,
    "axes.titlesize":    8,
    "axes.titlecolor":   "#E8C46A",
    "text.color":        "#E8C46A",
    "font.family":       "monospace",
    "legend.facecolor":  "#070a14",
    "legend.edgecolor":  "#111830",
    "legend.fontsize":   6,
    "figure.dpi":        110,
    "savefig.facecolor": "#05080d",
    "axes.spines.top":   False,
    "axes.spines.right": False,
}
def _mpl(): plt.rcParams.update(MPL_STYLE)

PROBE_STATUS_COLORS = {
    ProbeStatus.ACTIVE:        "#81C784",
    ProbeStatus.SILENT:        "#555555",
    ProbeStatus.CONFIRMED_OK:  "#E8C46A",
    ProbeStatus.CONFIRMED_BAD: "#D154FF",
    ProbeStatus.FALSIFIED:     "#CE93D8",
    ProbeStatus.DESTROYED:     "#FF8800",
    ProbeStatus.UNKNOWN:       "#4FC3F7",
}


# ══════════════════════════════════════════════════════════════════════════════
# §12  PLOTTING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def _plot_lazarus_overview(probes: List[LazarusProbe]) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.patch.set_facecolor("#05080d")

    # 1. Habitability scatter: reported vs actual
    ax1 = axes[0]
    for p in probes:
        clr = PROBE_STATUS_COLORS.get(p.status, "#888")
        ax1.scatter(p.habitability_score, p.actual_score,
                    color=clr, s=120, zorder=5,
                    edgecolors="#E8C46A", lw=0.5)
        ax1.annotate(p.agent_name.split("(")[-1].rstrip(")"),
                     (p.habitability_score, p.actual_score),
                     fontsize=5, color=clr,
                     xytext=(5, 3), textcoords="offset points")
    ax1.plot([0,1],[0,1], color="#3a4a70", lw=0.7, ls="--",
             label="Reported = Actual")
    ax1.scatter([], [], color="#CE93D8", s=60, label="FALSIFIED")
    ax1.scatter([], [], color="#81C784", s=60, label="CONFIRMED OK")
    ax1.scatter([], [], color="#E8C46A", s=60, label="HABITABLE")
    ax1.set_xlabel("Reported habitability"); ax1.set_ylabel("Actual habitability")
    ax1.set_title("LAZARUS PROBE — REPORTED vs ACTUAL\n(divergence = deception)")
    ax1.legend(fontsize=5.5); ax1.set_facecolor("#060a14")

    # 2. Signal quality bar
    ax2 = axes[1]
    names  = [p.agent_name.split("(")[-1].rstrip(")").strip() for p in probes]
    snrs   = [p.signal_snr_db for p in probes]
    data_c = [p.data_completeness for p in probes]
    clrs2  = [PROBE_STATUS_COLORS.get(p.status,"#888") for p in probes]
    x_pos  = np.arange(len(probes))
    bars2  = ax2.bar(x_pos, snrs, color=clrs2, alpha=0.85, width=0.6)
    ax2.axhline(0, color="#D154FF", lw=0.7, ls="--", label="Signal lost threshold")
    ax2.axhline(15, color="#81C784", lw=0.6, ls=":", label="Good SNR (15dB)")
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(names, rotation=45, ha="right", fontsize=5.5)
    ax2.set_ylabel("Signal SNR [dB]"); ax2.set_title("PROBE SIGNAL QUALITY")
    ax2.legend(fontsize=5.5)

    # 3. Data completeness pie
    ax3 = axes[2]
    statuses = {}
    for p in probes:
        key = p.status.name
        statuses[key] = statuses.get(key, 0) + 1
    clrs3  = [PROBE_STATUS_COLORS.get(ProbeStatus[k], "#888") for k in statuses]
    wedges, texts, autos = ax3.pie(
        list(statuses.values()), labels=list(statuses.keys()),
        colors=clrs3, autopct="%d", startangle=90,
        textprops={"fontsize":6,"color":"#E8C46A"})
    for at in autos: at.set_fontsize(5.5)
    ax3.set_title("PROBE STATUS DISTRIBUTION\n(12 Lazarus missions)")

    plt.tight_layout()
    return fig


def _plot_plan_ab(plan_a: PlanAStatus, plan_b: PlanBStatus) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.patch.set_facecolor("#05080d")

    # 1. Plan A progress gauge
    ax1 = axes[0,0]
    frac = plan_a.fraction_complete
    theta= np.linspace(0, 2*math.pi*frac, 300)
    clr_a= "#81C784" if frac>=1 else "#E8C46A" if frac>0.5 else "#D154FF"
    ax1.plot(np.cos(theta), np.sin(theta), color=clr_a, lw=10, solid_capstyle="round")
    ax1.add_patch(Circle((0,0), 0.75, color="#060a14", zorder=3))
    ax1.text(0, 0.12, f"{frac*100:.1f}%", ha="center", fontsize=22,
             color=clr_a, fontfamily="monospace", fontweight="bold")
    ax1.text(0, -0.18, "PLAN A", ha="center", fontsize=10,
             color="#E8C46A", fontfamily="monospace")
    ax1.text(0, -0.38, f"{plan_a.coefficients_known}/{plan_a.coefficients_total} coefficients",
             ha="center", fontsize=7, color="#888", fontfamily="monospace")
    ax1.text(0, -0.55, f"SOLVED: {'YES ✓' if plan_a.solved else 'NOT YET'}",
             ha="center", fontsize=7,
             color="#81C784" if plan_a.solved else "#D154FF",
             fontfamily="monospace")
    ax1.set_xlim(-1.2,1.2); ax1.set_ylim(-1.2,1.2)
    ax1.set_aspect("equal"); ax1.axis("off")
    ax1.set_title("MURPHY'S EQUATION PROGRESS")

    # 2. Coefficient attribution
    ax2 = axes[0,1]
    labels2 = ["Brand (40yr)","TARS Crystal","Murph Earth-side","Unknown"]
    values2 = [plan_a.brand_contribution, plan_a.tars_contribution,
                plan_a.murph_contribution,
                max(0, plan_a.coefficients_total - plan_a.coefficients_known)]
    colors2 = ["#E8C46A","#c040ff","#81C784","#3a4a70"]
    wedges2, texts2, autos2 = ax2.pie(
        values2, labels=labels2, colors=colors2, autopct="%d",
        startangle=90, textprops={"fontsize":6,"color":"#E8C46A"})
    for at in autos2: at.set_fontsize(6)
    ax2.set_title("EQUATION COEFFICIENTS — ATTRIBUTION")

    # 3. Colony ship readiness
    ax3 = axes[0,2]
    ships_r = plan_a.colony_ships_ready
    ships_t = plan_a.colony_ships_total
    for i in range(ships_t):
        clr3 = "#81C784" if i < ships_r else "#1a2540"
        ec3  = "#E8C46A" if i < ships_r else "#3a4a70"
        ax3.add_patch(FancyBboxPatch((i%5*1.1+0.05, (i//5)*1.4+0.05),
                                      0.9, 1.2, boxstyle="round,pad=0.08",
                                      fc=clr3, ec=ec3, lw=1.0))
        ax3.text(i%5*1.1+0.5, (i//5)*1.4+0.65, f"S{i+1}",
                 ha="center", va="center", fontsize=7,
                 color="#E8C46A" if i<ships_r else "#555",
                 fontfamily="monospace")
    ax3.set_xlim(-0.1, 5.6); ax3.set_ylim(-0.1, 2.8)
    ax3.set_aspect("equal"); ax3.axis("off")
    ax3.set_title(f"COLONY SHIPS  {ships_r}/{ships_t} READY\n"
                  f"Capacity: {plan_a.colony_capacity():,} people")

    # 4. Plan B embryo fitness distribution
    ax4 = axes[1,0]
    fit_arr = plan_b.embryo_bank.fitness_distribution()
    ax4.hist(fit_arr, bins=40, color="#CE93D8", alpha=0.80, edgecolor="#0a0a20")
    ax4.axvline(fit_arr.mean(), color="#E8C46A", lw=1.0, ls="--",
                label=f"Mean={fit_arr.mean():.3f}")
    ax4.axvline(0.60, color="#D154FF", lw=0.7, ls=":", label="Min threshold")
    ax4.set_xlabel("Fitness score"); ax4.set_ylabel("Count")
    ax4.set_title(f"EMBRYO FITNESS — {plan_b.embryo_bank.n:,} embryos\n"
                  f"Diversity={plan_b.embryo_bank.diversity_idx:.4f}")
    ax4.legend(fontsize=6)

    # 5. Population projection (gen 1, 2)
    ax5 = axes[1,1]
    gens  = ["Embryos","Viable","Gen 1","Gen 2","MVP threshold"]
    vals5 = [plan_b.embryo_bank.n, plan_b.viable_embryos(),
             plan_b.gen1_population(), plan_b.gen2_population(),
             plan_b.mvp_threshold]
    cols5 = ["#4FC3F7","#81C784","#E8C46A","#FF8800","#D154FF"]
    bars5 = ax5.bar(gens, vals5, color=cols5, alpha=0.85)
    ax5.bar_label(bars5, fmt="%d", padding=3, fontsize=7, color="#fff")
    ax5.axhline(plan_b.mvp_threshold, color="#D154FF", lw=0.8, ls="--",
                label=f"MVP={plan_b.mvp_threshold}")
    ax5.set_ylabel("People"); ax5.set_title("PLAN B — POPULATION PROJECTIONS")
    ax5.legend(fontsize=6)

    # 6. Bottleneck / inbreeding risk
    ax6 = axes[1,2]
    n_arr     = np.logspace(1, 4, 200)
    div_arr   = np.linspace(0.3, 1.0, 200)
    N_eff_arr = n_arr * plan_b.embryo_bank.diversity_idx
    F_arr     = 1.0/(2*N_eff_arr) * 10  # after 10 generations
    ax6.semilogx(n_arr, np.clip(F_arr, 0, 1), color="#D154FF", lw=1.2,
                 label="Inbreeding F (10 gen)")
    ax6.axvline(plan_b.gen1_population(), color="#E8C46A", lw=0.9, ls="--",
                label=f"Gen1 N={plan_b.gen1_population()}")
    ax6.axhline(0.05, color="#81C784", lw=0.7, ls=":", label="F=0.05 acceptable")
    ax6.set_xlabel("Founding population N")
    ax6.set_ylabel("Inbreeding coefficient F")
    ax6.set_title("GENETIC BOTTLENECK RISK\n(Founder's Effect model)")
    ax6.legend(fontsize=6)

    plt.tight_layout()
    return fig


def _plot_blight(blight: BlightSpreadModel) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 2, figsize=(15, 9))
    fig.patch.set_facecolor("#05080d")

    # 1. Crop timeline
    ax1 = axes[0,0]
    yr_arr = np.linspace(2048, 2100, 300)
    crop_colors = {"Wheat":"#E8C46A","Corn":"#FF8800","Rice":"#81C784",
                   "Soy":"#4FC3F7","Okra":"#CE93D8","Potato":"#D154FF","Cassava":"#FFB74D"}
    for crop, clr in crop_colors.items():
        frac_arr = [blight.blight_fraction(crop, y) for y in yr_arr]
        ax1.plot(yr_arr, frac_arr, color=clr, lw=1.1, label=crop)
    ax1.axvline(MISSION_START_YR, color="#E8C46A", lw=0.9, ls="--",
                label=f"Mission start {MISSION_START_YR}")
    ax1.set_xlabel("Year"); ax1.set_ylabel("Fraction destroyed")
    ax1.set_title("CROP BLIGHT PROGRESSION\n(Global agricultural collapse)")
    ax1.legend(fontsize=5.5, ncol=2)

    # 2. Food production index
    ax2 = axes[0,1]
    fpi_arr = [blight.food_production_index(y) for y in yr_arr]
    cal_arr = [blight.calories_per_person_per_day(y) for y in yr_arr]
    ax2.plot(yr_arr, fpi_arr, color="#E8C46A", lw=1.3, label="Food production index")
    ax2b = ax2.twinx()
    ax2b.plot(yr_arr, cal_arr, color="#4FC3F7", lw=1.0, ls="--",
              label="Cal/person/day")
    ax2.axhline(0.5, color="#D154FF", lw=0.7, ls=":", label="Critical 50%")
    ax2.axvline(MISSION_START_YR, color="#E8C46A", lw=0.8, ls="--")
    ax2.set_xlabel("Year"); ax2.set_ylabel("FPI [0–1]", color="#E8C46A")
    ax2b.set_ylabel("Calories/person/day", color="#4FC3F7")
    ax2.set_title("FOOD PRODUCTION & CALORIE AVAILABILITY")
    lines  = [ax2.lines[0], ax2b.lines[0]]
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, fontsize=6)

    # 3. Population projection
    ax3 = axes[1,0]
    pop_df = blight.population_projection(2060, 2120)
    ax3.fill_between(pop_df["year"], pop_df["population"]/1e9, 0,
                     alpha=0.25, color="#D154FF")
    ax3.plot(pop_df["year"], pop_df["population"]/1e9,
             color="#D154FF", lw=1.3, label="Carrying capacity")
    ax3.axhline(EARTH_POP_2067/1e9, color="#555", lw=0.6, ls=":",
                label=f"2067 pop: {EARTH_POP_2067/1e9:.1f}B")
    ext_yr = blight.extinction_year()
    if ext_yr < 2120:
        ax3.axvline(ext_yr, color="#CE93D8", lw=1.0, ls="--",
                    label=f"Extinction ~{ext_yr:.0f}")
    ax3.axvline(MISSION_START_YR, color="#E8C46A", lw=0.9, ls="--",
                label="Mission start")
    ax3.set_xlabel("Year"); ax3.set_ylabel("Population [billions]")
    ax3.set_title(f"POPULATION PROJECTION\nExtinction estimate: {ext_yr:.0f}")
    ax3.legend(fontsize=6)

    # 4. Urgency score and mission deadline
    ax4 = axes[1,1]
    urg_arr = pop_df["mission_urgency"].values
    yr_plot = pop_df["year"].values
    ax4.fill_between(yr_plot, urg_arr, 0, alpha=0.25,
                     color="#FF8800")
    ax4.plot(yr_plot, urg_arr, color="#FF8800", lw=1.3)
    ax4.axhline(0.90, color="#D154FF", lw=0.7, ls="--",
                label="90% urgency — critical deadline")
    ax4.axhline(0.50, color="#FFB74D", lw=0.6, ls=":", label="50% urgency")
    ax4.axvline(MISSION_START_YR, color="#E8C46A", lw=0.9, ls="--",
                label="Mission start")
    ax4.set_xlabel("Year"); ax4.set_ylabel("Mission urgency [0–1]")
    ax4.set_title("COLONY MISSION URGENCY SCORE\n(1 = existential deadline)")
    ax4.legend(fontsize=6)

    plt.tight_layout()
    return fig


def _plot_achievements(scorer: MissionScorer) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.patch.set_facecolor("#05080d")

    # 1. Points by tier
    ax1 = axes[0]
    tier_sums = {}
    tier_colors = {
        AchievementTier.BRONZE.value:  "#CD7F32",
        AchievementTier.SILVER.value:  "#C0C0C0",
        AchievementTier.GOLD.value:    "#FFD700",
        AchievementTier.PLATINUM.value:"#E5E4E2",
        AchievementTier.LEGEND.value:  "#E8C46A",
    }
    for a in scorer.achievements:
        if a.unlocked:
            tier_sums[a.tier.value] = tier_sums.get(a.tier.value,0) + a.points
    if tier_sums:
        bars1 = ax1.bar(list(tier_sums.keys()), list(tier_sums.values()),
                         color=[tier_colors.get(k,"#888") for k in tier_sums],
                         alpha=0.85)
        ax1.bar_label(bars1, fmt="%d pts", padding=3, fontsize=7, color="#fff")
    ax1.set_ylabel("Points earned"); ax1.set_title("ACHIEVEMENTS BY TIER")
    ax1.tick_params(axis="x", rotation=20, labelsize=7)

    # 2. Achievement unlock timeline
    ax2 = axes[1]
    unlocked = [a for a in scorer.achievements if a.unlocked]
    locked   = [a for a in scorer.achievements if not a.unlocked]
    ax2.barh([a.name for a in unlocked], [a.points for a in unlocked],
              color="#81C784", alpha=0.85, label="Unlocked")
    ax2.barh([a.name for a in locked], [a.points for a in locked],
              color="#1a2540", alpha=0.85, label="Locked")
    ax2.set_xlabel("Points"); ax2.set_title("ACHIEVEMENT STATUS")
    ax2.legend(fontsize=6); ax2.tick_params(axis="y", labelsize=6)

    # 3. Success probability gauge
    ax3 = axes[2]
    n_unlocked = sum(1 for a in scorer.achievements if a.unlocked)
    prob_arr   = np.array([scorer.risk_adjusted_probability(i)
                            for i in range(len(scorer.achievements)+1)])
    ax3.plot(range(len(prob_arr)), prob_arr*100, color="#E8C46A", lw=1.5)
    ax3.fill_between(range(len(prob_arr)), prob_arr*100, 0,
                     alpha=0.15, color="#E8C46A")
    ax3.axvline(n_unlocked, color="#81C784", lw=1.0, ls="--",
                label=f"Current: {scorer.risk_adjusted_probability(n_unlocked)*100:.0f}%")
    ax3.axhline(50, color="#FFB74D", lw=0.6, ls=":", label="50% probability")
    ax3.axhline(90, color="#81C784", lw=0.6, ls=":", label="90% probability")
    ax3.set_xlabel("Achievements unlocked")
    ax3.set_ylabel("Mission success probability [%]")
    ax3.set_title(f"MISSION SUCCESS PROBABILITY\nTotal: {scorer.total_points()} pts "
                  f"({scorer.success_score()*100:.1f}% of max)")
    ax3.legend(fontsize=6)

    plt.tight_layout()
    return fig


def _plot_data_drives(mgr: DataDriveManager) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#05080d")
    rep = mgr.integrity_report()

    # 1. Size breakdown
    ax1 = axes[0]
    names1 = [d.drive_id for d in mgr.drives]
    sizes  = [d.size_bits/1e9 for d in mgr.drives]
    clrs1  = ["#c040ff" if d.is_tars_crystal else
               "#81C784" if d.verified else "#D154FF"
               for d in mgr.drives]
    bars1  = ax1.barh(names1, sizes, color=clrs1, alpha=0.85)
    ax1.bar_label(bars1, fmt="%.2f Gb", padding=3, fontsize=6, color="#fff")
    ax1.set_xlabel("Data size [Gigabits]")
    ax1.set_title(f"DATA DRIVE SIZES\nTotal: {rep['total_GB']:.2f} GB")

    # 2. Integrity status
    ax2 = axes[1]
    statuses  = {DataDriveStatus.VERIFIED.value:    0,
                 DataDriveStatus.CORRUPTED.value:   0,
                 DataDriveStatus.TRANSMITTED.value: 0,
                 DataDriveStatus.PENDING.value:      0}
    for d in mgr.drives:
        statuses[d.status.value] = statuses.get(d.status.value,0)+1
    st_c = {DataDriveStatus.VERIFIED.value:   "#81C784",
            DataDriveStatus.CORRUPTED.value:  "#D154FF",
            DataDriveStatus.TRANSMITTED.value:"#E8C46A",
            DataDriveStatus.PENDING.value:    "#4FC3F7"}
    keys  = [k for k, v in statuses.items() if v > 0]
    vals  = [statuses[k] for k in keys]
    clrs2 = [st_c.get(k,"#888") for k in keys]
    ax2.pie(vals, labels=keys, colors=clrs2, autopct="%d",
            textprops={"fontsize":6,"color":"#E8C46A"}, startangle=90)
    ax2.set_title(f"DATA INTEGRITY\n{rep['integrity_pct']:.0f}% verified")

    # 3. Murphy coefficients from drives
    ax3 = axes[2]
    ax3.axis("off")
    items = [
        ("TARS Crystal Drives",  str(rep["tars_crystals"])),
        ("Total Murphy Coeffs",  str(rep["total_murphy_coeffs"])),
        ("Total Data",           f"{rep['total_GB']:.3f} GB"),
        ("Total Bits",           f"{rep['total_bits']:.2e}"),
        ("Verified Drives",      f"{rep['verified']}/{rep['total_drives']}"),
        ("Integrity",            f"{rep['integrity_pct']:.0f}%"),
    ]
    y = 0.95
    ax3.text(0.05, y, "DATA DRIVE REPORT", fontsize=9, color="#E8C46A",
             fontfamily="monospace", fontweight="bold",
             transform=ax3.transAxes)
    y -= 0.12
    for lbl, val in items:
        ax3.text(0.05, y, f"  {lbl}:", fontsize=7, color="#888",
                 fontfamily="monospace", transform=ax3.transAxes)
        ax3.text(0.05, y-0.07, f"    {val}", fontsize=8, color="#E8C46A",
                 fontfamily="monospace", fontweight="bold",
                 transform=ax3.transAxes)
        y -= 0.15

    plt.tight_layout()
    return fig


def _plot_mission_timeline(reporter: MissionReporter) -> plt.Figure:
    _mpl()
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor("#05080d")
    tl = reporter.mission_timeline()
    cat_colors = {
        "EARTH":       "#E8C46A",
        "SATURN":      "#CE93D8",
        "GARGANTUA":   "#FF8800",
        "MILLER":      "#4FC3F7",
        "MANN":        "#D154FF",
        "TESSERACT":   "#c040ff",
        "EDMUNDS":     "#81C784",
        "COLONY":      "#FFD700",
        "CRITICAL":    "#D154FF",
        "DISCOVERY":   "#c040ff",
        "BREAKTHROUGH":"#FFD700",
        "MISSION":     "#E8C46A",
        "PLAN_A":      "#81C784",
        "PLAN_B":      "#4FC3F7",
    }
    years = tl["Year"].values
    events= tl["Event"].values
    cats  = tl["Category"].values
    y_pos = np.linspace(0, 1, len(events))

    ax.axhline(0.5, color="#1a2040", lw=40, alpha=0.3, solid_capstyle="butt")
    for y, yr, evt, cat in zip(y_pos, years, events, cats):
        clr = cat_colors.get(cat, "#888")
        ax.scatter([yr], [y], color=clr, s=80, zorder=5,
                   edgecolors="#E8C46A", lw=0.5)
        ax.plot([yr, yr], [y, 0.5], color=clr, lw=0.5, alpha=0.4)
        ha = "right" if yr < np.median(years) else "left"
        ax.text(yr + (5 if ha=="left" else -5), y,
                f"{yr}: {evt[:45]}", ha=ha, va="center",
                fontsize=5.5, color=clr, fontfamily="monospace")

    ax.axvline(MISSION_START_YR, color="#E8C46A", lw=1.5, ls="--", alpha=0.7)
    ax.text(MISSION_START_YR+1, 0.95, "ENDURANCE LAUNCH", color="#E8C46A",
            fontsize=6.5, fontfamily="monospace")
    ax.set_xlim(2045, 2165)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("Year (Earth coordinate time)")
    ax.set_yticks([]); ax.set_title("INTERSTELLAR MISSION TIMELINE (Canonical)", fontsize=9)
    ax.set_facecolor("#05080d")
    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# §13  MAIN STREAMLIT PAGE
# ══════════════════════════════════════════════════════════════════════════════
def mission_reporter_page():
    init_session_state()
    _mpl()
    S = st.session_state
    R: MissionReporter = S["reporter"]

    st.markdown("""
    <div style="border-left:3px solid #FFD700;padding:.55rem 1.2rem;
                margin-bottom:1.2rem;background:rgba(255,215,0,0.03);
                font-family:monospace;">
    <div style="color:#FFD700;font-size:.95rem;letter-spacing:.12em;font-weight:600;">
    ◈ MISSION REPORTER &amp; NASA DATA ARCHIVE</div>
    <div style="color:#5a6a90;font-size:.62rem;margin-top:.2rem;">
    Lazarus Archive · Plan A / Plan B · Blight Model · Achievements ·
    Data Drives · NASA Reports · Mission Timeline
    </div></div>""", unsafe_allow_html=True)

    (tab_lazarus, tab_plan_ab, tab_blight,
     tab_achieve, tab_drives,
     tab_nasa, tab_timeline) = st.tabs([
        "🛸 LAZARUS ARCHIVE",
        "◎ PLAN A / PLAN B",
        "🌾 BLIGHT MODEL",
        "🏆 ACHIEVEMENTS",
        "💾 DATA DRIVES",
        "📋 NASA REPORT",
        "📅 MISSION TIMELINE",
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1 — LAZARUS ARCHIVE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_lazarus:
        fig_laz = _plot_lazarus_overview(R.lazarus)
        st.pyplot(fig_laz, width='stretch'); plt.close(fig_laz)
        st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#FFD700;margin-top:.5rem;">◈ FULL LAZARUS PROBE MANIFEST</div>',
                    unsafe_allow_html=True)
        df_laz = R.lazarus_df()
        st.dataframe(df_laz, width='stretch', hide_index=True)
        best = R.best_candidates(3)
        st.markdown(f"""
        <div style="font-family:monospace;font-size:.60rem;color:#c0c0e0;
                    background:rgba(7,10,20,.92);padding:.6rem;
                    border:1px solid rgba(255,215,0,.15);border-radius:3px;margin-top:.5rem;">
        <b style="color:#FFD700;">── TOP 3 CANDIDATE PLANETS ──</b><br>
        {'<br>'.join([f'  {i+1}. <b style="color:#E8C46A;">{p.planet_name}</b> — '
                      f'ESI {p.actual_score:.3f} — {p.status.value}'
                      for i, p in enumerate(best)])}
        </div>""", unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — PLAN A / PLAN B
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_plan_ab:
        c1, c2 = st.columns([1, 3])
        with c1:
            tars_c = st.slider("TARS coefficients", 0, 42, int(S["plan_a_tars"]), 1)
            murph_c= st.slider("Murph coefficients", 0, 42, int(S["plan_a_murph"]), 1)
            ships_r= st.slider("Colony ships ready", 0, 10, int(S["plan_a_ships"]), 1)
            S["plan_a_tars"] = tars_c; S["plan_a_murph"] = murph_c
            S["plan_a_ships"] = ships_r
            R.plan_a.tars_contribution  = tars_c
            R.plan_a.murph_contribution = murph_c
            R.plan_a.colony_ships_ready = ships_r
            R.plan_a.__post_init__()
            su_a = R.plan_a.summary(); su_b = R.plan_b.summary()
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c0e0;
                        background:rgba(7,10,20,.92);padding:.65rem;
                        border:1px solid rgba(255,215,0,.18);border-radius:3px;
                        line-height:2.0;">
            <b style="color:#FFD700;">PLAN A</b><br>
            Eq: <b style="color:#E8C46A;">{su_a['equation_pct']:.1f}%</b>
            ({su_a['coefficients_known']}/42)<br>
            SOLVED: <b style="color:{'#81C784' if su_a['solved'] else '#D154FF'};">
            {'YES ✓' if su_a['solved'] else 'NO'}</b><br>
            Ships: <b>{su_a['colony_ships_ready']}/{R.plan_a.colony_ships_total}</b><br>
            Capacity: <b>{su_a['total_capacity']:,}</b><br>
            <br>
            <b style="color:#4FC3F7;">PLAN B</b><br>
            Embryos: <b>{su_b['embryo_count']:,}</b><br>
            Viable: <b>{su_b['viable_embryos']:,}</b><br>
            Gen1: <b style="color:#81C784;">{su_b['gen1_population']:,}</b><br>
            MVP: <b>{'✓ YES' if su_b['exceeds_mvp'] else '✗ NO'}</b><br>
            Bottleneck: <b style="color:#D154FF;">{su_b['bottleneck_risk']:.4f}</b>
            </div>""", unsafe_allow_html=True)
        with c2:
            fig_ab = _plot_plan_ab(R.plan_a, R.plan_b)
            st.pyplot(fig_ab, width='stretch'); plt.close(fig_ab)
        with st.expander("◈ Top 20 Embryos by Fitness"):
            st.dataframe(R.plan_b.embryo_bank.top_embryos(20),
                         width='stretch', hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — BLIGHT MODEL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_blight:
        fig_bl = _plot_blight(R.blight)
        st.pyplot(fig_bl, width='stretch'); plt.close(fig_bl)
        ext_yr = R.blight.extinction_year()
        fpi_now = R.blight.food_production_index(MISSION_START_YR+30)
        st.markdown(f"""
        <div style="font-family:monospace;font-size:.60rem;color:#c0c0e0;
                    background:rgba(7,10,20,.92);padding:.5rem;
                    border:1px solid rgba(255,215,0,.12);border-radius:3px;">
        Estimated extinction year: <b style="color:#D154FF;">{ext_yr:.0f}</b>  ·
        FPI at 2097: <b style="color:#FF8800;">{fpi_now:.3f}</b>  ·
        Calories at 2097: <b>{R.blight.calories_per_person_per_day(MISSION_START_YR+30):.0f}/day</b>  ·
        Mission urgency: <b style="color:#D154FF;">CRITICAL</b>
        </div>""", unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 4 — ACHIEVEMENTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_achieve:
        c1, c2 = st.columns([1, 3])
        with c1:
            unlk = st.selectbox("Unlock achievement",
                                 [a["name"] for a in ACHIEVEMENT_CATALOGUE])
            if st.button("🏆 UNLOCK", width='stretch', type="primary"):
                result = R.scorer.unlock(unlk)
                if result:
                    st.success(f"🏆 {result.name} — {result.points} pts!")
                else:
                    st.info("Already unlocked or not found.")
            pts   = R.scorer.total_points()
            maxp  = R.scorer.max_points()
            prob  = R.scorer.risk_adjusted_probability(
                     sum(1 for a in R.scorer.achievements if a.unlocked))
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.60rem;color:#c0c0e0;
                        background:rgba(7,10,20,.92);padding:.65rem;
                        border:1px solid rgba(255,215,0,.15);border-radius:3px;
                        line-height:2.0;">
            Total points: <b style="color:#FFD700;">{pts:,}</b><br>
            Max possible: <b>{maxp:,}</b><br>
            Score: <b>{R.scorer.success_score()*100:.1f}%</b><br>
            Success prob: <b style="color:#81C784;">{prob*100:.0f}%</b>
            </div>""", unsafe_allow_html=True)
        with c2:
            fig_ach = _plot_achievements(R.scorer)
            st.pyplot(fig_ach, width='stretch'); plt.close(fig_ach)
            st.dataframe(R.scorer.achievements_df(),
                         width='stretch', hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 5 — DATA DRIVES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_drives:
        c1, c2 = st.columns([1, 3])
        with c1:
            d_cont  = st.text_input("Content description", value=S["drive_content"])
            d_size  = st.number_input("Size (Mbits)", value=float(S["drive_size_mb"]),
                                       min_value=0.01, format="%.2f")
            d_xtal  = st.checkbox("TARS Crystal", value=bool(S["drive_is_crystal"]))
            d_coeff = st.slider("Murphy coefficients", 0, 42, int(S["drive_coeffs"]), 1)
            S["drive_content"] = d_cont; S["drive_size_mb"] = d_size
            S["drive_is_crystal"] = d_xtal; S["drive_coeffs"] = d_coeff
            if st.button("💾 SUBMIT DRIVE", width='stretch', type="primary"):
                drive = R.drives.submit_drive(
                    d_cont, int(d_size*1e6), is_tars=d_xtal, coeffs=d_coeff)
                st.success(f"Drive {drive.drive_id} submitted — SHA: {drive.sha256_hash[:12]}...")
            rep_d = R.drives.integrity_report()
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c0e0;
                        background:rgba(7,10,20,.92);padding:.6rem;
                        border:1px solid rgba(255,215,0,.12);border-radius:3px;
                        line-height:2.0;">
            Drives: <b>{rep_d['total_drives']}</b><br>
            Verified: <b style="color:#81C784;">{rep_d['verified']}</b><br>
            Corrupted: <b style="color:#D154FF;">{rep_d['corrupted']}</b><br>
            Total data: <b>{rep_d['total_GB']:.3f} GB</b><br>
            Murphy coeffs: <b>{rep_d['total_murphy_coeffs']}</b>
            </div>""", unsafe_allow_html=True)
        with c2:
            fig_dd = _plot_data_drives(R.drives)
            st.pyplot(fig_dd, width='stretch'); plt.close(fig_dd)
            st.dataframe(R.drives.drives_df(),
                         width='stretch', hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 6 — NASA REPORT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_nasa:
        if st.button("📋 GENERATE NASA FINAL REPORT",
                     width='stretch', type="primary"):
            S["nasa_report"] = R.generate_nasa_report()
        if S.get("nasa_report"):
            rpt = S["nasa_report"]
            kpis = [
                ("Plan A %",    f"{rpt['plan_a']['equation_pct']:.1f}%",     "#FFD700"),
                ("Plan B MVP",  "YES" if rpt['plan_b']['exceeds_mvp'] else "NO","#4FC3F7"),
                ("Best Planet", rpt["best_planet"][:12],                      "#81C784"),
                ("Extinction",  f"~{rpt['blight_extinction_year']:.0f}",     "#D154FF"),
                ("Score",       str(rpt["total_score"]),                       "#E8C46A"),
                ("Success %",   f"{rpt['success_prob']*100:.0f}%",            "#81C784"),
            ]
            cols = st.columns(len(kpis))
            for col, (lbl,val,clr) in zip(cols, kpis):
                col.markdown(
                    f'<div style="background:rgba(7,10,20,.9);border:1px solid {clr}44;'
                    f'padding:.4rem;text-align:center;border-radius:2px;font-family:monospace;">'
                    f'<div style="color:#444;font-size:.48rem;">{lbl}</div>'
                    f'<div style="color:{clr};font-size:.82rem;">{val}</div></div>',
                    unsafe_allow_html=True)
            st.json(rpt)
        else:
            st.info("Click button to generate the final NASA mission report.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 7 — MISSION TIMELINE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_timeline:
        fig_tl = _plot_mission_timeline(R)
        st.pyplot(fig_tl, width='stretch'); plt.close(fig_tl)
        tl_df  = R.mission_timeline()
        cat_colors_html = {
            "CRITICAL":    "#D154FF", "DISCOVERY": "#c040ff",
            "BREAKTHROUGH":"#FFD700", "MISSION":   "#E8C46A",
            "PLAN_A":      "#81C784", "PLAN_B":    "#4FC3F7",
            "EARTH":       "#E8C46A", "GARGANTUA": "#FF8800",
        }
        for _, row in tl_df.iterrows():
            clr = cat_colors_html.get(row["Category"], "#888")
            st.markdown(
                f'<div style="font-family:monospace;font-size:.60rem;'
                f'border-left:3px solid {clr};padding:.2rem .6rem;margin:.1rem 0;">'
                f'<span style="color:{clr};">{row["Year"]}</span>'
                f' — <span style="color:#E8C46A;">{row["Event"]}</span>'
                f' <span style="color:#555;">[{row["Location"]}]</span></div>',
                unsafe_allow_html=True)
