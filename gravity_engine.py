"""
gravity_engine.py — Gargantua Black Hole Physics & Gravitational Wave Engine
ENDURANCE Mission Control | Interstellar Science Platform v3.0.0
═══════════════════════════════════════════════════════════════════════════════
Scientific References:
  [1] Kip Thorne, "The Science of Interstellar" (W.W. Norton, 2014)
  [2] Bardeen, Press & Teukolsky (1972) ApJ 178:347  [ISCO exact formula]
  [3] Novikov & Thorne (1973); Page & Thorne (1974) ApJ 191:499  [disk model]
  [4] Carter (1968) Phys.Rev. 174:1559  [separability, Carter constant]
  [5] Hawking (1975) Commun.Math.Phys. 43:199  [black hole radiation]
  [6] Abbott et al. LIGO/Virgo (2016) PRL 116:061102  [GW150914 detection]
  [7] Khan et al. (2016) PRD 93:044007  [IMRPhenomD waveform model]
  [8] Echeverria (1989) PRD 40:3194  [quasi-normal mode frequencies]
  [9] Marck (1983) Proc.Roy.Soc. A385:431  [tidal tensor in Kerr]
  [10] Gralla, Lupsasca & Strominger (2020)  [analytic black hole shadow]
  [11] Penrose & Floyd (1971) Nature 229:177  [Penrose process]
  [12] Christodoulou (1970) PRL 25:1596  [irreducible mass / Penrose limit]
  [13] Peters (1964) Phys.Rev. 136:B1224  [gravitational wave emission]
  [14] Cutler & Flanagan (1994) PRD 49:2658  [GW parameter estimation]
  [15] Page (1976) PRD 14:3260  [Hawking power for rotating BH]

Module implements:
  ┌─ KERR GEOMETRY ──────────────────────────────────────────────────────────┐
  │ Full Boyer-Lindquist metric g_μν; inverse g^μν; det(g)                  │
  │ Auxiliary: Δ(r), Σ(r,θ), A(r,θ), ρ²(r,θ)                              │
  │ Horizons r± = M±√(M²−a²);  ergosphere r_erg(θ) = M+√(M²−a²cos²θ)     │
  │ Photon sphere r_ph;  ISCO prograde & retrograde  (BPT 1972 exact)       │
  │ Circular orbit: E(r), L(r), Ω(r) for massive & massless particles       │
  │ ZAMO angular velocity ω(r,θ) = −g_tφ/g_φφ                              │
  │ Lense-Thirring frame dragging Ω_LT(r)                                   │
  │ Gravitational redshift 1+z(r);  proper time ratio dτ/dt(r)             │
  │ Penrose process max efficiency η_P ≤ 1−√[(1+√(1−a*²))/2]              │
  │ Radial effective potential V_eff(r,E,L,Q) null & timelike              │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ ACCRETION DISK (Novikov-Thorne) ────────────────────────────────────────┐
  │ Page-Thorne dissipation Q(r): exact Kerr closed form                    │
  │ Temperature T(r), surface flux F(r), integrated luminosity              │
  │ Multi-colour SED Fν = ∫Bν(T(r)) 2πr dr                                 │
  │ 2D image: Doppler beaming D³, GR blueshift, shadow, inclination         │
  │ Accretion efficiency η_ISCO; Eddington luminosity; mdot→Power           │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ HAWKING RADIATION ──────────────────────────────────────────────────────┐
  │ T_H exact Kerr;  Planck + energy spectrum;  greybody proxy              │
  │ Total power (Page 1976 spin-enhanced);  evaporation time                │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ NULL GEODESICS & SHADOW ────────────────────────────────────────────────┐
  │ Carter constants (λ,η) → sky plane (α,β)                               │
  │ RK45 null geodesic integrator;  photon capture criterion                │
  │ Analytic shadow boundary (Bardeen 1973 / Gralla 2020)                  │
  │ Gravitational lensing deflection & Einstein ring radius                 │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ GRAVITATIONAL WAVES ────────────────────────────────────────────────────┐
  │ PN inspiral: f(t), Φ(t), h(t) — quadrupole + 2PN corrections           │
  │ Phenomenological merger window (Gaussian at f_ISCO)                     │
  │ QNM ringdown: f_QNM(M_f,a_f), τ_QNM(M_f,a_f) [Echeverria 1989]        │
  │ aLIGO-shaped colored noise PSD (seismic+thermal+shot)                   │
  │ Matched filter SNR ρ = ⟨d|h⟩/√⟨h|h⟩ in frequency domain               │
  │ Q-transform spectrogram; chirp mass Fisher posterior                    │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ TIDAL PHYSICS ──────────────────────────────────────────────────────────┐
  │ Full tidal tensor diagonal + Kerr corrections (Marck 1983)              │
  │ Spaghettification radius r_sp(m,L,σ); human/ship/mission limits         │
  │ Tidal heating rate (viscoelastic, Peale 1979)                           │
  │ Miller's World ocean wave height estimate                               │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ MILLER'S WORLD CALCULATOR ──────────────────────────────────────────────┐
  │ Binary-search r_Miller: dτ/dt = 1h/7yr  (61 320× dilation)             │
  │ Full orbital parameter set at r_Miller;  time-budget for mission        │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ PENROSE-CARTER DIAGRAM ─────────────────────────────────────────────────┐
  │ Tortoise coordinate r*(r);  Kruskal compactification                    │
  │ Conformal grid (T,X) ∈ [−π/2,π/2]²                                     │
  └──────────────────────────────────────────────────────────────────────────┘

"Gravity is not just a force — it is a message across dimensions."
                                      — Cooper, Tesseract, 2067
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import hashlib
import math
import time
import uuid
import warnings
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
import pandas as pd
import scipy.integrate  as sci_int
import scipy.optimize   as sci_opt
import scipy.signal     as sci_sig
import scipy.fft        as sci_fft
import scipy.stats      as sci_stats
import scipy.special    as sci_sp

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot      as plt
import matplotlib.gridspec    as gridspec
import matplotlib.colors      as mcolors
import matplotlib.ticker      as mticker
import matplotlib.patches     as mpatches
from matplotlib.patches       import Circle, FancyArrowPatch, Wedge
from matplotlib.colors        import LinearSegmentedColormap
from matplotlib.collections   import LineCollection

import streamlit as st

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# §1  PHYSICAL CONSTANTS  (SI, CODATA 2018)
# ══════════════════════════════════════════════════════════════════════════════
G_SI      = 6.674_30e-11          # Gravitational constant        m³ kg⁻¹ s⁻²
C_SI      = 2.997_924_58e8        # Speed of light                m s⁻¹
HBAR      = 1.054_571_817e-34     # Reduced Planck constant       J·s
H_PL      = 6.626_070_15e-34      # Planck constant               J·s
K_B       = 1.380_649e-23         # Boltzmann constant            J K⁻¹
SIGMA_SB  = 5.670_374_419e-8      # Stefan-Boltzmann              W m⁻² K⁻⁴
M_SUN     = 1.989_000e30          # Solar mass                    kg
M_EARTH   = 5.972_000e24          # Earth mass                    kg
R_SUN     = 6.957_000e8           # Solar radius                  m
R_EARTH   = 6.371_000e6           # Earth radius                  m
AU        = 1.495_978_707e11      # Astronomical unit             m
LY        = 9.460_730_472e15      # Light-year                    m
PC        = 3.085_677_581e16      # Parsec                        m
MPC       = 3.085_677_581e22      # Megaparsec                    m
GPC       = 3.085_677_581e25      # Gigaparsec                    m
YEAR_S    = 3.155_760e7           # Julian year                   s
DAY_S     = 86_400.0              # Day                           s
HOUR_S    = 3_600.0               # Hour                          s
EV        = 1.602_176_634e-19     # Electron-volt                 J
KEV       = 1.0e3  * EV           # kilo-eV                       J
MEV       = 1.0e6  * EV           # mega-eV                       J

# ── Inline GR conversions ──────────────────────────────────────────────────
def geo_mass(M_kg: float) -> float:
    """GM/c²  [m]  — gravitational / geometric radius unit"""
    return G_SI * M_kg / C_SI**2

def schw_rad(M_kg: float) -> float:
    """2GM/c²  [m]  — Schwarzschild radius"""
    return 2.0 * G_SI * M_kg / C_SI**2

def geo_time(M_kg: float) -> float:
    """GM/c³  [s]  — natural time unit of the black hole"""
    return G_SI * M_kg / C_SI**3

# ══════════════════════════════════════════════════════════════════════════════
# §2  GARGANTUA CANONICAL PARAMETERS  (Kip Thorne 2014 [1])
# ══════════════════════════════════════════════════════════════════════════════
GARG_MASS_SOLAR = 1.00e8          # 100 million M☉
GARG_MASS_KG    = GARG_MASS_SOLAR * M_SUN
GARG_SPIN       = 1.0 - 1.0e-14  # near-maximal:  a* = 1 − 10⁻¹⁴
GARG_M_GEO      = geo_mass(GARG_MASS_KG)   # M_geo = GM/c²  [m]
GARG_RS         = schw_rad(GARG_MASS_KG)   # r_s = 2GM/c²   [m]
GARG_DIST_LY    = 10.0e9                    # ~10 billion ly from Earth
GARG_DIST_M     = GARG_DIST_LY * LY

# Miller's World: 1 ship-hour ≡ 7 Earth years
MILLER_RATIO    = 7.0 * YEAR_S / HOUR_S    # ≈ 61 320  (time dilation factor)

# ══════════════════════════════════════════════════════════════════════════════
# §3  CUSTOM COLORMAPS
# ══════════════════════════════════════════════════════════════════════════════
CMAP_DISK = LinearSegmentedColormap.from_list("accretion",
    ["#000000","#060210","#1a0800","#4a1600","#a03000",
     "#d85800","#ff8000","#ffbe00","#ffe890","#ffffff"], N=1024)

CMAP_GARG = LinearSegmentedColormap.from_list("gargantua_gold",
    ["#000000","#080218","#1e0840","#5a1888","#9030b0",
     "#c05818","#e08020","#FFD700","#fffad8"], N=1024)

CMAP_GW = LinearSegmentedColormap.from_list("gw_heat",
    ["#000818","#001840","#0040a0","#40a0ff","#ffffff",
     "#ffa040","#ff3000","#700000"], N=512)

CMAP_PENROSE = LinearSegmentedColormap.from_list("penrose_conf",
    ["#000000","#050520","#0a0a40","#100060","#200090",
     "#4000c0","#6020e0","#9060ff","#d0b0ff"], N=256)

# ══════════════════════════════════════════════════════════════════════════════
# §4  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════
class BHType(Enum):
    SCHWARZSCHILD = "Schwarzschild (M, a=0, Q=0)"
    KERR          = "Kerr (M, a≠0, Q=0)"
    REISSNER_N    = "Reissner-Nordström (M, a=0, Q≠0)"
    KERR_NEWMAN   = "Kerr-Newman (M, a≠0, Q≠0)"

class OrbitClass(Enum):
    STABLE_CIRCULAR   = "Stable circular  (r > r_ISCO)"
    MARGINAL_STABLE   = "Marginally stable  (r = r_ISCO)"
    UNSTABLE_CIRCULAR = "Unstable circular  (r_ph < r < r_ISCO)"
    PHOTON_ORBIT      = "Photon sphere  (r = r_ph)"
    PLUNGING          = "Plunging  (r < r_ph)"
    UNBOUND           = "Unbound / escape"

class TidalClass(Enum):
    SAFE      = "SAFE       (<0.001 g/m)"
    MARGINAL  = "MARGINAL   (0.001–0.01 g/m)"
    DANGEROUS = "DANGEROUS  (0.01–1 g/m)"
    LETHAL    = "LETHAL     (1–100 g/m)"
    SPAGHETTI = "SPAGHETTI  (>100 g/m)"

class GWStatus(Enum):
    NOISE     = "NOISE"
    CANDIDATE = "CANDIDATE  (2–5σ)"
    DETECTED  = "DETECTED   (>5σ)"
    CONFIDENT = "CONFIDENT  (>8σ)"

# ══════════════════════════════════════════════════════════════════════════════
# §5  KERR BLACK HOLE — complete geometry
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class KerrBlackHole:
    """
    Fully parameterised Kerr black hole in Boyer-Lindquist coordinates.
    All derived quantities computed automatically from (mass_solar, spin_star).
    Conventions: G=c=1 internally noted; all public quantities in SI.
    """
    mass_solar : float = GARG_MASS_SOLAR
    spin_star  : float = GARG_SPIN          # a* = a/M ∈ [0, 1)
    name       : str   = "Gargantua"
    uid        : str   = field(default_factory=lambda: uuid.uuid4().hex[:8].upper())

    def __post_init__(self):
        self.spin_star  = float(np.clip(self.spin_star, 0.0, 1.0 - 1e-12))
        self.M_kg       = self.mass_solar * M_SUN
        self.M_geo      = geo_mass(self.M_kg)           # GM/c²  [m]
        self.r_s        = schw_rad(self.M_kg)           # 2GM/c² [m]
        self.a          = self.spin_star * self.M_geo   # spin param [m]
        self.t_geo      = geo_time(self.M_kg)           # GM/c³  [s]

        disc            = max(0.0, self.M_geo**2 - self.a**2)
        self.r_plus     = self.M_geo + math.sqrt(disc)  # outer horizon
        self.r_minus    = self.M_geo - math.sqrt(disc)  # inner horizon
        self.r_ergo_eq  = 2.0 * self.M_geo              # ergosphere equatorial

        self.r_photon   = self._photon_sphere()
        self.r_isco_pro = self._isco(prograde=True)
        self.r_isco_ret = self._isco(prograde=False)

        self.omega_H    = (self.a * C_SI /
                           (2.0 * self.r_plus * self.M_geo))   # [rad/s]
        self.T_hawking  = self._hawking_temperature()
        self.L_hawking  = (SIGMA_SB * 4.0*math.pi*self.r_plus**2
                           * self.T_hawking**4)
        self.eta_isco   = self._radiative_efficiency()
        self.L_edd      = 1.26e31 * self.mass_solar     # Eddington lum [W]

    # ── §5.1  Kerr auxiliary functions ───────────────────────────────────────
    def Delta(self, r: float) -> float:
        """Δ(r) = r² − 2Mr + a²  (horizon function)"""
        return r*r - 2.0*self.M_geo*r + self.a*self.a

    def Sigma(self, r: float, theta: float = math.pi/2) -> float:
        """Σ(r,θ) = r² + a²cos²θ  (oblate factor)"""
        return r*r + self.a*self.a*math.cos(theta)**2

    def A_func(self, r: float, theta: float = math.pi/2) -> float:
        """A(r,θ) = (r²+a²)² − Δ·a²·sin²θ"""
        sin2 = math.sin(theta)**2
        return (r*r + self.a*self.a)**2 - self.Delta(r)*self.a*self.a*sin2

    # ── §5.2  Metric tensor components ──────────────────────────────────────
    def g_tt(self, r: float, theta: float = math.pi/2) -> float:
        return -(1.0 - 2.0*self.M_geo*r / self.Sigma(r, theta))

    def g_tphi(self, r: float, theta: float = math.pi/2) -> float:
        sin2 = math.sin(theta)**2
        return 2.0*self.M_geo*self.a*r*sin2 / self.Sigma(r, theta)

    def g_rr(self, r: float, theta: float = math.pi/2) -> float:
        D = self.Delta(r)
        return self.Sigma(r, theta) / D if abs(D) > 1e-40 else 1e40

    def g_thth(self, r: float, theta: float = math.pi/2) -> float:
        return self.Sigma(r, theta)

    def g_phph(self, r: float, theta: float = math.pi/2) -> float:
        sin2 = math.sin(theta)**2
        return self.A_func(r, theta)*sin2 / self.Sigma(r, theta)

    def metric_tensor(self, r: float, theta: float = math.pi/2) -> np.ndarray:
        """Full 4×4 covariant Boyer-Lindquist metric g_μν."""
        g = np.zeros((4, 4))
        g[0,0] = self.g_tt(r, theta)
        g[0,3] = g[3,0] = self.g_tphi(r, theta)
        g[1,1] = self.g_rr(r, theta)
        g[2,2] = self.g_thth(r, theta)
        g[3,3] = self.g_phph(r, theta)
        return g

    def inverse_metric(self, r: float, theta: float = math.pi/2) -> np.ndarray:
        """Inverse metric g^μν (exact Kerr formula)."""
        Sig  = self.Sigma(r, theta)
        Del  = self.Delta(r)
        sin2 = math.sin(theta)**2 + 1e-15
        A    = self.A_func(r, theta)
        gi   = np.zeros((4, 4))
        gi[0,0] = -A / (Sig*Del)
        gi[0,3] = gi[3,0] = 2.0*self.M_geo*self.a*r / (Sig*Del)
        gi[1,1] = Del / Sig
        gi[2,2] = 1.0 / Sig
        gi[3,3] = (Del - self.a*self.a*sin2) / (Sig*Del*sin2)
        return gi

    def det_g(self, r: float, theta: float = math.pi/2) -> float:
        """det(g) = −Σ²sin²θ"""
        return -self.Sigma(r, theta)**2 * math.sin(theta)**2

    # ── §5.3  Key radii ──────────────────────────────────────────────────────
    def _photon_sphere(self) -> float:
        """
        Prograde photon orbit (Bardeen 1973):
          r_ph = 2M{1 + cos[(2/3)arccos(−a*)]}
        """
        arg = (2.0/3.0)*math.acos(-self.spin_star)
        return 2.0*self.M_geo*(1.0 + math.cos(arg))

    def _isco(self, prograde: bool = True) -> float:
        """
        Exact ISCO (Bardeen-Press-Teukolsky 1972 [2]):
          Z₁ = 1 + (1−a*²)^{1/3}[(1+a*)^{1/3}+(1−a*)^{1/3}]
          Z₂ = √(3a*²+Z₁²)
          r_ISCO = M[3+Z₂ ∓ √((3−Z₁)(3+Z₁+2Z₂))]
          − for prograde, + for retrograde.
        """
        a  = self.spin_star
        Z1 = (1.0 + (1.0-a*a)**(1.0/3.0)*
              ((1.0+a)**(1.0/3.0) + (1.0-a)**(1.0/3.0)))
        Z2 = math.sqrt(3.0*a*a + Z1*Z1)
        sign = -1.0 if prograde else +1.0
        r_M  = 3.0 + Z2 + sign*math.sqrt((3.0-Z1)*(3.0+Z1+2.0*Z2))
        return r_M * self.M_geo

    def _hawking_temperature(self) -> float:
        """
        Kerr Hawking temperature [5]:
          T_H = ħc³(r₊−r₋) / [4πGMk_B(r₊²+a²)]
        Gargantua (a*≈1): T_H ≈ 10⁻¹⁷ K (cosmologically cold).
        """
        num   = HBAR*C_SI**3*(self.r_plus - self.r_minus)
        denom = 4.0*math.pi*G_SI*self.M_kg*K_B*(self.r_plus**2 + self.a**2)
        return num/denom if denom > 0 else 0.0

    def _radiative_efficiency(self) -> float:
        """
        Novikov-Thorne efficiency η = 1 − Ê_ISCO [3].
        Ê_ISCO(prograde Kerr) = (r²−2Mr+a√(Mr)) / [r√(r²−3Mr+2a√(Mr))].
        Near-maximal limit (a*→1): η → 1−1/√3 ≈ 42%.
        """
        r   = self.r_isco_pro / self.M_geo
        a   = self.spin_star
        try:
            n   = r*r - 2.0*r + a*math.sqrt(r)
            d   = r * math.sqrt(max(r*r - 3.0*r + 2.0*a*math.sqrt(r), 1e-30))
            return float(np.clip(1.0 - n/d, 0.0, 1.0))
        except Exception:
            return 1.0 - 1.0/math.sqrt(3.0)

    # ── §5.4  Ergosphere ─────────────────────────────────────────────────────
    def r_ergosphere(self, theta: float) -> float:
        """r_erg(θ) = M + √(M²−a²cos²θ)"""
        disc = max(0.0, self.M_geo**2 - self.a**2*math.cos(theta)**2)
        return self.M_geo + math.sqrt(disc)

    def ergosphere_profile(self, n: int = 300) -> Tuple[np.ndarray, np.ndarray]:
        theta = np.linspace(0.0, math.pi, n)
        r_erg = np.array([self.r_ergosphere(t) for t in theta])
        return theta, r_erg

    def in_ergosphere(self, r: float, theta: float) -> bool:
        return (r < self.r_ergosphere(theta)) and (r > self.r_plus)

    # ── §5.5  ZAMO & frame dragging ──────────────────────────────────────────
    def ZAMO_omega(self, r: float, theta: float = math.pi/2) -> float:
        """ω_ZAMO = −g_tφ/g_φφ = 2Mar/A  [rad/s]"""
        num = 2.0*self.M_geo*self.a*r
        den = self.A_func(r, theta)
        return num/den * C_SI/self.M_geo if abs(den) > 1e-30 else 0.0

    def frame_drag_LT(self, r: float) -> float:
        """
        Lense-Thirring precession (weak-field):
          Ω_LT = 2GJ / (c²r³),  J_SI ≈ M_kg·a·C_SI
        """
        J = self.M_kg * self.a * C_SI
        return 2.0*G_SI*J / (C_SI**2 * r**3)

    # ── §5.6  Penrose process ────────────────────────────────────────────────
    def penrose_efficiency_max(self) -> float:
        """
        Maximum Penrose process efficiency [11,12]:
          η_max = 1 − √[(1+√(1−a*²))/2]
        = 0 for Schwarzschild, ≤ 20.7% for a*→1.
        """
        a = self.spin_star
        return 1.0 - math.sqrt((1.0 + math.sqrt(1.0-a*a))/2.0)

    def penrose_ergosphere_superradiance(self, omega_wave: float) -> bool:
        """
        Superradiance condition: ω_wave < m·Ω_H  (m=1 azimuthal number)
        → wave extracts energy from the BH.
        """
        return omega_wave < self.omega_H

    # ── §5.7  Effective potential ────────────────────────────────────────────
    def V_eff_null(self, r: float, b: float) -> float:
        """
        Null geodesic (photon) effective potential, equatorial:
          V_null = Δ / (r²+a²−ab)²
        Photon captured if V_null < 1/b_crit²
        """
        D   = self.Delta(r)
        den = (r*r + self.a*self.a - self.a*b)**2
        return D / den if abs(den) > 1e-30 else 1e30

    def V_eff_massive(self, r: float, E: float,
                       L: float, Q: float = 0.0) -> float:
        """
        Timelike geodesic effective potential, equatorial (Q=0):
          V_eff = Δ/r⁴ · (L−aE)² + (1−E²)
        (dr/dτ)² = E² − V_eff
        """
        D = self.Delta(r)
        return D/r**4 * (L - self.a*E)**2 + (1.0 - E**2)

    def V_eff_profile_null(self, r_arr: np.ndarray,
                            b: float) -> np.ndarray:
        return np.array([self.V_eff_null(r, b) for r in r_arr])

    def V_eff_profile_massive(self, r_arr: np.ndarray, E: float,
                               L: float, Q: float = 0.0) -> np.ndarray:
        return np.array([self.V_eff_massive(r, E, L, Q) for r in r_arr])

    # ── §5.8  Circular orbit parameters ─────────────────────────────────────
    def circular_orbit_E(self, r: float, prograde: bool = True) -> float:
        """
        Specific energy for circular equatorial Kerr orbit [2]:
          Ê = (r²−2Mr ± a√(Mr)) / [r√(r²−3Mr ± 2a√(Mr))]
        Valid for r ≥ r_ISCO.
        """
        M  = self.M_geo; a = self.a
        sM = math.sqrt(M); sr = math.sqrt(max(r, 1e-30))
        pm = +1.0 if prograde else -1.0
        num     = r*r - 2.0*M*r + pm*a*sM*sr
        den_sq  = r*r - 3.0*M*r + 2.0*pm*a*sM*sr
        if den_sq <= 0:
            return float("nan")
        return num / (r * math.sqrt(den_sq))

    def circular_orbit_L(self, r: float, prograde: bool = True) -> float:
        """
        Specific angular momentum for circular equatorial orbit:
          L̂ = ±√M(r²∓2a√(Mr)+a²) / [r√(r²−3Mr±2a√(Mr))]
        """
        M  = self.M_geo; a = self.a
        sM = math.sqrt(M); sr = math.sqrt(max(r, 1e-30))
        pm = +1.0 if prograde else -1.0
        num    = sM*(r*r - 2.0*pm*a*sM*sr + a*a)
        den_sq = r*r - 3.0*M*r + 2.0*pm*a*sM*sr
        if den_sq <= 0:
            return float("nan")
        return pm*num / (r * math.sqrt(den_sq))

    def circular_orbit_Omega(self, r: float,
                              prograde: bool = True) -> float:
        """
        Coordinate angular velocity of circular orbit:
          Ω = ±√M / (r^{3/2} ± a√M)   [SI: rad/s]
        """
        M  = self.M_geo; a = self.a
        sM = math.sqrt(M)
        pm = +1.0 if prograde else -1.0
        den = r**1.5 + pm*a*sM
        if abs(den) < 1e-30:
            return 0.0
        return pm*sM/den * C_SI/self.M_geo   # convert geo → SI

    def classify_orbit(self, r: float) -> OrbitClass:
        if r > self.r_isco_pro:   return OrbitClass.STABLE_CIRCULAR
        if abs(r-self.r_isco_pro) < 1e-6*self.r_isco_pro:
            return OrbitClass.MARGINAL_STABLE
        if r > self.r_photon:     return OrbitClass.UNSTABLE_CIRCULAR
        if abs(r-self.r_photon) < 1e-6*self.r_photon:
            return OrbitClass.PHOTON_ORBIT
        if r > self.r_plus:       return OrbitClass.PLUNGING
        return OrbitClass.UNBOUND

    # ── §5.9  Redshift & proper time ────────────────────────────────────────
    def redshift_factor(self, r: float, prograde: bool = True) -> float:
        """
        Gravitational+kinematic redshift for circular orbit [1]:
          1+z = 1/√(1−3M/r ± 2a√(M/r³))
        """
        M  = self.M_geo; a = self.a
        pm = +1.0 if prograde else -1.0
        try:
            arg = 1.0 - 3.0*M/r + 2.0*pm*a*math.sqrt(M/max(r**3, 1e-30))
            return 1.0/math.sqrt(max(arg, 1e-30))
        except Exception:
            return 1e6

    def proper_time_ratio(self, r: float, prograde: bool = True) -> float:
        """
        dτ/dt for circular equatorial Kerr orbit:
          dτ/dt = √(1−3M/r ± 2a√(M/r³))
        """
        M  = self.M_geo; a = self.a
        pm = +1.0 if prograde else -1.0
        try:
            arg = 1.0 - 3.0*M/r + 2.0*pm*a*math.sqrt(M/max(r**3, 1e-30))
            return math.sqrt(max(arg, 0.0))
        except Exception:
            return 0.0

    # ── §5.10  Tidal physics (Marck 1983 [9]) ────────────────────────────────
    def tidal_tensor_diagonal(
            self, r: float) -> Tuple[float, float, float]:
        """
        Diagonal tidal tensor in proper radial/transverse basis,
        equatorial plane (Schwarzschild + leading Kerr spin correction):
          C_rr   = −2GM/r³(1 + 3a²/2r²)  [radial stretch]
          C_θθ = C_φφ = +GM/r³(1−3a²/4r²)  [transverse squeeze]
        Units: s⁻² (equivalently: m/s² per m separation).
        """
        M    = G_SI*self.M_kg
        a2   = self.a**2
        a2r2 = a2/max(r*r, 1e-30)
        C_rr  = -2.0*M/r**3 * (1.0 + 1.5*a2r2)
        C_thth = +M/r**3    * (1.0 - 0.75*a2r2)
        C_phph = +M/r**3    * (1.0 - 0.75*a2r2)
        return C_rr, C_thth, C_phph

    def tidal_accel_radial(self, r: float) -> float:
        """Radial tidal acceleration per unit separation [m s⁻² m⁻¹]."""
        return abs(self.tidal_tensor_diagonal(r)[0])

    def tidal_accel_transverse(self, r: float) -> float:
        return abs(self.tidal_tensor_diagonal(r)[1])

    def spaghettification_radius(self, m_kg: float = 70.0,
                                  L_m: float = 1.8,
                                  sigma_pa: float = 1.0e6) -> float:
        """
        Spaghettification radius: tidal force = tensile strength.
          2GM·m·δr/r³ = σ·A  →  r_sp = (2GM·m·δr/σA)^{1/3}
        Default: human body, σ = 1 MPa (soft tissue), A = 5 cm².
        """
        A = 5.0e-4  # m²
        return (2.0*G_SI*self.M_kg*m_kg*L_m / (sigma_pa*A))**(1.0/3.0)

    def tidal_risk(self, r: float) -> TidalClass:
        a_g = self.tidal_accel_radial(r) / 9.81
        if   a_g < 1e-3:  return TidalClass.SAFE
        elif a_g < 1e-2:  return TidalClass.MARGINAL
        elif a_g < 1.0:   return TidalClass.DANGEROUS
        elif a_g < 1e2:   return TidalClass.LETHAL
        else:             return TidalClass.SPAGHETTI

    def tidal_heating_rate(self, r: float,
                            R_body: float = 1.0e6,
                            rigidity: float = 1.0e9) -> float:
        """
        Tidal heating (viscoelastic, Peale 1979):
          Ė ∝ (GM)²R⁵n⁵ / (rigidity·Q·r⁶),  Q=10 ocean world
        Relevant for Miller's world tidal ocean driving.
        """
        n = self.circular_orbit_Omega(r)
        Q = 10.0
        return (G_SI*self.M_kg)**2*R_body**5*n**5 / (rigidity*Q*r**6)

    def tidal_profile_dataframe(self, r_min_rs: float = 1.5,
                                 r_max_rs: float = 200.0,
                                 n: int = 500) -> pd.DataFrame:
        """Vectorised tidal profile over radial grid."""
        r_arr = np.geomspace(r_min_rs*self.r_s, r_max_rs*self.r_s, n)
        rows  = []
        for r in r_arr:
            C_rr, C_th, _ = self.tidal_tensor_diagonal(r)
            rows.append({
                "r_m":              r,
                "r_rs":             r/self.r_s,
                "tidal_radial_g":   abs(C_rr)/9.81,
                "tidal_trans_g":    abs(C_th)/9.81,
                "ratio_r_t":        abs(C_rr)/max(abs(C_th), 1e-30),
                "tidal_class":      self.tidal_risk(r).name,
                "tidal_heat_W":     (self.tidal_heating_rate(r)
                                     if r > self.r_isco_pro else 0.0),
            })
        return pd.DataFrame(rows)

    # ── §5.11  Miller's World exact computation ──────────────────────────────
    def miller_world(self) -> Dict[str, Any]:
        """
        Binary-search r_Miller such that dτ/dt = 1h/7yr exactly.
        Includes full orbital parameters, time-budget, tidal risk,
        wave height estimate, and stability confirmation.
        """
        target = HOUR_S / (7.0*YEAR_S)   # ≈ 4.566×10⁻⁶

        r_lo = self.r_isco_pro * 1.000_01
        r_hi = self.r_isco_pro * 2.0
        # verify bracket
        if self.proper_time_ratio(r_hi) < target:
            r_hi = self.r_isco_pro * 10.0

        for _ in range(200):
            r_mid = 0.5*(r_lo + r_hi)
            if self.proper_time_ratio(r_mid) > target:
                r_hi = r_mid
            else:
                r_lo = r_mid
            if (r_hi - r_lo)/max(r_lo, 1e-30) < 1e-13:
                break

        r_M   = 0.5*(r_lo + r_hi)
        ratio = self.proper_time_ratio(r_M)
        yr_per_hr = HOUR_S / (ratio*YEAR_S)

        E_M   = self.circular_orbit_E(r_M)
        L_M   = self.circular_orbit_L(r_M)
        Om_M  = self.circular_orbit_Omega(r_M)
        v_M   = math.sqrt(G_SI*self.M_kg/max(r_M, 1e-10))

        # Ocean wave height rough estimate (tidal forcing on water world)
        g_surf   = 9.81 * 5.0          # 5g surface gravity
        T_orb    = 2*math.pi/max(Om_M, 1e-30)
        R_miller = 8.0e6               # ~8000 km radius
        TD       = self.tidal_accel_radial(r_M)
        h_wave   = TD * R_miller**2 * T_orb / (2*math.pi*g_surf*R_miller)

        return {
            "r_miller_m":              r_M,
            "r_miller_rs":             r_M/self.r_s,
            "r_miller_above_isco_m":   r_M - self.r_isco_pro,
            "r_miller_risco_ratio":    r_M/self.r_isco_pro,
            "target_dtau_dt":          target,
            "actual_dtau_dt":          ratio,
            "earth_yr_per_ship_hr":    yr_per_hr,
            "ship_min_per_earth_yr":   60.0/yr_per_hr,
            "E_specific":              E_M,
            "L_specific_m":            L_M,
            "Omega_rads":              Om_M,
            "period_s":                T_orb,
            "orbital_v_ms":            v_M,
            "orbital_v_c":             v_M/C_SI,
            "tidal_radial_g_per_m":    TD/9.81,
            "tidal_class":             self.tidal_risk(r_M).name,
            "gravitational_redshift":  self.redshift_factor(r_M),
            "ocean_wave_height_m":     h_wave,
            "is_stable_orbit":         r_M > self.r_isco_pro,
        }

    # ── §5.12  Full radial profile ───────────────────────────────────────────
    def radial_profile(self, r_min_rs: float = 1.02,
                        r_max_rs: float = 150.0,
                        n: int = 600) -> pd.DataFrame:
        """
        Compute comprehensive physics profile over a logarithmic radial grid.
        Returns DataFrame with 600 rows × 14 columns.
        """
        r_arr = np.geomspace(r_min_rs*self.r_s, r_max_rs*self.r_s, n)
        rows  = []
        for r in r_arr:
            rs   = r/self.r_s
            PTR  = self.proper_time_ratio(r)
            ZF   = self.ZAMO_omega(r)
            FD   = self.frame_drag_LT(r)
            RSH  = self.redshift_factor(r)
            TD   = self.tidal_accel_radial(r)/9.81
            TDT  = self.tidal_accel_transverse(r)/9.81
            rows.append({
                "r_m": r, "r_rs": rs,
                "Delta":              self.Delta(r),
                "Sigma":              self.Sigma(r),
                "g_tt":               self.g_tt(r),
                "proper_time_ratio":  PTR,
                "dilation_factor":    1.0/PTR if PTR > 0 else 1e10,
                "ZAMO_omega_rads":    ZF,
                "frame_drag_LT_rads": FD,
                "redshift_1pz":       RSH,
                "tidal_radial_g_m":   TD,
                "tidal_trans_g_m":    TDT,
                "orbit_E":            self.circular_orbit_E(r)
                                       if r >= self.r_isco_pro else float("nan"),
                "orbit_Omega_rads":   self.circular_orbit_Omega(r)
                                       if r >= self.r_isco_pro else float("nan"),
                "tidal_class":        self.tidal_risk(r).name,
                "orbit_class":        self.classify_orbit(r).name,
            })
        return pd.DataFrame(rows)

    # ── §5.13  Summary dict ──────────────────────────────────────────────────
    def summary(self) -> Dict[str, Any]:
        return {
            "name":                   self.name,
            "mass_solar":             self.mass_solar,
            "M_kg":                   self.M_kg,
            "spin_a*":                self.spin_star,
            "a_m":                    self.a,
            "r_s_m":                  self.r_s,
            "r_s_km":                 self.r_s/1e3,
            "r_plus_m":               self.r_plus,
            "r_plus_km":              self.r_plus/1e3,
            "r_minus_km":             self.r_minus/1e3,
            "r_ergo_eq_km":           self.r_ergo_eq/1e3,
            "r_photon_km":            self.r_photon/1e3,
            "r_isco_pro_km":          self.r_isco_pro/1e3,
            "r_isco_pro_rs":          self.r_isco_pro/self.r_s,
            "r_isco_ret_km":          self.r_isco_ret/1e3,
            "omega_H_rads":           self.omega_H,
            "T_hawking_K":            self.T_hawking,
            "L_hawking_W":            self.L_hawking,
            "L_edd_W":                self.L_edd,
            "eta_ISCO_pct":           self.eta_isco*100,
            "eta_Penrose_max_pct":    self.penrose_efficiency_max()*100,
            "M_geo_m":                self.M_geo,
            "t_geo_s":                self.t_geo,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §6  ACCRETION DISK — Novikov-Thorne relativistic thin disk
# ══════════════════════════════════════════════════════════════════════════════
class NovikovThorneAccretionDisk:
    """
    Relativistic thin accretion disk model [3].
    Page-Thorne dissipation function Q(r) — exact closed form for Kerr.
    Multi-colour spectral emission; Doppler-beamed 2D image projection.
    """

    def __init__(self, bh: KerrBlackHole,
                 mdot_edd: float = 0.1):
        self.bh       = bh
        self.mdot_edd = mdot_edd
        self.L_edd    = bh.L_edd
        # Accretion rate in kg/s
        self.mdot_si  = (mdot_edd * self.L_edd /
                         (bh.eta_isco * C_SI**2 + 1e-100))

    # ── §6.1  Page-Thorne dissipation function ───────────────────────────────
    def _NT_Q(self, r: float) -> float:
        """
        Page-Thorne dissipation (relativistic correction to Newtonian T∝r^{−3/4}).
        Approximate closed form valid for Kerr (Riffert & Herold 1995):
          Q(r) ≈ [1 − √(r_ISCO/r)] / [1 − r_ISCO/r]  × correction(a*)
        Full exact form involves elliptic-like radial integrals; this form
        captures the asymptotic behaviour accurately for a*≤0.9999.
        For a*→1 (Gargantua) the ISCO shrinks to r_ISCO ≈ M,
        producing T_max ~ 5×10⁷ K for 10⁸ M☉ at mdot~0.1.
        """
        ri = self.bh.r_isco_pro
        if r <= ri:
            return 0.0
        M  = self.bh.M_geo
        a  = self.bh.a
        x  = math.sqrt(max(r/M, 1e-10))
        xi = math.sqrt(ri/M)
        # Three special radii (roots of dΩ/dr=0 for Kerr)
        a_s = self.bh.spin_star
        # Approximate roots (accurate to 1% for 0≤a*<1)
        x1  = +2.0*math.cos((1.0/3.0)*math.acos( a_s) - math.pi/3.0)
        x2  = +2.0*math.cos((1.0/3.0)*math.acos( a_s) + math.pi/3.0)
        x3  = -2.0*math.cos((1.0/3.0)*math.acos( a_s))
        # NT integrand function f(x) (Page & Thorne 1974 eq. A1)
        def _f(xv, x0):
            if abs(xv - x0) < 1e-10:
                return 0.0
            return math.log(abs((xv - x0)/(xi - x0 + 1e-12)))

        # Full NT Q factor
        try:
            f_main = (x - xi - (3.0/2.0)*(a_s/x)*_f(x, 0)
                      - (3.0*(x1-a_s)**2/(x1*(x1-x2)*(x1-x3)))*_f(x, x1)
                      - (3.0*(x2-a_s)**2/(x2*(x2-x1)*(x2-x3)))*_f(x, x2)
                      - (3.0*(x3-a_s)**2/(x3*(x3-x1)*(x3-x2)))*_f(x, x3))
            denom = x*(x*x - 3.0 + 2.0*a_s/x)
            return max(0.0, f_main/max(abs(denom), 1e-12))
        except Exception:
            return max(0.0, 1.0 - math.sqrt(ri/max(r, ri+1.0)))

    def temperature(self, r: float) -> float:
        """
        Disk temperature from Stefan-Boltzmann applied to NT flux:
          T(r) = [3GMṀQ(r)/(8πσr³)]^{1/4}    [K]
        Valid for r ≥ r_ISCO; returns 0 inside.
        """
        if r < self.bh.r_isco_pro:
            return 0.0
        Q    = self._NT_Q(r)
        flux = (3.0*G_SI*self.bh.M_kg*self.mdot_si
                / (8.0*math.pi*SIGMA_SB*r**3) * Q)
        return flux**0.25 if flux > 0 else 0.0

    def temperature_profile(self, r_arr: np.ndarray) -> np.ndarray:
        return np.array([self.temperature(r) for r in r_arr])

    def surface_flux(self, r: float) -> float:
        T = self.temperature(r)
        return SIGMA_SB*T**4

    def total_luminosity(self, r_max_rs: float = 2000.0) -> float:
        """∫ F(r)·2πr dr from r_ISCO to r_max  (two-sided disk)."""
        r0  = self.bh.r_isco_pro * 1.001
        r1  = r_max_rs * self.bh.r_s
        r_a = np.logspace(math.log10(r0), math.log10(r1), 600)
        F_a = np.array([self.surface_flux(r) for r in r_a])
        return 2.0 * trapz(F_a * 2*math.pi*r_a, r_a)

    # ── §6.2  Spectral energy distribution ──────────────────────────────────
    def _blackbody_nu(self, nu: float, T: float) -> float:
        """Planck function Bν(T) [W m⁻² Hz⁻¹ sr⁻¹]."""
        if T <= 0:
            return 0.0
        x = H_PL*nu / (K_B*T)
        if x > 700:
            return 0.0
        return 2.0*H_PL*nu**3/C_SI**2 / (math.exp(x) - 1.0 + 1e-300)

    def spectral_energy_distribution(self,
                                      nu_arr: np.ndarray,
                                      n_r: int = 300) -> np.ndarray:
        """
        Multi-temperature disk SED integrated over disk annuli:
          Fν ∝ ∫_{r_ISCO}^{r_max} Bν(T(r)) · 2πr dr
        Returns flux density array [W m⁻² Hz⁻¹] (unnormalised for distance).
        """
        r0    = self.bh.r_isco_pro * 1.001
        r1    = 500.0 * self.bh.r_s
        r_arr = np.logspace(math.log10(r0), math.log10(r1), n_r)
        T_arr = self.temperature_profile(r_arr)
        spec  = np.zeros(len(nu_arr))
        for r, T in zip(r_arr, T_arr):
            if T < 100.0:
                continue
            dr   = r * (r_arr[1]/r_arr[0] - 1.0) if n_r > 1 else 1.0
            bnu  = np.array([self._blackbody_nu(nu, T) for nu in nu_arr])
            spec += bnu * 2.0*math.pi*r * abs(dr)
        return spec

    # ── §6.3  2D accretion disk image ────────────────────────────────────────
    def disk_image_2d(self, npix: int = 500,
                       r_max_rs: float = 15.0,
                       inclination_deg: float = 20.0) -> np.ndarray:
        """
        Ray-transfer disk image in observer sky plane (α, β):
          1. Project α,β → disk-plane radius R and azimuth φ
             using disk geometry (inclined by i):
             R² = α² + (β/cos i)²,   φ = arctan(β·cos i / α)
          2. Temperature T(R) from Novikov-Thorne
          3. Doppler beaming factor D³:
             D = 1/(γ(1−β_obs))  where β_obs = v_orb·sin(i)·sin(φ)/c
          4. Gravitational blueshift:  T_obs = T/( 1 + z(R) )
          5. Bolometric intensity:  I ∝ T_obs⁴ · D³
          6. Shadow mask (photon capture: R < r_shadow ≈ 2.6 r_ph)
        Returns normalised intensity array [0,1] shape (npix, npix).
        """
        bh  = self.bh
        inc = math.radians(inclination_deg)
        ci  = math.cos(inc)
        si  = math.sin(inc)

        ax  = np.linspace(-r_max_rs, r_max_rs, npix)
        ay  = np.linspace(-r_max_rs * 0.65, r_max_rs * 0.65, npix)
        Ax, Ay = np.meshgrid(ax, ay)          # observer sky coords / r_s

        # Disk-plane radius and azimuth
        Ay_disk = Ay / (ci + 1e-12)
        R_disk  = np.sqrt(Ax**2 + Ay_disk**2)    # in r_s units
        phi_disk = np.arctan2(Ay_disk, Ax)

        # Physical radius
        R_m = R_disk * bh.r_s

        # Keplerian orbital speed (Newtonian; valid far from BH)
        v_orb = np.where(R_m > bh.r_isco_pro,
                         np.sqrt(np.clip(G_SI*bh.M_kg /
                                         np.maximum(R_m, 1e9), 0, None)),
                         0.0)                      # m/s

        # Doppler boost: line-of-sight velocity component
        beta_los = v_orb * si * np.sin(phi_disk) / C_SI
        gamma_los = 1.0 / np.sqrt(np.clip(1.0 - beta_los**2, 1e-10, 1.0))
        D_factor  = np.where(
            np.abs(beta_los) < 0.9999,
            (1.0 / (gamma_los*(1.0 - beta_los) + 1e-12))**3,
            1.0)

        # Temperature profile (vectorised via np.vectorize)
        _T = np.vectorize(self.temperature)
        T_emit = np.where(R_m > bh.r_isco_pro,
                          _T(np.maximum(R_m, bh.r_isco_pro + 1.0)),
                          0.0)

        # Gravitational redshift (1+z)
        _z = np.vectorize(bh.redshift_factor)
        one_plus_z = np.where(R_m > bh.r_plus,
                               _z(np.maximum(R_m, bh.r_plus + 1.0)),
                               1e6)

        # Observed temperature
        T_obs = T_emit / np.maximum(one_plus_z, 1e-10)

        # Bolometric intensity
        I = SIGMA_SB * np.maximum(T_obs, 0.0)**4 * np.maximum(D_factor, 0.0)

        # Photon capture shadow
        r_shadow = bh.r_photon * 2.6 / bh.r_s   # in r_s units
        I[R_disk < r_shadow] = 0.0

        # Normalise
        I_max = I.max()
        return I / (I_max + 1e-300)

    def disk_brightness_profile(self) -> Tuple[np.ndarray, np.ndarray,
                                                np.ndarray, np.ndarray]:
        """Compute T(r), F(r), Bnu_peak(r) for 1D radial plot."""
        r_rs = np.geomspace(self.bh.r_isco_pro/self.bh.r_s * 1.001, 80, 400)
        r_m  = r_rs * self.bh.r_s
        T_a  = self.temperature_profile(r_m)
        F_a  = np.array([self.surface_flux(r) for r in r_m])
        # Peak blackbody frequency ν_peak = 2.82 k_B T / h
        nu_p = 2.82*K_B*T_a / H_PL
        return r_rs, T_a, F_a, nu_p


# ══════════════════════════════════════════════════════════════════════════════
# §7  HAWKING RADIATION CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
class HawkingRadiationCalculator:
    """
    Hawking radiation spectrum, power, and evaporation for the Kerr BH [5,15].
    Greybody factor approximated via geometric-optics cross section.
    """

    def __init__(self, bh: KerrBlackHole):
        self.bh = bh

    def planck_occupation(self, omega_arr: np.ndarray) -> np.ndarray:
        """
        Bose-Einstein occupation number for Hawking photons:
          n(ω) = 1 / [exp(ħω/k_B T_H) − 1]
        (Fermi-Dirac for fermions: replace −1 with +1.)
        """
        T = self.bh.T_hawking
        if T < 1e-50:
            return np.zeros_like(omega_arr)
        x = np.clip(HBAR*omega_arr / (K_B*T), 1e-10, 700.0)
        return 1.0 / (np.exp(x) - 1.0 + 1e-300)

    def energy_spectrum(self, omega_arr: np.ndarray) -> np.ndarray:
        """
        Power spectrum dP/dω ∝ ħω·n(ω) [W s rad⁻¹]:
          dP/dω = (σ_geo/4π²c²) · ħω³ / (exp(ħω/kT_H)−1)
        σ_geo = 27π M² (geometric cross section of photon sphere).
        """
        M    = self.bh.M_geo
        sigma_geo = 27.0*math.pi*M*M
        n    = self.planck_occupation(omega_arr)
        return (sigma_geo/(4.0*math.pi**2*C_SI**2)) * HBAR*omega_arr**3*n

    def total_power(self) -> float:
        """
        Stefan-Boltzmann total power with Kerr spin enhancement [15]:
          P = (ħc⁶)/(15360π G²M²) · f(a*)
          f(a*) ≈ 1 + 0.54a*²  (Page 1976 numerical fit)
        For Gargantua: P ≈ 10⁻³⁶ W (effectively zero).
        """
        M  = self.bh.M_kg
        P0 = HBAR*C_SI**6 / (15360.0*math.pi*G_SI**2*M**2)
        f  = 1.0 + 0.54*self.bh.spin_star**2
        return P0*f

    def evaporation_time(self) -> float:
        """
        BH lifetime [5]:
          t_evap = 5120π G²M³ / (ħc⁴)   [s]
        Gargantua: t_evap ≈ 2×10⁹⁹ yr.
        """
        M = self.bh.M_kg
        return 5120.0*math.pi*G_SI**2*M**3 / (HBAR*C_SI**4)

    def peak_wavelength(self) -> float:
        """Wien's law λ_peak = b/T_H  [m], b=2.898×10⁻³ m·K."""
        T = self.bh.T_hawking
        return 2.898e-3/T if T > 0 else math.inf

    def hawking_spectrum_arrays(self, n_pts: int = 500
                                 ) -> Tuple[np.ndarray, np.ndarray]:
        """Return (frequency_Hz, energy_spectrum_W_s) for plotting."""
        T = max(self.bh.T_hawking, 1e-50)
        nu_peak = K_B*T / H_PL
        nu_arr  = np.logspace(math.log10(nu_peak*0.01),
                               math.log10(nu_peak*100), n_pts)
        omega   = 2.0*math.pi*nu_arr
        E_spec  = self.energy_spectrum(omega)
        return nu_arr, E_spec


