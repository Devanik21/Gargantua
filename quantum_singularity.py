"""
quantum_singularity.py — Quantum Gravity, Singularity Physics & Bulk Dimensional Engine
ENDURANCE Mission Control | Interstellar Science Platform v3.0.0
═══════════════════════════════════════════════════════════════════════════════
Scientific References:
  [1]  Wheeler (1955) Phys.Rev. 97:511  [Quantum foam & spacetime topology]
  [2]  Ashtekar & Lewandowski (2004) Class.Quant.Grav. 21:R53  [LQG review]
  [3]  Domagala & Lewandowski (2004) Class.Quant.Grav. 21:5233  [Barbero-Immirzi γ]
  [4]  Bojowald (2001) PRL 86:5227  [Loop quantum cosmology — quantum bounce]
  [5]  Ashtekar, Pawlowski & Singh (2006) PRL 96:141301  [LQC exact bounce]
  [6]  Belinskii, Khalatnikov & Lifshitz (1970) Adv.Phys. 19:525  [BKL singularity]
  [7]  Misner (1969) PRL 22:1071  [Mixmaster universe oscillations]
  [8]  Hawking (1975) Commun.Math.Phys. 43:199  [Black hole radiation]
  [9]  Page (1993) PRL 71:3743  [Information in black hole radiation — Page curve]
  [10] Penington (2020) JHEP 09:002  [Entanglement wedge reconstruction]
  [11] Almheiri, Mahajan, Maldacena & Zhao (2020) JHEP 01:089  [Island rule]
  [12] Almheiri, Engelhardt, Marolf & Maxfield (2019) JHEP 12:063  [Quantum extremal surface]
  [13] Maldacena, Shenker & Stanford (2016) JHEP 08:106  [Chaos bound λ_L ≤ 2πkT/ℏ]
  [14] Kitaev (2015) KITP talks  [SYK model]
  [15] Sachdev & Ye (1993) PRL 70:3339  [SY model — precursor to SYK]
  [16] Unruh (1976) PRD 14:870  [Unruh effect]
  [17] Casimir (1948) Proc.Kon.Ned.Akad.Wet. 51:793  [Casimir effect]
  [18] Schwinger (1951) Phys.Rev. 82:664  [Pair production in electric field]
  [19] Ryu & Takayanagi (2006) PRL 96:181602  [Holographic entanglement entropy]
  [20] Maldacena & Susskind (2013) Fortschr.Phys. 61:781  [ER=EPR]
  [21] Penrose (1965) PRL 14:57  [Singularity theorem]
  [22] Thorne (2014) "The Science of Interstellar" W.W. Norton  [Film physics]

Module implements:
  ┌─ PLANCK SCALE & QUANTUM FOAM ───────────────────────────────────────────┐
  │ Complete Planck unit system (CODATA 2018)                               │
  │ Virtual BH nucleation rate Γ ∝ exp(−S_BH) per Planck 4-volume          │
  │ Wheeler foam topology: genus fluctuation spectrum                        │
  │ Spacetime granularity: area gap Δ_A = 4√3π γ ℓ_P²                     │
  │ Quantum gravity correction to Lorentz dispersion: δω/ω ~ (E/E_P)^n    │
  │ Trans-Planckian frequency cutoff at k·ℓ_P ~ 1                          │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ LOOP QUANTUM GRAVITY ──────────────────────────────────────────────────┐
  │ Area spectrum: A_n = 8πγℓ_P² Σ_i √(j_i(j_i+1)) [2]                   │
  │ Volume spectrum: V ~ (γℓ_P²)^(3/2) [2]                                 │
  │ Barbero-Immirzi γ = 0.2375 (Domagala-Lewandowski 2004) [3]             │
  │ Spin-1/2 network: minimal area gap, first 20 eigenvalues               │
  │ Weave state: continuum approximation, N nodes/area                      │
  │ LQC effective Friedmann: H² = (8πG/3)ρ(1−ρ/ρ_crit) [4,5]             │
  │ Critical density ρ_crit = 3/(8πγ²λ² κ²) ≈ 0.41 ρ_Planck              │
  │ Quantum bounce: symmetric contraction→expansion, no singularity        │
  │ Wheeler-DeWitt in minisuperspace: −∂²Ψ/∂β² + V(β)Ψ = 0               │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ SINGULARITY INTERIOR & BKL OSCILLATIONS ───────────────────────────────┐
  │ Kasner metric: ds² = −dt² + Σ t^{2p_i}(dx^i)²                         │
  │ Kasner constraints: Σp_i=1, Σp_i²=1; parameterisation via u∈[1,∞) [6]│
  │ BKL map: u→u−1 (u>2) or u→1/(u−1) (1<u<2) [6]                        │
  │ Mixmaster: chaotic oscillation between Kasner epochs [7]               │
  │ Kasner exponent spiral: phase-space topology & chaotic attractor        │
  │ Spacelike singularity approach: local Kasner + BKL bounce              │
  │ Bianchi IX: scale factors (a,b,c) — anisotropy parameter Ω_Bianchi    │
  │ Quantum resolution: curvature bound R_max ~ 1/ℓ_P²                    │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ HAWKING INFORMATION & PAGE CURVE ─────────────────────────────────────┐
  │ BH entropy: S_BH = A/(4ℓ_P²) = 4πM² (in Planck units)                │
  │ Evaporation: dM/dt = −1/(15360πM²) [Planck units] [8]                 │
  │ Evaporation time t_evap = 5120πM₀³                                     │
  │ Page time t_Page ≈ t_evap/2 (entropy turnover) [9]                    │
  │ Scrambling time t_scr = β/2π × ln(S_BH) [13]                          │
  │ Entanglement entropy S(t): Hawking→Page curve with island correction   │
  │ Island rule: S_gen = S_rad + A_island/(4G) [11]                        │
  │ Quantum extremal surface: minimise over all island choices [12]        │
  │ Page curve reconstruction: S(t) = min over no-island/island saddles    │
  │ Information retention: unitarity constraint on S_ent(t)                │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ UNRUH EFFECT & VACUUM PHYSICS ────────────────────────────────────────┐
  │ Unruh temperature T_U = ℏa/(2πck_B) [16]                              │
  │ Thermal Planck spectrum at T_U for uniformly accelerated observer      │
  │ Unruh-DeWitt detector: response function R(ω,a)                       │
  │ Casimir pressure P = −π²ℏc/(240d⁴) between parallel plates [17]      │
  │ Casimir energy as a function of plate separation d                     │
  │ Schwinger pair production rate W/V ∝ E² exp(−πE_crit/E) [18]         │
  │ Critical Schwinger field E_crit = m_e²c³/(eℏ) ≈ 1.32×10¹⁸ V/m       │
  │ Vacuum polarisation: non-linear QED corrections to Maxwell             │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ QUANTUM CHAOS & SCRAMBLING ────────────────────────────────────────────┐
  │ MSS chaos bound: λ_L ≤ 2πk_BT/ℏ; BH saturates [13]                   │
  │ OTOC F(t) = ⟨V†(t)W†V(t)W⟩: scrambling diagnostic                   │
  │ OTOC decay: F(t) ≈ 1 − (ε/N)exp(λ_L t) for t<t_scr                   │
  │ SYK model spectral density (large-q limit) [14,15]                    │
  │ Level spacing statistics: Wigner-Dyson GUE distribution                │
  │ Spectral form factor: ramp + plateau from random matrix theory         │
  │ Information scrambling complexity: circuit depth ~ S_BH                │
  │ Quantum Lyapunov exponent vs temperature: T-linear regime              │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ HOLOGRAPHY & ER=EPR ───────────────────────────────────────────────────┐
  │ Ryu-Takayanagi: S_EE = Area(γ_A)/(4G) [19]                            │
  │ 2D CFT interval entropy: S = (c/3)ln(l/ε) (vacuum)                    │
  │ Finite temperature: S = (c/3)ln[(β/π)sinh(πl/β)/ε]                   │
  │ Holographic mutual information I(A:B): phase transition                 │
  │ ER=EPR: entangled BH pair ↔ Einstein-Rosen bridge [20]                │
  │ Thermofield double state |TFD⟩ = Σ e^{−βE_n/2}|n⟩_L|n⟩_R            │
  │ Wormhole length growth: dl/dt ~ c (classical), exponential (quantum)   │
  │ Holographic complexity: C = Vol(extremal surface)/(GℓAdS)              │
  │ Subregion duality: bulk wedge from boundary RT surface                 │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ COOPER'S SINGULARITY CROSSING ─────────────────────────────────────────┐
  │ Proper time from horizon to Gargantua singularity (Kerr interior)      │
  │ Cauchy horizon instability: mass inflation, blue-shift divergence       │
  │ Quantum decoherence timescale: τ_dec ~ ℏ/k_BT_H                       │
  │ TARS data crystal capacity: Bekenstein bound S = 2πER/(ℏc)             │
  │ Bulk transmission fidelity: signal attenuation e^{−ky} vs bulk         │
  │ Cooper quantum state evolution inside the Tesseract                     │
  │ Information encoding: gravity perturbation on singularity worldsheet   │
  │ Murphy's signal bandwidth: Shannon capacity of gravity channel          │
  └──────────────────────────────────────────────────────────────────────────┘

"The singularity is not the end. It is where the old rules shatter — and
 something stranger, truer, takes their place."
                              — Cooper, Gargantua interior, 2067
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import math
import warnings
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Sequence

import numpy as np
trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
import pandas as pd
import scipy.integrate  as sci_int
import scipy.optimize   as sci_opt
import scipy.special    as sci_sp
import scipy.stats      as sci_stats
import scipy.linalg     as sci_la

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot      as plt
import matplotlib.gridspec    as gridspec
import matplotlib.colors      as mcolors
import matplotlib.ticker      as mticker
import matplotlib.patches     as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.colors        import LinearSegmentedColormap
from matplotlib.collections   import LineCollection

import streamlit as st

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# §1  PHYSICAL CONSTANTS  (SI, CODATA 2018)
# ══════════════════════════════════════════════════════════════════════════════
G_SI       = 6.674_30e-11           # Gravitational constant          m³ kg⁻¹ s⁻²
C_SI       = 2.997_924_58e8         # Speed of light                  m s⁻¹
HBAR_SI    = 1.054_571_817e-34      # Reduced Planck constant         J·s
H_SI       = 6.626_070_15e-34       # Planck constant                 J·s
KB_SI      = 1.380_649e-23          # Boltzmann constant              J K⁻¹
E_CHARGE   = 1.602_176_634e-19      # Elementary charge               C
M_E_SI     = 9.109_383_7015e-31     # Electron mass                   kg
M_SUN      = 1.989e30              # Solar mass                      kg
ALPHA_EM   = 7.297_352_5693e-3     # Fine structure constant         (dimensionless)
SIGMA_SB   = 5.670_374_419e-8      # Stefan-Boltzmann                W m⁻² K⁻⁴

# ── Planck units (derived) ────────────────────────────────────────────────────
LP    = math.sqrt(HBAR_SI * G_SI / C_SI**3)            # 1.6162e-35 m
TP    = LP / C_SI                                        # 5.3912e-44 s
MP    = math.sqrt(HBAR_SI * C_SI / G_SI)               # 2.1764e-8  kg
EP    = MP * C_SI**2                                     # 1.9561e9   J
TP_K  = EP / KB_SI                                      # Planck temperature K
RHO_P = MP / LP**3                                       # 5.1550e96  kg m⁻³

# ── LQG constants ────────────────────────────────────────────────────────────
GAMMA_BI  = 0.2375          # Barbero-Immirzi parameter (Domagala-Lewandowski 2004)
# Minimum area gap from LQG: Δ_A = 4√3 π γ ℓ_P²
A_MIN_LQG = 4.0 * math.sqrt(3.0) * math.pi * GAMMA_BI * LP**2   # m²
# Critical density in LQC
# ρ_crit = 3 / (8π γ² λ² κ²) where λ² = 4√3 π γ ℓ_P² (area gap)
# Simplified: ρ_crit ≈ 0.41 ρ_P (Ashtekar-Pawlowski-Singh 2006)
RHO_CRIT_LQC = 0.4088 * RHO_P

# ── Gargantua parameters (canon, Thorne 2014) ────────────────────────────────
GARG_MASS_MSUN = 1.0e8               # Gargantua mass in solar masses
GARG_MASS_KG   = GARG_MASS_MSUN * M_SUN
GARG_SPIN      = 0.9999              # Near-extremal Kerr spin parameter a/M
GARG_RS_M      = 2.0 * G_SI * GARG_MASS_KG / C_SI**2   # Schwarzschild radius
# Hawking temperature of Gargantua
GARG_TH_K      = HBAR_SI * C_SI**3 / (8.0 * math.pi * G_SI * GARG_MASS_KG * KB_SI)
# BH entropy (Bekenstein-Hawking)
GARG_SBH       = math.pi * (GARG_RS_M / 2.0)**2 / LP**2   # dimensionless

# ── Schwinger critical field ──────────────────────────────────────────────────
E_SCHWINGER = M_E_SI**2 * C_SI**3 / (E_CHARGE * HBAR_SI)   # ~1.32e18 V/m


# ══════════════════════════════════════════════════════════════════════════════
# §2  COLOUR PALETTE (matches ENDURANCE master CSS)
# ══════════════════════════════════════════════════════════════════════════════
_GOLD    = "#E8C46A"
_BLUE    = "#4FC3F7"
_PURPLE  = "#8060ff"
_GREEN   = "#81C784"
_ORANGE  = "#FF8800"
_PINK    = "#D154FF"
_RED     = "#ff4060"
_CYAN    = "#00e5ff"
_BG0     = "#020408"
_BG1     = "#04060c"
_BG2     = "#060a14"
_BG3     = "#0a1020"
_TEXT    = "#c8d0e0"
_DIM     = "#304070"

_CMAP_QUANTUM = LinearSegmentedColormap.from_list(
    "quantum",
    [_BG0, "#1a0540", _PURPLE, "#c040ff", _PINK, _GOLD],
    N=512
)
_CMAP_HEAT = LinearSegmentedColormap.from_list(
    "heat",
    [_BG0, "#1a0520", "#8060ff", "#ff4060", _GOLD],
    N=512
)
_CMAP_CHAOS = LinearSegmentedColormap.from_list(
    "chaos",
    [_BG0, "#001a20", _BLUE, _CYAN, "#ffffff"],
    N=512
)


# ══════════════════════════════════════════════════════════════════════════════
# §3  DATACLASSES
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class PlanckState:
    """Complete Planck unit system and quantum foam state."""
    l_P: float = LP
    t_P: float = TP
    m_P: float = MP
    E_P: float = EP
    T_P: float = TP_K
    rho_P: float = RHO_P
    A_min: float = A_MIN_LQG
    rho_crit_lqc: float = RHO_CRIT_LQC


@dataclass
class KasnerEpoch:
    """Single Kasner epoch parametrised by u ∈ [1,∞)."""
    u: float
    p1: float = field(init=False)
    p2: float = field(init=False)
    p3: float = field(init=False)

    def __post_init__(self):
        u = self.u
        denom = 1.0 + u + u**2
        # BKL parameterisation (sorted p1 ≤ p2 ≤ p3)
        self.p1 = -u / denom
        self.p2 = (1.0 + u) / denom
        self.p3 = u * (1.0 + u) / denom

    @property
    def check_sum(self) -> float:
        """Must equal 1."""
        return self.p1 + self.p2 + self.p3

    @property
    def check_sum_sq(self) -> float:
        """Must equal 1."""
        return self.p1**2 + self.p2**2 + self.p3**2


@dataclass
class PageCurveState:
    """State for Hawking information / Page curve computation."""
    M0_planck: float    # Initial BH mass in Planck units (m_P)
    t_evap: float = field(init=False)
    t_page: float = field(init=False)
    t_scr: float  = field(init=False)
    S_BH0: float  = field(init=False)

    def __post_init__(self):
        # All in Planck units (G=c=ℏ=k=1)
        self.t_evap  = 5120.0 * math.pi * self.M0_planck**3
        self.t_page  = self.t_evap / 2.0
        self.S_BH0   = 4.0 * math.pi * self.M0_planck**2
        # Scrambling time: t_scr = (M/m_P) × (4/π) × ln(S_BH0)
        # In Planck units: t_scr = 4 × M × ln(4πM²) / (2π)
        self.t_scr   = (4.0 * self.M0_planck / (2.0 * math.pi)) * math.log(self.S_BH0 + 1.0)


@dataclass
class SYKParams:
    """Sachdev-Ye-Kitaev model parameters."""
    N: int   = 32      # Number of Majorana fermions (must be divisible by 4)
    q: int   = 4       # Interaction order (q-body SYK)
    J: float = 1.0     # Coupling variance  J² = J_rms²
    beta: float = 10.0 # Inverse temperature β = 1/T


# ══════════════════════════════════════════════════════════════════════════════
# §4  PLANCK SCALE & QUANTUM FOAM ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class PlanckFoamEngine:
    """
    Computes quantum gravity foam observables:
    virtual BH nucleation rates, spacetime granularity, Planck-scale dispersion.
    """

    @staticmethod
    def virtual_bh_nucleation_rate(M_bh_planck: float) -> float:
        """
        Virtual BH nucleation rate per Planck 4-volume.
        Γ ≈ A_prefactor × exp(−S_BH) = A × exp(−4π M²)  [Planck units]

        For a Planck-mass BH (M=1): Γ ≈ exp(−4π) ≈ 3.49×10⁻⁶
        """
        S_bh = 4.0 * math.pi * M_bh_planck**2
        # Include one-loop prefactor ∝ M^{-2} (graviton propagator)
        prefactor = max(M_bh_planck**(-2), 1e-300)
        rate = prefactor * math.exp(-min(S_bh, 700.0))
        return rate

    @staticmethod
    def foam_topology_number(l_scale_planck: float) -> float:
        """
        Expected number of topology changes (wormholes/handles) per unit 3-volume
        at scale l (in Planck units).
        n_top(l) ≈ exp(−S_min) / l⁴   where S_min ~ (l/l_P)²
        For l >> l_P: topology is classical (smooth).
        For l ~ l_P: topology fluctuations O(1) per Planck volume.
        """
        S_min = max(l_scale_planck**2, 1e-300)
        if S_min > 700:
            return 0.0
        return math.exp(-S_min) / max(l_scale_planck**4, 1e-300)

    @staticmethod
    def granularity_spectrum(n_max: int = 20) -> Tuple[np.ndarray, np.ndarray]:
        """
        LQG area spectrum: first n_max eigenvalues.
        A_n = 8πγℓ_P² Σ_i √(j_i(j_i+1))
        For single spin-j link: A(j) = 8πγℓ_P² √(j(j+1))
        j ∈ {1/2, 1, 3/2, 2, ...}

        Returns (j_array, area_eigenvalues_in_LP2)
        """
        j_vals = np.array([n * 0.5 for n in range(1, n_max + 1)])
        A_vals = 8.0 * math.pi * GAMMA_BI * np.sqrt(j_vals * (j_vals + 1.0))  # in ℓ_P²
        return j_vals, A_vals

    @staticmethod
    def dispersion_correction(E_J: float, n_LIV: int = 1) -> float:
        """
        Lorentz-invariance violation (LIV) dispersion correction.
        δω/ω ~ (E/E_P)^n  for n=1 (linear) or n=2 (quadratic).
        E in Joules.
        Returns fractional correction δω/ω.
        """
        ratio = E_J / EP
        return ratio**n_LIV

    @staticmethod
    def foam_power_spectrum(k_max_m: float = 1.0 / LP, N_pts: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """
        Metric fluctuation power spectrum P_h(k) at Planck scale.
        P_h(k) ~ (ℓ_P/L)² × exp(−(kℓ_P)²)  [Gaussian foam model]
        Returns (k, P_h) in SI.
        """
        k = np.logspace(np.log10(k_max_m * 1e-6), np.log10(k_max_m), N_pts)
        x = k * LP
        P_h = LP**2 * np.exp(-x**2)
        return k, P_h


# ══════════════════════════════════════════════════════════════════════════════
# §5  LOOP QUANTUM GRAVITY ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class LQGEngine:
    """
    Loop Quantum Gravity and Loop Quantum Cosmology computations.
    """

    @staticmethod
    def spin_network_area_eigenvalues(j_max_half_int: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """
        Area spectrum for a single spin-j edge in LQG.
        A(j) = 8πγℓ_P² √(j(j+1))  for j = 1/2, 1, 3/2, ..., j_max
        Returns (j_array, A_m2)  with A in m².
        """
        j = np.array([k * 0.5 for k in range(1, j_max_half_int * 2 + 1)])
        A = 8.0 * math.pi * GAMMA_BI * LP**2 * np.sqrt(j * (j + 1.0))
        return j, A

    @staticmethod
    def volume_eigenvalue_approx(j_node: float) -> float:
        """
        Approximate volume eigenvalue for a trivalent node with all spins = j.
        V ~ (γℓ_P²)^{3/2} × √(j(j+1/2)(j+1)) (Thiemann formula, approx)
        Returns V in m³.
        """
        V = (GAMMA_BI * LP**2)**1.5 * math.sqrt(j_node * (j_node + 0.5) * (j_node + 1.0))
        return V

    @staticmethod
    def lqc_effective_hubble(rho_SI: float) -> float:
        """
        LQC effective Friedmann equation:
        H² = (8πG/3) × ρ × (1 − ρ/ρ_crit)
        ρ_crit = 0.4088 ρ_P ≈ 2.11×10^96 kg/m³

        Returns H in s⁻¹.  Returns 0 at the quantum bounce (ρ=ρ_crit).
        """
        if rho_SI >= RHO_CRIT_LQC:
            return 0.0
        H2 = (8.0 * math.pi * G_SI / 3.0) * rho_SI * (1.0 - rho_SI / RHO_CRIT_LQC)
        return math.sqrt(max(H2, 0.0))

    @staticmethod
    def lqc_bounce_trajectory(N_pts: int = 800) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        LQC minisuperspace bounce: integrate scale factor a(t) through quantum bounce.
        Uses effective LQC Friedmann + continuity equation.

        Radiation-dominated universe: ρ = ρ_r0 / a⁴
        H² = (8πG/3) ρ (1 − ρ/ρ_crit)

        Returns (t, a, H, rho) normalised so a(bounce)=1, ρ(bounce)=ρ_crit.
        All in Planck units.
        """
        # Normalise: a_bounce = 1, ρ_bounce = ρ_crit
        # ρ_r0 = ρ_crit × a_bounce⁴ = ρ_crit (with a_bounce=1)
        rho_r0 = 1.0   # ρ_crit units
        # Time range (Planck units, symmetric about bounce at t=0)
        t_span = 12.0
        t = np.linspace(-t_span, t_span, N_pts)
        a = np.zeros(N_pts)
        H = np.zeros(N_pts)
        rho = np.zeros(N_pts)

        # Integrate: da/dt = aH(a)
        # At bounce (t=0): a=1, ρ=1 (in our normalisation)
        # For radiation: ρ = rho_r0/a⁴
        # H = sqrt((8πG/3) ρ (1−ρ/ρ_crit))
        # Use 4th-order RK from t=0 outward

        dt = t[1] - t[0]
        idx0 = N_pts // 2

        # At bounce
        a[idx0] = 1.0
        rho[idx0] = rho_r0
        H[idx0] = 0.0

        # Forward integration
        for i in range(idx0, N_pts - 1):
            a_i = a[i]
            rho_i = rho_r0 / a_i**4
            H_i = math.sqrt(max((8.0 * math.pi / 3.0) * rho_i * (1.0 - rho_i / 1.0), 0.0))
            k1 = a_i * H_i
            a_m = a_i + 0.5 * dt * k1
            rho_m = rho_r0 / max(a_m**4, 1e-30)
            H_m = math.sqrt(max((8.0 * math.pi / 3.0) * rho_m * (1.0 - rho_m), 0.0))
            k2 = a_m * H_m
            a_m2 = a_i + 0.5 * dt * k2
            rho_m2 = rho_r0 / max(a_m2**4, 1e-30)
            H_m2 = math.sqrt(max((8.0 * math.pi / 3.0) * rho_m2 * (1.0 - rho_m2), 0.0))
            k3 = a_m2 * H_m2
            a_f = a_i + dt * k3
            rho_f = rho_r0 / max(a_f**4, 1e-30)
            H_f = math.sqrt(max((8.0 * math.pi / 3.0) * rho_f * (1.0 - rho_f), 0.0))
            k4 = a_f * H_f
            a[i + 1] = a_i + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            rho[i + 1] = rho_r0 / max(a[i + 1]**4, 1e-30)
            H[i + 1] = math.sqrt(max((8.0 * math.pi / 3.0) * rho[i+1] * (1.0 - rho[i+1]), 0.0))

        # Backward integration (t < 0): da/dt = -a|H|
        for i in range(idx0, 0, -1):
            a_i = a[i]
            rho_i = rho_r0 / max(a_i**4, 1e-30)
            H_i = math.sqrt(max((8.0 * math.pi / 3.0) * rho_i * (1.0 - rho_i), 0.0))
            k1 = -a_i * H_i
            a_m = a_i + 0.5 * (-dt) * k1
            rho_m = rho_r0 / max(a_m**4, 1e-30)
            H_m = math.sqrt(max((8.0 * math.pi / 3.0) * rho_m * (1.0 - rho_m), 0.0))
            k2 = -a_m * H_m
            a_m2 = a_i + 0.5 * (-dt) * k2
            rho_m2 = rho_r0 / max(a_m2**4, 1e-30)
            H_m2 = math.sqrt(max((8.0 * math.pi / 3.0) * rho_m2 * (1.0 - rho_m2), 0.0))
            k3 = -a_m2 * H_m2
            a_f = a_i + (-dt) * k3
            rho_f = rho_r0 / max(a_f**4, 1e-30)
            H_f = math.sqrt(max((8.0 * math.pi / 3.0) * rho_f * (1.0 - rho_f), 0.0))
            k4 = -a_f * H_f
            a[i - 1] = a_i + ((-dt) / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            rho[i - 1] = rho_r0 / max(a[i-1]**4, 1e-30)
            H[i - 1] = -math.sqrt(max((8.0 * math.pi / 3.0) * rho[i-1] * (1.0 - rho[i-1]), 0.0))

        return t, a, H, rho

    @staticmethod
    def wdw_wavefunction(alpha_arr: np.ndarray, k_factor: float = 1.0) -> np.ndarray:
        """
        Wheeler-DeWitt wavefunction in minisuperspace.
        Simplified 1+1D: −d²Ψ/dα² + V(α)Ψ = 0
        where α = ln(a),  V(α) = −k² e^{4α}  (radiation-dominated, k=0 spatial)

        Solve via WKB:  Ψ(α) = A exp(±i∫√(−V)dα) when V < 0.
        Returns |Ψ(α)|² normalised.
        """
        # Use Hartle-Hawking no-boundary wavefunction: Ψ ~ Ai(f(α))
        # V(α) = -k²_eff exp(4α) + Λ exp(6α)
        # For radiation+Λ: V = (1/(6π²G)) exp(6α)(Λ − 8πG/a²)
        # Simplify: use Airy function in α-space
        # Ψ(α) ∝ Ai(-α_turn − α) where α_turn is the turning point
        k_eff = k_factor
        # WKB: Ψ(α) ∝ |p(α)|^{-1/2} cos(∫p dα − π/4)
        # p(α) = sqrt(max(k_eff² e^{4α}, 0))
        psi = np.zeros_like(alpha_arr)
        for i, alpha in enumerate(alpha_arr):
            p2 = k_eff**2 * math.exp(4.0 * alpha) if alpha > 0 else -k_eff**2 * math.exp(4.0 * alpha)
            if p2 > 0:
                p = math.sqrt(p2)
                # WKB oscillatory region
                phase = k_eff * math.exp(2.0 * alpha) / 2.0
                psi[i] = math.cos(phase) / math.sqrt(p + 1e-30)
            else:
                # Tunnelling (exponential) region
                kappa = math.sqrt(max(-p2, 1e-30))
                psi[i] = math.exp(-kappa * abs(alpha)) / math.sqrt(kappa + 1e-30)

        # Normalise
        norm = np.sqrt(trapz(psi**2, alpha_arr) + 1e-30)
        return psi / norm


# ══════════════════════════════════════════════════════════════════════════════
# §6  BKL SINGULARITY & KASNER ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class BKLEngine:
    """
    Belinskii-Khalatnikov-Lifshitz singularity oscillations.
    Implements the BKL map, Kasner epoch sequence, and mixmaster chaos.
    """

    @staticmethod
    def kasner_from_u(u: float) -> Tuple[float, float, float]:
        """
        Kasner exponents from BKL parameter u ∈ [1, ∞).
        p₁ = −u/(1+u+u²),  p₂ = (1+u)/(1+u+u²),  p₃ = u(1+u)/(1+u+u²)
        Constraints: Σp_i = 1, Σp_i² = 1.
        Sorted so p₁ ≤ p₂ ≤ p₃.
        """
        u = max(u, 1.0 + 1e-12)
        denom = 1.0 + u + u**2
        p1 = -u / denom
        p2 = (1.0 + u) / denom
        p3 = u * (1.0 + u) / denom
        return p1, p2, p3

    @staticmethod
    def bkl_map(u: float) -> float:
        """
        BKL map: one Kasner epoch to the next.
        If u > 2:     u → u − 1
        If 1 < u ≤ 2: u → 1/(u − 1)  (triggers large anisotropy bounce)
        """
        u = max(u, 1.0 + 1e-12)
        if u > 2.0:
            return u - 1.0
        else:
            return 1.0 / (u - 1.0)

    @staticmethod
    def mixmaster_sequence(u0: float, N_epochs: int = 60) -> List[Dict]:
        """
        Generate N_epochs Kasner epochs starting from u₀.
        Returns list of dicts with u, p1, p2, p3, era_index.
        """
        epochs = []
        u = u0
        era = 0
        epoch_in_era = 0
        for _ in range(N_epochs):
            p1, p2, p3 = BKLEngine.kasner_from_u(u)
            epochs.append({
                "u": u,
                "p1": p1,
                "p2": p2,
                "p3": p3,
                "era": era,
                "epoch_in_era": epoch_in_era,
            })
            u_next = BKLEngine.bkl_map(u)
            if u_next > 1.0e6:   # Near u=1 singularity → new era
                era += 1
                epoch_in_era = 0
                u = 1.0 + 1.0 / u_next if u_next > 1e6 else u_next
            else:
                u = u_next
                epoch_in_era += 1
                if 1.0 < u <= 2.0:
                    era += 1
                    epoch_in_era = 0
        return epochs

    @staticmethod
    def bianchi_ix_scale_factors(
        N_pts: int = 600, tau_max: float = 5.0
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Simplified Bianchi IX (mixmaster) scale factors a(τ), b(τ), c(τ)
        near the singularity (τ → ∞ in logarithmic time Ω = −ln V).
        Uses the Kasner epoch approximation:
        In each epoch, a~τ^p1, b~τ^p2, c~τ^p3 with BKL transitions.

        Returns (tau, a, b, c) where τ is proper time to singularity.
        """
        tau = np.linspace(0.01, tau_max, N_pts)
        a = np.ones(N_pts)
        b = np.ones(N_pts)
        c = np.ones(N_pts)

        u_current = 3.7    # starting u
        epoch_epochs = BKLEngine.mixmaster_sequence(u_current, N_epochs=40)

        # Divide time into segments (each epoch gets equal log-time)
        n_ep = len(epoch_epochs)
        tau_log = np.log(tau / tau[0] + 1.0)
        t_log_max = tau_log[-1]
        seg_len = t_log_max / n_ep

        for i in range(N_pts):
            ep_idx = min(int(tau_log[i] / seg_len), n_ep - 1)
            ep = epoch_epochs[ep_idx]
            p1, p2, p3 = ep["p1"], ep["p2"], ep["p3"]
            # Within epoch: scale as (τ_local)^p
            tau_local = (tau_log[i] % seg_len) / seg_len + 1e-10
            a[i] = tau_local**p3   # largest exponent
            b[i] = tau_local**p2
            c[i] = max(tau_local**p1, 1e-30)  # can go to zero (p1<0)

        return tau, a, b, c


# ══════════════════════════════════════════════════════════════════════════════
# §7  HAWKING INFORMATION & PAGE CURVE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class PageCurveEngine:
    """
    Black hole information paradox: evaporation, entanglement entropy,
    Page curve with and without island corrections.
    All quantities in Planck units (G = c = ℏ = k_B = 1).
    """

    def __init__(self, M0_planck: float = 1000.0):
        self.state = PageCurveState(M0_planck=M0_planck)

    def mass_at_time(self, t: np.ndarray) -> np.ndarray:
        """
        M(t) = M₀ (1 − t/t_evap)^{1/3}  [exact for massless Schwarzschild]
        """
        t_clip = np.clip(t, 0.0, self.state.t_evap)
        return self.state.M0_planck * (1.0 - t_clip / self.state.t_evap) ** (1.0 / 3.0)

    def bh_entropy(self, t: np.ndarray) -> np.ndarray:
        """S_BH(t) = 4π M(t)²  [Bekenstein-Hawking]"""
        M = self.mass_at_time(t)
        return 4.0 * math.pi * M**2

    def hawking_radiation_entropy(self, t: np.ndarray) -> np.ndarray:
        """
        Entropy of emitted Hawking radiation in the semi-classical picture
        (no information recovery):  S_rad_semicl(t) = S_BH(0) − S_BH(t)
        (cumulative entropy emitted, growing monotonically).
        """
        return self.state.S_BH0 - self.bh_entropy(t)

    def page_curve_entropy(self, t: np.ndarray) -> np.ndarray:
        """
        Page curve (unitary): S_ent(t) = min(S_rad_emitted(t), S_BH(t))
        At t < t_Page: S_ent grows like Hawking radiation entropy.
        At t > t_Page: S_ent decreases back to zero as BH fully evaporates.
        """
        S_rad = self.hawking_radiation_entropy(t)
        S_bh  = self.bh_entropy(t)
        return np.minimum(S_rad, S_bh)

    def island_entropy(self, t: np.ndarray, alpha_island: float = 0.03) -> np.ndarray:
        """
        Island rule correction to entanglement entropy.
        S_gen = S_Hawking + A_island/(4G)
        The island saddle dominates after t_Page, reducing S_ent.

        Simple two-saddle model:
          No island:   S_no_isl(t) = S_rad_semicl(t)  [grows monotonically]
          Island:      S_isl(t)    = 2 S_BH(t) + α × const  [decreasing]
          S_QES(t) = min(S_no_isl, S_isl)  ← quantum extremal surface
        """
        S_no_island = self.hawking_radiation_entropy(t)
        # Island contribution: twice the entropy of the interior island + area
        S_island = 2.0 * self.bh_entropy(t) + alpha_island * self.state.S_BH0
        S_island = np.maximum(S_island, 0.0)
        return np.minimum(S_no_island, S_island)

    def scrambling_diagnostic(self, N_pts: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """
        OTOC-inspired decay through scrambling time t_scr.
        F(t) ≈ 1 − (1/S_BH0) exp(λ_L × t)
        where λ_L = 2π T_H = 1/(4M) [Planck units, Schwarzschild].
        Returns (t, F(t)) up to t = 3 t_scr.
        """
        M0 = self.state.M0_planck
        lambda_L = 1.0 / (4.0 * M0)  # BH saturates chaos bound
        t_scr = self.state.t_scr
        t = np.linspace(0.0, 3.0 * t_scr, N_pts)
        epsilon = 1.0 / self.state.S_BH0
        F = 1.0 - epsilon * np.exp(lambda_L * t)
        F = np.clip(F, -0.1, 1.0)
        return t, F


# ══════════════════════════════════════════════════════════════════════════════
# §8  UNRUH EFFECT & VACUUM PHYSICS ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class UnruhVacuumEngine:
    """
    Unruh effect, Casimir energy, Schwinger pair production,
    and vacuum fluctuation physics.
    """

    @staticmethod
    def unruh_temperature(a_ms2: float) -> float:
        """T_U = ℏa/(2πck_B)  [SI]. a in m/s²."""
        return HBAR_SI * a_ms2 / (2.0 * math.pi * C_SI * KB_SI)

    @staticmethod
    def unruh_spectrum(omega_array: np.ndarray, a_ms2: float) -> np.ndarray:
        """
        Planck spectrum at Unruh temperature T_U.
        n̄(ω) = 1/(exp(2πc ω/a) − 1)   [mean photon number per mode]
        ω in rad/s, a in m/s².
        """
        x = 2.0 * math.pi * C_SI * omega_array / a_ms2
        # Avoid overflow
        x = np.clip(x, 1e-6, 700.0)
        return 1.0 / (np.exp(x) - 1.0 + 1e-30)

    @staticmethod
    def casimir_pressure(d_m: float) -> float:
        """
        Casimir pressure between two perfectly conducting parallel plates.
        P = −π²ℏc/(240 d⁴)  [SI, N/m²]
        d in metres.
        """
        return -math.pi**2 * HBAR_SI * C_SI / (240.0 * d_m**4)

    @staticmethod
    def casimir_energy(d_m: float, area_m2: float) -> float:
        """E_Cas = −π²ℏc A/(720 d³)"""
        return -math.pi**2 * HBAR_SI * C_SI * area_m2 / (720.0 * d_m**3)

    @staticmethod
    def schwinger_pair_rate(E_field_Vm: float) -> float:
        """
        Schwinger e+e− pair production rate per unit 4-volume.
        W/V = (αE²/(4π²)) × exp(−π E_crit/E)   [SI, pairs m⁻³ s⁻¹]
        E_crit = m_e²c³/(eℏ) ≈ 1.32×10¹⁸ V/m
        For E << E_crit this is exponentially suppressed.
        """
        if E_field_Vm <= 0.0:
            return 0.0
        exponent = -math.pi * E_SCHWINGER / max(E_field_Vm, 1e-300)
        if exponent < -700:
            return 0.0
        prefactor = ALPHA_EM * E_field_Vm**2 / (4.0 * math.pi**2)
        return prefactor * math.exp(exponent)

    @staticmethod
    def vacuum_energy_density_qed() -> float:
        """
        QED zero-point energy density (UV-regulated at Planck scale).
        ρ_vac = (1/2) ∫₀^{k_P} ħω d³k/(2π)³ = ħc k_P⁴/(16π²)
        Returns ρ_vac in J/m³.
        """
        k_P = 1.0 / LP  # Planck wave vector
        return HBAR_SI * C_SI * k_P**4 / (16.0 * math.pi**2)

    @staticmethod
    def unruh_power_radiated(a_ms2: float, detector_cross_section_m2: float = 1e-20) -> float:
        """
        Power absorbed by an Unruh-DeWitt detector at acceleration a.
        P ∝ σ_det × T_U⁴ × σ_SB  [blackbody limit]
        """
        T_U = UnruhVacuumEngine.unruh_temperature(a_ms2)
        return detector_cross_section_m2 * SIGMA_SB * T_U**4


# ══════════════════════════════════════════════════════════════════════════════
# §9  QUANTUM CHAOS ENGINE  (OTOC, SYK, Lyapunov)
# ══════════════════════════════════════════════════════════════════════════════
class QuantumChaosEngine:
    """
    Quantum chaos diagnostics:
    - Maldacena-Shenker-Stanford chaos bound
    - Out-of-time-order correlators (OTOC)
    - SYK model spectral density
    - Level spacing statistics (Wigner-Dyson)
    - Spectral form factor
    """

    @staticmethod
    def chaos_bound_temperature(T_K: float) -> float:
        """
        MSS chaos bound: λ_L ≤ 2πk_BT/ℏ  [s⁻¹]
        Black holes saturate this bound.
        """
        return 2.0 * math.pi * KB_SI * T_K / HBAR_SI

    @staticmethod
    def bh_lyapunov(M_kg: float) -> float:
        """
        BH Lyapunov exponent = surface gravity κ = c³/(4GM) [s⁻¹]
        Equals 2πT_H/ℏ × ℏ = c³/(4GM).  Returns λ_L in s⁻¹.
        """
        return C_SI**3 / (4.0 * G_SI * M_kg)

    @staticmethod
    def otoc(t_arr: np.ndarray, T_K: float, M_BH_kg: float, N_dof: int = 100) -> np.ndarray:
        """
        OTOC diagnostic for a BH with N_dof degrees of freedom at temperature T_K.
        F(t)/F(0) ≈ 1 − (1/N) exp(λ_L t)   for t < t_scr
        Saturates at ~ 0 after t_scr.

        t_arr in seconds.
        """
        lambda_L = QuantumChaosEngine.bh_lyapunov(M_BH_kg)
        T_H_K = HBAR_SI * C_SI**3 / (8.0 * math.pi * G_SI * M_BH_kg * KB_SI)
        S_bh = 4.0 * math.pi * (G_SI * M_BH_kg / (HBAR_SI * C_SI))**2 * C_SI**4 / G_SI**2 / C_SI**2
        # In natural units: S = 4πM²  (Planck)
        S_bh_planck = (M_BH_kg / MP)**2 * 4.0 * math.pi
        t_scr_s = math.log(max(S_bh_planck, 2.0)) / lambda_L

        epsilon = 1.0 / max(N_dof, 2)
        F = 1.0 - epsilon * np.exp(lambda_L * t_arr)
        # Plateau after scrambling
        mask = t_arr > t_scr_s
        F[mask] = 0.0 + 0.05 * np.random.randn(mask.sum()) * 0.01  # thermal noise floor
        return np.clip(F, -0.05, 1.0)

    @staticmethod
    def syk_spectral_density(omega_arr: np.ndarray, J_rms: float = 1.0,
                              N_maj: int = 32, q: int = 4) -> np.ndarray:
        """
        SYK model spectral density ρ(E) in the large-N, large-q limit.
        Semi-circle law with Schwarzian corrections at low E.

        ρ(E) = (1/2π) √(4J̃² − E²) / J̃²   for |E| < 2J̃
        J̃² = J² × binom(N,q) × (q-1)!/q = J² (N^q/q!) / (4^...)
        Simplified: J̃_eff = J × √(N choose q) / 2^(q/2)

        At very low E: corrections from Schwarzian → exponential suppression.
        """
        import math as _math
        # Effective coupling
        log_binom = (sum(_math.log(i) for i in range(N_maj - q + 1, N_maj + 1))
                     - sum(_math.log(i) for i in range(1, q + 1)))
        J_tilde = J_rms * _math.exp(0.5 * log_binom) / (2.0 ** (q / 2.0))
        J_tilde = min(J_tilde, 1e10)  # numerical cap

        rho = np.zeros_like(omega_arr, dtype=float)
        mask = np.abs(omega_arr) < 2.0 * J_tilde
        if mask.any():
            rho[mask] = np.sqrt(4.0 * J_tilde**2 - omega_arr[mask]**2) / (2.0 * math.pi * J_tilde**2)

        # Schwarzian low-E correction: enhancement ~ exp(2π√(2NE/J)) for E>0
        low_E_mask = (omega_arr > 0) & (omega_arr < 0.2 * J_tilde)
        if low_E_mask.any() and N_maj > 0:
            correction = np.exp(2.0 * math.pi * np.sqrt(
                np.maximum(2.0 * N_maj * omega_arr[low_E_mask] / max(J_tilde, 1e-30), 0.0)
            ) * 0.1)   # damped
            rho[low_E_mask] *= correction

        return rho

    @staticmethod
    def level_spacing_gue(N_levels: int = 200, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate level spacing statistics for a GUE random matrix (Wigner-Dyson).
        Returns (s_bins, p_s) histogram of spacings.
        GUE: P(s) = (32/π²) s² exp(−4s²/π)
        """
        rng = np.random.default_rng(seed)
        H = rng.standard_normal((N_levels, N_levels)) + 1j * rng.standard_normal((N_levels, N_levels))
        H = (H + H.conj().T) / (2.0 * math.sqrt(2.0 * N_levels))
        eigvals = np.sort(np.linalg.eigvalsh(H).real)
        spacings = np.diff(eigvals)
        # Unfold: normalise by mean spacing
        mean_s = np.mean(spacings)
        s = spacings / max(mean_s, 1e-30)
        s_bins = np.linspace(0.0, 4.0, 60)
        counts, _ = np.histogram(s, bins=s_bins, density=True)
        s_mid = 0.5 * (s_bins[:-1] + s_bins[1:])
        return s_mid, counts

    @staticmethod
    def spectral_form_factor(beta: float, t_max: float, N_pts: int = 400,
                              N_levels: int = 200, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
        """
        Spectral form factor SFF(t) = |Z(β+it)/Z(β)|²
        For a GUE random matrix, shows dip → ramp → plateau.
        Returns (t_arr, SFF).
        """
        rng = np.random.default_rng(seed)
        H = rng.standard_normal((N_levels, N_levels)) + 1j * rng.standard_normal((N_levels, N_levels))
        H = (H + H.conj().T) / (2.0 * math.sqrt(2.0 * N_levels))
        eigvals = np.sort(np.linalg.eigvalsh(H).real)

        t_arr = np.linspace(0.0, t_max, N_pts)
        Z_beta = np.sum(np.exp(-beta * eigvals))
        SFF = np.zeros(N_pts)
        for i, t in enumerate(t_arr):
            Z_it = np.sum(np.exp((-beta + 1j * t) * eigvals))
            SFF[i] = (np.abs(Z_it)**2) / max(Z_beta**2, 1e-30)

        return t_arr, SFF


# ══════════════════════════════════════════════════════════════════════════════
# §10  HOLOGRAPHY ENGINE  (RT, ER=EPR, AdS/CFT)
# ══════════════════════════════════════════════════════════════════════════════
class HolographyEngine:
    """
    Holographic entanglement entropy, ER=EPR correspondence,
    and AdS/CFT observables.
    """

    @staticmethod
    def rt_entropy_vacuum(l: float, c_central: float = 12.0, epsilon: float = 1e-3) -> float:
        """
        Ryu-Takayanagi entropy for a 2D CFT interval of length l in vacuum.
        S = (c/3) ln(l/ε)   [in units of k_B]
        """
        return (c_central / 3.0) * math.log(max(l / epsilon, 1.0 + 1e-12))

    @staticmethod
    def rt_entropy_thermal(l: float, beta: float, c_central: float = 12.0, epsilon: float = 1e-3) -> float:
        """
        RT entropy at finite temperature β=1/T for a single interval of length l.
        S = (c/3) ln[(β/π) sinh(πl/β) / ε]
        """
        arg = (beta / math.pi) * math.sinh(math.pi * l / beta) / epsilon
        return (c_central / 3.0) * math.log(max(arg, 1.0 + 1e-12))

    @staticmethod
    def mutual_information(l_A: float, l_B: float, l_sep: float,
                            beta: float, c_central: float = 12.0, epsilon: float = 1e-3) -> float:
        """
        Holographic mutual information between two intervals A (length l_A) and B (l_B)
        separated by distance l_sep on a thermal circle.
        I(A:B) = S_A + S_B − S_{A∪B}

        Phase transition: for small l_sep, connected RT surface dominates.
        """
        S_A  = HolographyEngine.rt_entropy_thermal(l_A,            beta, c_central, epsilon)
        S_B  = HolographyEngine.rt_entropy_thermal(l_B,            beta, c_central, epsilon)
        S_AB_connected    = HolographyEngine.rt_entropy_thermal(l_A + l_B + l_sep, beta, c_central, epsilon)
        S_AB_disconnected = S_A + S_B
        S_AB = min(S_AB_connected, S_AB_disconnected)
        return max(S_A + S_B - S_AB, 0.0)

    @staticmethod
    def wormhole_length_growth(t_s: np.ndarray, T_H_K: float, M_kg: float) -> np.ndarray:
        """
        ER=EPR wormhole length growth (eternal BH in AdS).
        Classical: L(t) = 2v_w t  where v_w ~ c (horizon velocity)
        Quantum: L(t) ~ 2 r_s + 2c × max(t − t_scramble, 0)

        Returns L in metres.
        """
        t_scr_s = math.log(
            max(4.0 * math.pi * (M_kg / MP)**2, 2.0)
        ) / QuantumChaosEngine.bh_lyapunov(M_kg)
        r_s = 2.0 * G_SI * M_kg / C_SI**2
        L = 2.0 * r_s + 2.0 * C_SI * np.maximum(t_s - t_scr_s, 0.0)
        return L

    @staticmethod
    def holographic_complexity(t_s: float, M_kg: float) -> float:
        """
        Holographic complexity C_V (Volume conjecture):
        C_V = Vol(maximal slice) / (Gℓ_AdS)
        For large-t: dC/dt = 2 M_ADM / ħ
        C(t) ~ 2 M t / ħ  [in Planck units: C ~ 2 M_planck t_planck t]
        """
        M_P_units = M_kg / MP
        t_P_units = t_s / TP
        return 2.0 * M_P_units * t_P_units

    @staticmethod
    def tfd_entanglement_spectrum(N_modes: int, beta: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Thermofield double state |TFD⟩ = Z^{-1/2} Σ_n exp(−βE_n/2)|n⟩_L|n⟩_R.
        Return (E_n, Schmidt coefficients λ_n = exp(−βE_n)/Z).
        E_n ~ n (harmonic oscillator ladder).
        """
        n_arr = np.arange(N_modes, dtype=float)
        E_n = n_arr    # harmonic spectrum E_n = n
        weights = np.exp(-beta * E_n)
        Z = weights.sum()
        lambdas = weights / Z
        return E_n, lambdas


# ══════════════════════════════════════════════════════════════════════════════
# §11  COOPER'S SINGULARITY CROSSING ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class CooperCrossingEngine:
    """
    Physics of Cooper's journey inside Gargantua:
    interior proper time, TARS data capacity, bulk transmission fidelity,
    quantum decoherence, Murphy's signal bandwidth.
    """

    @staticmethod
    def schwarzschild_interior_proper_time(r0_m: float, M_kg: float) -> float:
        """
        Proper time from radial position r₀ (inside horizon) to the singularity r=0.
        For radial free-fall:
        τ(r₀→0) = (π/2) √(r₀³/(2GM/c²)) × (c/...) 
        
        From exact integration of geodesic equation:
        τ = (2/3) √(r₀/(2GM)) × r₀/c  [simplified]
        
        More precisely: τ = (π/2)(r_s/c)^{1/2} × r₀^{3/2} / r_s ... 
        
        Exact result from Schwarzschild interior metric:
        τ_max(from r=r_s to r=0) = π G M / c³
        τ(r₀) = (π GM/c³) × sin²(η/2)  where cosh²(η/2) = r₀/r_s ... 
        
        Use standard cycloid parameterisation:
        r = (r_s/2)(1 + cos η),  τ = (r_s/2)(η + sin η)/c
        At r=r₀: cos η₀ = 2r₀/r_s − 1, so η₀ = arccos(2r₀/r_s − 1)
        τ(r₀→0) = τ(η₀→π) = (r_s/(2c)) × (π − η₀ + sin η₀)
        """
        r_s = 2.0 * G_SI * M_kg / C_SI**2
        if r0_m >= r_s:
            return 0.0
        cos_eta = 2.0 * r0_m / r_s - 1.0
        cos_eta = max(-1.0, min(1.0, cos_eta))
        eta0 = math.acos(cos_eta)
        tau = (r_s / (2.0 * C_SI)) * (math.pi - eta0 + math.sin(eta0))
        return tau  # seconds

    @staticmethod
    def bekenstein_tars_capacity(E_total_J: float, R_m: float) -> float:
        """
        Bekenstein bound on information capacity of TARS data crystal:
        I ≤ 2π R E / (ħ c ln 2)   [bits]
        E_total_J: total energy of TARS system.
        R_m: characteristic radius (size of crystal).
        """
        bits = 2.0 * math.pi * R_m * E_total_J / (HBAR_SI * C_SI * math.log(2.0))
        return bits

    @staticmethod
    def bulk_transmission_fidelity(y_bulk_planck: float, M_BH_planck: float) -> float:
        """
        Randall-Sundrum bulk transmission: graviton (gravity signal) amplitude
        attenuates as exp(−k|y|) where k is the AdS curvature scale ~ 1/ℓ_P.
        Fidelity = |T|² = exp(−2 k y)  (simplified single-RS brane)
        y in Planck lengths.
        """
        k = 1.0   # k = 1/ℓ_P in Planck units
        return math.exp(-2.0 * k * y_bulk_planck)

    @staticmethod
    def quantum_decoherence_time(T_H_K: float) -> float:
        """
        Thermal decoherence timescale near BH horizon:
        τ_dec = ħ / (k_B T_H)  [SI, seconds]
        """
        return HBAR_SI / (KB_SI * T_H_K)

    @staticmethod
    def murphy_signal_bandwidth(P_signal_W: float, T_noise_K: float, Delta_nu_Hz: float) -> float:
        """
        Shannon capacity of Cooper's gravity channel to Murphy:
        C = Δν × log₂(1 + SNR)  [bits/s]
        SNR = P_signal / (k_B T_noise Δν)
        """
        noise_W = KB_SI * T_noise_K * Delta_nu_Hz
        snr = P_signal_W / max(noise_W, 1e-300)
        return Delta_nu_Hz * math.log2(1.0 + max(snr, 0.0))

    @staticmethod
    def cooper_radial_trajectory(N_pts: int = 600) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Cooper free-fall trajectory inside Gargantua (Schwarzschild approximation).
        Using cycloid parameterisation:
        r(η) = (r_s/2)(1 + cos η),  τ(η) = (r_s/(2c))(η + sin η)
        for η ∈ [η₀, π], starting at r₀ = 0.999 r_s (just below horizon).

        Returns (tau_s, r_m, curvature_R_m2) where R ∝ M/r³ (tidal).
        """
        M_kg = GARG_MASS_KG
        r_s = GARG_RS_M
        # Start just below horizon
        r0 = 0.9999 * r_s
        cos_eta0 = 2.0 * r0 / r_s - 1.0
        eta0 = math.acos(max(-1.0, min(1.0, cos_eta0)))
        eta_arr = np.linspace(eta0 + 1e-6, math.pi - 1e-6, N_pts)

        r_arr  = (r_s / 2.0) * (1.0 + np.cos(eta_arr))
        tau_arr = (r_s / (2.0 * C_SI)) * (eta_arr + np.sin(eta_arr))
        tau_arr -= tau_arr[0]   # zero at entry

        # Tidal curvature: R_tidal ~ GM/r³ (Riemann invariant approximation)
        r_clip = np.maximum(r_arr, r_s * 1e-6)
        curv = G_SI * M_kg / r_clip**3   # s⁻²

        return tau_arr, r_arr, curv

    @staticmethod
    def quantum_state_fidelity(
        tau_arr: np.ndarray, decoherence_rate_Hz: float, entanglement_growth: float = 0.05
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Cooper's quantum state fidelity F(τ) = exp(−γ τ) during singularity crossing.
        Bulk entanglement with TARS grows simultaneously.
        decoherence_rate_Hz: γ = 1/τ_dec [s⁻¹]
        Returns (F_purity, S_entanglement_bits) vs τ.
        """
        F = np.exp(-decoherence_rate_Hz * tau_arr)
        S_ent = entanglement_growth * np.log1p(decoherence_rate_Hz * tau_arr + 1e-30) * 1000.0
        return F, S_ent


# ══════════════════════════════════════════════════════════════════════════════
# §12  FIGURE HELPERS — consistent ENDURANCE aesthetics
# ══════════════════════════════════════════════════════════════════════════════
def _fig_style(ax, title: str = "", xlabel: str = "", ylabel: str = "", invert_x: bool = False):
    """Apply ENDURANCE plot style to a single axes."""
    ax.set_facecolor(_BG2)
    ax.tick_params(colors=_DIM, labelsize=6)
    ax.spines["bottom"].set_color("#101830")
    ax.spines["left"].set_color("#101830")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color="#0c1020", linestyle=":", alpha=0.5, lw=0.5)
    if title:
        ax.set_title(title, color=_GOLD, fontsize=7.5, fontfamily="monospace", pad=4)
    if xlabel:
        ax.set_xlabel(xlabel, color=_DIM, fontsize=6, fontfamily="monospace")
    if ylabel:
        ax.set_ylabel(ylabel, color=_DIM, fontsize=6, fontfamily="monospace")
    if invert_x:
        ax.invert_xaxis()


def _make_fig(rows: int = 1, cols: int = 1, size=(10, 4.5)):
    fig = plt.figure(figsize=size, facecolor=_BG1)
    fig.patch.set_facecolor(_BG1)
    axes = []
    gs = gridspec.GridSpec(rows, cols, figure=fig, hspace=0.45, wspace=0.35)
    for r in range(rows):
        for c in range(cols):
            ax = fig.add_subplot(gs[r, c])
            ax.set_facecolor(_BG2)
            axes.append(ax)
    return fig, axes


# ══════════════════════════════════════════════════════════════════════════════
# §13  TAB 1 — PLANCK FOAM VISUALISATION
# ══════════════════════════════════════════════════════════════════════════════
def _render_planck_foam_tab():
    st.markdown(f"""<p style="font-family:monospace;font-size:0.72rem;color:{_DIM};">
    Wheeler (1955) quantum foam: at the Planck scale ℓ_P ≈ 1.62×10⁻³⁵ m,
    spacetime undergoes violent topology fluctuations — virtual black holes nucleate,
    wormholes open and close, geometry loses all smoothness.
    LQG resolves this by quantising area itself: Δ_A = 4√3πγℓ_P².
    </p>""", unsafe_allow_html=True)

    ps = PlanckState()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div style="background:{_BG2};border:1px solid rgba(128,96,255,0.25);
        border-radius:4px;padding:0.6rem;font-family:monospace;text-align:center;">
        <div style="color:{_DIM};font-size:0.58rem;">PLANCK LENGTH</div>
        <div style="color:{_PURPLE};font-size:1.1rem;font-weight:600;">1.616×10⁻³⁵ m</div>
        <div style="color:{_DIM};font-size:0.55rem;">ℓ_P = √(ħG/c³)</div></div>""",
        unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style="background:{_BG2};border:1px solid rgba(232,196,106,0.25);
        border-radius:4px;padding:0.6rem;font-family:monospace;text-align:center;">
        <div style="color:{_DIM};font-size:0.58rem;">PLANCK ENERGY</div>
        <div style="color:{_GOLD};font-size:1.1rem;font-weight:600;">1.956×10⁹ J</div>
        <div style="color:{_DIM};font-size:0.55rem;">E_P = m_P c²</div></div>""",
        unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div style="background:{_BG2};border:1px solid rgba(79,195,247,0.25);
        border-radius:4px;padding:0.6rem;font-family:monospace;text-align:center;">
        <div style="color:{_DIM};font-size:0.58rem;">LQG AREA GAP</div>
        <div style="color:{_BLUE};font-size:1.1rem;font-weight:600;">{A_MIN_LQG:.3e} m²</div>
        <div style="color:{_DIM};font-size:0.55rem;">Δ_A = 4√3πγℓ_P²</div></div>""",
        unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div style="background:{_BG2};border:1px solid rgba(255,136,0,0.25);
        border-radius:4px;padding:0.6rem;font-family:monospace;text-align:center;">
        <div style="color:{_DIM};font-size:0.58rem;">PLANCK DENSITY</div>
        <div style="color:{_ORANGE};font-size:1.1rem;font-weight:600;">5.155×10⁹⁶ kg/m³</div>
        <div style="color:{_DIM};font-size:0.55rem;">ρ_P = m_P/ℓ_P³</div></div>""",
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Controls ──────────────────────────────────────────────────────────────
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        n_max_area = st.slider("Area eigenvalues (j_max × 2)", 4, 30, 16, 2, key="qs_j_max")
        n_LIV = st.radio("LIV dispersion order n", [1, 2], horizontal=True, key="qs_liv_n")
    with col_c2:
        E_probe_GeV = st.slider("Probe energy (GeV)", 1, int(1e6), 1000, key="qs_E_probe")
        show_foam_power = st.checkbox("Show foam power spectrum", True, key="qs_foam_ps")

    E_probe_J = E_probe_GeV * 1.602e-10   # GeV → Joules
    delta_omega = PlanckFoamEngine.dispersion_correction(E_probe_J, n_LIV)

    j_arr, A_arr = PlanckFoamEngine.granularity_spectrum(n_max_area)
    k_foam, P_foam = PlanckFoamEngine.foam_power_spectrum(N_pts=400)

    fig, axes = _make_fig(1, 3, size=(13, 4.2))
    ax1, ax2, ax3 = axes

    # ── Plot 1: LQG area spectrum ─────────────────────────────────────────────
    colors_j = plt.cm.plasma(np.linspace(0.2, 0.95, len(j_arr)))
    bars = ax1.bar(range(len(j_arr)), A_arr / A_MIN_LQG, color=colors_j, edgecolor=_BG0, linewidth=0.3)
    ax1.axhline(1.0, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label="min area gap")
    _fig_style(ax1, "LQG AREA SPECTRUM", "Spin j index", "A_j / A_min (area units)")
    ax1.set_xticks(range(len(j_arr)))
    ax1.set_xticklabels([f"{jv:.1f}" for jv in j_arr], fontsize=4.5, rotation=60)
    ax1.legend(fontsize=5, framealpha=0.3)

    # ── Plot 2: Virtual BH nucleation rate vs mass ────────────────────────────
    M_range = np.linspace(0.5, 5.0, 120)
    rates = np.array([PlanckFoamEngine.virtual_bh_nucleation_rate(m) for m in M_range])
    ax2.semilogy(M_range, np.maximum(rates, 1e-300), color=_PINK, lw=1.4)
    ax2.axvline(1.0, color=_GOLD, lw=0.8, ls=":", alpha=0.7, label="M = m_P")
    _fig_style(ax2, "VIRTUAL BH NUCLEATION RATE", "M [Planck masses]", "Γ [per Planck 4-vol]")
    ax2.legend(fontsize=5, framealpha=0.3)

    # ── Plot 3: Foam power spectrum OR LIV dispersion ─────────────────────────
    if show_foam_power:
        kLP = k_foam * LP
        ax3.loglog(kLP, P_foam / LP**2, color=_CYAN, lw=1.2)
        ax3.axvline(1.0, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label="k = 1/ℓ_P")
        _fig_style(ax3, "FOAM POWER SPECTRUM", "k·ℓ_P (dimensionless)", "P_h / ℓ_P² [m²]")
        ax3.legend(fontsize=5, framealpha=0.3)
    else:
        E_range_GeV = np.logspace(0, 7, 200)
        E_range_J   = E_range_GeV * 1.602e-10
        dw_n1 = np.array([PlanckFoamEngine.dispersion_correction(E, 1) for E in E_range_J])
        dw_n2 = np.array([PlanckFoamEngine.dispersion_correction(E, 2) for E in E_range_J])
        ax3.loglog(E_range_GeV, dw_n1, color=_PURPLE, lw=1.2, label="n=1 (linear)")
        ax3.loglog(E_range_GeV, dw_n2, color=_GREEN, lw=1.2, label="n=2 (quadratic)")
        ax3.axvline(E_probe_GeV, color=_GOLD, lw=0.8, ls=":")
        _fig_style(ax3, "LIV DISPERSION CORRECTION δω/ω", "E [GeV]", "δω/ω")
        ax3.legend(fontsize=5, framealpha=0.3)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""<p style="font-family:monospace;font-size:0.65rem;color:{_DIM};">
    LIV correction at {E_probe_GeV} GeV (n={n_LIV}):
    <span style="color:{_GOLD};">δω/ω = {delta_omega:.3e}</span> — 
    {'detectable by gamma-ray telescopes' if delta_omega > 1e-17 else 'sub-detection threshold (FERMI-LAT limit ~10⁻¹⁷)'}
    </p>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §14  TAB 2 — LOOP QUANTUM GRAVITY & BOUNCE
# ══════════════════════════════════════════════════════════════════════════════
def _render_lqg_tab():
    st.markdown(f"""<p style="font-family:monospace;font-size:0.72rem;color:{_DIM};">
    Loop Quantum Gravity quantises the gravitational field into spin networks.
    Area and volume become discrete: the Big Bang singularity is replaced by a
    quantum bounce where ρ reaches ρ_crit ≈ 0.41 ρ_P.
    </p>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        gamma_val = st.number_input("Barbero-Immirzi γ", 0.1, 1.0, GAMMA_BI, 0.01, key="qs_gamma",
                                     format="%.4f")
    with col2:
        j_max_spin = st.slider("Spin j_max (half-integer)", 1, 20, 8, 1, key="qs_j_spin")
    with col3:
        wdw_k = st.slider("WdW k factor", 0.1, 5.0, 1.0, 0.1, key="qs_wdw_k")

    # LQC bounce
    t_bounce, a_bounce, H_bounce, rho_bounce = LQGEngine.lqc_bounce_trajectory(N_pts=700)

    # WdW
    alpha_arr = np.linspace(-3.0, 3.0, 500)
    psi_wdw = LQGEngine.wdw_wavefunction(alpha_arr, k_factor=wdw_k)

    # Spin network area spectrum
    j_arr_spin, A_arr_spin = LQGEngine.spin_network_area_eigenvalues(j_max_spin)
    A_min_custom = 8.0 * math.pi * gamma_val * LP**2 * math.sqrt(0.5 * 1.5)  # j=1/2
    A_custom = 8.0 * math.pi * gamma_val * LP**2 * np.sqrt(j_arr_spin * (j_arr_spin + 1.0))

    fig, axes = _make_fig(2, 3, size=(14, 8.5))
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    # ── LQC scale factor bounce ───────────────────────────────────────────────
    ax1.plot(t_bounce, a_bounce, color=_BLUE, lw=1.4, label="a(t)")
    ax1.axvline(0.0, color=_GOLD, lw=0.8, ls="--", alpha=0.6, label="bounce t=0")
    ax1.fill_between(t_bounce, 0, a_bounce, alpha=0.08, color=_BLUE)
    _fig_style(ax1, "LQC BOUNCE: SCALE FACTOR a(t)", "t [Planck units]", "a(t) [normalised]")
    ax1.legend(fontsize=5, framealpha=0.3)

    # ── LQC Hubble parameter ──────────────────────────────────────────────────
    ax2.plot(t_bounce, H_bounce, color=_PURPLE, lw=1.2, label="H(t)")
    ax2.axhline(0.0, color=_DIM, lw=0.5, ls=":")
    ax2.axvline(0.0, color=_GOLD, lw=0.8, ls="--", alpha=0.6, label="bounce")
    _fig_style(ax2, "LQC HUBBLE RATE H(t)", "t [Planck units]", "H [Planck units]")
    ax2.legend(fontsize=5, framealpha=0.3)

    # ── Density through bounce ────────────────────────────────────────────────
    ax3.plot(t_bounce, rho_bounce, color=_ORANGE, lw=1.2, label="ρ(t)/ρ_crit")
    ax3.axhline(1.0, color=_RED, lw=0.8, ls="--", alpha=0.8, label="ρ_crit")
    ax3.axvline(0.0, color=_GOLD, lw=0.8, ls="--", alpha=0.6)
    ax3.set_ylim(-0.05, 1.3)
    _fig_style(ax3, "DENSITY: QUANTUM BOUNCE", "t [Planck units]", "ρ/ρ_crit")
    ax3.legend(fontsize=5, framealpha=0.3)

    # ── WdW wavefunction ─────────────────────────────────────────────────────
    ax4.plot(alpha_arr, psi_wdw**2, color=_CYAN, lw=1.2, label="|Ψ(α)|²")
    ax4.fill_between(alpha_arr, 0, psi_wdw**2, alpha=0.15, color=_CYAN)
    ax4.axvline(0.0, color=_GOLD, lw=0.8, ls="--", alpha=0.6, label="α=0 (a=1)")
    _fig_style(ax4, "WHEELER-DeWITT WAVEFUNCTION", "α = ln(a)", "|Ψ(α)|²")
    ax4.legend(fontsize=5, framealpha=0.3)

    # ── LQG area spectrum (custom γ) ──────────────────────────────────────────
    colors_c = plt.cm.plasma(np.linspace(0.2, 0.9, len(j_arr_spin)))
    ax5.bar(range(len(j_arr_spin)), A_custom / A_min_custom, color=colors_c,
            edgecolor=_BG0, linewidth=0.3)
    ax5.axhline(1.0, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label=f"A_min (γ={gamma_val:.4f})")
    _fig_style(ax5, f"LQG AREA SPECTRUM (γ={gamma_val:.4f})", "j index", "A/A_min")
    ax5.legend(fontsize=5, framealpha=0.3)

    # ── Volume eigenvalues vs j ───────────────────────────────────────────────
    j_vol = np.linspace(0.5, float(j_max_spin), 60)
    V_vol = np.array([LQGEngine.volume_eigenvalue_approx(j) for j in j_vol])
    ax6.plot(j_vol, V_vol / LP**3, color=_GREEN, lw=1.4)
    ax6.fill_between(j_vol, 0, V_vol / LP**3, alpha=0.12, color=_GREEN)
    _fig_style(ax6, "LQG VOLUME EIGENVALUES", "j (spin)", "V [ℓ_P³]")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    rho_crit_val = RHO_CRIT_LQC
    st.markdown(f"""<div style="background:{_BG2};border:1px solid rgba(79,195,247,0.15);
    border-radius:4px;padding:0.6rem 1rem;font-family:monospace;font-size:0.65rem;color:{_DIM};">
    ρ_crit = {rho_crit_val:.3e} kg/m³ = 0.41 ρ_P &nbsp;·&nbsp;
    A_min(γ={gamma_val:.4f}) = {A_min_custom:.3e} m² &nbsp;·&nbsp;
    Bounce replaces classical singularity: Big Bang → Big Bounce at ρ = ρ_crit
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §15  TAB 3 — BKL SINGULARITY & KASNER OSCILLATIONS
# ══════════════════════════════════════════════════════════════════════════════
def _render_bkl_tab():
    st.markdown(f"""<p style="font-family:monospace;font-size:0.72rem;color:{_DIM};">
    The BKL (Belinskii-Khalatnikov-Lifshitz) analysis shows that generic spacelike
    singularities exhibit chaotic oscillations between Kasner epochs.
    Each epoch has metric ds²= −dt² + t^{"{"}2p₁{"}"}dx² + … with Σp_i=1, Σp_i²=1.
    The BKL map u→u−1 (u>2) or 1/(u−1) generates the mixmaster chaos.
    </p>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        u0_val = st.number_input("Initial BKL parameter u₀", 1.01, 20.0, 7.3, 0.1, key="qs_u0",
                                  format="%.2f")
        N_ep = st.slider("Number of Kasner epochs", 10, 80, 45, 5, key="qs_n_ep")
    with col2:
        show_bianchi = st.checkbox("Show Bianchi IX scale factors", True, key="qs_bianchi")

    epochs = BKLEngine.mixmaster_sequence(u0_val, N_ep)
    tau_b, a_b, b_b, c_b = BKLEngine.bianchi_ix_scale_factors(N_pts=600)

    u_seq     = [ep["u"]  for ep in epochs]
    p1_seq    = [ep["p1"] for ep in epochs]
    p2_seq    = [ep["p2"] for ep in epochs]
    p3_seq    = [ep["p3"] for ep in epochs]
    era_seq   = [ep["era"] for ep in epochs]

    fig, axes = _make_fig(2, 3, size=(14, 8.0))
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    # ── u parameter sequence ─────────────────────────────────────────────────
    idx = np.arange(len(u_seq))
    ax1.step(idx, u_seq, where="mid", color=_BLUE, lw=1.0)
    ax1.scatter(idx, u_seq, c=u_seq, cmap="plasma", s=12, zorder=4, vmin=1, vmax=max(u_seq)+1)
    ax1.axhline(2.0, color=_GOLD, lw=0.8, ls="--", alpha=0.6, label="u=2 (era boundary)")
    _fig_style(ax1, "BKL u-PARAMETER SEQUENCE", "Epoch index", "u value")
    ax1.legend(fontsize=5, framealpha=0.3)

    # ── Kasner exponents ──────────────────────────────────────────────────────
    ax2.plot(idx, p1_seq, color=_RED, lw=1.0, label="p₁ (negative)")
    ax2.plot(idx, p2_seq, color=_BLUE, lw=1.0, label="p₂")
    ax2.plot(idx, p3_seq, color=_GREEN, lw=1.0, label="p₃ (largest)")
    ax2.axhline(0.0, color=_DIM, lw=0.5, ls=":")
    _fig_style(ax2, "KASNER EXPONENTS vs EPOCH", "Epoch index", "p_i")
    ax2.legend(fontsize=5, framealpha=0.3)

    # ── Kasner triangle (p1-p2-p3 phase space) ───────────────────────────────
    ax3.scatter(p1_seq, p3_seq, c=era_seq, cmap="plasma", s=14, alpha=0.85,
                vmin=min(era_seq), vmax=max(era_seq)+1)
    ax3.axhline(0, color=_DIM, lw=0.4, ls=":")
    ax3.axvline(0, color=_DIM, lw=0.4, ls=":")
    # Kasner circle: p1²+p3² ≤ 1, p1+p3 ≤ 1
    _fig_style(ax3, "KASNER PHASE PORTRAIT (p₁ vs p₃)", "p₁", "p₃")
    ax3.set_xlim(-0.55, 0.05)
    ax3.set_ylim(-0.05, 1.05)

    # ── Era histogram ────────────────────────────────────────────────────────
    max_era = max(era_seq) + 1
    era_counts = [era_seq.count(e) for e in range(max_era)]
    ax4.bar(range(max_era), era_counts, color=_PURPLE, edgecolor=_BG0, lw=0.3)
    _fig_style(ax4, "EPOCHS PER BKL ERA", "Era index", "Epoch count")

    # ── Bianchi IX scale factors ──────────────────────────────────────────────
    if show_bianchi:
        ax5.semilogy(tau_b, a_b, color=_BLUE,   lw=1.0, label="a(τ)")
        ax5.semilogy(tau_b, b_b, color=_GREEN,  lw=1.0, label="b(τ)")
        ax5.semilogy(tau_b, np.maximum(c_b, 1e-8), color=_RED, lw=1.0, label="c(τ)")
        _fig_style(ax5, "BIANCHI IX SCALE FACTORS", "τ (log-time)", "Scale factor")
        ax5.legend(fontsize=5, framealpha=0.3)

    # ── Anisotropy metric ─────────────────────────────────────────────────────
    anisotropy = np.array(p1_seq)**2 + np.array(p2_seq)**2 + np.array(p3_seq)**2
    ax6.plot(idx, anisotropy, color=_ORANGE, lw=1.2, label="Σp²_i")
    ax6.axhline(1.0, color=_GOLD, lw=0.8, ls="--", alpha=0.6, label="Kasner constraint Σp²=1")
    ax6.set_ylim(0.95, 1.05)
    _fig_style(ax6, "KASNER CONSISTENCY CHECK Σp²", "Epoch", "Σp²_i")
    ax6.legend(fontsize=5, framealpha=0.3)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Epoch table
    df_epochs = pd.DataFrame([{
        "epoch": i, "u": f"{ep['u']:.4f}",
        "p₁": f"{ep['p1']:.4f}", "p₂": f"{ep['p2']:.4f}", "p₃": f"{ep['p3']:.4f}",
        "era": ep["era"], "Σp": f"{ep['p1']+ep['p2']+ep['p3']:.6f}",
        "Σp²": f"{ep['p1']**2+ep['p2']**2+ep['p3']**2:.6f}"
    } for i, ep in enumerate(epochs[:20])])
    st.dataframe(df_epochs, use_container_width=True, height=280)


# ══════════════════════════════════════════════════════════════════════════════
# §16  TAB 4 — HAWKING INFORMATION & PAGE CURVE
# ══════════════════════════════════════════════════════════════════════════════
def _render_page_curve_tab():
    st.markdown(f"""<p style="font-family:monospace;font-size:0.72rem;color:{_DIM};">
    Page (1993): if black hole evaporation is unitary, the entanglement entropy
    of Hawking radiation must peak at the Page time t_Page ≈ t_evap/2 and then
    decrease. The island rule (Almheiri et al. 2020) provides the QFT mechanism:
    a quantum extremal surface inside the BH contributes to S_ent for t > t_Page.
    </p>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        M0_planck = st.number_input("Initial BH mass [Planck masses]", 10.0, 5000.0, 500.0, 50.0,
                                     key="qs_M_page", format="%.0f")
    with col2:
        alpha_isl = st.slider("Island correction factor α", 0.01, 0.2, 0.05, 0.005, key="qs_alpha_isl")
    with col3:
        show_scramble = st.checkbox("Show OTOC scrambling", True, key="qs_show_otoc")

    engine = PageCurveEngine(M0_planck)
    state  = engine.state

    t_norm = np.linspace(0.0, state.t_evap * 1.05, 600)
    S_bh   = engine.bh_entropy(t_norm)
    S_hawk = engine.hawking_radiation_entropy(t_norm)
    S_page = engine.page_curve_entropy(t_norm)
    S_isl  = engine.island_entropy(t_norm, alpha_isl)

    t_scr_s, F_otoc = engine.scrambling_diagnostic(500)

    fig, axes = _make_fig(2, 3, size=(14, 8.0))
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    # ── Page curve ────────────────────────────────────────────────────────────
    t_n = t_norm / state.t_evap   # normalised to t_evap
    ax1.plot(t_n, S_bh   / state.S_BH0, color=_BLUE,   lw=1.2, label="S_BH(t)")
    ax1.plot(t_n, S_hawk / state.S_BH0, color=_RED,    lw=1.0, ls="--", label="S_Hawking (semi-cl.)")
    ax1.plot(t_n, S_page / state.S_BH0, color=_GREEN,  lw=1.5, label="Page curve")
    ax1.plot(t_n, S_isl  / state.S_BH0, color=_PURPLE, lw=1.2, ls=":", label="Island corrected")
    ax1.axvline(0.5, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label="t_Page")
    ax1.axvline(state.t_scr / state.t_evap, color=_CYAN, lw=0.7, ls=":", alpha=0.7, label="t_scr")
    _fig_style(ax1, "PAGE CURVE & ISLAND RULE", "t / t_evap", "S / S_BH(0)")
    ax1.legend(fontsize=5, framealpha=0.3)

    # ── BH mass evolution ─────────────────────────────────────────────────────
    M_t = engine.mass_at_time(t_norm)
    ax2.plot(t_n, M_t / M0_planck, color=_ORANGE, lw=1.3)
    ax2.fill_between(t_n, 0, M_t / M0_planck, alpha=0.1, color=_ORANGE)
    ax2.axvline(0.5, color=_GOLD, lw=0.8, ls="--", alpha=0.6)
    _fig_style(ax2, "BH MASS EVAPORATION M(t)/M₀", "t / t_evap", "M(t)/M₀")

    # ── Entropy difference ΔS = S_BH - S_Page ────────────────────────────────
    delta_S = S_bh - S_page
    ax3.plot(t_n, delta_S / state.S_BH0, color=_PINK, lw=1.2, label="S_BH − S_Page")
    ax3.fill_between(t_n, 0, delta_S / state.S_BH0, alpha=0.12, color=_PINK)
    ax3.axvline(0.5, color=_GOLD, lw=0.8, ls="--", alpha=0.6)
    _fig_style(ax3, "ENTROPY GAP: SEMI-CLASSICAL vs UNITARY", "t/t_evap", "ΔS/S₀")
    ax3.legend(fontsize=5, framealpha=0.3)

    # ── OTOC ─────────────────────────────────────────────────────────────────
    t_scr_n = t_scr_s / state.t_scr
    ax4.plot(t_scr_s / state.t_scr, F_otoc, color=_CYAN, lw=1.2, label="F(t)/F(0)")
    ax4.axhline(0.0, color=_DIM, lw=0.5, ls=":")
    ax4.axvline(1.0, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label="t_scr")
    ax4.axhline(1.0 / state.S_BH0, color=_RED, lw=0.7, ls=":", label="1/S_BH (noise floor)")
    _fig_style(ax4, "OTOC: SCRAMBLING DIAGNOSTIC", "t / t_scr", "F(t)")
    ax4.legend(fontsize=5, framealpha=0.3)
    ax4.set_xlim(0, 3)

    # ── Hawking temperature vs mass ───────────────────────────────────────────
    M_range = np.linspace(1.0, M0_planck, 300)
    T_H_range = 1.0 / (8.0 * math.pi * M_range)   # Planck units: T_H = 1/(8πM)
    ax5.plot(M_range / M0_planck, T_H_range / (1.0 / (8.0 * math.pi * 1.0)), color=_RED, lw=1.3)
    ax5.axvline(1.0 / M0_planck, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label="Planck remnant")
    _fig_style(ax5, "HAWKING TEMPERATURE vs MASS", "M/M₀", "T_H [Planck units]")
    ax5.legend(fontsize=5, framealpha=0.3)

    # ── Scrambling time vs mass ────────────────────────────────────────────────
    M_srange = np.linspace(10.0, M0_planck * 2, 300)
    t_scr_range = (4.0 * M_srange / (2.0 * math.pi)) * np.log(4.0 * math.pi * M_srange**2 + 1.0)
    ax6.plot(M_srange, t_scr_range / (5120.0 * math.pi * M_srange**3) * 100, color=_GREEN, lw=1.2)
    _fig_style(ax6, "SCRAMBLING vs EVAPORATION TIME RATIO", "M [m_P]", "t_scr/t_evap [%]")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""<div style="display:flex;gap:1rem;flex-wrap:wrap;">
    <div style="background:{_BG2};border:1px solid rgba(232,196,106,0.2);border-radius:4px;
    padding:0.5rem 1rem;font-family:monospace;font-size:0.65rem;color:{_DIM};">
      M₀ = {M0_planck:.0f} m_P &nbsp;·&nbsp; S_BH(0) = {state.S_BH0:.3e} &nbsp;·&nbsp;
      t_evap = {state.t_evap:.3e} t_P &nbsp;·&nbsp; t_Page = {state.t_page:.3e} t_P &nbsp;·&nbsp;
      t_scr = {state.t_scr:.3e} t_P
    </div></div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §17  TAB 5 — UNRUH EFFECT & VACUUM PHYSICS
# ══════════════════════════════════════════════════════════════════════════════
def _render_unruh_tab():
    st.markdown(f"""<p style="font-family:monospace;font-size:0.72rem;color:{_DIM};">
    An observer undergoing uniform acceleration a perceives the Minkowski vacuum
    as a thermal bath at T_U = ℏa/(2πck_B) (Unruh 1976).
    For the ENDURANCE crew near Gargantua, Casimir and Schwinger effects define
    the quantum vacuum structure of the local spacetime.
    </p>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        log_a = st.slider("Acceleration log₁₀(a) [m/s²]", 0.0, 30.0, 20.0, 0.5, key="qs_log_a")
        a_ms2 = 10.0**log_a
    with col2:
        d_nm = st.slider("Casimir plate separation d [nm]", 1, 1000, 100, 1, key="qs_d_nm")
        d_m  = d_nm * 1e-9
    with col3:
        log_E_field = st.slider("E-field log₁₀(E) [V/m]", 10.0, 19.0, 16.0, 0.1, key="qs_E_field")
        E_field = 10.0**log_E_field

    T_unruh = UnruhVacuumEngine.unruh_temperature(a_ms2)
    P_cas   = UnruhVacuumEngine.casimir_pressure(d_m)
    E_cas   = UnruhVacuumEngine.casimir_energy(d_m, 1.0)  # per m²
    W_sch   = UnruhVacuumEngine.schwinger_pair_rate(E_field)
    rho_vac = UnruhVacuumEngine.vacuum_energy_density_qed()

    # Unruh spectrum
    omega_arr = np.logspace(8, 18, 400)  # rad/s
    spectrum  = UnruhVacuumEngine.unruh_spectrum(omega_arr, a_ms2)

    # Casimir force vs d
    d_range   = np.logspace(-10, -6, 300)  # 0.1 nm → 1 μm
    P_range   = np.abs([UnruhVacuumEngine.casimir_pressure(d) for d in d_range])

    # Schwinger rate vs field
    E_range   = np.logspace(14, 19, 300)
    W_range   = np.array([UnruhVacuumEngine.schwinger_pair_rate(E) for E in E_range])

    fig, axes = _make_fig(2, 3, size=(14, 8.0))
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    # ── Unruh spectrum ────────────────────────────────────────────────────────
    ax1.loglog(omega_arr, spectrum, color=_BLUE, lw=1.3)
    ax1.fill_between(omega_arr, 1e-30, spectrum, alpha=0.1, color=_BLUE)
    _fig_style(ax1, f"UNRUH THERMAL SPECTRUM (a={a_ms2:.1e} m/s²)", "ω [rad/s]", "n̄(ω)")

    # ── Unruh temperature vs acceleration ─────────────────────────────────────
    a_range = np.logspace(10, 32, 400)
    T_range = np.array([UnruhVacuumEngine.unruh_temperature(a) for a in a_range])
    ax2.loglog(a_range, T_range, color=_PURPLE, lw=1.3)
    ax2.axvline(a_ms2, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label=f"a={a_ms2:.1e}")
    ax2.axhline(T_unruh, color=_GOLD, lw=0.8, ls="--", alpha=0.5)
    ax2.axvline(C_SI**2 / LP, color=_PINK, lw=0.8, ls=":", alpha=0.6, label="Planck accel.")
    _fig_style(ax2, "UNRUH TEMPERATURE vs ACCELERATION", "a [m/s²]", "T_U [K]")
    ax2.legend(fontsize=5, framealpha=0.3)

    # ── Casimir pressure vs separation ────────────────────────────────────────
    ax3.loglog(d_range * 1e9, P_range, color=_GREEN, lw=1.3)
    ax3.axvline(d_nm, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label=f"d={d_nm} nm")
    ax3.axhline(abs(P_cas), color=_GOLD, lw=0.5, ls="--", alpha=0.5)
    _fig_style(ax3, "CASIMIR PRESSURE |P| vs SEPARATION", "d [nm]", "|P| [Pa]")
    ax3.legend(fontsize=5, framealpha=0.3)

    # ── Schwinger rate vs field ───────────────────────────────────────────────
    mask_pos = W_range > 1e-300
    if mask_pos.any():
        ax4.semilogy(np.log10(E_range[mask_pos]), W_range[mask_pos], color=_RED, lw=1.3)
    ax4.axvline(np.log10(E_SCHWINGER), color=_GOLD, lw=0.8, ls="--", alpha=0.7,
                label=f"E_crit = {E_SCHWINGER:.2e} V/m")
    ax4.axvline(log_E_field, color=_CYAN, lw=0.8, ls=":", alpha=0.7)
    _fig_style(ax4, "SCHWINGER PAIR RATE vs E-FIELD", "log₁₀(E [V/m])", "Γ [pairs/m³/s]")
    ax4.legend(fontsize=5, framealpha=0.3)

    # ── Vacuum energy density ─────────────────────────────────────────────────
    k_planck_cut = np.logspace(-3, 0, 200) / LP  # k from 0 to 1/ℓ_P
    rho_k = HBAR_SI * C_SI * k_planck_cut**4 / (16.0 * math.pi**2)
    ax5.loglog(k_planck_cut * LP, rho_k, color=_ORANGE, lw=1.3)
    ax5.axvline(1.0, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label="k = 1/ℓ_P")
    _fig_style(ax5, "QED VACUUM ENERGY DENSITY", "k·ℓ_P (Planck units)", "ρ_vac [J/m³]")
    ax5.legend(fontsize=5, framealpha=0.3)

    # ── Summary metrics ───────────────────────────────────────────────────────
    labels = ["T_Unruh [K]", "|P_Casimir| [Pa]", "E_Casimir/m² [J/m²]",
              "Schwinger Γ\n[pairs/m³s]", "ρ_vac [J/m³]"]
    vals   = [T_unruh, abs(P_cas), abs(E_cas), max(W_sch, 1e-300), rho_vac]
    colors = [_BLUE, _GREEN, _CYAN, _RED, _ORANGE]
    log_vals = [math.log10(max(v, 1e-300)) for v in vals]
    bar_colors = colors
    bars = ax6.barh(labels, log_vals, color=bar_colors, edgecolor=_BG0, lw=0.3)
    _fig_style(ax6, "VACUUM PHYSICS SUMMARY [log₁₀]", "log₁₀(value)", "")
    for bar, lv in zip(bars, log_vals):
        ax6.text(lv + 0.1, bar.get_y() + bar.get_height() / 2,
                 f"{10**lv:.2e}", va="center", fontsize=4.5, color=_GOLD, fontfamily="monospace")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# §18  TAB 6 — QUANTUM CHAOS, OTOC & SYK
# ══════════════════════════════════════════════════════════════════════════════
def _render_chaos_tab():
    st.markdown(f"""<p style="font-family:monospace;font-size:0.72rem;color:{_DIM};">
    Maldacena, Shenker & Stanovic (2016): quantum chaos is bounded
    λ_L ≤ 2πk_BT/ℏ. Black holes are the fastest scramblers in nature —
    they saturate this bound. The SYK model is the minimal holographic
    model of a black hole, with exactly solvable quantum chaos.
    </p>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        N_maj   = st.slider("SYK: N Majorana fermions", 8, 64, 32, 4, key="qs_N_maj")
        J_syk   = st.number_input("SYK coupling J", 0.1, 5.0, 1.0, 0.1, key="qs_J_syk", format="%.1f")
    with col2:
        beta_syk = st.slider("β = 1/T (SYK)", 0.5, 30.0, 8.0, 0.5, key="qs_beta_syk")
        seed_lvl = st.number_input("RMT seed", 1, 999, 42, 1, key="qs_rmt_seed")
    with col3:
        M_chaos_msun = st.number_input("BH mass [M_sun] for Lyapunov",
                                        1.0, 1e9, 1e8, 1e7,
                                        format="%.2e", key="qs_M_chaos")

    M_chaos_kg = M_chaos_msun * M_SUN
    lambda_L_bh = QuantumChaosEngine.bh_lyapunov(M_chaos_kg)
    T_H_chaos   = HBAR_SI * C_SI**3 / (8.0 * math.pi * G_SI * M_chaos_kg * KB_SI)
    chaos_bound = QuantumChaosEngine.chaos_bound_temperature(T_H_chaos)

    omega_syk = np.linspace(-4.0 * J_syk, 4.0 * J_syk, 600)
    rho_syk   = QuantumChaosEngine.syk_spectral_density(omega_syk, J_syk, N_maj, q=4)

    s_mid, p_s = QuantumChaosEngine.level_spacing_gue(N_levels=int(seed_lvl) + 150, seed=int(seed_lvl))
    # Wigner-Dyson GUE analytic
    s_an     = np.linspace(0.01, 4.0, 200)
    P_gue_an = (32.0 / math.pi**2) * s_an**2 * np.exp(-4.0 * s_an**2 / math.pi)
    P_poi_an = np.exp(-s_an)   # Poisson (integrable comparison)

    t_sff, SFF = QuantumChaosEngine.spectral_form_factor(
        beta_syk, t_max=200.0, N_pts=400, N_levels=int(seed_lvl) + 150, seed=int(seed_lvl)
    )

    fig, axes = _make_fig(2, 3, size=(14, 8.0))
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    # ── SYK spectral density ──────────────────────────────────────────────────
    ax1.plot(omega_syk, rho_syk, color=_PURPLE, lw=1.4)
    ax1.fill_between(omega_syk, 0, rho_syk, alpha=0.15, color=_PURPLE)
    _fig_style(ax1, f"SYK SPECTRAL DENSITY (N={N_maj}, J={J_syk})", "E [J units]", "ρ(E)")

    # ── Level spacing statistics ──────────────────────────────────────────────
    ax2.bar(s_mid, p_s, width=(s_mid[1]-s_mid[0])*0.9, color=_BLUE, alpha=0.6,
            label="Numerical GUE")
    ax2.plot(s_an, P_gue_an, color=_GOLD, lw=1.3, label="Wigner-Dyson GUE")
    ax2.plot(s_an, P_poi_an, color=_RED,  lw=1.0, ls="--", label="Poisson (integrable)")
    _fig_style(ax2, "LEVEL SPACING STATISTICS P(s)", "s/⟨s⟩", "P(s)")
    ax2.legend(fontsize=5, framealpha=0.3)
    ax2.set_xlim(0, 4)

    # ── Spectral form factor ──────────────────────────────────────────────────
    ax3.semilogy(t_sff, np.maximum(SFF, 1e-6), color=_CYAN, lw=1.0)
    ax3.axhline(1.0 / (N_maj + 150), color=_GOLD, lw=0.8, ls="--", alpha=0.7, label="Plateau 1/L")
    _fig_style(ax3, f"SPECTRAL FORM FACTOR (β={beta_syk})", "t", "SFF(t)")
    ax3.legend(fontsize=5, framealpha=0.3)

    # ── Lyapunov vs T ────────────────────────────────────────────────────────
    T_range_K = np.logspace(-5, 7, 400)
    lambda_bound = np.array([QuantumChaosEngine.chaos_bound_temperature(T) for T in T_range_K])
    ax4.loglog(T_range_K, lambda_bound, color=_GREEN, lw=1.3, label="MSS bound 2πkT/ℏ")
    ax4.axvline(T_H_chaos, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label=f"T_H Gargantua")
    ax4.axhline(lambda_L_bh, color=_ORANGE, lw=0.8, ls=":", alpha=0.7, label=f"λ_L BH = {lambda_L_bh:.3e} s⁻¹")
    _fig_style(ax4, "CHAOS BOUND λ_L ≤ 2πk_BT/ℏ", "T [K]", "λ_L [s⁻¹]")
    ax4.legend(fontsize=5, framealpha=0.3)

    # ── BH scrambling time vs mass ────────────────────────────────────────────
    M_range_msun = np.logspace(0, 10, 300)
    M_range_kg   = M_range_msun * M_SUN
    lambda_range = np.array([QuantumChaosEngine.bh_lyapunov(M) for M in M_range_kg])
    T_H_range    = HBAR_SI * C_SI**3 / (8.0 * math.pi * G_SI * M_range_kg * KB_SI)
    S_BH_range   = 4.0 * math.pi * (M_range_kg / MP)**2
    t_scr_range  = np.log(S_BH_range) / lambda_range / (3.156e7)  # years
    ax5.loglog(M_range_msun, t_scr_range, color=_PINK, lw=1.3)
    ax5.axvline(M_chaos_msun, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label=f"M_Garg")
    _fig_style(ax5, "BH SCRAMBLING TIME t_scr vs M", "M [M_sun]", "t_scr [years]")
    ax5.legend(fontsize=5, framealpha=0.3)

    # ── OTOC for BH ───────────────────────────────────────────────────────────
    t_bh_s = np.linspace(0, 5.0 / lambda_L_bh, 500)
    F_bh   = QuantumChaosEngine.otoc(t_bh_s.copy(), T_H_chaos, M_chaos_kg, N_dof=int(S_BH_range.min()))
    ax6.plot(t_bh_s * lambda_L_bh, F_bh, color=_RED, lw=1.2)
    ax6.axhline(0.0, color=_DIM, lw=0.5, ls=":")
    ax6.axvline(math.log(S_BH_range[0]) if S_BH_range[0] > 1 else 5.0,
                color=_GOLD, lw=0.8, ls="--", alpha=0.7, label="t_scr × λ_L")
    _fig_style(ax6, "OTOC F(t) — BH INFORMATION SCRAMBLING", "t·λ_L (dimensionless)", "F(t)/F(0)")
    ax6.legend(fontsize=5, framealpha=0.3)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(f"""<div style="font-family:monospace;font-size:0.65rem;color:{_DIM};
    background:{_BG2};border:1px solid rgba(128,96,255,0.15);border-radius:4px;padding:0.5rem 1rem;">
    Gargantua (M={M_chaos_msun:.2e} M☉): &nbsp;
    T_H = <span style="color:{_GOLD};">{T_H_chaos:.3e} K</span> &nbsp;·&nbsp;
    λ_L = <span style="color:{_GOLD};">{lambda_L_bh:.3e} s⁻¹</span> &nbsp;·&nbsp;
    MSS bound = <span style="color:{_GREEN};">{chaos_bound:.3e} s⁻¹</span> &nbsp;·&nbsp;
    Ratio λ_L/bound = <span style="color:{'#81C784' if abs(lambda_L_bh/chaos_bound - 1) < 0.01 else _RED};">
    {lambda_L_bh / chaos_bound:.6f}</span> (should be 1.0)
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §19  TAB 7 — HOLOGRAPHY & ER=EPR
# ══════════════════════════════════════════════════════════════════════════════
def _render_holography_tab():
    st.markdown(f"""<p style="font-family:monospace;font-size:0.72rem;color:{_DIM};">
    Ryu-Takayanagi (2006): entanglement entropy = area of minimal bulk surface / 4G.
    Maldacena-Susskind (2013): every Einstein-Rosen bridge corresponds to an
    entangled quantum state (ER=EPR). Gargantua and its hypothetical mirror form
    the thermofield double — connected by a growing wormhole.
    </p>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        c_cft = st.slider("CFT central charge c", 1, 100, 12, 1, key="qs_c_cft")
        l_interval = st.slider("Interval length l [AdS units]", 0.1, 10.0, 3.0, 0.1, key="qs_l_int")
    with col2:
        beta_cft = st.slider("β = 1/T [AdS units]", 0.5, 20.0, 5.0, 0.5, key="qs_beta_cft")
        epsilon_uv = st.number_input("UV cutoff ε", 1e-4, 0.1, 1e-3, format="%.0e", key="qs_eps_uv")
    with col3:
        M_er_epr_msun = st.number_input("BH mass [M_sun] for ER=EPR",
                                          1.0, 1e9, 1e8, 1e7,
                                          format="%.2e", key="qs_M_er_epr")
        N_tfd_modes   = st.slider("TFD Schmidt modes", 5, 50, 20, 5, key="qs_N_tfd")

    M_er_kg = M_er_epr_msun * M_SUN
    T_H_er  = HBAR_SI * C_SI**3 / (8.0 * math.pi * G_SI * M_er_kg * KB_SI)

    # RT entropy vs interval length
    l_arr  = np.linspace(0.01, 15.0, 300)
    S_vac  = np.array([HolographyEngine.rt_entropy_vacuum(l, c_cft, epsilon_uv) for l in l_arr])
    S_th   = np.array([HolographyEngine.rt_entropy_thermal(l, beta_cft, c_cft, epsilon_uv) for l in l_arr])

    # Mutual information vs separation
    sep_arr = np.linspace(0.01, 8.0, 300)
    l_A = l_B = l_interval / 2.0
    MI_arr  = np.array([HolographyEngine.mutual_information(l_A, l_B, s, beta_cft, c_cft, epsilon_uv)
                         for s in sep_arr])

    # ER=EPR wormhole growth
    t_wh_s = np.linspace(0.0, 4.0 * G_SI * M_er_kg / C_SI**3, 400)
    L_wh   = HolographyEngine.wormhole_length_growth(t_wh_s, T_H_er, M_er_kg)

    # TFD spectrum
    E_tfd, lam_tfd = HolographyEngine.tfd_entanglement_spectrum(N_tfd_modes, beta=beta_cft)
    S_tfd_von_Neumann = -np.sum(lam_tfd * np.log(lam_tfd + 1e-30))

    # Holographic complexity growth
    t_cmpl = np.linspace(0.0, 3.0 * G_SI * M_er_kg / C_SI**3, 300)
    C_comp = np.array([HolographyEngine.holographic_complexity(t, M_er_kg) for t in t_cmpl])

    fig, axes = _make_fig(2, 3, size=(14, 8.0))
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    # ── RT entropy vs interval ─────────────────────────────────────────────────
    ax1.plot(l_arr, S_vac, color=_BLUE,   lw=1.2, label="Vacuum S(l)")
    ax1.plot(l_arr, S_th,  color=_ORANGE, lw=1.2, label=f"Thermal (β={beta_cft})")
    ax1.axvline(l_interval, color=_GOLD, lw=0.8, ls="--", alpha=0.7)
    _fig_style(ax1, f"RT ENTANGLEMENT ENTROPY (c={c_cft})", "l [AdS units]", "S_EE [k_B]")
    ax1.legend(fontsize=5, framealpha=0.3)

    # ── Mutual information ────────────────────────────────────────────────────
    ax2.plot(sep_arr, MI_arr, color=_PURPLE, lw=1.3, label="I(A:B)")
    ax2.fill_between(sep_arr, 0, MI_arr, alpha=0.12, color=_PURPLE)
    ax2.axhline(0.0, color=_DIM, lw=0.5, ls=":")
    _fig_style(ax2, "HOLOGRAPHIC MUTUAL INFORMATION", "Separation d [AdS units]", "I(A:B) [k_B]")
    ax2.legend(fontsize=5, framealpha=0.3)

    # ── TFD Schmidt spectrum ──────────────────────────────────────────────────
    ax3.bar(E_tfd, lam_tfd, color=_CYAN, edgecolor=_BG0, lw=0.3, width=0.7)
    ax3.set_title(f"TFD ENTANGLEMENT SPECTRUM (β={beta_cft})", color=_GOLD,
                  fontsize=7.5, fontfamily="monospace")
    ax3.set_facecolor(_BG2)
    ax3.tick_params(colors=_DIM, labelsize=6)
    ax3.spines["bottom"].set_color("#101830")
    ax3.spines["left"].set_color("#101830")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.grid(True, color="#0c1020", linestyle=":", alpha=0.5, lw=0.5)
    ax3.text(0.98, 0.95, f"S_vN = {S_tfd_von_Neumann:.3f} k_B", transform=ax3.transAxes,
             ha="right", va="top", color=_GOLD, fontsize=6, fontfamily="monospace")
    ax3.set_xlabel("Mode n", color=_DIM, fontsize=6, fontfamily="monospace")
    ax3.set_ylabel("λ_n", color=_DIM, fontsize=6, fontfamily="monospace")

    # ── ER=EPR wormhole growth ────────────────────────────────────────────────
    r_s_er = 2.0 * G_SI * M_er_kg / C_SI**2
    ax4.plot(t_wh_s / (G_SI * M_er_kg / C_SI**3), L_wh / r_s_er,
             color=_GREEN, lw=1.3, label="L(t)/r_s")
    ax4.axvline(0.0, color=_DIM, lw=0.5, ls=":")
    _fig_style(ax4, "ER=EPR WORMHOLE LENGTH GROWTH", "t [GM/c³ units]", "L / r_s")
    ax4.legend(fontsize=5, framealpha=0.3)

    # ── RT entropy: vacuum vs thermal at fixed l ───────────────────────────────
    beta_range = np.linspace(0.5, 30.0, 300)
    S_at_l = np.array([HolographyEngine.rt_entropy_thermal(l_interval, b, c_cft, epsilon_uv)
                        for b in beta_range])
    ax5.plot(beta_range, S_at_l, color=_PINK, lw=1.3, label=f"S_EE(l={l_interval})")
    ax5.axvline(beta_cft, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label=f"β={beta_cft}")
    _fig_style(ax5, "RT ENTROPY vs TEMPERATURE", "β = 1/T [AdS units]", f"S_EE(l={l_interval})")
    ax5.legend(fontsize=5, framealpha=0.3)

    # ── Holographic complexity ────────────────────────────────────────────────
    ax6.plot(t_cmpl / (G_SI * M_er_kg / C_SI**3), C_comp, color=_ORANGE, lw=1.3)
    ax6.set_yscale("log")
    _fig_style(ax6, "HOLOGRAPHIC COMPLEXITY C_V(t)", "t [GM/c³]", "C_V [Planck units]")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    S_rt_vac = HolographyEngine.rt_entropy_vacuum(l_interval, c_cft, epsilon_uv)
    S_rt_th  = HolographyEngine.rt_entropy_thermal(l_interval, beta_cft, c_cft, epsilon_uv)
    st.markdown(f"""<div style="font-family:monospace;font-size:0.65rem;color:{_DIM};
    background:{_BG2};border:1px solid rgba(79,195,247,0.15);border-radius:4px;padding:0.5rem 1rem;">
    l={l_interval:.1f}: S_vac = <span style="color:{_GOLD};">{S_rt_vac:.4f} k_B</span> &nbsp;·&nbsp;
    S_thermal(β={beta_cft}) = <span style="color:{_GOLD};">{S_rt_th:.4f} k_B</span> &nbsp;·&nbsp;
    TFD von Neumann = <span style="color:{_GREEN};">{S_tfd_von_Neumann:.4f} k_B</span> &nbsp;·&nbsp;
    ER bridge 2r_s = <span style="color:{_BLUE};">{2*r_s_er:.3e} m</span>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §20  TAB 8 — COOPER'S SINGULARITY CROSSING
# ══════════════════════════════════════════════════════════════════════════════
def _render_cooper_tab():
    st.markdown(f"""<p style="font-family:monospace;font-size:0.72rem;color:{_DIM};">
    Cooper's journey inside Gargantua: after crossing the event horizon at r = r_s ≈ 2 AU,
    proper time to the classical singularity is τ_max = π GM/c³ ≈ 26 minutes.
    Inside the Tesseract, TARS transmits quantum gravity data with capacity
    bounded by Bekenstein's entropy bound I ≤ 2πRE/ℏc·ln2.
    </p>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        M_coop_msun = st.number_input("Gargantua M [M_sun]",
                                       1e6, 1e10, 1e8, 1e7, format="%.2e", key="qs_M_coop")
        r0_frac     = st.slider("Entry radius r₀/r_s", 0.5, 0.9999, 0.999, 0.0001,
                                 format="%.4f", key="qs_r0_frac")
    with col2:
        E_tars_J    = st.number_input("TARS total energy [J]", 1e6, 1e20, 1e15, format="%.2e",
                                       key="qs_E_tars")
        R_tars_m    = st.number_input("TARS crystal radius [m]", 0.01, 1.0, 0.1, format="%.2f",
                                       key="qs_R_tars")
    with col3:
        y_bulk_lp   = st.slider("Bulk distance y [ℓ_P]", 0.0, 20.0, 5.0, 0.5, key="qs_y_bulk")
        P_signal_W  = st.number_input("Signal power [W]", 1e-30, 1e10, 1e3, format="%.2e",
                                       key="qs_P_signal")

    M_coop_kg = M_coop_msun * M_SUN
    r_s_coop  = 2.0 * G_SI * M_coop_kg / C_SI**2
    r0_m      = r0_frac * r_s_coop
    T_H_coop  = HBAR_SI * C_SI**3 / (8.0 * math.pi * G_SI * M_coop_kg * KB_SI)

    tau_max_s      = CooperCrossingEngine.schwarzschild_interior_proper_time(r0_m, M_coop_kg)
    bekenstein_bits = CooperCrossingEngine.bekenstein_tars_capacity(E_tars_J, R_tars_m)
    fidelity        = CooperCrossingEngine.bulk_transmission_fidelity(y_bulk_lp, M_coop_msun)
    tau_dec_s       = CooperCrossingEngine.quantum_decoherence_time(T_H_coop)
    bandwidth_bps   = CooperCrossingEngine.murphy_signal_bandwidth(P_signal_W, T_H_coop, 1e6)

    # Cooper's trajectory
    tau_arr, r_arr, curv_arr = CooperCrossingEngine.cooper_radial_trajectory(N_pts=500)
    # Quantum state fidelity
    gamma_dec = 1.0 / max(tau_dec_s, 1e-300)
    F_q, S_ent_q = CooperCrossingEngine.quantum_state_fidelity(tau_arr, gamma_dec * 0.001)

    fig, axes = _make_fig(2, 3, size=(14, 8.5))
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    # ── Cooper radial trajectory r(τ) ─────────────────────────────────────────
    ax1.plot(tau_arr / 60.0, r_arr / r_s_coop, color=_BLUE, lw=1.4)
    ax1.fill_between(tau_arr / 60.0, 0, r_arr / r_s_coop, alpha=0.08, color=_BLUE)
    ax1.axhline(0.0, color=_RED, lw=0.8, ls="--", alpha=0.7, label="Singularity r=0")
    ax1.axhline(1.0, color=_GOLD, lw=0.7, ls=":", alpha=0.5, label="Horizon r=r_s")
    _fig_style(ax1, "COOPER: RADIAL FREEFALL r(τ)", "Proper time τ [min]", "r / r_s")
    ax1.legend(fontsize=5, framealpha=0.3)

    # ── Tidal curvature ───────────────────────────────────────────────────────
    ax2.semilogy(tau_arr / 60.0, curv_arr, color=_ORANGE, lw=1.2)
    ax2.fill_between(tau_arr / 60.0, 1e-30, curv_arr, alpha=0.08, color=_ORANGE)
    ax2.axhline(C_SI**2 / LP**2, color=_RED, lw=0.8, ls="--", alpha=0.7, label="Planck curvature")
    _fig_style(ax2, "TIDAL CURVATURE R_tidal [s⁻²]", "τ [min]", "GM/r³ [s⁻²]")
    ax2.legend(fontsize=5, framealpha=0.3)

    # ── Bekenstein capacity vs crystal radius ──────────────────────────────────
    R_range = np.logspace(-3, 1, 300)
    bits_R  = np.array([CooperCrossingEngine.bekenstein_tars_capacity(E_tars_J, R) for R in R_range])
    ax3.loglog(R_range, bits_R, color=_GREEN, lw=1.3)
    ax3.axvline(R_tars_m, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label=f"R={R_tars_m:.2f} m")
    ax3.axhline(bekenstein_bits, color=_GOLD, lw=0.5, ls="--", alpha=0.5)
    _fig_style(ax3, "BEKENSTEIN CAPACITY vs CRYSTAL RADIUS", "R [m]", "Bits [I ≤ 2πRE/ℏc·ln2]")
    ax3.legend(fontsize=5, framealpha=0.3)

    # ── Bulk fidelity vs y ────────────────────────────────────────────────────
    y_range   = np.linspace(0.0, 30.0, 300)
    fid_range = np.array([CooperCrossingEngine.bulk_transmission_fidelity(y, 1.0) for y in y_range])
    ax4.semilogy(y_range, np.maximum(fid_range, 1e-14), color=_PURPLE, lw=1.3)
    ax4.axvline(y_bulk_lp, color=_GOLD, lw=0.8, ls="--", alpha=0.7, label=f"y={y_bulk_lp} ℓ_P")
    ax4.axhline(fidelity, color=_GOLD, lw=0.5, ls="--", alpha=0.5)
    _fig_style(ax4, "BULK TRANSMISSION FIDELITY |T|²", "Bulk distance y [ℓ_P]", "|T|²")
    ax4.legend(fontsize=5, framealpha=0.3)

    # ── Quantum state fidelity ────────────────────────────────────────────────
    ax5.plot(tau_arr / 60.0, F_q, color=_CYAN, lw=1.2, label="|F|² (purity)")
    ax5.plot(tau_arr / 60.0, S_ent_q / max(S_ent_q.max(), 1.0), color=_PINK, lw=1.0, ls="--",
             label="S_ent [normalised]")
    ax5.axhline(0.0, color=_DIM, lw=0.5, ls=":")
    _fig_style(ax5, "COOPER QUANTUM STATE INSIDE TESSERACT", "τ [min]", "Fidelity / S_ent [norm]")
    ax5.legend(fontsize=5, framealpha=0.3)
    ax5.set_ylim(-0.05, 1.1)

    # ── Murphy signal bandwidth ───────────────────────────────────────────────
    P_range_W = np.logspace(-30, 10, 300)
    bw_range  = np.array([CooperCrossingEngine.murphy_signal_bandwidth(P, T_H_coop, 1e6)
                           for P in P_range_W])
    ax6.loglog(P_range_W, bw_range, color=_GOLD, lw=1.3)
    ax6.axvline(P_signal_W, color=_CYAN, lw=0.8, ls="--", alpha=0.7,
                label=f"P={P_signal_W:.1e} W → {bandwidth_bps:.2e} bps")
    _fig_style(ax6, "MURPHY SIGNAL CHANNEL CAPACITY", "P_signal [W]", "C [bits/s]")
    ax6.legend(fontsize=5, framealpha=0.3)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Summary dashboard
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.markdown(f"""<div style="background:{_BG2};border:1px solid rgba(79,195,247,0.2);
        border-radius:4px;padding:0.6rem;font-family:monospace;text-align:center;">
        <div style="color:{_DIM};font-size:0.58rem;">PROPER TIME TO SINGULARITY</div>
        <div style="color:{_BLUE};font-size:1.05rem;font-weight:600;">{tau_max_s/60.0:.2f} min</div>
        <div style="color:{_DIM};font-size:0.52rem;">from r₀={r0_frac:.4f}·r_s</div></div>""",
        unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""<div style="background:{_BG2};border:1px solid rgba(129,199,132,0.2);
        border-radius:4px;padding:0.6rem;font-family:monospace;text-align:center;">
        <div style="color:{_DIM};font-size:0.58rem;">TARS DATA CAPACITY</div>
        <div style="color:{_GREEN};font-size:1.05rem;font-weight:600;">{bekenstein_bits:.3e}</div>
        <div style="color:{_DIM};font-size:0.52rem;">bits (Bekenstein bound)</div></div>""",
        unsafe_allow_html=True)
    with col_s3:
        st.markdown(f"""<div style="background:{_BG2};border:1px solid rgba(128,96,255,0.2);
        border-radius:4px;padding:0.6rem;font-family:monospace;text-align:center;">
        <div style="color:{_DIM};font-size:0.58rem;">BULK FIDELITY |T|²</div>
        <div style="color:{_PURPLE};font-size:1.05rem;font-weight:600;">{fidelity:.4f}</div>
        <div style="color:{_DIM};font-size:0.52rem;">at y={y_bulk_lp:.1f} ℓ_P</div></div>""",
        unsafe_allow_html=True)
    with col_s4:
        st.markdown(f"""<div style="background:{_BG2};border:1px solid rgba(232,196,106,0.2);
        border-radius:4px;padding:0.6rem;font-family:monospace;text-align:center;">
        <div style="color:{_DIM};font-size:0.58rem;">MURPHY BANDWIDTH</div>
        <div style="color:{_GOLD};font-size:1.05rem;font-weight:600;">{bandwidth_bps:.3e} bps</div>
        <div style="color:{_DIM};font-size:0.52rem;">Shannon, Δν=1 MHz</div></div>""",
        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §21  OVERVIEW METRICS BANNER
# ══════════════════════════════════════════════════════════════════════════════
def _render_qs_overview():
    """Top-of-page module summary with key Gargantua quantum observables."""
    tau_max = CooperCrossingEngine.schwarzschild_interior_proper_time(
        0.9999 * GARG_RS_M, GARG_MASS_KG
    )
    lambda_L_garg = QuantumChaosEngine.bh_lyapunov(GARG_MASS_KG)
    S_bh_garg = 4.0 * math.pi * (GARG_MASS_KG / MP)**2
    t_scr_garg_yr = math.log(max(S_bh_garg, 2.0)) / lambda_L_garg / 3.156e7
    bekenstein_tars = CooperCrossingEngine.bekenstein_tars_capacity(1e15, 0.1)
    unruh_garg_horizon = UnruhVacuumEngine.unruh_temperature(C_SI**2 / GARG_RS_M)

    st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;margin-bottom:0.8rem;">
  <div style="background:linear-gradient(135deg,rgba(128,96,255,0.12),rgba(4,6,12,0.9));
    border:1px solid rgba(128,96,255,0.25);border-radius:4px;padding:0.6rem;
    font-family:monospace;text-align:center;">
    <div style="color:{_DIM};font-size:0.56rem;">GARGANTUA S_BH</div>
    <div style="color:{_PURPLE};font-size:0.95rem;font-weight:600;">{S_bh_garg:.3e}</div>
    <div style="color:{_DIM};font-size:0.52rem;">Bekenstein-Hawking entropy</div>
  </div>
  <div style="background:linear-gradient(135deg,rgba(79,195,247,0.12),rgba(4,6,12,0.9));
    border:1px solid rgba(79,195,247,0.25);border-radius:4px;padding:0.6rem;
    font-family:monospace;text-align:center;">
    <div style="color:{_DIM};font-size:0.56rem;">QUANTUM SCRAMBLING TIME</div>
    <div style="color:{_BLUE};font-size:0.95rem;font-weight:600;">{t_scr_garg_yr:.3e} yr</div>
    <div style="color:{_DIM};font-size:0.52rem;">t_scr = ln(S)/λ_L</div>
  </div>
  <div style="background:linear-gradient(135deg,rgba(232,196,106,0.12),rgba(4,6,12,0.9));
    border:1px solid rgba(232,196,106,0.25);border-radius:4px;padding:0.6rem;
    font-family:monospace;text-align:center;">
    <div style="color:{_DIM};font-size:0.56rem;">INTERIOR PROPER TIME</div>
    <div style="color:{_GOLD};font-size:0.95rem;font-weight:600;">{tau_max/60.0:.2f} min</div>
    <div style="color:{_DIM};font-size:0.52rem;">r=0.9999r_s → singularity</div>
  </div>
  <div style="background:linear-gradient(135deg,rgba(129,199,132,0.12),rgba(4,6,12,0.9));
    border:1px solid rgba(129,199,132,0.25);border-radius:4px;padding:0.6rem;
    font-family:monospace;text-align:center;">
    <div style="color:{_DIM};font-size:0.56rem;">UNRUH T @ HORIZON</div>
    <div style="color:{_GREEN};font-size:0.95rem;font-weight:600;">{unruh_garg_horizon:.3e} K</div>
    <div style="color:{_DIM};font-size:0.52rem;">a = c²/r_s at horizon</div>
  </div>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;margin-bottom:1rem;">
  <div style="background:{_BG2};border:1px solid rgba(255,136,0,0.2);border-radius:4px;
    padding:0.5rem;font-family:monospace;text-align:center;">
    <div style="color:{_DIM};font-size:0.56rem;">PLANCK LENGTH</div>
    <div style="color:{_ORANGE};font-size:0.88rem;font-weight:600;">1.616×10⁻³⁵ m</div>
  </div>
  <div style="background:{_BG2};border:1px solid rgba(128,96,255,0.15);border-radius:4px;
    padding:0.5rem;font-family:monospace;text-align:center;">
    <div style="color:{_DIM};font-size:0.56rem;">LQG AREA GAP Δ_A</div>
    <div style="color:{_PURPLE};font-size:0.88rem;font-weight:600;">{A_MIN_LQG:.3e} m²</div>
  </div>
  <div style="background:{_BG2};border:1px solid rgba(79,195,247,0.15);border-radius:4px;
    padding:0.5rem;font-family:monospace;text-align:center;">
    <div style="color:{_DIM};font-size:0.56rem;">LQC BOUNCE DENSITY</div>
    <div style="color:{_BLUE};font-size:0.88rem;font-weight:600;">0.41 ρ_Planck</div>
  </div>
  <div style="background:{_BG2};border:1px solid rgba(129,199,132,0.15);border-radius:4px;
    padding:0.5rem;font-family:monospace;text-align:center;">
    <div style="color:{_DIM};font-size:0.56rem;">MSS CHAOS BOUND</div>
    <div style="color:{_GREEN};font-size:0.88rem;font-weight:600;">λ_L ≤ 2πkT/ℏ</div>
  </div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §22  MAIN PAGE ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
def quantum_singularity_page():
    """
    Quantum Singularity Lab — 8th backend for INTERSTELLAR science platform.
    Renders 8 tabs covering: Planck foam, LQG, BKL/Kasner, Page curve,
    Unruh/vacuum, quantum chaos/SYK, holography/ER=EPR, Cooper's crossing.
    """
    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="border-left:3px solid {_PURPLE};padding-left:1rem;margin-bottom:0.8rem;">
  <div style="font-family:'Rajdhani',sans-serif;font-size:1.65rem;font-weight:700;
              color:{_PURPLE};letter-spacing:0.08em;">QUANTUM SINGULARITY LAB</div>
  <div style="font-family:monospace;font-size:0.65rem;color:{_DIM};margin-top:0.15rem;">
    Planck Scale · Loop Quantum Gravity · BKL Oscillations · Page Curve ·
    Unruh Effect · Quantum Chaos · Holography · Cooper's Interior Crossing
  </div>
  <div style="font-family:monospace;font-size:0.60rem;color:rgba(128,96,255,0.45);margin-top:0.25rem;">
    "The singularity is not the end — it is where the old rules shatter."  — Cooper, 2067
  </div>
</div>""", unsafe_allow_html=True)

    # ── Overview metrics ──────────────────────────────────────────────────────
    _render_qs_overview()

    # ── Eight scientific tabs ─────────────────────────────────────────────────
    tab_labels = [
        "⚛  PLANCK FOAM",
        "◉  LOOP QG",
        "⟁  BKL SINGULARITY",
        "∿  PAGE CURVE",
        "∅  UNRUH / VACUUM",
        "χ  QUANTUM CHAOS",
        "∞  HOLOGRAPHY",
        "◈  COOPER CROSSING",
    ]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        _render_planck_foam_tab()

    with tabs[1]:
        _render_lqg_tab()

    with tabs[2]:
        _render_bkl_tab()

    with tabs[3]:
        _render_page_curve_tab()

    with tabs[4]:
        _render_unruh_tab()

    with tabs[5]:
        _render_chaos_tab()

    with tabs[6]:
        _render_holography_tab()

    with tabs[7]:
        _render_cooper_tab()

    # ── References footer ─────────────────────────────────────────────────────
    with st.expander("◈ Scientific References & Equations"):
        st.markdown(f"""
<div style="font-family:monospace;font-size:0.62rem;color:{_DIM};
     columns:2;column-gap:2rem;line-height:1.7;">
<b style="color:{_PURPLE};">PLANCK SCALE:</b><br>
ℓ_P = √(ħG/c³) = 1.616×10⁻³⁵ m &nbsp;·&nbsp; t_P = ℓ_P/c = 5.391×10⁻⁴⁴ s<br>
m_P = √(ħc/G) = 2.176×10⁻⁸ kg &nbsp;·&nbsp; T_P = E_P/k_B = 1.417×10³² K<br>
Δ_A = 4√3π γ ℓ_P² (LQG minimum area gap, γ = 0.2375)<br>
Virtual BH rate: Γ ~ m_P⁻² exp(−4πM²/m_P²) per Planck 4-vol [1]<br><br>

<b style="color:{_BLUE};">LOOP QUANTUM GRAVITY:</b><br>
Area spectrum: A(j) = 8πγℓ_P² √(j(j+1)) [2,3]<br>
LQC Friedmann: H² = (8πG/3)ρ(1−ρ/ρ_crit) [4,5]<br>
ρ_crit ≈ 0.41 ρ_P — quantum bounce replaces Big Bang [5]<br>
Wheeler-DeWitt: −∂²Ψ/∂α² + V(α)Ψ = 0, α=ln(a)<br><br>

<b style="color:{_GOLD};">BKL SINGULARITY:</b><br>
Kasner: Σp_i=1, Σp_i²=1; u-param: p_1=−u/(1+u+u²) [6]<br>
BKL map: u→u−1 (u>2) or 1/(u−1) (1<u<2) [6,7]<br>
Mixmaster: chaotic sequence of Kasner epochs → singularity [7]<br><br>

<b style="color:{_GREEN};">PAGE CURVE & ISLAND:</b><br>
S_BH = 4πM², t_evap = 5120πM³ [Planck units]<br>
t_Page ≈ t_evap/2; t_scr = (M/2π) ln(S_BH) [9,13]<br>
Island rule: S_gen = S_rad + A_island/4G [11,12]<br><br>

<b style="color:{_ORANGE};">UNRUH & VACUUM:</b><br>
T_U = ħa/(2πck_B) [16] &nbsp;·&nbsp; P_Cas = −π²ħc/(240d⁴) [17]<br>
Schwinger: Γ/V ∝ E² exp(−πE_crit/E), E_crit=m_e²c³/(eħ) [18]<br><br>

<b style="color:{_CYAN};">QUANTUM CHAOS:</b><br>
MSS bound: λ_L ≤ 2πk_BT/ħ; BH saturates [13]<br>
SYK density: ρ(E)=(1/2π)√(4J̃²−E²)/J̃² [large q] [14,15]<br>
OTOC: F(t) ≈ 1−(1/N)exp(λ_L t), t<t_scr [13]<br><br>

<b style="color:{_PINK};">HOLOGRAPHY & ER=EPR:</b><br>
RT: S_EE = Area(γ_A)/(4G) [19]<br>
2D CFT: S = (c/3)ln[(β/π)sinh(πl/β)/ε]<br>
ER=EPR: entangled BH pair ↔ Einstein-Rosen bridge [20]<br><br>

<b style="color:{_PURPLE};">COOPER CROSSING:</b><br>
Cycloid: r=(r_s/2)(1+cosη), τ=(r_s/2c)(η+sinη)<br>
τ_max = (r_s/2c)(π−η₀+sinη₀) to singularity<br>
Bekenstein: I ≤ 2πRE/(ħc·ln2) [8]<br>
Bulk: |T|² = exp(−2ky), k=1/ℓ_AdS [Randall-Sundrum]
</div>""", unsafe_allow_html=True)
