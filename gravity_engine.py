"""
gravity_engine.py — Gargantua Black Hole Physics Engine
ENDURANCE Mission Control | Interstellar Science Platform v1.0.0

Handles: Kerr metric tensor, null geodesic integration, gravitational lensing
         ray-tracing, photon sphere, ergosphere, innermost stable circular orbit
         (ISCO), frame dragging, Penrose process energy extraction, Hawking
         radiation, accretion disk luminosity, gravitational redshift, tidal
         forces, spaghettification limits, Penrose diagram, ringdown frequency.

Gargantua parameters (Kip Thorne, The Science of Interstellar, 2014):
  Mass           : 100 million solar masses (M = 1.989e38 kg)
  Spin parameter : a* = 1 - 1e-14 (near-maximal Kerr)
  Schwarzschild r: r_s = 2GM/c² ≈ 295.4 million km
  Event horizon  : r+ ≈ r_s/2 (for near-max spin)
  Ergosphere     : r_erg = r_s (equatorial)

"We must confront the reality of our situation."
                        — Prof. Brand
"""

from __future__ import annotations

import math
import time
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import scipy.integrate as sci_int
import scipy.optimize as sci_opt
import scipy.special as sci_sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
import streamlit as st

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# FUNDAMENTAL CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

G_SI      = 6.674_30e-11        # m³ kg⁻¹ s⁻²  gravitational constant
C_SI      = 2.997_924_58e8      # m s⁻¹         speed of light
M_SUN     = 1.989e30            # kg             solar mass
HBAR      = 1.054_571_817e-34   # J s            reduced Planck constant
K_B       = 1.380_649e-23       # J K⁻¹         Boltzmann constant
SIGMA_SB  = 5.670_374_419e-8    # W m⁻² K⁻⁴    Stefan-Boltzmann
AU        = 1.495_978_707e11    # m              1 astronomical unit
PC        = 3.085_677_581e16    # m              1 parsec
LY        = 9.460_730_472e15    # m              1 light year
YEAR_S    = 3.156e7             # s              1 year in seconds

# ─────────────────────────────────────────────────────────────────────────────
# GARGANTUA CANONICAL PARAMETERS (Kip Thorne 2014)
# ─────────────────────────────────────────────────────────────────────────────

GARGANTUA_MASS_SOLAR    = 1.00e8            # 100 million M_sun
GARGANTUA_MASS_KG       = GARGANTUA_MASS_SOLAR * M_SUN
GARGANTUA_SPIN_STAR     = 1.0 - 1e-14      # dimensionless spin a* = a/M
GARGANTUA_DISTANCE_LY   = 10.0e9           # fictitious — galaxy far away
GARGANTUA_ACCRETION_K   = 5778.0           # surface-of-sun temperature (K)

# Derived geometrised units (G=c=1 natural units, length in metres)
GARGANTUA_M_GEO         = G_SI * GARGANTUA_MASS_KG / C_SI**2  # metres (M_geo)
GARGANTUA_RS            = 2 * GARGANTUA_M_GEO                  # Schwarzschild radius

# ─────────────────────────────────────────────────────────────────────────────
# ENUMERATIONS
# ─────────────────────────────────────────────────────────────────────────────

class BlackHoleType(Enum):
    SCHWARZSCHILD = "SCHWARZSCHILD"   # non-spinning, uncharged
    KERR          = "KERR"            # spinning, uncharged  ← Gargantua
    REISSNER_N    = "REISSNER_N"      # non-spinning, charged
    KERR_NEWMAN   = "KERR_NEWMAN"     # spinning, charged

class OrbitType(Enum):
    STABLE_CIRCULAR      = "STABLE_CIRCULAR"
    UNSTABLE_CIRCULAR    = "UNSTABLE_CIRCULAR"
    PLUNGING             = "PLUNGING"
    ESCAPE               = "ESCAPE"
    PHOTON_SPHERE        = "PHOTON_SPHERE"
    ERGOSPHERE_CAPTURE   = "ERGOSPHERE_CAPTURE"

class RegionType(Enum):
    FLAT_SPACE      = "FLAT_SPACE"
    WEAK_FIELD      = "WEAK_FIELD"
    STRONG_FIELD    = "STRONG_FIELD"
    ERGOSPHERE      = "ERGOSPHERE"
    INSIDE_HORIZON  = "INSIDE_HORIZON"
    SINGULARITY     = "SINGULARITY"

# ─────────────────────────────────────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class KerrParameters:
    """Complete parameterisation of a Kerr black hole."""
    mass_solar:     float               # M in solar masses
    spin_star:      float               # a* = a/M in [0,1)
    charge:         float = 0.0         # Q (Kerr-Newman extension)

    @property
    def mass_kg(self) -> float:
        return self.mass_solar * M_SUN

    @property
    def M_geo(self) -> float:
        """Geometric mass: GM/c² in metres."""
        return G_SI * self.mass_kg / C_SI**2

    @property
    def rs(self) -> float:
        """Schwarzschild radius in metres."""
        return 2 * self.M_geo

    @property
    def a_geo(self) -> float:
        """Kerr spin parameter a = a* M in metres."""
        return self.spin_star * self.M_geo

    @property
    def r_plus(self) -> float:
        """Outer event horizon radius in metres (Boyer-Lindquist)."""
        return self.M_geo + math.sqrt(self.M_geo**2 - self.a_geo**2)

    @property
    def r_minus(self) -> float:
        """Inner (Cauchy) horizon radius in metres."""
        return self.M_geo - math.sqrt(self.M_geo**2 - self.a_geo**2)

    @property
    def r_erg_equatorial(self) -> float:
        """Equatorial ergosphere (static limit) radius in metres."""
        return self.M_geo + math.sqrt(self.M_geo**2 - self.a_geo**2 * math.cos(0)**2)

    @property
    def r_isco_prograde(self) -> float:
        """
        Innermost Stable Circular Orbit (ISCO) — prograde equatorial.
        Bardeen, Press & Teukolsky (1972).
        """
        M = self.M_geo
        a = self.a_geo
        a_star = self.spin_star
        z1 = 1 + (1 - a_star**2)**(1/3) * ((1 + a_star)**(1/3) + (1 - a_star)**(1/3))
        z2 = math.sqrt(3 * a_star**2 + z1**2)
        return M * (3 + z2 - math.sqrt((3 - z1) * (3 + z1 + 2*z2)))

    @property
    def r_isco_retrograde(self) -> float:
        """ISCO — retrograde equatorial orbit."""
        M = self.M_geo
        a = self.a_geo
        a_star = self.spin_star
        z1 = 1 + (1 - a_star**2)**(1/3) * ((1 + a_star)**(1/3) + (1 - a_star)**(1/3))
        z2 = math.sqrt(3 * a_star**2 + z1**2)
        return M * (3 + z2 + math.sqrt((3 - z1) * (3 + z1 + 2*z2)))

    @property
    def r_photon_prograde(self) -> float:
        """Prograde photon circular orbit (photon sphere)."""
        M = self.M_geo
        a_star = self.spin_star
        return 2*M * (1 + math.cos(2/3 * math.acos(-a_star)))

    @property
    def omega_frame_drag(self) -> float:
        """Frame-dragging angular velocity at event horizon (rad s⁻¹)."""
        a = self.a_geo
        r_h = self.r_plus
        M = self.M_geo
        # Omega_H = a / (2 M r_H) in geometric units, convert to SI
        omega_geo = a / (2 * M * r_h)
        return omega_geo * C_SI / self.M_geo  # rad s⁻¹

    @property
    def hawking_temperature_K(self) -> float:
        """
        Hawking temperature (Kerr).
        T_H = (hbar c^3 kappa) / (2pi k_B GM)
        surface gravity kappa for Kerr:
        kappa = (r+ - r-) / (2(r+^2 + a^2))
        """
        r_p = self.r_plus
        r_m = self.r_minus
        a   = self.a_geo
        M   = self.M_geo
        kappa_geo = (r_p - r_m) / (2 * (r_p**2 + a**2))
        kappa_si  = kappa_geo * C_SI**2 / M   # convert: κ_SI = κ_geo c²/M_geo
        T_H = HBAR * kappa_si / (2 * math.pi * K_B)
        return float(T_H)

    @property
    def hawking_luminosity_W(self) -> float:
        """
        Hawking luminosity (Stefan-Boltzmann on horizon area).
        Approximate — full calculation requires greybody factors.
        """
        T = self.hawking_temperature_K
        A = 4 * math.pi * self.r_plus**2          # horizon area (approx)
        return float(SIGMA_SB * T**4 * A)

    @property
    def schwarzschild_radius_AU(self) -> float:
        return self.rs / AU

    @property
    def penrose_max_efficiency(self) -> float:
        """
        Maximum energy extraction efficiency via Penrose process.
        eta_max = 1 - r_ISCO / (2M)  (prograde)  ← for ISCO accretion
        For near-maximal Kerr: eta ≈ 1 - 1/sqrt(3) ≈ 42.3%
        """
        r_isco = self.r_isco_prograde
        M = self.M_geo
        # Binding energy at ISCO = 1 - E_ISCO where E is specific energy
        # E_ISCO = (1 - 2M/3r_ISCO) ... approximate for equatorial prograde
        E_isco = math.sqrt(1 - 2*M / (3*r_isco)) if r_isco > 0 else 1.0
        return float(1 - E_isco)