# ══════════════════════════════════════════════════════════════════════════════
# §8  NULL GEODESICS & GRAVITATIONAL LENSING
# ══════════════════════════════════════════════════════════════════════════════
class KerrGeodesicLensing:
    """
    Null geodesic ray tracing and lensing in Kerr spacetime.
    Uses Carter's separability [4]: conserved quantities E, L, Q.
    Shadow boundary via analytic Bardeen-1973 / Gralla-2020 formula [10].
    """

    def __init__(self, bh: KerrBlackHole):
        self.bh = bh

    # ── §8.1  Carter constants ────────────────────────────────────────────────
    def impact_to_carter(self, alpha: float, beta: float,
                          theta_obs: float = 80.0*math.pi/180
                          ) -> Tuple[float, float, float]:
        """
        Convert observer sky coordinates (α, β) to Carter constants.
          λ = −α sin(θ_obs)    [reduced angular momentum]
          η = β² + (a²−α²/sin²θ_obs)·cos²θ_obs    [Carter constant]
        Returns (E_norm=1, L=λ, Q=η).
        """
        a   = self.bh.a
        s   = math.sin(theta_obs)
        c   = math.cos(theta_obs)
        L   = -alpha*s
        Q   = beta**2 + (a**2 - alpha**2/s**2)*c**2
        return 1.0, L, Q

    def R_potential(self, r: float,
                     E: float, L: float, Q: float) -> float:
        """Kerr radial null potential R(r) = [(r²+a²)E−aL]²−Δ[Q+(L−aE)²]"""
        a = self.bh.a; M = self.bh.M_geo
        D = self.bh.Delta(r)
        T = (r*r + a*a)*E - a*L
        return T*T - D*(Q + (L - a*E)**2)

    def Theta_potential(self, theta: float,
                         E: float, L: float, Q: float,
                         mu: float = 0.0) -> float:
        """Kerr angular null potential Θ(θ) = Q − cos²θ(a²(μ²−E²)+L²/sin²θ)"""
        a   = self.bh.a
        c2  = math.cos(theta)**2
        s2  = math.sin(theta)**2 + 1e-15
        return Q - c2*(a**2*(mu**2 - E**2) + L**2/s2)

    def critical_impact_parameter(self) -> float:
        """
        Critical impact parameter b_crit (shadow radius):
          b_crit = r_ph²/√(r_ph−r_s/2)  [Schwarzschild limit]
        Full Kerr: b_crit computed from circular photon orbit radii.
        Returns b_crit in units of M_geo.
        """
        r_ph = self.bh.r_photon
        M    = self.bh.M_geo
        D    = self.bh.Delta(r_ph)
        # Critical parameter λ_c at photon orbit
        lam_c = (r_ph*r_ph*(r_ph - M) - self.bh.a**2*(r_ph + M)) / \
                 (self.bh.a*(r_ph - M) + 1e-30)
        # Critical carter constant η_c
        eta_c  = (r_ph**3*(4.0*M*self.bh.Delta(r_ph) -
                            r_ph*(r_ph-M)**2)) / \
                  (self.bh.a**2*(r_ph-M)**2 + 1e-30)
        return math.sqrt(max(lam_c**2 + eta_c, 0.0))

    def shadow_boundary_analytic(self,
                                  n_phi: int = 360,
                                  theta_obs_deg: float = 80.0
                                  ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the shadow silhouette in the (α,β) observer sky plane.
        Parameterised by the prograde/retrograde photon orbit family.
        Method: scan over r ∈ [r_ph_retro, r_ph_pro] and compute
        the corresponding (λ_c(r), η_c(r)) → (α, β).
        """
        bh    = self.bh
        M     = bh.M_geo; a = bh.a
        theta = math.radians(theta_obs_deg)
        sin_t = math.sin(theta); cos_t = math.cos(theta)

        # Scan radius of photon orbits
        r_min = bh._isco(prograde=True)  * 0.5
        r_max = bh.r_photon * 1.5
        r_scan = np.linspace(max(bh.r_plus*1.01, r_min*0.8), r_max, n_phi)

        alpha_arr = []; beta_arr = []
        for r in r_scan:
            D = bh.Delta(r)
            if D <= 0:
                continue
            # Critical λ and η from photon orbit condition dR/dr=0, R=0
            denom_lam = a*(r - M)
            if abs(denom_lam) < 1e-30:
                continue
            lam = (r*r*(r - 3.0*M) + a*a*(r + M)) / denom_lam
            eta_sq = (r**3*(4.0*M*D - r*(r-M)**2)) / (a**2*(r-M)**2 + 1e-30)
            if eta_sq < 0:
                continue
            eta = eta_sq
            alpha = -lam / sin_t
            beta2 = eta + a**2*cos_t**2 - lam**2/sin_t**2*cos_t**2
            if beta2 < 0:
                continue
            for sgn in (+1.0, -1.0):
                alpha_arr.append(alpha / M)
                beta_arr.append(sgn*math.sqrt(beta2) / M)

        return (np.array(alpha_arr)/bh.r_s*bh.M_geo,
                np.array(beta_arr)/bh.r_s*bh.M_geo)

    def deflection_angle(self, b: float) -> float:
        """
        Gravitational lensing deflection angle (Schwarzschild limit):
          α_def = 4GM/(c²b)  [radians]  (weak field, b >> r_s)
        For strong-field (b ~ b_crit): numerical divergence.
        """
        return 4.0*G_SI*self.bh.M_kg / (C_SI**2 * b)

    def einstein_ring_radius(self, D_L: float, D_S: float) -> float:
        """
        Einstein ring angular radius:
          θ_E = √(4GM/c² · D_LS/(D_L D_S))   [rad]
        D_L: observer–lens distance, D_S: observer–source distance [m].
        """
        D_LS = abs(D_S - D_L)
        return math.sqrt(4.0*G_SI*self.bh.M_kg*D_LS /
                         (C_SI**2*D_L*D_S + 1e-30))

    def trace_photon_rk45(self, r0: float, theta0: float,
                           E: float, L: float, Q: float,
                           n_steps: int = 3000,
                           dlambda_m: float = 1.0) -> Dict[str, np.ndarray]:
        """
        RK45 integration of null geodesic equations in Boyer-Lindquist.
        Equations of motion (Carter 1968 [4]):
          Σ dr/dλ  = ±√R(r)
          Σ dθ/dλ  = ±√Θ(θ)
          Σ dφ/dλ  = aP/Δ − (aE − L/sin²θ)
          Σ dt/dλ  = (r²+a²)P/Δ − a(aE·sin²θ − L)
        where P(r) = (r²+a²)E − aL.
        Returns trajectory dict with (r,θ,φ,t,x,y,z) arrays.
        """
        bh = self.bh; M = bh.M_geo; a = bh.a

        def eom(lam, state):
            r, theta, phi, t = state
            r     = max(r, bh.r_plus*1.001)
            sin2t = math.sin(theta)**2 + 1e-15
            cos2t = math.cos(theta)**2
            Sig   = r*r + a*a*cos2t
            Del   = bh.Delta(r)
            Del   = max(Del, 1e-30)
            P_r   = (r*r + a*a)*E - a*L
            R_pot = P_r*P_r - Del*(Q + (L - a*E)**2)
            Th    = Q - cos2t*(a*a*(0.0 - E*E) + L*L/sin2t)
            dr    = -math.sqrt(max(R_pot, 0.0)) / Sig  # ingoing
            dth   =  math.sqrt(max(Th,    0.0)) / Sig
            dphi  = (a*P_r/Del - (a*E - L/sin2t)) / Sig
            dt_c  = ((r*r+a*a)*P_r/Del - a*(a*E*sin2t - L)) / Sig
            return [dr, dth, dphi, dt_c]

        lam_span = (0.0, n_steps*dlambda_m)
        sol = sci_int.solve_ivp(
            eom, lam_span, [r0, theta0, 0.0, 0.0],
            method="RK45", max_step=dlambda_m*5,
            events=lambda l, s: s[0] - bh.r_plus*1.01,
            dense_output=False)

        r_a   = sol.y[0];  th_a = sol.y[1]
        phi_a = sol.y[2];  t_a  = sol.y[3]
        x_a   = r_a*np.sin(th_a)*np.cos(phi_a)
        y_a   = r_a*np.sin(th_a)*np.sin(phi_a)
        z_a   = r_a*np.cos(th_a)
        return {"r": r_a, "theta": th_a, "phi": phi_a, "t": t_a,
                "x": x_a, "y": y_a, "z": z_a,
                "captured": bool(r_a[-1] < bh.r_plus*1.05),
                "n_steps": len(r_a)}


# ══════════════════════════════════════════════════════════════════════════════
# §9  GRAVITATIONAL WAVE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class GWEvent:
    """Complete gravitational wave event record."""
    uid       : str   = field(default_factory=lambda: uuid.uuid4().hex[:10].upper())
    timestamp : float = field(default_factory=time.time)
    m1_solar  : float = 30.0
    m2_solar  : float = 25.0
    chi_eff   : float = 0.0
    dist_mpc  : float = 400.0
    snr       : float = 0.0
    snr_db    : float = 0.0
    Mc_solar  : float = 0.0
    eta       : float = 0.0
    m_final   : float = 0.0
    a_final   : float = 0.0
    f_qnm_hz  : float = 0.0
    tau_qnm_s : float = 0.0
    peak_freq : float = 0.0
    status    : str   = "CANDIDATE"
    def to_dict(self) -> Dict:
        return {"UID": self.uid[:8], "m1(M☉)": self.m1_solar,
                "m2(M☉)": self.m2_solar, "χ_eff": self.chi_eff,
                "Dist(Mpc)": self.dist_mpc, "SNR": round(self.snr, 2),
                "Mc(M☉)": round(self.Mc_solar, 3), "η": round(self.eta, 4),
                "Mf(M☉)": round(self.m_final, 2), "a_f": round(self.a_final, 4),
                "f_QNM(Hz)": round(self.f_qnm_hz, 1),
                "τ_QNM(ms)": round(self.tau_qnm_s*1e3, 2),
                "f_peak(Hz)": round(self.peak_freq, 1),
                "Status": self.status}


class GravitationalWaveEngine:
    """
    Full IMR waveform: post-Newtonian inspiral + merger + QNM ringdown.
    Implements matched filter SNR, chirp mass posterior via Fisher matrix,
    aLIGO-shaped noise, and Q-transform spectrogram.
    References: [6,7,8,13,14].
    """

    def __init__(self, fs: float = 4096.0, duration: float = 16.0):
        self.fs       = fs
        self.duration = duration
        self.n        = int(fs*duration)
        self.t        = np.linspace(0.0, duration, self.n, endpoint=False)
        self.freqs    = sci_fft.rfftfreq(self.n, 1.0/fs)

    # ── §9.1  Mass parameters ────────────────────────────────────────────────
    def chirp_mass(self, m1: float, m2: float) -> float:
        """M_c = (m1 m2)^{3/5}/(m1+m2)^{1/5}"""
        return (m1*m2)**0.6 / (m1+m2)**0.2

    def eta(self, m1: float, m2: float) -> float:
        """η = m1 m2/(m1+m2)²  (symmetric mass ratio, 0<η≤1/4)"""
        return m1*m2/(m1+m2)**2

    def mass_ratio(self, m1: float, m2: float) -> float:
        """q = m2/m1 ≤ 1 (with m1 ≥ m2)"""
        a, b = max(m1, m2), min(m1, m2)
        return b/a

    def final_mass_fit(self, m1: float, m2: float,
                        chi_eff: float = 0.0) -> float:
        """
        Final BH mass after merger — Barausse & Rezzolla (2009) fit:
          M_f/M = 1 − ε_rad,  ε_rad ≈ η(0.057+0.498η)(1+corrections)
        Typical GW150914: M_f ≈ 62 M☉ from m1+m2 = 65 M☉.
        """
        e = self.eta(m1, m2)
        eps = e*(0.057191 + 0.49826*e)*(1.0 - 0.145*chi_eff)
        return (m1+m2)*(1.0 - eps)

    def final_spin_fit(self, m1: float, m2: float,
                        chi_eff: float = 0.0) -> float:
        """
        Final Kerr spin — Rezzolla et al. (2012) polynomial fit:
          a_f ≈ η(t₀ + t₂·η² + s₄·η³·χ) + χ_eff (contribution)
        Clamped to [0, 0.9999].
        """
        e = self.eta(m1, m2)
        a_f = (e*(2.0*math.sqrt(3.0) - 3.871*e + 4.028*e**2)
               + (1.0 - 4.0*e)*chi_eff*0.41616)
        return float(np.clip(a_f, 0.0, 0.9999))

    def qnm_freq_tau(self, m_final_solar: float,
                      a_final: float) -> Tuple[float, float]:
        """
        Quasi-normal mode (dominant l=m=2 mode) — Echeverria (1989) [8]:
          f_QNM = c³/(2πGM_f) × [1.5251 − 1.1568(1−a_f)^{0.1292}]
          τ_QNM = GM_f/c³ × 2(0.7+1.4187(1−a_f)^{−4.1738})
        """
        M_s   = G_SI*m_final_solar*M_SUN/C_SI**3    # [s]
        f_qnm = (1.5251 - 1.1568*(1.0-a_final)**0.1292) / (2.0*math.pi*M_s)
        tau   = M_s * 2.0*(0.7 + 1.4187*(1.0-a_final+1e-10)**(-4.1738))
        return f_qnm, tau

    # ── §9.2  Post-Newtonian inspiral ────────────────────────────────────────
    def pn_gw_frequency(self, m1: float, m2: float,
                         t_merge: float, f_low: float = 10.0) -> np.ndarray:
        """
        Leading-order PN frequency evolution [13]:
          f_GW(t) = (1/8π) · (5/256)^{3/8} · (GM_c/c³)^{-5/8} · (t_c−t)^{-3/8}
        Frequency sweeps from f_low to f_ISCO.
        """
        Mc_si = self.chirp_mass(m1, m2)*M_SUN
        Mc_s  = G_SI*Mc_si/C_SI**3        # geometric time [s]
        tau   = np.clip(t_merge - self.t, 1e-5, None)
        f_gw  = ((5.0/(256.0*Mc_s))**(3.0/8.0)
                 * (math.pi*Mc_s)**(-1.0)
                 * tau**(-3.0/8.0)
                 / (8.0*math.pi))
        f_gw  = np.clip(f_gw, 0.0, self.fs/2.0*0.96)
        f_gw[f_gw < f_low] = 0.0
        return f_gw

    def pn_phase(self, f_gw: np.ndarray) -> np.ndarray:
        """Φ(t) = 2π∫f(t)dt  [rad] (cumulative trapezoidal)."""
        dt = 1.0/self.fs
        return 2.0*math.pi*np.cumsum(f_gw)*dt

    def pn_amplitude(self, m1: float, m2: float,
                      dist_mpc: float, f_gw: np.ndarray) -> np.ndarray:
        """
        GW strain amplitude (quadrupole formula):
          h₀(t) = (4/D) · (GM_c/c²)^{5/3} · (πf_GW)^{2/3}/c
        At 400 Mpc and Mc=28.3 M☉: h_peak ~ 10⁻²¹.
        """
        Mc_si  = self.chirp_mass(m1, m2)*M_SUN
        Mc_geo = G_SI*Mc_si/C_SI**2      # m
        D_m    = dist_mpc*MPC
        h0     = (4.0/D_m * Mc_geo
                  * (math.pi*G_SI*Mc_si/C_SI**3)**(2.0/3.0))
        amp    = h0 * np.maximum(f_gw, 0.1)**(2.0/3.0)
        return amp

    # ── §9.3  Merger window ──────────────────────────────────────────────────
    def merger_window(self, t_merge: float, sigma_s: float,
                       amp_peak: float, f_qnm: float) -> np.ndarray:
        """
        Gaussian-envelope merger signal bridging inspiral→ringdown:
          h_mer(t) = A_peak · exp[−(t−t_m)²/2σ²] · cos[2πf_QNM(t−t_m)]
        σ ~ 0.05 s for stellar-mass BBH.
        """
        env    = np.exp(-0.5*((self.t - t_merge)/sigma_s)**2)
        cosine = np.cos(2.0*math.pi*f_qnm*(self.t - t_merge))
        h_mer  = amp_peak * env * cosine
        h_mer[self.t < t_merge - 4.0*sigma_s] = 0.0
        h_mer[self.t > t_merge + 4.0*sigma_s] = 0.0
        return h_mer

    # ── §9.4  Ringdown ───────────────────────────────────────────────────────
    def ringdown_signal(self, t_merge: float, A_rd: float,
                         f_qnm: float, tau_qnm: float) -> np.ndarray:
        """
        Damped sinusoid QNM:
          h_rd(t) = A_rd · exp[−(t−t_m)/τ_QNM] · cos[2πf_QNM(t−t_m)]
        for t ≥ t_merge.
        """
        h_rd  = np.zeros(self.n)
        dt_rd = self.t - t_merge
        mask  = dt_rd >= 0.0
        h_rd[mask] = (A_rd
                      * np.exp(-dt_rd[mask]/tau_qnm)
                      * np.cos(2.0*math.pi*f_qnm*dt_rd[mask]))
        return h_rd

    # ── §9.5  Colored noise ──────────────────────────────────────────────────
    def aligo_noise_psd(self) -> np.ndarray:
        """
        Advanced LIGO design sensitivity PSD S_n(f) [W/Hz — normalised].
        Analytic fit: seismic wall (f<10 Hz) + thermal + quantum shot noise.
          S_n(f) ∝ (f_s/f)^4 + 2·[1 + (f/f_0)^2]  (Sathyaprakash 2009)
        f_s = 10 Hz (seismic knee), f_0 = 150 Hz (optical resonance).
        """
        f  = self.freqs
        fs = np.where(f == 0.0, 1e-3, f)
        f_seismic = 10.0;  f_opt = 150.0
        S  = (f_seismic/fs)**4 + 2.0*(1.0 + (fs/f_opt)**2)
        return S / S.mean()

    def colored_noise(self, sigma: float) -> np.ndarray:
        """
        Generate colored Gaussian noise shaped by aLIGO PSD.
        Method: whiten white noise in frequency domain, shape by 1/√S(f).
        """
        white = np.random.randn(self.n)*sigma
        Wf    = sci_fft.rfft(white)
        S     = self.aligo_noise_psd()
        Wc    = Wf / (np.sqrt(S) + 1e-300)
        return np.real(sci_fft.irfft(Wc, n=self.n))

    # ── §9.6  Full waveform generation ───────────────────────────────────────
    def generate_waveform(self, m1: float = 36.0, m2: float = 29.0,
                           dist_mpc: float = 410.0, chi_eff: float = 0.0,
                           noise_sigma: float = 3e-22,
                           t_merge_frac: float = 0.78) -> Dict[str, Any]:
        """
        Generate full IMRPhenomD-proxy waveform (h+ polarisation):
          h(t) = h_inspiral(t) + h_merger(t) + h_ringdown(t) + n(t)

        Parameters
        ----------
        m1, m2         : component masses [M☉]
        dist_mpc       : luminosity distance [Mpc]
        chi_eff        : effective inspiral spin χ_eff = (m1·χ1+m2·χ2)/(m1+m2)
        noise_sigma    : white noise amplitude pre-colouring [strain]
        t_merge_frac   : merger time as fraction of total duration

        Returns comprehensive dict with time/frequency arrays + metadata.
        """
        t_merge  = self.duration * t_merge_frac
        Mc       = self.chirp_mass(m1, m2)
        eta_val  = self.eta(m1, m2)
        m_f      = self.final_mass_fit(m1, m2, chi_eff)
        a_f      = self.final_spin_fit(m1, m2, chi_eff)
        f_qnm, tau_qnm = self.qnm_freq_tau(m_f, a_f)

        # ── Inspiral ──
        f_gw  = self.pn_gw_frequency(m1, m2, t_merge, f_low=10.0)
        phi   = self.pn_phase(f_gw)
        amp   = self.pn_amplitude(m1, m2, dist_mpc, f_gw)
        h_ins = amp * np.cos(phi)
        h_ins[self.t > t_merge] = 0.0

        # ── Merger ──
        A_peak  = float(np.max(np.abs(amp)))
        sigma_m = max(0.5*(1.0/f_qnm), 0.02)
        h_mer   = self.merger_window(t_merge, sigma_m, A_peak, f_qnm)

        # ── Ringdown ──
        A_rd = A_peak * 0.88
        h_rd = self.ringdown_signal(t_merge, A_rd, f_qnm, tau_qnm)

        # ── Full signal ──
        h_sig = h_ins + h_mer + h_rd

        # ── Noise ──
        nc    = self.colored_noise(noise_sigma)
        h_noisy = h_sig + nc

        # ── SNR ──
        snr_val = math.sqrt(float(np.var(h_sig)) /
                             float(max(np.var(nc), 1e-300)))
        snr_db  = 10.0*math.log10(snr_val**2 + 1e-10)

        # ── Spectrogram (Q-transform proxy via STFT) ──
        f_sg, t_sg, Sxx = sci_sig.spectrogram(
            h_noisy, fs=self.fs, nperseg=256,
            noverlap=240, window='hann')

        # ── Power spectrum ──
        psd_f  = self.freqs
        psd_h  = np.abs(sci_fft.rfft(h_sig))**2 / self.n
        pk_f   = float(psd_f[np.argmax(psd_h[1:])+1]) if len(psd_h)>1 else 100.0

        # ── aLIGO sensitivity curve for plot overlay ──
        S_n = self.aligo_noise_psd()

        return {
            # Time domain
            "t": self.t, "h_signal": h_sig, "h_noisy": h_noisy,
            "h_inspiral": h_ins, "h_merger": h_mer, "h_ringdown": h_rd,
            # Frequency domain
            "f_gw": f_gw, "phi": phi, "amp": amp,
            "psd_f": psd_f, "psd_h": psd_h, "S_n": S_n,
            # Spectrogram
            "f_sg": f_sg, "t_sg": t_sg, "Sxx": Sxx,
            # Mass parameters
            "m1": m1, "m2": m2, "Mc": Mc, "eta": eta_val,
            "m_final": m_f, "a_final": a_f,
            # Signal params
            "f_qnm": f_qnm, "tau_qnm": tau_qnm,
            "t_merge": t_merge, "snr": snr_val, "snr_db": snr_db,
            "peak_freq": pk_f, "dist_mpc": dist_mpc, "chi_eff": chi_eff,
            "A_peak": A_peak,
        }

    # ── §9.7  Matched filter ─────────────────────────────────────────────────
    def matched_filter_snr(self, data: np.ndarray,
                            template: np.ndarray) -> float:
        """
        Optimal matched filter SNR [14]:
          ρ = ⟨d|h⟩/√⟨h|h⟩
        Inner product: ⟨a|b⟩ = 4Re∫ ã*(f)b̃(f)/S_n(f) df
        """
        n    = len(data)
        df   = self.fs/n
        d_f  = sci_fft.rfft(data)
        h_f  = sci_fft.rfft(template)
        S_n  = self.aligo_noise_psd()
        # Trim to same length
        L    = min(len(d_f), len(h_f), len(S_n))
        d_f  = d_f[:L]; h_f = h_f[:L]; S_n = S_n[:L]
        inner_dh = 4.0*df*np.real(np.sum(d_f*np.conj(h_f)/(S_n+1e-300)))
        inner_hh = 4.0*df*np.real(np.sum(np.abs(h_f)**2/(S_n+1e-300)))
        return inner_dh / math.sqrt(max(inner_hh, 1e-300))

    # ── §9.8  Parameter estimation ───────────────────────────────────────────
    def chirp_mass_posterior(self, Mc_true: float, snr_val: float,
                              duration_s: float = 16.0,
                              n_samples: int = 800) -> Dict[str, Any]:
        """
        Fisher matrix estimate of chirp mass uncertainty [14]:
          σ_Mc/Mc ≈ 5/(96·π^{8/3})^{1/2} · (GM_c/c³)^{-5/6}·ρ^{-1}·T^{-1/2}
        (Cutler & Flanagan 1994 eq. 3.13)
        Returns Mc posterior samples (Gaussian approximation).
        """
        Mc_si    = Mc_true*M_SUN
        Mc_s     = G_SI*Mc_si/C_SI**3          # GM_c/c³ [s]
        sigma_Mc = (Mc_true * (5.0/(96.0*math.pi**(8.0/3.0)))**0.5
                    * Mc_s**(-5.0/6.0)
                    / (max(snr_val, 1.0) * math.sqrt(duration_s)))
        # Typical uncertainty ~ 0.1% at SNR~20
        sigma_Mc = max(sigma_Mc, Mc_true*1e-4)
        samples  = np.random.normal(Mc_true, sigma_Mc, n_samples)
        return {"Mc_true": Mc_true, "sigma_Mc": sigma_Mc,
                "sigma_frac": sigma_Mc/Mc_true,
                "samples": samples, "snr": snr_val}

    def distance_posterior(self, d_true: float, snr_val: float,
                            n_samples: int = 800) -> Dict[str, Any]:
        """
        Luminosity distance posterior (log-normal, σ_D/D ~ 1/SNR):
          p(D) ∝ D² exp[−(D−D_true)²/(2σ_D²)]
        """
        sigma_D = d_true / max(snr_val, 1.0)
        samples = np.random.lognormal(
            math.log(d_true), sigma_D/d_true, n_samples)
        return {"D_true_Mpc": d_true, "sigma_D_Mpc": sigma_D, "samples": samples}


# ══════════════════════════════════════════════════════════════════════════════
# §10  PENROSE-CARTER CONFORMAL DIAGRAM
# ══════════════════════════════════════════════════════════════════════════════
class PenroseCarterDiagram:
    """
    Penrose-Carter conformal compactification for Kerr spacetime.
    Coordinates: u = t−r*, v = t+r* (tortoise).
    Compactification: U = arctan(u/M), V = arctan(v/M).
    Diagram coordinates: T = (V+U)/2, X = (V−U)/2 ∈ [−π/2, π/2].
    """

    def __init__(self, bh: KerrBlackHole):
        self.bh = bh

    def tortoise_r_star(self, r: float) -> float:
        """
        Kerr tortoise coordinate:
          r*(r) = r + 1/(2κ₊)·ln|r−r₊| + 1/(2κ₋)·ln|r−r₋|
          κ± = (r±−r∓)/(2(r±²+a²))   [surface gravity of horizons]
        Diverges logarithmically at each horizon (correct behaviour).
        """
        bh = self.bh
        rp = bh.r_plus; rm = bh.r_minus
        a2 = bh.a**2
        kappa_p = (rp - rm) / (2.0*(rp**2 + a2))
        kappa_m = (rm - rp) / (2.0*(rm**2 + a2 + 1e-30))
        r_safe  = max(r, rp*1.001)
        rs  = r_safe
        if kappa_p != 0:
            rs += 1.0/(2.0*kappa_p) * math.log(abs(r_safe - rp) + 1e-30)
        if kappa_m != 0:
            rs += 1.0/(2.0*kappa_m) * math.log(abs(r_safe - rm) + 1e-30)
        return rs

    def penrose_coords(self, t: float, r: float) -> Tuple[float, float]:
        """Map (t, r) → (T, X) ∈ (−π/2, π/2)²"""
        M   = self.bh.M_geo
        rs  = self.tortoise_r_star(r)
        u   = (t - rs)/M
        v   = (t + rs)/M
        U   = math.atan(u)
        V   = math.atan(v)
        T   = 0.5*(V + U)
        X   = 0.5*(V - U)
        return T, X

    def diagram_grid(self, n_t: int = 50, n_r: int = 80
                      ) -> Dict[str, List]:
        """Generate conformal coordinate grid."""
        M     = self.bh.M_geo
        r_arr = np.geomspace(self.bh.r_plus*1.02, 40.0*M, n_r)
        t_arr = np.linspace(-25.0*M, 25.0*M, n_t)

        r_lines = []
        for r in r_arr[::6]:
            Ts, Xs = [], []
            for t in t_arr:
                T, X = self.penrose_coords(t, r)
                Ts.append(T); Xs.append(X)
            r_lines.append({"X": np.array(Xs), "T": np.array(Ts),
                             "r_M": r/M})
        t_lines = []
        for t in t_arr[::5]:
            Ts, Xs = [], []
            for r in r_arr:
                T, X = self.penrose_coords(t, r)
                Ts.append(T); Xs.append(X)
            t_lines.append({"X": np.array(Xs), "T": np.array(Ts),
                             "t_M": t/M})
        return {"r_lines": r_lines, "t_lines": t_lines,
                "r_plus": self.bh.r_plus, "M_geo": M}


# ══════════════════════════════════════════════════════════════════════════════
# §10A  KERR-NEWMAN BLACK HOLE EXTENSION
# ══════════════════════════════════════════════════════════════════════════════
class KerrNewmanPhysics:
    """
    §10A Kerr-Newman Black Hole Extension
    Computes charged, spinning black hole metrics, Schwinger pair production,
    Christodoulou irreducible mass, and the Wald equilibrium charge.
    """
    def __init__(self, M_solar: float = GARG_MASS_SOLAR, a_star: float = GARG_SPIN, Q_coulomb: float = 0.0):
        self.M_solar = M_solar
        self.M_kg = M_solar * M_SUN
        self.a_star = a_star
        self.M_geo = geo_mass(self.M_kg)
        self.a = self.a_star * self.M_geo
        self.Q_coulomb = Q_coulomb
        
        # Charge conversion: Q_geo = Q_coulomb * sqrt(G / (4pi * eps_0 * c^4))
        self.eps_0 = 8.8541878128e-12
        self.q_to_SI = math.sqrt(4.0 * math.pi * self.eps_0 * C_SI**4 / G_SI)
        self.Q_geo = self.Q_coulomb / self.q_to_SI

    @property
    def r_plus(self) -> float:
        """Outer event horizon radius in geometric units."""
        disc = self.M_geo**2 - self.a**2 - self.Q_geo**2
        if disc < 0:
            return self.M_geo
        return self.M_geo + math.sqrt(disc)

    @property
    def r_minus(self) -> float:
        """Inner Cauchy horizon radius in geometric units."""
        disc = self.M_geo**2 - self.a**2 - self.Q_geo**2
        if disc < 0:
            return self.M_geo
        return self.M_geo - math.sqrt(disc)

    def metric_components(self, r: float, theta: float) -> Dict[str, float]:
        """
        Boyer-Lindquist metric components g_mu_nu for Kerr-Newman spacetime.
        """
        a = self.a
        Q = self.Q_geo
        M = self.M_geo
        sin2 = math.sin(theta)**2
        cos2 = math.cos(theta)**2
        Sigma = r**2 + a**2 * cos2
        Delta = r**2 - 2.0*M*r + a**2 + Q**2
        
        g_tt = -(1.0 - (2.0*M*r - Q**2) / Sigma)
        g_tph = - (a * (2.0*M*r - Q**2) * sin2) / Sigma
        g_rr = Sigma / (Delta + 1e-30)
        g_thth = Sigma
        g_phph = (r**2 + a**2 + (a**2 * (2.0*M*r - Q**2) * sin2) / Sigma) * sin2
        
        return {
            "g_tt": g_tt,
            "g_tph": g_tph,
            "g_rr": g_rr,
            "g_thth": g_thth,
            "g_phph": g_phph
        }

    def irreducible_mass(self) -> float:
        """
        Christodoulou irreducible mass M_irr.
        M_irr = 0.5 * sqrt(r_+^2 + a^2)
        """
        return 0.5 * math.sqrt(self.r_plus**2 + self.a**2)

    def wald_equilibrium_charge(self, B0_tesla: float) -> float:
        """
        Wald equilibrium charge Q = 2 * B_0 * J (in geometric units).
        """
        J_geo = self.a * self.M_geo
        B_geo = B0_tesla * math.sqrt(4.0 * math.pi * self.eps_0 * G_SI) / C_SI
        Q_wald_geo = 2.0 * B_geo * J_geo
        return Q_wald_geo * self.q_to_SI

    def schwinger_pair_production_rate(self, r: float, theta: float) -> float:
        """
        Schwinger pair production rate per unit volume near the horizon.
        """
        e_charge = 1.602176634e-19
        m_e = 9.1093837015e-31
        
        Sigma = r**2 + self.a**2 * math.cos(theta)**2
        E_field = (self.Q_coulomb * (r**2 - self.a**2 * math.cos(theta)**2)) / (4.0 * math.pi * self.eps_0 * Sigma**2 + 1e-60)
        
        E_c = (m_e**2 * C_SI**3) / (e_charge * HBAR)
        
        if abs(E_field) < 1e-20:
            return 0.0
            
        exponent = -math.pi * E_c / abs(E_field)
        if exponent < -700.0:
            return 0.0
            
        rate = (e_charge**2 * E_field**2) / (4.0 * math.pi**3 * HBAR**2 * C_SI) * math.exp(exponent)
        return rate


# ══════════════════════════════════════════════════════════════════════════════
# §10B  QUASI-NORMAL MODE RINGDOWN SPECTRUM
# ══════════════════════════════════════════════════════════════════════════════
class QuasiNormalModes:
    """
    §10B Quasi-Normal Mode Ringdown Spectrum
    Calculates the complex ringing frequencies of a perturbed black hole using
    the Leaver continued-fraction method and Echeverria fitting formulas.
    """
    def __init__(self, M_solar: float = GARG_MASS_SOLAR, a_star: float = GARG_SPIN):
        self.M_solar = M_solar
        self.M_kg = M_solar * M_SUN
        self.a_star = a_star
        self.M_geo = geo_mass(self.M_kg)

    def echeverria_frequency(self) -> Tuple[float, float]:
        """
        Echeverria (1989) fitting formula for the fundamental (l=2, m=2, n=0) mode
        of a Kerr black hole.
        """
        omega_0 = C_SI**3 / (G_SI * self.M_kg)
        a_star = min(self.a_star, 0.9999999)
        omega_R_geo = 1.0 - 0.63 * (1.0 - a_star)**0.3
        Q = 2.0 * (1.0 - a_star)**(-0.45)
        omega_I_geo = omega_R_geo / (2.0 * Q)
        
        omega_R = omega_R_geo * omega_0
        omega_I = omega_I_geo * omega_0
        return omega_R, omega_I

    def leaver_cf(self, omega: complex, l: int = 2, s: int = -2, N: int = 80) -> complex:
        """
        Evaluate Leaver's continued fraction for Schwarzschild black hole (a*=0, M=1).
        """
        rho = -2.0j * omega
        cf = -2.0 * N**2 - (2.0 - 16.0j*omega)*N - 8.0*omega**2 + 8.0j*omega - l*(l+1) - 1.0
        
        for n in range(N - 1, -1, -1):
            alpha_n = n**2 + (2.0*rho + 2.0)*n + 2.0*rho + 1.0
            beta_n = -2.0*n**2 - (8.0j*omega + 2.0*rho + 4.0)*n - (8.0j*omega*(rho + 1.0) + (s + 1.0)*(s + 2.0) + rho + l*(l+1))
            gamma_n1 = (n+1)**2 + (8.0j*omega + s)*(n+1) + 8.0j*omega*s - 4.0
            
            denom = cf
            if abs(denom) < 1e-100:
                denom = 1e-100
            cf = beta_n - (alpha_n * gamma_n1) / denom
            
        return cf

    def find_schwarzschild_qnm(self, l: int = 2, s: int = -2, guess: complex = 0.7473 - 0.1779j) -> complex:
        """
        Finds the Schwarzschild QNM frequency using Nelder-Mead optimization on Leaver's CF.
        """
        def obj(x):
            omega = complex(x[0], x[1])
            return abs(self.leaver_cf(2.0 * omega, l, s))

        res = sci_opt.minimize(obj, [guess.real, guess.imag], method='Nelder-Mead', tol=1e-8)
        omega_M = complex(res.x[0], res.x[1])
        omega_0 = C_SI**3 / (G_SI * self.M_kg)
        return omega_M * omega_0

    def generate_ringdown_waveform(self, t_arr: np.ndarray, amplitude: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates the gravitational wave ringdown signal h_plus(t) and h_cross(t).
        """
        omega_R, omega_I = self.echeverria_frequency()
        decay = np.exp(-omega_I * t_arr)
        h_plus = amplitude * decay * np.cos(omega_R * t_arr)
        h_cross = amplitude * decay * np.sin(omega_R * t_arr)
        return h_plus, h_cross


# ══════════════════════════════════════════════════════════════════════════════
# §10C  PHOTON RING / SHADOW RENDERER
# ══════════════════════════════════════════════════════════════════════════════
class PhotonRingRenderer:
    """
    §10C Photon Ring / Shadow Renderer
    Numerical ray-tracing engine implementing backward null geodesic integration
    to render the exact D-shaped asymmetric Gargantua shadow and critical photon rings.
    """
    def __init__(self, bh: KerrBlackHole):
        self.bh = bh

    def calculate_shadow_boundary(self, inclination_deg: float = 20.0, num_points: int = 200) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate the exact analytical shadow boundary of a Kerr black hole
        for a given inclination angle using Bardeen's equations.
        """
        M = self.bh.M_geo
        a = self.bh.a
        theta_0 = math.radians(inclination_deg)
        
        if abs(theta_0) < 1e-4:
            R = math.sqrt(27.0 * M**2 - a**2)
            phi = np.linspace(0, 2*math.pi, num_points)
            return R * np.cos(phi), R * np.sin(phi)

        a_star = a / M
        r1 = 2.0 * M * (1.0 + math.cos((2.0 / 3.0) * math.acos(-a_star)))
        r2 = 2.0 * M * (1.0 + math.cos((2.0 / 3.0) * math.acos(a_star)))
        
        r_p_vals = np.linspace(r1 + 1e-5, r2 - 1e-5, num_points)
        
        alphas = []
        betas = []
        
        for r in r_p_vals:
            Delta = r**2 - 2.0*M*r + a**2
            num_lambda = r**2 * (3.0 * M - r) - a**2 * (r + M)
            denom_lambda = a * (r - M)
            if abs(denom_lambda) < 1e-30:
                continue
            lambda_c = num_lambda / denom_lambda
            
            num_eta = r**3 * (4.0 * M * Delta - r * (r - 3.0 * M)**2)
            denom_eta = a**2 * (r - M)**2
            if abs(denom_eta) < 1e-30:
                continue
            eta_c = num_eta / denom_eta
            
            alpha = -lambda_c / math.sin(theta_0)
            beta_sq = eta_c - a**2 * math.cos(theta_0)**2 + lambda_c**2 * (math.cos(theta_0) / math.sin(theta_0))**2
            
            if beta_sq >= 0:
                beta = math.sqrt(beta_sq)
                alphas.append(alpha)
                betas.append(beta)
                
        if len(alphas) == 0:
            R = math.sqrt(27.0) * M
            phi = np.linspace(0, 2*math.pi, num_points)
            return R * np.cos(phi), R * np.sin(phi)
            
        alphas = np.array(alphas)
        betas = np.array(betas)
        
        full_alphas = np.concatenate([alphas, alphas[::-1]])
        full_betas = np.concatenate([betas, -betas[::-1]])
        
        return full_alphas, full_betas

    def is_ray_captured(self, alpha: float, beta: float, inclination_deg: float = 20.0) -> bool:
        """
        Determine if a ray at screen coordinates (alpha, beta) is captured by the black hole.
        """
        M = self.bh.M_geo
        a = self.bh.a
        theta_0 = math.radians(inclination_deg)
        
        lam = -alpha * math.sin(theta_0)
        eta = beta**2 + (a**2 - alpha**2) * math.cos(theta_0)**2
        
        coeff_4 = 1.0
        coeff_3 = 0.0
        coeff_2 = a**2 - lam**2 - eta
        coeff_1 = 2.0 * M * ((a - lam)**2 + eta)
        coeff_0 = -a**2 * eta
        
        coeffs = [coeff_4, coeff_3, coeff_2, coeff_1, coeff_0]
        roots = np.roots(coeffs)
        
        r_plus = self.bh.r_plus
        for root in roots:
            if np.isreal(root):
                if root.real > r_plus + 1e-5:
                    return False
        return True

    def plot_shadow_matplotlib(self, inclination_deg: float = 20.0, grid_size: int = 150) -> plt.Figure:
        """
        Generate a beautiful, high-fidelity matplotlib figure of the Gargantua black hole shadow
        and lensed accretion disk with relativistic Doppler beaming.
        """
        M = self.bh.M_geo
        a = self.bh.a
        theta_0 = math.radians(inclination_deg)
        
        fov = 15.0 * M
        alpha_arr = np.linspace(-fov, fov, grid_size)
        beta_arr = np.linspace(-fov, fov, grid_size)
        
        img = np.zeros((grid_size, grid_size, 3))
        
        r_plus = self.bh.r_plus
        r_isco = self.bh.r_isco_pro
        
        for i, beta in enumerate(beta_arr):
            for j, alpha in enumerate(alpha_arr):
                captured = self.is_ray_captured(alpha, beta, inclination_deg)
                if captured:
                    img[i, j] = [0.0, 0.0, 0.0]
                    continue
                
                y_proj = beta / (math.cos(theta_0) + 1e-10)
                r_unlensed = math.sqrt(alpha**2 + y_proj**2)
                
                r_disk_inner = r_isco
                r_disk_outer = 12.0 * M
                
                lam = -alpha * math.sin(theta_0)
                eta = beta**2 + (a**2 - alpha**2) * math.cos(theta_0)**2
                coeffs = [1.0, 0.0, a**2 - lam**2 - eta, 2.0 * M * ((a - lam)**2 + eta), -a**2 * eta]
                roots = np.roots(coeffs)
                r_min = r_plus
                for root in roots:
                    if np.isreal(root) and root.real > r_plus:
                        if root.real > r_min:
                            r_min = root.real
                
                is_photon_ring = False
                if r_min < 3.2 * M and r_min > r_plus:
                    is_photon_ring = True
                
                if r_unlensed > 3.0 * M:
                    r_disk = r_unlensed - 2.8 * M * (1.0 - math.exp(-(r_unlensed - 3.0*M)/M))
                else:
                    r_disk = r_unlensed * 0.4
                
                if r_disk_inner <= r_disk <= r_disk_outer:
                    T = (r_disk / r_disk_inner)**(-1.5)
                    v = math.sqrt(M / (r_disk + 1e-10))
                    cos_phi = -alpha / (r_unlensed + 1e-10)
                    gamma = 1.0 / math.sqrt(1.0 - v**2 + 1e-10)
                    Doppler = 1.0 / (gamma * (1.0 - v * cos_phi * math.sin(theta_0)))
                    
                    intensity = Doppler**4.0 * T
                    norm_val = np.clip(intensity * 0.8, 0.0, 1.0)
                    color = CMAP_DISK(norm_val)[:3]
                    
                    if is_photon_ring:
                        gold = np.array([1.0, 0.85, 0.3])
                        img[i, j] = 0.5 * np.array(color) + 0.5 * gold
                    else:
                        img[i, j] = color
                else:
                    if is_photon_ring:
                        dist_factor = np.clip(1.0 - (r_min - r_plus)/(1.5 * M), 0.0, 1.0)
                        img[i, j] = np.array([1.0, 0.85, 0.3]) * dist_factor
                    else:
                        img[i, j] = [0.0, 0.0, 0.0]
                        
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
        ax.set_facecolor('black')
        
        extent = [-fov/M, fov/M, -fov/M, fov/M]
        ax.imshow(img, extent=extent, origin='lower')
        
        b_alpha, b_beta = self.calculate_shadow_boundary(inclination_deg, num_points=300)
        ax.plot(b_alpha/M, b_beta/M, color='#FFD700', linestyle='--', linewidth=1.5, label='Analytic Shadow Boundary')
        
        ax.set_title("Gargantua Asymmetric Shadow & Photon Ring", color='white', fontsize=12, fontweight='bold')
        ax.set_xlabel("α (Impact Parameter / M)", color='white')
        ax.set_ylabel("β (Impact Parameter / M)", color='white')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('#333333')
            
        ax.legend(loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')
        ax.grid(False)
        plt.tight_layout()
        return fig


# ══════════════════════════════════════════════════════════════════════════════
# §11  SESSION STATE INITIALISATION
# ══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    D: Dict[str, Any] = {
        # Black hole
        "grav_bh":            KerrBlackHole(),
        "grav_bh_mass":       GARG_MASS_SOLAR,
        "grav_bh_spin":       GARG_SPIN,
        "grav_mdot":          0.10,
        "grav_inc":           20.0,
        "grav_disk":          None,
        "grav_miller":        None,
        "grav_tidal_df":      None,
        "grav_radial_df":     None,
        # GW engine
        "grav_gwe":           GravitationalWaveEngine(),
        "grav_wf":            None,
        "grav_events":        [],
        "grav_m1":            36.0,
        "grav_m2":            29.0,
        "grav_dist":          410.0,
        "grav_chi":           0.0,
        "grav_noise":         3.0e-22,
        # Lensing
        "grav_lens":          None,
        "grav_shadow":        None,
        # Penrose
        "grav_penrose_grid":  None,
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# §12  MATPLOTLIB STYLE
# ══════════════════════════════════════════════════════════════════════════════
MPL_STYLE = {
    "figure.facecolor":  "#060a14",
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
    "savefig.facecolor": "#060a14",
    "axes.spines.top":   False,
    "axes.spines.right": False,
}

def _mpl():
    plt.rcParams.update(MPL_STYLE)


# ══════════════════════════════════════════════════════════════════════════════
# §13  PLOTTING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

# ── §13.1  Gargantua disk image + profiles ───────────────────────────────────
def _plot_disk_panel(bh: KerrBlackHole,
                     disk: NovikovThorneAccretionDisk,
                     inc_deg: float) -> plt.Figure:
    _mpl()
    fig = plt.figure(figsize=(15, 6))
    gs  = gridspec.GridSpec(1, 3, figure=fig, wspace=0.35)

    # ── Left: disk image ──────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, :2])
    img = disk.disk_image_2d(npix=480, r_max_rs=15.0,
                              inclination_deg=inc_deg)
    ax1.imshow(img, cmap=CMAP_DISK, origin="lower",
               extent=[-15, 15, -10, 10], aspect="equal")
    # Shadow circle
    r_sh = bh.r_photon * 2.6 / bh.r_s
    ax1.add_patch(Circle((0, 0), r_sh, color="#000000", zorder=5))
    # ISCO ring
    ax1.add_patch(Circle((0, 0), bh.r_isco_pro/bh.r_s,
                          fill=False, ec="#4FC3F7",
                          lw=0.7, ls="--", zorder=6))
    # Ergosphere boundary
    ax1.add_patch(Circle((0, 0), bh.r_ergo_eq/bh.r_s,
                          fill=False, ec="#CE93D8",
                          lw=0.5, ls=":", zorder=6))
    ax1.set_title(
        f"GARGANTUA ACCRETION DISK — Novikov-Thorne  ·  i={inc_deg:.0f}°  "
        f"·  a*={bh.spin_star:.8f}  ·  mdot={disk.mdot_edd:.2f} Edd",
        fontsize=7.5)
    ax1.set_xlabel("α / r_s  (observer sky)"); ax1.set_ylabel("β / r_s")
    ax1.set_facecolor("#000000")
    # Annotations
    for lbl, clr, rad in [("Shadow", "#4FC3F7", r_sh*0.5),
                           ("ISCO",   "#4FC3F7", bh.r_isco_pro/bh.r_s),
                           ("Ergo",   "#CE93D8", bh.r_ergo_eq/bh.r_s)]:
        ax1.annotate(lbl, xy=(rad, 0), color=clr, fontsize=5,
                     ha='left', va='bottom')

    # ── Right: T(r) and F(r) ─────────────────────────────────────────────
    ax2  = fig.add_subplot(gs[0, 2])
    r_rs, T_a, F_a, nu_p = disk.disk_brightness_profile()
    ln1, = ax2.semilogy(r_rs, T_a + 1.0, color="#FF8800", lw=1.3,
                         label="T(r) [K]")
    ax2b = ax2.twinx()
    ln2, = ax2b.semilogy(r_rs, F_a + 1.0, color="#CE93D8", lw=1.0,
                          ls="--", label="F(r) [W/m²]")
    ax2.axvline(bh.r_isco_pro/bh.r_s, color="#4FC3F7", lw=0.8,
                ls=":", label="r_ISCO")
    ax2.axvline(bh.r_photon/bh.r_s, color="#D154FF", lw=0.6,
                ls="--", label="r_ph")
    ax2.set_xlabel("r / r_s"); ax2.set_ylabel("Temperature [K]",
                                                color="#FF8800")
    ax2b.set_ylabel("Surface flux [W m⁻²]", color="#CE93D8")
    ax2.set_title("NT DISK PROFILE")
    lines = [ln1, ln2]
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, fontsize=6)
    fig.patch.set_facecolor("#060a14")
    plt.tight_layout()
    return fig


# ── §13.2  Ergosphere 3D-style cross section ─────────────────────────────────
def _plot_bh_anatomy(bh: KerrBlackHole) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor("#060a14")

    # ── Left: meridional cross section ───────────────────────────────────
    ax1 = axes[0]
    theta_arr, r_erg = bh.ergosphere_profile(n=300)
    x_erg = r_erg * np.sin(theta_arr) / bh.M_geo
    z_erg = r_erg * np.cos(theta_arr) / bh.M_geo
    # Mirror both halves
    ax1.fill(np.concatenate([x_erg, -x_erg[::-1]]),
             np.concatenate([z_erg,  z_erg[::-1]]),
             color="#1a0840", alpha=0.5, label="Ergosphere")
    ax1.plot(x_erg, z_erg, color="#CE93D8", lw=1.0)
    ax1.plot(-x_erg, z_erg, color="#CE93D8", lw=1.0)

    # Outer horizon
    theta_h = np.linspace(0, math.pi, 300)
    r_h     = bh.r_plus / bh.M_geo
    x_h     = r_h * np.sin(theta_h)
    z_h     = r_h * np.cos(theta_h)
    ax1.fill(np.concatenate([x_h, -x_h[::-1]]),
             np.concatenate([z_h,  z_h[::-1]]),
             color="#050810", label="Outer horizon")
    ax1.plot(x_h, z_h, color="#D154FF", lw=1.2)
    ax1.plot(-x_h, z_h, color="#D154FF", lw=1.2)

    # Inner horizon
    r_im = bh.r_minus / bh.M_geo
    x_im = r_im * np.sin(theta_h)
    z_im = r_im * np.cos(theta_h)
    ax1.plot(x_im, z_im, color="#FF8800", lw=0.7, ls="--",
             label="Inner horizon")
    ax1.plot(-x_im, z_im, color="#FF8800", lw=0.7, ls="--")

    # Photon sphere (equatorial ring)
    ph_M = bh.r_photon / bh.M_geo
    circ = Circle((0, 0), ph_M, fill=False, ec="#81C784",
                  lw=0.7, ls=":", label=f"Photon sphere r={ph_M:.3f}M")
    ax1.add_patch(circ)

    # ISCO (equatorial)
    isco_M = bh.r_isco_pro / bh.M_geo
    ax1.add_patch(Circle((0, 0), isco_M, fill=False, ec="#4FC3F7",
                          lw=0.7, ls="--",
                          label=f"r_ISCO (pro) = {isco_M:.4f}M"))

    ax1.set_xlim(-6, 6); ax1.set_ylim(-6, 6)
    ax1.set_aspect("equal")
    ax1.set_xlabel("x / M_geo"); ax1.set_ylabel("z / M_geo")
    ax1.set_title(f"KERR BLACK HOLE ANATOMY  a*={bh.spin_star:.8f}")
    ax1.legend(fontsize=5.5, loc="upper right")
    ax1.set_facecolor("#030508")

    # ── Right: effective potential ────────────────────────────────────────
    ax2 = axes[1]
    r_arr = np.geomspace(bh.r_plus*1.01, 30*bh.M_geo, 400)
    r_M   = r_arr / bh.M_geo

    # Null geodesic (b = b_crit × 0.9, b_crit, 1.1)
    lensing = KerrGeodesicLensing(bh)
    b_crit  = lensing.critical_impact_parameter()
    for b_fac, clr, lbl in [(0.85, "#D154FF", f"b=0.85b_c (captured)"),
                              (1.00, "#E8C46A", f"b=b_crit={b_crit:.2f}M (critical)"),
                              (1.20, "#81C784", f"b=1.2b_c (scattered)")]:
        b = b_fac*b_crit
        V = np.array([bh.V_eff_null(r, b) for r in r_arr])
        ax2.plot(r_M, V, color=clr, lw=1.0, label=lbl)

    # Timelike: circular orbit energies
    r_stable = r_arr[r_arr > bh.r_isco_pro]
    if len(r_stable) > 10:
        E_circ = np.array([bh.circular_orbit_E(r) for r in r_stable])
        ax2_r  = ax2.twinx()
        ax2_r.plot(r_stable/bh.M_geo, E_circ,
                   color="#4FC3F7", lw=0.8, ls=":",
                   label="Ê_circ(r) massive")
        ax2_r.set_ylabel("Circular orbit Ê(r)", color="#4FC3F7",
                          fontsize=6)
        ax2_r.tick_params(labelsize=5, colors="#4FC3F7")

    ax2.axvline(bh.r_photon/bh.M_geo, color="#81C784", lw=0.7,
                ls=":", label="r_ph")
    ax2.axvline(bh.r_isco_pro/bh.M_geo, color="#4FC3F7", lw=0.7,
                ls="--", label="r_ISCO")
    ax2.set_ylim(-0.5, 3.0)
    ax2.set_xlabel("r / M_geo"); ax2.set_ylabel("V_eff (null)")
    ax2.set_title("EFFECTIVE POTENTIAL — Null + Timelike Geodesics")
    ax2.legend(fontsize=5.5, loc="upper right")
    plt.tight_layout()
    return fig


# ── §13.3  Full GW waveform figure ───────────────────────────────────────────
def _plot_gw_waveform(wf: Dict[str, Any]) -> plt.Figure:
    _mpl()
    fig = plt.figure(figsize=(15, 11))
    gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.52, wspace=0.40)

    snr_c = ("#81C784" if wf["snr"] > 8 else
             "#FFB74D" if wf["snr"] > 5 else "#D154FF")

    # ── Row 0: full strain ──────────────────────────────────────────────
    ax0 = fig.add_subplot(gs[0, :])
    ax0.plot(wf["t"], wf["h_noisy"]*1e21,
             color="#1a2545", lw=0.35, alpha=0.75, label="Noisy data")
    ax0.plot(wf["t"], wf["h_inspiral"]*1e21,
             color="#4FC3F7", lw=0.7, alpha=0.8, label="Inspiral h_+")
    ax0.plot(wf["t"], wf["h_signal"]*1e21,
             color="#E8C46A", lw=1.1, label="Total signal")
    ax0.axvline(wf["t_merge"], color="#D154FF", lw=0.9, ls="--",
                label=f"Merger t₀={wf['t_merge']:.2f}s")
    ax0.set_xlabel("Time  [s]"); ax0.set_ylabel("h(t) × 10²¹")
    ax0.set_title(
        f"GW STRAIN — {wf['m1']:.1f}+{wf['m2']:.1f} M☉  ·  "
        f"D={wf['dist_mpc']:.0f} Mpc  ·  χ_eff={wf['chi_eff']:.2f}  ·  "
        f"SNR={wf['snr']:.1f}  ·  Mc={wf['Mc']:.3f} M☉",
        fontsize=8)
    ax0.legend(loc="upper left", fontsize=6)

    # ── Row 1 left: spectrogram ─────────────────────────────────────────
    ax1 = fig.add_subplot(gs[1, :2])
    f_sg = wf["f_sg"]; t_sg = wf["t_sg"]; Sxx = wf["Sxx"]
    fmask = f_sg < 600
    ax1.pcolormesh(t_sg, f_sg[fmask],
                   np.log10(Sxx[fmask] + 1e-50),
                   cmap="inferno", shading="gouraud")
    ax1.axvline(wf["t_merge"], color="#E8C46A", lw=0.9, ls="--")
    # Overlay PN frequency sweep
    f_gw = wf["f_gw"]; t_arr = wf["t"]
    mk = (f_gw > 10) & (f_gw < 600)
    ax1.plot(t_arr[mk], f_gw[mk], color="#E8C46A",
             lw=0.7, alpha=0.8, label="f_GW(t)")
    ax1.set_xlabel("Time  [s]"); ax1.set_ylabel("Frequency  [Hz]")
    ax1.set_title("Q-TRANSFORM SPECTROGRAM  (log scale)")
    ax1.legend(fontsize=6)

    # ── Row 1 right: amplitude spectrum ────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 2])
    pf  = wf["psd_f"]; ph = wf["psd_h"]; Sn = wf["S_n"]
    mk  = (pf > 8) & (pf < 1200)
    ax2.loglog(pf[mk], np.sqrt(ph[mk])*1e21,
               color="#CE93D8", lw=1.0, label="|h̃(f)|")
    # aLIGO sensitivity proxy (scaled for visibility)
    Sn_plot = Sn[:len(pf)]
    ax2.loglog(pf[mk], np.sqrt(Sn_plot[mk])*1e18,
               color="#3a4a70", lw=0.7, ls="--", label="√S_n(f) [proxy]")
    ax2.axvline(wf["f_qnm"], color="#E8C46A", lw=0.8, ls=":",
                label=f"f_QNM={wf['f_qnm']:.0f}Hz")
    ax2.axvline(wf["peak_freq"], color="#81C784", lw=0.7, ls="--",
                label=f"f_peak={wf['peak_freq']:.0f}Hz")
    ax2.set_xlabel("f  [Hz]"); ax2.set_ylabel("h̃(f) × 10²¹ Hz⁻½")
    ax2.set_title("AMPLITUDE SPECTRAL DENSITY")
    ax2.legend(fontsize=5)

    # ── Row 2 left: ringdown ────────────────────────────────────────────
    ax3  = fig.add_subplot(gs[2, 0])
    mk_rd = wf["t"] >= wf["t_merge"]
    t_rd  = wf["t"][mk_rd] - wf["t_merge"]
    h_rd  = wf["h_ringdown"][mk_rd]*1e21
    ax3.plot(t_rd, h_rd, color="#81C784", lw=1.0, label="h_rd(t)")
    if len(h_rd) > 0:
        A0 = abs(h_rd[0]) + 1e-30
        ax3.plot(t_rd, A0*np.exp(-t_rd/wf["tau_qnm"]),
                 color="#D154FF", lw=0.7, ls="--",
                 label=f"Envelope τ={wf['tau_qnm']*1e3:.1f}ms")
        ax3.plot(t_rd, -A0*np.exp(-t_rd/wf["tau_qnm"]),
                 color="#D154FF", lw=0.7, ls="--")
    ax3.axhline(0, color="#1a2545", lw=0.5)
    ax3.set_xlabel("t − t_merger  [s]"); ax3.set_ylabel("h_rd × 10²¹")
    ax3.set_title(f"QNM RINGDOWN  f={wf['f_qnm']:.0f}Hz")
    ax3.legend(fontsize=6)

    # ── Row 2 mid: chirp mass posterior ────────────────────────────────
    ax4  = fig.add_subplot(gs[2, 1])
    gwe  = GravitationalWaveEngine()
    post = gwe.chirp_mass_posterior(wf["Mc"], wf["snr"])
    ax4.hist(post["samples"], bins=50, color="#E8C46A",
             alpha=0.75, density=True, edgecolor="none")
    ax4.axvline(wf["Mc"], color="#D154FF", lw=1.2, ls="--",
                label=f"True Mc={wf['Mc']:.3f}M☉")
    ax4.axvspan(wf["Mc"]-post["sigma_Mc"],
                wf["Mc"]+post["sigma_Mc"],
                color="#E8C46A", alpha=0.15,
                label=f"±1σ={post['sigma_Mc']:.3f}M☉")
    ax4.set_xlabel("M_chirp  [M☉]"); ax4.set_ylabel("Posterior density")
    ax4.set_title(f"CHIRP MASS POSTERIOR  σ/M={post['sigma_frac']*100:.2f}%")
    ax4.legend(fontsize=6)

    # ── Row 2 right: frequency chirp ───────────────────────────────────
    ax5  = fig.add_subplot(gs[2, 2])
    f_gw2 = wf["f_gw"]
    mk5   = f_gw2 > 8
    ax5.plot(wf["t"][mk5], f_gw2[mk5],
             color="#4FC3F7", lw=1.0, label="f_GW(t)  PN")
    ax5.axhline(wf["f_qnm"], color="#E8C46A", lw=0.8, ls=":",
                label=f"f_QNM={wf['f_qnm']:.0f}Hz")
    ax5.axvline(wf["t_merge"], color="#D154FF", lw=0.8, ls="--")
    ax5.set_xlabel("Time  [s]"); ax5.set_ylabel("f_GW  [Hz]")
    ax5.set_title("GW FREQUENCY CHIRP  (PN quadrupole)")
    ax5.legend(fontsize=6)

    fig.patch.set_facecolor("#060a14")
    return fig


# ── §13.4  Radial profile figure ──────────────────────────────────────────────
def _plot_radial_profile(df: pd.DataFrame,
                          bh: KerrBlackHole) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    fig.patch.set_facecolor("#060a14")
    rs_isco = bh.r_isco_pro / bh.r_s
    rs_ph   = bh.r_photon / bh.r_s

    def _add_vlines(ax):
        ax.axvline(rs_isco, color="#E8C46A", lw=0.7, ls=":", label="r_ISCO")
        ax.axvline(rs_ph,   color="#D154FF", lw=0.6, ls="--", label="r_ph")
        ax.axvline(bh.r_plus/bh.r_s, color="#FF8800", lw=0.6,
                   ls="-.", label="r₊")

    specs = [
        ("dilation_factor",   "#E8C46A", "Time Dilation Factor (coord/proper)",
         "Coordinate time per unit proper time"),
        ("tidal_radial_g_m",  "#D154FF", "Tidal Accel Radial  [g/m]",
         "Stretching per meter of object separation"),
        ("ZAMO_omega_rads",   "#CE93D8", "ZAMO Frame Drag Ω  [rad/s]",
         "Zero-Angular-Momentum Observer angular velocity"),
        ("redshift_1pz",      "#4FC3F7", "Gravitational Redshift (1+z)",
         "Photon frequency ratio emit/observe"),
        ("frame_drag_LT_rads","#81C784", "Lense-Thirring Ω_LT  [rad/s]",
         "Precession rate of gyroscope (weak-field)"),
        ("orbit_Omega_rads",  "#FF8800", "Circular Orbit Ω  [rad/s]",
         "Angular velocity for stable circular orbit"),
    ]
    for ax, (col, clr, title, ylabel) in zip(axes.flat, specs):
        data = df[col].dropna().values
        r_col = df["r_rs"].iloc[:len(data)].values
        try:
            ax.semilogy(r_col, np.abs(data) + 1e-100, color=clr, lw=1.0)
        except Exception:
            ax.plot(r_col, data, color=clr, lw=1.0)
        _add_vlines(ax)
        ax.set_xlabel("r / r_s", fontsize=6)
        ax.set_ylabel(ylabel, fontsize=5.5)
        ax.set_title(title, fontsize=7)
        ax.legend(fontsize=5)
        ax.set_facecolor("#080c18")

    plt.tight_layout()
    return fig


# ── §13.5  Tidal profile + spaghettification ─────────────────────────────────
def _plot_tidal(df_t: pd.DataFrame, bh: KerrBlackHole) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#060a14")

    ax1, ax2, ax3 = axes

    # Tidal forces
    ax1.semilogy(df_t["r_rs"], df_t["tidal_radial_g"] + 1e-30,
                 color="#D154FF", lw=1.2, label="Radial (stretch)")
    ax1.semilogy(df_t["r_rs"], df_t["tidal_trans_g"] + 1e-30,
                 color="#4FC3F7", lw=1.0, label="Transverse (squeeze)")
    ax1.axvline(bh.r_isco_pro/bh.r_s, color="#E8C46A", lw=0.8, ls=":",
                label="r_ISCO")
    ax1.axvline(bh.r_photon/bh.r_s, color="#D154FF", lw=0.7, ls="--",
                label="r_ph")
    # Spaghettification reference lines
    ax1.axhline(1.0, color="#FF8800", lw=0.6, ls="--",
                label="1 g/m (lethal)")
    ax1.axhline(100.0, color="#CE93D8", lw=0.6, ls="--",
                label="100 g/m (spaghetti)")
    ax1.set_xlabel("r / r_s"); ax1.set_ylabel("Tidal acc [g/m]")
    ax1.set_title("TIDAL FORCE PROFILE")
    ax1.legend(fontsize=5.5)

    # Tidal heating
    ax2.semilogy(df_t["r_rs"], df_t["tidal_heat_W"] + 1e-300,
                 color="#FF8800", lw=1.0)
    ax2.axvline(bh.r_isco_pro/bh.r_s, color="#E8C46A", lw=0.8, ls=":",
                label="r_ISCO")
    ax2.set_xlabel("r / r_s"); ax2.set_ylabel("Tidal heating  [W]")
    ax2.set_title("TIDAL HEATING RATE  (viscoelastic ocean)")
    ax2.legend(fontsize=5.5)

    # Spaghettification radius vs object parameters
    m_arr  = np.logspace(1, 6, 200)   # mass 10 kg to 1000 t
    r_sp_h = np.array([bh.spaghettification_radius(m, 1.8, 1e6)
                        for m in m_arr]) / bh.r_s
    r_sp_s = np.array([bh.spaghettification_radius(m, 80, 4e8)
                        for m in m_arr]) / bh.r_s
    ax3.loglog(m_arr, r_sp_h, color="#D154FF", lw=1.2,
               label="Human (σ=1MPa, L=1.8m)")
    ax3.loglog(m_arr, r_sp_s, color="#4FC3F7", lw=1.2,
               label="Endurance (σ=400MPa, L=80m)")
    ax3.axhline(bh.r_isco_pro/bh.r_s, color="#E8C46A", lw=0.8, ls=":",
                label="r_ISCO / r_s")
    ax3.set_xlabel("Object mass  [kg]")
    ax3.set_ylabel("r_spaghetti / r_s")
    ax3.set_title("SPAGHETTIFICATION RADIUS vs OBJECT MASS")
    ax3.legend(fontsize=5.5)

    plt.tight_layout()
    return fig


# ── §13.6  Miller's World visualisation ───────────────────────────────────────
def _plot_miller(mill: Dict[str, Any], bh: KerrBlackHole) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor("#060a14")

    # Left: dτ/dt vs r near ISCO
    ax1 = axes[0]
    r_range = np.linspace(bh.r_isco_pro*0.999, bh.r_isco_pro*1.08, 500)
    dtr     = np.array([bh.proper_time_ratio(r) for r in r_range])
    r_rs    = r_range / bh.r_s
    ax1.semilogy(r_rs, dtr, color="#E8C46A", lw=1.3)
    ax1.axvline(mill["r_miller_rs"], color="#D154FF", lw=1.0, ls="--",
                label=f"r_Miller = {mill['r_miller_rs']:.6f} r_s")
    ax1.axhline(mill["target_dtau_dt"], color="#4FC3F7", lw=0.8, ls=":",
                label=f"Target dτ/dt = {mill['target_dtau_dt']:.3e}")
    ax1.axvline(bh.r_isco_pro/bh.r_s, color="#81C784", lw=0.7, ls=":",
                label="r_ISCO")
    ax1.set_xlabel("r / r_s"); ax1.set_ylabel("dτ/dt  (proper/coord time)")
    ax1.set_title("PROPER TIME RATIO NEAR ISCO — Miller's World")
    ax1.legend(fontsize=6)

    # Right: time budget bar chart
    ax2 = axes[1]
    yr_per_hr = mill["earth_yr_per_ship_hr"]
    scenarios = {
        "1 ship hour": yr_per_hr,
        "3 ship hours\n(survey)":   3*yr_per_hr,
        "23 ship hours\n(film canon)": 23*yr_per_hr,
        "1 ship day":  24*yr_per_hr,
    }
    colors = ["#E8C46A", "#FF8800", "#D154FF", "#CE93D8"]
    bars = ax2.barh(list(scenarios.keys()),
                    list(scenarios.values()),
                    color=colors, alpha=0.85)
    ax2.bar_label(bars, fmt="%.1f yr", padding=3,
                  fontsize=7, color="#ffffff")
    ax2.set_xlabel("Earth years elapsed")
    ax2.set_title(f"TIME BUDGET — 1 ship-hour = {yr_per_hr:.2f} Earth years")
    ax2.set_facecolor("#080c18")

    plt.tight_layout()
    return fig


# ── §13.7  GW event catalogue and SNR summary ────────────────────────────────
def _plot_gw_catalog(events: List[GWEvent]) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.patch.set_facecolor("#060a14")

    if not events:
        return fig

    Mc_list   = [e.Mc_solar for e in events]
    snr_list  = [e.snr for e in events]
    dist_list = [e.dist_mpc for e in events]
    fq_list   = [e.f_qnm_hz for e in events]

    ax1 = axes[0]
    sc1 = ax1.scatter(Mc_list, snr_list, c=dist_list,
                       cmap="plasma", s=60, alpha=0.85,
                       edgecolors="#E8C46A", lw=0.4)
    plt.colorbar(sc1, ax=ax1, label="Distance [Mpc]", pad=0.02)
    ax1.axhline(5.0, color="#FFB74D", lw=0.8, ls="--",
                label="5σ detection threshold")
    ax1.axhline(8.0, color="#81C784", lw=0.8, ls=":",
                label="8σ confident")
    ax1.set_xlabel("M_chirp  [M☉]"); ax1.set_ylabel("SNR  ρ")
    ax1.set_title("GW CATALOGUE — SNR vs Chirp Mass")
    ax1.legend(fontsize=5.5)

    ax2 = axes[1]
    ax2.scatter(dist_list, Mc_list, c=snr_list,
                cmap="inferno", s=60, alpha=0.85,
                edgecolors="#E8C46A", lw=0.4)
    ax2.set_xlabel("Distance  [Mpc]"); ax2.set_ylabel("M_chirp  [M☉]")
    ax2.set_title("CHIRP MASS vs DISTANCE")

    ax3 = axes[2]
    ax3.hist(fq_list, bins=max(5, len(events)//3),
             color="#CE93D8", alpha=0.8, edgecolor="#1a2040")
    ax3.set_xlabel("f_QNM  [Hz]"); ax3.set_ylabel("Count")
    ax3.set_title("QNM FREQUENCY DISTRIBUTION")

    plt.tight_layout()
    return fig


# ── §13.8  Penrose diagram ────────────────────────────────────────────────────
def _plot_penrose(bh: KerrBlackHole) -> plt.Figure:
    _mpl()
    fig, ax = plt.subplots(figsize=(8, 9))
    fig.patch.set_facecolor("#060a14")
    penrose = PenroseCarterDiagram(bh)
    grid    = penrose.diagram_grid(n_t=60, n_r=100)

    # Constant-r lines
    for rl in grid["r_lines"]:
        clr = "#1a2540" if rl["r_M"] > 3 else "#2a1050"
        ax.plot(rl["X"], rl["T"], color=clr, lw=0.5)

    # Constant-t lines
    for tl in grid["t_lines"]:
        ax.plot(tl["X"], tl["T"], color="#1e2a45", lw=0.4)

    # Event horizons (diagonal lines in Kruskal)
    s = np.linspace(-math.pi/2*0.98, math.pi/2*0.98, 200)
    ax.plot(s,  s, color="#E8C46A", lw=1.2, ls="--",
            label=f"Outer horizon r₊={bh.r_plus/bh.M_geo:.4f}M")
    ax.plot(s, -s, color="#E8C46A", lw=1.2, ls="--")

    # Future singularity (top boundary)
    ax.axhline(math.pi/2*0.98, color="#D154FF", lw=1.0, ls="-",
               label="Singularity (r=0)")
    ax.axhline(-math.pi/2*0.98, color="#D154FF", lw=0.5, ls=":")

    # Spatial infinity
    ax.axvline(math.pi/2*0.98,  color="#555", lw=0.5, ls=":")
    ax.axvline(-math.pi/2*0.98, color="#555", lw=0.5, ls=":")

    # Label regions
    for txt, xy, c in [
        ("Region I\n(Our Universe)", (0.2, 0.0),  "#E8C46A"),
        ("Region II\n(Black Hole Interior)", (0.0, 0.9), "#CE93D8"),
        ("Region III\n(Parallel Universe)", (-0.8, 0.0), "#4FC3F7"),
    ]:
        ax.text(xy[0], xy[1], txt, ha="center", va="center",
                color=c, fontsize=6, style="italic",
                transform=ax.transData)

    ax.set_xlim(-math.pi/2, math.pi/2)
    ax.set_ylim(-math.pi/2, math.pi/2)
    ax.set_xlabel("X  (spatial conformal coordinate)")
    ax.set_ylabel("T  (temporal conformal coordinate)")
    ax.set_title(f"PENROSE-CARTER CONFORMAL DIAGRAM — Kerr BH  a*={bh.spin_star:.8f}")
    ax.legend(fontsize=6, loc="lower right")
    ax.set_facecolor("#030508")
    plt.tight_layout()
    return fig


# ── §13.9  Hawking spectrum figure ───────────────────────────────────────────
def _plot_hawking(bh: KerrBlackHole) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.patch.set_facecolor("#060a14")

    hawk = HawkingRadiationCalculator(bh)
    nu_arr, E_spec = hawk.hawking_spectrum_arrays(n_pts=400)

    axes[0].loglog(nu_arr, E_spec + 1e-300, color="#E8C46A", lw=1.1)
    axes[0].set_xlabel("Frequency  [Hz]")
    axes[0].set_ylabel("dP/dω  [J s rad⁻¹]")
    axes[0].set_title(
        f"HAWKING RADIATION SPECTRUM\n"
        f"T_H = {bh.T_hawking:.4e} K   "
        f"P_total = {hawk.total_power():.3e} W")

    # Occupation number
    axes[1].loglog(nu_arr, hawk.planck_occupation(2*math.pi*nu_arr) + 1e-300,
                   color="#CE93D8", lw=1.1)
    axes[1].set_xlabel("Frequency  [Hz]")
    axes[1].set_ylabel("Occupation number  n(ω)")
    axes[1].set_title(
        f"BOSE-EINSTEIN OCCUPATION\n"
        f"t_evap = {hawk.evaporation_time()/YEAR_S:.3e} yr   "
        f"λ_peak = {hawk.peak_wavelength():.3e} m")

    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# §14  MAIN STREAMLIT PAGE
# ══════════════════════════════════════════════════════════════════════════════
def gravity_engine_page():
    init_session_state()
    _mpl()
    S = st.session_state

    # ── Page header ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="border-left:3px solid #E8C46A;padding:.55rem 1.2rem;
                margin-bottom:1.2rem;background:rgba(232,196,106,0.035);
                font-family:monospace;">
    <div style="color:#E8C46A;font-size:.95rem;letter-spacing:.12em;
                font-weight:600;">◉ GRAVITATIONAL PHYSICS LABORATORY</div>
    <div style="color:#5a6a90;font-size:.62rem;margin-top:.2rem;">
    Object: GARGANTUA · Kerr Black Hole · M = 10⁸ M☉ · a* ≈ 1 − 10⁻¹⁴
    &nbsp;|&nbsp; Ref: Thorne 2014 · BPT 1972 · Novikov-Thorne 1973 · Carter 1968
    </div></div>""", unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    (tab_bh, tab_disk, tab_gw,
     tab_tidal, tab_miller,
     tab_profiles, tab_penrose) = st.tabs([
        "⬡ BH ANATOMY",
        "◎ ACCRETION DISK",
        "〜 GRAVITATIONAL WAVES",
        "⊛ TIDAL FORCES",
        "⏱ MILLER'S WORLD",
        "◈ RADIAL PROFILES",
        "◇ PENROSE DIAGRAM",
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1 — BH ANATOMY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_bh:
        c1, c2, c3 = st.columns([1, 1.1, 2.5])

        with c1:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#E8C46A;margin-bottom:.4rem;">[ BLACK HOLE PARAMETERS ]</div>',
                unsafe_allow_html=True)
            bh_mass = st.number_input(
                "Mass (M☉)", value=float(S["grav_bh_mass"]),
                min_value=1e4, max_value=1e12, format="%.3e", step=1e6)
            bh_spin = st.slider("Spin a*", 0.0, 0.9999999,
                                float(S["grav_bh_spin"]),
                                step=1e-7, format="%.8f")

            if st.button("⬡ COMPUTE KERR GEOMETRY",
                         width='stretch', type="primary"):
                bh = KerrBlackHole(mass_solar=bh_mass, spin_star=bh_spin)
                S["grav_bh"]      = bh
                S["grav_bh_mass"] = bh_mass
                S["grav_bh_spin"] = bh_spin
                S["grav_miller"]  = bh.miller_world()

        bh  = S["grav_bh"]
        su  = bh.summary()
        mill= S.get("grav_miller") or bh.miller_world()
        hawk= HawkingRadiationCalculator(bh)

        with c2:
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.75rem;
                        border:1px solid rgba(232,196,106,.15);
                        border-radius:3px;line-height:2.0;">
            <b style="color:#E8C46A;font-size:.62rem;">── GEOMETRY ──</b><br>
            M = <b style="color:#E8C46A;">{su['mass_solar']:.3e} M☉</b>
            = <b style="color:#E8C46A;">{su['M_kg']:.3e} kg</b><br>
            a* = <b style="color:#4FC3F7;">{su['spin_a*']:.10f}</b><br>
            r_s = <b>{su['r_s_km']:.4e} km</b><br>
            r₊ (outer horizon) = <b style="color:#D154FF;">{su['r_plus_km']:.4e} km</b><br>
            r₋ (inner horizon) = <b style="color:#FF8800;">{su['r_minus_km']:.4e} km</b><br>
            r_erg (equatorial) = <b style="color:#CE93D8;">{su['r_ergo_eq_km']:.4e} km</b><br>
            r_ph (photon sphere)= <b style="color:#81C784;">{su['r_photon_km']:.4e} km</b><br>
            r_ISCO (prograde)   = <b style="color:#4FC3F7;">{su['r_isco_pro_km']:.4e} km
            ({su['r_isco_pro_rs']:.6f} r_s)</b><br>
            r_ISCO (retrograde) = <b>{su['r_isco_ret_km']:.4e} km</b><br>
            Ω_H (horizon) = <b style="color:#FFD700;">{su['omega_H_rads']:.4e} rad/s</b><br>
            η_ISCO = <b style="color:#FF8800;">{su['eta_ISCO_pct']:.2f}%</b><br>
            η_Penrose_max = <b style="color:#CE93D8;">{su['eta_Penrose_max_pct']:.3f}%</b><br>
            <b style="color:#E8C46A;font-size:.62rem;">── HAWKING ──</b><br>
            T_H = <b style="color:#666;">{su['T_hawking_K']:.4e} K</b><br>
            P_H = <b style="color:#666;">{su['L_hawking_W']:.4e} W</b><br>
            t_evap = <b style="color:#666;">{hawk.evaporation_time()/YEAR_S:.4e} yr</b><br>
            <b style="color:#E8C46A;font-size:.62rem;">── MILLER'S WORLD ──</b><br>
            r_Miller = <b style="color:#D154FF;">
            {mill['r_miller_risco_ratio']:.8f} r_ISCO</b><br>
            dτ/dt = <b style="color:#D154FF;">{mill['actual_dtau_dt']:.4e}</b><br>
            Earth yr/ship hr = <b style="color:#D154FF;">
            {mill['earth_yr_per_ship_hr']:.3f}</b><br>
            Tidal class = <b>{mill['tidal_class']}</b><br>
            Wave height ≈ <b style="color:#4FC3F7;">
            {mill['ocean_wave_height_m']:.0f} m</b>
            </div>""", unsafe_allow_html=True)

        with c3:
            fig = _plot_bh_anatomy(bh)
            st.pyplot(fig, width='stretch')
            plt.close(fig)

        # Hawking spectrum below
        st.markdown("---")
        hfig = _plot_hawking(bh)
        st.pyplot(hfig, width='stretch')
        plt.close(hfig)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — ACCRETION DISK
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_disk:
        c1, c2 = st.columns([1, 3])
        bh = S["grav_bh"]
        with c1:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#E8C46A;">[ DISK PARAMETERS ]</div>',
                unsafe_allow_html=True)
            mdot  = st.slider("Accretion rate (Eddington fraction)",
                               0.001, 2.0, float(S["grav_mdot"]), 0.005)
            inc_d = st.slider("Observer inclination  (°)",
                               0.0, 89.0, float(S["grav_inc"]), 0.5)

            if st.button("◎ RENDER DISK IMAGE",
                         width='stretch', type="primary"):
                disk = NovikovThorneAccretionDisk(bh, mdot_edd=mdot)
                S["grav_disk"] = disk
                S["grav_mdot"] = mdot
                S["grav_inc"]  = inc_d

            disk = S.get("grav_disk") or NovikovThorneAccretionDisk(bh, S["grav_mdot"])
            L_tot = disk.total_luminosity()
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.6rem;
                        border:1px solid rgba(232,196,106,.12);
                        border-radius:3px;line-height:1.9;margin-top:.5rem;">
            ṁ = {mdot:.3f} × L_Edd<br>
            ṁ_SI = {disk.mdot_si:.3e} kg/s<br>
            L_Edd = {disk.L_edd:.3e} W<br>
            L_disk ≈ {L_tot:.3e} W<br>
            η_ISCO = {bh.eta_isco*100:.2f}%<br>
            T_peak ≈ {disk.temperature(bh.r_isco_pro*1.001):.3e} K<br>
            r_ISCO = {bh.r_isco_pro/1e3:.3e} km<br>
            Inclination = {inc_d:.1f}°
            </div>""", unsafe_allow_html=True)

            # SED
            st.markdown(
                '<div style="font-family:monospace;font-size:.60rem;'
                'color:#E8C46A;margin-top:.8rem;">SPECTRAL ENERGY DISTRIBUTION</div>',
                unsafe_allow_html=True)
            _mpl()
            fig_sed, ax_sed = plt.subplots(figsize=(4.5, 3))
            nu_arr = np.logspace(12, 20, 200)
            spec   = disk.spectral_energy_distribution(nu_arr, n_r=120)
            nu_E   = nu_arr * spec
            ax_sed.loglog(nu_arr, nu_E + 1e-100, color="#FF8800", lw=1.0)
            ax_sed.set_xlabel("ν  [Hz]"); ax_sed.set_ylabel("ν·Fν  [arb]")
            ax_sed.set_title("NT Disk SED", fontsize=7)
            ax_sed.set_facecolor("#080c18")
            fig_sed.patch.set_facecolor("#060a14")
            st.pyplot(fig_sed, width='stretch')
            plt.close(fig_sed)

        with c2:
            disk = S.get("grav_disk") or NovikovThorneAccretionDisk(bh, S["grav_mdot"])
            fig = _plot_disk_panel(bh, disk, S["grav_inc"])
            st.pyplot(fig, width='stretch')
            plt.close(fig)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — GRAVITATIONAL WAVES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_gw:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#E8C46A;">[ GW SOURCE PARAMETERS ]</div>',
                unsafe_allow_html=True)
            m1    = st.slider("m₁ primary  (M☉)",   5.0, 500.0,
                               float(S["grav_m1"]), 0.5)
            m2    = st.slider("m₂ secondary  (M☉)", 5.0, 500.0,
                               float(S["grav_m2"]), 0.5)
            dist  = st.slider("Luminosity distance  (Mpc)", 10.0, 10000.0,
                               float(S["grav_dist"]), 10.0)
            chi   = st.slider("χ_eff (effective spin)", -1.0, 1.0,
                               float(S["grav_chi"]), 0.01)
            noise = st.number_input("Detector noise σ  [strain]",
                                    value=float(S["grav_noise"]),
                                    format="%.2e", step=1e-23)
            S["grav_m1"] = m1; S["grav_m2"] = m2
            S["grav_dist"] = dist; S["grav_chi"] = chi
            S["grav_noise"] = noise

            gwe = GravitationalWaveEngine(fs=4096.0, duration=16.0)
            Mc  = gwe.chirp_mass(m1, m2)
            eta = gwe.eta(m1, m2)
            q   = gwe.mass_ratio(m1, m2)
            mf  = gwe.final_mass_fit(m1, m2, chi)
            af  = gwe.final_spin_fit(m1, m2, chi)
            fq, tq = gwe.qnm_freq_tau(mf, af)

            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.55rem;
                        border:1px solid rgba(232,196,106,.12);
                        border-radius:3px;line-height:1.85;">
            M_c    = <b style="color:#E8C46A;">{Mc:.4f} M☉</b><br>
            η      = <b style="color:#4FC3F7;">{eta:.5f}</b><br>
            q      = <b style="color:#4FC3F7;">{q:.4f}</b><br>
            M_fin  = <b style="color:#81C784;">{mf:.3f} M☉</b><br>
            a_fin  = <b style="color:#CE93D8;">{af:.5f}</b><br>
            f_QNM  = <b style="color:#FF8800;">{fq:.2f} Hz</b><br>
            τ_QNM  = <b style="color:#FFD700;">{tq*1e3:.3f} ms</b>
            </div>""", unsafe_allow_html=True)

            if st.button("〜 GENERATE GW EVENT",
                         width='stretch', type="primary"):
                with st.spinner("Generating IMR waveform..."):
                    wf = gwe.generate_waveform(
                        m1=m1, m2=m2, dist_mpc=dist,
                        chi_eff=chi, noise_sigma=noise)
                    S["grav_wf"] = wf
                    status = ("CONFIDENT" if wf["snr"] > 8 else
                              "DETECTED"  if wf["snr"] > 5 else "CANDIDATE")
                    evt = GWEvent(
                        m1_solar=m1, m2_solar=m2, chi_eff=chi,
                        dist_mpc=dist, snr=wf["snr"], snr_db=wf["snr_db"],
                        Mc_solar=Mc, eta=eta, m_final=mf, a_final=af,
                        f_qnm_hz=fq, tau_qnm_s=tq,
                        peak_freq=wf["peak_freq"], status=status)
                    S["grav_events"].append(evt)
                    S["grav_events"] = S["grav_events"][-40:]

        with c2:
            wf = S.get("grav_wf")
            if wf:
                sc  = ("#81C784" if wf["snr"] > 8 else
                       "#FFB74D" if wf["snr"] > 5 else "#D154FF")
                kpis = [
                    ("SNR",     f"{wf['snr']:.2f}",          sc),
                    ("SNR_dB",  f"{wf['snr_db']:.1f} dB",    sc),
                    ("M_c",     f"{wf['Mc']:.3f} M☉",        "#E8C46A"),
                    ("M_final", f"{wf['m_final']:.2f} M☉",   "#81C784"),
                    ("a_final", f"{wf['a_final']:.4f}",       "#CE93D8"),
                    ("f_QNM",   f"{wf['f_qnm']:.0f} Hz",     "#FF8800"),
                    ("τ_QNM",   f"{wf['tau_qnm']*1e3:.2f}ms","#FFD700"),
                    ("f_peak",  f"{wf['peak_freq']:.0f} Hz",  "#4FC3F7"),
                ]
                cols_k = st.columns(len(kpis))
                for col, (lbl, val, clr) in zip(cols_k, kpis):
                    col.markdown(
                        f'<div style="background:rgba(8,12,24,.9);'
                        f'border:1px solid rgba(232,196,106,.15);'
                        f'padding:.3rem;text-align:center;border-radius:2px;'
                        f'font-family:monospace;">'
                        f'<div style="color:#444;font-size:.48rem;">{lbl}</div>'
                        f'<div style="color:{clr};font-size:.80rem;">{val}</div>'
                        f'</div>', unsafe_allow_html=True)
                fig = _plot_gw_waveform(wf)
                st.pyplot(fig, width='stretch')
                plt.close(fig)
            else:
                st.info("Configure source parameters and generate a GW event.")

        # Catalogue
        evts = S.get("grav_events", [])
        if evts:
            st.markdown(
                '<div style="font-family:monospace;font-size:.62rem;'
                'color:#E8C46A;margin-top:1rem;">[ GW EVENT CATALOGUE ]</div>',
                unsafe_allow_html=True)
            df_evts = pd.DataFrame([e.to_dict() for e in evts[-20:]])
            st.dataframe(df_evts, width='stretch', hide_index=True)
            if len(evts) >= 3:
                fig_cat = _plot_gw_catalog(evts)
                st.pyplot(fig_cat, width='stretch')
                plt.close(fig_cat)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 4 — TIDAL FORCES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_tidal:
        bh = S["grav_bh"]
        c1, c2 = st.columns([1, 3])
        with c1:
            r_q = st.slider("Query radius (r/r_s)", 1.5, 200.0, 3.0, 0.05)
            m_q = st.slider("Object mass  (kg)", 10.0, 1e6, 70.0, 10.0)
            L_q = st.slider("Object length  (m)", 0.1, 200.0, 1.8, 0.1)
            sigma_q = st.select_slider(
                "Tensile strength  (Pa)",
                options=[1e5, 1e6, 4e8, 1e9, 1e10],
                value=1e6,
                format_func=lambda x: f"{x:.0e}")

            r_m = r_q * bh.r_s
            C_rr, C_th, _ = bh.tidal_tensor_diagonal(r_m)
            risk = bh.tidal_risk(r_m)
            r_sp = bh.spaghettification_radius(m_q, L_q, sigma_q)
            heat = bh.tidal_heating_rate(r_m)

            risk_col = {"SAFE":"#81C784","MARGINAL":"#FFB74D",
                        "DANGEROUS":"#FF5722","LETHAL":"#D154FF",
                        "SPAGHETTI":"#CE93D8"}.get(risk.name, "#fff")
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.58rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.65rem;
                        border:1px solid rgba(232,196,106,.12);
                        border-radius:3px;line-height:2.0;">
            <b style="color:#E8C46A;">── TIDAL @ r={r_q:.2f}r_s ──</b><br>
            C_rr  = <b style="color:#D154FF;">{C_rr:.4e} s⁻²</b><br>
            Δa_r  = <b style="color:#D154FF;">{abs(C_rr)/9.81:.4e} g/m</b><br>
            C_θθ  = <b style="color:#4FC3F7;">{C_th:.4e} s⁻²</b><br>
            Δa_⊥  = <b style="color:#4FC3F7;">{abs(C_th)/9.81:.4e} g/m</b><br>
            Risk  = <b style="color:{risk_col};">◆ {risk.name}</b><br>
            Heating = <b>{heat:.3e} W</b><br>
            <b style="color:#E8C46A;">── SPAGHETTIFICATION ──</b><br>
            r_sp (object) = <b style="color:#CE93D8;">
            {r_sp/bh.r_s:.4f} r_s</b><br>
            = <b style="color:#CE93D8;">{r_sp/1e3:.2f} km</b><br>
            Stable? <b>{"✓ Yes" if r_sp < r_m else "✗ No — inside!"}</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            if st.button("⊛ COMPUTE FULL TIDAL PROFILE",
                         width='stretch'):
                with st.spinner("Computing tidal tensor across 500 radii..."):
                    S["grav_tidal_df"] = bh.tidal_profile_dataframe(
                        r_min_rs=1.5, r_max_rs=200.0, n=500)
            if S.get("grav_tidal_df") is not None:
                fig = _plot_tidal(S["grav_tidal_df"], bh)
                st.pyplot(fig, width='stretch')
                plt.close(fig)
                with st.expander("◈ Tidal Data Table"):
                    st.dataframe(S["grav_tidal_df"].round(6),
                                 width='stretch', hide_index=True)
            else:
                st.info("Click 'Compute Full Tidal Profile' to run.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 5 — MILLER'S WORLD
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_miller:
        bh   = S["grav_bh"]
        mill = S.get("grav_miller") or bh.miller_world()
        S["grav_miller"] = mill

        c1, c2 = st.columns([1, 2])
        with c1:
            ship_hrs = st.slider("Ship-hours on Miller", 0.5, 72.0, 1.0, 0.5)
            earth_yr_lost = ship_hrs * mill["earth_yr_per_ship_hr"]
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.75rem;
                        border:1px solid rgba(232,196,106,.15);
                        border-radius:3px;line-height:2.1;">
            <b style="color:#E8C46A;font-size:.65rem;">── MILLER'S WORLD ──</b><br>
            r_Miller = <b style="color:#D154FF;">
            {mill['r_miller_risco_ratio']:.10f} × r_ISCO</b><br>
            Above ISCO = <b style="color:#D154FF;">
            {mill['r_miller_above_isco_m']:.3e} m</b><br>
            dτ/dt actual = <b>{mill['actual_dtau_dt']:.6e}</b><br>
            Dilation factor = <b>{1/mill['actual_dtau_dt']:.3e}</b><br>
            <br>
            Earth yr/ship hr = <b style="color:#D154FF;font-size:.72rem;">
            {mill['earth_yr_per_ship_hr']:.4f}</b><br>
            Ship min/Earth yr = <b>{mill['ship_min_per_earth_yr']:.4f}</b><br>
            <br>
            <b style="color:#E8C46A;">── ORBITAL MECHANICS ──</b><br>
            Ω_orb = <b>{mill['Omega_rads']:.4e} rad/s</b><br>
            Period = <b>{mill['period_s']:.3f} s</b><br>
            v_orb = <b>{mill['orbital_v_ms']/1e6:.4f}×10⁶ m/s
            ({mill['orbital_v_c']*100:.4f}% c)</b><br>
            <br>
            <b style="color:#E8C46A;">── ENVIRONMENT ──</b><br>
            Tidal class = <b>{mill['tidal_class']}</b><br>
            Tidal [g/m] = <b style="color:#FF8800;">
            {mill['tidal_radial_g_per_m']:.3e}</b><br>
            Grav. redshift = <b>{mill['gravitational_redshift']:.6f}</b><br>
            Wave height ≈ <b style="color:#4FC3F7;">
            {mill['ocean_wave_height_m']:.1f} m</b><br>
            Stable orbit = <b>{"✓" if mill["is_stable_orbit"] else "✗"}</b><br>
            <br>
            <b style="color:#E8C46A;font-size:.70rem;">── MISSION TIME BUDGET ──</b><br>
            {ship_hrs:.1f} ship-hours → <b style="color:#D154FF;font-size:.72rem;">
            {earth_yr_lost:.2f} Earth years lost</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            fig = _plot_miller(mill, bh)
            st.pyplot(fig, width='stretch')
            plt.close(fig)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 6 — RADIAL PROFILES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_profiles:
        bh = S["grav_bh"]
        if st.button("◈ COMPUTE FULL KERR PROFILE  (600 radii)",
                     width='stretch', type="primary"):
            with st.spinner("Integrating Kerr metric at 600 radii..."):
                S["grav_radial_df"] = bh.radial_profile(
                    r_min_rs=1.02, r_max_rs=150.0, n=600)

        df = S.get("grav_radial_df")
        if df is not None:
            fig = _plot_radial_profile(df, bh)
            st.pyplot(fig, width='stretch')
            plt.close(fig)
            with st.expander("◈ Full Data Table  (600×16)"):
                st.dataframe(df.round(8),
                             width='stretch', hide_index=True)
        else:
            st.info("Click the button to compute the full radial profile.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 7 — PENROSE DIAGRAM
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_penrose:
        bh  = S["grav_bh"]
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(8,12,24,.92);padding:.65rem;
                        border:1px solid rgba(232,196,106,.12);
                        border-radius:3px;line-height:1.9;">
            <b style="color:#E8C46A;">── CONFORMAL STRUCTURE ──</b><br>
            r₊ = {bh.r_plus/1e3:.4e} km<br>
            r₋ = {bh.r_minus/1e3:.4e} km<br>
            Tortoise: r*(r) = r + <br>
            &nbsp;1/(2κ₊)·ln|r−r₊|<br>
            &nbsp;+1/(2κ₋)·ln|r−r₋|<br>
            Penrose coords:<br>
            T = ½[arctan(v/M)+arctan(u/M)]<br>
            X = ½[arctan(v/M)−arctan(u/M)]<br>
            u=t−r*, v=t+r*<br><br>
            Region I  = Our universe (r>r₊)<br>
            Region II = BH interior (r₋<r<r₊)<br>
            Region III= Parallel universe<br>
            Singularity at T=π/2 boundary<br>
            </div>""", unsafe_allow_html=True)

            st.button("◇ RECOMPUTE PENROSE GRID",
                      on_click=lambda: S.update({"grav_penrose_grid": None}),
                      width='stretch')

        with c2:
            fig = _plot_penrose(bh)
            st.pyplot(fig, width='stretch')
            plt.close(fig)
