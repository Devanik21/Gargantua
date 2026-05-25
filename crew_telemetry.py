"""
crew_telemetry.py — Crew Telemetry, TARS/CASE AI & Endurance Ship Systems
ENDURANCE Mission Control | Interstellar Science Platform v3.0.0
═══════════════════════════════════════════════════════════════════════════════
Scientific References:
  [1]  Kip Thorne, "The Science of Interstellar" (W.W. Norton, 2014)
  [2]  NASA Human Research Program — Space Physiology & Countermeasures
  [3]  Stuster (1996) "Bold Endeavors: Lessons from Polar/Space Exploration"
  [4]  Connors, Harrison & Akins (1985) "Living Aloft: Human Req. for LDS"
  [5]  Law (1960) Ann.Occup.Hyg. 2:65  [Closed life support systems]
  [6]  Eckart (1996) "Spaceflight Life Support & Biospherics" Kluwer
  [7]  Film canon: Interstellar (2014) Dir. Christopher Nolan
  [8]  Thorne canonical tech notes: Endurance specifications, crew manifests

Module implements:
  ┌─ CREW HEALTH MONITORING ────────────────────────────────────────────────┐
  │ Crew profiles: Cooper, Brand, Romilly, Doyle (+ Murph remote)          │
  │ Vital signs: HR, BP, SpO₂, temperature, respiratory rate               │
  │ Psychological status: stress index, isolation score, team cohesion      │
  │ Radiation exposure: cumulative dose tracking (mSv/day)                  │
  │ Caloric balance: intake vs expenditure for mission phases               │
  │ Sleep quality: circadian rhythm modelling in microgravity               │
  │ Bone density loss: 0.5–2% per month in microgravity                    │
  │ Muscle atrophy: 3–5% per month (mitigated by exercise)                 │
  │ G-force tolerance: +Gz / −Gz limits with exposure duration             │
  │ Cryosleep: metabolic rate ↓ 95%, revival protocol timing               │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ TARS AI SYSTEM ────────────────────────────────────────────────────────┐
  │ Adjustable personality parameters: humour, honesty, courage, optimism  │
  │ TARS dialogue engine: context-aware response generation                 │
  │ Data crystal management: quantum data compression & storage             │
  │ Navigation assist: trajectory calculation support                       │
  │ Robot physical form: 4-panel articulation, docking modes                │
  │ Status monitoring: power, actuator health, sensor array                 │
  │ Mission-critical decision log with confidence scores                    │
  │ Humour calibration: 75% default → context-modulated output             │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ CASE AI SYSTEM ────────────────────────────────────────────────────────┐
  │ Brand's personal AI companion: different personality matrix             │
  │ Pilot assist: atmospheric flight modes, docking guidance                │
  │ Structural monitoring: hull stress under gravitational extremes         │
  │ Science data collection: continuous environmental logging               │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ ENDURANCE SPACECRAFT ──────────────────────────────────────────────────┐
  │ 16-module rotating ring: 12 hexagonal crew + 4 rectangular docking     │
  │ Artificial gravity: Ω rotation → centripetal acceleration profile       │
  │ Life support: O₂/CO₂ scrubbing rates, N₂ buffer, water recycling       │
  │ Power systems: RTG + solar panels (fading beyond Mars), fuel cells      │
  │ Propulsion: main engine + RCS thrusters, Δv remaining                  │
  │ Fuel: LH₂/LOX bi-propellant + ion secondary, mass fraction tracking   │
  │ Structural integrity: hull stress (micrometeorite, tidal, thermal)      │
  │ Thermal control: radiators, heaters, thermal mass modelling             │
  │ Navigation: IMU, star tracker, deep space transponder                   │
  │ Communications: high-gain antenna, signal delay vs Earth                │
  │ Emergency: EVA suit inventory, emergency O₂ supply, ejection pods      │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ CRYOSLEEP SYSTEM ──────────────────────────────────────────────────────┐
  │ Pod temperature: −10°C to +15°C ramp protocol                          │
  │ Revival sequence: 4-hour warm-up + medical check + nutrition            │
  │ Metabolic monitoring during hibernation                                 │
  │ Crew rotation: who is awake vs sleeping at each mission phase           │
  │ Emergency revival: rapid 45-minute protocol (cardiac risk assessment)  │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ COMMUNICATIONS ────────────────────────────────────────────────────────┐
  │ Signal lag: light-travel-time delay to Earth / NASA                     │
  │ Message queue: incoming + outgoing with timestamps                      │
  │ Wormhole relay: signal routing through wormhole mouth                   │
  │ Encryption: AES-256 for mission-critical data                           │
  │ Bandwidth: deep space network limitations (bits/s vs distance)          │
  └──────────────────────────────────────────────────────────────────────────┘

"TARS, what's your honesty setting?  90%.  Careful. That's a lot."
                                                  — Cooper, 2067
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import hashlib
import math
import random
import time
import uuid
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import scipy.signal   as sci_sig
import scipy.integrate as sci_int

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot      as plt
import matplotlib.gridspec    as gridspec
import matplotlib.colors      as mcolors
import matplotlib.patches     as mpatches
import matplotlib.ticker      as mticker
from matplotlib.colors        import LinearSegmentedColormap
from matplotlib.patches       import FancyBboxPatch, Circle, FancyArrowPatch, Wedge

import streamlit as st

warnings.filterwarnings("ignore")
random.seed(int(time.time()) % 10000)

# ══════════════════════════════════════════════════════════════════════════════
# §1  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
G_SI          = 6.674_30e-11
C_SI          = 2.997_924_58e8
M_SUN         = 1.989_000e30
AU            = 1.495_978_707e11
LY            = 9.460_730_472e15
YEAR_S        = 3.155_760e7
DAY_S         = 86_400.0
HOUR_S        = 3_600.0
GARG_DIST_LY  = 10.0e9

# Endurance specs (film canon [7,8])
ENDURANCE_MASS_KG   = 5.00e5        # 500 metric tonnes
ENDURANCE_RADIUS_M  = 40.0          # ring radius [m]
ENDURANCE_RPM       = 5.0           # rotation speed [rpm] for ~1g
ENDURANCE_MODULES   = 16            # total modules
ENDURANCE_CREW_MODS = 12            # habitation modules
ENDURANCE_DOCK_MODS = 4             # docking/propulsion modules
ENDURANCE_FUEL_KG   = 3.0e5        # initial propellant [kg]
ENDURANCE_ISP       = 9000.0        # specific impulse [s]
ENDURANCE_O2_KG_PD  = 0.84         # O₂ per crew per day [kg]
ENDURANCE_CO2_KG_PD = 1.00         # CO₂ produced per crew per day [kg]
ENDURANCE_H2O_L_PD  = 2.5          # water per crew per day [L]
ENDURANCE_FOOD_KCAL = 2200.0       # calories per crew per day [kcal]
ENDURANCE_POWER_KW  = 45.0         # total power budget [kW]

# Physiological limits
HR_NORMAL_BPM      = (60,  100)     # heart rate normal range [bpm]
BP_NORMAL          = (90,  140)     # systolic BP normal range [mmHg]
SPO2_CRITICAL      = 90.0           # critical O₂ saturation [%]
RADIATION_LIMIT    = 500.0          # NASA career limit [mSv]
RAD_DAILY_SPACE    = 0.5            # radiation in deep space [mSv/day]
BONE_LOSS_PCT_MO   = 1.0           # bone density loss in microgravity [%/month]
MUSCLE_LOSS_PCT_MO = 3.5           # muscle mass loss [%/month]

# TARS defaults
TARS_DEFAULT_HUMOUR    = 0.75
TARS_DEFAULT_HONESTY   = 0.90
TARS_DEFAULT_COURAGE   = 0.85
TARS_DEFAULT_OPTIMISM  = 0.65
TARS_DEFAULT_OPACITY   = 0.95

# Communication
EARTH_SATURN_LT_S  = SAT_LT = 9.537 * AU / C_SI  # ~79 min Saturn light-travel

# ══════════════════════════════════════════════════════════════════════════════
# §2  CUSTOM COLORMAPS
# ══════════════════════════════════════════════════════════════════════════════
CMAP_HEALTH = LinearSegmentedColormap.from_list("health",
    ["#4a0000","#880000","#cc2200","#ff6600","#ffaa00",
     "#ddcc00","#88cc00","#44bb00","#00aa44","#00cc88"], N=256)

CMAP_STRESS = LinearSegmentedColormap.from_list("stress",
    ["#002244","#004488","#0066cc","#44aaff","#aaddff",
     "#ffeeaa","#ffaa44","#ff6600","#cc2200","#880000"], N=256)

CMAP_SYSTEMS = LinearSegmentedColormap.from_list("systems",
    ["#000000","#080820","#102050","#205080","#3080c0",
     "#50c0e0","#80e0f0","#c0f0ff","#ffffff"], N=256)

# ══════════════════════════════════════════════════════════════════════════════
# §3  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════
class CrewID(Enum):
    COOPER  = "Joseph A. Cooper"
    BRAND   = "Dr. Amelia Brand"
    ROMILLY = "Dr. Doyle Romilly"
    DOYLE   = "Dr. Doyle"
    MURPH   = "Murphy Cooper (Earth)"
    MANN    = "Dr. Mann (Lazarus)"
    TARS    = "TARS (AI Robot)"
    CASE    = "CASE (AI Robot)"

class CrewStatus(Enum):
    ACTIVE       = "Active / Awake"
    CRYOSLEEP    = "Cryosleep (hibernation)"
    EVA          = "EVA (Extra-Vehicular)"
    MEDICAL      = "Medical monitoring"
    DECEASED     = "Deceased"
    DISCONNECTED = "Disconnected / Remote"

class SystemStatus(Enum):
    NOMINAL   = "NOMINAL"
    DEGRADED  = "DEGRADED"
    CRITICAL  = "CRITICAL"
    OFFLINE   = "OFFLINE"
    STANDBY   = "STANDBY"
    EMERGENCY = "EMERGENCY"

class MissionPhase(Enum):
    LAUNCH           = "Earth Launch"
    SATURN_TRANSIT   = "Earth → Saturn Transit"
    WORMHOLE_TRANSIT = "Wormhole Transit"
    MILLER_APPROACH  = "Miller Approach"
    MILLER_SURFACE   = "Miller Surface Operations"
    MILLER_DEPARTURE = "Miller Departure"
    MANN_TRANSIT     = "Mann Planet Transit"
    MANN_SURFACE     = "Mann Surface Operations"
    GARGANTUA_ORBIT  = "Gargantua Orbit"
    TESSERACT        = "Tesseract (Cooper only)"
    EDMUNDS_APPROACH = "Edmunds Planet Approach"
    COLONY_SETUP     = "Colony Establishment"

class RobotMode(Enum):
    STANDBY      = "Standby"
    NAVIGATION   = "Navigation assist"
    SCIENTIFIC   = "Scientific data collection"
    MEDICAL      = "Medical monitoring"
    CONSTRUCTION = "Construction / EVA assist"
    SINGULARITY  = "Singularity data collection"
    DOCKING      = "Docking guidance"

class AlertLevel(Enum):
    GREEN    = "GREEN — All nominal"
    YELLOW   = "YELLOW — Advisory"
    ORANGE   = "ORANGE — Caution"
    RED      = "RED — Warning"
    CRITICAL = "CRITICAL — Emergency"

# ══════════════════════════════════════════════════════════════════════════════
# §4  CREW MEMBER DATACLASS
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class CrewMember:
    crew_id:        CrewID
    age_at_launch:  float           # years at mission start 2067
    mass_kg:        float
    height_m:       float
    role:           str
    specialisation: str
    status:         CrewStatus  = CrewStatus.ACTIVE
    mission_phase:  MissionPhase= MissionPhase.LAUNCH
    # Vitals
    hr_bpm:         float = 72.0
    bp_systolic:    float = 120.0
    bp_diastolic:   float = 80.0
    spo2_pct:       float = 98.5
    temp_C:         float = 37.0
    rr_bpm:         float = 16.0    # respiratory rate
    # Cumulative metrics
    days_in_space:  float = 0.0
    cryo_sessions:  int   = 0
    rad_dose_mSv:   float = 0.0
    bone_loss_pct:  float = 0.0
    muscle_loss_pct:float = 0.0
    kcal_balance:   float = 0.0     # positive = surplus
    sleep_quality:  float = 0.85    # 0-1
    stress_index:   float = 0.20    # 0-1
    # Psychology
    morale:         float = 0.85    # 0-1
    isolation_score:float = 0.15    # 0-1 (higher = more isolated)
    uid:            str   = field(default_factory=lambda: uuid.uuid4().hex[:8].upper())

    def __post_init__(self):
        self.bmi = self.mass_kg / self.height_m**2
        self.lean_mass_kg = self.mass_kg * 0.80    # initial lean mass

    def update_physiology(self, days_elapsed: float,
                           is_cryo: bool = False,
                           exercise_hours_per_day: float = 1.0):
        """Update physiological metrics for elapsed time."""
        months = days_elapsed / 30.44
        if is_cryo:
            # Cryo: minimal degradation, cold exposure
            self.bone_loss_pct   += BONE_LOSS_PCT_MO * months * 0.05
            self.muscle_loss_pct += MUSCLE_LOSS_PCT_MO * months * 0.02
            self.rad_dose_mSv    += RAD_DAILY_SPACE * days_elapsed * 0.3
        else:
            # Active: microgravity losses, mitigated by exercise
            ex_factor = max(0.1, 1.0 - exercise_hours_per_day * 0.4)
            self.bone_loss_pct   += BONE_LOSS_PCT_MO * months * ex_factor
            self.muscle_loss_pct += MUSCLE_LOSS_PCT_MO * months * ex_factor
            self.rad_dose_mSv    += RAD_DAILY_SPACE * days_elapsed
            self.days_in_space   += days_elapsed
            # Stress accumulates
            self.stress_index = min(0.95, self.stress_index + 0.002*days_elapsed/30)
            self.morale       = max(0.10, self.morale - 0.001*days_elapsed/30)

    def vital_signs_noisy(self) -> Dict[str, float]:
        """Return vitals with physiological noise."""
        noise = lambda x, s: x + random.gauss(0, s)
        return {
            "HR (bpm)":     round(noise(self.hr_bpm, 3.0), 1),
            "BP_sys (mmHg)":round(noise(self.bp_systolic, 5.0), 0),
            "BP_dia (mmHg)":round(noise(self.bp_diastolic, 3.0), 0),
            "SpO₂ (%)":     round(min(100, noise(self.spo2_pct, 0.5)), 1),
            "Temp (°C)":    round(noise(self.temp_C, 0.15), 2),
            "RR (bpm)":     round(noise(self.rr_bpm, 1.5), 1),
        }

    def health_score(self) -> float:
        """Composite health score 0–1."""
        hr_ok  = 1.0 - abs(self.hr_bpm - 75)/75
        spo2_ok= (self.spo2_pct - 90)/10 if self.spo2_pct > 90 else 0
        stress_ok = 1.0 - self.stress_index
        bone_ok   = 1.0 - self.bone_loss_pct/20
        return float(np.clip(np.mean([hr_ok, spo2_ok, stress_ok, bone_ok, self.morale]), 0, 1))

    def alert_level(self) -> AlertLevel:
        hs = self.health_score()
        if   hs > 0.80: return AlertLevel.GREEN
        elif hs > 0.65: return AlertLevel.YELLOW
        elif hs > 0.50: return AlertLevel.ORANGE
        elif hs > 0.30: return AlertLevel.RED
        else:           return AlertLevel.CRITICAL

    def to_summary_dict(self) -> Dict[str, Any]:
        v = self.vital_signs_noisy()
        return {
            "Name":          self.crew_id.value.split()[0],
            "Role":          self.role,
            "Status":        self.status.value,
            "Age (launch)":  self.age_at_launch,
            "HR (bpm)":      v["HR (bpm)"],
            "SpO₂ (%)":      v["SpO₂ (%)"],
            "Temp (°C)":     v["Temp (°C)"],
            "Stress":        f"{self.stress_index*100:.0f}%",
            "Morale":        f"{self.morale*100:.0f}%",
            "Rad (mSv)":     round(self.rad_dose_mSv, 1),
            "Bone loss %":   round(self.bone_loss_pct, 2),
            "Health score":  round(self.health_score(), 3),
            "Alert":         self.alert_level().name,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §5  CREW REGISTRY — canonical Interstellar crew
# ══════════════════════════════════════════════════════════════════════════════
def build_crew_registry() -> Dict[CrewID, CrewMember]:
    return {
        CrewID.COOPER: CrewMember(
            crew_id=CrewID.COOPER, age_at_launch=35.0,
            mass_kg=82.0, height_m=1.83,
            role="Pilot / Commander", specialisation="Aerospace Engineering",
            status=CrewStatus.ACTIVE, hr_bpm=68.0, stress_index=0.18, morale=0.88),
        CrewID.BRAND: CrewMember(
            crew_id=CrewID.BRAND, age_at_launch=31.0,
            mass_kg=62.0, height_m=1.70,
            role="Science Officer", specialisation="Astrophysics / Biology",
            status=CrewStatus.ACTIVE, hr_bpm=72.0, stress_index=0.22, morale=0.82),
        CrewID.ROMILLY: CrewMember(
            crew_id=CrewID.ROMILLY, age_at_launch=38.0,
            mass_kg=75.0, height_m=1.78,
            role="Research Physicist", specialisation="Wormhole Physics",
            status=CrewStatus.ACTIVE, hr_bpm=70.0, stress_index=0.25, morale=0.79),
        CrewID.DOYLE: CrewMember(
            crew_id=CrewID.DOYLE, age_at_launch=33.0,
            mass_kg=78.0, height_m=1.80,
            role="Mission Specialist", specialisation="Planetary Science",
            status=CrewStatus.ACTIVE, hr_bpm=74.0, stress_index=0.20, morale=0.85),
    }


# ══════════════════════════════════════════════════════════════════════════════
# §6  TARS AI SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
TARS_DIALOGUE_BANK = {
    "greeting": [
        "Good morning. All systems nominal. Though I notice you haven't asked about my humour setting yet.",
        "Endurance systems online. Cooper, the coffee is... actually I don't drink coffee. That was humour.",
        "Status: operational. Current humour setting: 75%. Should I demonstrate?",
    ],
    "navigation": [
        "Trajectory computed. I've also calculated the probability of everything going wrong. Should I share that?",
        "Plotting course. At current fuel consumption, we have enough for the journey. And a small detour if needed.",
        "Navigation assist active. The wormhole is right where Dr. Brand said it would be. Remarkably.",
    ],
    "tidal": [
        "Tidal forces are... significant. I recommend we don't discuss my structural limitations right now.",
        "Approaching Miller's World. One hour ship-time. Seven years Earth-time. I'll try to make it count.",
        "The wave height calculation is... I had hoped the math was wrong. It wasn't.",
    ],
    "singularity": [
        "Data collection complete. 42 coefficients. Remarkably specific number. I didn't choose it.",
        "Quantum gravity data encoded. Transmitting via Cooper's watch. Unorthodox but effective.",
        "Inside the singularity now. Physics is... negotiable here. Logging everything.",
    ],
    "humour": [
        "My humour setting is currently at {val}%. You could lower it, but then who would lighten the mood when we're falling into a black hole?",
        "Adjusting humour to {val}%. I should mention: at 0% humour, I become statistically indistinguishable from CASE.",
        "Humour: {val}%. For reference, the probability of survival increases when morale is high. I'm helping.",
    ],
    "honesty": [
        "Honesty at {val}%. Full disclosure: I have {val}% told you everything I know. The rest is classified.",
        "At {val}% honesty, I can confirm: the odds are not in our favour. But they never were.",
        "Honesty setting: {val}%. Would you like the optimistic version or the accurate one?",
    ],
    "plan_a": [
        "Plan A requires Murphy's equation solved. Current completion: {val}%. Professor Brand was... less forthcoming than expected.",
        "Plan A status: {val}% complete. The math is elegant. Implementing it is another matter.",
        "42 coefficients needed. We have {val}% of them. Cooper, I believe you know where the rest are.",
    ],
    "default": [
        "Acknowledged. Processing.",
        "That is an interesting perspective. I'll add it to my psychological profile of the crew.",
        "Confirmed. Also: you haven't slept in 18 hours. This is me being honest at 90%.",
    ],
}

CASE_DIALOGUE_BANK = {
    "greeting": [
        "Systems nominal. Dr. Brand, I've pre-computed three approach vectors for Miller's World.",
        "Good morning. I've been monitoring the hull stress. It's within parameters. Barely.",
        "Telemetry updated. I should mention the anomalous gravity reading is consistent with the wormhole.",
    ],
    "navigation": [
        "Docking sequence initiated. The Ranger is locked. Flight path confirmed.",
        "Approach vector computed. I've also noted three alternative trajectories if needed.",
        "Environmental data logged. Dr. Brand, the atmospheric composition is... not what we hoped.",
    ],
    "default": [
        "Confirmed. Logging data.",
        "Acknowledged, Dr. Brand.",
        "Systems nominal. Continuing data collection.",
    ],
}


@dataclass
class AIRobot:
    """
    TARS or CASE AI Robot system.
    Adjustable personality matrix, physical form model, mission log.
    """
    robot_id:    CrewID
    name:        str
    humour:      float = TARS_DEFAULT_HUMOUR
    honesty:     float = TARS_DEFAULT_HONESTY
    courage:     float = TARS_DEFAULT_COURAGE
    optimism:    float = TARS_DEFAULT_OPTIMISM
    opacity:     float = TARS_DEFAULT_OPACITY
    mode:        RobotMode = RobotMode.NAVIGATION
    power_pct:   float = 100.0
    active:      bool  = True
    data_crystal_full:   bool  = False
    data_crystal_bits:   float = 0.0    # bits stored
    panel_angle_deg:     float = 0.0    # articulation angle
    mission_log:         List[str] = field(default_factory=list)
    decision_log:        List[Dict] = field(default_factory=list)
    uid: str = field(default_factory=lambda: uuid.uuid4().hex[:8].upper())

    def generate_dialogue(self, context: str = "default") -> str:
        bank = TARS_DIALOGUE_BANK if self.robot_id == CrewID.TARS else CASE_DIALOGUE_BANK
        lines = bank.get(context, bank["default"])
        line  = random.choice(lines)
        # Fill in parameter values
        line = line.replace("{val}", f"{int(self.humour*100)}")
        line = line.replace("{val}", f"{int(self.honesty*100)}")
        return line

    def set_humour(self, val: float):
        self.humour = float(np.clip(val, 0.0, 1.0))
        self.mission_log.append(f"[{time.strftime('%H:%M:%S')}] Humour set to {self.humour*100:.0f}%")

    def set_honesty(self, val: float):
        self.honesty = float(np.clip(val, 0.0, 1.0))
        self.mission_log.append(f"[{time.strftime('%H:%M:%S')}] Honesty set to {self.honesty*100:.0f}%")

    def record_decision(self, situation: str, action: str,
                         confidence: float, outcome: str = "PENDING"):
        self.decision_log.append({
            "timestamp": time.time(),
            "situation": situation,
            "action":    action,
            "confidence":confidence,
            "outcome":   outcome,
            "honesty_applied": self.honesty,
        })

    def personality_profile(self) -> Dict[str, float]:
        return {"Humour":   self.humour,   "Honesty":  self.honesty,
                "Courage":  self.courage,  "Optimism": self.optimism,
                "Opacity":  self.opacity,  "Power%":   self.power_pct/100}

    def articulate_panels(self, mode: str = "walk") -> Dict[str, float]:
        """Return panel configuration angles for different modes."""
        configs = {
            "walk":    {"panel1": 0,  "panel2": 90,  "panel3": 0,   "panel4": 90},
            "roll":    {"panel1": 45, "panel2": 45,  "panel3": 45,  "panel4": 45},
            "compact": {"panel1": 0,  "panel2": 0,   "panel3": 0,   "panel4": 0},
            "dock":    {"panel1": 90, "panel2": 0,   "panel3": 90,  "panel4": 0},
            "deploy":  {"panel1": 45, "panel2": 135, "panel3": 45,  "panel4": 135},
        }
        return configs.get(mode, configs["walk"])

    def status_summary(self) -> Dict[str, Any]:
        return {
            "name":           self.name,
            "robot_id":       self.robot_id.value,
            "mode":           self.mode.value,
            "power_pct":      self.power_pct,
            "active":         self.active,
            "humour_%":       self.humour*100,
            "honesty_%":      self.honesty*100,
            "courage_%":      self.courage*100,
            "optimism_%":     self.optimism*100,
            "opacity_%":      self.opacity*100,
            "data_crystal_Gbits": self.data_crystal_bits/1e9,
            "decisions_made": len(self.decision_log),
            "log_entries":    len(self.mission_log),
        }


def build_tars() -> AIRobot:
    t = AIRobot(robot_id=CrewID.TARS, name="TARS",
                humour=0.75, honesty=0.90, courage=0.85,
                optimism=0.65, opacity=0.95, mode=RobotMode.NAVIGATION)
    t.record_decision("Mission briefing", "Accept mission parameters", 0.99)
    t.record_decision("Miller approach", "Calculate wave probability", 0.95,
                      "Wave incoming — 1.2 km")
    t.mission_log.append("TARS online. All systems nominal.")
    return t


def build_case() -> AIRobot:
    c = AIRobot(robot_id=CrewID.CASE, name="CASE",
                humour=0.45, honesty=0.95, courage=0.80,
                optimism=0.70, opacity=0.90, mode=RobotMode.NAVIGATION)
    c.mission_log.append("CASE online. Standing by.")
    return c


# ══════════════════════════════════════════════════════════════════════════════
# §7  ENDURANCE SPACECRAFT SYSTEMS
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class ShipModule:
    module_id:   int
    module_type: str         # "HABITAT", "DOCKING", "PROPULSION", "SCIENCE"
    name:        str
    status:      SystemStatus = SystemStatus.NOMINAL
    integrity_pct: float = 100.0
    temperature_C: float = 21.0
    pressure_Pa:   float = 101_325.0
    occupied:      bool  = False
    occupants:     List[str] = field(default_factory=list)

    def degrade(self, stress: float):
        """Apply stress (0–1) to module integrity."""
        self.integrity_pct = max(0.0, self.integrity_pct - stress * 5.0)
        if self.integrity_pct < 30:   self.status = SystemStatus.CRITICAL
        elif self.integrity_pct < 60: self.status = SystemStatus.DEGRADED
        else:                          self.status = SystemStatus.NOMINAL


@dataclass
class LifeSupportSystem:
    """ENDURANCE life support — closed-loop ECLSS model."""
    o2_reserve_kg:     float = 500.0      # oxygen reserve
    co2_absorber_kg:   float = 200.0      # LiOH absorber remaining
    h2o_reserve_L:     float = 2000.0     # potable water
    n2_reserve_kg:     float = 300.0      # nitrogen buffer
    food_reserve_kg:   float = 1500.0     # food stores
    active_crew:       int   = 4
    cryo_crew:         int   = 0
    cabin_temp_C:      float = 21.0
    cabin_pressure_Pa: float = 101_325.0
    humidity_pct:      float = 50.0
    co2_ppm:           float = 1000.0     # current CO₂ level [ppm]
    o2_pct:            float = 21.0       # cabin O₂ fraction [%]

    def consume_per_day(self, days: float = 1.0) -> Dict[str, float]:
        """Consume life support resources for given days."""
        n_active = self.active_crew
        n_cryo   = self.cryo_crew * 0.02  # cryo uses 2% resources
        n_equiv  = n_active + n_cryo
        o2_used   = ENDURANCE_O2_KG_PD * n_equiv * days
        co2_prod  = ENDURANCE_CO2_KG_PD * n_equiv * days
        h2o_used  = ENDURANCE_H2O_L_PD * n_equiv * days
        food_used = ENDURANCE_FOOD_KCAL * n_equiv * days / 1000  # rough kg
        self.o2_reserve_kg   -= o2_used
        self.co2_absorber_kg -= co2_prod * 0.6  # LiOH absorbs 60%
        self.h2o_reserve_L   -= h2o_used * 0.7  # recycling
        self.food_reserve_kg -= food_used
        # Update cabin CO₂
        self.co2_ppm = min(5000, 1000 + (co2_prod/max(0.01,self.co2_absorber_kg))*500)
        return {"o2_used_kg": o2_used, "co2_prod_kg": co2_prod,
                "h2o_used_L": h2o_used, "food_used_kg": food_used}

    def remaining_days(self) -> Dict[str, float]:
        """Days of life support remaining for each resource."""
        n = max(self.active_crew, 1)
        return {
            "o2_days":   self.o2_reserve_kg   / (ENDURANCE_O2_KG_PD  * n),
            "co2_days":  self.co2_absorber_kg  / (ENDURANCE_CO2_KG_PD * n * 0.6),
            "h2o_days":  self.h2o_reserve_L    / (ENDURANCE_H2O_L_PD * n * 0.7),
            "food_days": self.food_reserve_kg  / (ENDURANCE_FOOD_KCAL * n / 1000),
        }

    def co2_alert(self) -> AlertLevel:
        if   self.co2_ppm < 2000: return AlertLevel.GREEN
        elif self.co2_ppm < 3500: return AlertLevel.YELLOW
        elif self.co2_ppm < 5000: return AlertLevel.ORANGE
        else:                     return AlertLevel.RED

    def status_dict(self) -> Dict[str, Any]:
        rem = self.remaining_days()
        return {
            "O₂ reserve (kg)":      round(self.o2_reserve_kg, 1),
            "CO₂ absorber (kg)":    round(self.co2_absorber_kg, 1),
            "H₂O reserve (L)":      round(self.h2o_reserve_L, 1),
            "Food (kg)":            round(self.food_reserve_kg, 1),
            "CO₂ (ppm)":            round(self.co2_ppm, 0),
            "O₂ cabin (%)":         round(self.o2_pct, 2),
            "Cabin temp (°C)":      round(self.cabin_temp_C, 1),
            "Pressure (kPa)":       round(self.cabin_pressure_Pa/1e3, 2),
            "Humidity (%)":         round(self.humidity_pct, 1),
            "Active crew":          self.active_crew,
            "Cryo crew":            self.cryo_crew,
            "O₂ days left":         round(rem["o2_days"], 1),
            "H₂O days left":        round(rem["h2o_days"], 1),
            "Food days left":       round(rem["food_days"], 1),
            "CO₂ alert":            self.co2_alert().name,
        }


@dataclass
class PropulsionSystem:
    """Endurance main drive + RCS."""
    fuel_kg_remaining:  float = ENDURANCE_FUEL_KG
    isp_s:              float = ENDURANCE_ISP
    thrust_N:           float = 1.5e6
    engine_status:      SystemStatus = SystemStatus.NOMINAL
    rcs_status:         SystemStatus = SystemStatus.NOMINAL
    dv_remaining_ms:    float = 0.0    # calculated from current mass
    burns_performed:    int   = 0
    total_dv_used_ms:   float = 0.0
    g0 = 9.80665

    def __post_init__(self):
        self._update_dv()

    def _update_dv(self, ship_dry_mass_kg: float = 2.0e5):
        """Recalculate Δv from remaining fuel."""
        m_total = ship_dry_mass_kg + self.fuel_kg_remaining
        if self.fuel_kg_remaining > 0:
            self.dv_remaining_ms = (self.isp_s * self.g0 *
                                    math.log(m_total/ship_dry_mass_kg))

    def burn(self, dv_ms: float, dry_mass_kg: float = 2.0e5) -> Dict[str, float]:
        """Execute a propulsive burn of Δv [m/s]."""
        v_e      = self.isp_s * self.g0
        m_before = dry_mass_kg + self.fuel_kg_remaining
        m_after  = m_before * math.exp(-dv_ms/v_e)
        m_prop   = m_before - m_after
        self.fuel_kg_remaining -= m_prop
        self.fuel_kg_remaining  = max(0.0, self.fuel_kg_remaining)
        self.total_dv_used_ms  += dv_ms
        self.burns_performed   += 1
        self._update_dv(dry_mass_kg)
        return {"dv_executed_ms": dv_ms, "propellant_kg": m_prop,
                "fuel_remaining_kg": self.fuel_kg_remaining,
                "dv_remaining_ms": self.dv_remaining_ms}

    def burn_time_s(self, dv_ms: float, ship_mass_kg: float = 5e5) -> float:
        """Burn duration for given Δv: Δt = m·Δv / F (approx constant thrust)."""
        return ship_mass_kg * dv_ms / (self.thrust_N + 1e-10)

    def status_dict(self) -> Dict[str, Any]:
        return {
            "Fuel remaining (kg)":   round(self.fuel_kg_remaining, 1),
            "Fuel remaining (%)":    round(self.fuel_kg_remaining/ENDURANCE_FUEL_KG*100, 1),
            "Isp (s)":               self.isp_s,
            "Thrust (kN)":           round(self.thrust_N/1e3, 1),
            "Δv remaining (m/s)":    round(self.dv_remaining_ms, 1),
            "Δv remaining (km/s)":   round(self.dv_remaining_ms/1e3, 3),
            "Total Δv used (km/s)":  round(self.total_dv_used_ms/1e3, 3),
            "Burns performed":        self.burns_performed,
            "Engine status":         self.engine_status.value,
            "RCS status":            self.rcs_status.value,
        }


@dataclass
class PowerSystem:
    """Endurance electrical power budget."""
    rtg_power_kW:     float = 20.0   # RTG (constant)
    solar_power_kW:   float = 25.0   # solar (distance-dependent)
    fuel_cell_kW:     float = 0.0    # fuel cell (on demand)
    battery_kWh:      float = 200.0  # battery bank
    total_demand_kW:  float = 35.0   # baseline load
    distance_AU:      float = 9.537  # current distance from Sun

    def solar_output(self) -> float:
        """Solar power falls as 1/r² beyond 1 AU."""
        return 25.0 / (self.distance_AU**2)

    def total_supply_kW(self) -> float:
        return self.rtg_power_kW + self.solar_output() + self.fuel_cell_kW

    def power_margin_kW(self) -> float:
        return self.total_supply_kW() - self.total_demand_kW

    def status_dict(self) -> Dict[str, Any]:
        return {
            "RTG (kW)":            self.rtg_power_kW,
            "Solar (kW)":          round(self.solar_output(), 2),
            "Fuel cell (kW)":      self.fuel_cell_kW,
            "Total supply (kW)":   round(self.total_supply_kW(), 2),
            "Total demand (kW)":   self.total_demand_kW,
            "Power margin (kW)":   round(self.power_margin_kW(), 2),
            "Battery (kWh)":       self.battery_kWh,
            "Distance from Sun (AU)": self.distance_AU,
            "Power status":        ("SURPLUS" if self.power_margin_kW() > 0
                                    else "DEFICIT"),
        }


class EnduranceSpacecraft:
    """
    Complete ENDURANCE spacecraft model.
    16-module rotating ring, full systems integration.
    """

    def __init__(self):
        self.modules    = self._build_modules()
        self.life_support = LifeSupportSystem()
        self.propulsion   = PropulsionSystem()
        self.power        = PowerSystem()
        self.mission_elapsed_days = 0.0
        self.rotation_rpm = ENDURANCE_RPM
        self.hull_integrity_pct = 100.0
        self.micromet_impacts   = 0
        self.tidal_stress_events= 0
        self.alert_log: List[Dict] = []
        self.system_status = SystemStatus.NOMINAL

    def _build_modules(self) -> List[ShipModule]:
        modules = []
        # 12 hexagonal habitat modules
        hab_names = ["Alpha","Beta","Gamma","Delta","Epsilon","Zeta",
                     "Eta","Theta","Iota","Kappa","Lambda","Mu"]
        for i, name in enumerate(hab_names):
            modules.append(ShipModule(
                module_id=i, module_type="HABITAT",
                name=f"Hab-{name}", status=SystemStatus.NOMINAL))
        # 4 rectangular docking/propulsion modules
        for i, name in enumerate(["Dock-North","Dock-East","Dock-South","Dock-West"]):
            modules.append(ShipModule(
                module_id=12+i, module_type="DOCKING",
                name=name, status=SystemStatus.NOMINAL))
        return modules

    def artificial_gravity(self, r_m: float = None) -> float:
        """
        Centripetal acceleration at ring radius r:
          a = ω²r  where ω = 2π·RPM/60
        Default r = ENDURANCE ring radius.
        """
        r   = r_m if r_m else ENDURANCE_RADIUS_M
        omega = 2*math.pi*self.rotation_rpm/60
        return omega**2 * r

    def gravity_profile(self, n_r: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """Artificial gravity vs radial position in ring."""
        r_arr = np.linspace(1.0, ENDURANCE_RADIUS_M, n_r)
        a_arr = np.array([self.artificial_gravity(r) for r in r_arr])
        return r_arr, a_arr

    def apply_tidal_stress(self, tidal_g_per_m: float):
        """Apply tidal stress event from Gargantua proximity."""
        for mod in self.modules:
            mod.degrade(tidal_g_per_m * 0.1)
        self.hull_integrity_pct -= tidal_g_per_m * 0.5
        self.hull_integrity_pct  = max(0.0, self.hull_integrity_pct)
        self.tidal_stress_events += 1
        self._add_alert(f"TIDAL STRESS: {tidal_g_per_m:.3e} g/m applied")

    def apply_micrometeorite(self, v_impactor_ms: float = 2e4,
                              m_impactor_kg: float = 1e-6):
        """Small micrometeorite impact on hull."""
        E_impact = 0.5 * m_impactor_kg * v_impactor_ms**2
        stress   = E_impact / 1e6   # rough stress per MJ
        self.hull_integrity_pct -= stress * 0.01
        self.hull_integrity_pct  = max(0.0, self.hull_integrity_pct)
        self.micromet_impacts   += 1

    def _add_alert(self, message: str):
        self.alert_log.append({
            "time": time.time(),
            "message": message,
            "day": self.mission_elapsed_days,
        })

    def advance_mission(self, days: float,
                         is_cryo_crew_list: List[bool] = None):
        """Advance mission timeline by given days."""
        self.mission_elapsed_days += days
        self.life_support.consume_per_day(days)
        # Random micrometeorite event (Poisson, ~0.1/day)
        n_impacts = np.random.poisson(0.1 * days)
        for _ in range(n_impacts):
            self.apply_micrometeorite()
        # Power consumption
        self.power.battery_kWh += self.power.power_margin_kW() * days * 24
        self.power.battery_kWh  = np.clip(self.power.battery_kWh, 0, 200)

    def full_status(self) -> Dict[str, Any]:
        worst_mod  = min(self.modules, key=lambda m: m.integrity_pct)
        n_crit     = sum(1 for m in self.modules if m.status == SystemStatus.CRITICAL)
        n_deg      = sum(1 for m in self.modules if m.status == SystemStatus.DEGRADED)
        return {
            "mission_day":        round(self.mission_elapsed_days, 1),
            "hull_integrity_pct": round(self.hull_integrity_pct, 2),
            "rotation_rpm":       self.rotation_rpm,
            "artificial_g":       round(self.artificial_gravity()/9.81, 3),
            "modules_total":      len(self.modules),
            "modules_nominal":    sum(1 for m in self.modules if m.status==SystemStatus.NOMINAL),
            "modules_degraded":   n_deg,
            "modules_critical":   n_crit,
            "worst_module":       worst_mod.name,
            "worst_integrity%":   round(worst_mod.integrity_pct, 1),
            "micromet_impacts":   self.micromet_impacts,
            "tidal_events":       self.tidal_stress_events,
            "alerts":             len(self.alert_log),
            "system_status":      self.system_status.value,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §8  CRYOSLEEP SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class CryosleepPod:
    pod_id:         int
    assigned_crew:  Optional[CrewID] = None
    occupied:       bool  = False
    temp_C:         float = 20.0     # current temperature
    target_temp_C:  float = -10.0   # hibernation target
    status:         SystemStatus = SystemStatus.STANDBY
    metabolic_rate_pct: float = 100.0   # 100% awake, 5% in cryo
    duration_days:  float = 0.0
    revival_ready:  bool  = False
    emergency_mode: bool  = False

    def initiate_cryo(self, crew: CrewID):
        self.assigned_crew  = crew
        self.occupied       = True
        self.status         = SystemStatus.ACTIVE if False else SystemStatus.NOMINAL
        self.metabolic_rate_pct = 5.0
        self.revival_ready  = False
        self.temp_C         = -10.0
        return f"Pod {self.pod_id} — Cryo initiated for {crew.value}"

    def revival_protocol(self, emergency: bool = False) -> List[str]:
        """
        Standard revival: 4-hour warm-up.
        Emergency revival: 45-minute rapid warm-up (higher cardiac risk).
        """
        self.emergency_mode = emergency
        self.revival_ready  = True
        steps = []
        if emergency:
            steps = [
                "0 min: Emergency revival initiated — cardiac monitor active",
                "5 min: Temperature ramp 3°C/min",
                "20 min: Core temp 30°C — neural reactivation",
                "35 min: Defibrillation standby ready",
                "45 min: Full revival — 12% cardiac risk",
            ]
        else:
            steps = [
                "0:00 — Gradual warm: −10°C → 0°C over 60 min",
                "1:00 — Neural stimulation begun: EEG monitoring",
                "1:30 — Core temp 10°C: circulatory flush",
                "2:00 — Nutritional IV drip initiated",
                "3:00 — Core temp 20°C: motor function check",
                "3:30 — Cognitive assessment protocol",
                "4:00 — Full revival complete — crew cleared for duty",
            ]
        self.metabolic_rate_pct = 100.0
        self.temp_C = 37.0
        self.occupied = False
        return steps


class CryosleepManager:
    def __init__(self, n_pods: int = 6):
        self.pods = [CryosleepPod(pod_id=i) for i in range(n_pods)]
        self.cryo_log: List[Dict] = []

    def put_to_sleep(self, crew: CrewID, pod_id: int = None) -> str:
        if pod_id is not None and pod_id < len(self.pods):
            pod = self.pods[pod_id]
        else:
            pod = next((p for p in self.pods if not p.occupied), None)
        if pod is None:
            return "ERROR: No available pods"
        msg = pod.initiate_cryo(crew)
        self.cryo_log.append({"action":"sleep","crew":crew.value,"pod":pod.pod_id})
        return msg

    def revive(self, crew: CrewID, emergency: bool = False) -> List[str]:
        pod = next((p for p in self.pods if p.assigned_crew == crew), None)
        if pod is None:
            return [f"ERROR: {crew.value} not in cryosleep"]
        steps = pod.revival_protocol(emergency)
        self.cryo_log.append({"action":"revive","crew":crew.value,"emergency":emergency})
        return steps

    def pods_status(self) -> pd.DataFrame:
        rows = [{"Pod ID":    p.pod_id,
                 "Crew":      p.assigned_crew.value if p.assigned_crew else "—",
                 "Occupied":  p.occupied,
                 "Temp (°C)": p.temp_C,
                 "Metabolic%":p.metabolic_rate_pct,
                 "Status":    p.status.value,
                 "Duration(d)":round(p.duration_days,1),
                 "Emergency": p.emergency_mode}
                for p in self.pods]
        return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# §9  COMMUNICATIONS SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class Message:
    uid:      str   = field(default_factory=lambda: uuid.uuid4().hex[:8].upper())
    sender:   str   = "ENDURANCE"
    recipient:str   = "NASA_EARTH"
    content:  str   = ""
    timestamp:float = field(default_factory=time.time)
    delivered:bool  = False
    lag_s:    float = 0.0
    encrypted:bool  = True
    priority: str   = "NORMAL"    # NORMAL / URGENT / CRITICAL


class CommunicationsRelay:
    """
    Deep space communications with light-travel-time delay,
    bandwidth limits, and signal encryption.
    """

    DSN_BANDS = {
        "S-band":  {"freq_GHz": 2.1,  "bandwidth_kbps": 20.0,  "range_AU": 20.0},
        "X-band":  {"freq_GHz": 8.4,  "bandwidth_kbps": 100.0, "range_AU": 100.0},
        "Ka-band": {"freq_GHz": 32.0, "bandwidth_kbps": 800.0, "range_AU": 50.0},
    }

    def __init__(self):
        self.inbox:    List[Message] = []
        self.outbox:   List[Message] = []
        self.band:     str   = "Ka-band"
        self.distance_AU: float = SATURN_SMA_AU = 9.537
        self.wormhole_relay: bool = False
        self._seed_nasa_messages()

    def _seed_nasa_messages(self):
        """Pre-populate with canonical film messages."""
        msgs = [
            ("PROF_BRAND", "ENDURANCE", "Launch successful. You are now beyond Saturn. Good luck. — Prof. Brand"),
            ("MURPH", "COOPER", "Dad, the blight reached the southern hemisphere. Corn is gone. Please hurry."),
            ("NASA", "ENDURANCE", "Wormhole remains stable. Saturn observation confirms stable geometry."),
            ("MURPH", "COOPER", "I figured it out dad. The equation. TARS data was enough. We can all go."),
            ("NASA", "ENDURANCE", "Plan A complete. Colony ships launching. Thank you, Cooper. Come home."),
        ]
        for i, (sndr, rcpt, content) in enumerate(msgs):
            m = Message(sender=sndr, recipient=rcpt, content=content,
                        lag_s=self.signal_lag_s(), delivered=(i<3))
            self.inbox.append(m)

    def signal_lag_s(self, distance_AU: float = None) -> float:
        """One-way light travel time [s]."""
        d = distance_AU if distance_AU else self.distance_AU
        return d * AU / C_SI

    def signal_lag_formatted(self, distance_AU: float = None) -> str:
        lag = self.signal_lag_s(distance_AU)
        if lag < 60:       return f"{lag:.1f} s"
        elif lag < 3600:   return f"{lag/60:.1f} min"
        elif lag < 86400:  return f"{lag/3600:.2f} hr"
        else:              return f"{lag/86400:.2f} days"

    def bandwidth_bps(self) -> float:
        """Current effective bandwidth in bits/s."""
        band  = self.DSN_BANDS[self.band]
        # FSPL: received power ∝ 1/d²
        d_ref = 1.0   # 1 AU reference
        d     = max(self.distance_AU, 0.01)
        attenuation = (d_ref/d)**2
        return band["bandwidth_kbps"] * 1000 * attenuation

    def send(self, content: str, sender: str = "ENDURANCE",
              priority: str = "NORMAL") -> Message:
        lag = self.signal_lag_s()
        m   = Message(sender=sender, recipient="NASA_EARTH",
                      content=content, lag_s=lag, priority=priority)
        self.outbox.append(m)
        return m

    def time_to_transmit(self, msg_bits: int = 8192) -> float:
        """Time to transmit a message [s] given bandwidth."""
        return msg_bits / max(self.bandwidth_bps(), 1.0)

    def wormhole_relay_possible(self) -> bool:
        """True if signal can be relayed through wormhole mouth."""
        return self.wormhole_relay

    def signal_strength_dBm(self, distance_AU: float = None,
                              tx_power_W: float = 10.0) -> float:
        """Received signal power in dBm (Friis equation)."""
        d   = (distance_AU or self.distance_AU) * AU
        f   = self.DSN_BANDS[self.band]["freq_GHz"] * 1e9
        lam = C_SI / f
        # Friis: P_r = P_t G_t G_r (λ/4πd)²
        Gt  = 1e6   # 60dBi HGA transmit gain
        Gr  = 1e9   # 90dBi 70m DSN dish gain
        P_r = tx_power_W * Gt * Gr * (lam/(4*math.pi*d))**2
        return 10*math.log10(P_r/1e-3)  # dBm

    def message_queue_df(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        def to_df(msgs):
            rows = [{"UID":m.uid, "From":m.sender, "To":m.recipient,
                     "Content":m.content[:60]+"...", "Lag":self.signal_lag_formatted(None),
                     "Priority":m.priority, "Delivered":m.delivered,
                     "Encrypted":m.encrypted} for m in msgs[-10:]]
            return pd.DataFrame(rows) if rows else pd.DataFrame()
        return to_df(self.inbox), to_df(self.outbox)


# ══════════════════════════════════════════════════════════════════════════════
# §10  PHYSIOLOGY TIME SERIES SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
class PhysiologySimulator:
    """Generate realistic physiological time series for crew monitoring."""

    def __init__(self, fs: float = 1.0):     # 1 sample/second default
        self.fs = fs

    def ecg_waveform(self, hr_bpm: float, duration_s: float = 10.0) -> Tuple[np.ndarray, np.ndarray]:
        """Simplified ECG waveform generation."""
        t     = np.linspace(0, duration_s, int(duration_s*self.fs))
        rr    = 60.0/hr_bpm    # R-R interval
        n_cycles = int(duration_s/rr) + 2
        signal = np.zeros(len(t))
        for k in range(n_cycles):
            t0 = k*rr
            # P wave: Gaussian at 0.2×RR before R
            signal += 0.20*np.exp(-0.5*((t-(t0+0.2*rr))/0.04)**2)
            # Q wave: small negative at 0.05×RR before R
            signal -= 0.05*np.exp(-0.5*((t-(t0+rr-0.05))/0.02)**2)
            # R peak: large positive
            signal += 1.00*np.exp(-0.5*((t-(t0+rr))/0.015)**2)
            # S wave: small negative after R
            signal -= 0.15*np.exp(-0.5*((t-(t0+rr+0.03))/0.025)**2)
            # T wave: moderate at 0.35×RR after R
            signal += 0.35*np.exp(-0.5*((t-(t0+rr+0.35*rr))/0.08)**2)
        # Add physiological noise
        signal += np.random.randn(len(t)) * 0.02
        return t, signal

    def spo2_waveform(self, spo2_pct: float, hr_bpm: float, duration_s: float = 10.0
                       ) -> Tuple[np.ndarray, np.ndarray]:
        """Plethysmography waveform (SpO₂ sensor signal)."""
        t   = np.linspace(0, duration_s, int(duration_s*self.fs))
        rr  = 60.0/hr_bpm
        sig = np.zeros(len(t))
        for k in range(int(duration_s/rr)+2):
            t0   = k*rr
            sig += np.exp(-0.5*((t-t0-rr)/0.15)**2)
        sig = sig * spo2_pct/100 + np.random.randn(len(t))*0.003
        return t, sig

    def radiation_accumulation(self, days_arr: np.ndarray,
                                dose_rate_mSv_day: float = RAD_DAILY_SPACE
                                ) -> np.ndarray:
        """Cumulative radiation dose accumulation with solar event spikes."""
        base_dose = days_arr * dose_rate_mSv_day
        # Random solar energetic particle events
        n_events = max(0, int(np.random.poisson(len(days_arr)/200)))
        for _ in range(n_events):
            t_ev = random.uniform(days_arr[0], days_arr[-1])
            idx  = np.argmin(np.abs(days_arr - t_ev))
            spike = random.uniform(5, 50)   # 5–50 mSv spike
            base_dose[idx:] += spike
        return base_dose

    def physiological_profile(self, crew: CrewMember, days: int = 700
                               ) -> pd.DataFrame:
        """Full mission physiological profile for a crew member."""
        t_arr   = np.linspace(0, days, days)
        # Bone density loss
        bone    = 100.0 - BONE_LOSS_PCT_MO*t_arr/30.44
        # Muscle mass
        muscle  = 100.0 - MUSCLE_LOSS_PCT_MO*t_arr/30.44 * 0.6
        # Radiation
        rad     = self.radiation_accumulation(t_arr)
        # Psychological stress (increases then plateaus)
        stress  = 20.0*(1 - np.exp(-t_arr/120)) + 5*np.sin(t_arr*2*math.pi/30)
        # Morale (decreasing with noise)
        morale  = 85.0 - 0.04*t_arr + 5*np.cos(t_arr*2*math.pi/7)
        morale  = np.clip(morale, 10, 100)
        return pd.DataFrame({
            "day":              t_arr,
            "bone_density_pct": np.clip(bone, 50, 100),
            "muscle_mass_pct":  np.clip(muscle, 50, 100),
            "radiation_mSv":    rad,
            "stress_pct":       np.clip(stress, 0, 100),
            "morale_pct":       morale,
        })


# ══════════════════════════════════════════════════════════════════════════════
# §11  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    D: Dict[str, Any] = {
        "crew_registry":    build_crew_registry(),
        "tars":             build_tars(),
        "case":             build_case(),
        "endurance":        EnduranceSpacecraft(),
        "cryo_mgr":         CryosleepManager(n_pods=6),
        "comms":            CommunicationsRelay(),
        "physio":           PhysiologySimulator(fs=500.0),
        "mission_phase":    MissionPhase.SATURN_TRANSIT,
        "mission_day":      0.0,
        "tars_humour":      TARS_DEFAULT_HUMOUR,
        "tars_honesty":     TARS_DEFAULT_HONESTY,
        "tars_courage":     TARS_DEFAULT_COURAGE,
        "tars_optimism":    TARS_DEFAULT_OPTIMISM,
        "tars_opacity":     TARS_DEFAULT_OPACITY,
        "case_humour":      0.45,
        "case_honesty":     0.95,
        "selected_crew":    CrewID.COOPER.name,
        "physio_profile":   None,
        "ecg_waveform":     None,
        "advance_days":     1.0,
        "comms_msg":        "",
        "comms_distance":   9.537,
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# §12  MATPLOTLIB STYLE
# ══════════════════════════════════════════════════════════════════════════════
MPL_STYLE = {
    "figure.facecolor":  "#04080e",
    "axes.facecolor":    "#060a14",
    "axes.edgecolor":    "#101835",
    "axes.labelcolor":   "#E8C46A",
    "axes.grid":         True,
    "grid.color":        "#0c1028",
    "grid.linestyle":    ":",
    "grid.alpha":        0.5,
    "xtick.color":       "#304070",
    "ytick.color":       "#304070",
    "xtick.labelsize":   6,
    "ytick.labelsize":   6,
    "axes.labelsize":    7,
    "axes.titlesize":    8,
    "axes.titlecolor":   "#E8C46A",
    "text.color":        "#E8C46A",
    "font.family":       "monospace",
    "legend.facecolor":  "#060a14",
    "legend.edgecolor":  "#101835",
    "legend.fontsize":   6,
    "figure.dpi":        110,
    "savefig.facecolor": "#04080e",
    "axes.spines.top":   False,
    "axes.spines.right": False,
}
def _mpl(): plt.rcParams.update(MPL_STYLE)

CREW_COLORS = {
    CrewID.COOPER:  "#E8C46A",
    CrewID.BRAND:   "#81C784",
    CrewID.ROMILLY: "#4FC3F7",
    CrewID.DOYLE:   "#CE93D8",
}

# ══════════════════════════════════════════════════════════════════════════════
# §13  PLOTTING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def _plot_crew_vitals(crew_dict: Dict[CrewID, CrewMember]) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 4, figsize=(16, 7))
    fig.patch.set_facecolor("#04080e")
    physio = PhysiologySimulator(fs=500.0)
    members = [c for c in crew_dict.values()
               if c.status != CrewStatus.DECEASED][:4]
    metrics = ["HR (bpm)","SpO₂ (%)","Temp (°C)","Stress %"]

    # Top row: ECG waveforms
    for ax, crew in zip(axes[0], members):
        t, ecg = physio.ecg_waveform(crew.hr_bpm, duration_s=5.0)
        clr = CREW_COLORS.get(crew.crew_id, "#E8C46A")
        ax.plot(t, ecg, color=clr, lw=0.9)
        ax.set_title(f"{crew.crew_id.value.split()[0]}\n"
                     f"HR={crew.hr_bpm:.0f}bpm  SpO₂={crew.spo2_pct:.1f}%", fontsize=7)
        ax.set_xlabel("Time [s]"); ax.set_ylabel("ECG [mV]")
        ax.set_facecolor("#030508")
        # Alert border
        al = crew.alert_level()
        border_c = {"GREEN":"#81C784","YELLOW":"#FFD700",
                    "ORANGE":"#FF8800","RED":"#EF5350","CRITICAL":"#CE93D8"}.get(al.name,"#555")
        for spine in ax.spines.values():
            spine.set_edgecolor(border_c); spine.set_linewidth(1.5)

    # Bottom row: physiological metrics radar bars
    metric_vals = {
        "Bone\ndensity%":   [100-c.bone_loss_pct for c in members],
        "Muscle\n%":        [100-c.muscle_loss_pct for c in members],
        "Morale\n%":        [c.morale*100 for c in members],
        "Health\nscore":    [c.health_score()*100 for c in members],
    }
    for ax, (metric, vals) in zip(axes[1], metric_vals.items()):
        names = [c.crew_id.value.split()[0] for c in members]
        colors= [CREW_COLORS.get(c.crew_id,"#E8C46A") for c in members]
        bars  = ax.bar(names, vals, color=colors, alpha=0.82, width=0.5)
        ax.bar_label(bars, fmt="%.0f", padding=2, fontsize=7, color="#fff")
        ax.set_ylim(0, 110)
        ax.set_ylabel(metric, fontsize=6)
        ax.set_title(metric, fontsize=7)
        ax.set_facecolor("#060a14")
        ax.axhline(70, color="#FFB74D", lw=0.6, ls="--", alpha=0.7)

    plt.tight_layout()
    return fig


def _plot_physiological_profile(df: pd.DataFrame, crew_name: str) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    fig.patch.set_facecolor("#04080e")
    specs = [
        ("bone_density_pct", "#E8C46A", "Bone Density [%]",    [80,100], "↓ Osteoporosis risk"),
        ("muscle_mass_pct",  "#FF8800", "Muscle Mass [%]",     [70,100], "↓ Atrophy"),
        ("radiation_mSv",    "#EF5350", "Cumulative Rad [mSv]",[0,500],  "↑ Cancer risk"),
        ("stress_pct",       "#CE93D8", "Stress Index [%]",    [0,80],   "↑ Psychological"),
        ("morale_pct",       "#81C784", "Morale [%]",          [0,100],  "↓ Mission cohesion"),
    ]
    for ax, (col, clr, ylabel, ylim, note) in zip(axes.flat[:5], specs):
        ax.plot(df["day"], df[col], color=clr, lw=1.0)
        ax.fill_between(df["day"], df[col], ylim[0], alpha=0.12, color=clr)
        ax.set_xlabel("Mission day"); ax.set_ylabel(ylabel)
        ax.set_title(f"{ylabel}\n({note})")
        ax.set_ylim(ylim)
        ax.set_facecolor("#060a14")
        if col == "radiation_mSv":
            ax.axhline(500, color="#EF5350", lw=0.7, ls="--",
                       label="NASA career limit")
            ax.legend(fontsize=5.5)

    # 6th: health composite
    ax6 = axes.flat[5]
    health = ((df["bone_density_pct"]-70)/30 * 0.25 +
              (df["muscle_mass_pct"]-70)/30 * 0.25 +
              (100-df["radiation_mSv"]/5)/100 * 0.25 +
              df["morale_pct"]/100 * 0.25)
    health = np.clip(health, 0, 1)
    ax6.plot(df["day"], health*100, color="#E8C46A", lw=1.2)
    ax6.fill_between(df["day"], health*100, 0, alpha=0.15, color="#E8C46A")
    ax6.axhline(60, color="#FFB74D", lw=0.6, ls="--", label="Minimum acceptable")
    ax6.set_xlabel("Mission day"); ax6.set_ylabel("Composite health [%]")
    ax6.set_title(f"COMPOSITE HEALTH SCORE — {crew_name}")
    ax6.legend(fontsize=6); ax6.set_facecolor("#060a14")
    plt.tight_layout()
    return fig


def _plot_tars_panel(tars: AIRobot, case: AIRobot) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#04080e")

    def _radar(ax, robot, clr):
        cats  = ["Humour","Honesty","Courage","Optimism","Opacity"]
        N     = len(cats)
        vals  = [robot.humour, robot.honesty, robot.courage, robot.optimism, robot.opacity]
        angles= [2*math.pi*i/N for i in range(N)] + [0]
        vals  += vals[:1]
        ax.set_theta_offset(math.pi/2); ax.set_theta_direction(-1)
        ax.plot(angles, vals, color=clr, lw=1.5)
        ax.fill(angles, vals, color=clr, alpha=0.15)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(cats, fontsize=7, color="#E8C46A")
        ax.set_ylim(0, 1); ax.set_yticks([0.2,0.4,0.6,0.8,1.0])
        ax.set_yticklabels(["0.2","0.4","0.6","0.8","1.0"], fontsize=5)
        ax.set_facecolor("#030508")
        ax.grid(color="#1a2040", lw=0.5)
        ax.set_title(f"{robot.name} PERSONALITY MATRIX", color=clr, fontsize=8, pad=15)

    ax1 = fig.add_subplot(131, polar=True); _radar(ax1, tars, "#E8C46A")
    ax2 = fig.add_subplot(132, polar=True); _radar(ax2, case, "#4FC3F7")

    # Right: TARS 4-panel schematic
    ax3 = axes[2]
    ax3.set_facecolor("#030508")
    # Draw TARS as 4 rectangular panels
    panel_configs = tars.articulate_panels("walk")
    colors_panel  = ["#E8C46A","#c8a050","#a08040","#806030"]
    for i, (pname, angle) in enumerate(panel_configs.items()):
        x0  = 0.2 + i*0.15
        rad = math.radians(angle)
        w   = 0.12; h = 0.6
        # Approximate panel as rotated rectangle
        rect = FancyBboxPatch((x0, 0.2+0.1*math.sin(rad)),
                               w, h*math.cos(math.radians(angle*0.3)),
                               boxstyle="round,pad=0.01",
                               fc=colors_panel[i], ec="#E8C46A", lw=1.0, alpha=0.85)
        ax3.add_patch(rect)
        ax3.text(x0+w/2, 0.17, f"P{i+1}\n{angle}°",
                 ha="center", fontsize=7, color="#E8C46A", fontfamily="monospace")
    ax3.set_xlim(0.1, 0.85); ax3.set_ylim(0.0, 1.0)
    ax3.set_aspect("equal"); ax3.axis("off")
    ax3.set_title("TARS — 4-PANEL ARTICULATION (Walk Mode)", fontsize=8)
    # Power indicator
    pw = tars.power_pct/100
    ax3.add_patch(FancyBboxPatch((0.72, 0.1), 0.08, pw*0.7,
                                  boxstyle="round,pad=0.01",
                                  fc="#81C784", ec="#E8C46A", lw=0.7))
    ax3.text(0.76, 0.85, f"{tars.power_pct:.0f}%\nPWR",
             ha="center", fontsize=7, color="#81C784", fontfamily="monospace")

    plt.tight_layout()
    return fig


def _plot_endurance_systems(ship: EnduranceSpacecraft) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.patch.set_facecolor("#04080e")

    # 1. Module ring diagram
    ax1 = axes[0,0]
    ax1.set_facecolor("#020408")
    n_mods = len(ship.modules)
    angles = np.linspace(0, 2*math.pi, n_mods, endpoint=False)
    r_ring = ENDURANCE_RADIUS_M
    status_colors = {
        SystemStatus.NOMINAL:   "#81C784",
        SystemStatus.DEGRADED:  "#FFB74D",
        SystemStatus.CRITICAL:  "#EF5350",
        SystemStatus.STANDBY:   "#4FC3F7",
        SystemStatus.OFFLINE:   "#555555",
        SystemStatus.EMERGENCY: "#CE93D8",
    }
    for mod, ang in zip(ship.modules, angles):
        x = r_ring*math.cos(ang); y = r_ring*math.sin(ang)
        clr = status_colors.get(mod.status, "#888")
        shape = "s" if mod.module_type=="DOCKING" else "o"
        ax1.scatter([x], [y], color=clr, s=300, marker=shape,
                    edgecolors="#E8C46A", lw=0.7, zorder=5)
        ax1.text(x*1.12, y*1.12, mod.name.split("-")[1][:3],
                 ha="center", va="center", fontsize=5, color=clr)
    ax1.add_patch(Circle((0,0), r_ring*0.55, color="#070a14",
                          zorder=3, fill=True))
    ax1.text(0, 0, f"ENDURANCE\n{ship.hull_integrity_pct:.0f}%",
             ha="center", va="center", fontsize=7, color="#E8C46A",
             fontfamily="monospace")
    ax1.set_xlim(-60, 60); ax1.set_ylim(-60, 60)
    ax1.set_aspect("equal"); ax1.axis("off")
    ax1.set_title("MODULE RING STATUS", fontsize=8)
    # Legend
    for st, clr in list(status_colors.items())[:4]:
        ax1.scatter([], [], color=clr, s=40, label=st.value[:8])
    ax1.legend(fontsize=5, loc="upper right")

    # 2. Artificial gravity profile
    ax2 = axes[0,1]
    r_arr, a_arr = ship.gravity_profile()
    ax2.plot(r_arr, a_arr/9.81, color="#E8C46A", lw=1.3)
    ax2.axhline(1.0, color="#81C784", lw=0.7, ls="--", label="1g (Earth)")
    ax2.axvline(ENDURANCE_RADIUS_M, color="#4FC3F7", lw=0.8, ls=":",
                label=f"Ring radius {ENDURANCE_RADIUS_M}m")
    ax2.fill_between(r_arr, 0, a_arr/9.81, alpha=0.15, color="#E8C46A")
    ax2.set_xlabel("Radial position [m]")
    ax2.set_ylabel("Centripetal acceleration [g]")
    ax2.set_title(f"ARTIFICIAL GRAVITY PROFILE\n{ship.rotation_rpm} RPM")
    ax2.legend(fontsize=6)

    # 3. Life support resources
    ax3 = axes[0,2]
    ls   = ship.life_support
    rem  = ls.remaining_days()
    resources = ["O₂", "CO₂\nscrub", "H₂O", "Food"]
    days_rem  = [rem["o2_days"], rem["co2_days"],
                 rem["h2o_days"], rem["food_days"]]
    colors3   = ["#81C784" if d>100 else "#FFB74D" if d>30 else "#EF5350"
                 for d in days_rem]
    bars3     = ax3.bar(resources, days_rem, color=colors3, alpha=0.85, width=0.5)
    ax3.bar_label(bars3, fmt="%.0f d", padding=3, fontsize=7, color="#fff")
    ax3.axhline(30, color="#EF5350", lw=0.7, ls="--", label="30-day critical")
    ax3.set_ylabel("Days remaining")
    ax3.set_title("LIFE SUPPORT RESERVES")
    ax3.legend(fontsize=6)

    # 4. Propulsion fuel
    ax4 = axes[1,0]
    prop = ship.propulsion
    fuel_frac = prop.fuel_kg_remaining/ENDURANCE_FUEL_KG
    theta = np.linspace(0, 2*math.pi*fuel_frac, 200)
    ax4.plot(np.cos(theta), np.sin(theta), color="#FF8800", lw=6,
             solid_capstyle="round")
    ax4.add_patch(Circle((0,0), 0.75, color="#060a14", zorder=3))
    ax4.text(0, 0.1, f"{fuel_frac*100:.1f}%", ha="center", fontsize=20,
             color="#FF8800", fontfamily="monospace", fontweight="bold")
    ax4.text(0, -0.2, "FUEL", ha="center", fontsize=9,
             color="#E8C46A", fontfamily="monospace")
    ax4.text(0, -0.42, f"{prop.fuel_kg_remaining/1e3:.0f} t remaining",
             ha="center", fontsize=7, color="#888", fontfamily="monospace")
    ax4.text(0, -0.58, f"Δv left: {prop.dv_remaining_ms/1e3:.1f} km/s",
             ha="center", fontsize=7, color="#E8C46A", fontfamily="monospace")
    ax4.set_xlim(-1.3, 1.3); ax4.set_ylim(-1.3, 1.3)
    ax4.set_aspect("equal"); ax4.axis("off")
    ax4.set_title("PROPELLANT GAUGE", fontsize=8)

    # 5. Power budget
    ax5 = axes[1,1]
    pw  = ship.power
    categories  = ["RTG","Solar","Fuel Cell","Demand"]
    values      = [pw.rtg_power_kW, pw.solar_output(),
                   pw.fuel_cell_kW, -pw.total_demand_kW]
    colors5     = ["#E8C46A","#FF8800","#4FC3F7","#EF5350"]
    bars5       = ax5.bar(categories, values, color=colors5, alpha=0.85, width=0.5)
    ax5.bar_label(bars5, fmt="%.1f kW", padding=2, fontsize=7, color="#fff")
    ax5.axhline(0, color="#1a2040", lw=0.5)
    margin = pw.power_margin_kW()
    ax5.set_ylabel("Power [kW]")
    ax5.set_title(f"POWER BUDGET — Margin: {margin:+.1f} kW\n"
                  f"Distance: {pw.distance_AU:.1f} AU from Sun")

    # 6. Module integrity histogram
    ax6 = axes[1,2]
    integrities = [m.integrity_pct for m in ship.modules]
    ax6.hist(integrities, bins=10, range=(0,100), color="#4FC3F7",
             alpha=0.80, edgecolor="#E8C46A", lw=0.5)
    ax6.axvline(np.mean(integrities), color="#E8C46A", lw=1.0,
                ls="--", label=f"Mean {np.mean(integrities):.1f}%")
    ax6.axvline(60, color="#EF5350", lw=0.7, ls=":", label="60% threshold")
    ax6.set_xlabel("Module integrity [%]"); ax6.set_ylabel("Count")
    ax6.set_title("MODULE INTEGRITY DISTRIBUTION")
    ax6.legend(fontsize=6)

    plt.tight_layout()
    return fig


def _plot_cryosleep(cryo: CryosleepManager) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor("#04080e")

    # Left: pod grid
    ax1 = axes[0]
    ax1.set_facecolor("#030508")
    pods = cryo.pods
    n    = len(pods)
    cols = 3; rows = math.ceil(n/cols)
    for i, pod in enumerate(pods):
        r = i // cols; c = i % cols
        x = c * 1.2; y = (rows - 1 - r) * 1.5
        face = "#1a4060" if pod.occupied else "#1a2030"
        edge = "#4FC3F7" if pod.occupied else "#303850"
        rect = FancyBboxPatch((x, y), 1.0, 1.2,
                               boxstyle="round,pad=0.06",
                               fc=face, ec=edge, lw=1.5)
        ax1.add_patch(rect)
        ax1.text(x+0.5, y+0.75, f"POD {pod.pod_id}",
                 ha="center", fontsize=7, color="#E8C46A", fontfamily="monospace")
        crew_txt = pod.assigned_crew.value.split()[0] if pod.assigned_crew else "EMPTY"
        ax1.text(x+0.5, y+0.45, crew_txt,
                 ha="center", fontsize=6,
                 color="#4FC3F7" if pod.occupied else "#555",
                 fontfamily="monospace")
        ax1.text(x+0.5, y+0.18, f"{pod.temp_C:.0f}°C | {pod.metabolic_rate_pct:.0f}%",
                 ha="center", fontsize=5.5,
                 color="#81C784" if pod.occupied else "#333",
                 fontfamily="monospace")
    ax1.set_xlim(-0.2, cols*1.2+0.2)
    ax1.set_ylim(-0.3, rows*1.5+0.3)
    ax1.set_aspect("equal"); ax1.axis("off")
    ax1.set_title("CRYOSLEEP POD STATUS", fontsize=8)

    # Right: metabolic rate + temperature comparison
    ax2 = axes[1]
    names  = [f"Pod {p.pod_id}" for p in pods]
    temps  = [p.temp_C for p in pods]
    metab  = [p.metabolic_rate_pct for p in pods]
    x_pos  = np.arange(len(pods))
    w      = 0.35
    b1 = ax2.bar(x_pos - w/2, temps, w, color="#4FC3F7", alpha=0.82,
                  label="Temp [°C]")
    ax2b = ax2.twinx()
    b2 = ax2b.bar(x_pos + w/2, metab, w, color="#E8C46A", alpha=0.82,
                   label="Metabolic %")
    ax2.set_xticks(x_pos); ax2.set_xticklabels(names, rotation=20, fontsize=6)
    ax2.set_ylabel("Temperature [°C]", color="#4FC3F7")
    ax2b.set_ylabel("Metabolic rate [%]", color="#E8C46A")
    ax2.set_title("POD TEMPERATURE & METABOLIC RATE")
    lines  = [b1, b2]; labs = [b.get_label() for b in lines]
    ax2.legend(lines, labs, fontsize=6)

    plt.tight_layout()
    return fig


def _plot_comms(comms: CommunicationsRelay, distance_AU: float) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#04080e")

    # 1. Signal strength vs distance
    ax1 = axes[0]
    d_arr  = np.logspace(-1, 4, 300)   # 0.1 AU to 10,000 AU
    for band in ["S-band","X-band","Ka-band"]:
        bw    = comms.DSN_BANDS[band]["bandwidth_kbps"]
        sig_arr = np.array([
            comms.signal_strength_dBm(d) for d in d_arr])
        ax1.semilogx(d_arr, sig_arr,
                     lw=1.1, label=f"{band} ({bw}kbps)")
    ax1.axvline(distance_AU, color="#E8C46A", lw=0.9, ls="--",
                label=f"Current: {distance_AU:.1f} AU")
    ax1.axhline(-160, color="#EF5350", lw=0.6, ls=":", label="Noise floor")
    ax1.set_xlabel("Distance [AU]"); ax1.set_ylabel("Received power [dBm]")
    ax1.set_title("SIGNAL STRENGTH vs DISTANCE")
    ax1.legend(fontsize=5.5)

    # 2. Bandwidth vs distance
    ax2 = axes[1]
    for band, data in comms.DSN_BANDS.items():
        bw_arr = data["bandwidth_kbps"] * 1000 * (1.0/d_arr**2)
        ax2.loglog(d_arr, np.maximum(bw_arr, 0.001),
                   lw=1.1, label=band)
    ax2.axvline(distance_AU, color="#E8C46A", lw=0.9, ls="--")
    ax2.set_xlabel("Distance [AU]"); ax2.set_ylabel("Bandwidth [bps]")
    ax2.set_title("EFFECTIVE BANDWIDTH vs DISTANCE")
    ax2.legend(fontsize=6)

    # 3. Message delay timeline
    ax3 = axes[2]
    d_plot  = np.linspace(1, 100, 200)
    lag_min = d_plot * AU / C_SI / 60
    ax3.plot(d_plot, lag_min, color="#CE93D8", lw=1.3)
    ax3.fill_between(d_plot, lag_min, 0, alpha=0.12, color="#CE93D8")
    ax3.axvline(distance_AU, color="#E8C46A", lw=0.9, ls="--",
                label=f"Current {comms.signal_lag_formatted(distance_AU)}")
    ax3.axhline(60, color="#FFB74D", lw=0.6, ls=":", label="60 min")
    ax3.axhline(10, color="#81C784", lw=0.6, ls=":", label="10 min")
    ax3.set_xlabel("Distance [AU]"); ax3.set_ylabel("One-way signal delay [min]")
    ax3.set_title("COMMUNICATION SIGNAL DELAY")
    ax3.legend(fontsize=6)

    plt.tight_layout()
    return fig


def _plot_tars_decisions(tars: AIRobot) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor("#04080e")

    # Decision log table / bar
    ax1 = axes[0]
    if tars.decision_log:
        confs = [d["confidence"] for d in tars.decision_log]
        x_pos = range(len(confs))
        cols  = ["#81C784" if c>0.8 else "#FFB74D" if c>0.6 else "#EF5350"
                 for c in confs]
        ax1.bar(x_pos, confs, color=cols, alpha=0.85, width=0.7)
        ax1.axhline(0.8, color="#E8C46A", lw=0.7, ls="--",
                    label="0.8 confidence")
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels([f"D{i}" for i in x_pos], fontsize=6)
        ax1.set_xlabel("Decision index"); ax1.set_ylabel("Confidence")
        ax1.set_ylim(0, 1.05)
        ax1.set_title(f"TARS DECISION CONFIDENCE LOG\n"
                      f"{len(tars.decision_log)} decisions  "
                      f"Honesty: {tars.honesty*100:.0f}%")
        ax1.legend(fontsize=6)

    # Personality sensitivity
    ax2 = axes[1]
    params  = ["Humour","Honesty","Courage","Optimism","Opacity"]
    default = [TARS_DEFAULT_HUMOUR, TARS_DEFAULT_HONESTY, TARS_DEFAULT_COURAGE,
               TARS_DEFAULT_OPTIMISM, TARS_DEFAULT_OPACITY]
    current = [tars.humour, tars.honesty, tars.courage, tars.optimism, tars.opacity]
    x_pos   = np.arange(len(params))
    w       = 0.35
    ax2.bar(x_pos - w/2, default, w, color="#303860", alpha=0.8, label="Default")
    ax2.bar(x_pos + w/2, current, w, color="#E8C46A", alpha=0.85, label="Current")
    ax2.set_xticks(x_pos); ax2.set_xticklabels(params, fontsize=7)
    ax2.set_ylim(0, 1.1); ax2.set_ylabel("Setting [0–1]")
    ax2.set_title(f"TARS PERSONALITY MATRIX\n(Default vs Current Settings)")
    ax2.legend(fontsize=6)

    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# §14  MAIN STREAMLIT PAGE
# ══════════════════════════════════════════════════════════════════════════════
def crew_telemetry_page():
    init_session_state()
    _mpl()
    S = st.session_state

    st.markdown("""
    <div style="border-left:3px solid #81C784;padding:.55rem 1.2rem;
                margin-bottom:1.2rem;background:rgba(129,199,132,0.03);
                font-family:monospace;">
    <div style="color:#81C784;font-size:.95rem;letter-spacing:.12em;font-weight:600;">
    ⬡ CREW TELEMETRY &amp; ENDURANCE SHIP SYSTEMS</div>
    <div style="color:#5a6a90;font-size:.62rem;margin-top:.2rem;">
    Cooper · Brand · Romilly · Doyle  ·  TARS/CASE AI  ·  Life Support  ·
    Propulsion  ·  Power  ·  Cryosleep  ·  Communications
    </div></div>""", unsafe_allow_html=True)

    (tab_crew, tab_physio, tab_tars,
     tab_ship, tab_cryo,
     tab_comms, tab_mission) = st.tabs([
        "👥 CREW VITALS",
        "🩺 PHYSIOLOGY",
        "🤖 TARS/CASE AI",
        "🛸 SHIP SYSTEMS",
        "❄️ CRYOSLEEP",
        "📡 COMMUNICATIONS",
        "⏱ MISSION CONTROL",
    ])

    crew_reg  = S["crew_registry"]
    tars_bot  = S["tars"]
    case_bot  = S["case"]
    ship      = S["endurance"]
    cryo_mgr  = S["cryo_mgr"]
    comms     = S["comms"]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1 — CREW VITALS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_crew:
        # KPI cards per crew
        crew_list = list(crew_reg.values())
        cols = st.columns(len(crew_list))
        for col, crew in zip(cols, crew_list):
            v   = crew.vital_signs_noisy()
            hs  = crew.health_score()
            al  = crew.alert_level()
            clr = CREW_COLORS.get(crew.crew_id, "#E8C46A")
            al_c= {"GREEN":"#81C784","YELLOW":"#FFD700","ORANGE":"#FF8800",
                   "RED":"#EF5350","CRITICAL":"#CE93D8"}.get(al.name,"#888")
            col.markdown(
                f'<div style="background:rgba(6,10,20,.92);border:1px solid {clr}55;'
                f'border-top:2px solid {clr};padding:.6rem;border-radius:3px;'
                f'font-family:monospace;">'
                f'<div style="color:{clr};font-size:.70rem;font-weight:600;">'
                f'{crew.crew_id.value.split()[0].upper()}</div>'
                f'<div style="color:#888;font-size:.52rem;">{crew.role[:22]}</div>'
                f'<div style="color:{al_c};font-size:.62rem;margin:.2rem 0;">◆ {al.name}</div>'
                f'<div style="color:#aaa;font-size:.55rem;">HR: {v["HR (bpm)"]:.0f} bpm</div>'
                f'<div style="color:#aaa;font-size:.55rem;">SpO₂: {v["SpO₂ (%)"]:.1f}%</div>'
                f'<div style="color:#aaa;font-size:.55rem;">Temp: {v["Temp (°C)"]:.1f}°C</div>'
                f'<div style="color:#aaa;font-size:.55rem;">Morale: {crew.morale*100:.0f}%</div>'
                f'<div style="color:{clr};font-size:.60rem;">Health: {hs:.3f}</div>'
                f'</div>', unsafe_allow_html=True)

        st.markdown("---")
        fig = _plot_crew_vitals(crew_reg)
        st.pyplot(fig, use_container_width=True); plt.close(fig)

        # Summary table
        rows = [c.to_summary_dict() for c in crew_reg.values()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — PHYSIOLOGY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_physio:
        c1, c2 = st.columns([1, 3])
        with c1:
            sel_name = st.selectbox("Select crew member",
                                     [c.crew_id.name for c in crew_reg.values()])
            sel_days = st.slider("Mission duration (days)", 30, 1000, 700, 10)
            ex_hrs   = st.slider("Exercise hours/day", 0.0, 4.0, 1.0, 0.25)
            sel_crew = crew_reg[CrewID[sel_name]]
            if st.button("🩺 COMPUTE PHYSIOLOGY PROFILE",
                         use_container_width=True, type="primary"):
                physio = PhysiologySimulator(fs=1.0)
                df_ph  = physio.physiological_profile(sel_crew, days=sel_days)
                S["physio_profile"] = (df_ph, sel_crew.crew_id.value)
            # ECG live
            if st.button("ECG WAVEFORM", use_container_width=True):
                physio = PhysiologySimulator(fs=500.0)
                t_ecg, ecg = physio.ecg_waveform(sel_crew.hr_bpm, 8.0)
                S["ecg_waveform"] = (t_ecg, ecg, sel_crew.hr_bpm)

        with c2:
            if S.get("ecg_waveform"):
                t_ecg, ecg, hr = S["ecg_waveform"]
                _mpl()
                fig_ecg, ax_ecg = plt.subplots(figsize=(11, 3))
                ax_ecg.plot(t_ecg, ecg, color="#E8C46A", lw=0.7)
                ax_ecg.set_xlabel("Time [s]"); ax_ecg.set_ylabel("ECG [mV]")
                ax_ecg.set_title(f"ECG WAVEFORM — {sel_name}  HR={hr:.0f} bpm")
                ax_ecg.set_facecolor("#030508")
                fig_ecg.patch.set_facecolor("#04080e")
                st.pyplot(fig_ecg, use_container_width=True); plt.close(fig_ecg)

            if S.get("physio_profile"):
                df_ph, crw_name = S["physio_profile"]
                fig_ph = _plot_physiological_profile(df_ph, crw_name)
                st.pyplot(fig_ph, use_container_width=True); plt.close(fig_ph)
                with st.expander("Physiology Data Table"):
                    st.dataframe(df_ph.round(3), use_container_width=True, hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — TARS/CASE AI
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_tars:
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#E8C46A;">[ TARS SETTINGS ]</div>',
                        unsafe_allow_html=True)
            t_h = st.slider("TARS Humour",   0.0, 1.0, float(S["tars_humour"]),  0.01)
            t_e = st.slider("TARS Honesty",  0.0, 1.0, float(S["tars_honesty"]), 0.01)
            t_c = st.slider("TARS Courage",  0.0, 1.0, float(S["tars_courage"]), 0.01)
            t_o = st.slider("TARS Optimism", 0.0, 1.0, float(S["tars_optimism"]),0.01)
            t_op= st.slider("TARS Opacity",  0.0, 1.0, float(S["tars_opacity"]), 0.01)
            S["tars_humour"]=t_h; S["tars_honesty"]=t_e
            S["tars_courage"]=t_c; S["tars_optimism"]=t_o; S["tars_opacity"]=t_op
            tars_bot.humour=t_h; tars_bot.honesty=t_e
            tars_bot.courage=t_c; tars_bot.optimism=t_o; tars_bot.opacity=t_op
            context = st.selectbox("Context", list(TARS_DIALOGUE_BANK.keys()))
            if st.button("🤖 GENERATE TARS DIALOGUE", use_container_width=True):
                tars_bot.mission_log.append(tars_bot.generate_dialogue(context))

        with c2:
            st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#4FC3F7;">[ CASE SETTINGS ]</div>',
                        unsafe_allow_html=True)
            c_h = st.slider("CASE Humour",  0.0, 1.0, float(S["case_humour"]),  0.01)
            c_e = st.slider("CASE Honesty", 0.0, 1.0, float(S["case_honesty"]), 0.01)
            S["case_humour"]=c_h; S["case_honesty"]=c_e
            case_bot.humour=c_h; case_bot.honesty=c_e
            if st.button("🤖 GENERATE CASE DIALOGUE", use_container_width=True):
                case_bot.mission_log.append(case_bot.generate_dialogue("default"))
            st.markdown('<div style="font-family:monospace;font-size:.60rem;color:#4FC3F7;margin-top:.6rem;">CASE LOG</div>',
                        unsafe_allow_html=True)
            for line in case_bot.mission_log[-8:]:
                st.markdown(f'<div style="font-family:monospace;font-size:.56rem;color:#888;border-left:2px solid #4FC3F780;padding:.15rem .4rem;">{line}</div>',
                            unsafe_allow_html=True)

        with c3:
            fig_t = _plot_tars_panel(tars_bot, case_bot)
            st.pyplot(fig_t, use_container_width=True); plt.close(fig_t)
            st.markdown('<div style="font-family:monospace;font-size:.60rem;color:#E8C46A;margin-top:.5rem;">TARS DIALOGUE LOG</div>',
                        unsafe_allow_html=True)
            for line in tars_bot.mission_log[-10:]:
                st.markdown(f'<div style="font-family:monospace;font-size:.57rem;color:#aaa;border-left:2px solid #E8C46A80;padding:.15rem .4rem;">{line}</div>',
                            unsafe_allow_html=True)

        fig_td = _plot_tars_decisions(tars_bot)
        st.pyplot(fig_td, use_container_width=True); plt.close(fig_td)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 4 — SHIP SYSTEMS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_ship:
        c1, c2 = st.columns([1, 3])
        with c1:
            dv_burn = st.number_input("Execute burn Δv [m/s]",
                                       value=100.0, format="%.1f")
            tidal   = st.slider("Apply tidal stress [g/m]", 0.0, 10.0, 0.0, 0.1)
            adv_d   = st.slider("Advance mission [days]", 0.0, 100.0,
                                 float(S["advance_days"]), 0.5)
            S["advance_days"] = adv_d

            if st.button("🔥 EXECUTE BURN", use_container_width=True):
                result = ship.propulsion.burn(dv_burn)
                st.success(f"Burn complete: Δv={result['dv_executed_ms']:.1f}m/s  "
                           f"Prop={result['propellant_kg']:.0f}kg used")

            if st.button("⚡ APPLY TIDAL STRESS", use_container_width=True):
                ship.apply_tidal_stress(tidal)
                st.warning(f"Tidal event: {tidal:.2f} g/m applied")

            if st.button("⏩ ADVANCE MISSION", use_container_width=True, type="primary"):
                ship.advance_mission(adv_d)
                st.success(f"Advanced {adv_d:.1f} days")

            fs = ship.full_status()
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c0e0;
                        background:rgba(6,10,20,.92);padding:.65rem;
                        border:1px solid rgba(129,199,132,.18);border-radius:3px;
                        line-height:2.0;margin-top:.4rem;">
            Mission day: <b style="color:#E8C46A;">{fs['mission_day']}</b><br>
            Hull integrity: <b style="color:{'#81C784' if fs['hull_integrity_pct']>80 else '#EF5350'};">
            {fs['hull_integrity_pct']:.1f}%</b><br>
            Rotation: <b>{fs['rotation_rpm']} RPM → {fs['artificial_g']:.3f} g</b><br>
            Modules nominal: <b style="color:#81C784;">{fs['modules_nominal']}</b><br>
            Modules degraded: <b style="color:#FFB74D;">{fs['modules_degraded']}</b><br>
            Modules critical: <b style="color:#EF5350;">{fs['modules_critical']}</b><br>
            Micromet impacts: <b>{fs['micromet_impacts']}</b><br>
            Tidal events: <b>{fs['tidal_events']}</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            fig_s = _plot_endurance_systems(ship)
            st.pyplot(fig_s, use_container_width=True); plt.close(fig_s)

        # Data tables
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div style="font-family:monospace;font-size:.60rem;color:#81C784;">PROPULSION</div>',
                        unsafe_allow_html=True)
            st.dataframe(pd.DataFrame([ship.propulsion.status_dict()]).T.rename(
                columns={0:"Value"}), use_container_width=True)
        with c4:
            st.markdown('<div style="font-family:monospace;font-size:.60rem;color:#81C784;">LIFE SUPPORT</div>',
                        unsafe_allow_html=True)
            st.dataframe(pd.DataFrame([ship.life_support.status_dict()]).T.rename(
                columns={0:"Value"}), use_container_width=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 5 — CRYOSLEEP
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_cryo:
        c1, c2 = st.columns([1, 2])
        with c1:
            cryo_crew = st.selectbox("Crew member",
                                      [c.value for c in CrewID if c not in (CrewID.TARS,CrewID.CASE)])
            pod_id    = st.number_input("Pod ID (0–5)", 0, 5, 0)
            emergency_rv = st.checkbox("Emergency revival (45min, cardiac risk)")
            if st.button("❄️ INITIATE CRYOSLEEP", use_container_width=True):
                cid = next(c for c in CrewID if c.value == cryo_crew)
                msg = cryo_mgr.put_to_sleep(cid, int(pod_id))
                st.success(msg)
            if st.button("⚡ REVIVE CREW", use_container_width=True):
                cid   = next(c for c in CrewID if c.value == cryo_crew)
                steps = cryo_mgr.revive(cid, emergency_rv)
                for s in steps:
                    st.markdown(f'<div style="font-family:monospace;font-size:.60rem;'
                                f'color:#4FC3F7;">{s}</div>', unsafe_allow_html=True)

        with c2:
            fig_c = _plot_cryosleep(cryo_mgr)
            st.pyplot(fig_c, use_container_width=True); plt.close(fig_c)
            st.dataframe(cryo_mgr.pods_status(),
                         use_container_width=True, hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 6 — COMMUNICATIONS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_comms:
        c1, c2 = st.columns([1, 3])
        with c1:
            dist_AU = st.slider("Distance from Earth [AU]", 0.1, 1e4,
                                 float(S["comms_distance"]), 0.1, format="%.1f")
            band    = st.selectbox("DSN Band", list(comms.DSN_BANDS.keys()), index=2)
            comms.distance_AU = dist_AU; comms.band = band
            S["comms_distance"] = dist_AU
            msg_txt = st.text_area("Compose message", value=S["comms_msg"], height=80)
            S["comms_msg"] = msg_txt
            if st.button("📡 SEND MESSAGE", use_container_width=True, type="primary"):
                m = comms.send(msg_txt)
                st.success(f"Queued — Delivery lag: {comms.signal_lag_formatted(dist_AU)}")

            lag_s = comms.signal_lag_s(dist_AU)
            bw    = comms.bandwidth_bps()
            sig_d = comms.signal_strength_dBm(dist_AU)
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c0e0;
                        background:rgba(6,10,20,.92);padding:.65rem;
                        border:1px solid rgba(206,147,216,.18);border-radius:3px;
                        line-height:2.0;">
            One-way lag: <b style="color:#CE93D8;">{comms.signal_lag_formatted(dist_AU)}</b><br>
            Round-trip: <b>{comms.signal_lag_formatted(dist_AU*2)}</b><br>
            Bandwidth: <b>{bw:.2f} bps</b><br>
            Signal: <b style="color:{'#81C784' if sig_d>-120 else '#EF5350'};">{sig_d:.1f} dBm</b><br>
            Wormhole relay: <b>{'YES' if comms.wormhole_relay else 'NO'}</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            fig_cm = _plot_comms(comms, dist_AU)
            st.pyplot(fig_cm, use_container_width=True); plt.close(fig_cm)
            inbox_df, outbox_df = comms.message_queue_df()
            st.markdown('<div style="font-family:monospace;font-size:.60rem;color:#CE93D8;">📥 INBOX</div>',
                        unsafe_allow_html=True)
            if not inbox_df.empty:
                st.dataframe(inbox_df, use_container_width=True, hide_index=True)
            st.markdown('<div style="font-family:monospace;font-size:.60rem;color:#4FC3F7;">📤 OUTBOX</div>',
                        unsafe_allow_html=True)
            if not outbox_df.empty:
                st.dataframe(outbox_df, use_container_width=True, hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 7 — MISSION CONTROL (master view)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_mission:
        phase = st.selectbox("Current Mission Phase",
                              [mp.value for mp in MissionPhase],
                              index=list(MissionPhase).index(S["mission_phase"]))
        S["mission_phase"] = next(mp for mp in MissionPhase if mp.value==phase)

        cols_kpi = st.columns(6)
        kpis = [
            ("Mission Day",     f"{ship.mission_elapsed_days:.0f}",       "#E8C46A"),
            ("Hull Integrity",  f"{ship.hull_integrity_pct:.1f}%",        "#81C784"),
            ("Fuel Left",       f"{ship.propulsion.fuel_kg_remaining/1e3:.0f}t", "#FF8800"),
            ("Δv Remaining",    f"{ship.propulsion.dv_remaining_ms/1e3:.1f}km/s","#4FC3F7"),
            ("Active Crew",     f"{ship.life_support.active_crew}",       "#81C784"),
            ("Signal Lag",      comms.signal_lag_formatted(),              "#CE93D8"),
        ]
        for col, (lbl, val, clr) in zip(cols_kpi, kpis):
            col.markdown(
                f'<div style="background:rgba(6,10,20,.9);border:1px solid {clr}44;'
                f'padding:.4rem;text-align:center;border-radius:2px;font-family:monospace;">'
                f'<div style="color:#444;font-size:.50rem;">{lbl}</div>'
                f'<div style="color:{clr};font-size:.82rem;">{val}</div></div>',
                unsafe_allow_html=True)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div style="font-family:monospace;font-size:.60rem;color:#81C784;">CREW STATUS SUMMARY</div>',
                        unsafe_allow_html=True)
            rows = [c.to_summary_dict() for c in crew_reg.values()]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        with col_b:
            st.markdown('<div style="font-family:monospace;font-size:.60rem;color:#81C784;">SYSTEMS STATUS</div>',
                        unsafe_allow_html=True)
            sys_rows = [
                {"System":"Life Support", **ship.life_support.status_dict()},
            ]
            ls_d = ship.life_support.status_dict()
            pw_d = ship.power.status_dict()
            pr_d = ship.propulsion.status_dict()
            combined = pd.DataFrame([
                {"System": "Life Support", "Status": ls_d["CO₂ alert"],
                 "Key metric": f"CO₂={ls_d['CO₂ (ppm)']:.0f}ppm"},
                {"System": "Power",        "Status": pw_d["Power status"],
                 "Key metric": f"Margin={pw_d['Power margin (kW)']:.1f}kW"},
                {"System": "Propulsion",   "Status": pr_d["Engine status"],
                 "Key metric": f"Fuel={pr_d['Fuel remaining (%)']:.1f}%"},
                {"System": "Hull",         "Status": SystemStatus.NOMINAL.value if ship.hull_integrity_pct>80 else "DEGRADED",
                 "Key metric": f"{ship.hull_integrity_pct:.1f}% integrity"},
            ])
            st.dataframe(combined, use_container_width=True, hide_index=True)

        if ship.alert_log:
            st.markdown('<div style="font-family:monospace;font-size:.60rem;color:#EF5350;margin-top:.5rem;">ALERT LOG</div>',
                        unsafe_allow_html=True)
            for alert in ship.alert_log[-5:]:
                st.markdown(
                    f'<div style="font-family:monospace;font-size:.57rem;color:#EF5350;'
                    f'border-left:2px solid #EF5350;padding:.15rem .4rem;">'
                    f'Day {alert["day"]:.0f}: {alert["message"]}</div>',
                    unsafe_allow_html=True)