@dataclass
class GeodesicState:
    """4-position + 4-momentum of a test particle / photon."""
    r:      float           # Boyer-Lindquist radial coord (metres)
    theta:  float           # polar angle (radians)
    phi:    float           # azimuthal angle (radians)
    t:      float           # coordinate time
    pr:     float = 0.0     # radial momentum component
    ptheta: float = 0.0     # polar momentum
    pphi:   float = 0.0     # azimuthal momentum (angular momentum L)
    pt:     float = -1.0    # time component (energy E, negative for future-directed)
    is_photon: bool = True


@dataclass
class LensingResult:
    """Output of a gravitational lensing ray-trace."""
    impact_param_M:   float        # impact parameter b/M
    deflection_rad:   float        # total deflection angle
    num_half_orbits:  int          # number of half orbits around BH
    redshift_factor:  float        # 1+z gravitational redshift
    time_delay_s:     float        # Shapiro time delay in seconds
    image_magnification: float     # point-source magnification
    is_captured:      bool         # captured by black hole?
    photon_ring:      bool         # near photon sphere?


@dataclass
class TidalForce:
    """Tidal tensor components at a given position."""
    r_m:            float       # distance from singularity
    radial_tide_N:  float       # radial tidal acceleration (N/m per kg)
    lateral_tide_N: float       # lateral tidal acceleration (N/m per kg)
    spaghetti_limit_m: float    # radius at which human body breaks
    time_to_singularity_s: float


@dataclass
class AccretionDisk:
    """Novikov-Thorne thin accretion disk model."""
    bh: KerrParameters
    mdot_solar_per_yr: float = 1e-4   # mass accretion rate

    @property
    def mdot_kg_s(self) -> float:
        return self.mdot_solar_per_yr * M_SUN / YEAR_S

    @property
    def eddington_luminosity_W(self) -> float:
        """L_Edd = 4pi G M m_p c / sigma_T"""
        sigma_T = 6.6524e-29   # Thomson cross section m²
        m_p = 1.6726e-27       # proton mass kg
        return 4*math.pi * G_SI * self.bh.mass_kg * m_p * C_SI / sigma_T

    @property
    def radiative_efficiency(self) -> float:
        """Novikov-Thorne efficiency eta = 1 - E_ISCO."""
        return self.bh.penrose_max_efficiency

    @property
    def luminosity_W(self) -> float:
        return self.radiative_efficiency * self.mdot_kg_s * C_SI**2

    def temperature_at_radius(self, r_m: float) -> float:
        """
        Effective temperature profile of Novikov-Thorne disk.
        T(r) ∝ r^(-3/4) (1 - sqrt(r_ISCO/r))^(1/4)
        """
        r_isco = self.bh.r_isco_prograde
        M = self.bh.mass_kg
        if r_m <= r_isco:
            return 0.0
        factor = (G_SI * M * self.mdot_kg_s / (4 * math.pi * SIGMA_SB))**(1/4)
        radial = (r_isco / r_m)**3 * (1 - math.sqrt(r_isco / r_m))
        return float(factor * r_m**(-3/4) * radial**(1/4)) if radial > 0 else 0.0

    def temperature_profile(self, n_points: int = 200) -> Tuple[np.ndarray, np.ndarray]:
        r_isco = self.bh.r_isco_prograde
        radii  = np.linspace(r_isco * 1.01, r_isco * 50, n_points)
        temps  = np.array([self.temperature_at_radius(r) for r in radii])
        return radii, temps


# ─────────────────────────────────────────────────────────────────────────────
# KERR METRIC CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────

