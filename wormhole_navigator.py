"""
wormhole_navigator.py — Wormhole Physics & Interstellar Navigation Engine
ENDURANCE Mission Control | Interstellar Science Platform v3.0.0
═══════════════════════════════════════════════════════════════════════════════
Scientific References:
  [1]  Morris & Thorne (1988) Am.J.Phys. 56:395  [Traversable wormhole]
  [2]  Morris, Thorne & Yurtsever (1988) PRL 61:1446  [Wormhole time machines]
  [3]  Ellis (1973) J.Math.Phys. 14:104  [Ellis drainhole — first exact solution]
  [4]  Visser (1995) "Lorentzian Wormholes" AIP Press  [Comprehensive review]
  [5]  Kip Thorne, "The Science of Interstellar" (W.W. Norton, 2014)
  [6]  Hochberg & Visser (1997) PRL 78:2050  [Energy conditions]
  [7]  Ford & Roman (1996) PRD 53:5496  [Quantum inequality, exotic matter]
  [8]  Taylor & Wheeler, "Exploring Black Holes" (Addison Wesley, 2000)
  [9]  Hohmann (1925); Braeunig (1998)  [Hohmann transfer orbit]
  [10] Bate, Mueller & White (1971) "Fundamentals of Astrodynamics"
  [11] Penrose (1965); Hawking (1966)  [Singularity theorems]
  [12] Alcubierre (1994) Class.Quant.Grav. 11:L73  [Warp drive for comparison]
  [13] Forward (1984) J.Propulsion 0:415  [Exotic matter propulsion]

Module implements:
  ┌─ WORMHOLE GEOMETRY ─────────────────────────────────────────────────────┐
  │ Morris-Thorne metric: ds² = −e^{2Φ}c²dt² + dl² + r(l)²dΩ²  [1]       │
  │ Shape function b(r): determines throat geometry                         │
  │ Redshift function Φ(r): determines time dilation through wormhole       │
  │ Throat radius b₀: minimum traversable radius                            │
  │ Embedding diagram: upper/lower universe sheet connection                │
  │ Flaring-out condition: b'(r₀) < 1 (required for traversability)        │
  │ Exotic matter distribution ρ_exotic(r) and tension τ(r)                │
  │ Ellis drainhole exact solution: Φ=0, b(r)=b₀²/r                       │
  │ Power-law family: b(r) = b₀(b₀/r)^α, α ∈ [0,1)                       │
  │ Null energy condition violation quantification                          │
  │ Geodesic completeness verification                                      │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ EXOTIC MATTER PHYSICS ─────────────────────────────────────────────────┐
  │ Negative energy density ρ_exotic = −T^{00}/c² < 0                      │
  │ Total exotic mass M_exotic = ∫ρ_exotic dV                               │
  │ Casimir energy density: ρ_C = −π²ħc/(720 d⁴) [7]                      │
  │ Quantum inequality bound: max |ρ_neg| × τ² ≤ ħ/(12π²c) [7]            │
  │ Required exotic mass vs throat radius scaling                            │
  │ Comparison: exotic mass vs Jupiter, Sun, galaxy                         │
  │ Feasibility metrics per wormhole configuration                          │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ TRAVERSAL PHYSICS ─────────────────────────────────────────────────────┐
  │ Transit time for traveller: τ_traveller = ∫ dl / (v_traverse)          │
  │ Transit time for external observer: t_external = ∫ e^{-Φ} dl/v         │
  │ Tidal force on traveller: |∂²ξ/∂τ²| < g_max (survivability)           │
  │ Acceleration felt by traveller: a = c²Φ'(r)  [redshift gradient]       │
  │ Wormhole stability: perturbation analysis                               │
  │ Entry/exit conditions: velocity, angle, approach trajectory             │
  │ Light travel time Saturn → wormhole                                     │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ INTERSTELLAR NAVIGATION ───────────────────────────────────────────────┐
  │ Saturn-to-wormhole trajectory (Hohmann + patched conics)               │
  │ Wormhole location near Saturn (Thorne canon: ~1 AU from Saturn)        │
  │ Gargantua system arrival: planet survey sequence                        │
  │ Orbital insertion: Endurance parking orbit parameters                  │
  │ Miller approach: spiral descent to near-ISCO                           │
  │ Gravitational slingshot: Gargantua flyby Δv calculations               │
  │ Plan B trajectory: Edmunds Planet rendezvous                           │
  │ Δv budgets, fuel mass fractions, engine specific impulse                │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ ORBITAL MECHANICS ─────────────────────────────────────────────────────┐
  │ Kepler's laws: period, semi-major axis, velocity                        │
  │ Vis-viva equation: v² = GM(2/r − 1/a)                                  │
  │ Hohmann transfer: Δv₁, Δv₂, transfer time                              │
  │ Gravity assist (slingshot): Δv from flyby geometry                     │
  │ Patched conics: sphere of influence boundaries                          │
  │ Lambert's problem: two-point boundary value trajectory                 │
  │ Hyperbolic escape/capture: v_∞, hyperbolic excess velocity              │
  │ Three-body: Lagrange points, stability                                  │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ MISSION TRAJECTORY PLANNER ────────────────────────────────────────────┐
  │ Full ENDURANCE mission Δv budget: launch → Saturn → wormhole            │
  │ Propellant mass fraction: Tsiolkovsky for each leg                     │
  │ Travel time accounting with relativistic corrections                    │
  │ Optimal launch window: Earth-Saturn synodic period                      │
  │ Gargantua system gravity map: Miller/Mann/Edmunds orbital data         │
  └──────────────────────────────────────────────────────────────────────────┘

"The wormhole is not a tunnel. It is a fold — a crease in spacetime itself."
                                             — Prof. Brand, NASA, 2063
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import math
import uuid
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
import pandas as pd
import scipy.integrate as sci_int
import scipy.optimize  as sci_opt
import scipy.special   as sci_sp

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot    as plt
import matplotlib.gridspec  as gridspec
import matplotlib.patches   as mpatches
import matplotlib.colors    as mcolors
import matplotlib.ticker    as mticker
from matplotlib.colors      import LinearSegmentedColormap
from matplotlib.patches     import FancyArrowPatch, Circle, Arc, FancyBboxPatch
from mpl_toolkits.mplot3d   import Axes3D

import streamlit as st

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# §1  PHYSICAL CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
G_SI      = 6.674_30e-11
C_SI      = 2.997_924_58e8
HBAR      = 1.054_571_817e-34
K_B       = 1.380_649e-23
M_SUN     = 1.989_000e30
L_SUN     = 3.828_000e26
M_EARTH   = 5.972_000e24
M_JUPITER = 1.898_000e27
M_SAT     = 5.683_000e26
R_EARTH   = 6.371_000e6
R_SAT     = 6.033_000e7
AU        = 1.495_978_707e11
LY        = 9.460_730_472e15
PC        = 3.085_677_581e16
YEAR_S    = 3.155_760e7
DAY_S     = 86_400.0
HOUR_S    = 3_600.0

# Gargantua
GARG_MASS_SOLAR = 1.00e8
GARG_MASS_KG    = GARG_MASS_SOLAR * M_SUN
GARG_M_GEO      = G_SI * GARG_MASS_KG / C_SI**2
GARG_RS         = 2.0 * GARG_M_GEO
GARG_SPIN       = 1.0 - 1e-14

# Interstellar wormhole (Thorne canon [5])
WORM_THROAT_M   = 1.0e9           # ~1000 km throat radius (Canon: ~1 AU diam)
WORM_LOC_SAT_AU = 1.0             # wormhole ~1 AU from Saturn (near L1-like)
SATURN_SMA_AU   = 9.537           # Saturn semi-major axis [AU]
WORM_SAT_DIST_M = WORM_LOC_SAT_AU * AU

# Solar system orbital parameters
SOL_MASS    = M_SUN
EARTH_SMA_M = 1.0 * AU
SAT_SMA_M   = 9.537 * AU

# Endurance parameters (film canon)
ENDURANCE_MASS_KG   = 5.0e5     # ~500 tonnes
ENDURANCE_ISP_S     = 9_000.0   # specific impulse (ion engine proxy) [s]
ENDURANCE_THRUST_N  = 1.5e6     # thrust [N]
RANGER_MASS_KG      = 1.5e4     # Ranger shuttle
LANDER_MASS_KG      = 2.0e4     # Lander

# ══════════════════════════════════════════════════════════════════════════════
# §2  CUSTOM COLORMAPS
# ══════════════════════════════════════════════════════════════════════════════
CMAP_WORM = LinearSegmentedColormap.from_list("wormhole",
    ["#000000","#050020","#100050","#2000a0","#4020e0",
     "#8060ff","#c0a0ff","#e0d0ff","#ffffff"], N=512)

CMAP_EXOTIC = LinearSegmentedColormap.from_list("exotic_matter",
    ["#000000","#200030","#600060","#c000c0","#ff00ff",
     "#ff80ff","#ffffff"], N=256)

CMAP_TRAJ = LinearSegmentedColormap.from_list("trajectory",
    ["#0a1428","#1040a0","#2080ff","#60c0ff","#E8C46A","#FF8800"], N=512)

# ══════════════════════════════════════════════════════════════════════════════
# §3  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════
class ShapeFunction(Enum):
    ELLIS        = "Ellis drainhole: b(r)=b₀²/r  (exact solution)"
    POWER_LAW    = "Power-law: b(r)=b₀(b₀/r)^α"
    EXPONENTIAL  = "Exponential: b(r)=b₀·exp(1−r/b₀)"
    ASYMPTOTIC   = "Asymptotic flat: b(r)=b₀r₀/(r₀+r−b₀)"
    CASIMIR      = "Casimir-supported: b(r)=b₀[1−(r−b₀)²/ℓ²]"

class RedshiftFunction(Enum):
    ZERO         = "Zero redshift: Φ=0  (tidal force from shape only)"
    CONSTANT     = "Constant: Φ=Φ₀ (uniform blueshift)"
    POWER        = "Power-law: Φ=−Φ₀(b₀/r)^n"
    INVERSE      = "Inverse: Φ=−b₀/r"
    INTERSTELLAR = "Interstellar canonical: Φ≈0 (tidal optimised)"

class TraversalStatus(Enum):
    VIABLE         = "VIABLE — survivable transit"
    MARGINAL       = "MARGINAL — extreme but survivable"
    TIDAL_LETHAL   = "LETHAL — tidal forces exceed human limit"
    TIME_EXCESSIVE = "EXCESSIVE — transit time too long"
    UNSTABLE       = "UNSTABLE — perturbation collapses wormhole"

class ManeuverType(Enum):
    HOHMANN        = "Hohmann transfer"
    BI_ELLIPTIC    = "Bi-elliptic transfer"
    GRAVITY_ASSIST = "Gravity assist / slingshot"
    DIRECT         = "Direct insertion"
    SPIRAL_ION     = "Ion spiral (low-thrust)"

# ══════════════════════════════════════════════════════════════════════════════
# §4  WORMHOLE GEOMETRY ENGINE
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class WormholeGeometry:
    """
    Morris-Thorne traversable wormhole spacetime [1].
    Metric: ds² = −e^{2Φ(l)}c²dt² + dl² + r(l)²(dθ²+sin²θ dφ²)
    where l is the proper radial distance from throat (l=0 at throat).
    Shape: r(l) = √(b₀² + l²)  for Ellis; generalised by b(r).
    """
    throat_radius_m : float = WORM_THROAT_M      # b₀ [m]
    shape_type      : ShapeFunction = ShapeFunction.ELLIS
    redshift_type   : RedshiftFunction = RedshiftFunction.ZERO
    shape_alpha     : float = 0.5     # for power-law family
    redshift_phi0   : float = 0.0    # for non-zero redshift
    uid             : str   = field(default_factory=lambda: uuid.uuid4().hex[:8].upper())

    def __post_init__(self):
        self.b0 = self.throat_radius_m

    # ── §4.1  Shape function b(r) ────────────────────────────────────────────
    def b(self, r: float) -> float:
        """Shape function b(r) ≥ 0; b(b₀) = b₀ (throat)."""
        b0 = self.b0
        r  = max(r, b0)
        if self.shape_type == ShapeFunction.ELLIS:
            return b0*b0 / r
        elif self.shape_type == ShapeFunction.POWER_LAW:
            a = self.shape_alpha
            return b0 * (b0/r)**a
        elif self.shape_type == ShapeFunction.EXPONENTIAL:
            return b0 * math.exp(1 - r/b0)
        elif self.shape_type == ShapeFunction.ASYMPTOTIC:
            r0 = b0
            return b0*r0 / (r0 + r - b0)
        elif self.shape_type == ShapeFunction.CASIMIR:
            ell = b0 * 3.0
            val = b0 * (1 - (r - b0)**2/ell**2)
            return max(0.0, val)
        return b0

    def b_prime(self, r: float, dr: float = 1.0) -> float:
        """Numerical derivative b'(r) = db/dr."""
        return (self.b(r + dr) - self.b(r - dr)) / (2*dr)

    def flaring_out_condition(self, r: float) -> float:
        """
        Flaring-out condition for traversability [1]:
          (b − rb') / (2b²) > 0  at throat
        Equivalently: b'(b₀) < 1  (must be satisfied).
        Returns the value (b − rb')/(2b²); positive → traversable.
        """
        b_r  = self.b(r)
        bp   = self.b_prime(r)
        return (b_r - r*bp) / (2*b_r**2 + 1e-30)

    # ── §4.2  Redshift function Φ(r) ────────────────────────────────────────
    def Phi(self, r: float) -> float:
        """Redshift function Φ(r); e^{2Φ} = time-time metric component."""
        b0 = self.b0
        r  = max(r, b0)
        if self.redshift_type == RedshiftFunction.ZERO:
            return 0.0
        elif self.redshift_type == RedshiftFunction.CONSTANT:
            return self.redshift_phi0
        elif self.redshift_type == RedshiftFunction.POWER:
            return -self.redshift_phi0 * (b0/r)**2
        elif self.redshift_type == RedshiftFunction.INVERSE:
            return -b0/r
        elif self.redshift_type == RedshiftFunction.INTERSTELLAR:
            return 0.0  # Thorne's Interstellar wormhole: zero tidal forces
        return 0.0

    def Phi_prime(self, r: float, dr: float = 1.0) -> float:
        return (self.Phi(r + dr) - self.Phi(r - dr)) / (2*dr)

    # ── §4.3  Proper radial distance l(r) ───────────────────────────────────
    def proper_distance_l(self, r: float) -> float:
        """
        Proper radial distance from throat:
          l(r) = ±∫_{b₀}^{r} dr'/√(1 − b(r')/r')
        Integrated numerically.
        """
        b0 = self.b0
        if r <= b0:
            return 0.0
        def integrand(rp):
            b_rp = self.b(rp)
            denom = 1.0 - b_rp/rp
            return 1.0/math.sqrt(max(denom, 1e-10))
        result, _ = sci_int.quad(integrand, b0*1.0001, r, limit=200)
        return result

    def r_from_l(self, l: float, tol: float = 1.0) -> float:
        """Invert l(r) to get r given l (numerical root finding)."""
        if l <= 0:
            return self.b0
        try:
            sol = sci_opt.brentq(
                lambda r: self.proper_distance_l(r) - l,
                self.b0*1.0001, self.b0*(1 + l/self.b0 + 1)*10,
                xtol=tol, maxiter=100)
            return sol
        except Exception:
            return self.b0 + l  # fallback: flat space approximation

    # ── §4.4  Embedding diagram ──────────────────────────────────────────────
    def embedding_surface(self, r_max_b0: float = 8.0,
                           n_r: int = 200) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Upper-universe embedding surface z(r):
          dz/dr = ±1/√(r/b(r) − 1)
        Returns (r_arr, l_arr, z_arr) for plotting.
        Integration from throat outward.
        """
        b0    = self.b0
        r_arr = np.geomspace(b0*1.0001, r_max_b0*b0, n_r)
        z_arr = np.zeros(n_r)
        for i in range(1, n_r):
            dr      = r_arr[i] - r_arr[i-1]
            r_mid   = 0.5*(r_arr[i] + r_arr[i-1])
            b_mid   = self.b(r_mid)
            radicand = r_mid/b_mid - 1.0
            dz_dr   = 1.0/math.sqrt(max(radicand, 1e-8))
            z_arr[i] = z_arr[i-1] + dz_dr*dr
        l_arr = np.array([self.proper_distance_l(r) for r in r_arr])
        return r_arr, l_arr, z_arr

    # ── §4.5  Metric components ──────────────────────────────────────────────
    def g_tt(self, r: float) -> float:
        """g_tt = −e^{2Φ(r)}"""
        return -math.exp(2*self.Phi(r))

    def g_ll(self, r: float) -> float:
        """g_ll = 1  (proper radial coordinate)"""
        return 1.0

    def g_thth(self, r: float) -> float:
        """g_θθ = r(l)²"""
        return r**2

    # ── §4.6  Exotic matter ──────────────────────────────────────────────────
    def stress_energy_tensor(self, r: float) -> Dict[str, float]:
        """
        Einstein field equations → stress-energy of matter supporting wormhole.
        For Morris-Thorne metric in orthonormal frame [1]:
          8πG T^{ôô}/c⁴ = −b'(r)/(r²)                   [energy density]
          8πG T^{l̂l̂}/c⁴ = (2/r)(1−b/r)Φ' − b'/(r²)    [radial tension]
          8πG T^{θ̂θ̂}/c⁴ = (1−b/r)[Φ''+(Φ')² + Φ'/r − b'r−b/(2r²(1−b/r)) − Φ'/r]  [lateral]
        Returns: energy_density [kg/m³], radial_tension [Pa], lateral_pressure [Pa].
        """
        bp  = self.b_prime(r)
        bv  = self.b(r)
        Phip= self.Phi_prime(r)
        G8pi = 8*math.pi*G_SI
        # Energy density (exotic if negative)
        rho  = -bp / (G8pi * C_SI**2 * r**2)   # [kg/m³]
        # Radial tension τ(r) = −T^{rr} (positive = tension, negative = pressure)
        if r > self.b0:
            f    = 1.0 - bv/r
            tau  = -(2.0/r * f * Phip - bp/r**2) * C_SI**4/(G8pi)
        else:
            tau  = 0.0
        # Lateral pressure
        p_lat = 0.0  # simplified (full expression requires Φ'')
        return {"rho_kg_m3": rho, "radial_tension_Pa": tau,
                "lateral_pressure_Pa": p_lat,
                "is_exotic": rho < 0,
                "nec_violation": rho + tau/C_SI**2 < 0}

    def exotic_mass_total(self, r_max_b0: float = 100.0) -> float:
        """
        Total exotic mass (volume integral of |ρ_exotic|):
          M_exotic = ∫_{b₀}^{r_max} |ρ(r)| 4πr² dr
        Units: kg.
        """
        b0 = self.b0
        def integrand(r):
            rho = self.stress_energy_tensor(r)["rho_kg_m3"]
            return abs(rho) * 4*math.pi*r**2
        r_arr = np.geomspace(b0*1.001, r_max_b0*b0, 500)
        rho_arr = np.array([abs(self.stress_energy_tensor(r)["rho_kg_m3"])
                             for r in r_arr])
        return trapz(rho_arr * 4*math.pi*r_arr**2, r_arr)

    def flaring_satisfies(self) -> bool:
        """Check flaring-out condition at throat."""
        return self.b_prime(self.b0*1.001) < 1.0

    def summary(self) -> Dict[str, Any]:
        M_ex  = self.exotic_mass_total()
        return {
            "throat_radius_m":   self.b0,
            "throat_radius_km":  self.b0/1e3,
            "shape_type":        self.shape_type.value,
            "redshift_type":     self.redshift_type.value,
            "b_prime_at_throat": self.b_prime(self.b0*1.001),
            "flaring_condition": self.flaring_satisfies(),
            "Phi_at_throat":     self.Phi(self.b0),
            "g_tt_at_throat":    self.g_tt(self.b0),
            "exotic_mass_kg":    M_ex,
            "exotic_mass_Jupiter": M_ex/M_JUPITER,
            "exotic_mass_Sun":   M_ex/M_SUN,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §5  EXOTIC MATTER PHYSICS
# ══════════════════════════════════════════════════════════════════════════════
class ExoticMatterPhysics:
    """
    Quantitative exotic matter analysis: Casimir energy, quantum inequality
    bounds, feasibility assessment for wormhole maintenance.
    References: Ford & Roman [7], Visser [4].
    """

    def __init__(self, wormhole: WormholeGeometry):
        self.wh = wormhole

    def casimir_energy_density(self, plate_sep_m: float) -> float:
        """
        Casimir energy density between parallel plates [7]:
          ρ_C = −π²ħc / (720 d⁴)  [J/m³]
        Negative energy density — the only known macroscopic source.
        """
        return -math.pi**2 * HBAR * C_SI / (720.0 * plate_sep_m**4)

    def casimir_total_energy(self, plate_sep_m: float,
                              plate_area_m2: float) -> float:
        """Total Casimir energy E_C = ρ_C × volume  [J]."""
        return self.casimir_energy_density(plate_sep_m) * plate_sep_m * plate_area_m2

    def quantum_inequality_bound(self, sampling_time_s: float) -> float:
        """
        Ford-Roman quantum inequality [7]:
          ∫ ρ(τ) g(τ) dτ ≥ −ħ/(12π²c·τ₀⁴)
        Maximum magnitude of negative energy density observable in time τ₀.
        Returns |ρ_max| [J/m³].
        """
        return HBAR / (12.0 * math.pi**2 * C_SI * sampling_time_s**4)

    def required_plate_sep_for_throat(self) -> float:
        """
        Plate separation needed for Casimir energy to support wormhole throat.
        Rough estimate: ρ_C × b₀³ ~ M_exotic × c²
        → d = (π²ħc b₀³ / (720 M_exotic c²))^{1/4}
        """
        M_ex = max(self.wh.exotic_mass_total(), 1e-10)
        b0   = self.wh.b0
        num  = math.pi**2 * HBAR * C_SI * b0**3
        den  = 720.0 * M_ex * C_SI**2
        return (num/den)**0.25

    def exotic_mass_scaling_table(self) -> pd.DataFrame:
        """Table of exotic mass vs throat radius for various shape functions."""
        b0_arr = np.geomspace(1e3, 1e12, 20)   # 1 km to 1 AU
        rows = []
        for b0 in b0_arr:
            for shape in [ShapeFunction.ELLIS, ShapeFunction.POWER_LAW]:
                wh  = WormholeGeometry(b0, shape_type=shape)
                M_ex = wh.exotic_mass_total()
                rows.append({
                    "b₀ (m)":       b0,
                    "b₀ (km)":      b0/1e3,
                    "Shape":        shape.name,
                    "M_exotic (kg)": M_ex,
                    "M_exotic/M_Jupiter": M_ex/M_JUPITER,
                    "M_exotic/M_Sun": M_ex/M_SUN,
                    "feasible_1e12J": abs(M_ex*C_SI**2) < 1e40,
                })
        return pd.DataFrame(rows)

    def feasibility_report(self) -> Dict[str, Any]:
        M_ex   = self.wh.exotic_mass_total()
        E_ex   = abs(M_ex) * C_SI**2
        d_cas  = self.required_plate_sep_for_throat()
        rho_c  = self.casimir_energy_density(d_cas)
        qi     = self.quantum_inequality_bound(HOUR_S)
        return {
            "throat_km":          self.wh.b0/1e3,
            "exotic_mass_kg":     M_ex,
            "exotic_mass_Jupiter":M_ex/M_JUPITER,
            "exotic_energy_J":    E_ex,
            "exotic_energy_stars": E_ex / (L_SUN*YEAR_S),
            "casimir_plate_sep_m": d_cas,
            "casimir_rho_J_m3":   rho_c,
            "QI_bound_J_m3":      qi,
            "ratio_rho_to_QI":    abs(rho_c)/qi if qi > 0 else 0,
            "feasibility":        ("Theoretically possible"
                                   if abs(rho_c) < qi * 1e10
                                   else "Beyond known physics"),
        }


# ══════════════════════════════════════════════════════════════════════════════
# §6  WORMHOLE TRAVERSAL CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
class WormholeTraversalCalculator:
    """
    Physics of actually flying through a Morris-Thorne wormhole [1,4,5].
    Computes transit time, tidal forces, and survivability for the Endurance.
    """

    HUMAN_TIDAL_LIMIT = 10.0 * 9.81   # 10g per meter [m/s² per m]
    HUMAN_ACCEL_LIMIT = 5.0  * 9.81   # 5g sustained [m/s²]

    def __init__(self, wormhole: WormholeGeometry):
        self.wh = wormhole

    def transit_time_traveller(self, v_traverse: float,
                                n_l: int = 400) -> float:
        """
        Proper time for traversal at speed v through wormhole (l from −L to +L):
          τ = ∫_{-L}^{+L} dl/v(l)
        For constant v: τ = 2L/v  where L = proper length of wormhole.
        L estimated as l(r_max) where b(r_max) ≪ b₀.
        """
        b0     = self.wh.b0
        r_max  = b0 * 10.0   # practical outer boundary
        L_prop = self.wh.proper_distance_l(r_max)   # one-sided proper length
        total_L = 2.0 * L_prop
        return total_L / v_traverse

    def transit_time_external(self, v_traverse: float) -> float:
        """
        Coordinate time for external observer watching traversal:
          t_ext = ∫ e^{-Φ(r)} dl / v
        For Φ=0: t_ext = τ_traveller.
        """
        b0    = self.wh.b0
        r_max = b0 * 10.0
        r_arr = np.geomspace(b0*1.001, r_max, 200)
        l_arr = np.array([self.wh.proper_distance_l(r) for r in r_arr])
        Phi_arr = np.array([self.wh.Phi(r) for r in r_arr])
        # Integrand: e^{-Φ}/v at each proper-distance point
        integrand = np.exp(-Phi_arr) / v_traverse
        # Integrate over l (proper distance)
        dl_arr = np.gradient(l_arr)
        t_one_side = np.sum(integrand * dl_arr)
        return 2.0 * t_one_side

    def tidal_force_at_throat(self) -> float:
        """
        Radial tidal force per unit separation at throat [1]:
          Δa/Δξ = −(e^{−2Φ}/r)(d²r/dl² − r(Φ')²)  (radial component)
        For Ellis wormhole (Φ=0): Δa/Δξ = b₀²/(r(l))^4  [s⁻²]
        At throat: = 1/b₀²  × c²  [m/s² per m separation]
        """
        b0 = self.wh.b0
        # Radial geodesic deviation (simplified for Φ=0):
        # d²ξ^r/dτ² = −R^r_{τrτ} ξ^r = (b₀²/(r⁴) - Φ'²)ξ^r
        # At r=b₀: R^r_{τrτ} = −b₀''/(2b₀)  (for Morris-Thorne)
        # Ellis exact: Δa/Δξ = c²/b₀²
        return C_SI**2 / (b0**2)

    def tidal_force_profile(self, n_l: int = 300
                             ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Tidal force profile along wormhole proper distance l.
        Returns (l_arr_m, tidal_radial_g_per_m, tidal_lateral_g_per_m).
        """
        b0     = self.wh.b0
        r_max  = b0 * 8.0
        r_arr  = np.geomspace(b0*1.001, r_max, n_l)
        l_arr  = np.array([self.wh.proper_distance_l(r) for r in r_arr])
        # Radial tidal: c²/r² × f(b,Φ)
        tidal_r = C_SI**2 / r_arr**2 * (self.wh.b(r_arr[0]) / r_arr)**1
        tidal_r = np.array([C_SI**2/r**2*(self.wh.b(r)/r) for r in r_arr])
        # Lateral tidal (different sign)
        tidal_l = np.array([C_SI**2/(2*r**2) for r in r_arr])
        return l_arr, tidal_r/9.81, tidal_l/9.81

    def survivability_check(self, v_traverse: float,
                             crew_separation_m: float = 1.8
                             ) -> TraversalStatus:
        """Check if traversal is survivable for human crew."""
        tidal_throat = self.tidal_force_at_throat() * crew_separation_m / 9.81
        accel        = abs(self.wh.Phi_prime(self.wh.b0*1.01)) * C_SI**2 / 9.81
        tau          = self.transit_time_traveller(v_traverse)

        if tidal_throat > 100.0:
            return TraversalStatus.TIDAL_LETHAL
        elif tidal_throat > 10.0 or accel > self.HUMAN_ACCEL_LIMIT/9.81:
            return TraversalStatus.MARGINAL
        elif tau > 30.0*DAY_S:
            return TraversalStatus.TIME_EXCESSIVE
        else:
            return TraversalStatus.VIABLE

    def interstellar_wormhole_profile(self) -> Dict[str, Any]:
        """
        Profile for the Interstellar canon wormhole near Saturn.
        Throat ~1 AU in diameter per some interpretations; Thorne [5] uses
        ~1 km as physically well-motivated for macroscopic traversal.
        """
        v_tr  = 0.1 * C_SI   # 10% c traversal
        tau   = self.transit_time_traveller(v_tr)
        t_ext = self.transit_time_external(v_tr)
        tidal = self.tidal_force_at_throat() * 1.8 / 9.81
        status= self.survivability_check(v_tr)
        return {
            "throat_radius_m":      self.wh.b0,
            "throat_radius_km":     self.wh.b0/1e3,
            "traversal_speed_c":    0.1,
            "tau_traveller_s":      tau,
            "tau_traveller_hr":     tau/HOUR_S,
            "t_external_s":         t_ext,
            "t_external_hr":        t_ext/HOUR_S,
            "tidal_at_throat_g_m":  tidal,
            "peak_accel_g":         abs(self.wh.Phi_prime(self.wh.b0))*C_SI**2/9.81,
            "traversal_status":     status.value,
            "wormhole_viable":      status == TraversalStatus.VIABLE,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §7  ORBITAL MECHANICS ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class OrbitalMechanics:
    """
    Keplerian orbital mechanics, Hohmann transfers, gravity assists,
    vis-viva equation, and escape/capture trajectories.
    References: Bate-Mueller-White [10], Braeunig [9].
    """

    def __init__(self, central_mass_kg: float = M_SUN):
        self.M   = central_mass_kg
        self.mu  = G_SI * central_mass_kg    # gravitational parameter [m³/s²]

    # ── §7.1  Kepler ─────────────────────────────────────────────────────────
    def orbital_velocity(self, r: float, a: float = None) -> float:
        """
        Vis-viva equation: v² = μ(2/r − 1/a)  [m/s]
        For circular orbit (a=r): v_c = √(μ/r).
        """
        a = a if a is not None else r
        return math.sqrt(self.mu * (2.0/r - 1.0/a))

    def orbital_period(self, a: float) -> float:
        """T = 2π√(a³/μ)  [s]"""
        return 2*math.pi*math.sqrt(a**3/self.mu)

    def escape_velocity(self, r: float) -> float:
        """v_esc = √(2μ/r)  [m/s]"""
        return math.sqrt(2*self.mu/r)

    def circular_orbit_altitude(self, T_s: float) -> float:
        """Semi-major axis from orbital period: a = (μT²/4π²)^{1/3}"""
        return (self.mu * T_s**2 / (4*math.pi**2))**(1/3)

    def sphere_of_influence(self, m_planet: float, a_planet: float) -> float:
        """r_SOI = a (m/M)^{2/5}  (Laplace sphere of influence)"""
        return a_planet * (m_planet/self.M)**(2/5)

    # ── §7.2  Hohmann transfer ────────────────────────────────────────────────
    def hohmann_transfer(self, r1: float, r2: float) -> Dict[str, float]:
        """
        Hohmann two-impulse transfer between circular orbits [9].
        r1: initial orbit radius, r2: target orbit radius.
        a_transfer = (r1+r2)/2.
        Δv₁ = v_transfer_periapsis − v_circular_1
        Δv₂ = v_circular_2 − v_transfer_apoapsis
        """
        a_tr  = 0.5*(r1 + r2)
        v1_c  = self.orbital_velocity(r1)
        v2_c  = self.orbital_velocity(r2)
        v_per = self.orbital_velocity(r1, a_tr)   # speed at periapsis of transfer
        v_apo = self.orbital_velocity(r2, a_tr)   # speed at apoapsis of transfer
        dv1   = abs(v_per - v1_c)
        dv2   = abs(v2_c  - v_apo)
        T_tr  = self.orbital_period(a_tr) / 2.0
        return {
            "r1_m": r1, "r2_m": r2,
            "a_transfer_m": a_tr,
            "dv1_ms": dv1, "dv2_ms": dv2,
            "dv_total_ms": dv1+dv2,
            "dv_total_kms": (dv1+dv2)/1e3,
            "transfer_time_s": T_tr,
            "transfer_time_days": T_tr/DAY_S,
            "v_periapsis_ms": v_per,
            "v_apoapsis_ms":  v_apo,
        }

    # ── §7.3  Gravity assist ──────────────────────────────────────────────────
    def gravity_assist_dv(self, v_inf_approach: float,
                           flyby_body_mass: float,
                           r_periapsis: float,
                           turn_angle_rad: float = None) -> Dict[str, float]:
        """
        Gravity assist (slingshot) Δv calculation.
        Maximum Δv at periapsis:
          v_turn = 2·v_∞·sin(δ/2)  where sin(δ/2) = 1/(1+r_p·v_∞²/(μ_body))
        v_∞: hyperbolic excess velocity at body
        """
        mu_body = G_SI * flyby_body_mass
        # Eccentricity of hyperbolic trajectory
        e = 1.0 + r_periapsis * v_inf_approach**2 / mu_body
        # Half-deflection angle
        sin_half_delta = 1.0/e
        sin_half_delta = min(sin_half_delta, 0.9999)
        delta = 2.0*math.asin(sin_half_delta)
        # Δv from slingshot (magnitude of velocity vector change)
        dv_assist = 2.0 * v_inf_approach * math.sin(delta/2.0)
        # v_periapsis
        v_peri = math.sqrt(v_inf_approach**2 + 2*mu_body/r_periapsis)
        return {
            "v_inf_ms":       v_inf_approach,
            "r_periapsis_m":  r_periapsis,
            "eccentricity":   e,
            "deflection_rad": delta,
            "deflection_deg": math.degrees(delta),
            "dv_assist_ms":   dv_assist,
            "dv_assist_kms":  dv_assist/1e3,
            "v_periapsis_ms": v_peri,
        }

    def gargantua_slingshot(self, r_periapsis_rs: float,
                             v_approach_ms: float) -> Dict[str, float]:
        """
        Gravity assist around Gargantua at r_peri = r_periapsis_rs × r_s.
        Includes relativistic correction: actual deflection larger than Newtonian.
        GR deflection: δ_GR = 4GM/(c²b) × [1 + v²/c²] (approximate).
        """
        r_s  = 2*G_SI*GARG_MASS_KG/C_SI**2
        r_p  = r_periapsis_rs * r_s
        # Newtonian
        newt = self.gravity_assist_dv(v_approach_ms, GARG_MASS_KG, r_p)
        # GR correction factor (approximate, using post-Newtonian result)
        b_impact = r_p   # impact parameter ≈ r_peri for nearly parabolic
        gr_corr  = 1.0 + (v_approach_ms/C_SI)**2 + G_SI*GARG_MASS_KG/(C_SI**2*r_p)
        dv_gr    = newt["dv_assist_ms"] * gr_corr
        # Time dilation at periapsis
        dtr = math.sqrt(max(0, 1 - r_s/r_p - (v_approach_ms/C_SI)**2))
        return {
            **newt,
            "r_periapsis_rs":   r_periapsis_rs,
            "GR_correction":    gr_corr,
            "dv_GR_corrected_ms": dv_gr,
            "dv_GR_kms":        dv_gr/1e3,
            "time_dilation_dtr": dtr,
            "rs_m":             r_s,
        }

    # ── §7.4  Hyperbolic trajectory ───────────────────────────────────────────
    def hyperbolic_trajectory(self, v_inf: float,
                               r_periapsis: float,
                               central_mass: float = None,
                               n_pts: int = 400) -> Dict[str, np.ndarray]:
        """
        Full hyperbolic trajectory (r, θ) for flyby.
          r(θ) = a(e²−1) / (1 + e·cosθ)
          a = −μ/v_∞²,   e = 1 + r_p v_∞²/μ
        Returns (x, y, r, theta) arrays in [m].
        """
        mu  = self.mu if central_mass is None else G_SI*central_mass
        a   = -mu / v_inf**2          # negative for hyperbola
        e   = 1.0 + r_periapsis*v_inf**2/mu
        # Angular range: from −θ_inf to +θ_inf
        theta_inf = math.acos(-1.0/e) * 0.98   # asymptotic angle
        theta_arr = np.linspace(-theta_inf, theta_inf, n_pts)
        r_arr     = a*(e**2 - 1) / (1 + e*np.cos(theta_arr))
        x_arr     = r_arr * np.cos(theta_arr)
        y_arr     = r_arr * np.sin(theta_arr)
        v_peri    = math.sqrt(v_inf**2 + 2*mu/r_periapsis)
        return {
            "theta": theta_arr, "r": r_arr,
            "x": x_arr, "y": y_arr,
            "a_m": a, "e": e,
            "r_periapsis_m": r_periapsis,
            "v_inf_ms": v_inf, "v_periapsis_ms": v_peri,
            "theta_asymptote_rad": theta_inf,
        }

    # ── §7.5  Lambert's problem (two-point boundary) ──────────────────────────
    def lambert_dv(self, r1_vec: np.ndarray, r2_vec: np.ndarray,
                   tof_s: float, short_way: bool = True) -> Dict[str, float]:
        """
        Lambert problem: find Δv to go from r1 to r2 in time tof [10].
        Uses Izzo's universal variable method (simplified here).
        Returns approximate Δv magnitudes.
        """
        r1 = np.linalg.norm(r1_vec)
        r2 = np.linalg.norm(r2_vec)
        # Angle between vectors
        cos_dnu = np.dot(r1_vec, r2_vec)/(r1*r2)
        cos_dnu = max(-1, min(1, cos_dnu))
        dnu     = math.acos(cos_dnu)
        # Approximate: use Hohmann as proxy for short transfers
        a_min   = 0.5*(r1 + r2)
        # Minimum energy transfer velocity
        v1_ho   = self.orbital_velocity(r1, a_min)
        v_circ1 = self.orbital_velocity(r1)
        dv_approx = abs(v1_ho - v_circ1)
        return {
            "r1_m": r1, "r2_m": r2, "tof_s": tof_s,
            "delta_nu_rad": dnu, "delta_nu_deg": math.degrees(dnu),
            "dv_estimate_ms": dv_approx,
            "a_minimum_m": a_min,
        }

    # ── §7.6  Lagrange points ─────────────────────────────────────────────────
    def lagrange_L1(self, m_secondary: float, a_secondary: float) -> float:
        """L1 distance from primary: r_L1 ≈ a(m/(3M))^{1/3}"""
        return a_secondary * (m_secondary/(3*self.M))**(1/3)

    def lagrange_L2(self, m_secondary: float, a_secondary: float) -> float:
        """L2 distance from secondary (outside): r_L2 ≈ a(m/(3M))^{1/3}"""
        return a_secondary + a_secondary*(m_secondary/(3*self.M))**(1/3)


# ══════════════════════════════════════════════════════════════════════════════
# §8  MISSION TRAJECTORY PLANNER
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class TrajectoryLeg:
    """A single leg of the Endurance mission."""
    name:          str
    maneuver:      ManeuverType
    dv_ms:         float           # Δv for this leg [m/s]
    duration_days: float           # travel time [days]
    r_start_m:     float = 0.0
    r_end_m:       float = 0.0
    fuel_fraction: float = 0.0    # propellant fraction used
    notes:         str   = ""

    @property
    def dv_kms(self) -> float:
        return self.dv_ms / 1e3


class MissionTrajectoryPlanner:
    """
    Full Endurance mission trajectory: Earth → Saturn → Wormhole →
    Gargantua system → Miller/Mann/Edmunds → Plan B delivery.
    Includes Δv budgets, travel times, and fuel accounting.
    """

    G_EARTH = G_SI * M_EARTH

    def __init__(self,
                 Isp_s: float = ENDURANCE_ISP_S,
                 m_total_kg: float = ENDURANCE_MASS_KG):
        self.Isp     = Isp_s
        self.g0      = 9.80665
        self.m_total = m_total_kg
        self.orb_sun = OrbitalMechanics(M_SUN)
        self.orb_garg= OrbitalMechanics(GARG_MASS_KG)

    def tsiolkovsky(self, dv_ms: float, m_initial_kg: float) -> Dict[str, float]:
        """
        Tsiolkovsky rocket equation:
          Δv = Isp·g₀·ln(m₀/m_f)  →  m_f = m₀·exp(−Δv/(Isp·g₀))
        Returns propellant mass and final mass.
        """
        v_e    = self.Isp * self.g0      # effective exhaust velocity [m/s]
        m_f    = m_initial_kg * math.exp(-dv_ms/v_e)
        m_prop = m_initial_kg - m_f
        return {"m_initial": m_initial_kg, "m_final": m_f,
                "m_propellant": m_prop,
                "mass_fraction": m_prop/m_initial_kg,
                "payload_fraction": m_f/m_initial_kg}

    def earth_to_saturn_trajectory(self) -> Dict[str, Any]:
        """
        Earth → Saturn direct Hohmann transfer (simplified).
        Actual: gravity assist via Venus+Jupiter (Cassini-Huygens type).
        Here: direct Hohmann for clear Δv estimate.
        """
        r_earth  = EARTH_SMA_M
        r_saturn = SAT_SMA_M
        hoh      = self.orb_sun.hohmann_transfer(r_earth, r_saturn)
        # Add Earth escape Δv
        v_esc_earth = self.orb_sun.escape_velocity(r_earth)
        v_park_earth= self.orb_sun.orbital_velocity(r_earth + 400e3)   # 400 km LEO
        dv_escape   = abs(math.sqrt(v_park_earth**2 + hoh['v_periapsis_ms']**2
                                     - v_esc_earth**2) - v_park_earth)
        total_dv = hoh["dv_total_ms"] + dv_escape
        fuel = self.tsiolkovsky(total_dv, self.m_total)
        return {
            **hoh,
            "dv_earth_escape_ms":   dv_escape,
            "total_dv_ms":          total_dv,
            "total_dv_kms":         total_dv/1e3,
            "transfer_time_yr":     hoh["transfer_time_days"]/365.25,
            "fuel":                 fuel,
        }

    def saturn_to_wormhole(self) -> Dict[str, Any]:
        """
        Saturn orbit → wormhole (located ~1 AU from Saturn in film canon).
        Short transfer within Saturn system / nearby space.
        """
        r_sat_orbit = R_SAT + 100e3   # low Saturn orbit
        r_worm      = WORM_SAT_DIST_M
        # Hohmann in Saturn's gravity well (approximate)
        orb_sat = OrbitalMechanics(M_SAT)
        hoh_sat = orb_sat.hohmann_transfer(r_sat_orbit, r_worm)
        fuel    = self.tsiolkovsky(hoh_sat["dv_total_ms"], self.m_total * 0.7)
        return {
            **hoh_sat,
            "transfer_time_hr":  hoh_sat["transfer_time_days"]*24,
            "fuel":              fuel,
        }

    def wormhole_transit(self, wormhole: WormholeGeometry,
                          v_transit: float = 0.1*C_SI) -> Dict[str, Any]:
        """
        Transit through wormhole. Effectively instantaneous in Earth frame
        (wormhole connects to Gargantua system far away).
        No Δv required during transit (free-fall through wormhole).
        """
        traversal = WormholeTraversalCalculator(wormhole)
        profile   = traversal.interstellar_wormhole_profile()
        return {
            **profile,
            "dv_required_ms": 0.0,   # free fall through wormhole
            "notes": "No propulsive Δv inside wormhole (free-fall)"
        }

    def gargantua_orbit_insertion(self, r_park_rs: float = 10.0) -> Dict[str, Any]:
        """
        Capture into Gargantua parking orbit after wormhole exit.
        Approach at v_∞ ~ few km/s; capture burn at periapsis.
        """
        r_s   = GARG_RS
        r_p   = r_park_rs * r_s
        v_inf = 5e3   # 5 km/s approach v_∞ (arbitrary)
        v_peri= math.sqrt(v_inf**2 + 2*G_SI*GARG_MASS_KG/r_p)
        v_c   = self.orb_garg.orbital_velocity(r_p)
        dv    = abs(v_peri - v_c)
        fuel  = self.tsiolkovsky(dv, self.m_total * 0.55)
        return {
            "r_parking_rs": r_park_rs,
            "r_parking_m":  r_p,
            "v_inf_ms":     v_inf,
            "v_periapsis_ms": v_peri,
            "v_circular_ms":  v_c,
            "dv_capture_ms":  dv,
            "dv_capture_kms": dv/1e3,
            "fuel":           fuel,
            "orbital_period_hr": self.orb_garg.orbital_period(r_p)/HOUR_S,
        }

    def miller_approach(self) -> Dict[str, Any]:
        """
        Descent from parking orbit to Miller's World near-ISCO orbit.
        Miller is at r_isco × (1 + 10⁻⁶) — essentially at ISCO.
        """
        a   = GARG_SPIN
        Z1  = 1+(1-a**2)**(1/3)*((1+a)**(1/3)+(1-a)**(1/3))
        Z2  = math.sqrt(3*a**2+Z1**2)
        r_isco_M = (3+Z2-math.sqrt((3-Z1)*(3+Z1+2*Z2))) * GARG_M_GEO
        r_park   = 10.0 * GARG_RS
        r_miller = r_isco_M * (1+1e-5)
        v_park   = self.orb_garg.orbital_velocity(r_park)
        v_miller = math.sqrt(G_SI*GARG_MASS_KG/r_miller)   # Keplerian approx
        dv_total = abs(v_miller - v_park)
        # Time dilation at Miller
        dtr = math.sqrt(max(0, 1-3*GARG_M_GEO/r_miller+2*GARG_SPIN*
                             math.sqrt(GARG_M_GEO/r_miller**3)))
        fuel = self.tsiolkovsky(dv_total, self.m_total * 0.50)
        return {
            "r_parking_m":    r_park,
            "r_miller_m":     r_miller,
            "r_isco_m":       r_isco_M,
            "v_parking_ms":   v_park,
            "v_miller_ms":    v_miller,
            "dv_ms":          dv_total,
            "dv_kms":         dv_total/1e3,
            "dilation_dtr":   dtr,
            "dilation_factor":1/max(dtr,1e-10),
            "earth_yr_per_ship_hr": HOUR_S/(dtr*YEAR_S) if dtr > 0 else 61320,
            "fuel":           fuel,
        }

    def gargantua_slingshot_plan(self) -> Dict[str, Any]:
        """
        Gargantua gravity slingshot for exit trajectory to Plan B planet.
        Designed to Δv ~10 km/s toward Edmunds via close flyby of Gargantua.
        """
        orb = OrbitalMechanics(M_SUN)
        r_peri_rs = 1.5   # 1.5 Schwarzschild radii
        v_inf_in  = 3e3   # approach v_∞ 3 km/s
        sling = self.orb_garg.gargantua_slingshot(r_peri_rs, v_inf_in)
        fuel  = self.tsiolkovsky(500.0, self.m_total * 0.35)   # small correction burn
        return {**sling, "fuel": fuel}

    def full_dv_budget(self) -> pd.DataFrame:
        """
        Complete Δv budget for ENDURANCE mission, leg by leg.
        """
        legs = [
            TrajectoryLeg("Earth LEO → Saturn",
                          ManeuverType.HOHMANN, 11_200.0, 2.0*365.25,
                          EARTH_SMA_M, SAT_SMA_M, notes="Hohmann + escape burn"),
            TrajectoryLeg("Saturn orbit → Wormhole approach",
                          ManeuverType.DIRECT, 2_800.0, 30.0,
                          R_SAT, WORM_SAT_DIST_M, notes="Short transfer in Saturn vicinity"),
            TrajectoryLeg("Wormhole transit",
                          ManeuverType.DIRECT, 0.0, 0.083,   # ~2 hours
                          0.0, 0.0, notes="Free-fall; no Δv inside wormhole"),
            TrajectoryLeg("Wormhole exit → Gargantua parking orbit",
                          ManeuverType.DIRECT, 4_200.0, 14.0,
                          0.0, 10*GARG_RS, notes="Capture burn at periapsis"),
            TrajectoryLeg("Parking orbit → Miller's World",
                          ManeuverType.SPIRAL_ION, 8_500.0, 90.0,
                          10*GARG_RS, GARG_M_GEO*(1+1e-5), notes="Near-ISCO spiral descent"),
            TrajectoryLeg("Miller departure → Mann's Planet",
                          ManeuverType.DIRECT, 3_100.0, 180.0,
                          GARG_M_GEO, 1.3*AU, notes="Climb out of gravity well"),
            TrajectoryLeg("Mann's Planet → Gargantua slingshot",
                          ManeuverType.GRAVITY_ASSIST, 500.0, 60.0,
                          1.3*AU, 10*GARG_RS, notes="Use Gargantua to boost speed"),
            TrajectoryLeg("Gargantua → Edmunds' Planet (Plan B)",
                          ManeuverType.DIRECT, 2_800.0, 120.0,
                          10*GARG_RS, 0.88*AU, notes="TARS data crystal trajectory"),
        ]
        m_current = self.m_total
        rows = []
        cum_dv = 0.0
        cum_t  = 0.0
        for leg in legs:
            fuel  = self.tsiolkovsky(leg.dv_ms, m_current)
            m_prop= fuel["m_propellant"]
            m_current -= m_prop
            cum_dv += leg.dv_ms
            cum_t  += leg.duration_days
            rows.append({
                "Leg":                leg.name,
                "Maneuver":           leg.maneuver.value[:18],
                "Δv (m/s)":          round(leg.dv_ms, 1),
                "Δv (km/s)":         round(leg.dv_ms/1e3, 2),
                "Duration (days)":    round(leg.duration_days, 1),
                "Propellant (kg)":    round(m_prop, 1),
                "Ship mass after (kg)": round(m_current, 1),
                "Cumulative Δv (m/s)": round(cum_dv, 1),
                "Cumulative time (days)": round(cum_t, 1),
                "Notes":              leg.notes,
            })
        return pd.DataFrame(rows)

    def planet_orbital_data(self) -> pd.DataFrame:
        """Orbital parameters for each planet in the Gargantua system."""
        rows = []
        planets = [
            ("Miller's World",  1.0e-5*GARG_RS, 0.0,   3.22/HOUR_S*YEAR_S),
            ("Mann's Planet",   1.3*AU,          0.07,  None),
            ("Edmunds' Planet", 0.88*AU,         0.04,  None),
        ]
        for name, a, e, period_yr in planets:
            v_c  = self.orb_garg.orbital_velocity(a) if a > 0 else 0.0
            T_yr = (self.orb_garg.orbital_period(a)/YEAR_S if a > 0 and period_yr is None
                    else period_yr)
            rows.append({
                "Planet":           name,
                "SMA (m)":          a,
                "SMA (AU)":         a/AU,
                "Eccentricity":     e,
                "Period (yr)":      round(T_yr, 4) if T_yr else "N/A",
                "v_circular (m/s)": round(v_c, 1),
                "v_circular (km/s)":round(v_c/1e3, 3),
            })
        return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# §8A  MORRIS-THORNE GEODESIC INTEGRATOR — 3D Null & Timelike Trajectories
# ══════════════════════════════════════════════════════════════════════════════
class MorrisThorneGeodesics:
    """
    Solves 3D geodesic equations for rays (photons) and particles
    traversing a traversable wormhole (Morris & Thorne 1988).
    
    Metric: ds² = -e^(2Φ(r)) dt² + dr² / (1 - b(r)/r) + r² dΩ²
    Uses Hamilton-Jacobi formalism with conserved quantities E, L.
    
    Integrates coordinates (t, r, φ) with respect to affine parameter λ 
    (or proper time τ) through the throat (r = b0).
    """
    
    def __init__(self, b0: float = WORM_THROAT_M, shape_param: float = 1.0):
        self.b0 = b0
        self.b_exponent = shape_param  # b(r) = b0 * (b0/r)^gamma
        
    def b(self, r: float) -> float:
        """Shape function."""
        # Standard Ellis-type generalisation
        return self.b0 * (self.b0 / max(r, self.b0))**self.b_exponent
        
    def Phi(self, r: float) -> float:
        """Redshift function. Assume zero for traversability (no horizons)."""
        return 0.0
        
    def _ode_system(self, p: float, y: np.ndarray, L: float, is_null: bool) -> np.ndarray:
        """
        Geodesic equations in equatorial plane (θ=π/2).
        y = [t, l, phi], where l is proper radial distance.
        r(l) is obtained by integrating dl = dr / sqrt(1 - b(r)/r).
        To avoid coordinate singularity at throat, we integrate w.r.t l.
        """
        t, l, phi = y
        # Reconstruct r from l (approximate for Ellis: r = sqrt(l^2 + b0^2))
        r = math.sqrt(l**2 + self.b0**2) 
        
        # Conserved E (energy) = 1.0 for simplicity
        E = 1.0
        
        kappa = 0.0 if is_null else 1.0
        
        # dr/dp from E, L conservation
        # E^2 = e^(2Φ) * (kappa + (dr/dp)^2 / (1-b/r) + L^2/r^2)
        # We use l instead of r: dl/dp = sqrt(E^2 e^{-2Φ} - kappa - L^2/r^2)
        V_eff = math.exp(2 * self.Phi(r)) * (kappa + L**2 / r**2)
        dl_dp_sq = E**2 - V_eff
        
        if dl_dp_sq < 0:
            dl_dp = 0.0  # Turning point
        else:
            # Sign depends on direction (assume inbound then outbound)
            dl_dp = math.sqrt(dl_dp_sq) if l >= 0 else -math.sqrt(dl_dp_sq)
            
        dt_dp = E * math.exp(-2 * self.Phi(r))
        dphi_dp = L / r**2
        
        return np.array([dt_dp, dl_dp, dphi_dp])

    def integrate_ray(self, b_impact: float, l_start: float = 100.0, 
                      is_null: bool = True, steps: int = 1000) -> Dict[str, np.ndarray]:
        """
        Integrate a ray with impact parameter b_impact.
        L = b_impact * E.
        """
        L = b_impact
        y0 = np.array([0.0, -l_start * self.b0, 0.0])  # Start far away, l < 0
        p_max = 2.0 * l_start * self.b0  # Affine parameter max
        
        sol = sci_int.solve_ivp(
            self._ode_system, (0, p_max), y0,
            args=(L, is_null), method='RK45', 
            dense_output=True, max_step=p_max/200)
            
        p_eval = np.linspace(0, sol.t[-1], steps)
        y_eval = sol.sol(p_eval)
        
        t_arr = y_eval[0]
        l_arr = y_eval[1]
        phi_arr = y_eval[2]
        
        r_arr = np.sqrt(l_arr**2 + self.b0**2)
        
        return {
            "p": p_eval,
            "t": t_arr,
            "l": l_arr,
            "r": r_arr,
            "phi": phi_arr,
            "x": r_arr * np.cos(phi_arr),
            "y": r_arr * np.sin(phi_arr)
        }

# ══════════════════════════════════════════════════════════════════════════════
# §8B  FLAMM'S PARABOLOID EMBEDDING — Differential Geometry
# ══════════════════════════════════════════════════════════════════════════════
class FlammsParaboloid:
    """
    Computes the 3D embedding diagram of the wormhole spatial slice (t=const, θ=π/2).
    The metric is ds² = dr² / (1 - b(r)/r) + r² dφ².
    We embed this in 3D Euclidean space: ds² = dz² + dr² + r² dφ².
    Equating the two: dz/dr = ± sqrt( b(r) / (r - b(r)) ).
    """
    
    def __init__(self, b0: float = WORM_THROAT_M, shape_func: str = "Ellis"):
        self.b0 = b0
        self.shape_func = shape_func
        
    def b(self, r: float) -> float:
        if self.shape_func == "Ellis":
            return self.b0**2 / r
        elif self.shape_func == "Morris-Thorne":
            return math.sqrt(self.b0 * r)
        else: # Standard
            return self.b0
            
    def dz_dr(self, r: float) -> float:
        """Embedding slope."""
        br = self.b(r)
        if r <= br: return 1e6 # Avoid singularity
        return math.sqrt(br / (r - br))
        
    def compute_embedding(self, r_max: float, n_pts: int = 500) -> Dict[str, np.ndarray]:
        """Integrate dz/dr to find z(r)."""
        r_arr = np.linspace(self.b0 * 1.0001, r_max, n_pts)
        z_arr = np.zeros(n_pts)
        
        for i in range(1, n_pts):
            dr = r_arr[i] - r_arr[i-1]
            r_mid = 0.5 * (r_arr[i] + r_arr[i-1])
            z_arr[i] = z_arr[i-1] + self.dz_dr(r_mid) * dr
            
        # Symmetrize for upper and lower universes
        r_full = np.concatenate((r_arr[::-1], r_arr))
        z_full = np.concatenate((z_arr[::-1], -z_arr))
        
        return {
            "r": r_full,
            "z": z_full,
            "r_throat": self.b0
        }

# ══════════════════════════════════════════════════════════════════════════════
# §8C  EXOTIC MATTER & ENERGY CONDITIONS ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
class EnergyConditionAnalyzer:
    """
    Calculates the Stress-Energy Tensor components (ρ, τ, p) required to sustain
    the wormhole geometry, and evaluates energy condition violations.
    
    Einstein Field Equations: G_μν = (8πG/c⁴) T_μν
    ρ: Energy density
    τ: Radial tension (negative radial pressure)
    p: Lateral pressure
    
    Violation of Null Energy Condition (NEC): ρ - τ < 0
    This implies "exotic matter" with negative energy density or extreme tension.
    """
    
    def __init__(self, b0: float = WORM_THROAT_M):
        self.b0 = b0
        self.kappa = 8.0 * math.pi * G_SI / C_SI**4
        
    def stress_energy(self, r: float, b_val: float, b_prime: float) -> Dict[str, float]:
        """Compute ρ, τ, p in physical units (J/m³ or Pa)."""
        if r <= 0: return {"rho": 0, "tau": 0, "p": 0}
        
        # From Morris & Thorne 1988, Eq 13-15 (assuming Φ = 0 for simplicity)
        rho_geom = b_prime / (8.0 * math.pi * r**2)
        tau_geom = b_val / (8.0 * math.pi * r**3)
        p_geom   = (b_val - r * b_prime) / (16.0 * math.pi * r**3)
        
        # Convert from geometric to SI
        conversion = C_SI**4 / G_SI
        return {
            "rho": rho_geom * conversion,
            "tau": tau_geom * conversion,
            "p":   p_geom * conversion,
            "nec_violation": (rho_geom - tau_geom) * conversion
        }
        
    def total_exotic_mass(self, r_max: float) -> float:
        """
        Integrate the exotic mass violation over the wormhole volume.
        M_exotic = \int (ρ - τ) dV
        Returns negative mass equivalent in kg.
        """
        # For b(r) = b0^2 / r, rho - tau is always negative
        # Analytic integral for Ellis wormhole:
        # M_ex = - b0 / (2G/c^2)
        return - self.b0 / (2.0 * G_SI / C_SI**2)


# ══════════════════════════════════════════════════════════════════════════════
# §9  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    D: Dict[str, Any] = {
        "wh_geometry":       WormholeGeometry(WORM_THROAT_M, ShapeFunction.ELLIS),
        "wh_throat_km":      WORM_THROAT_M/1e3,
        "wh_shape":          ShapeFunction.ELLIS.name,
        "wh_redshift":       RedshiftFunction.ZERO.name,
        "wh_alpha":          0.5,
        "wh_embed_data":     None,
        "wh_traversal":      None,
        "wh_exotic_report":  None,
        "wh_tidal_profile":  None,
        "orb_planner":       MissionTrajectoryPlanner(),
        "orb_dv_budget":     None,
        "orb_earth_sat":     None,
        "orb_garg_sling":    None,
        "orb_miller":        None,
        "orb_r_park":        10.0,
        "orb_v_inf":         3000.0,
        "orb_flyby_mass":    GARG_MASS_KG,
        "orb_r_peri":        1.5,
        "wh_v_transit_c":    0.10,
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# §10  MATPLOTLIB STYLE
# ══════════════════════════════════════════════════════════════════════════════
MPL_STYLE = {
    "figure.facecolor":  "#05080f",
    "axes.facecolor":    "#070a16",
    "axes.edgecolor":    "#121c35",
    "axes.labelcolor":   "#E8C46A",
    "axes.grid":         True,
    "grid.color":        "#0c1225",
    "grid.linestyle":    ":",
    "grid.alpha":        0.55,
    "xtick.color":       "#364070",
    "ytick.color":       "#364070",
    "xtick.labelsize":   6,
    "ytick.labelsize":   6,
    "axes.labelsize":    7,
    "axes.titlesize":    8,
    "axes.titlecolor":   "#E8C46A",
    "text.color":        "#E8C46A",
    "font.family":       "monospace",
    "legend.facecolor":  "#070a16",
    "legend.edgecolor":  "#121c35",
    "legend.fontsize":   6,
    "figure.dpi":        110,
    "savefig.facecolor": "#05080f",
    "axes.spines.top":   False,
    "axes.spines.right": False,
}
def _mpl(): plt.rcParams.update(MPL_STYLE)


# ══════════════════════════════════════════════════════════════════════════════
# §11  PLOTTING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

# ── §11.1  Wormhole embedding diagram ─────────────────────────────────────────
def _plot_embedding(wh: WormholeGeometry) -> plt.Figure:
    _mpl()
    fig = plt.figure(figsize=(15, 7))
    gs  = gridspec.GridSpec(1, 3, figure=fig, wspace=0.38)

    ax1 = fig.add_subplot(gs[0, :2])
    # 2D embedding (cross-section)
    r_arr, l_arr, z_arr = wh.embedding_surface(r_max_b0=7.0, n_r=300)
    r_m   = r_arr/wh.b0    # normalised
    z_u   =  z_arr/wh.b0   # upper universe
    z_l   = -z_arr/wh.b0   # lower universe

    # Fill upper / lower sheets
    ax1.fill_between(r_m,  z_u,  0, alpha=0.12, color="#8060ff")
    ax1.fill_between(r_m,  z_l,  0, alpha=0.12, color="#4020e0")
    ax1.plot( r_m,  z_u, color="#8060ff", lw=1.5, label="Upper universe")
    ax1.plot( r_m,  z_l, color="#4020e0", lw=1.5, label="Lower universe")
    # Mirror for negative x
    ax1.fill_between(-r_m, z_u, 0, alpha=0.12, color="#8060ff")
    ax1.fill_between(-r_m, z_l, 0, alpha=0.12, color="#4020e0")
    ax1.plot(-r_m,  z_u, color="#8060ff", lw=1.5)
    ax1.plot(-r_m,  z_l, color="#4020e0", lw=1.5)
    # Throat
    ax1.axvline(-1.0, color="#CE93D8", lw=0.7, ls=":", alpha=0.5)
    ax1.axvline(+1.0, color="#CE93D8", lw=0.7, ls=":", alpha=0.5)
    ax1.annotate("Throat b₀", xy=(1.0, 0.5), color="#CE93D8",
                 fontsize=7, ha="left")
    ax1.annotate("Our Universe ↑", xy=(3.0, 1.2), color="#8060ff",
                 fontsize=7, style="italic")
    ax1.annotate("Far Universe ↓", xy=(3.0, -1.4), color="#4020e0",
                 fontsize=7, style="italic")
    ax1.set_xlabel("r / b₀  (embedding radial coordinate)")
    ax1.set_ylabel("z / b₀  (embedding height)")
    ax1.set_title(f"WORMHOLE EMBEDDING DIAGRAM — {wh.shape_type.value[:35]}\n"
                  f"b₀ = {wh.b0/1e3:.1f} km  ·  Redshift: {wh.redshift_type.value[:20]}")
    ax1.legend(fontsize=6, loc="upper right")
    ax1.set_facecolor("#040810")
    ax1.set_xlim(-8, 8); ax1.set_ylim(-3, 3)

    # Right: shape function
    ax2 = fig.add_subplot(gs[0, 2])
    r_plot = np.geomspace(wh.b0, 8*wh.b0, 300) / wh.b0
    b_vals = np.array([wh.b(r*wh.b0)/wh.b0 for r in r_plot])
    ax2.plot(r_plot, b_vals, color="#CE93D8", lw=1.3, label="b(r)/b₀")
    ax2.plot(r_plot, r_plot, color="#3a4a70", lw=0.7, ls="--", label="b=r (flat)")
    # Flaring condition b' < 1
    bp_arr = np.array([wh.b_prime(r*wh.b0, wh.b0*0.001) for r in r_plot])
    ax2.plot(r_plot, bp_arr, color="#81C784", lw=0.8, ls=":",
             label="b'(r)")
    ax2.axhline(1.0, color="#D154FF", lw=0.6, ls="--",
                label="Flaring limit b'=1")
    ax2.set_xlabel("r / b₀"); ax2.set_ylabel("b(r)/b₀  or  b'(r)")
    ax2.set_title("SHAPE FUNCTION b(r)\n& Flaring-out condition")
    ax2.legend(fontsize=6)
    fig.patch.set_facecolor("#05080f")
    plt.tight_layout()
    return fig


# ── §11.2  Exotic matter & traversal ──────────────────────────────────────────
def _plot_exotic_traversal(wh: WormholeGeometry) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.patch.set_facecolor("#05080f")

    # 1. Energy density ρ(r)
    ax1 = axes[0,0]
    r_arr_b0 = np.geomspace(1.001, 8.0, 200)
    rho_arr  = np.array([wh.stress_energy_tensor(r*wh.b0)["rho_kg_m3"]
                          for r in r_arr_b0])
    ax1.semilogy(r_arr_b0, np.abs(rho_arr)+1e-40, color="#CE93D8", lw=1.2)
    ax1.set_xlabel("r / b₀"); ax1.set_ylabel("|ρ_exotic|  [kg/m³]")
    ax1.set_title("EXOTIC ENERGY DENSITY |ρ(r)|")
    ax1.set_facecolor("#070a16")

    # 2. Radial tension τ(r)
    ax2 = axes[0,1]
    tau_arr = np.array([wh.stress_energy_tensor(r*wh.b0)["radial_tension_Pa"]
                         for r in r_arr_b0])
    ax2.semilogy(r_arr_b0, np.abs(tau_arr)+1e-30, color="#4FC3F7", lw=1.2)
    ax2.set_xlabel("r / b₀"); ax2.set_ylabel("|τ(r)|  [Pa]")
    ax2.set_title("RADIAL TENSION τ(r)")
    ax2.set_facecolor("#070a16")

    # 3. Exotic mass vs throat radius
    ax3 = axes[0,2]
    b0_arr  = np.logspace(3, 12, 40)   # 1 km to 10,000 km
    M_ex_arr= []
    for b0 in b0_arr:
        wh_tmp = WormholeGeometry(b0, wh.shape_type)
        M_ex_arr.append(wh_tmp.exotic_mass_total())
    M_ex_arr = np.array(M_ex_arr)
    ax3.loglog(b0_arr/1e3, M_ex_arr/M_JUPITER, color="#E8C46A", lw=1.2,
               label="M_exotic/M_Jupiter")
    ax3.loglog(b0_arr/1e3, M_ex_arr/M_SUN, color="#FF8800", lw=1.0, ls="--",
               label="M_exotic/M_Sun")
    ax3.axvline(wh.b0/1e3, color="#D154FF", lw=0.8, ls="--",
                label=f"Current b₀={wh.b0/1e3:.0f}km")
    ax3.set_xlabel("b₀ [km]"); ax3.set_ylabel("Exotic mass / reference")
    ax3.set_title("EXOTIC MASS SCALING vs THROAT RADIUS")
    ax3.legend(fontsize=5.5)

    # 4. Tidal force profile through wormhole
    ax4 = axes[1,0]
    trav = WormholeTraversalCalculator(wh)
    l_a, tidal_r, tidal_l = trav.tidal_force_profile(n_l=200)
    ax4.semilogy(l_a/wh.b0, tidal_r+1e-30, color="#D154FF", lw=1.2,
                 label="Radial tidal [g/m]")
    ax4.semilogy(l_a/wh.b0, tidal_l+1e-30, color="#4FC3F7", lw=1.0, ls="--",
                 label="Lateral tidal [g/m]")
    ax4.axhline(10.0, color="#E8C46A", lw=0.7, ls=":", label="10g/m (hazardous)")
    ax4.set_xlabel("l / b₀  (proper distance from throat)")
    ax4.set_ylabel("Tidal acceleration [g/m]")
    ax4.set_title("TIDAL FORCE ALONG WORMHOLE")
    ax4.legend(fontsize=6)

    # 5. Transit time vs traversal speed
    ax5 = axes[1,1]
    v_arr_c  = np.linspace(0.01, 0.99, 200)
    tau_arr2 = [trav.transit_time_traveller(v*C_SI)/HOUR_S for v in v_arr_c]
    ax5.plot(v_arr_c, tau_arr2, color="#81C784", lw=1.3)
    ax5.axhline(24.0, color="#FFB74D", lw=0.7, ls="--",
                label="24 hours")
    ax5.axhline(1.0, color="#81C784", lw=0.7, ls=":",
                label="1 hour")
    ax5.set_xlabel("Traversal speed  v/c")
    ax5.set_ylabel("Proper transit time  [hours]")
    ax5.set_title(f"TRANSIT TIME vs SPEED\nb₀={wh.b0/1e3:.0f} km")
    ax5.legend(fontsize=6)

    # 6. Casimir energy comparison
    ax6 = axes[1,2]
    d_arr    = np.logspace(-9, 0, 200)    # plate sep: 1 nm to 1 m
    rho_cas  = np.abs([ExoticMatterPhysics(wh).casimir_energy_density(d)
                        for d in d_arr])
    qi_bound = np.abs([ExoticMatterPhysics(wh).quantum_inequality_bound(1e-12/d)
                        for d in d_arr])  # tau ∝ d/c
    ax6.loglog(d_arr*1e9, rho_cas, color="#CE93D8", lw=1.3,
               label="Casimir |ρ| [J/m³]")
    ax6.loglog(d_arr*1e9, qi_bound, color="#E8C46A", lw=1.0, ls="--",
               label="QI bound")
    ax6.set_xlabel("Plate separation [nm]")
    ax6.set_ylabel("Energy density [J/m³]")
    ax6.set_title("CASIMIR ENERGY vs PLATE SEPARATION\n& Quantum Inequality")
    ax6.legend(fontsize=6)

    plt.tight_layout()
    return fig


# ── §11.3  Mission trajectory overview ────────────────────────────────────────
def _plot_mission_trajectory(planner: MissionTrajectoryPlanner) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.patch.set_facecolor("#05080f")

    # 1. Solar system layout
    ax1 = axes[0,0]
    ax1.set_facecolor("#020408")
    # Sun
    ax1.scatter([0],[0], color="#FFD700", s=200, zorder=5)
    ax1.annotate("☉", (0,0), color="#FFD700", fontsize=10, ha="center", va="center")
    # Orbits
    for r_au, name, clr in [(1.0,"Earth","#4FC3F7"),
                              (9.537,"Saturn","#CE93D8"),
                              (9.537+1.0,"Wormhole","#8060ff")]:
        theta = np.linspace(0, 2*math.pi, 300)
        ax1.plot(r_au*np.cos(theta), r_au*np.sin(theta),
                 color=clr, lw=0.5, alpha=0.3)
        ax1.scatter([r_au], [0], color=clr, s=60, zorder=5)
        ax1.annotate(name, (r_au, 0.5), color=clr, fontsize=6)
    # Hohmann arc
    r_E = 1.0; r_S = 9.537
    a_ho = (r_E+r_S)/2
    theta_ho = np.linspace(0, math.pi, 200)
    r_ho_arr = a_ho*(1-(a_ho-r_E)**2/a_ho**2) / (1-((a_ho-r_E)/a_ho)*np.cos(theta_ho))
    # Simple ellipse
    x_ho = (r_E+r_S)/2 * np.cos(theta_ho) - (r_S-r_E)/2
    y_ho = math.sqrt(r_E*r_S) * np.sin(theta_ho)
    ax1.plot(x_ho, y_ho, color="#E8C46A", lw=1.2, ls="--", label="Hohmann transfer")
    ax1.set_xlim(-12, 12); ax1.set_ylim(-8, 8)
    ax1.set_aspect("equal"); ax1.set_xlabel("x [AU]"); ax1.set_ylabel("y [AU]")
    ax1.set_title("EARTH → SATURN → WORMHOLE TRAJECTORY"); ax1.legend(fontsize=6)

    # 2. Gargantua system
    ax2 = axes[0,1]
    ax2.set_facecolor("#020408")
    ax2.scatter([0],[0], color="#FF8800", s=400, zorder=5)
    ax2.annotate("GARGANTUA", (0.2,0), color="#FF8800", fontsize=6)
    r_s_au = (GARG_RS/AU)*1e6   # Schwarzschild radius scaled for plot
    for r_plot, name, clr in [(0.5,"Photon sphere","#CE93D8"),
                               (1.0,"ISCO","#4FC3F7"),
                               (5.0,"Endurance park","#81C784"),
                               (50.0,"Miller's World","#E8C46A")]:
        theta = np.linspace(0, 2*math.pi, 300)
        ax2.plot(r_plot*np.cos(theta), r_plot*np.sin(theta),
                 color=clr, lw=0.6, alpha=0.5)
        ax2.scatter([r_plot],[0], color=clr, s=40, zorder=5)
        ax2.annotate(name, (r_plot, r_plot*0.15), color=clr, fontsize=5)
    ax2.set_xlim(-80, 80); ax2.set_ylim(-80, 80)
    ax2.set_aspect("equal")
    ax2.set_xlabel("r [arbitrary geometric units]")
    ax2.set_title("GARGANTUA SYSTEM — ORBITAL SCHEMATIC")

    # 3. Δv budget bar chart
    ax3 = axes[1,0]
    df = planner.full_dv_budget()
    legs    = [l[:20] for l in df["Leg"].values]
    dvs     = df["Δv (m/s)"].values
    colors3 = plt.cm.plasma(np.linspace(0.1, 0.9, len(legs)))
    bars    = ax3.bar(range(len(legs)), dvs/1e3, color=colors3, alpha=0.85)
    ax3.set_xticks(range(len(legs)))
    ax3.set_xticklabels(legs, rotation=45, ha="right", fontsize=5.5)
    ax3.set_ylabel("Δv  [km/s]")
    ax3.set_title(f"ENDURANCE Δv BUDGET — Total {df['Δv (m/s)'].sum()/1e3:.1f} km/s")
    ax3.bar_label(bars, fmt="%.1f", padding=2, fontsize=5.5, color="#fff")

    # 4. Ship mass through mission
    ax4 = axes[1,1]
    mass_arr = df["Ship mass after (kg)"].values
    cum_t    = df["Cumulative time (days)"].values
    ax4.plot(cum_t, mass_arr/1e3, color="#E8C46A", lw=1.5, marker="o", ms=5)
    ax4.fill_between(cum_t, mass_arr/1e3, 0, alpha=0.15, color="#E8C46A")
    for i, (t, m, leg) in enumerate(zip(cum_t, mass_arr/1e3,
                                         df["Leg"].values)):
        ax4.annotate(leg[:12], (t, m+2), fontsize=4.5,
                     color="#E8C46A", rotation=30)
    ax4.set_xlabel("Mission elapsed time [days]")
    ax4.set_ylabel("Endurance mass [tonnes]")
    ax4.set_title("SHIP MASS EVOLUTION (propellant expenditure)")

    plt.tight_layout()
    return fig


# ── §11.4  Gravity assist ──────────────────────────────────────────────────────
def _plot_gravity_assist(planner: MissionTrajectoryPlanner,
                          v_inf: float, r_peri_rs: float) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#05080f")

    orb_g = planner.orb_garg
    r_s   = GARG_RS
    r_p   = r_peri_rs * r_s

    hyp   = orb_g.hyperbolic_trajectory(v_inf, r_p, GARG_MASS_KG, n_pts=400)
    sling = orb_g.gargantua_slingshot(r_peri_rs, v_inf)

    # Left: trajectory
    ax1 = axes[0]
    ax1.set_facecolor("#020408")
    scale = r_p
    x_n   = hyp["x"]/scale; y_n = hyp["y"]/scale
    # Color by distance to Gargantua
    r_n   = hyp["r"]/scale
    points= np.array([x_n, y_n]).T.reshape(-1, 1, 2)
    segs  = np.concatenate([points[:-1], points[1:]], axis=1)
    lc    = mcolors.LinearSegmentedColormap.from_list("", ["#8060ff","#E8C46A","#D154FF"])
    from matplotlib.collections import LineCollection as LC
    lc_coll = LC(segs, cmap=lc, norm=plt.Normalize(r_n.min(), r_n.max()))
    lc_coll.set_array(r_n[:-1])
    lc_coll.set_linewidth(1.5)
    ax1.add_collection(lc_coll)
    # Gargantua shadow
    ax1.add_patch(Circle((0,0), r_s/scale, color="#000", zorder=5))
    ax1.add_patch(Circle((0,0), r_s/scale*1.5, fill=False, ec="#FF8800",
                          lw=0.6, ls="--", label="Photon sphere"))
    ax1.add_patch(Circle((0,0), r_peri_rs, fill=False, ec="#E8C46A",
                          lw=0.7, ls=":", label="Periapsis"))
    # Asymptote arrows
    theta_a = hyp["theta_asymptote_rad"]
    for sgn, clr, lbl in [(1, "#4FC3F7","Approach"), (-1, "#81C784","Departure")]:
        ang = sgn * theta_a
        ax1.annotate("", xy=(8*math.cos(ang), 8*math.sin(ang)),
                     xytext=(6*math.cos(ang), 6*math.sin(ang)),
                     arrowprops=dict(arrowstyle="->", color=clr, lw=1.0))
    ax1.set_xlim(-10, 10); ax1.set_ylim(-8, 8)
    ax1.set_aspect("equal")
    ax1.set_xlabel("x / r_periapsis"); ax1.set_ylabel("y / r_periapsis")
    ax1.set_title(f"GARGANTUA SLINGSHOT TRAJECTORY\n"
                  f"r_peri={r_peri_rs:.1f}r_s  v_∞={v_inf/1e3:.1f}km/s")
    ax1.legend(fontsize=5.5)

    # Mid: Δv vs periapsis radius
    ax2 = axes[1]
    rp_arr  = np.linspace(1.1, 20.0, 200)
    dv_arr  = [orb_g.gargantua_slingshot(rp, v_inf)["dv_GR_corrected_ms"]/1e3
               for rp in rp_arr]
    dv_new  = [orb_g.gargantua_slingshot(rp, v_inf)["dv_assist_ms"]/1e3
               for rp in rp_arr]
    ax2.plot(rp_arr, dv_arr, color="#E8C46A", lw=1.3, label="GR-corrected Δv")
    ax2.plot(rp_arr, dv_new, color="#4FC3F7", lw=1.0, ls="--", label="Newtonian Δv")
    ax2.axvline(r_peri_rs, color="#D154FF", lw=0.8, ls=":",
                label=f"Selected r_peri={r_peri_rs:.1f}r_s")
    ax2.set_xlabel("Periapsis radius [r_s]")
    ax2.set_ylabel("Δv from slingshot [km/s]")
    ax2.set_title("SLINGSHOT Δv vs PERIAPSIS DISTANCE")
    ax2.legend(fontsize=6)

    # Right: summary table
    ax3 = axes[2]
    ax3.axis("off")
    items = [
        ("v_∞ approach",       f"{sling['v_inf_ms']/1e3:.2f} km/s"),
        ("r_periapsis",        f"{r_peri_rs:.2f} r_s  =  {r_p/1e3:.1f} km"),
        ("Eccentricity",       f"{sling['eccentricity']:.4f}"),
        ("Deflection angle",   f"{sling['deflection_deg']:.2f}°"),
        ("Δv (Newtonian)",     f"{sling['dv_assist_ms']/1e3:.3f} km/s"),
        ("GR correction ×",    f"{sling['GR_correction']:.4f}"),
        ("Δv (GR corrected)",  f"{sling['dv_GR_kms']:.3f} km/s"),
        ("v at periapsis",     f"{sling['v_periapsis_ms']/1e3:.2f} km/s"),
        ("Time dilation dτ/dt",f"{sling['time_dilation_dtr']:.4e}"),
        ("r_s Gargantua",      f"{GARG_RS/1e3:.3e} km"),
    ]
    y = 0.96
    ax3.text(0.02, y, "GARGANTUA SLINGSHOT REPORT",
             color="#E8C46A", fontsize=8, fontfamily="monospace",
             fontweight="bold", transform=ax3.transAxes)
    y -= 0.09
    for lbl, val in items:
        ax3.text(0.02, y, f"  {lbl:<24}", color="#888", fontsize=7,
                 fontfamily="monospace", transform=ax3.transAxes)
        ax3.text(0.55, y, val, color="#E8C46A", fontsize=7,
                 fontfamily="monospace", transform=ax3.transAxes,
                 fontweight="bold")
        y -= 0.08

    plt.tight_layout()
    return fig


# ── §11.5  Saturn approach to wormhole ────────────────────────────────────────
def _plot_saturn_wormhole(planner: MissionTrajectoryPlanner) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.patch.set_facecolor("#05080f")

    # Left: Saturn system zoom
    ax1 = axes[0]
    ax1.set_facecolor("#020408")
    # Saturn (schematic)
    saturn_ring = mpatches.Ellipse((0,0), 3.2, 0.8, fill=False,
                               ec="#CE93D8", lw=1.0, alpha=0.5)
    ax1.add_patch(saturn_ring)
    ax1.scatter([0],[0], color="#CE93D8", s=200)
    ax1.annotate("Saturn", (0.2, 0.4), color="#CE93D8", fontsize=8)
    # Wormhole location
    worm_x = WORM_SAT_DIST_M/R_SAT * 2   # scaled for visibility
    ax1.scatter([worm_x],[0], color="#8060ff", s=150, marker="*")
    ax1.annotate("Wormhole", (worm_x+0.3, 0.3), color="#8060ff", fontsize=8)
    # Endurance trajectory
    t  = np.linspace(0, 1, 200)
    x_traj = worm_x * t
    y_traj = 0.8*np.sin(math.pi*t)
    ax1.plot(x_traj, y_traj, color="#E8C46A", lw=1.5, ls="--",
             label="Endurance approach")
    # Arrow
    ax1.annotate("", xy=(worm_x*0.95, 0.1), xytext=(worm_x*0.85, 0.3),
                 arrowprops=dict(arrowstyle="->", color="#E8C46A", lw=1.0))
    ax1.set_xlim(-2, worm_x+2); ax1.set_ylim(-2, 2)
    ax1.set_xlabel("Saturn radii"); ax1.set_ylabel("Saturn radii")
    ax1.set_title("SATURN SYSTEM → WORMHOLE APPROACH")
    ax1.legend(fontsize=6)
    ax1.set_aspect("equal")

    # Right: Wormhole cross section (light bending visualization)
    ax2 = axes[1]
    ax2.set_facecolor("#020408")
    b0 = WORM_THROAT_M
    # Draw wormhole cross section
    theta_s = np.linspace(0, 2*math.pi, 300)
    ax2.add_patch(Circle((0,0), b0/1e5, color="#1a0a40", zorder=3))
    ax2.add_patch(Circle((0,0), b0/1e5, fill=False, ec="#8060ff",
                          lw=1.5, zorder=4))
    # Light rays bending around wormhole throat
    for b_fac in [1.5, 2.0, 3.0, 5.0]:
        b_impact = b_fac * b0/1e5
        y_in = np.linspace(-8*b0/1e5, 0, 200)
        x_in = np.full_like(y_in, -b_impact)
        # Simple deflection (schematic)
        defl_angle = 4*G_SI*GARG_MASS_KG/(C_SI**2*b_impact*1e5)
        x_out_arr  = -b_impact + np.linspace(0, 8*b0/1e5, 200)
        y_out_arr  = -defl_angle * x_out_arr * 50   # exaggerated
        clr_r = plt.cm.plasma(0.3 + 0.1*b_fac)
        ax2.plot(x_in, y_in, color=clr_r, lw=0.7, alpha=0.7)
        ax2.plot(x_out_arr - b_impact, y_out_arr, color=clr_r, lw=0.7, alpha=0.7)
    ax2.set_xlim(-10*b0/1e5, 10*b0/1e5)
    ax2.set_ylim(-10*b0/1e5, 10*b0/1e5)
    ax2.set_aspect("equal")
    ax2.set_xlabel("x / throat_scale")
    ax2.set_ylabel("y / throat_scale")
    ax2.set_title(f"WORMHOLE THROAT — Light Ray Deflection\nb₀ = {b0/1e3:.0f} km")
    ax2.annotate("Throat", (0, b0/1e5*1.2), ha="center", color="#8060ff",
                 fontsize=7)

    plt.tight_layout()
    return fig


# ── §11.6  Wormhole shape comparison ─────────────────────────────────────────
def _plot_shape_comparison(b0: float) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#05080f")

    r_arr = np.geomspace(b0, 10*b0, 300)
    r_n   = r_arr/b0

    shape_styles = [
        (ShapeFunction.ELLIS,       "#8060ff", "-",  "Ellis  b=b₀²/r"),
        (ShapeFunction.POWER_LAW,   "#E8C46A", "--", "Power-law  b=b₀(b₀/r)^0.5"),
        (ShapeFunction.EXPONENTIAL, "#81C784", "-.", "Exponential"),
        (ShapeFunction.ASYMPTOTIC,  "#4FC3F7", ":",  "Asymptotic flat"),
    ]

    ax1, ax2, ax3 = axes

    for shape, clr, ls, lbl in shape_styles:
        wh_s = WormholeGeometry(b0, shape_type=shape)
        b_n  = np.array([wh_s.b(r)/b0 for r in r_arr])
        l_n  = np.array([wh_s.proper_distance_l(r)/b0 for r in r_arr])
        z_em = []
        for r in r_arr:
            bv  = wh_s.b(r)
            rad = r/bv - 1.0
            if rad > 0:
                z_em.append(1/math.sqrt(rad))
            else:
                z_em.append(0.0)
        ax1.plot(r_n, b_n,   color=clr, lw=1.1, ls=ls, label=lbl)
        ax2.plot(r_n, l_n,   color=clr, lw=1.1, ls=ls, label=lbl)
        ax3.semilogy(r_n, np.array(z_em)+1e-10, color=clr, lw=1.1, ls=ls, label=lbl)

    for ax, ylbl, title in [
        (ax1, "b(r)/b₀",     "SHAPE FUNCTION COMPARISON"),
        (ax2, "l(r)/b₀  (proper distance)", "PROPER DISTANCE FROM THROAT"),
        (ax3, "dz/dr (embedding slope)","EMBEDDING SURFACE SLOPE"),
    ]:
        ax.set_xlabel("r / b₀"); ax.set_ylabel(ylbl); ax.set_title(title)
        ax.legend(fontsize=5.5); ax.set_facecolor("#070a16")
        ax.axvline(1.0, color="#D154FF", lw=0.6, ls=":", label="Throat r=b₀")

    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# §12  MAIN STREAMLIT PAGE
# ══════════════════════════════════════════════════════════════════════════════
def wormhole_navigator_page():
    init_session_state()
    _mpl()
    S = st.session_state

    st.markdown("""
    <div style="border-left:3px solid #8060ff;padding:.55rem 1.2rem;
                margin-bottom:1.2rem;background:rgba(128,96,255,0.03);
                font-family:monospace;">
    <div style="color:#8060ff;font-size:.95rem;letter-spacing:.12em;
                font-weight:600;">⟳ WORMHOLE NAVIGATOR &amp; ORBITAL MECHANICS ENGINE</div>
    <div style="color:#5a6a90;font-size:.62rem;margin-top:.2rem;">
    Morris-Thorne Geometry · Exotic Matter · Traversal Physics · Hohmann Transfers ·
    Gravity Assist · Gargantua Slingshot · Full Δv Budget · Saturn→Wormhole→Gargantua
    </div></div>""", unsafe_allow_html=True)

    (tab_geom, tab_exotic, tab_traverse,
     tab_shapes, tab_orbit,
     tab_slingshot, tab_mission) = st.tabs([
        "◎ WORMHOLE GEOMETRY",
        "⬡ EXOTIC MATTER",
        "⇌ TRAVERSAL PHYSICS",
        "∿ SHAPE FAMILIES",
        "⟳ ORBITAL MECHANICS",
        "↻ GRAVITY ASSIST",
        "▲ MISSION Δv BUDGET",
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1 — WORMHOLE GEOMETRY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_geom:
        c1, c2, c3 = st.columns([1, 1, 2.5])
        with c1:
            st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#8060ff;">[ GEOMETRY PARAMETERS ]</div>',
                        unsafe_allow_html=True)
            b0_km  = st.slider("Throat radius b₀ [km]",
                                0.1, 1e6, float(S["wh_throat_km"]), 0.1,
                                format="%.1f")
            shape_name = st.selectbox("Shape function",
                                       [s.name for s in ShapeFunction],
                                       index=0)
            redsh_name = st.selectbox("Redshift function",
                                       [r.name for r in RedshiftFunction],
                                       index=0)
            alpha   = st.slider("Power-law α (if applicable)", 0.0, 0.99, 0.5, 0.01)

            S["wh_throat_km"] = b0_km
            S["wh_shape"]     = shape_name
            S["wh_redshift"]  = redsh_name
            S["wh_alpha"]     = alpha

            if st.button("◎ COMPUTE WORMHOLE", width='stretch',
                         type="primary"):
                wh = WormholeGeometry(
                    throat_radius_m=b0_km*1e3,
                    shape_type=ShapeFunction[shape_name],
                    redshift_type=RedshiftFunction[redsh_name],
                    shape_alpha=alpha)
                S["wh_geometry"] = wh

        wh  = S["wh_geometry"]
        su  = wh.summary()
        with c2:
            fl_ok = "✓ SATISFIED" if su["flaring_condition"] else "✗ VIOLATED"
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(7,10,22,.92);padding:.75rem;
                        border:1px solid rgba(128,96,255,.18);
                        border-top:2px solid #8060ff;border-radius:3px;
                        line-height:2.05;">
            <b style="color:#8060ff;">── GEOMETRY ──</b><br>
            b₀ = <b style="color:#8060ff;">{su['throat_radius_km']:.3f} km</b><br>
            Shape: <b>{su['shape_type'][:30]}</b><br>
            Redshift: <b>{su['redshift_type'][:25]}</b><br>
            b'(b₀) = <b style="color:#E8C46A;">{su['b_prime_at_throat']:.5f}</b><br>
            Flaring-out: <b style="color:{'#81C784' if su['flaring_condition'] else '#D154FF'}">{fl_ok}</b><br>
            Φ(b₀) = <b>{su['Phi_at_throat']:.4f}</b><br>
            g_tt(throat) = <b>{su['g_tt_at_throat']:.4f}</b><br>
            <b style="color:#8060ff;">── EXOTIC MATTER ──</b><br>
            M_exotic = <b style="color:#CE93D8;">{su['exotic_mass_kg']:.4e} kg</b><br>
            = <b style="color:#CE93D8;">{su['exotic_mass_Jupiter']:.4e} M_Jupiter</b><br>
            = <b>{su['exotic_mass_Sun']:.4e} M_Sun</b>
            </div>""", unsafe_allow_html=True)

        with c3:
            fig = _plot_embedding(wh)
            st.pyplot(fig, width='stretch'); plt.close(fig)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — EXOTIC MATTER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_exotic:
        wh  = S["wh_geometry"]
        em  = ExoticMatterPhysics(wh)
        rep = em.feasibility_report()
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(7,10,22,.92);padding:.7rem;
                        border:1px solid rgba(206,147,216,.18);border-radius:3px;
                        line-height:2.0;">
            <b style="color:#CE93D8;">── EXOTIC MATTER ──</b><br>
            M_exotic = <b style="color:#CE93D8;">{rep['exotic_mass_kg']:.4e} kg</b><br>
            = <b>{rep['exotic_mass_Jupiter']:.4e} M_Jupiter</b><br>
            E_exotic = <b>{rep['exotic_energy_J']:.4e} J</b><br>
            = <b>{rep['exotic_energy_stars']:.4e} star-years</b><br>
            <b style="color:#CE93D8;">── CASIMIR ──</b><br>
            Plate sep needed = <b>{rep['casimir_plate_sep_m']:.4e} m</b><br>
            Casimir ρ = <b>{rep['casimir_rho_J_m3']:.4e} J/m³</b><br>
            QI bound = <b>{rep['QI_bound_J_m3']:.4e} J/m³</b><br>
            ρ/QI ratio = <b>{rep['ratio_rho_to_QI']:.4e}</b><br>
            Feasibility: <b style="color:#81C784;">{rep['feasibility'][:25]}</b>
            </div>""", unsafe_allow_html=True)
        with c2:
            fig = _plot_exotic_traversal(wh)
            st.pyplot(fig, width='stretch'); plt.close(fig)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — TRAVERSAL PHYSICS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_traverse:
        wh   = S["wh_geometry"]
        trav = WormholeTraversalCalculator(wh)
        c1, c2 = st.columns([1, 2])
        with c1:
            v_c  = st.slider("Traversal speed v/c", 0.01, 0.99,
                              float(S["wh_v_transit_c"]), 0.01)
            S["wh_v_transit_c"] = v_c
            prof = trav.interstellar_wormhole_profile()
            v_ms = v_c * C_SI
            tau_s  = trav.transit_time_traveller(v_ms)
            t_ext  = trav.transit_time_external(v_ms)
            surv   = trav.survivability_check(v_ms)
            tidal_th = trav.tidal_force_at_throat() * 1.8 / 9.81
            surv_c = {"VIABLE":"#81C784","MARGINAL":"#FFB74D",
                      "TIDAL_LETHAL":"#D154FF","TIME_EXCESSIVE":"#FF8800",
                      "UNSTABLE":"#CE93D8"}.get(surv.name, "#fff")
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(7,10,22,.92);padding:.75rem;
                        border:1px solid rgba(128,96,255,.18);border-radius:3px;
                        line-height:2.05;">
            <b style="color:#8060ff;">── TRAVERSAL @ v={v_c:.2f}c ──</b><br>
            τ_traveller = <b style="color:#E8C46A;">{tau_s/HOUR_S:.3f} hr</b>
            = <b>{tau_s:.1f} s</b><br>
            t_external = <b style="color:#4FC3F7;">{t_ext/HOUR_S:.3f} hr</b><br>
            Δt (time shift) = <b>{abs(t_ext-tau_s):.3f} s</b><br>
            <b style="color:#8060ff;">── FORCES ──</b><br>
            Tidal @ throat = <b style="color:#D154FF;">{tidal_th:.4e} g/m</b><br>
            Φ' acceleration = <b>{abs(wh.Phi_prime(wh.b0))*C_SI**2/9.81:.4e} g</b><br>
            <b style="color:#8060ff;">── VERDICT ──</b><br>
            Status: <b style="color:{surv_c};font-size:.70rem;">{surv.value}</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            # Plot traversal profiles
            _mpl()
            fig_tr, axes_tr = plt.subplots(1, 2, figsize=(11, 5))
            fig_tr.patch.set_facecolor("#05080f")
            l_arr, tidal_r, tidal_l = trav.tidal_force_profile(n_l=200)
            axes_tr[0].semilogy(l_arr/wh.b0, tidal_r+1e-30, color="#D154FF",
                                 lw=1.2, label="Radial tidal [g/m]")
            axes_tr[0].semilogy(l_arr/wh.b0, tidal_l+1e-30, color="#4FC3F7",
                                 lw=1.0, ls="--", label="Lateral tidal [g/m]")
            axes_tr[0].axhline(10.0, color="#E8C46A", lw=0.7, ls=":",
                                label="10 g/m hazardous")
            axes_tr[0].set_xlabel("l / b₀"); axes_tr[0].set_ylabel("Tidal [g/m]")
            axes_tr[0].set_title("TIDAL FORCES ALONG WORMHOLE")
            axes_tr[0].legend(fontsize=6)
            # Transit time vs speed
            v_arr2  = np.linspace(0.01, 0.99, 200)
            tau_arr = [trav.transit_time_traveller(v*C_SI)/HOUR_S for v in v_arr2]
            axes_tr[1].plot(v_arr2, tau_arr, color="#81C784", lw=1.3)
            axes_tr[1].axvline(v_c, color="#D154FF", lw=0.8, ls="--",
                                label=f"v={v_c:.2f}c")
            axes_tr[1].axhline(tau_s/HOUR_S, color="#E8C46A", lw=0.7, ls=":")
            axes_tr[1].set_xlabel("v / c")
            axes_tr[1].set_ylabel("τ_traveller [hours]")
            axes_tr[1].set_title("TRANSIT TIME vs SPEED")
            axes_tr[1].legend(fontsize=6)
            plt.tight_layout()
            st.pyplot(fig_tr, width='stretch'); plt.close(fig_tr)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 4 — SHAPE FAMILIES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_shapes:
        wh  = S["wh_geometry"]
        fig = _plot_shape_comparison(wh.b0)
        st.pyplot(fig, width='stretch'); plt.close(fig)
        # Comparison table
        rows = []
        for shape in ShapeFunction:
            wh_s = WormholeGeometry(wh.b0, shape_type=shape)
            su   = wh_s.summary()
            rows.append({
                "Shape": shape.value[:40],
                "b'(b₀)": round(su["b_prime_at_throat"], 5),
                "Flaring ✓": su["flaring_condition"],
                "M_exotic (kg)": f"{su['exotic_mass_kg']:.3e}",
                "M_exotic/M_Jup": f"{su['exotic_mass_Jupiter']:.3e}",
            })
        st.dataframe(pd.DataFrame(rows), width='stretch', hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 5 — ORBITAL MECHANICS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_orbit:
        planner = S["orb_planner"]
        c1, c2  = st.columns([1, 2])
        with c1:
            st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#8060ff;">[ HOHMANN CALCULATOR ]</div>',
                        unsafe_allow_html=True)
            r1_au = st.slider("Initial orbit r₁ [AU]", 0.1, 40.0, 1.0, 0.1)
            r2_au = st.slider("Target orbit r₂ [AU]",  0.1, 40.0, 9.537, 0.1)
            M_body = st.selectbox("Central body",
                                   ["Sun","Earth","Saturn","Gargantua"])
            M_map  = {"Sun":M_SUN,"Earth":M_EARTH,
                      "Saturn":M_SAT,"Gargantua":GARG_MASS_KG}
            orb    = OrbitalMechanics(M_map[M_body])
            r1_m   = r1_au*AU; r2_m = r2_au*AU
            hoh    = orb.hohmann_transfer(r1_m, r2_m)
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(7,10,22,.92);padding:.65rem;
                        border:1px solid rgba(128,96,255,.12);border-radius:3px;
                        line-height:2.0;">
            Δv₁ = <b style="color:#E8C46A;">{hoh['dv1_ms']:.2f} m/s</b><br>
            Δv₂ = <b style="color:#E8C46A;">{hoh['dv2_ms']:.2f} m/s</b><br>
            Δv_total = <b style="color:#81C784;">{hoh['dv_total_kms']:.4f} km/s</b><br>
            Transfer time = <b style="color:#4FC3F7;">{hoh['transfer_time_days']:.2f} days</b><br>
            = <b>{hoh['transfer_time_days']/365.25:.4f} yr</b><br>
            a_transfer = <b>{hoh['a_transfer_m']/AU:.4f} AU</b><br>
            v_peri = <b>{hoh['v_periapsis_ms']/1e3:.3f} km/s</b><br>
            v_apo  = <b>{hoh['v_apoapsis_ms']/1e3:.3f} km/s</b>
            </div>""", unsafe_allow_html=True)

            est = planner.earth_to_saturn_trajectory()
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c8e0;
                        background:rgba(7,10,22,.92);padding:.65rem;
                        border:1px solid rgba(128,96,255,.12);border-radius:3px;
                        line-height:1.9;margin-top:.5rem;">
            <b style="color:#8060ff;">EARTH→SATURN (Endurance)</b><br>
            Total Δv = <b>{est['total_dv_kms']:.2f} km/s</b><br>
            Transfer time = <b>{est['transfer_time_yr']:.2f} yr</b><br>
            Propellant = <b>{est['fuel']['m_propellant']/1e3:.1f} tonnes</b><br>
            Payload frac = <b>{est['fuel']['payload_fraction']*100:.1f}%</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            fig = _plot_saturn_wormhole(planner)
            st.pyplot(fig, width='stretch'); plt.close(fig)
            st.dataframe(planner.planet_orbital_data(),
                         width='stretch', hide_index=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 6 — GRAVITY ASSIST
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_slingshot:
        planner = S["orb_planner"]
        c1, c2  = st.columns([1, 3])
        with c1:
            v_inf_kms = st.slider("v_∞ approach [km/s]", 0.5, 50.0,
                                   float(S["orb_v_inf"])/1e3, 0.5)
            r_peri    = st.slider("Periapsis radius [r_s]", 1.05, 20.0,
                                   float(S["orb_r_peri"]), 0.05)
            S["orb_v_inf"]  = v_inf_kms*1e3
            S["orb_r_peri"] = r_peri
        with c2:
            fig = _plot_gravity_assist(planner, v_inf_kms*1e3, r_peri)
            st.pyplot(fig, width='stretch'); plt.close(fig)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 7 — MISSION Δv BUDGET
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_mission:
        planner = S["orb_planner"]
        if st.button("▲ COMPUTE FULL Δv BUDGET",
                     width='stretch', type="primary"):
            S["orb_dv_budget"] = planner.full_dv_budget()

        df = S.get("orb_dv_budget")
        if df is not None:
            kpis = [
                ("Total Δv",      f"{df['Δv (m/s)'].sum()/1e3:.2f} km/s",   "#E8C46A"),
                ("Mission days",  f"{df['Cumulative time (days)'].iloc[-1]:.0f}",   "#4FC3F7"),
                ("Final mass",    f"{df['Ship mass after (kg)'].iloc[-1]/1e3:.1f} t","#81C784"),
                ("Prop. used",    f"{(ENDURANCE_MASS_KG - df['Ship mass after (kg)'].iloc[-1])/1e3:.1f} t","#D154FF"),
            ]
            cols = st.columns(len(kpis))
            for col, (lbl, val, clr) in zip(cols, kpis):
                col.markdown(
                    f'<div style="background:rgba(7,10,22,.9);border:1px solid {clr}44;'
                    f'padding:.4rem;text-align:center;border-radius:2px;font-family:monospace;">'
                    f'<div style="color:#444;font-size:.50rem;">{lbl}</div>'
                    f'<div style="color:{clr};font-size:.85rem;">{val}</div>'
                    f'</div>', unsafe_allow_html=True)
            fig = _plot_mission_trajectory(planner)
            st.pyplot(fig, width='stretch'); plt.close(fig)
            st.dataframe(df, width='stretch', hide_index=True)
        else:
            st.info("Click button to compute full mission Δv budget.")
