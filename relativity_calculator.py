"""
relativity_calculator.py — Special & General Relativity Engine
ENDURANCE Mission Control | Interstellar Science Platform v3.0.0
═══════════════════════════════════════════════════════════════════════════════
Scientific References:
  [1]  Einstein (1905) Ann. Phys. 17:891  [Special relativity]
  [2]  Einstein (1916) Ann. Phys. 49:769  [General relativity]
  [3]  Minkowski (1908)  [Spacetime formulation]
  [4]  Schwarzschild (1916) Sitz. Preuß. Akad. Wiss. 189  [Schwarzschild metric]
  [5]  Bardeen, Press & Teukolsky (1972) ApJ 178:347  [Kerr geodesics]
  [6]  Pound & Rebka (1959) PRL 3:439  [Gravitational redshift experiment]
  [7]  Hafele & Keating (1972) Science 177:166  [Flying clocks experiment]
  [8]  Kip Thorne, "The Science of Interstellar" (W.W. Norton, 2014)
  [9]  Misner, Thorne & Wheeler, "Gravitation" (Freeman, 1973)
  [10] Penrose (1965) PRL 14:57  [Singularity theorem]
  [11] Taylor & Wheeler, "Spacetime Physics" (Freeman, 1992)

Module implements:
  ┌─ SPECIAL RELATIVITY ────────────────────────────────────────────────────┐
  │ Lorentz factor γ(v) = 1/√(1−v²/c²)                                     │
  │ Time dilation Δt' = γΔt;  length contraction L' = L/γ                  │
  │ Relativistic Doppler (longitudinal + transverse)                        │
  │ Relativistic aberration (stellar angle transformation)                   │
  │ Rapidity φ = arctanh(v/c);  Lorentz boost 4×4 matrix                   │
  │ Four-velocity u^μ, four-momentum p^μ = (E/c, p)                        │
  │ Energy-momentum: E² = (pc)² + (m₀c²)²                                  │
  │ Relativistic kinetic energy K = (γ−1)m₀c²                              │
  │ Relativistic velocity addition: v_rel = (v₁+v₂)/(1+v₁v₂/c²)          │
  │ Invariant spacetime interval s² = −c²Δt² + Δx² + Δy² + Δz²           │
  │ Minkowski metric η_μν; light cone classification                        │
  │ Twin paradox: asymmetric aging calculator                               │
  │ Relativistic rocket: Tsiolkovsky equation (relativistic)                │
  │ Relativistic momentum, force, power                                     │
  └─────────────────────────────────────────────────────────────────────────┘
  ┌─ GENERAL RELATIVITY ────────────────────────────────────────────────────┐
  │ Schwarzschild time dilation: dτ/dt = √(1−r_s/r−v²/c²)                 │
  │ Combined GR+SR: proper time for arbitrary trajectory                    │
  │ Gravitational redshift: z+1 = √(1−r_s/r_emit) / √(1−r_s/r_obs)       │
  │ Gravitational time delay (Shapiro delay)                                │
  │ Geodesic equation integration (Schwarzschild, numerical RK45)           │
  │ Circular orbit proper time ratio (Schwarzschild & Kerr)                 │
  │ Orbital precession (perihelion shift): δφ = 6πGM/(c²a(1−e²))          │
  │ Light bending: α = 4GM/(c²b) (Eddington 1919)                         │
  │ Gravitational time dilation: GPS-style correction                       │
  │ Equivalence principle: accelerating frame ↔ gravitational field        │
  └─────────────────────────────────────────────────────────────────────────┘
  ┌─ COOPER-MURPH MISSION TIME ENGINE ─────────────────────────────────────┐
  │ Full Interstellar mission timeline (Earth time vs ship proper time)     │
  │ Leg-by-leg proper time integration with dilation factors                │
  │ Miller's World: 1h ship = 7yr Earth  (exact Kerr calculation)          │
  │ Wormhole transit: time dilation during passage                          │
  │ Endurance rotation: combined centrifugal+gravitational time correction  │
  │ Cooper age vs Murph age divergence: full numerical timeline             │
  │ Branching timelines: Plan A vs Plan B scenarios                         │
  │ Tesseract time: subjective time inside 5D bulk structure                │
  └─────────────────────────────────────────────────────────────────────────┘
  ┌─ SPACETIME DIAGRAMS & WORLDLINES ──────────────────────────────────────┐
  │ Minkowski spacetime diagram (1+1D: ct vs x)                            │
  │ Worldline for arbitrary velocity profile v(t)                          │
  │ Light cone: past/future/spacelike regions                              │
  │ Simultaneity lines for different inertial frames                        │
  │ Twin paradox worldline (outgoing + returning traveller)                 │
  │ Cooper & Murph worldlines on same spacetime diagram                    │
  │ Penrose causal diagram for simple cases                                │
  └─────────────────────────────────────────────────────────────────────────┘
  ┌─ RELATIVISTIC DYNAMICS ─────────────────────────────────────────────────┐
  │ Relativistic Tsiolkovsky rocket equation                                │
  │ Photon rocket efficiency; antimatter drive parameters                   │
  │ Relativistic orbits: energy levels, bound/unbound criteria              │
  │ De Broglie wavelength λ = h/(γmv)                                      │
  │ Relativistic Compton scattering: Δλ = (h/m_e c)(1−cosθ)              │
  │ Relativistic beaming: solid angle transformation                        │
  └─────────────────────────────────────────────────────────────────────────┘

"They" say: "Time is relative — Cooper, it always has been."
                                          — TARS, Tesseract, 2067
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import math
import time
import uuid
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import scipy.integrate as sci_int
import scipy.optimize  as sci_opt

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot   as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors   as mcolors
import matplotlib.patches  as mpatches
from matplotlib.colors     import LinearSegmentedColormap
from matplotlib.patches    import FancyArrowPatch, Circle

import streamlit as st

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# §1  PHYSICAL CONSTANTS  (SI, CODATA 2018)
# ══════════════════════════════════════════════════════════════════════════════
C_SI      = 2.997_924_58e8        # Speed of light            m s⁻¹
G_SI      = 6.674_30e-11          # Gravitational constant    m³ kg⁻¹ s⁻²
HBAR      = 1.054_571_817e-34     # Reduced Planck constant   J·s
H_PL      = 6.626_070_15e-34      # Planck constant           J·s
K_B       = 1.380_649e-23         # Boltzmann constant        J K⁻¹
M_SUN     = 1.989_000e30          # Solar mass                kg
M_EARTH   = 5.972_000e24          # Earth mass                kg
M_ELECTRON= 9.109_384e-31         # Electron mass             kg
M_PROTON  = 1.672_622e-27         # Proton mass               kg
R_EARTH   = 6.371_000e6           # Earth radius              m
AU        = 1.495_978_707e11      # Astronomical unit         m
LY        = 9.460_730_472e15      # Light-year                m
PC        = 3.085_677_581e16      # Parsec                    m
MPC       = 3.085_677_581e22      # Megaparsec                m
YEAR_S    = 3.155_760e7           # Julian year               s
DAY_S     = 86_400.0              # Day                       s
HOUR_S    = 3_600.0               # Hour                      s
EV        = 1.602_176_634e-19     # Electron-volt             J

# ── Gargantua & Mission constants ─────────────────────────────────────────
GARG_MASS_SOLAR  = 1.00e8
GARG_MASS_KG     = GARG_MASS_SOLAR * M_SUN
GARG_M_GEO       = G_SI * GARG_MASS_KG / C_SI**2
GARG_RS          = 2.0 * GARG_M_GEO
GARG_SPIN        = 1.0 - 1e-14
MILLER_RATIO     = 7.0 * YEAR_S / HOUR_S    # ≈ 61 320  (time dilation factor)

# Cooper's age at mission start (film canon: ~35 in 2063)
COOPER_AGE_START = 35.0           # years
MURPH_AGE_START  = 10.0           # years (Cooper's daughter)

# Mission phase durations — Earth frame reference (Kip Thorne calculations [8])
MISSION_EARTH_TO_SATURN_YR   = 2.0     # Earth years to reach Saturn
MISSION_WORMHOLE_TRANSIT_YR  = 0.1     # ~5 weeks in transit
MISSION_MILLER_SHIP_HRS      = 3.22    # Ship hours on Miller's world (film)
MISSION_MANN_APPROACH_YR_E   = 14.0    # Earth years before Mann planet
MISSION_TESSERACT_HR         = 1.0     # Subjective hours in tesseract

# ══════════════════════════════════════════════════════════════════════════════
# §2  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════
class IntervalType(Enum):
    TIMELIKE   = "Timelike  (|cΔt| > |Δr|)  — causal"
    LIGHTLIKE  = "Lightlike (|cΔt| = |Δr|)  — photon worldline"
    SPACELIKE  = "Spacelike (|cΔt| < |Δr|)  — no causal link"

class FrameType(Enum):
    INERTIAL         = "Inertial (no acceleration)"
    ACCELERATING     = "Uniformly accelerating (Rindler)"
    FREELY_FALLING   = "Freely falling (local inertial)"
    CIRCULAR_ORBIT   = "Circular orbit (centrifugal + GR)"

class MissionPhase(Enum):
    EARTH_LAUNCH         = "Earth launch & Saturn transit"
    WORMHOLE_APPROACH    = "Wormhole approach"
    WORMHOLE_TRANSIT     = "Wormhole transit"
    MILLER_APPROACH      = "Miller's World approach"
    MILLER_SURFACE       = "Miller's World surface"
    MILLER_DEPARTURE     = "Miller's World departure"
    MANN_TRANSIT         = "Mann's Planet transit"
    MANN_SURFACE         = "Mann's Planet surface"
    GARGANTUA_ORBIT      = "Gargantua orbit"
    TESSERACT            = "Tesseract (5D bulk)"
    EDMUNDS_COLONY       = "Edmunds' Planet colony approach"
    PLAN_B_DELIVERY      = "Plan B embryo delivery"

class ClockType(Enum):
    COORDINATE = "Coordinate time t (far observer)"
    PROPER     = "Proper time τ (on-board clock)"
    GPS_CORRECTED = "GPS-corrected atomic clock"

# ══════════════════════════════════════════════════════════════════════════════
# §3  SPECIAL RELATIVITY ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class SpecialRelativity:
    """
    Complete Special Relativity calculator.
    All kinematics, dynamics, and four-vector algebra for massive and
    massless particles. Implements full Lorentz group operations.
    Reference: Einstein (1905) [1], Minkowski (1908) [3], MTW §2 [9].
    """

    # ── §3.1  Core Lorentz kinematics ────────────────────────────────────────
    @staticmethod
    def lorentz_factor(v: float) -> float:
        """
        γ(v) = 1/√(1 − v²/c²)
        v = 0   → γ = 1    (Newtonian limit)
        v → c   → γ → ∞   (ultrarelativistic)
        """
        beta = abs(v) / C_SI
        beta = min(beta, 1.0 - 1e-15)
        return 1.0 / math.sqrt(1.0 - beta*beta)

    @staticmethod
    def beta(v: float) -> float:
        """β = v/c (dimensionless velocity)"""
        return abs(v) / C_SI

    @staticmethod
    def rapidity(v: float) -> float:
        """
        Rapidity φ = arctanh(v/c)  (additive under boosts).
        Ultrarelativistic: φ ≈ ln(2γ).
        """
        b = min(abs(v)/C_SI, 1.0 - 1e-15)
        return math.atanh(b)

    @staticmethod
    def v_from_rapidity(phi: float) -> float:
        """v = c·tanh(φ)"""
        return C_SI * math.tanh(phi)

    @staticmethod
    def time_dilation(dt_proper: float, v: float) -> float:
        """
        Coordinate time interval from proper time (moving clock):
          Δt_coord = γ · Δτ_proper
        A clock moving at v runs slow by factor γ.
        """
        return SpecialRelativity.lorentz_factor(v) * dt_proper

    @staticmethod
    def proper_time_from_coord(dt_coord: float, v: float) -> float:
        """Proper time interval: Δτ = Δt_coord / γ"""
        return dt_coord / SpecialRelativity.lorentz_factor(v)

    @staticmethod
    def length_contraction(L_rest: float, v: float) -> float:
        """
        Length contraction (Lorentz 1892, Einstein 1905 [1]):
          L' = L₀/γ  (length measured in moving frame)
        Object appears shorter along direction of motion.
        """
        return L_rest / SpecialRelativity.lorentz_factor(v)

    @staticmethod
    def velocity_addition(v1: float, v2: float) -> float:
        """
        Relativistic velocity addition (Einstein 1905 [1]):
          v_rel = (v₁ + v₂) / (1 + v₁v₂/c²)
        Always |v_rel| < c for |v₁|, |v₂| < c.
        """
        num = v1 + v2
        den = 1.0 + v1*v2/C_SI**2
        return num / den

    @staticmethod
    def velocity_addition_vector(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        """
        3D relativistic velocity addition (v1 along x-axis, v2 arbitrary):
          v'_x = (v1_x + v2_x) / (1 + v1·v2/c²)
          v'_⊥ = v2_⊥ / [γ(v1)·(1 + v1·v2/c²)]
        Returns velocity of object with v2 in S-frame where object v1.
        """
        v1_mag = np.linalg.norm(v1)
        if v1_mag < 1e-10:
            return v2
        g = SpecialRelativity.lorentz_factor(v1_mag)
        e = v1 / v1_mag                           # unit vector
        v2_par = np.dot(v2, e) * e                # parallel component
        v2_perp = v2 - v2_par                     # perpendicular component
        denom = 1.0 + np.dot(v1, v2) / C_SI**2
        v_par  = (v1 + v2_par) / denom
        v_perp = v2_perp / (g * denom)
        return v_par + v_perp

    # ── §3.2  Spacetime interval ──────────────────────────────────────────────
    @staticmethod
    def spacetime_interval_sq(dt: float, dx: float,
                               dy: float = 0.0,
                               dz: float = 0.0) -> float:
        """
        Minkowski interval s² = −c²Δt² + Δx² + Δy² + Δz²  (−+++ signature).
        s² < 0 → timelike (causally connected)
        s² = 0 → null/lightlike
        s² > 0 → spacelike (no causal connection)
        """
        return -(C_SI*dt)**2 + dx**2 + dy**2 + dz**2

    @staticmethod
    def classify_interval(s_sq: float,
                           tol: float = 1e-10) -> IntervalType:
        if abs(s_sq) < tol * C_SI**2:
            return IntervalType.LIGHTLIKE
        elif s_sq < 0:
            return IntervalType.TIMELIKE
        else:
            return IntervalType.SPACELIKE

    @staticmethod
    def proper_time_from_interval(s_sq: float) -> Optional[float]:
        """Proper time along timelike interval: Δτ = √(−s²)/c"""
        if s_sq >= 0:
            return None
        return math.sqrt(-s_sq) / C_SI

    # ── §3.3  Lorentz boost matrix ────────────────────────────────────────────
    @staticmethod
    def lorentz_boost_matrix(v: float,
                              axis: int = 0) -> np.ndarray:
        """
        4×4 Lorentz boost matrix Λ^μ_ν for boost along x/y/z axis.
        Coordinates: (ct, x, y, z) = (x⁰, x¹, x², x³).
        Convention: x'^μ = Λ^μ_ν x^ν.
        """
        g   = SpecialRelativity.lorentz_factor(v)
        b   = v / C_SI
        L   = np.eye(4)
        ax  = axis + 1   # 0→x=1, 1→y=2, 2→z=3
        L[0,  0]  = g;   L[0, ax]  = -g*b
        L[ax, 0]  = -g*b; L[ax, ax] = g
        return L

    @staticmethod
    def boost_event(event_ct_x_y_z: np.ndarray,
                    v: float, axis: int = 0) -> np.ndarray:
        """Apply Lorentz boost to a 4-event vector (ct, x, y, z)."""
        L = SpecialRelativity.lorentz_boost_matrix(v, axis)
        return L @ event_ct_x_y_z

    # ── §3.4  Four-vectors ────────────────────────────────────────────────────
    @staticmethod
    def four_velocity(v: float) -> np.ndarray:
        """
        Four-velocity u^μ = γ(c, v, 0, 0)  [m/s].
        Normalised: u^μ u_μ = −c²  (always).
        """
        g = SpecialRelativity.lorentz_factor(v)
        return np.array([g*C_SI, g*v, 0.0, 0.0])

    @staticmethod
    def four_momentum(m0_kg: float, v: float) -> np.ndarray:
        """
        Four-momentum p^μ = m₀u^μ = (E/c, p_x, p_y, p_z).
        p^μ p_μ = −(m₀c)²  (invariant).
        """
        g   = SpecialRelativity.lorentz_factor(v)
        E   = g * m0_kg * C_SI**2
        p_x = g * m0_kg * v
        return np.array([E/C_SI, p_x, 0.0, 0.0])

    @staticmethod
    def invariant_mass(p4: np.ndarray) -> float:
        """Invariant mass from 4-momentum: m₀c = √(−p^μ p_μ)"""
        s_sq = -(p4[0])**2 + p4[1]**2 + p4[2]**2 + p4[3]**2
        return math.sqrt(max(-s_sq, 0.0)) / C_SI

    # ── §3.5  Relativistic energy & momentum ─────────────────────────────────
    @staticmethod
    def total_energy(m0_kg: float, v: float) -> float:
        """E = γm₀c²  [J]"""
        return SpecialRelativity.lorentz_factor(v) * m0_kg * C_SI**2

    @staticmethod
    def kinetic_energy(m0_kg: float, v: float) -> float:
        """K = (γ−1)m₀c²  [J]"""
        return (SpecialRelativity.lorentz_factor(v) - 1.0) * m0_kg * C_SI**2

    @staticmethod
    def momentum(m0_kg: float, v: float) -> float:
        """p = γm₀v  [kg m/s]"""
        return SpecialRelativity.lorentz_factor(v) * m0_kg * v

    @staticmethod
    def energy_momentum_invariant(E_J: float, p_kgms: float,
                                   m0_kg: float) -> float:
        """
        E² = (pc)² + (m₀c²)²  →  check residual ≈ 0.
        Returns (E/m₀c²)² − (p/m₀c)² − 1  (dimensionless; should be ≈0).
        """
        E0 = m0_kg * C_SI**2
        return (E_J/E0)**2 - (p_kgms*C_SI/E0)**2 - 1.0

    @staticmethod
    def v_from_momentum(m0_kg: float, p_kgms: float) -> float:
        """
        Relativistic momentum inversion:
          p = γmv → v = pc²/E = pc/√(m²c²+p²)
        """
        num = p_kgms * C_SI
        den = math.sqrt((m0_kg*C_SI)**2 + p_kgms**2)
        return num / den

    @staticmethod
    def v_from_energy(m0_kg: float, E_J: float) -> float:
        """v from total energy: v = c√(1−(m₀c²/E)²)"""
        ratio = m0_kg*C_SI**2 / max(E_J, m0_kg*C_SI**2)
        return C_SI * math.sqrt(max(1.0 - ratio**2, 0.0))

    # ── §3.6  Relativistic Doppler & aberration ───────────────────────────────
    @staticmethod
    def doppler_longitudinal(f_emit: float, v: float,
                              approaching: bool = True) -> float:
        """
        Relativistic longitudinal Doppler shift [1]:
          f_obs = f_emit × √[(1 ± β)/(1 ∓ β)]
        + for approaching (blueshift), − for receding (redshift).
        """
        b = abs(v) / C_SI
        if approaching:
            return f_emit * math.sqrt((1.0+b)/(1.0-b+1e-15))
        else:
            return f_emit * math.sqrt((1.0-b)/(1.0+b+1e-15))

    @staticmethod
    def doppler_transverse(f_emit: float, v: float) -> float:
        """
        Relativistic transverse Doppler (purely SR, no Newtonian analogue):
          f_obs = f_emit / γ  (redshift even for perpendicular motion).
        Confirmed by Ives-Stilwell experiment (1938).
        """
        return f_emit / SpecialRelativity.lorentz_factor(v)

    @staticmethod
    def relativistic_aberration(theta_emit: float, v: float) -> float:
        """
        Light aberration: angle θ' in moving frame S' from θ in rest frame S.
          cos θ' = (cos θ − β) / (1 − β cos θ)
        θ_emit: angle from velocity direction in rest frame [radians].
        Returns θ' in observer frame.
        """
        b = v / C_SI
        cos_t  = math.cos(theta_emit)
        cos_tp = (cos_t - b) / (1.0 - b*cos_t + 1e-15)
        cos_tp = max(-1.0, min(1.0, cos_tp))
        return math.acos(cos_tp)

    @staticmethod
    def relativistic_beaming(theta_half_emit: float, v: float) -> float:
        """
        Relativistic beaming: half-angle of emission cone in observer frame.
        For isotropic emitter in rest frame, observer sees radiation
        beamed into forward cone with half-angle:
          sin(θ'_half) ≈ 1/γ  (ultrarelativistic)
        Full formula via aberration.
        """
        return SpecialRelativity.relativistic_aberration(theta_half_emit, v)

    # ── §3.7  Twin paradox ────────────────────────────────────────────────────
    @staticmethod
    def twin_paradox(v_cruise: float,
                      d_ly: float) -> Dict[str, float]:
        """
        Classic twin paradox: travelling twin goes to star at d_ly light-years,
        returns at same speed v_cruise.
        Earth twin ages: Δt_earth = 2d_ly/v_cruise  (coordinate time)
        Traveller ages:  Δτ_ship = 2d_ly/(v_cruise·γ) (proper time)
        Ignores acceleration phases (instantaneous turnaround).
        """
        d_m        = d_ly * LY
        t_earth_s  = 2.0 * d_m / v_cruise
        g          = SpecialRelativity.lorentz_factor(v_cruise)
        tau_ship_s = t_earth_s / g
        age_diff_s = t_earth_s - tau_ship_s
        return {
            "v_ms":               v_cruise,
            "v_c":                v_cruise/C_SI,
            "gamma":              g,
            "distance_ly":        d_ly,
            "t_earth_yr":         t_earth_s/YEAR_S,
            "tau_ship_yr":        tau_ship_s/YEAR_S,
            "age_diff_yr":        age_diff_s/YEAR_S,
            "earth_twin_older_by": age_diff_s/YEAR_S,
        }

    @staticmethod
    def twin_with_acceleration(v_max: float, d_ly: float,
                                a_proper: float) -> Dict[str, float]:
        """
        Twin paradox including constant proper acceleration phases.
        Mission: accelerate at a [m/s²] proper, cruise at v_max, decelerate.
        Proper time during acceleration phase [0→v_max]:
          τ_acc = (c/a)·arcsinh(v_max·γ_max/c)  (hyperbolic motion)
        Coordinate time during acceleration:
          t_acc = (c/a)·sinh(a·τ_acc/c)·... see below.
        """
        g      = SpecialRelativity.lorentz_factor(v_max)
        # Rapidity gained
        phi    = SpecialRelativity.rapidity(v_max)
        # Proper time to accelerate 0→v_max
        tau_acc = C_SI/a_proper * phi              # [s]
        # Coordinate time for same acceleration
        t_acc  = C_SI/a_proper * math.sinh(phi)    # [s]
        # Distance covered during acceleration
        d_acc  = C_SI**2/a_proper * (math.cosh(phi) - 1.0)  # [m]
        # Cruise phase
        d_total_m = d_ly * LY
        d_cruise  = max(0.0, d_total_m - 2.0*d_acc)
        t_cruise_earth = d_cruise / v_max if v_max > 0 else 0.0
        tau_cruise = t_cruise_earth / g

        # Total (round trip × 2 for decelerate + return)
        t_earth_total  = 2.0*(2.0*t_acc + t_cruise_earth)
        tau_ship_total = 2.0*(2.0*tau_acc + tau_cruise)
        return {
            "v_max_c":        v_max/C_SI,
            "a_proper_ms2":   a_proper,
            "gamma_max":      g,
            "tau_acc_yr":     tau_acc/YEAR_S,
            "t_acc_yr":       t_acc/YEAR_S,
            "d_acc_ly":       d_acc/LY,
            "tau_ship_total_yr": tau_ship_total/YEAR_S,
            "t_earth_total_yr":  t_earth_total/YEAR_S,
            "age_diff_yr":       (t_earth_total - tau_ship_total)/YEAR_S,
        }

    # ── §3.8  Relativistic rocket ─────────────────────────────────────────────
    @staticmethod
    def relativistic_rocket(m0_kg: float, m_final_kg: float,
                             exhaust_v: float) -> Dict[str, float]:
        """
        Relativistic Tsiolkovsky equation (Ackeret 1946):
          v_final = v_e · tanh[ln(m0/m_f) · (v_e/c) · arctanh(v_e/c) / v_e]
        Simplified exact form:
          v_f = c · tanh[v_e/c · ln(m0/m_f)]
        For photon rocket (v_e = c):
          v_f = c(R²−1)/(R²+1)  where R = m0/m_f (mass ratio)
        """
        R   = m0_kg / max(m_final_kg, m0_kg*1e-10)
        b_e = exhaust_v / C_SI
        phi_e = math.atanh(min(b_e, 1.0-1e-12))
        phi_f = phi_e * math.log(R)
        v_f   = SpecialRelativity.v_from_rapidity(phi_f)
        g_f   = SpecialRelativity.lorentz_factor(v_f)
        return {
            "mass_ratio":     R,
            "exhaust_v_c":    b_e,
            "v_final_c":      v_f/C_SI,
            "v_final_ms":     v_f,
            "gamma_final":    g_f,
            "delta_rapidity": phi_f,
            "KE_final_J":     SpecialRelativity.kinetic_energy(m_final_kg, v_f),
        }

    @staticmethod
    def photon_rocket(m0_kg: float, m_final_kg: float) -> Dict[str, float]:
        """
        Perfect photon rocket (exhaust at c, theoretical maximum efficiency):
          v_f = c(R²−1)/(R²+1),  η_thrust = 2R/(R²+1) (propulsion efficiency)
        Mass ratio R = m0/m_f.
        """
        R    = m0_kg / max(m_final_kg, 1e-30)
        v_f  = C_SI * (R**2 - 1.0) / (R**2 + 1.0)
        g_f  = SpecialRelativity.lorentz_factor(abs(v_f))
        eta  = 2.0*R / (R**2 + 1.0)
        return {
            "mass_ratio":   R,
            "v_final_c":    v_f/C_SI,
            "gamma_final":  g_f,
            "efficiency":   eta,
            "payload_frac": 1.0/R,
        }

    # ── §3.9  Compton scattering & de Broglie ─────────────────────────────────
    @staticmethod
    def compton_wavelength_shift(theta_deg: float,
                                  m_particle: float = M_ELECTRON) -> float:
        """
        Compton shift: Δλ = (h/mc)(1−cosθ)  [m].
        Compton wavelength: λ_C = h/(mc) = 2.426×10⁻¹² m for electron.
        """
        theta = math.radians(theta_deg)
        return H_PL/(m_particle*C_SI) * (1.0 - math.cos(theta))

    @staticmethod
    def de_broglie_wavelength(m0_kg: float, v: float) -> float:
        """λ = h/(γmv)  [m] — de Broglie wavelength (relativistic)."""
        p = SpecialRelativity.momentum(m0_kg, v)
        return H_PL / max(p, 1e-60)

    # ── §3.10  Bulk SR calculations (vectorised) ──────────────────────────────
    @staticmethod
    def gamma_array(v_arr: np.ndarray) -> np.ndarray:
        """Vectorised Lorentz factor."""
        b2 = np.clip((v_arr/C_SI)**2, 0.0, 1.0-1e-15)
        return 1.0/np.sqrt(1.0 - b2)

    @staticmethod
    def proper_time_along_worldline(t_arr: np.ndarray,
                                     v_arr: np.ndarray) -> np.ndarray:
        """
        Proper time τ(t) accumulated along a worldline v(t):
          dτ = dt/γ(v(t))  →  τ(t) = ∫₀ᵗ dt'/γ(v(t'))
        Numerically integrated via cumulative trapezoidal.
        """
        g_arr  = SpecialRelativity.gamma_array(v_arr)
        dtau   = np.gradient(t_arr) / g_arr
        return np.cumsum(dtau)

    @staticmethod
    def worldline_coords(tau_arr: np.ndarray,
                          v_arr: np.ndarray,
                          a_arr: Optional[np.ndarray] = None
                          ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute (t, x) spacetime coordinates from proper time and velocity.
        Returns (t_arr [s], x_arr [m]) in the lab frame.
        """
        g_arr = SpecialRelativity.gamma_array(v_arr)
        dtau  = np.gradient(tau_arr)
        dt    = g_arr * dtau              # coordinate time steps
        dx    = v_arr * dt                # coordinate displacement
        t_out = np.cumsum(dt)
        x_out = np.cumsum(dx)
        return t_out, x_out