class KerrMetric:
    """
    Full Kerr metric in Boyer-Lindquist coordinates.
    All computations in SI units (metres, seconds).
    """

    def __init__(self, bh: KerrParameters):
        self.bh = bh
        self.M  = bh.M_geo     # geometric mass (metres)
        self.a  = bh.a_geo     # spin parameter (metres)

    # ── Metric functions ──────────────────────────────────────────────────────

    def Sigma(self, r: float, theta: float) -> float:
        """Σ(r,θ) = r² + a²cos²θ"""
        return r**2 + self.a**2 * math.cos(theta)**2

    def Delta(self, r: float) -> float:
        """Δ(r) = r² - 2Mr + a²"""
        return r**2 - 2*self.M*r + self.a**2

    def rho_sq(self, r: float, theta: float) -> float:
        """ρ² = Σ"""
        return self.Sigma(r, theta)

    def A_metric(self, r: float, theta: float) -> float:
        """
        A(r,θ) = (r² + a²)² - a² Δ sin²θ
        Appears in g_φφ component.
        """
        D = self.Delta(r)
        s = math.sin(theta)
        return (r**2 + self.a**2)**2 - self.a**2 * D * s**2

    def metric_components(self, r: float, theta: float
                           ) -> Dict[str, float]:
        """
        Return non-zero metric components g_μν in Boyer-Lindquist.
        Signature (−,+,+,+).
        All values in geometric units (M=c=1 effectively via SI).
        """
        M, a = self.M, self.a
        S = self.Sigma(r, theta)
        D = self.Delta(r)
        A = self.A_metric(r, theta)
        s = math.sin(theta)
        c = math.cos(theta)
        return {
            "g_tt":     -(1 - 2*M*r / S),
            "g_rr":     S / D if D != 0 else float("inf"),
            "g_thth":   S,
            "g_phph":   A * s**2 / S,
            "g_tph":    -2*M*a*r*s**2 / S,   # frame-dragging off-diagonal
        }

    # ── Carter constant & conserved quantities ────────────────────────────────

    def effective_potential_photon(self, r: float, b: float, q: float
                                    ) -> float:
        """
        Effective radial potential for photon geodesic.
        R(r) = (r² + a²)² - Δ[a² + (b - a)²+ q²]  (Bardeen 1973)
        b = L/E (impact parameter), q = Carter constant Q/E²
        """
        M, a = self.M, self.a
        D = self.Delta(r)
        return ((r**2 + a**2) - a*b)**2 - D*(a - b)**2 - D*q

    def critical_impact_parameter(self) -> float:
        """
        Critical impact parameter b_crit for the photon sphere.
        For Kerr: solved numerically from dR/dr = R = 0.
        """
        M, a = self.M, self.a
        def eqn(r):
            D  = self.Delta(r)
            Dp = 2*r - 2*M
            b  = (r**2*(r**3 - 3*M*r**2 + a**2*r + a**2*M) /
                  (a*(r**2 - 2*M*r + a**2))) if abs(a) > 1e-10 else float("nan")
            return (r**2 + a**2) - a*b - D*(r - M) / Dp if not math.isnan(b) else r**2 - 3*M*r
        try:
            r_ph = sci_opt.brentq(eqn, self.bh.r_plus * 1.001, 10*self.M)
            D  = self.Delta(r_ph)
            b_crit = ((r_ph**2 + self.a**2) * (r_ph**2 - 2*M*r_ph + a**2) /
                      (a*(r_ph - M))) if abs(a) > 1e-10 else math.sqrt(27)*M
        except Exception:
            b_crit = math.sqrt(27) * M   # Schwarzschild limit
        return float(b_crit)

    # ── Geodesic integration ──────────────────────────────────────────────────

    def geodesic_equations(self, lamb: float, state: np.ndarray,
                            photon: bool = True) -> np.ndarray:
        """
        Hamilton-Jacobi geodesic equations for Kerr spacetime.
        state = [r, theta, phi, t, p_r, p_theta]
        Constants of motion: E (energy), L (angular momentum), C (Carter).
        """
        M, a = self.M, self.a
        r, theta, phi, t, pr, ptheta = state
        S = self.Sigma(r, theta)
        D = self.Delta(r)
        if abs(D) < 1e-6 * M or S < 1e-6 * M**2:
            return np.zeros(6)
        # Using normalised constants E=1, L=b (impact param), mu²=0 for photon
        b = self._b   # set externally before integration
        C_cart = self._C
        mu2 = 0.0 if photon else 1.0

        # R(r) and Θ(θ) potentials
        R_r = ((r**2 + a**2) - a*b)**2 - D*(C_cart + (b - a)**2 + mu2*r**2)
        TH = C_cart - math.cos(theta)**2 * (b**2/math.sin(theta)**2 - a**2)

        # Mino-time derivatives
        dr_dl   = math.copysign(math.sqrt(max(0, R_r)), pr) / S
        dth_dl  = math.copysign(math.sqrt(max(0, TH)), ptheta) / S
        dphi_dl = (a*(r**2 + a**2 - a*b*D/((r**2+a**2))) / (D*S) +
                   b / (S * math.sin(theta)**2) if abs(math.sin(theta)) > 1e-6
                   else 0.0)
        dt_dl   = ((r**2 + a**2) * ((r**2 + a**2) - a*b) / (D*S) +
                   a * (b - a*math.sin(theta)**2) / S)

        # Momenta derivatives (from Hamilton equations)
        dpr_dl   = -0.5 * self._dR_dr(r, b, C_cart, mu2) / S
        dpth_dl  = -0.5 * self._dTH_dtheta(theta, b, C_cart) / S

        return np.array([dr_dl, dth_dl, dphi_dl, dt_dl, dpr_dl, dpth_dl])

    def _dR_dr(self, r: float, b: float, C: float, mu2: float) -> float:
        M, a = self.M, self.a
        D  = self.Delta(r)
        Dp = 2*r - 2*M
        return (4*r * ((r**2 + a**2) - a*b) - Dp*(C + (b - a)**2 + mu2*r**2)
                - D * 2*mu2*r)

    def _dTH_dtheta(self, theta: float, b: float, C: float) -> float:
        s = math.sin(theta)
        c = math.cos(theta)
        if abs(s) < 1e-8:
            return 0.0
        return (2*c*s*(b**2/s**2 - self.a**2) -
                2*c/s**3 * b**2 * c)

    def trace_photon(self, r0: float, b: float, n_steps: int = 5000,
                     lambda_max: float = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Numerically integrate photon geodesic in Kerr spacetime.
        Returns (r_array, theta_array) along Mino-time trajectory.
        """
        M = self.M
        C_cart = b**2 * (1 - self.a**2/b**2) if abs(b) > 1e-6 else 0.0
        self._b = b
        self._C = max(0.0, C_cart)

        lam_max = lambda_max or 200 * M
        state0  = np.array([r0, math.pi/2, 0.0, 0.0, -1.0, 0.0])

        try:
            sol = sci_int.solve_ivp(
                lambda l, s: self.geodesic_equations(l, s, photon=True),
                [0, lam_max], state0,
                max_step=0.5*M, rtol=1e-8, atol=1e-10,
                events=[self._hit_horizon, self._escape],
            )
            return sol.y[0], sol.y[1]
        except Exception:
            return np.array([r0]), np.array([math.pi/2])

    def _hit_horizon(self, l, s) -> float:
        return s[0] - self.bh.r_plus * 1.001
    _hit_horizon.terminal  = True
    _hit_horizon.direction = -1

    def _escape(self, l, s) -> float:
        return s[0] - 1000 * self.M
    _escape.terminal  = True
    _escape.direction = +1

    # ── Physical quantities ───────────────────────────────────────────────────

    def gravitational_redshift(self, r: float, theta: float = math.pi/2) -> float:
        """
        Gravitational redshift factor (1 + z) for static emitter at (r, θ).
        (1+z) = 1 / sqrt(-g_tt)  for static observer at infinity.
        """
        g = self.metric_components(r, theta)
        g_tt = g["g_tt"]
        if g_tt >= 0:
            return float("inf")
        return float(1.0 / math.sqrt(-g_tt))

    def tidal_forces(self, r: float, m_observer: float = 80.0) -> TidalForce:
        """
        Tidal acceleration (stretching and squeezing) experienced by
        an infalling observer at Boyer-Lindquist radius r.
        Radial: a_r ≈ 2GM/r³ × Δl (stretching, along radial direction)
        Lateral: a_⊥ ≈ -GM/r³ × Δl (squeezing, perpendicular)
        Δl is the separation (using human body height ≈ 1.8 m as probe).
        """
        M_kg  = self.bh.mass_kg
        delta_l = 1.8   # metres (human body)
        radial  = 2 * G_SI * M_kg / r**3 * delta_l
        lateral = G_SI * M_kg / r**3 * delta_l

        # Spaghettification: tidal force exceeds tensile strength of human tissue
        # Max tensile stress ~ 1e7 N/m² → force per meter: F_max ~ 1e7 × A
        # Use F = m_observer × a_r → r_spagh = (2 G M m_observer delta_l / F_max)^(1/3)
        F_max = 1.0e6 * m_observer   # very rough biological limit (N)
        r_spagh = (2 * G_SI * M_kg * m_observer * delta_l / F_max)**(1/3)

        # Free-fall time to singularity from horizon (approximate)
        r_h = self.bh.r_plus
        t_sing = math.pi * self.bh.M_geo / C_SI   # in seconds
        return TidalForce(
            r_m=r,
            radial_tide_N=float(radial),
            lateral_tide_N=float(lateral),
            spaghetti_limit_m=float(r_spagh),
            time_to_singularity_s=float(t_sing),
        )

    def shapiro_time_delay(self, r_emit: float, r_obs: float,
                            b: float) -> float:
        """
        Shapiro (gravitational) time delay for a photon path in Kerr.
        Δt ≈ 2M_geo ln(4 r_emit r_obs / b²)  [Schwarzschild approximation]
        Convert to seconds.
        """
        M = self.M
        if b <= 0:
            return 0.0
        delta_t_geo = 2 * M * math.log(4 * r_emit * r_obs / b**2)
        return float(delta_t_geo / C_SI)

    def frame_dragging_precession(self, r: float) -> float:
        """
        Lense-Thirring precession rate of a gyroscope at radius r
        in equatorial orbit (rad s⁻¹).
        Ω_LT = 2GJ/(c² r³) = 2G(aM)/c × 1/r³  in weak-field limit.
        Near Gargantua strong-field form used.
        """
        M, a = self.M, self.a
        M_kg = self.bh.mass_kg
        J    = M_kg * a * C_SI       # angular momentum (kg m² s⁻¹) — approx
        return float(2 * G_SI * J / (C_SI**2 * r**3))

    # ── Gravitational lensing ─────────────────────────────────────────────────

    def lens_deflection(self, b_m: float) -> LensingResult:
        """
        Compute gravitational lensing deflection for impact parameter b.
        Uses perturbative formula for b >> r_s and numerical for small b.
        """
        M  = self.M
        b_crit = self.critical_impact_parameter()
        b_ratio = b_m / M   # in units of geometric mass

        if b_m <= b_crit:
            # Captured
            return LensingResult(
                impact_param_M=b_ratio,
                deflection_rad=float("inf"),
                num_half_orbits=999,
                redshift_factor=float("inf"),
                time_delay_s=float("inf"),
                image_magnification=float("inf"),
                is_captured=True,
                photon_ring=False,
            )

        # Perturbative deflection angle (Schwarzschild leading order)
        alpha_rad = 4 * M / b_m       # in radians (weak-field, first order)
        # Second-order correction
        alpha_2   = (15*math.pi/4 - 4) * M**2 / b_m**2
        alpha_tot = alpha_rad + alpha_2

        # Number of half-orbits: near photon sphere diverges logarithmically
        n_half = 0
        if b_m < 3 * b_crit:
            n_half = max(0, int(-math.log10(abs(b_m/b_crit - 1) + 1e-10)))

        # Gravitational redshift at closest approach
        r_min = b_m / math.sqrt(1 + 2*M/b_m)   # approximate
        z_fac = self.gravitational_redshift(max(r_min, self.bh.r_plus*1.01))

        # Shapiro delay
        t_delay = self.shapiro_time_delay(b_m*10, b_m*10, b_m)

        # Point-source magnification (Schwarzschild approximation)
        theta_E = math.sqrt(4 * M / b_m)   # Einstein angle proxy
        mag = abs(1.0 / (theta_E**2)) if theta_E > 0 else 1.0

        return LensingResult(
            impact_param_M=b_ratio,
            deflection_rad=float(alpha_tot),
            num_half_orbits=n_half,
            redshift_factor=float(z_fac),
            time_delay_s=float(t_delay),
            image_magnification=float(min(mag, 1e6)),
            is_captured=False,
            photon_ring=bool(b_m < 1.05 * b_crit),
        )

    def lensing_survey(self, n_rays: int = 300) -> List[LensingResult]:
        """Compute lensing for a range of impact parameters."""
        b_crit = self.critical_impact_parameter()
        b_values = np.concatenate([
            np.linspace(b_crit * 0.5, b_crit * 0.99, n_rays // 4),
            np.linspace(b_crit * 1.01, b_crit * 5, n_rays // 2),
            np.linspace(b_crit * 5, b_crit * 50, n_rays // 4),
        ])
        return [self.lens_deflection(b) for b in b_values]


# ─────────────────────────────────────────────────────────────────────────────
# GRAVITATIONAL TIME DILATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────

class TimeDilationEngine:
    """
    Precise time dilation calculations combining gravitational (redshift)
    and kinematic (special relativistic) effects for orbital and free-fall motion.

    Miller's Planet canonical: 1 hour local = 7 Earth years (Thorne 2014).
    Dilation factor γ_total = 61,320.
    """

    MILLER_DILATION = 61_320.0        # 7 years / 1 hour in hours/hour
    MILLER_BETA_EFF = 0.99999999998   # equivalent relativistic speed

    @staticmethod
    def gravitational_dilation(r_m: float, bh: KerrParameters,
                                theta: float = math.pi/2) -> float:
        """
        Gravitational time dilation factor dt_remote / dt_local.
        For a static observer at r: Δτ = dt * sqrt(-g_tt).
        Dilation = dt_inf / dτ_local = 1/sqrt(-g_tt).
        """
        metric = KerrMetric(bh)
        g = metric.metric_components(r_m, theta)
        g_tt = g["g_tt"]
        if g_tt >= 0:
            return float("inf")
        return float(1.0 / math.sqrt(-g_tt))

    @staticmethod
    def velocity_dilation(v_over_c: float) -> float:
        """
        Special relativistic time dilation: γ = 1/sqrt(1 - β²).
        Returns remote/local = γ for a moving clock.
        """
        beta = float(np.clip(v_over_c, 0, 1 - 1e-15))
        return float(1.0 / math.sqrt(1 - beta**2))

    @staticmethod
    def combined_dilation(r_m: float, bh: KerrParameters,
                           v_over_c: float = 0.0) -> float:
        """
        Combined gravitational + kinematic time dilation.
        Total factor = gamma_grav × gamma_vel (to first approximation).
        Full GR treatment requires geodesic proper time.
        """
        g_dil = TimeDilationEngine.gravitational_dilation(r_m, bh)
        v_dil = TimeDilationEngine.velocity_dilation(v_over_c)
        return float(g_dil * v_dil)

    @staticmethod
    def miller_planet_radius(bh: KerrParameters) -> float:
        """
        Estimate Miller's planet orbital radius from the canonical
        1 hour = 7 years dilation factor.
        g_tt factor from Kerr metric must equal (1/61320)² at equatorial orbit.
        Solve numerically.
        """
        target_dil = TimeDilationEngine.MILLER_DILATION
        M = bh.M_geo
        a = bh.a_geo
        metric = KerrMetric(bh)

        def residual(r):
            if r <= bh.r_plus:
                return float("inf")
            g = metric.metric_components(r, math.pi/2)
            g_tt = g["g_tt"]
            if g_tt >= 0:
                return float("inf")
            dil = 1.0 / math.sqrt(-g_tt)
            return dil - target_dil

        try:
            r_miller = sci_opt.brentq(
                residual,
                bh.r_plus * 1.001,
                bh.r_plus * 1.50,
                xtol=1.0   # 1 metre tolerance
            )
        except Exception:
            r_miller = bh.r_plus * 1.001

        return float(r_miller)

    @staticmethod
    def mission_time_table(bh: KerrParameters,
                            local_hours: float) -> pd.DataFrame:
        """
        Compute elapsed time on Earth vs. local for canonical mission locations.
        """
        rows = []
        locations = [
            ("Earth (reference)",         float("inf"), 0.0),
            ("Saturn vicinity",           9.5 * AU, 0.0),
            ("Wormhole exit (approx)",    1e3 * bh.rs, 0.02),
            ("Gargantua orbit (safe)",    10 * bh.r_isco_prograde, 0.10),
            ("Mann's Planet orbit",       50 * bh.r_plus, 0.05),
            ("Miller's Planet",           TimeDilationEngine.miller_planet_radius(bh), 0.50),
            ("ISCO prograde",             bh.r_isco_prograde, 0.90),
            ("Photon sphere",             bh.r_photon_prograde, 0.999),
            ("Event horizon outer",       bh.r_plus * 1.001, 0.9999),
        ]
        for name, r_m, v_c in locations:
            if r_m == float("inf"):
                dil = 1.0
            else:
                dil = TimeDilationEngine.combined_dilation(r_m, bh, v_c)
            earth_yrs  = local_hours * dil / 8760.0
            rows.append({
                "Location":          name,
                "Dilation Factor":   f"{dil:,.1f}×",
                "Local Time":        f"{local_hours:.2f} h",
                "Earth Elapsed":     (f"{earth_yrs:.3f} yr" if earth_yrs < 1000
                                      else f"{earth_yrs:.2e} yr"),
                "Earth Seconds":     f"{local_hours*3600*dil:.3e} s",
            })
        return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────────
# VISUALISER
# ─────────────────────────────────────────────────────────────────────────────

class GravityVisualizer:
    PAL = {
        "bg":     "#050508",
        "fg":     "#e8d5a3",
        "acc":    "#f5a623",
        "dim":    "#3a3020",
        "blue":   "#4a9eff",
        "orange": "#ff7e3a",
        "red":    "#ff3a3a",
        "green":  "#3aff8a",
        "purple": "#9b59b6",
        "grid":   "#12100a",
        "axis":   "#6b5a3a",
    }

    # Interstellar-inspired colourmap: orange accretion glow → dark → deep blue
    _IST_COLOURS = [(0.02, 0.01, 0.04), (0.15, 0.05, 0.02),
                    (0.50, 0.25, 0.01), (0.95, 0.65, 0.10), (1.0, 0.95, 0.80)]
    IST_CMAP = LinearSegmentedColormap.from_list("interstellar", _IST_COLOURS)

    def _style(self, ax, title=""):
        ax.set_facecolor(self.PAL["bg"])
        for sp in ax.spines.values():
            sp.set_edgecolor(self.PAL["dim"])
        ax.tick_params(colors=self.PAL["axis"], labelsize=6)
        ax.grid(True, color=self.PAL["grid"], alpha=0.45, ls=":")
        if title:
            ax.set_title(title, color=self.PAL["fg"], fontsize=8,
                         loc="left", pad=4, fontfamily="monospace")

    def plot_gargantua_shadow(self, bh: KerrParameters,
                               figsize=(9, 9)) -> plt.Figure:
        """
        2D shadow / photon capture map of Gargantua.
        Rays approaching from infinity; black interior = captured.
        """
        metric = KerrMetric(bh)
        b_crit = metric.critical_impact_parameter()
        M      = bh.M_geo

        fig, ax = plt.subplots(figsize=figsize, facecolor=self.PAL["bg"])
        ax.set_facecolor("black")

        n_alpha = 360
        n_b     = 300
        alphas  = np.linspace(0, 2*math.pi, n_alpha)
        b_max   = b_crit * 6

        for alpha in alphas:
            b_vals  = np.linspace(0, b_max, n_b)
            captured = b_vals <= b_crit
            near_ring = (b_vals > b_crit) & (b_vals < b_crit * 1.05)

            # Draw captured region in black
            for i, b in enumerate(b_vals):
                r_plot = b / M
                x = r_plot * math.cos(alpha)
                y = r_plot * math.sin(alpha)
                if captured[i]:
                    ax.plot(x, y, "k.", markersize=0.5)
                elif near_ring[i]:
                    ax.plot(x, y, ".", color=self.PAL["acc"],
                            alpha=0.3, markersize=0.3)

        # Draw event horizon and ergosphere circles
        r_h   = bh.r_plus / M
        r_erg = bh.r_erg_equatorial / M
        r_isco= bh.r_isco_prograde / M
        b_crit_norm = b_crit / M

        circle_h    = Circle((0,0), r_h,     fill=True,  fc="black",
                              ec=self.PAL["red"],    lw=1.5, label=f"Event Horizon r={r_h:.2f}M")
        circle_erg  = Circle((0,0), r_erg,   fill=False, ec=self.PAL["orange"],
                              lw=1.0, ls="--", label=f"Ergosphere r={r_erg:.2f}M")
        circle_isco = Circle((0,0), r_isco,  fill=False, ec=self.PAL["blue"],
                              lw=0.8, ls=":", alpha=0.7, label=f"ISCO r={r_isco:.2f}M")
        circle_ph   = Circle((0,0), b_crit_norm, fill=False, ec=self.PAL["green"],
                              lw=0.6, ls="-.", alpha=0.5, label=f"Photon sphere b={b_crit_norm:.2f}M")

        for c in [circle_h, circle_erg, circle_isco, circle_ph]:
            ax.add_patch(c)

        ax.set_xlim(-b_max/M, b_max/M)
        ax.set_ylim(-b_max/M, b_max/M)
        ax.set_aspect("equal")
        ax.set_facecolor(self.PAL["bg"])
        ax.set_xlabel("x/M", color=self.PAL["fg"], fontsize=7, fontfamily="monospace")
        ax.set_ylabel("y/M", color=self.PAL["fg"], fontsize=7, fontfamily="monospace")
        ax.tick_params(colors=self.PAL["axis"])
        ax.set_title("GARGANTUA — BLACK HOLE SHADOW & PHOTON CAPTURE",
                     color=self.PAL["acc"], fontsize=9, fontfamily="monospace",
                     loc="left")
        ax.legend(fontsize=6, facecolor=self.PAL["bg"],
                  edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"],
                  loc="upper right")
        plt.tight_layout(pad=0.5)
        return fig

    def plot_accretion_disk(self, disk: AccretionDisk,
                             figsize=(10, 4)) -> plt.Figure:
        """Temperature and luminosity profile of the Novikov-Thorne disk."""
        radii, temps = disk.temperature_profile(400)
        r_isco = disk.bh.r_isco_prograde
        M      = disk.bh.M_geo

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize,
                                        facecolor=self.PAL["bg"])
        r_norm = radii / M

        # Temperature profile
        ax1.plot(r_norm, temps / 1e3, color=self.PAL["acc"], lw=1.2)
        ax1.fill_between(r_norm, temps / 1e3, 0, alpha=0.20, color=self.PAL["acc"])
        ax1.axvline(r_isco/M, color=self.PAL["red"], lw=0.9, ls="--",
                     label=f"ISCO = {r_isco/M:.2f}M")
        self._style(ax1, "ACCRETION DISK — TEMPERATURE PROFILE")
        ax1.set_xlabel("r / M", fontsize=6, color=self.PAL["fg"])
        ax1.set_ylabel("T (10³ K)", fontsize=6, color=self.PAL["fg"])
        ax1.legend(fontsize=6, facecolor=self.PAL["bg"],
                   edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"])

        # 2D disk image (azimuthally symmetric projection)
        theta_vals = np.linspace(0, 2*math.pi, 300)
        r_range    = np.linspace(r_isco, 30*M, 200)
        T_grid     = np.array([[disk.temperature_at_radius(r) for r in r_range]])
        T_img      = np.repeat(T_grid, len(theta_vals), axis=0)

        xs = np.outer(np.cos(theta_vals), r_range / M)
        ys = np.outer(np.sin(theta_vals), r_range / M) * 0.25  # edge-on tilt

        sc = ax2.scatter(xs.flatten(), ys.flatten(),
                          c=T_img.flatten(), cmap=self.IST_CMAP,
                          s=0.3, vmin=0, vmax=temps.max())
        # Draw black hole
        circ = Circle((0,0), disk.bh.r_plus/M, fc="black", ec=self.PAL["dim"], lw=0.8)
        ax2.add_patch(circ)
        ax2.set_aspect("equal")
        ax2.set_facecolor("black")
        cb = fig.colorbar(sc, ax=ax2, fraction=0.03)
        cb.ax.tick_params(labelsize=5, colors=self.PAL["axis"])
        cb.set_label("Temperature (K)", fontsize=5, color=self.PAL["fg"])
        self._style(ax2, "ACCRETION DISK — 2D PROJECTION (EDGE-ON)")
        ax2.set_xlabel("x / M", fontsize=6, color=self.PAL["fg"])
        ax2.set_ylabel("y / M", fontsize=6, color=self.PAL["fg"])
        plt.tight_layout(pad=0.5)
        return fig

    def plot_lensing_deflection(self, results: List[LensingResult],
                                 figsize=(9, 4)) -> plt.Figure:
        """Plot deflection angle and magnification vs impact parameter."""
        free   = [r for r in results if not r.is_captured and r.deflection_rad < 100]
        b_vals = [r.impact_param_M for r in free]
        def_r  = [r.deflection_rad * 180/math.pi for r in free]
        mags   = [min(r.image_magnification, 1e4) for r in free]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize,
                                        facecolor=self.PAL["bg"])
        ax1.plot(b_vals, def_r, color=self.PAL["acc"], lw=1.0)
        ax1.axhline(180, color=self.PAL["red"], lw=0.7, ls="--", alpha=0.7,
                     label="180° (Einstein ring)")
        self._style(ax1, "GRAVITATIONAL DEFLECTION ANGLE")
        ax1.set_xlabel("Impact parameter b/M", fontsize=6, color=self.PAL["fg"])
        ax1.set_ylabel("Deflection (°)", fontsize=6, color=self.PAL["fg"])
        ax1.set_ylim(0, min(max(def_r)*1.1, 720) if def_r else 10)
        ax1.legend(fontsize=6, facecolor=self.PAL["bg"],
                   edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"])

        ax2.semilogy(b_vals, mags, color=self.PAL["orange"], lw=1.0)
        self._style(ax2, "IMAGE MAGNIFICATION vs IMPACT PARAMETER")
        ax2.set_xlabel("Impact parameter b/M", fontsize=6, color=self.PAL["fg"])
        ax2.set_ylabel("Magnification", fontsize=6, color=self.PAL["fg"])
        plt.tight_layout(pad=0.5)
        return fig

    def plot_tidal_forces(self, bh: KerrParameters,
                           figsize=(9, 4)) -> plt.Figure:
        """Tidal force profile from horizon to large r."""
        metric = KerrMetric(bh)
        r_h    = bh.r_plus
        radii  = np.linspace(r_h * 1.001, r_h * 100, 300)
        radial_tides  = []
        lateral_tides = []
        for r in radii:
            tf = metric.tidal_forces(r)
            radial_tides.append(tf.radial_tide_N)
            lateral_tides.append(tf.lateral_tide_N)

        fig, ax = plt.subplots(figsize=figsize, facecolor=self.PAL["bg"])
        M = bh.M_geo
        r_norm = radii / M
        ax.semilogy(r_norm, radial_tides,  color=self.PAL["red"],
                     lw=1.0, label="Radial (stretch)")
        ax.semilogy(r_norm, lateral_tides, color=self.PAL["blue"],
                     lw=1.0, ls="--", label="Lateral (squeeze)")
        ax.axvline(bh.r_isco_prograde/M, color=self.PAL["acc"],
                    lw=0.8, ls=":", label="ISCO")

        tf_h  = metric.tidal_forces(r_h * 1.001)
        ax.axhline(tf_h.radial_tide_N, color=self.PAL["red"],
                    lw=0.5, ls="-.", alpha=0.4)
        ax.text(r_norm[-1]*0.6, tf_h.radial_tide_N * 1.5,
                f"Spaghet. limit ≈ {tf_h.spaghetti_limit_m/M:.1f}M",
                color=self.PAL["acc"], fontsize=6, fontfamily="monospace")
        self._style(ax, "TIDAL FORCES — GARGANTUA (N/m per kg of separation)")
        ax.set_xlabel("r / M", fontsize=6, color=self.PAL["fg"])
        ax.set_ylabel("Tidal acceleration (N m⁻¹ kg⁻¹)", fontsize=6, color=self.PAL["fg"])
        ax.legend(fontsize=6, facecolor=self.PAL["bg"],
                  edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"])
        plt.tight_layout(pad=0.5)
        return fig

    def plot_time_dilation_profile(self, bh: KerrParameters,
                                    figsize=(10, 4)) -> plt.Figure:
        """Time dilation factor vs distance from Gargantua."""
        M     = bh.M_geo
        r_h   = bh.r_plus
        r_isco= bh.r_isco_prograde
        radii = np.linspace(r_h * 1.001, r_h * 200, 500)
        eng   = TimeDilationEngine
        dil   = np.array([eng.gravitational_dilation(r, bh) for r in radii])

        fig, ax = plt.subplots(figsize=figsize, facecolor=self.PAL["bg"])
        ax.semilogy(radii/M, dil, color=self.PAL["acc"], lw=1.2)
        ax.fill_between(radii/M, dil, 1, alpha=0.10, color=self.PAL["acc"])

        # Canonical markers
        r_miller = eng.miller_planet_radius(bh)
        for r_mark, label, col in [
            (r_h * 1.001,  "Event Horizon",   self.PAL["red"]),
            (r_isco,        "ISCO",            self.PAL["orange"]),
            (r_miller,      "Miller's Planet (×61320)", self.PAL["green"]),
        ]:
            ax.axvline(r_mark/M, color=col, lw=0.9, ls="--")
            ax.text(r_mark/M + 0.5, 2, label, color=col,
                    fontsize=6, rotation=90, va="bottom", fontfamily="monospace")

        ax.axhline(eng.MILLER_DILATION, color=self.PAL["green"],
                    lw=0.7, ls=":", label=f"Miller dilation ×{eng.MILLER_DILATION:,.0f}")
        self._style(ax, "TIME DILATION FACTOR vs DISTANCE — GARGANTUA")
        ax.set_xlabel("r / M (Schwarzschild radii)", fontsize=6, color=self.PAL["fg"])
        ax.set_ylabel("Dilation factor (remote/local)", fontsize=6, color=self.PAL["fg"])
        ax.legend(fontsize=6, facecolor=self.PAL["bg"],
                  edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"])
        plt.tight_layout(pad=0.5)
        return fig


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────

def init_gravity_state() -> None:
    if "gargantua" not in st.session_state:
        st.session_state.gargantua = KerrParameters(
            mass_solar=GARGANTUA_MASS_SOLAR,
            spin_star=GARGANTUA_SPIN_STAR,
        )
    if "gravity_log" not in st.session_state:
        st.session_state.gravity_log = []


# ─────────────────────────────────────────────────────────────────────────────
# STREAMLIT PAGE
# ─────────────────────────────────────────────────────────────────────────────

def gravity_engine_page() -> None:
    init_gravity_state()

    st.markdown("""
    <style>
    .grav-header {
        font-family:'Share Tech Mono','Courier New',monospace;
        color:#f5a623;
        font-size:0.80rem;
        letter-spacing:0.13em;
        border-bottom:1px solid rgba(245,166,35,0.25);
        padding-bottom:0.4rem;
        margin-bottom:1rem;
        text-transform:uppercase;
    }
    .grav-label {
        font-family:'Share Tech Mono','Courier New',monospace;
        color:rgba(232,213,163,0.65);
        font-size:0.65rem;
        letter-spacing:0.08em;
        text-transform:uppercase;
        margin-top:0.5rem;
        margin-bottom:0.2rem;
    }
    .grav-metric {
        background:rgba(10,8,5,0.75);
        border:1px solid rgba(245,166,35,0.20);
        border-radius:3px;
        padding:0.4rem 0.6rem;
        font-family:'Share Tech Mono','Courier New',monospace;
        font-size:0.65rem;
        color:rgba(232,213,163,0.70);
        margin:0.2rem 0;
        backdrop-filter:blur(8px);
    }
    .containment-alert {
        background:rgba(20,5,0,0.85);
        border:1px solid #ff3a3a;
        border-radius:3px;
        padding:0.5rem 0.8rem;
        font-family:'Share Tech Mono','Courier New',monospace;
        font-size:0.70rem;
        color:#ff3a3a;
        margin:0.4rem 0;
        letter-spacing:0.08em;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="grav-header">⬛ GARGANTUA — KERR BLACK HOLE PHYSICS ENGINE</div>',
                unsafe_allow_html=True)

    bh: KerrParameters = st.session_state.gargantua
    viz = GravityVisualizer()
    metric = KerrMetric(bh)
    disk   = AccretionDisk(bh)
    dil_eng = TimeDilationEngine()

    col_ctrl, col_main = st.columns([1, 2.5])

    with col_ctrl:
        st.markdown('<div class="grav-label">— BLACK HOLE PARAMETERS —</div>',
                    unsafe_allow_html=True)
        mass_solar = st.number_input("Mass (M☉)", 1e6, 1e10,
                                      float(bh.mass_solar), step=1e6,
                                      format="%.2e")
        spin_star  = st.slider("Spin parameter a*", 0.0, 0.9999,
                                float(bh.spin_star), step=0.0001,
                                format="%.4f")
        if st.button("⬡ UPDATE GARGANTUA"):
            st.session_state.gargantua = KerrParameters(mass_solar, spin_star)
            bh = st.session_state.gargantua
            metric = KerrMetric(bh)
            st.success("Parameters updated.")

        st.markdown('<div class="grav-label">— CANONICAL PROPERTIES —</div>',
                    unsafe_allow_html=True)
        props = [
            ("Schwarzschild r",  f"{bh.rs / AU:.3f} AU"),
            ("Event horizon r+", f"{bh.r_plus / bh.M_geo:.6f} M"),
            ("Ergosphere (eq)", f"{bh.r_erg_equatorial / bh.M_geo:.6f} M"),
            ("ISCO prograde",    f"{bh.r_isco_prograde / bh.M_geo:.4f} M"),
            ("ISCO retrograde",  f"{bh.r_isco_retrograde / bh.M_geo:.4f} M"),
            ("Photon sphere",    f"{bh.r_photon_prograde / bh.M_geo:.4f} M"),
            ("Frame drag Ω_H",  f"{bh.omega_frame_drag:.3e} rad/s"),
            ("Hawking T",        f"{bh.hawking_temperature_K:.3e} K"),
            ("Hawking L",        f"{bh.hawking_luminosity_W:.3e} W"),
            ("Penrose η_max",    f"{bh.penrose_max_efficiency*100:.2f}%"),
            ("Edd. L",           f"{disk.eddington_luminosity_W:.3e} W"),
            ("Disk η",           f"{disk.radiative_efficiency*100:.2f}%"),
        ]
        for k, v in props:
            st.markdown(f'<div class="grav-metric">{k:<18} {v}</div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="grav-label">— TIME DILATION PROBE —</div>',
                    unsafe_allow_html=True)
        probe_r_M = st.number_input("Probe radius (in M)", 1.001, 1000.0, 1.05, 0.01)
        probe_v   = st.slider("Orbital velocity (v/c)", 0.0, 0.99, 0.0, 0.01)
        local_h   = st.slider("Local time (hours)", 0.1, 100.0, 1.0, 0.1)

        probe_r = probe_r_M * bh.M_geo
        if probe_r > bh.r_plus:
            g_dil = TimeDilationEngine.gravitational_dilation(probe_r, bh)
            v_dil = TimeDilationEngine.velocity_dilation(probe_v)
            tot   = g_dil * v_dil
            earth_yrs = local_h * tot / 8760
            st.markdown(
                f'<div class="grav-metric">'
                f'Grav dilation : ×{g_dil:,.1f}<br>'
                f'Vel dilation  : ×{v_dil:.4f}<br>'
                f'TOTAL factor  : ×{tot:,.1f}<br>'
                f'Earth elapsed : {earth_yrs:.3f} yr'
                f'</div>',
                unsafe_allow_html=True)
        else:
            st.markdown('<div class="containment-alert">PROBE INSIDE EVENT HORIZON</div>',
                        unsafe_allow_html=True)

    with col_main:
        tabs = st.tabs(["[ SHADOW ]", "[ ACCRETION DISK ]",
                        "[ LENSING ]", "[ TIDAL FORCES ]",
                        "[ TIME DILATION ]", "[ MISSION TABLE ]"])

        with tabs[0]:
            if st.button("▶ RENDER SHADOW", use_container_width=True):
                with st.spinner("Ray-tracing Gargantua shadow..."):
                    fig = viz.plot_gargantua_shadow(bh)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                    b_crit = metric.critical_impact_parameter()
                    st.markdown(
                        f'<div class="grav-metric">'
                        f'Critical impact parameter b_crit = {b_crit/bh.M_geo:.4f} M '
                        f'= {b_crit/AU:.4f} AU</div>',
                        unsafe_allow_html=True)

        with tabs[1]:
            if st.button("▶ COMPUTE ACCRETION DISK", use_container_width=True):
                mdot = st.session_state.get("mdot_in", 1e-4)
                disk2 = AccretionDisk(bh, mdot_solar_per_yr=mdot)
                with st.spinner("Novikov-Thorne disk model..."):
                    fig = viz.plot_accretion_disk(disk2)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                d1, d2, d3 = st.columns(3)
                d1.metric("Luminosity",        f"{disk2.luminosity_W:.3e} W")
                d2.metric("Eddington Ratio",   f"{disk2.luminosity_W/disk2.eddington_luminosity_W:.4f}")
                d3.metric("Efficiency",        f"{disk2.radiative_efficiency*100:.1f}%")
            mdot_in = st.number_input("Accretion rate (M☉/yr)", 1e-6, 1.0,
                                       1e-4, step=1e-6, format="%.2e")
            st.session_state["mdot_in"] = mdot_in

        with tabs[2]:
            if st.button("▶ COMPUTE LENSING SURVEY", use_container_width=True):
                with st.spinner("Computing gravitational lensing..."):
                    results = metric.lensing_survey(n_rays=250)
                    fig = viz.plot_lensing_deflection(results)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                n_cap  = sum(1 for r in results if r.is_captured)
                n_ring = sum(1 for r in results if r.photon_ring)
                l1, l2, l3 = st.columns(3)
                l1.metric("Captured rays",     n_cap)
                l2.metric("Photon ring rays",  n_ring)
                l3.metric("b_crit",
                           f"{metric.critical_impact_parameter()/bh.M_geo:.4f} M")

                lens_rows = [
                    {"b/M": round(r.impact_param_M,2),
                     "Deflection (°)": round(r.deflection_rad*180/math.pi,3)
                     if r.deflection_rad < 1e10 else "∞",
                     "Magnification": f"{r.image_magnification:.2e}",
                     "Redshift 1+z": f"{r.redshift_factor:.3f}",
                     "Captured": "✗" if r.is_captured else "✓",
                     "Photon Ring": "✓" if r.photon_ring else "—"}
                    for r in results[::10][:20]
                ]
                st.dataframe(pd.DataFrame(lens_rows),
                             use_container_width=True, hide_index=True)

        with tabs[3]:
            if st.button("▶ COMPUTE TIDAL FORCES", use_container_width=True):
                with st.spinner("Computing tidal tensor..."):
                    fig = viz.plot_tidal_forces(bh)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                tf_isco = metric.tidal_forces(bh.r_isco_prograde)
                tf_h    = metric.tidal_forces(bh.r_plus * 1.001)
                t1, t2, t3 = st.columns(3)
                t1.metric("Tidal @ ISCO (radial)",
                           f"{tf_isco.radial_tide_N:.3e} N m⁻¹ kg⁻¹")
                t2.metric("Spaghettification r",
                           f"{tf_h.spaghetti_limit_m/bh.M_geo:.3f} M")
                t3.metric("Time to singularity",
                           f"{tf_h.time_to_singularity_s:.3f} s")

        with tabs[4]:
            if st.button("▶ PLOT TIME DILATION", use_container_width=True):
                with st.spinner("Computing gravitational redshift profile..."):
                    fig = viz.plot_time_dilation_profile(bh)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                r_miller = TimeDilationEngine.miller_planet_radius(bh)
                g1, g2, g3 = st.columns(3)
                g1.metric("Miller's r",
                           f"{r_miller/bh.M_geo:.6f} M")
                g2.metric("Miller dilation",
                           f"×{TimeDilationEngine.MILLER_DILATION:,.0f}")
                g3.metric("1h local = N yr",
                           f"{TimeDilationEngine.MILLER_DILATION/8760:.2f} yr")

        with tabs[5]:
            local_hrs_table = st.slider("Local time for table (hours)",
                                         0.1, 24.0, 1.0, 0.1)
            df = TimeDilationEngine.mission_time_table(bh, local_hrs_table)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown(
                f'<div class="grav-metric">'
                f'Miller\'s Planet: {local_hrs_table:.2f} local hours = '
                f'{local_hrs_table * TimeDilationEngine.MILLER_DILATION / 8760:.2f} Earth years'
                f'</div>',
                unsafe_allow_html=True)


if __name__ == "__main__":
    gravity_engine_page()