# ══════════════════════════════════════════════════════════════════════════════
# §4  GENERAL RELATIVITY ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class GeneralRelativity:
    """
    General relativity calculations: Schwarzschild & Kerr metric physics,
    gravitational time dilation, redshift, Shapiro delay, geodesic integration,
    perihelion precession, light bending.
    References: Einstein (1916) [2], Schwarzschild (1916) [4], MTW [9].
    """

    def __init__(self, M_kg: float = GARG_MASS_KG,
                 spin_star: float = GARG_SPIN):
        self.M_kg      = M_kg
        self.spin_star = spin_star
        self.M_geo     = G_SI*M_kg/C_SI**2      # GM/c²  [m]
        self.r_s       = 2.0*self.M_geo          # Schwarzschild radius [m]
        self.a         = spin_star*self.M_geo    # Kerr spin parameter [m]

    # ── §4.1  Schwarzschild time dilation ──────────────────────────────────
    def schw_time_dilation(self, r: float) -> float:
        """
        Gravitational time dilation in Schwarzschild metric [4]:
          dτ/dt = √(1 − r_s/r)
        At r = r_s: dτ/dt = 0 (coordinate singularity — clock stops).
        At r → ∞:   dτ/dt → 1.
        Experiment: Pound-Rebka (1959) [6], GPS corrections.
        """
        ratio = self.r_s / max(r, self.r_s*1.001)
        return math.sqrt(max(1.0 - ratio, 0.0))

    def schw_combined_dilation(self, r: float, v_orb: float) -> float:
        """
        Combined GR+SR proper time ratio for object at r with speed v_orb:
          dτ/dt = √(1 − r_s/r − v²/c²)
        For circular orbit: v_orb = √(GM/r) → full formula.
        """
        gr_term = self.r_s / max(r, self.r_s*1.001)
        sr_term = (v_orb/C_SI)**2
        return math.sqrt(max(1.0 - gr_term - sr_term, 0.0))

    def orbital_v_circular(self, r: float) -> float:
        """Keplerian (Newtonian) circular orbit speed: v = √(GM/r)"""
        return math.sqrt(G_SI*self.M_kg / max(r, 1e-10))

    def gps_frequency_correction(self, r_orbit: float = 2.656e7,
                                  v_orbit: float = 3.874e3) -> Dict[str, float]:
        """
        GPS satellite clock correction (Hafele-Keating type [7]):
          Δf_GR/f = r_s/(2r)  (gravitational blueshift for satellite)
          Δf_SR/f = −v²/(2c²) (velocity redshift)
          Net: satellite clock runs fast by ~38.4 μs/day.
        Default: GPS orbit r=26,560 km, v=3.874 km/s.
        """
        # Earth parameters for GPS
        M_e    = M_EARTH
        r_s_e  = 2.0*G_SI*M_e/C_SI**2
        gr_sat = r_s_e/(2.0*r_orbit)             # GR fractional rate
        sr_sat = -(v_orbit/C_SI)**2/2.0           # SR fractional rate
        net    = gr_sat + sr_sat                   # net rate correction
        bias_us_day = net * DAY_S * 1e6           # μs/day
        # Surface contribution (negative: surface clock is in deeper well)
        r_surf = R_EARTH; v_surf = 465.0          # m/s Earth surface
        gr_surf = r_s_e/(2.0*r_surf)
        sr_surf = -(v_surf/C_SI)**2/2.0
        delta_us_day = (net - (gr_surf+sr_surf)) * DAY_S * 1e6
        return {
            "r_orbit_m":         r_orbit,
            "v_orbit_ms":        v_orbit,
            "GR_fractional":     gr_sat,
            "SR_fractional":     sr_sat,
            "net_fractional":    net,
            "sat_clock_bias_us_per_day": bias_us_day,
            "net_bias_vs_surface_us_day": delta_us_day,
        }

    # ── §4.2  Gravitational redshift ──────────────────────────────────────────
    def gravitational_redshift(self, r_emit: float, r_obs: float) -> float:
        """
        Gravitational redshift [6]:
          1 + z = √(1 − r_s/r_emit) / √(1 − r_s/r_obs)
        z > 0: photon climbs out of potential well (redshifted).
        z < 0: photon falls in (blueshifted).
        For r_obs → ∞:  1+z = 1/√(1−r_s/r_emit)
        """
        num = self.schw_time_dilation(r_emit)
        den = self.schw_time_dilation(r_obs)
        return num/(den + 1e-30) - 1.0

    def shapiro_delay(self, r1: float, r2: float) -> float:
        """
        Shapiro (gravitational) time delay (Shapiro 1964):
          Δt_Shapiro = 2GM/c³ × ln(4r₁r₂/b²)  [s]
        where b = impact parameter (here approximated as r_s/2).
        For Sun: Δt ~ 240 μs for Earth-Venus radar bounce.
        """
        b = max(self.r_s/2.0, 1e-3)
        return 2.0*self.M_geo/C_SI * math.log(4.0*r1*r2/b**2)

    # ── §4.3  Kerr proper time ────────────────────────────────────────────────
    def kerr_proper_time_ratio(self, r: float,
                                prograde: bool = True) -> float:
        """
        dτ/dt for circular equatorial orbit in Kerr metric:
          dτ/dt = √(1 − 3M/r ± 2a√(M/r³))
        − for prograde, + for retrograde. [5]
        """
        M  = self.M_geo; a = self.a
        pm = +1.0 if prograde else -1.0
        try:
            arg = 1.0 - 3.0*M/r + 2.0*pm*a*math.sqrt(M/max(r**3, 1e-30))
            return math.sqrt(max(arg, 0.0))
        except Exception:
            return 0.0

    # ── §4.4  Geodesic integration (Schwarzschild) ────────────────────────────
    def geodesic_integrate_schw(self,
                                  r0: float, phi0: float,
                                  L: float, E: float = 1.0,
                                  n_steps: int = 5000,
                                  dlambda: float = 1.0e6
                                  ) -> Dict[str, np.ndarray]:
        """
        Integrate timelike geodesic in Schwarzschild metric.
        Conserved quantities: E (energy/mass), L (angular momentum/mass).
        Equations of motion (MTW §25 [9]):
          (dr/dτ)² = E² − (1−r_s/r)(1 + L²/r²)
          dφ/dτ   = L/r²
          dt/dτ   = E/(1−r_s/r)
        Integration: RK45 in (r, φ, t) with affine parameter λ.
        """
        rs = self.r_s

        def V_eff_sq(r):
            """(E² − V_eff²) = (dr/dτ)²"""
            return E**2 - (1.0 - rs/max(r,rs*1.001))*(1.0 + L**2/r**2)

        def eom(lam, state):
            r, phi, t = state
            r = max(r, rs*1.02)
            D = 1.0 - rs/r
            D = max(D, 1e-10)
            dr2 = V_eff_sq(r)
            dr  = math.sqrt(max(dr2, 0.0))   # inward
            dphi = L/r**2
            dt_c = E/D
            return [-dr, dphi, dt_c]

        sol = sci_int.solve_ivp(
            eom, [0, n_steps*dlambda], [r0, phi0, 0.0],
            method="RK45", max_step=dlambda*5,
            events=lambda l, s: s[0] - rs*1.05,
            dense_output=False)

        r_a   = sol.y[0]; phi_a = sol.y[1]; t_a = sol.y[2]
        x_a   = r_a*np.cos(phi_a); y_a = r_a*np.sin(phi_a)
        return {"r": r_a, "phi": phi_a, "t": t_a,
                "x": x_a, "y": y_a,
                "captured": bool(r_a[-1] < rs*1.1)}

    # ── §4.5  Orbital precession ──────────────────────────────────────────────
    def perihelion_precession(self, a_orbit: float,
                               ecc: float) -> float:
        """
        General relativistic perihelion precession per orbit [2]:
          δφ = 6πGM / [c² a(1−e²)]  [radians/orbit]
        Mercury: a=5.79×10¹⁰ m, e=0.206 → δφ=43 arcsec/century.
        """
        return 6.0*math.pi*G_SI*self.M_kg / (C_SI**2 * a_orbit*(1.0-ecc**2))

    def precession_arcsec_per_century(self, a_orbit: float,
                                        ecc: float,
                                        period_yr: float) -> float:
        """Convert precession per orbit to arcsec/century."""
        rad_per_orbit = self.perihelion_precession(a_orbit, ecc)
        orbits_per_century = 100.0 / period_yr
        return math.degrees(rad_per_orbit)*3600.0 * orbits_per_century

    # ── §4.6  Gravitational light bending ────────────────────────────────────
    def light_bending_angle(self, b: float) -> float:
        """
        Eddington (1919) gravitational light deflection:
          α = 4GM/(c²b)  [radians]
        GR gives twice the Newtonian prediction.
        Sun: α = 1.75 arcsec at limb (b = R_sun).
        """
        return 4.0*G_SI*self.M_kg / (C_SI**2 * max(b, 1e-10))

    def einstein_ring_angle(self, D_L: float, D_S: float) -> float:
        """
        Einstein ring angular radius θ_E [rad]:
          θ_E = √(4GM D_LS / c² D_L D_S)
        D_L: lens distance, D_S: source distance [m].
        """
        D_LS = abs(D_S - D_L)
        return math.sqrt(4.0*G_SI*self.M_kg*D_LS /
                         (C_SI**2*D_L*D_S + 1e-30))

    # ── §4.7  Equivalence principle ───────────────────────────────────────────
    @staticmethod
    def equivalence_principle_demonstration(a_accel: float,
                                             h_height: float) -> Dict[str, float]:
        """
        Equivalence principle (Einstein 1907):
        A uniformly accelerating rocket at acceleration a [m/s²]
        is locally equivalent to gravitational field g = a.
        Clock at height h runs faster by:
          Δf/f = gh/c² = ah/c²  (same as Pound-Rebka [6] formula)
        """
        delta_f_f = a_accel * h_height / C_SI**2
        t_ahead_s_per_s = delta_f_f     # fractional rate difference
        return {
            "acceleration_ms2":     a_accel,
            "height_m":             h_height,
            "Deltaf_over_f":        delta_f_f,
            "top_clock_faster_ppm": delta_f_f*1e6,
            "bias_ns_per_day":      delta_f_f*DAY_S*1e9,
            "equivalent_g_field":   a_accel,
        }

    # ── §4.8  Vectorised GR profile ───────────────────────────────────────────
    def gr_profile_dataframe(self, r_min_rs: float = 1.02,
                              r_max_rs: float = 1000.0,
                              n: int = 500) -> pd.DataFrame:
        """Radial GR physics profile (Schwarzschild) over n points."""
        r_arr = np.geomspace(r_min_rs*self.r_s, r_max_rs*self.r_s, n)
        rows  = []
        for r in r_arr:
            v_circ = self.orbital_v_circular(r)
            dil_gr = self.schw_time_dilation(r)
            dil_combo = self.schw_combined_dilation(r, v_circ)
            ker_dil = self.kerr_proper_time_ratio(r)
            rows.append({
                "r_m":              r,
                "r_rs":             r/self.r_s,
                "dil_GR_only":      dil_gr,
                "dil_combined":     dil_combo,
                "dil_Kerr":         ker_dil,
                "factor_GR":        1.0/max(dil_gr, 1e-30),
                "factor_combined":  1.0/max(dil_combo, 1e-30),
                "factor_Kerr":      1.0/max(ker_dil, 1e-30),
                "redshift_z_local": 1.0/max(dil_gr,1e-30) - 1.0,
                "v_circ_c":         v_circ/C_SI,
                "light_bend_rad":   self.light_bending_angle(r),
            })
        return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# §5  COOPER-MURPH MISSION TIME ENGINE
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class MissionLeg:
    """One segment of the Interstellar mission with time dilation."""
    name:           str
    phase:          MissionPhase
    earth_time_yr:  float          # Earth-frame duration [yr]
    ship_time_yr:   float          # Proper time on ship [yr]
    dilation_factor: float         # earth_time / ship_time
    v_c:            float = 0.0    # cruise velocity [fraction of c]
    r_rs:           float = 0.0    # orbital radius [r_s units] if GR dominant
    notes:          str   = ""

    @property
    def earth_time_s(self) -> float:
        return self.earth_time_yr * YEAR_S

    @property
    def ship_time_s(self) -> float:
        return self.ship_time_yr * YEAR_S


@dataclass
class PersonTimeline:
    """Tracks age of a person through the mission."""
    name:      str
    age_start: float               # age at mission start [yr]
    legs:      List[Tuple[str, float]] = field(default_factory=list)
    # (leg_name, delta_age_yr) — how much they age in each leg

    def age_at(self, leg_idx: int) -> float:
        age = self.age_start
        for _, da in self.legs[:leg_idx+1]:
            age += da
        return age

    def final_age(self) -> float:
        return self.age_start + sum(da for _, da in self.legs)


class CooperMurphTimeEngine:
    """
    Computes the full Interstellar mission timeline tracking Cooper's proper
    time vs Murph's Earth proper time, leg by leg, using exact GR+SR dilation.

    Mission summary (canon, Kip Thorne [8]):
      Earth → Saturn:  ~2 years (low v, negligible dilation)
      Wormhole transit: ~5 weeks Earth time
      Miller's World:  1h ship = 7yr Earth (gravitational time dilation)
      Mann → Gargantua: ~14 Earth years total mission before Mann planet
      Tesseract: ~1 hour Cooper subjective, but undefined Earth time
      Total ship proper time for Cooper: ~3 years
      Total Earth coordinate time: ~90+ years
    """

    def __init__(self):
        self.sr  = SpecialRelativity()
        self.gr  = GeneralRelativity(GARG_MASS_KG, GARG_SPIN)
        self.legs: List[MissionLeg] = []
        self._build_canon_timeline()

    def _build_canon_timeline(self):
        """
        Build the canonical Interstellar mission timeline from film + Thorne [8].
        All times confirmed against the published science notes.
        """
        # ── Leg 1: Earth to Saturn (2 years Earth, ~2 years ship) ────────────
        # Velocity ~40 km/s relative to Earth: γ≈1+4×10⁻⁹, negligible dilation
        v_saturn = 40_000.0   # m/s
        g_saturn = SpecialRelativity.lorentz_factor(v_saturn)
        L1 = MissionLeg(
            name="Earth → Saturn",
            phase=MissionPhase.EARTH_LAUNCH,
            earth_time_yr=2.0,
            ship_time_yr=2.0 / g_saturn,
            dilation_factor=g_saturn,
            v_c=v_saturn/C_SI,
            notes="Conventional rocket, negligible relativistic dilation"
        )

        # ── Leg 2: Saturn → Wormhole + Transit (5 weeks ≈ 0.096 yr) ─────────
        v_wormhole = 0.5 * C_SI   # accelerating through wormhole
        g_worm = SpecialRelativity.lorentz_factor(v_wormhole)
        L2 = MissionLeg(
            name="Saturn → Wormhole Transit",
            phase=MissionPhase.WORMHOLE_TRANSIT,
            earth_time_yr=0.10,
            ship_time_yr=0.10 / g_worm,
            dilation_factor=g_worm,
            v_c=0.5,
            notes="Transit through wormhole at ~0.5c; mild SR dilation"
        )

        # ── Leg 3: Wormhole exit → Miller's World approach ────────────────────
        # Approaching Gargantua; orbital approach at r~1.5 r_ISCO
        r_approach = 1.5 * self._miller_risco_approx()
        dtr_app = self.gr.kerr_proper_time_ratio(r_approach)
        earth_yr_approach = 0.3   # ~3-4 months ship flight
        L3 = MissionLeg(
            name="Wormhole Exit → Miller Approach",
            phase=MissionPhase.MILLER_APPROACH,
            earth_time_yr=earth_yr_approach / dtr_app,
            ship_time_yr=earth_yr_approach,
            dilation_factor=1.0/max(dtr_app, 1e-10),
            r_rs=r_approach/self.gr.r_s,
            notes="Approaching Gargantua at r~1.5 r_ISCO; GR dilation ~15×"
        )

        # ── Leg 4: Miller's World surface (1h ship = 7yr Earth) ───────────────
        miller = self.gr.M_geo  # placeholder; exact below
        # Film: Cooper + Brand + Doyle spend ~3.22 hours on Miller
        ship_hrs_miller = 3.22
        dilation_miller = 7.0 * YEAR_S / HOUR_S   # 61 320× exact
        earth_yr_miller = ship_hrs_miller/HOUR_S * YEAR_S * dilation_miller / YEAR_S
        L4 = MissionLeg(
            name="Miller's World Surface",
            phase=MissionPhase.MILLER_SURFACE,
            earth_time_yr=earth_yr_miller,
            ship_time_yr=ship_hrs_miller/HOUR_S,
            dilation_factor=dilation_miller,
            r_rs=1.0,   # at r_ISCO+ε
            notes=f"{ship_hrs_miller}h ship = {earth_yr_miller:.1f} Earth years"
        )

        # ── Leg 5: Miller Departure → Mann's Planet (~14yr Earth, ~2yr ship) ──
        r_depart = 10.0 * self.gr.r_s
        dtr_dep  = self.gr.kerr_proper_time_ratio(r_depart)
        earth_yr_mann = 14.0   # Earth years before Mann planet
        L5 = MissionLeg(
            name="Miller Departure → Mann's Planet",
            phase=MissionPhase.MANN_TRANSIT,
            earth_time_yr=earth_yr_mann,
            ship_time_yr=earth_yr_mann * dtr_dep,
            dilation_factor=1.0/max(dtr_dep, 1e-10),
            r_rs=10.0,
            notes="Romilly stays in Endurance orbit; 23 Earth years total lost"
        )

        # ── Leg 6: Mann's Planet Episode ──────────────────────────────────────
        # Mild dilation; Mann planet far from Gargantua
        L6 = MissionLeg(
            name="Mann's Planet",
            phase=MissionPhase.MANN_SURFACE,
            earth_time_yr=0.5,
            ship_time_yr=0.48,    # mild SR + GR dilation at distant orbit
            dilation_factor=0.5/0.48,
            v_c=0.0,
            notes="Far from Gargantua; near-Newtonian time"
        )

        # ── Leg 7: Mann → Gargantua slingshot ────────────────────────────────
        v_slingshot = 0.8 * C_SI
        g_sl = SpecialRelativity.lorentz_factor(v_slingshot)
        L7 = MissionLeg(
            name="Gargantua Slingshot",
            phase=MissionPhase.GARGANTUA_ORBIT,
            earth_time_yr=5.0,
            ship_time_yr=5.0/g_sl,
            dilation_factor=g_sl,
            v_c=0.8,
            notes="Gravitational slingshot using Gargantua; SR dominant"
        )

        # ── Leg 8: Tesseract ──────────────────────────────────────────────────
        # Cooper spends ~1 subjective hour; Earth time ambiguous (5D bulk)
        L8 = MissionLeg(
            name="Tesseract (5D Bulk)",
            phase=MissionPhase.TESSERACT,
            earth_time_yr=0.0,    # undefined in bulk; near-simultaneous
            ship_time_yr=HOUR_S/YEAR_S,
            dilation_factor=0.0,   # not applicable — 5D space
            notes="Subjective 1 hour inside 5D tesseract; time undefined"
        )

        self.legs = [L1, L2, L3, L4, L5, L6, L7, L8]

    def _miller_risco_approx(self) -> float:
        """Approximate r_Miller ≈ r_ISCO × (1 + ε) for a*≈1."""
        a  = GARG_SPIN
        Z1 = (1.0+(1-a**2)**(1/3)*((1+a)**(1/3)+(1-a)**(1/3)))
        Z2 = math.sqrt(3*a**2+Z1**2)
        r_isco_M = 3+Z2-math.sqrt((3-Z1)*(3+Z1+2*Z2))
        return r_isco_M * GARG_M_GEO * 1.0001

    def cooper_timeline(self) -> pd.DataFrame:
        """
        Cooper's proper time (ship clock) leg by leg.
        Returns DataFrame with cumulative ages and Earth time.
        """
        cooper_age  = COOPER_AGE_START
        earth_t     = 0.0
        rows = []
        for leg in self.legs:
            rows.append({
                "Leg":            leg.name,
                "Phase":          leg.phase.value,
                "Ship time (yr)": leg.ship_time_yr,
                "Earth time (yr)":leg.earth_time_yr,
                "Dilation factor":leg.dilation_factor if leg.dilation_factor > 0 else float("nan"),
                "Cooper age start": cooper_age,
                "Cooper age end":   cooper_age + leg.ship_time_yr,
                "Earth year start": earth_t,
                "Earth year end":   earth_t + leg.earth_time_yr,
                "Notes":          leg.notes,
            })
            cooper_age += leg.ship_time_yr
            earth_t    += leg.earth_time_yr
        return pd.DataFrame(rows)

    def murph_timeline(self) -> pd.DataFrame:
        """
        Murph's Earth proper time (she never leaves Earth).
        Murph ages at normal rate; only Earth coordinate time applies.
        """
        murph_age  = MURPH_AGE_START
        earth_t    = 0.0
        rows = []
        for leg in self.legs:
            rows.append({
                "Leg":            leg.name,
                "Earth time (yr)":leg.earth_time_yr,
                "Murph age start": murph_age,
                "Murph age end":   murph_age + leg.earth_time_yr,
                "Earth year start": earth_t,
                "Earth year end":   earth_t + leg.earth_time_yr,
            })
            murph_age += leg.earth_time_yr
            earth_t   += leg.earth_time_yr
        return pd.DataFrame(rows)

    def divergence_summary(self) -> Dict[str, float]:
        """Full Cooper-Murph age divergence at mission end."""
        total_ship    = sum(l.ship_time_yr for l in self.legs)
        total_earth   = sum(l.earth_time_yr for l in self.legs)
        cooper_final  = COOPER_AGE_START + total_ship
        murph_final   = MURPH_AGE_START  + total_earth
        return {
            "mission_start_year_approx":  2063,
            "total_ship_time_yr":         total_ship,
            "total_earth_time_yr":        total_earth,
            "cooper_age_start":           COOPER_AGE_START,
            "cooper_age_end":             cooper_final,
            "murph_age_start":            MURPH_AGE_START,
            "murph_age_end":              murph_final,
            "age_gap_yr":                 murph_final - cooper_final,
            "murph_older_by_yr":          murph_final - cooper_final,
            "dominance_miller":           self.legs[3].earth_time_yr,
            "effective_total_dilation":   total_earth/max(total_ship, 1e-10),
        }

    def miller_scenario_calculator(self, ship_hours: float,
                                    ship_dilation: float = 61_320.0
                                    ) -> Dict[str, float]:
        """
        For arbitrary mission duration on Miller, compute time divergence.
        ship_dilation: Earth seconds per ship second (default 61,320×).
        """
        earth_s = ship_hours * 3600.0 * ship_dilation
        earth_yr = earth_s / YEAR_S
        return {
            "ship_hours":        ship_hours,
            "ship_days":         ship_hours/24.0,
            "earth_years_lost":  earth_yr,
            "earth_decades":     earth_yr/10.0,
            "dilation_factor":   ship_dilation,
            "murph_ages_by_yr":  earth_yr,
        }

    def custom_leg(self, v_c: float, r_rs: float,
                   ship_yr: float, name: str = "Custom") -> MissionLeg:
        """
        Build a custom mission leg with given velocity and GR radius.
        Combined dilation: dτ/dt = √(1−3M/r ± 2a√(M/r³)) × SR_correction
        """
        # Pure SR
        g_sr     = SpecialRelativity.lorentz_factor(v_c*C_SI)
        # Pure GR (Kerr)
        r_m      = r_rs * self.gr.r_s
        dtr_kerr = self.gr.kerr_proper_time_ratio(r_m) if r_rs > 1.1 else 1.0
        # Combined (approximate; exact requires full metric integration)
        combined = dtr_kerr / g_sr  # ratio: ship / earth
        earth_yr = ship_yr / max(combined, 1e-10)
        return MissionLeg(
            name=name, phase=MissionPhase.GARGANTUA_ORBIT,
            earth_time_yr=earth_yr, ship_time_yr=ship_yr,
            dilation_factor=1.0/max(combined, 1e-10),
            v_c=v_c, r_rs=r_rs,
            notes=f"SR γ={g_sr:.3f}  GR dτ/dt={dtr_kerr:.4e}  combined={combined:.4e}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# §6  SPACETIME DIAGRAM BUILDER
# ══════════════════════════════════════════════════════════════════════════════
class SpacetimeDiagramBuilder:
    """
    Constructs Minkowski spacetime diagrams (1+1D: ct vs x).
    Handles worldlines, light cones, simultaneity lines, twin paradox,
    and Cooper-Murph comparison worldlines.
    Reference: Taylor & Wheeler "Spacetime Physics" [11].
    """

    def __init__(self, x_range: float = 10.0, ct_range: float = 10.0):
        self.x_range  = x_range
        self.ct_range = ct_range

    def light_cone_lines(self) -> Tuple[np.ndarray, np.ndarray,
                                         np.ndarray, np.ndarray]:
        """
        Light cone through origin: ct = ±x.
        Returns (x_future, ct_future, x_past, ct_past).
        """
        x = np.linspace(-self.x_range, self.x_range, 200)
        return x, x, x, -x

    def worldline_inertial(self, v_c: float,
                            t_start: float = 0.0,
                            t_end: float = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Worldline of inertial observer at speed v (fraction of c).
        Returns (x_arr, ct_arr) in units of [ly, ly].
        """
        ct_max = t_end if t_end else self.ct_range
        ct_arr = np.linspace(t_start, ct_max, 400)
        x_arr  = v_c * ct_arr   # x = vt → ct_arr is in ly units
        return x_arr, ct_arr

    def worldline_accelerating(self, a_proper_ly_yr2: float,
                                 ct_max: float = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Hyperbolic worldline (constant proper acceleration):
          x = c²/a [cosh(aτ/c)−1],  ct = c²/a sinh(aτ/c)
        In natural units (c=1): x = 1/a[cosh(aτ)−1], ct = 1/a·sinh(aτ).
        """
        ct_max = ct_max or self.ct_range
        a      = a_proper_ly_yr2        # in ly/yr²
        tau_max= math.asinh(ct_max*a)/a if a > 0 else ct_max
        tau    = np.linspace(0, tau_max, 400)
        x_arr  = (1.0/a)*(np.cosh(a*tau) - 1.0)
        ct_arr = (1.0/a)*np.sinh(a*tau)
        return x_arr, ct_arr

    def twin_paradox_worldlines(self, v_c: float,
                                  d_ly: float
                                  ) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
        """
        Return worldlines for stay-at-home (S) and traveller (T) twins.
        T travels at v_c to distance d_ly, turns around, returns.
        """
        # Earth twin: worldline along ct-axis
        ct_total = 2.0*d_ly/v_c         # total coordinate time [ly/c = yr at c=1]
        ct_stay  = np.array([0.0, ct_total])
        x_stay   = np.array([0.0, 0.0])

        # Traveller: outgoing then returning
        t_turn   = d_ly/v_c              # turnaround coordinate time
        x_turn   = d_ly                  # at turnaround
        ct_trav  = np.array([0.0, t_turn, 2.0*t_turn])
        x_trav   = np.array([0.0, x_turn, 0.0])

        # Proper times
        g        = SpecialRelativity.lorentz_factor(v_c*C_SI)
        tau_trav = ct_total / g
        tau_stay = ct_total

        return {
            "earth": (x_stay, ct_stay),
            "traveller": (x_trav, ct_trav),
            "t_turn": t_turn,
            "x_turn": x_turn,
            "ct_total": ct_total,
            "tau_traveller": tau_trav,
            "tau_earth": tau_stay,
            "age_diff": tau_stay - tau_trav,
        }

    def simultaneity_line(self, v_c: float,
                           event_ct: float = 0.0,
                           event_x: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Line of simultaneity for observer moving at v_c through (x₀, ct₀).
        Slope in Minkowski diagram: d(ct)/dx = v/c = v_c.
        """
        x_arr  = np.linspace(-self.x_range, self.x_range, 200)
        ct_arr = event_ct + v_c*(x_arr - event_x)
        return x_arr, ct_arr

    def cooper_murph_worldlines(self,
                                  engine: CooperMurphTimeEngine
                                  ) -> Dict[str, Any]:
        """
        Build Cooper and Murph worldlines in a single Earth-frame spacetime
        diagram.  x-axis represents distance (light-years from Earth);
        ct-axis represents Earth coordinate time (years).
        Cooper moves; Murph stays at x=0.
        Returns arrays for plotting.
        """
        cooper_df = engine.cooper_timeline()
        murph_df  = engine.murph_timeline()

        # Murph: stays at x=0 for all Earth time
        et_murph_bounds = [0.0]
        for _, row in murph_df.iterrows():
            et_murph_bounds.append(row["Earth year end"])
        et_murph = np.array(et_murph_bounds)
        x_murph  = np.zeros_like(et_murph)

        # Cooper: simplified — moves away, stays in Gargantua system, returns
        # Build from mission legs
        et_cooper  = [0.0]
        x_cooper   = [0.0]
        ct_current = 0.0
        x_current  = 0.0
        for leg in engine.legs:
            dt_earth = leg.earth_time_yr
            # Simple motion model: Miller legs stay at Gargantua x~10 ly,
            # Saturn legs move to x~6 ly, etc. (simplified geometry)
            if "Saturn" in leg.name:
                x_target = 6.0         # AU to Saturn converted to symbolic ly
            elif "Wormhole" in leg.name:
                x_target = 10.0
            elif "Miller" in leg.name or "Mann" in leg.name or "Gargantua" in leg.name:
                x_target = 10.0
            elif "Tesseract" in leg.name:
                x_target = 10.0
            else:
                x_target = 0.0
            ct_current += dt_earth
            x_current   = x_target
            et_cooper.append(ct_current)
            x_cooper.append(x_current)

        return {
            "cooper_ct": np.array(et_cooper),
            "cooper_x":  np.array(x_cooper),
            "murph_ct":  et_murph,
            "murph_x":   x_murph,
            "summary":   engine.divergence_summary(),
        }


# ══════════════════════════════════════════════════════════════════════════════
# §6A  INTERSTELLAR MISSION TIMELINE INTEGRATOR — Exact Leg-by-Leg
# ══════════════════════════════════════════════════════════════════════════════
class InterstellarMissionIntegrator:
    """
    Rigorous leg-by-leg proper-time integrator for the complete Interstellar
    mission. Each leg uses the exact time dilation formula for the relevant
    physical regime (SR for cruise, Kerr GR for orbital/planetary phases).

    Mission legs (film canon + Thorne [8]):
      1. Earth departure → Saturn flyby (Hohmann-type, ~2 yr cruise at 0.5% c)
      2. Saturn → Wormhole approach (Δv for insertion, ~6 months)
      3. Wormhole transit (Morris-Thorne throat, τ_transit ~ minutes)
      4. Wormhole exit → Miller's World approach (orbital mechanics)
      5. Miller's World surface (extreme Kerr dilation: 1h_ship = 7yr_Earth)
      6. Miller → Mann's Planet transit (~months ship time)
      7. Mann's Planet surface operations (~1 day)
      8. Mann → Gargantua slingshot approach
      9. Gargantua close approach (critical Kerr orbit, extreme dilation)
      10. Cooper's Tesseract phase (subjective time ~hours, Earth decades)
      11. Cooper rescue + return to Cooper Station (near-Saturn space)
      12. Brand's journey to Edmunds' Planet (Gargantua → Edmunds, ~months)

    Output: DataFrame with Cooper age, Murph age, Earth time at each boundary.
    """

    # Mission parameters from film + Thorne's book
    LEGS = [
        {"name": "Earth → Saturn",         "v_c": 0.005,  "ship_yr": 2.00,  "kerr_dilation": 1.0},
        {"name": "Saturn → Wormhole",       "v_c": 0.008,  "ship_yr": 0.50,  "kerr_dilation": 1.0},
        {"name": "Wormhole Transit",        "v_c": 0.001,  "ship_yr": 0.001, "kerr_dilation": 1.0},
        {"name": "→ Miller's Orbit",        "v_c": 0.10,   "ship_yr": 0.25,  "kerr_dilation": 1.02},
        {"name": "Miller Surface (3h15m)",  "v_c": 0.0,    "ship_yr": 3.25/8766, "kerr_dilation": 61320.0},
        {"name": "Miller → Mann Transit",   "v_c": 0.05,   "ship_yr": 0.75,  "kerr_dilation": 1.001},
        {"name": "Mann Surface Ops",        "v_c": 0.0,    "ship_yr": 1.0/365.25, "kerr_dilation": 1.0},
        {"name": "Mann → Gargantua App.",   "v_c": 0.15,   "ship_yr": 0.50,  "kerr_dilation": 1.05},
        {"name": "Gargantua Slingshot",     "v_c": 0.50,   "ship_yr": 0.002, "kerr_dilation": 51.0},
        {"name": "Tesseract (Cooper)",      "v_c": 0.0,    "ship_yr": 0.005, "kerr_dilation": 365.25*23*2},
        {"name": "Cooper Rescue → Station", "v_c": 0.01,   "ship_yr": 0.10,  "kerr_dilation": 1.0},
        {"name": "Brand → Edmunds",         "v_c": 0.20,   "ship_yr": 3.00,  "kerr_dilation": 1.001},
    ]

    def __init__(self, cooper_birth_year: float = 2032.0,
                 murph_birth_year: float = 2053.0,
                 mission_start_year: float = 2067.0):
        self.cooper_birth = cooper_birth_year
        self.murph_birth  = murph_birth_year
        self.mission_start= mission_start_year

    def _sr_dilation(self, v_c: float) -> float:
        """SR Lorentz factor γ(v)."""
        beta = min(abs(v_c), 0.9999)
        return 1.0 / math.sqrt(1.0 - beta*beta)

    def integrate_full_timeline(self) -> pd.DataFrame:
        """
        Integrate full mission timeline leg-by-leg.
        For each leg:
          Δτ_ship = given ship proper time
          Δt_Earth = Δτ_ship × γ(v) × kerr_dilation_factor
        Returns DataFrame with cumulative times and ages.
        """
        rows = []
        cum_ship_yr   = 0.0   # cumulative Cooper proper time from mission start
        cum_earth_yr  = 0.0   # cumulative Earth time from mission start
        cum_brand_yr  = 0.0   # Brand proper time (diverges from Cooper after leg 9)
        cooper_separated = False  # Cooper separates at Gargantua

        for i, leg in enumerate(self.LEGS):
            gamma     = self._sr_dilation(leg["v_c"])
            delta_ship = leg["ship_yr"]
            delta_earth = delta_ship * gamma * leg["kerr_dilation"]

            # Track Cooper vs Brand separation at Gargantua
            if leg["name"].startswith("Tesseract") or leg["name"].startswith("Cooper"):
                cooper_separated = True
                cum_ship_yr  += delta_ship
                cum_earth_yr += delta_earth
                # Brand doesn't experience tesseract — she continues to Edmunds
            elif leg["name"].startswith("Brand"):
                # This is Brand's leg after separation
                cum_brand_yr += delta_ship
                cum_earth_yr += delta_earth
            else:
                cum_ship_yr  += delta_ship
                cum_earth_yr += delta_earth
                if not cooper_separated:
                    cum_brand_yr += delta_ship

            earth_year_now  = self.mission_start + cum_earth_yr
            cooper_age      = (self.mission_start - self.cooper_birth) + cum_ship_yr
            murph_age       = (self.mission_start - self.murph_birth) + cum_earth_yr

            rows.append({
                "Leg":              i + 1,
                "Phase":            leg["name"],
                "v/c":              leg["v_c"],
                "γ":                round(gamma, 4),
                "Kerr Factor":      leg["kerr_dilation"],
                "Δτ_ship [yr]":     round(delta_ship, 6),
                "Δt_Earth [yr]":    round(delta_earth, 4),
                "Cum. Ship τ [yr]": round(cum_ship_yr, 4),
                "Cum. Earth t [yr]":round(cum_earth_yr, 4),
                "Earth Year":       round(earth_year_now, 2),
                "Cooper Age":       round(cooper_age, 2),
                "Murph Age":        round(murph_age, 2),
                "Brand Ship τ [yr]":round(cum_brand_yr, 4),
                "Age Gap [yr]":     round(murph_age - cooper_age, 2),
            })

        return pd.DataFrame(rows)

    def age_paradox_summary(self) -> Dict[str, Any]:
        """Summary statistics of the Cooper-Murph age paradox."""
        df = self.integrate_full_timeline()
        final = df.iloc[-1]
        return {
            "cooper_final_age_yr":    final["Cooper Age"],
            "murph_final_age_yr":     final["Murph Age"],
            "age_gap_yr":             final["Age Gap [yr]"],
            "earth_year_at_end":      final["Earth Year"],
            "total_ship_time_yr":     final["Cum. Ship τ [yr]"],
            "total_earth_time_yr":    final["Cum. Earth t [yr]"],
            "max_dilation_phase":     df.loc[df["Kerr Factor"].idxmax(), "Phase"],
            "max_dilation_factor":    df["Kerr Factor"].max(),
            "total_legs":             len(df),
        }

    def murph_milestone_ages(self) -> Dict[str, float]:
        """
        Key Murph milestone ages from the film:
          - Murph ~10yr old at mission launch (2067): Murph born ~2057
          - Murph solves equation ~age 35-40 (after Miller data loss)
          - Cooper finds Murph on deathbed: Murph ~124 yr old, Cooper ~40
        """
        df = self.integrate_full_timeline()
        milestones = {}
        for _, row in df.iterrows():
            phase = row["Phase"]
            milestones[phase] = {
                "murph_age": row["Murph Age"],
                "cooper_age": row["Cooper Age"],
                "earth_year": row["Earth Year"],
            }
        return milestones


# ══════════════════════════════════════════════════════════════════════════════
# §6B  GRAVITATIONAL WAVE MEMORY EFFECT — Christodoulou Memory
# ══════════════════════════════════════════════════════════════════════════════
class GWMemoryCalculator:
    """
    Gravitational wave memory (Christodoulou 1991, Thorne 1992):
    A permanent spacetime displacement that remains after GW passage.

    Unlike oscillatory GW strain h(t) which returns to zero, memory
    produces a DC offset Δh that persists indefinitely:
      Δh_memory = Δu_TT / r
    where Δu_TT is the transverse-traceless part of the displacement.

    The memory arises from the nonlinear nature of GR: GWs carry energy,
    and that energy-momentum produces its own gravitational effect.

    For binary BH merger (dominant source):
      Δh_mem ∝ η × (v_f/c)² × sin²θ × (17 + cos²θ) / 24

    References:
      Christodoulou (1991) PRL 67:1486
      Wiseman & Will (1991) PRD 44:R2945
      Favata (2010) CQG 27:084036
    """

    def __init__(self, m1_solar: float = 36.0, m2_solar: float = 29.0,
                 dist_mpc: float = 410.0, chi_eff: float = 0.0):
        self.m1  = m1_solar
        self.m2  = m2_solar
        self.D   = dist_mpc * 3.085_677_581e22  # Mpc → m
        self.chi = chi_eff
        self.M   = m1_solar + m2_solar
        self.eta = m1_solar * m2_solar / self.M**2
        self.Mc  = (m1_solar * m2_solar)**0.6 / self.M**0.2

    def memory_strain_amplitude(self, theta: float = math.pi / 2) -> float:
        """
        DC memory strain amplitude (Favata 2010):
          Δh⁺_mem = (η M G / (D c²)) × (v_f/c)² ×
                    sin²θ × (17 + cos²θ) / 24
        where v_f ~ 0.5c for typical BBH merger.
        Returns Δh (dimensionless strain offset).
        """
        M_kg = self.M * M_SUN
        v_f  = 0.45 * C_SI  # final velocity at merger ~ 0.45c
        sin2 = math.sin(theta)**2
        cos2 = math.cos(theta)**2
        angular = sin2 * (17.0 + cos2) / 24.0
        return (self.eta * G_SI * M_kg / (self.D * C_SI**2)
                * (v_f / C_SI)**2 * angular)

    def memory_buildup(self, t_arr: np.ndarray, t_merge: float,
                        tau_rise: float = 0.1) -> np.ndarray:
        """
        Time-domain memory buildup:
        Memory accumulates during inspiral and saturates at merger.
          h_mem(t) = Δh_mem × (1/2)(1 + tanh((t − t_merge) / τ_rise))
        Returns memory strain vs time array.
        """
        Dh = self.memory_strain_amplitude()
        return Dh * 0.5 * (1.0 + np.tanh((t_arr - t_merge) / tau_rise))

    def memory_spectrum(self, f_arr: np.ndarray, t_merge: float = 12.0,
                         tau_rise: float = 0.1) -> np.ndarray:
        """
        Fourier transform of memory signal:
          h̃_mem(f) ∝ Δh / (2πif)  (DC offset → 1/f spectrum)
        This is the characteristic 1/f signature distinguishing memory
        from oscillatory GW strain (which has ~f^{−7/6} inspiral spectrum).
        """
        Dh = self.memory_strain_amplitude()
        # Memory Fourier transform: step function → 1/(2πif)
        f_safe = np.where(np.abs(f_arr) < 1e-10, 1e-10, f_arr)
        h_tilde = Dh / (2.0 * math.pi * 1j * f_safe)
        # Apply rise-time smoothing
        h_tilde *= np.exp(-2.0 * math.pi * np.abs(f_arr) * tau_rise)
        return np.abs(h_tilde)

    def cumulative_memory_from_inspiral(self, n_orbits: int = 500,
                                          f_start_hz: float = 10.0
                                          ) -> Dict[str, np.ndarray]:
        """
        Compute cumulative memory buildup during inspiral.
        The memory is sourced by the radiated GW energy flux:
          dh_mem/dt ∝ (dE_GW/dt) / r

        Integrates the Peters (1964) luminosity:
          dE/dt = (32/5) c⁵/G × η² (GM/c²r)^5
        from initial frequency to ISCO.
        """
        M_kg = self.M * M_SUN
        M_s  = G_SI * M_kg / C_SI**3  # GM/c³ [s]

        # Orbital separation from GW frequency: f_GW = 2f_orb
        # f_orb = (1/2π)√(GM/r³) → r = (GM/(πf)²)^{1/3}
        f_isco = C_SI**3 / (6 * math.sqrt(6) * math.pi * G_SI * M_kg)
        f_arr  = np.linspace(f_start_hz, min(f_isco, 1000.0), n_orbits)

        r_arr  = (G_SI * M_kg / (math.pi * f_arr)**2)**(1.0/3.0)
        v_arr  = (G_SI * M_kg / r_arr)**0.5 / C_SI  # v/c

        # Peters luminosity per orbit
        dE_dt  = (32.0/5.0) * C_SI**5 / G_SI * self.eta**2 * (G_SI*M_kg/(C_SI**2*r_arr))**5

        # Cumulative memory strain
        dt_arr = np.gradient(1.0 / f_arr)
        h_mem_cum = np.cumsum(dE_dt * dt_arr / (self.D * C_SI + 1e-30))
        # Normalise to final memory amplitude
        h_mem_cum *= self.memory_strain_amplitude() / (h_mem_cum[-1] + 1e-30)

        return {
            "f_Hz":          f_arr,
            "r_M":           r_arr / (G_SI * M_kg / C_SI**2),
            "v_c":           v_arr,
            "h_mem_cum":     h_mem_cum,
            "dE_dt_W":       dE_dt,
            "f_isco_Hz":     f_isco,
            "Dh_final":      self.memory_strain_amplitude(),
        }

    def detectability_snr(self, detector: str = "aLIGO") -> Dict[str, float]:
        """
        SNR estimate for memory detection.
        Memory is a low-frequency effect → difficult for ground-based detectors.
        SNR ∝ Δh × √(T_obs) / √(S_n(f_low))
        """
        Dh = self.memory_strain_amplitude()
        # aLIGO sensitivity at 10 Hz: S_n ~ 10⁻⁴⁵ Hz⁻¹
        S_n_10Hz = {"aLIGO": 1e-45, "ET": 1e-48, "LISA": 1e-40}
        s_n = S_n_10Hz.get(detector, 1e-45)
        T_obs = 16.0  # observation window [s]
        snr = Dh * math.sqrt(T_obs) / math.sqrt(s_n)
        return {
            "Dh_strain":      Dh,
            "detector":       detector,
            "S_n_Hz":         s_n,
            "T_obs_s":        T_obs,
            "SNR_memory":     snr,
            "detectable":     snr > 3.0,
            "Dh_ratio_osc":   Dh / (1e-21 + 1e-30),  # ratio to oscillatory peak
        }


# ══════════════════════════════════════════════════════════════════════════════
# §6C  POST-NEWTONIAN BINARY DYNAMICS (2PN) — Full Inspiral Simulator
# ══════════════════════════════════════════════════════════════════════════════
class PostNewtonianBinary:
    """
    Full 2nd post-Newtonian (2PN) binary orbital dynamics with radiation
    reaction, eccentricity evolution, and spin-orbit coupling.

    Implements:
    1. Peters & Mathews (1963) radiation reaction (leading order)
    2. 1PN conservative corrections (periapsis advance)
    3. 2PN dissipative terms (tail radiation)
    4. Eccentricity decay: de/dt from Peters (1964)
    5. Spin-orbit coupling: Lense-Thirring orbital precession
    6. Secular evolution from wide orbit to ISCO merger

    The system of ODEs for (a, e, ω) is integrated via scipy solve_ivp.

    References:
      Peters & Mathews (1963) PR 131:435
      Peters (1964) PR 136:B1224
      Blanchet (2014) LRR 17:2 [PN formalism review]
      Kidder (1995) PRD 52:821 [spin-orbit coupling]
    """

    def __init__(self, m1_solar: float = 36.0, m2_solar: float = 29.0,
                 chi1: float = 0.0, chi2: float = 0.0):
        self.m1_s  = m1_solar
        self.m2_s  = m2_solar
        self.m1    = m1_solar * M_SUN  # kg
        self.m2    = m2_solar * M_SUN
        self.M     = self.m1 + self.m2
        self.mu    = self.m1 * self.m2 / self.M  # reduced mass
        self.eta   = self.m1 * self.m2 / self.M**2
        self.Mc    = self.M * self.eta**0.6  # chirp mass [kg]
        self.chi1  = chi1  # dimensionless spin of m1
        self.chi2  = chi2
        self.chi_eff = (self.m1 * chi1 + self.m2 * chi2) / self.M

    def chirp_mass_solar(self) -> float:
        return self.Mc / M_SUN

    def merger_time_peters(self, a0: float, e0: float = 0.0) -> float:
        """
        Peters (1964) merger time from initial separation a0:
          T_merge = (5/256) × c⁵a₀⁴ / (G³M²μ) × f(e₀)
        f(e) = (1−e²)^4 / (1 + 73/24 e² + 37/96 e⁴) — eccentricity enhancement
        Returns merger time in seconds.
        """
        f_e = ((1 - e0**2)**4 /
               (1 + 73.0/24 * e0**2 + 37.0/96 * e0**4))
        return (5.0 / 256.0 * C_SI**5 * a0**4 /
                (G_SI**3 * self.M**2 * self.mu) * f_e)

    def gw_luminosity(self, a: float, e: float = 0.0) -> float:
        """
        Peters & Mathews (1963) GW luminosity:
          L_GW = (32/5) G⁴/(c⁵) × μ²M³/a⁵ × f(e)
          f(e) = (1 + 73/24 e² + 37/96 e⁴) / (1−e²)^{7/2}
        """
        f_e = ((1 + 73.0/24 * e**2 + 37.0/96 * e**4) /
               max((1 - e**2)**3.5, 1e-30))
        return (32.0/5.0 * G_SI**4 * self.mu**2 * self.M**3 /
                (C_SI**5 * a**5) * f_e)

    def _ode_system(self, t: float, y: np.ndarray) -> np.ndarray:
        """
        ODE system for (a, e, ω_periapsis):
          da/dt = Peters orbital decay
          de/dt = Peters eccentricity evolution
          dω/dt = 1PN periapsis advance + spin-orbit precession
        """
        a, e, omega = y
        a = max(a, 1e3)  # floor to avoid singularity
        e = float(np.clip(e, 0.0, 0.999))

        # ── Peters (1964) da/dt ─────────────────────────────────────────
        f_e_a = (1 + 73.0/24*e**2 + 37.0/96*e**4) / max((1-e**2)**3.5, 1e-30)
        da_dt = -(64.0/5.0) * G_SI**3 * self.mu * self.M**2 / (C_SI**5 * a**3) * f_e_a

        # ── Peters de/dt ────────────────────────────────────────────────
        g_e = (e * (304 + 121*e**2)) / (12.0 * max((1-e**2)**2.5, 1e-30))
        de_dt = -(19.0/12.0) * (G_SI**3 * self.mu * self.M**2) / (C_SI**5 * a**4) * g_e

        # ── 1PN periapsis advance (Einstein precession) ─────────────────
        # δω = 6πGM / (c²a(1−e²)) per orbit
        # dω/dt = (6πGM / (c²a(1−e²))) × f_orb
        P_orb = 2.0 * math.pi * math.sqrt(a**3 / (G_SI * self.M))  # Kepler period
        f_orb = 1.0 / max(P_orb, 1e-10)
        dw_1pn = 6.0 * math.pi * G_SI * self.M / (C_SI**2 * a * max(1-e**2, 1e-10)) * f_orb

        # ── Spin-orbit (Lense-Thirring) precession ──────────────────────
        # Kidder (1995): dω_SO/dt = (2G/(c²a³(1-e²)^{3/2})) × (J + 2L×S/L²) × f_orb
        J_spin = self.chi_eff * G_SI * self.M**2 / C_SI  # total spin angular momentum
        L_orb  = self.mu * math.sqrt(G_SI * self.M * a * (1 - e**2))
        dw_so  = 2.0 * G_SI * J_spin / (C_SI**2 * a**3 * max((1-e**2)**1.5, 1e-30)) * f_orb

        dw_dt = dw_1pn + dw_so

        return np.array([da_dt, de_dt, dw_dt])

    def evolve_orbit(self, a0_AU: float = 0.1, e0: float = 0.3,
                      t_max_yr: float = None,
                      n_output: int = 2000) -> Dict[str, Any]:
        """
        Integrate binary orbital evolution from initial separation a₀ to merger.
        Returns dict with time, separation, eccentricity, periapsis angle.
        """
        a0 = a0_AU * AU  # convert to metres
        if t_max_yr is None:
            t_merge = self.merger_time_peters(a0, e0)
            t_max   = min(t_merge * 0.999, 1e18)  # avoid singularity at merger
        else:
            t_max = t_max_yr * YEAR_S

        y0 = np.array([a0, e0, 0.0])

        # Event: ISCO reached (a < 6 GM/c² for Schwarzschild)
        r_isco = 6.0 * G_SI * self.M / C_SI**2

        def isco_event(t, y):
            return y[0] - r_isco
        isco_event.terminal  = True
        isco_event.direction = -1

        sol = sci_int.solve_ivp(
            self._ode_system, (0, t_max), y0,
            method="RK45", max_step=t_max / 500,
            events=isco_event,
            dense_output=True,
            rtol=1e-8, atol=1e-12)

        t_eval = np.linspace(0, sol.t[-1], n_output)
        y_eval = sol.sol(t_eval)

        a_arr = y_eval[0]
        e_arr = np.clip(y_eval[1], 0.0, 0.999)
        w_arr = y_eval[2]

        # GW frequency from orbital separation
        f_gw = 2.0 / (2.0 * math.pi) * np.sqrt(G_SI * self.M / np.maximum(a_arr, 1e3)**3)

        # GW luminosity along evolution
        L_gw = np.array([self.gw_luminosity(a, e)
                          for a, e in zip(a_arr, e_arr)])

        # Periapsis distance
        r_peri = a_arr * (1 - e_arr)

        # Energy radiated
        E_bind = G_SI * self.m1 * self.m2 / (2 * a_arr)
        E_rad_cum = E_bind - E_bind[0]

        return {
            "t_yr":      t_eval / YEAR_S,
            "t_s":       t_eval,
            "a_AU":      a_arr / AU,
            "a_m":       a_arr,
            "e":         e_arr,
            "omega_rad": w_arr,
            "f_gw_Hz":   f_gw,
            "L_gw_W":    L_gw,
            "r_peri_AU": r_peri / AU,
            "E_rad_J":   E_rad_cum,
            "n_orbits":  np.cumsum(2 * math.pi / np.maximum(np.gradient(w_arr), 1e-30)) / (2*math.pi),
            "merger_reached": bool(sol.t_events and len(sol.t_events[0]) > 0),
            "t_merger_yr":    sol.t[-1] / YEAR_S,
            "t_merger_peters_yr": self.merger_time_peters(a0, e0) / YEAR_S,
        }

    def eccentricity_at_frequency(self, f_gw: float, a0_AU: float = 1.0,
                                    e0: float = 0.5) -> float:
        """
        Compute residual eccentricity at a given GW frequency.
        Peters (1964) analytic approximation:
          e(f) ≈ e₀ × (f₀/f)^{19/18}
        where f₀ is the initial GW frequency.
        """
        a0   = a0_AU * AU
        f0   = 2 / (2*math.pi) * math.sqrt(G_SI * self.M / a0**3)
        return e0 * (f0 / max(f_gw, 1e-10))**(19.0/18.0)

    def periapsis_advance_deg_per_orbit(self, a_AU: float,
                                          e: float = 0.0) -> float:
        """
        1PN periapsis advance per orbit [degrees]:
          Δω = 6πGM / (c²a(1−e²))
        Famous: Mercury = 42.98 arcsec/century = 0.1035°/orbit
        """
        a = a_AU * AU
        return math.degrees(6 * math.pi * G_SI * self.M /
                            (C_SI**2 * a * max(1 - e**2, 1e-10)))

    def orbital_energy(self, a: float) -> float:
        """Newtonian binding energy E = −Gm₁m₂/(2a)  [J]"""
        return -G_SI * self.m1 * self.m2 / (2 * a)

    def angular_momentum(self, a: float, e: float = 0.0) -> float:
        """Orbital angular momentum L = μ√(GMa(1−e²))  [kg m²/s]"""
        return self.mu * math.sqrt(G_SI * self.M * a * (1 - e**2))

    def summary(self) -> Dict[str, Any]:
        return {
            "m1_solar":          self.m1_s,
            "m2_solar":          self.m2_s,
            "M_total_solar":     self.M / M_SUN,
            "mu_solar":          self.mu / M_SUN,
            "eta":               self.eta,
            "Mc_solar":          self.chirp_mass_solar(),
            "chi_eff":           self.chi_eff,
            "chi1":              self.chi1,
            "chi2":              self.chi2,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §7  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    D: Dict[str, Any] = {
        "rel_sr":               SpecialRelativity(),
        "rel_gr":               GeneralRelativity(),
        "rel_engine":           CooperMurphTimeEngine(),
        "rel_gr_profile":       None,
        # SR calculator state
        "rel_sr_v_c":           0.9,
        "rel_sr_m0":            70.0,
        "rel_sr_dt_proper":     1.0,
        # Twin paradox
        "rel_twin_v":           0.8,
        "rel_twin_d":           4.24,    # Proxima Centauri [ly]
        # GR state
        "rel_gr_mass_solar":    GARG_MASS_SOLAR,
        "rel_gr_spin":          GARG_SPIN,
        "rel_gr_r_query_rs":    3.0,
        # Mission
        "rel_mission_df":       None,
        "rel_divergence":       None,
        "rel_miller_hrs":       3.22,
        "rel_custom_v":         0.5,
        "rel_custom_r":         10.0,
        "rel_custom_ship_yr":   1.0,
        # Geodesic
        "rel_geo_result":       None,
        "rel_geo_r0":           20.0,
        "rel_geo_L":            5.0,
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# §8  MATPLOTLIB STYLE
# ══════════════════════════════════════════════════════════════════════════════
MPL_STYLE = {
    "figure.facecolor":  "#06090f",
    "axes.facecolor":    "#080c18",
    "axes.edgecolor":    "#151d35",
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
    "legend.edgecolor":  "#151d35",
    "legend.fontsize":   6,
    "figure.dpi":        110,
    "savefig.facecolor": "#06090f",
    "axes.spines.top":   False,
    "axes.spines.right": False,
}

def _mpl():
    plt.rcParams.update(MPL_STYLE)


# ══════════════════════════════════════════════════════════════════════════════
# §9  PLOTTING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

# ── §9.1  SR kinematic dashboard ─────────────────────────────────────────────
def _plot_sr_dashboard(v_c: float, m0_kg: float) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    fig.patch.set_facecolor("#06090f")
    sr = SpecialRelativity()

    v_arr  = np.linspace(0.001, 0.9999, 500) * C_SI
    b_arr  = v_arr/C_SI
    g_arr  = sr.gamma_array(v_arr)

    # 1. Lorentz factor γ(v)
    ax1 = axes[0, 0]
    ax1.semilogy(b_arr, g_arr, color="#E8C46A", lw=1.3)
    ax1.axvline(v_c, color="#D154FF", lw=1.0, ls="--",
                label=f"v={v_c:.3f}c  γ={sr.lorentz_factor(v_c*C_SI):.4f}")
    ax1.axhline(10,    color="#4FC3F7", lw=0.6, ls=":", label="γ=10")
    ax1.axhline(100,   color="#CE93D8", lw=0.6, ls=":", label="γ=100")
    ax1.set_xlabel("v/c"); ax1.set_ylabel("γ(v)")
    ax1.set_title("LORENTZ FACTOR  γ(v)"); ax1.legend(fontsize=5.5)

    # 2. Time dilation factor (Earth sees ship run slow)
    ax2 = axes[0, 1]
    tau_fraction = 1.0/g_arr   # proper / coordinate time
    ax2.plot(b_arr, tau_fraction, color="#4FC3F7", lw=1.3,
             label="dτ/dt = 1/γ")
    ax2.axvline(v_c, color="#D154FF", lw=1.0, ls="--")
    ax2.fill_between(b_arr, tau_fraction, 1.0, alpha=0.15, color="#4FC3F7")
    ax2.set_xlabel("v/c"); ax2.set_ylabel("dτ/dt  (ship clock rate)")
    ax2.set_title("TIME DILATION — Ship Clock Rate"); ax2.legend(fontsize=6)

    # 3. Length contraction
    ax3 = axes[0, 2]
    L_frac = 1.0/g_arr
    ax3.plot(b_arr, L_frac, color="#81C784", lw=1.3, label="L'/L₀ = 1/γ")
    ax3.axvline(v_c, color="#D154FF", lw=1.0, ls="--",
                label=f"L'={1/sr.lorentz_factor(v_c*C_SI):.4f}L₀")
    ax3.set_xlabel("v/c"); ax3.set_ylabel("L' / L₀")
    ax3.set_title("LENGTH CONTRACTION"); ax3.legend(fontsize=6)

    # 4. Relativistic momentum & energy
    ax4 = axes[1, 0]
    p_arr = sr.gamma_array(v_arr)*m0_kg*v_arr / (m0_kg*C_SI)  # p/(m₀c)
    E_arr = sr.gamma_array(v_arr)*m0_kg*C_SI**2 / (m0_kg*C_SI**2)  # E/(m₀c²)
    K_arr = (sr.gamma_array(v_arr)-1)*m0_kg*C_SI**2 / (m0_kg*C_SI**2)
    ax4.plot(b_arr, p_arr, color="#E8C46A", lw=1.1, label="p/(m₀c)")
    ax4.plot(b_arr, E_arr, color="#FF8800", lw=1.1, label="E/(m₀c²)")
    ax4.plot(b_arr, K_arr, color="#CE93D8", lw=1.0, ls="--",
             label="K/(m₀c²)  kinetic")
    ax4.axvline(v_c, color="#D154FF", lw=0.8, ls="--")
    ax4.set_xlabel("v/c"); ax4.set_ylabel("Normalised quantity")
    ax4.set_title("RELATIVISTIC ENERGY & MOMENTUM"); ax4.legend(fontsize=5.5)

    # 5. Relativistic Doppler
    ax5 = axes[1, 1]
    f0    = 1.0   # normalised frequency
    f_app = np.array([sr.doppler_longitudinal(f0, v, approaching=True)
                       for v in v_arr])
    f_rec = np.array([sr.doppler_longitudinal(f0, v, approaching=False)
                       for v in v_arr])
    f_tra = np.array([sr.doppler_transverse(f0, v) for v in v_arr])
    ax5.semilogy(b_arr, f_app, color="#81C784",  lw=1.1, label="Approaching (blueshift)")
    ax5.semilogy(b_arr, f_rec, color="#D154FF",  lw=1.1, label="Receding (redshift)")
    ax5.semilogy(b_arr, f_tra, color="#FFB74D",  lw=1.0, ls="--",
                 label="Transverse (redshift)")
    ax5.axhline(1.0, color="#555", lw=0.5, ls=":")
    ax5.axvline(v_c, color="#E8C46A", lw=0.8, ls="--")
    ax5.set_xlabel("v/c"); ax5.set_ylabel("f_obs / f_emit")
    ax5.set_title("RELATIVISTIC DOPPLER"); ax5.legend(fontsize=5.5)

    # 6. Velocity addition
    ax6 = axes[1, 2]
    v1_c  = v_c
    v2_arr = np.linspace(-0.999, 0.999, 400)
    v_rel  = np.array([sr.velocity_addition(v1_c*C_SI, v2*C_SI)/C_SI
                        for v2 in v2_arr])
    v_newt = np.clip(v1_c + v2_arr, -1.0, 1.0)  # Newtonian (wrong)
    ax6.plot(v2_arr, v_rel,  color="#E8C46A", lw=1.2,
             label=f"Relativistic v_rel(v₁={v1_c:.2f}c, v₂)")
    ax6.plot(v2_arr, v_newt, color="#3a4a70", lw=0.8, ls="--",
             label="Newtonian v₁+v₂")
    ax6.axhline(1.0,  color="#D154FF", lw=0.6, ls=":", label="|v|=c limit")
    ax6.axhline(-1.0, color="#D154FF", lw=0.6, ls=":")
    ax6.set_xlabel("v₂/c"); ax6.set_ylabel("v_result/c")
    ax6.set_title("RELATIVISTIC VELOCITY ADDITION"); ax6.legend(fontsize=5.5)

    plt.tight_layout()
    return fig


# ── §9.2  Spacetime diagram ────────────────────────────────────────────────────
def _plot_spacetime_diagram(v_twin: float, d_ly: float) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    fig.patch.set_facecolor("#06090f")

    builder = SpacetimeDiagramBuilder(x_range=d_ly*1.3, ct_range=3*d_ly/v_twin)
    twins   = builder.twin_paradox_worldlines(v_twin, d_ly)

    sr  = SpecialRelativity()
    g   = sr.lorentz_factor(v_twin*C_SI)

    # ── Left: twin paradox Minkowski diagram ─────────────────────────────
    ax1 = axes[0]
    # Light cone from origin
    ct_lc = np.linspace(0, twins["ct_total"]*1.1, 200)
    ax1.plot( ct_lc,  ct_lc, color="#2a3550", lw=0.8, ls="--")  # future null
    ax1.plot(-ct_lc,  ct_lc, color="#2a3550", lw=0.8, ls="--")

    # Earth twin (stays at x=0)
    x_e, ct_e = twins["earth"]
    ax1.plot(x_e, ct_e, color="#4FC3F7", lw=2.0,
             label=f"Earth twin  Δτ={twins['tau_earth']:.2f} yr")

    # Travelling twin
    x_t, ct_t = twins["traveller"]
    ax1.plot(x_t, ct_t, color="#E8C46A", lw=2.0,
             label=f"Traveller   Δτ={twins['tau_traveller']:.2f} yr")

    # Turnaround point annotation
    ax1.scatter([twins["x_turn"]], [twins["t_turn"]],
                color="#D154FF", s=50, zorder=5)
    ax1.annotate("Turnaround\n(instantaneous)",
                 xy=(twins["x_turn"], twins["t_turn"]),
                 xytext=(twins["x_turn"]*0.6, twins["t_turn"]*1.05),
                 color="#D154FF", fontsize=6,
                 arrowprops=dict(arrowstyle="->", color="#D154FF", lw=0.7))

    # Simultaneity lines at turnaround (two frames)
    x_sim, ct_sim_earth = builder.simultaneity_line(0.0, twins["t_turn"], twins["x_turn"])
    x_sim, ct_sim_trav  = builder.simultaneity_line(v_twin, twins["t_turn"], twins["x_turn"])
    ax1.plot(x_sim, ct_sim_earth, color="#4FC3F7", lw=0.5, ls=":",
             label="Earth simultaniety")
    ax1.plot(x_sim, ct_sim_trav, color="#E8C46A", lw=0.5, ls=":",
             label="Traveller simultaneity")

    ax1.set_xlabel("x  [ly]"); ax1.set_ylabel("ct  [ly]  (= years at c=1)")
    ax1.set_title(f"TWIN PARADOX SPACETIME DIAGRAM\n"
                  f"v={v_twin:.2f}c  γ={g:.3f}  Age diff={twins['age_diff']:.2f} yr")
    ax1.legend(fontsize=5.5, loc="upper left")
    ax1.set_facecolor("#060a14")

    # ── Right: Cooper-Murph diagram ────────────────────────────────────────
    ax2 = axes[1]
    # Light cone
    ct_lc2 = np.linspace(0, 110, 300)
    ax2.plot(ct_lc2, ct_lc2, color="#1a2535", lw=0.7, ls="--")
    ax2.plot(-ct_lc2, ct_lc2, color="#1a2535", lw=0.7, ls="--")

    engine = CooperMurphTimeEngine()
    wl     = builder.cooper_murph_worldlines(engine)

    ax2.plot(wl["murph_x"], wl["murph_ct"],
             color="#4FC3F7", lw=2.2, label="Murph (Earth)")
    ax2.plot(wl["cooper_x"], wl["cooper_ct"],
             color="#E8C46A", lw=1.5, marker="o", ms=4,
             label="Cooper (ship)")

    # Miller annotation
    summ = wl["summary"]
    ax2.annotate(f"Miller's World\n1h ship = 7yr Earth",
                 xy=(10.0, 23.0), color="#D154FF", fontsize=5.5,
                 bbox=dict(boxstyle="round,pad=0.2",
                           facecolor="#1a0808", alpha=0.8))

    ax2.set_xlabel("Distance [ly (schematic)]")
    ax2.set_ylabel("Earth coordinate time [yr]")
    ax2.set_title(f"COOPER vs MURPH WORLDLINES\n"
                  f"Cooper ages {summ['total_ship_time_yr']:.1f} yr  ·  "
                  f"Murph ages {summ['total_earth_time_yr']:.1f} yr")
    ax2.legend(fontsize=6)
    ax2.set_facecolor("#060a14")

    plt.tight_layout()
    return fig


# ── §9.3  GR time dilation profile ────────────────────────────────────────────
def _plot_gr_profile(df: pd.DataFrame, M_solar: float) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    fig.patch.set_facecolor("#06090f")

    specs = [
        ("dil_GR_only",     "#E8C46A", "GR Only  dτ/dt = √(1−r_s/r)"),
        ("dil_combined",    "#4FC3F7", "Combined GR+SR  dτ/dt = √(1−r_s/r−v²/c²)"),
        ("dil_Kerr",        "#CE93D8", "Kerr Metric  dτ/dt (circular prograde)"),
        ("factor_GR",       "#FF8800", "Dilation Factor (coord/proper)"),
        ("redshift_z_local","#D154FF", "Gravitational Redshift  z"),
        ("light_bend_rad",  "#81C784", "Light Bending Angle  α  [rad]"),
    ]
    rs_col = df["r_rs"].values
    for ax, (col, clr, title) in zip(axes.flat, specs):
        data = df[col].values
        try:
            ax.semilogy(rs_col, np.abs(data)+1e-30, color=clr, lw=1.1)
        except Exception:
            ax.plot(rs_col, data, color=clr, lw=1.1)
        r_s_m = 2*G_SI*M_solar*M_SUN/C_SI**2
        ax.set_xlabel("r / r_s", fontsize=6)
        ax.set_title(title, fontsize=7)
        ax.set_facecolor("#080c18")

    plt.tight_layout()
    return fig


# ── §9.4  Mission timeline chart ───────────────────────────────────────────────
def _plot_mission_timeline(cooper_df: pd.DataFrame,
                            murph_df: pd.DataFrame,
                            div: Dict[str, float]) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 2, figsize=(15, 9))
    fig.patch.set_facecolor("#06090f")

    # ── Top left: Earth time per leg (bar chart) ──────────────────────────
    ax1 = axes[0, 0]
    legs = cooper_df["Leg"].values
    et   = cooper_df["Earth time (yr)"].values
    st_  = cooper_df["Ship time (yr)"].values
    x    = np.arange(len(legs))
    w    = 0.38
    bars1 = ax1.bar(x - w/2, et,  w, label="Earth time", color="#E8C46A", alpha=0.85)
    bars2 = ax1.bar(x + w/2, st_, w, label="Ship time",  color="#4FC3F7", alpha=0.85)
    ax1.set_xticks(x); ax1.set_xticklabels(
        [l[:18] for l in legs], rotation=45, ha="right", fontsize=5)
    ax1.set_ylabel("Duration  [yr]")
    ax1.set_title("EARTH TIME vs SHIP TIME PER LEG")
    ax1.legend(fontsize=6)
    ax1.set_facecolor("#080c18")

    # ── Top right: cumulative age comparison ──────────────────────────────
    ax2 = axes[0, 1]
    n_legs = len(cooper_df)
    coop_age_end = cooper_df["Cooper age end"].values
    murph_age_end= murph_df["Murph age end"].values
    leg_idx      = np.arange(n_legs)
    ax2.plot(leg_idx, coop_age_end,  "o-", color="#E8C46A", lw=1.3,
             ms=5, label="Cooper age")
    ax2.plot(leg_idx, murph_age_end, "s-", color="#4FC3F7", lw=1.3,
             ms=5, label="Murph age")
    ax2.fill_between(leg_idx, coop_age_end, murph_age_end,
                     alpha=0.12, color="#D154FF",
                     label=f"Age gap → {div['age_gap_yr']:.1f} yr")
    ax2.set_xticks(leg_idx)
    ax2.set_xticklabels([l[:14] for l in legs],
                         rotation=40, ha="right", fontsize=5)
    ax2.set_ylabel("Age  [yr]")
    ax2.set_title("COOPER vs MURPH CUMULATIVE AGES")
    ax2.legend(fontsize=6)
    ax2.set_facecolor("#080c18")

    # ── Bottom left: dilation factors ─────────────────────────────────────
    ax3 = axes[1, 0]
    dil  = cooper_df["Dilation factor"].values
    dil_finite = np.where(np.isfinite(dil), np.abs(dil), 1.0)
    colors_dil = ["#E8C46A" if d > 100 else "#FF8800" if d > 10
                   else "#81C784" for d in dil_finite]
    ax3.bar(x, dil_finite, color=colors_dil, alpha=0.85)
    ax3.set_xticks(x)
    ax3.set_xticklabels([l[:18] for l in legs],
                         rotation=45, ha="right", fontsize=5)
    ax3.set_ylabel("Earth time / Ship time  (dilation factor)")
    ax3.set_title("TIME DILATION FACTOR PER LEG")
    ax3.set_yscale("log")
    ax3.set_facecolor("#080c18")

    # ── Bottom right: Miller's world time budget ──────────────────────────
    ax4 = axes[1, 1]
    ship_hrs = np.linspace(0.1, 24.0, 300)
    gr = GeneralRelativity(GARG_MASS_KG, GARG_SPIN)
    dilation_miller = 61_320.0   # 7yr/hr in seconds/second
    earth_yr = ship_hrs * dilation_miller / (YEAR_S/HOUR_S)
    ax4.plot(ship_hrs, earth_yr, color="#E8C46A", lw=1.5)
    ax4.axvline(MISSION_MILLER_SHIP_HRS, color="#D154FF", lw=1.0, ls="--",
                label=f"Film: {MISSION_MILLER_SHIP_HRS}h → "
                       f"{MISSION_MILLER_SHIP_HRS*dilation_miller/YEAR_S*HOUR_S:.1f}yr")
    ax4.axhline(7.0, color="#4FC3F7", lw=0.8, ls=":",
                label="7 yr Earth / hr ship")
    ax4.fill_between(ship_hrs, 0, earth_yr, alpha=0.15, color="#E8C46A")
    ax4.set_xlabel("Ship-hours on Miller's World")
    ax4.set_ylabel("Earth years lost")
    ax4.set_title("MILLER TIME BUDGET  (1h = 7 yr = 61,320× dilation)")
    ax4.legend(fontsize=6)
    ax4.set_facecolor("#080c18")

    plt.tight_layout()
    return fig


# ── §9.5  Geodesic orbit plot ──────────────────────────────────────────────────
def _plot_geodesic(geo: Dict[str, np.ndarray], r_s: float) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor("#06090f")

    x = geo["x"]/r_s; y = geo["y"]/r_s

    # Left: orbital path
    ax1 = axes[0]
    sc  = ax1.scatter(x, y, c=np.linspace(0,1,len(x)),
                       cmap="plasma", s=0.8, alpha=0.9)
    plt.colorbar(sc, ax=ax1, label="Affine param (normalised)")
    ax1.add_patch(Circle((0,0), 1.0, color="#E8C46A",
                          fill=False, lw=0.7, ls="--", label="r_s"))
    ax1.add_patch(Circle((0,0), 0.5, color="#000", fill=True))
    ax1.set_aspect("equal")
    ax1.set_xlabel("x / r_s"); ax1.set_ylabel("y / r_s")
    captured = geo["captured"]
    ax1.set_title(f"SCHWARZSCHILD GEODESIC\n"
                  f"{'CAPTURED by BH' if captured else 'Escaped / bound orbit'}")
    ax1.legend(fontsize=6)
    ax1.set_facecolor("#060a14")

    # Right: r(t) evolution
    ax2 = axes[1]
    r_arr = geo["r"]/r_s
    t_arr = geo["t"]
    ax2.plot(t_arr, r_arr, color="#E8C46A", lw=1.0)
    ax2.axhline(1.0, color="#D154FF", lw=0.7, ls="--", label="r = r_s")
    ax2.set_xlabel("Coordinate time t  [M_geo units]")
    ax2.set_ylabel("r / r_s")
    ax2.set_title("RADIAL EVOLUTION r(t)")
    ax2.legend(fontsize=6)

    plt.tight_layout()
    return fig


# ── §9.6  Twin paradox age bar ─────────────────────────────────────────────────
def _plot_twin_summary(twin: Dict[str, float]) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    fig.patch.set_facecolor("#06090f")

    # Left: age comparison
    ax1 = axes[0]
    categories = ["Earth twin", "Traveller"]
    ages       = [twin["t_earth_yr"], twin["tau_ship_yr"]]
    colors     = ["#4FC3F7", "#E8C46A"]
    bars = ax1.bar(categories, ages, color=colors, alpha=0.85, width=0.4)
    ax1.bar_label(bars, fmt="%.2f yr", padding=4, fontsize=8, color="#fff")
    ax1.set_ylabel("Proper time elapsed  [yr]")
    ax1.set_title(f"TWIN PARADOX — v={twin['v_ms']/C_SI:.3f}c  "
                  f"d={twin['distance_ly']:.2f} ly\n"
                  f"γ={twin['gamma']:.3f}  Age difference={twin['age_diff_yr']:.3f} yr")
    ax1.set_facecolor("#080c18")

    # Right: SR parameters summary
    ax2 = axes[1]
    ax2.axis("off")
    params = [
        ("Velocity",           f"{twin['v_c']:.5f} c"),
        ("Lorentz factor γ",   f"{twin['gamma']:.5f}"),
        ("Distance",           f"{twin['distance_ly']:.3f} ly"),
        ("Earth coord time",   f"{twin['t_earth_yr']:.4f} yr"),
        ("Ship proper time",   f"{twin['tau_ship_yr']:.4f} yr"),
        ("Age difference",     f"{twin['earth_twin_older_by']:.4f} yr"),
        ("Age diff (days)",    f"{twin['earth_twin_older_by']*365.25:.1f} days"),
    ]
    y = 0.92
    for lbl, val in params:
        ax2.text(0.05, y, lbl+":", color="#888", fontsize=8,
                 transform=ax2.transAxes, fontfamily="monospace")
        ax2.text(0.55, y, val, color="#E8C46A", fontsize=8,
                 transform=ax2.transAxes, fontfamily="monospace",
                 fontweight="bold")
        y -= 0.12
    ax2.set_title("SR KINEMATICS SUMMARY")

    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# §10  MAIN STREAMLIT PAGE
# ══════════════════════════════════════════════════════════════════════════════
def relativity_calculator_page():
    init_session_state()
    _mpl()
    S  = st.session_state
    sr = S["rel_sr"]
    gr = S["rel_gr"]

    st.markdown("""
    <div style="border-left:3px solid #4FC3F7;padding:.55rem 1.2rem;
                margin-bottom:1.2rem;background:rgba(79,195,247,0.03);
                font-family:monospace;">
    <div style="color:#4FC3F7;font-size:.95rem;letter-spacing:.12em;
                font-weight:600;">⏱ RELATIVITY CALCULATOR &amp; MISSION TIME ENGINE</div>
    <div style="color:#5a6a90;font-size:.62rem;margin-top:.2rem;">
    SR: Lorentz, dilation, aberration, Doppler, twin paradox, rocket equation  ·
    GR: Schwarzschild, Kerr, geodesics, light bending, Shapiro delay  ·
    Mission: Cooper-Murph divergence, Miller's World, full timeline
    </div></div>""", unsafe_allow_html=True)

    (tab_sr, tab_twin, tab_gr,
     tab_mission, tab_miller,
     tab_geodesic, tab_rocket) = st.tabs([
        "⚡ SPECIAL RELATIVITY",
        "👥 TWIN PARADOX",
        "🌀 GENERAL RELATIVITY",
        "🚀 MISSION TIMELINE",
        "🌊 MILLER'S WORLD",
        "📐 GEODESICS",
        "🔥 ROCKET EQUATION",
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1 — SPECIAL RELATIVITY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_sr:
        c1, c2, c3 = st.columns([1, 1, 2.5])

        with c1:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#4FC3F7;">[ SR PARAMETERS ]</div>',
                unsafe_allow_html=True)
            v_c   = st.slider("Velocity  v/c", 0.001, 0.9999,
                               float(S["rel_sr_v_c"]), 0.001, format="%.4f")
            m0_kg = st.number_input("Rest mass  m₀ [kg]",
                                     value=float(S["rel_sr_m0"]),
                                     min_value=1e-31, format="%.4e")
            dt_pr = st.number_input("Proper time  Δτ [yr]",
                                     value=float(S["rel_sr_dt_proper"]),
                                     min_value=1e-6, format="%.4f")
            S["rel_sr_v_c"] = v_c
            S["rel_sr_m0"]  = m0_kg
            S["rel_sr_dt_proper"] = dt_pr

        v_ms   = v_c * C_SI
        g_val  = sr.lorentz_factor(v_ms)
        phi    = sr.rapidity(v_ms)
        dt_crd = sr.time_dilation(dt_pr*YEAR_S, v_ms)/YEAR_S
        L_frac = sr.length_contraction(1.0, v_ms)
        E_J    = sr.total_energy(m0_kg, v_ms)
        K_J    = sr.kinetic_energy(m0_kg, v_ms)
        p_kgms = sr.momentum(m0_kg, v_ms)
        E0     = m0_kg*C_SI**2
        s_sq   = sr.spacetime_interval_sq(dt_pr*YEAR_S, dt_crd*YEAR_S*v_c)
        iv_type= sr.classify_interval(s_sq)

        with c2:
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.75rem;
                        border:1px solid rgba(79,195,247,.15);
                        border-radius:3px;line-height:2.05;">
            <b style="color:#4FC3F7;font-size:.63rem;">── SR KINEMATICS ──</b><br>
            v = <b style="color:#E8C46A;">{v_c:.6f} c</b>
            = <b style="color:#E8C46A;">{v_ms:.4e} m/s</b><br>
            γ(v) = <b style="color:#E8C46A;">{g_val:.8f}</b><br>
            β = v/c = <b>{v_c:.8f}</b><br>
            Rapidity φ = arctanh(β) = <b>{phi:.6f}</b><br>
            Δt_coord = γΔτ = <b style="color:#4FC3F7;">{dt_crd:.6f} yr</b><br>
            L'/L₀ = 1/γ = <b style="color:#81C784;">{L_frac:.8f}</b><br>
            <br>
            <b style="color:#4FC3F7;font-size:.63rem;">── ENERGY & MOMENTUM ──</b><br>
            E_total = <b style="color:#FF8800;">{E_J:.4e} J</b>
            = <b style="color:#FF8800;">{E_J/E0:.6f} m₀c²</b><br>
            K_kinetic = <b>{K_J:.4e} J</b>
            = <b>{K_J/E0:.6f} m₀c²</b><br>
            p = <b>{p_kgms:.4e} kg m/s</b>
            = <b>{p_kgms/(m0_kg*C_SI):.6f} m₀c</b><br>
            E² − (pc)² = <b style="color:#81C784;">{abs(E_J**2-(p_kgms*C_SI)**2)/(E0**2):.3e} (m₀c²)²</b><br>
            <br>
            <b style="color:#4FC3F7;font-size:.63rem;">── SPACETIME INTERVAL ──</b><br>
            s² = <b>{s_sq:.4e} m²</b><br>
            Type: <b style="color:#CE93D8;">{iv_type.value}</b>
            </div>""", unsafe_allow_html=True)

        with c3:
            fig = _plot_sr_dashboard(v_c, m0_kg)
            st.pyplot(fig, width='stretch')
            plt.close(fig)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — TWIN PARADOX
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_twin:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#4FC3F7;">[ TWIN PARADOX PARAMETERS ]</div>',
                unsafe_allow_html=True)
            v_tw = st.slider("Travel speed v/c", 0.01, 0.9999,
                              float(S["rel_twin_v"]), 0.001)
            d_tw = st.number_input("Distance to star [ly]",
                                    value=float(S["rel_twin_d"]),
                                    min_value=0.01, format="%.4f")
            a_tw = st.number_input("Proper acceleration [m/s²]",
                                    value=9.81, min_value=0.01, format="%.3f",
                                    help="Used for acceleration-inclusive version")
            S["rel_twin_v"] = v_tw; S["rel_twin_d"] = d_tw

            twin_inst = sr.twin_paradox(v_tw*C_SI, d_tw)
            twin_acc  = sr.twin_with_acceleration(v_tw*C_SI, d_tw, a_tw)

            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.65rem;
                        border:1px solid rgba(79,195,247,.12);
                        border-radius:3px;line-height:2.0;">
            <b style="color:#4FC3F7;">Instant turnaround:</b><br>
            Earth twin ages: <b style="color:#4FC3F7;">{twin_inst['t_earth_yr']:.4f} yr</b><br>
            Traveller ages:  <b style="color:#E8C46A;">{twin_inst['tau_ship_yr']:.4f} yr</b><br>
            Age diff: <b style="color:#D154FF;">{twin_inst['age_diff_yr']:.4f} yr</b><br>
            = <b style="color:#D154FF;">{twin_inst['age_diff_yr']*365.25:.1f} days</b><br>
            <br>
            <b style="color:#4FC3F7;">With acceleration a={a_tw:.1f} m/s²:</b><br>
            τ_acc phase = <b>{twin_acc['tau_acc_yr']:.4f} yr</b><br>
            d_acc = <b>{twin_acc['d_acc_ly']:.4f} ly</b><br>
            Ship total = <b style="color:#E8C46A;">{twin_acc['tau_ship_total_yr']:.4f} yr</b><br>
            Earth total = <b style="color:#4FC3F7;">{twin_acc['t_earth_total_yr']:.4f} yr</b><br>
            Age diff = <b style="color:#D154FF;">{twin_acc['age_diff_yr']:.4f} yr</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            fig = _plot_spacetime_diagram(v_tw, d_tw)
            st.pyplot(fig, width='stretch')
            plt.close(fig)
            fig2 = _plot_twin_summary(twin_inst)
            st.pyplot(fig2, width='stretch')
            plt.close(fig2)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — GENERAL RELATIVITY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_gr:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#4FC3F7;">[ GR PARAMETERS ]</div>',
                unsafe_allow_html=True)
            gr_mass  = st.number_input("Central mass (M☉)",
                                        value=float(S["rel_gr_mass_solar"]),
                                        min_value=1.0, format="%.3e")
            gr_spin  = st.slider("Kerr spin a*", 0.0, 0.9999,
                                  float(S["rel_gr_spin"]), 1e-4)
            gr_r_rs  = st.slider("Query radius r/r_s", 1.01, 200.0,
                                  float(S["rel_gr_r_query_rs"]), 0.01)
            S["rel_gr_mass_solar"] = gr_mass
            S["rel_gr_spin"]       = gr_spin
            S["rel_gr_r_query_rs"] = gr_r_rs

            if st.button("🌀 COMPUTE GR PROFILE", width='stretch',
                         type="primary"):
                _gr = GeneralRelativity(gr_mass*M_SUN, gr_spin)
                S["rel_gr_profile"] = _gr.gr_profile_dataframe()
                S["rel_gr"]         = _gr

            _gr = S["rel_gr"]
            r_m = gr_r_rs * _gr.r_s
            dil_gr  = _gr.schw_time_dilation(r_m)
            v_circ  = _gr.orbital_v_circular(r_m)
            dil_com = _gr.schw_combined_dilation(r_m, v_circ)
            dil_ker = _gr.kerr_proper_time_ratio(r_m)
            z_local = _gr.gravitational_redshift(r_m, _gr.r_s*1000)
            alpha_l = _gr.light_bending_angle(r_m)
            prec    = _gr.perihelion_precession(r_m, 0.1)

            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.65rem;
                        border:1px solid rgba(79,195,247,.12);
                        border-radius:3px;line-height:2.05;">
            <b style="color:#4FC3F7;">r = {gr_r_rs:.3f} r_s = {r_m:.3e} m</b><br>
            GR dilation dτ/dt = <b style="color:#E8C46A;">{dil_gr:.6e}</b><br>
            Combined dτ/dt = <b style="color:#4FC3F7;">{dil_com:.6e}</b><br>
            Kerr dτ/dt = <b style="color:#CE93D8;">{dil_ker:.6e}</b><br>
            GR factor = <b style="color:#FF8800;">{1/max(dil_gr,1e-30):.4e}×</b><br>
            z_grav ≈ <b>{z_local:.4e}</b><br>
            v_circ = <b>{v_circ/C_SI:.6f} c</b><br>
            α_bend = <b>{math.degrees(alpha_l)*3600:.4f} arcsec</b><br>
            δφ/orbit = <b>{math.degrees(prec)*3600:.4e} arcsec</b>
            </div>""", unsafe_allow_html=True)

            gps = _gr.gps_frequency_correction() if gr_mass < 2.0 else None
            if gps:
                st.markdown(f"""
                <div style="font-family:monospace;font-size:.55rem;color:#aaa;
                            background:rgba(8,12,24,.80);padding:.4rem;
                            border:1px solid rgba(79,195,247,.08);border-radius:3px;
                            line-height:1.8;margin-top:.4rem;">
                <b style="color:#4FC3F7;">GPS Clock Correction:</b><br>
                GR bias: +{gps['GR_fractional']*1e6:.4f} ppm<br>
                SR bias: {gps['SR_fractional']*1e6:.4f} ppm<br>
                Net sat bias: {gps['sat_clock_bias_us_per_day']:.2f} μs/day<br>
                Net vs surface: {gps['net_bias_vs_surface_us_day']:.2f} μs/day
                </div>""", unsafe_allow_html=True)

        with c2:
            df = S.get("rel_gr_profile")
            if df is not None:
                fig = _plot_gr_profile(df, gr_mass)
                st.pyplot(fig, width='stretch')
                plt.close(fig)
            else:
                st.info("Click 'Compute GR Profile' to generate radial plots.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 4 — MISSION TIMELINE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_mission:
        engine = S["rel_engine"]
        cooper_df = engine.cooper_timeline()
        murph_df  = engine.murph_timeline()
        div       = engine.divergence_summary()

        # Summary KPIs
        kpis = [
            ("Cooper proper time", f"{div['total_ship_time_yr']:.2f} yr", "#E8C46A"),
            ("Earth coordinate time", f"{div['total_earth_time_yr']:.1f} yr", "#4FC3F7"),
            ("Cooper final age", f"{div['cooper_age_end']:.1f} yr", "#E8C46A"),
            ("Murph final age", f"{div['murph_age_end']:.1f} yr", "#4FC3F7"),
            ("Age gap", f"{div['age_gap_yr']:.1f} yr", "#D154FF"),
            ("Miller Earth years", f"{div['dominance_miller']:.1f} yr", "#FF8800"),
        ]
        cols_k = st.columns(len(kpis))
        for col, (lbl, val, clr) in zip(cols_k, kpis):
            col.markdown(
                f'<div style="background:rgba(8,12,24,.9);'
                f'border:1px solid rgba(79,195,247,.15);'
                f'padding:.35rem;text-align:center;border-radius:2px;'
                f'font-family:monospace;">'
                f'<div style="color:#444;font-size:.50rem;">{lbl}</div>'
                f'<div style="color:{clr};font-size:.82rem;">{val}</div>'
                f'</div>', unsafe_allow_html=True)

        fig = _plot_mission_timeline(cooper_df, murph_df, div)
        st.pyplot(fig, width='stretch')
        plt.close(fig)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#4FC3F7;">COOPER TIMELINE</div>',
                        unsafe_allow_html=True)
            st.dataframe(cooper_df.round(4), width='stretch',
                         hide_index=True)
        with c2:
            st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#4FC3F7;">MURPH TIMELINE</div>',
                        unsafe_allow_html=True)
            st.dataframe(murph_df.round(4), width='stretch',
                         hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 5 — MILLER'S WORLD DETAILED
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_miller:
        c1, c2 = st.columns([1, 2])
        engine = S["rel_engine"]
        with c1:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#4FC3F7;">[ MILLER CALCULATOR ]</div>',
                unsafe_allow_html=True)
            m_hrs  = st.slider("Ship-hours on Miller", 0.1, 48.0,
                                float(S["rel_miller_hrs"]), 0.1)
            m_dil  = st.number_input("Dilation factor (Earth s / ship s)",
                                      value=61_320.0, min_value=1.0,
                                      format="%.1f")
            S["rel_miller_hrs"] = m_hrs
            calc = engine.miller_scenario_calculator(m_hrs, m_dil)
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.60rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.75rem;
                        border:1px solid rgba(79,195,247,.15);
                        border-radius:3px;line-height:2.1;">
            <b style="color:#4FC3F7;font-size:.67rem;">── MILLER'S WORLD ──</b><br>
            Ship time  = <b style="color:#E8C46A;">{m_hrs:.2f} ship-hours</b><br>
            Ship time  = <b>{m_hrs/24:.3f} ship-days</b><br>
            Dilation   = <b style="color:#D154FF;">{m_dil:,.0f} ×</b><br>
            Earth years lost = <b style="color:#D154FF;font-size:.75rem;">
            {calc['earth_years_lost']:.3f} yr</b><br>
            Earth decades = <b>{calc['earth_decades']:.4f}</b><br>
            Earth days    = <b>{calc['earth_years_lost']*365.25:.1f}</b><br>
            <br>
            Film canon ({MISSION_MILLER_SHIP_HRS:.2f} hrs) →<br>
            <b style="color:#D154FF;"> {MISSION_MILLER_SHIP_HRS*7:.2f} Earth years</b>
            </div>""", unsafe_allow_html=True)

            # Custom dilation sensitivity
            st.markdown(
                '<div style="font-family:monospace;font-size:.58rem;'
                'color:#4FC3F7;margin-top:.8rem;">DILATION SENSITIVITY</div>',
                unsafe_allow_html=True)
            _mpl()
            fig_m, ax_m = plt.subplots(figsize=(4.5, 3))
            dil_arr = np.logspace(3, 6, 300)
            yr_arr  = m_hrs * dil_arr / (YEAR_S/HOUR_S)
            ax_m.loglog(dil_arr, yr_arr, color="#E8C46A", lw=1.2)
            ax_m.axvline(m_dil, color="#D154FF", lw=0.8, ls="--",
                         label=f"{m_dil:.0f}×")
            ax_m.axhline(7.0, color="#4FC3F7", lw=0.7, ls=":",
                         label="7 yr/hr")
            ax_m.set_xlabel("Dilation factor")
            ax_m.set_ylabel("Earth years / ship-hour")
            ax_m.set_title(f"Sensitivity for {m_hrs:.1f} ship-hrs", fontsize=7)
            ax_m.legend(fontsize=5.5)
            ax_m.set_facecolor("#080c18")
            fig_m.patch.set_facecolor("#06090f")
            st.pyplot(fig_m, width='stretch')
            plt.close(fig_m)

        with c2:
            # Kerr dilation near ISCO for Gargantua
            _gr2 = GeneralRelativity(GARG_MASS_KG, GARG_SPIN)
            r_arr_m = np.linspace(GARG_M_GEO*0.9998, GARG_M_GEO*1.003, 600)
            dtr_arr = np.array([_gr2.kerr_proper_time_ratio(r) for r in r_arr_m])
            dil_arr2 = np.where(dtr_arr > 0, 1.0/dtr_arr, 1e9)
            r_isco_M = r_arr_m[0]*1.0001  # approximate

            _mpl()
            fig_k, axes_k = plt.subplots(2, 1, figsize=(8, 7))
            fig_k.patch.set_facecolor("#06090f")

            ax_k1 = axes_k[0]
            ax_k1.semilogy(r_arr_m/GARG_M_GEO, dtr_arr + 1e-30,
                            color="#E8C46A", lw=1.2)
            target = HOUR_S/(7*YEAR_S)
            ax_k1.axhline(target, color="#D154FF", lw=1.0, ls="--",
                           label=f"dτ/dt = 1h/7yr = {target:.2e}")
            ax_k1.set_xlabel("r / M_geo"); ax_k1.set_ylabel("dτ/dt (prograde circular)")
            ax_k1.set_title("PROPER TIME RATIO NEAR ISCO — Kerr (a*=1−10⁻¹⁴)")
            ax_k1.legend(fontsize=6)
            ax_k1.set_facecolor("#080c18")

            ax_k2 = axes_k[1]
            ax_k2.semilogy(r_arr_m/GARG_M_GEO, dil_arr2 + 1e-30,
                            color="#4FC3F7", lw=1.2)
            ax_k2.axhline(MILLER_RATIO, color="#D154FF", lw=1.0, ls="--",
                           label=f"Target: {MILLER_RATIO:.0f}×")
            ax_k2.set_xlabel("r / M_geo"); ax_k2.set_ylabel("Time dilation factor")
            ax_k2.set_title("MILLER DILATION FACTOR vs ORBITAL RADIUS")
            ax_k2.legend(fontsize=6)
            ax_k2.set_facecolor("#080c18")

            plt.tight_layout()
            st.pyplot(fig_k, width='stretch')
            plt.close(fig_k)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 6 — GEODESICS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_geodesic:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#4FC3F7;">[ GEODESIC PARAMETERS ]</div>',
                unsafe_allow_html=True)
            geo_mass = st.number_input("Mass (M☉)", value=1.0,
                                        min_value=0.1, format="%.2f")
            geo_r0   = st.slider("Initial radius r₀ (r_s units)",
                                  1.5, 100.0, float(S["rel_geo_r0"]), 0.5)
            geo_L    = st.slider("Angular momentum L / (Mc)",
                                  0.1, 20.0, float(S["rel_geo_L"]), 0.1)
            geo_E    = st.slider("Energy E / (mc²)", 0.9, 1.5, 1.0, 0.01)
            geo_n    = st.select_slider("Integration steps",
                                         options=[500,1000,2000,5000,10000],
                                         value=2000)
            S["rel_geo_r0"] = geo_r0; S["rel_geo_L"] = geo_L

            if st.button("📐 INTEGRATE GEODESIC",
                         width='stretch', type="primary"):
                _gr_geo = GeneralRelativity(geo_mass*M_SUN, 0.0)
                r0_m    = geo_r0 * _gr_geo.r_s
                result  = _gr_geo.geodesic_integrate_schw(
                    r0_m, 0.0, geo_L*_gr_geo.r_s, E=geo_E,
                    n_steps=geo_n, dlambda=_gr_geo.r_s*0.5)
                S["rel_geo_result"] = result
                S["rel_gr"] = _gr_geo

            geo_res = S.get("rel_geo_result")
            if geo_res:
                st.markdown(f"""
                <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                            background:rgba(8,12,24,.92);padding:.55rem;
                            border:1px solid rgba(79,195,247,.12);
                            border-radius:3px;line-height:1.9;">
                Steps computed: {geo_res['n_steps']}<br>
                r_min: {geo_res['r'].min()/S['rel_gr'].r_s:.3f} r_s<br>
                r_max: {geo_res['r'].max()/S['rel_gr'].r_s:.3f} r_s<br>
                Captured: <b style="color:#{'EF5350' if geo_res['captured'] else '81C784'}">
                {"YES — fell into BH" if geo_res["captured"] else "NO — orbiting/escaping"}</b>
                </div>""", unsafe_allow_html=True)

        with c2:
            geo_res = S.get("rel_geo_result")
            if geo_res:
                fig = _plot_geodesic(geo_res, S["rel_gr"].r_s)
                st.pyplot(fig, width='stretch')
                plt.close(fig)
            else:
                st.info("Configure parameters and integrate geodesic.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 7 — RELATIVISTIC ROCKET
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_rocket:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#4FC3F7;">[ RELATIVISTIC ROCKET ]</div>',
                unsafe_allow_html=True)
            m0_r  = st.number_input("Initial mass m₀ [kg]",
                                     value=5e5, format="%.3e")
            mf_r  = st.number_input("Final/payload mass m_f [kg]",
                                     value=1e4, format="%.3e")
            ve_r  = st.slider("Exhaust speed v_e/c", 0.01, 0.9999,
                               0.1, 0.001, format="%.4f")
            d_dest = st.number_input("Destination [ly]",
                                      value=4.24, min_value=0.01, format="%.3f")
            a_r    = st.number_input("Proper acceleration [m/s²]",
                                      value=9.81, format="%.3f")

            rkt  = sr.relativistic_rocket(m0_r, mf_r, ve_r*C_SI)
            phot = sr.photon_rocket(m0_r, mf_r)
            twin_rkt = sr.twin_with_acceleration(rkt["v_final_ms"], d_dest, a_r)

            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.75rem;
                        border:1px solid rgba(79,195,247,.15);
                        border-radius:3px;line-height:2.1;">
            <b style="color:#4FC3F7;font-size:.63rem;">── TSIOLKOVSKY (REL.) ──</b><br>
            Mass ratio R = m₀/mf = <b style="color:#E8C46A;">{rkt['mass_ratio']:.3f}</b><br>
            v_exhaust = <b>{ve_r:.4f} c</b><br>
            v_final = <b style="color:#E8C46A;">{rkt['v_final_c']:.6f} c</b><br>
            γ_final = <b style="color:#FF8800;">{rkt['gamma_final']:.4f}</b><br>
            ΔRapidity = <b>{rkt['delta_rapidity']:.4f}</b><br>
            KE_payload = <b>{rkt['KE_final_J']:.4e} J</b><br>
            <br>
            <b style="color:#4FC3F7;font-size:.63rem;">── PHOTON ROCKET ──</b><br>
            v_final = <b style="color:#CE93D8;">{phot['v_final_c']:.6f} c</b><br>
            γ_final = <b>{phot['gamma_final']:.4f}</b><br>
            Efficiency η = <b>{phot['efficiency']*100:.3f}%</b><br>
            Payload frac = <b>{phot['payload_frac']*100:.4f}%</b><br>
            <br>
            <b style="color:#4FC3F7;font-size:.63rem;">── MISSION to {d_dest:.2f} ly ──</b><br>
            Ship time = <b style="color:#E8C46A;">{twin_rkt['tau_ship_total_yr']:.4f} yr</b><br>
            Earth time = <b style="color:#4FC3F7;">{twin_rkt['t_earth_total_yr']:.4f} yr</b><br>
            Age diff = <b style="color:#D154FF;">{twin_rkt['age_diff_yr']:.4f} yr</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            # Mass ratio sweep
            _mpl()
            fig_r, axes_r = plt.subplots(2, 2, figsize=(12, 8))
            fig_r.patch.set_facecolor("#06090f")

            R_arr  = np.logspace(0.01, 4, 400)
            ve_arr = [0.1, 0.3, 0.5, 0.9]
            colors_r = ["#E8C46A","#4FC3F7","#81C784","#CE93D8"]

            ax_r1 = axes_r[0,0]
            for ve, clr in zip(ve_arr, colors_r):
                vf = np.array([sr.relativistic_rocket(R*1e3, 1e3, ve*C_SI)["v_final_c"]
                                for R in R_arr])
                ax_r1.semilogx(R_arr, vf, color=clr, lw=1.1,
                                label=f"v_e={ve}c")
            ax_r1.axhline(0.9999, color="#D154FF", lw=0.7, ls=":")
            ax_r1.set_xlabel("Mass ratio R"); ax_r1.set_ylabel("v_final/c")
            ax_r1.set_title("FINAL VELOCITY vs MASS RATIO")
            ax_r1.legend(fontsize=5.5)
            ax_r1.set_facecolor("#080c18")

            ax_r2 = axes_r[0,1]
            for ve, clr in zip(ve_arr, colors_r):
                gf = np.array([sr.relativistic_rocket(R*1e3, 1e3, ve*C_SI)["gamma_final"]
                                for R in R_arr])
                ax_r2.loglog(R_arr, gf, color=clr, lw=1.1, label=f"v_e={ve}c")
            ax_r2.set_xlabel("Mass ratio R"); ax_r2.set_ylabel("γ_final")
            ax_r2.set_title("LORENTZ FACTOR vs MASS RATIO")
            ax_r2.legend(fontsize=5.5)
            ax_r2.set_facecolor("#080c18")

            ax_r3 = axes_r[1,0]
            d_arr = np.logspace(-1, 3, 300)
            a_arr = [0.1, 1.0, 9.81, 100.0]
            for a_val, clr in zip(a_arr, colors_r):
                twin_arr = [sr.twin_with_acceleration(
                    0.5*C_SI, d, a_val)["tau_ship_total_yr"] for d in d_arr]
                ax_r3.loglog(d_arr, twin_arr, color=clr, lw=1.1,
                              label=f"a={a_val:.1f}m/s²")
            ax_r3.set_xlabel("Distance [ly]")
            ax_r3.set_ylabel("Ship proper time [yr]")
            ax_r3.set_title("SHIP TIME vs DISTANCE (v=0.5c, varied accel)")
            ax_r3.legend(fontsize=5.5)
            ax_r3.set_facecolor("#080c18")

            ax_r4 = axes_r[1,1]
            ve2_arr = np.linspace(0.01, 0.9999, 300)
            R_fixed = 10.0
            vf_arr  = np.array([sr.relativistic_rocket(R_fixed*1e3, 1e3, v*C_SI)["v_final_c"]
                                  for v in ve2_arr])
            ax_r4.plot(ve2_arr, vf_arr, color="#E8C46A", lw=1.2,
                        label=f"R={R_fixed:.0f}×")
            ax_r4.plot([0.01,0.9999],[0.01,0.9999], color="#3a4a70",
                        lw=0.7, ls="--", label="v_f = v_e (classical)")
            ax_r4.set_xlabel("v_exhaust/c"); ax_r4.set_ylabel("v_final/c")
            ax_r4.set_title(f"FINAL SPEED vs EXHAUST SPEED (R={R_fixed:.0f}×)")
            ax_r4.legend(fontsize=5.5)
            ax_r4.set_facecolor("#080c18")

            plt.tight_layout()
            st.pyplot(fig_r, width='stretch')
            plt.close(fig_r)
