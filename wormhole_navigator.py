"""
wormhole_navigator.py — Wormhole Physics & Interstellar Navigation Engine
ENDURANCE Mission Control | Interstellar Science Platform v1.0.0

Handles: Morris-Thorne traversable wormhole geometry, exotic matter requirements,
         throat stability conditions, tidal force constraints, wormhole embedding
         diagrams, Ellis drainhole solution, Saturn approach trajectory, wormhole
         transit simulation, Lagrange point calculations, planetary system orbital
         mechanics (Gargantua system: Miller / Mann / Edmunds planets), Kepler
         orbital elements, Hohmann transfer calculations, gravitational assist,
         resonance conditions, coordinate transformations (BL ↔ Cartesian ↔
         Boyer-Lindquist), ENDURANCE trajectory planning, proper time integration
         along worldlines.

Canonical Interstellar wormhole (Kip Thorne, The Science of Interstellar, 2014):
  Location       : Near Saturn (≈ 1 AU from Saturn, ~9.58 AU from Sun)
  Throat radius  : b₀ ≈ 1 AU (≈ 1.496 × 10¹¹ m)
  Shape function : b(r) = b₀² / r  (Ellis drainhole)
  Exotic matter  : ρ_exotic < 0 (negative energy density required)
  Transit time   : ≈ 1 hour ship-frame (Thorne estimate)

"We didn't run out of time, time ran out on us."
                        — Cooper
"""

from __future__ import annotations

import math
import time
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import scipy.integrate as sci_int
import scipy.optimize as sci_opt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, Arc
import streamlit as st

warnings.filterwarnings("ignore")

# ── Physical constants ────────────────────────────────────────────────────────
G_SI      = 6.674_30e-11
C_SI      = 2.997_924_58e8
M_SUN     = 1.989e30
M_EARTH   = 5.972e24
R_EARTH   = 6.371e6
M_SATURN  = 5.683e26
R_SATURN  = 5.832e7
AU        = 1.495_978_707e11
LY        = 9.460_730_472e15
PC        = 3.085_677_581e16
YEAR_S    = 3.156e7
DAY_S     = 86_400.0
HBAR      = 1.054_571_817e-34
K_B       = 1.380_649e-23

# ── Mission canonical constants ───────────────────────────────────────────────
SATURN_SEMIMAJOR_AU   = 9.5826          # Saturn orbit
WORMHOLE_DIST_SAT_AU  = 1.0             # wormhole ~ 1 AU from Saturn (film)
WORMHOLE_THROAT_M     = 1.0 * AU        # throat radius b₀ (Thorne estimate)
GARGANTUA_MASS_SOLAR  = 1.0e8
GARGANTUA_DIST_LY     = 1.0e10          # effectively another galaxy

# ─────────────────────────────────────────────────────────────────────────────
# ENUMERATIONS
# ─────────────────────────────────────────────────────────────────────────────

class WormholeType(Enum):
    MORRIS_THORNE   = "MORRIS_THORNE"    # general traversable
    ELLIS_DRAINHOLE = "ELLIS_DRAINHOLE"  # b(r) = b₀²/r
    VISSER_THIN     = "VISSER_THIN"      # thin-shell constructed
    LORENTZIAN      = "LORENTZIAN"       # general Lorentzian

class PlanetID(Enum):
    MILLER   = "MILLER"     # water world, 1h=7yr, near Gargantua
    MANN     = "MANN"       # frozen ammonia clouds, betrayal
    EDMUNDS  = "EDMUNDS"    # Cooper's destination after Tesseract
    EARTH    = "EARTH"      # Sol III, reference
    SATURN   = "SATURN"     # wormhole location

class ManeuverType(Enum):
    HOHMANN          = "HOHMANN"
    BI_ELLIPTIC      = "BI_ELLIPTIC"
    GRAVITATIONAL_ASSIST = "GRAVITATIONAL_ASSIST"
    POWERED_FLYBY    = "POWERED_FLYBY"
    ORBITAL_INSERTION = "ORBITAL_INSERTION"

class TrajectoryPhase(Enum):
    EARTH_ORBIT      = "EARTH_ORBIT"
    TRANS_SATURN     = "TRANS_SATURN"
    SATURN_FLYBY     = "SATURN_FLYBY"
    WORMHOLE_TRANSIT = "WORMHOLE_TRANSIT"
    GARGANTUA_APPROACH = "GARGANTUA_APPROACH"
    PLANETARY_DESCENT  = "PLANETARY_DESCENT"
    ASCENT_RENDEZVOUS  = "ASCENT_RENDEZVOUS"
    TRANS_EARTH        = "TRANS_EARTH"

# ─────────────────────────────────────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class WormholeGeometry:
    """
    Morris-Thorne traversable wormhole parameterisation.
    Spacetime metric (spherically symmetric, static):
    ds² = -e^{2Φ(r)} c²dt² + dr²/(1 - b(r)/r) + r²dΩ²
    """
    throat_radius_m:    float           # b₀ — throat radius (metres)
    shape_exponent:     float = 2.0     # b(r) = b₀^n / r^(n-1), n=2 → Ellis
    redshift_fn:        str   = "zero"  # "zero" (Φ=0) or "logarithmic"
    wormhole_type:      WormholeType = WormholeType.ELLIS_DRAINHOLE

    def shape_function(self, r: float) -> float:
        """b(r): shape function. Ellis drainhole: b(r) = b₀²/r"""
        b0 = self.throat_radius_m
        n  = self.shape_exponent
        return b0**n / r**(n - 1)

    def flare_out_condition(self, r: float) -> float:
        """
        Flare-out condition (required for traversability):
        (b - b'r) / (2b²) > 0 at throat.
        Returns > 0 if satisfied.
        """
        b0  = self.throat_radius_m
        b   = self.shape_function(r)
        eps = r * 1e-6
        bp  = (self.shape_function(r + eps) - self.shape_function(r - eps)) / (2*eps)
        return (b - bp * r) / (2 * b**2) if b > 0 else 0.0

    def redshift_function(self, r: float) -> float:
        """Φ(r): redshift function. Zero-tidal-force case: Φ = 0."""
        if self.redshift_fn == "zero":
            return 0.0
        elif self.redshift_fn == "logarithmic":
            b0 = self.throat_radius_m
            return 0.5 * math.log(1 - b0 / r) if r > b0 else float("-inf")
        return 0.0

    def proper_radial_distance(self, r: float) -> float:
        """
        Proper radial coordinate l(r) mapping to/from coordinate r.
        dl/dr = ±1/sqrt(1 - b(r)/r)
        Integrate from throat b₀ to r.
        """
        b0 = self.throat_radius_m
        if r <= b0:
            return 0.0
        def integrand(rp):
            b = self.shape_function(rp)
            val = 1 - b/rp
            return 1.0 / math.sqrt(max(val, 1e-12))
        result, _ = sci_int.quad(integrand, b0 * 1.0001, r,
                                   limit=200, epsabs=1e-8)
        return float(result)

    def embedding_coordinates(self, r_vals: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the embedding diagram z(r) for the wormhole.
        dz/dr = ±1/sqrt(r/b(r) - 1)
        Shows curvature of 2D equatorial slice in flat 3D space.
        """
        b0 = self.throat_radius_m
        z_vals = np.zeros_like(r_vals)
        for i, r in enumerate(r_vals):
            if r <= b0 * 1.00001:
                z_vals[i] = 0.0
                continue
            def dz_dr(rp):
                b = self.shape_function(rp)
                val = rp / b - 1
                return 1.0 / math.sqrt(max(val, 1e-10))
            try:
                z, _ = sci_int.quad(dz_dr, b0 * 1.0001, r,
                                     limit=200, epsabs=1e-8)
                z_vals[i] = z
            except Exception:
                z_vals[i] = z_vals[max(0, i-1)]
        return r_vals, z_vals

    def exotic_matter_density(self, r: float) -> float:
        """
        Energy density of exotic matter required at radius r.
        From Einstein field equations for the wormhole metric:
        8πG ρ_exotic = -b'(r) / r²
        (negative → exotic matter required)
        Returns value in kg/m³.
        """
        eps = r * 1e-6
        bp  = (self.shape_function(r + eps) - self.shape_function(r - eps)) / (2*eps)
        rho_geo = -bp / (8 * math.pi * r**2)    # in c=G=1 units
        rho_si  = rho_geo * C_SI**2 / G_SI       # convert to SI
        return float(rho_si)

    def total_exotic_energy_J(self) -> float:
        """
        Total exotic energy integrated over the wormhole volume.
        E_exotic = ∫ ρ_exotic × 4πr² dr  from b₀ to ∞ (truncated)
        In practice truncated at 10 b₀.
        """
        b0    = self.throat_radius_m
        r_max = 10 * b0
        def integrand(r):
            rho = self.exotic_matter_density(r)
            return rho * 4 * math.pi * r**2
        try:
            E, _ = sci_int.quad(integrand, b0 * 1.001, r_max,
                                  limit=500, epsabs=1e-6)
            return float(E * C_SI**2)  # convert energy density × volume → Joules
        except Exception:
            return float("-inf")

    def transit_time_proper(self, v_over_c: float = 0.5) -> float:
        """
        Proper time for traversal through wormhole at constant velocity v.
        Δτ = L_total / (γ v)  where L_total = 2 × l(r_max)
        Use throat length ≈ 2 b₀ for order of magnitude.
        """
        b0   = self.throat_radius_m
        v    = v_over_c * C_SI
        beta = v_over_c
        gamma = 1.0 / math.sqrt(1 - beta**2)
        L_total = 2 * b0     # approximate proper length of wormhole
        return float(L_total / (gamma * v))

    def tidal_constraint_velocity(self, g_limit_earth: float = 10.0) -> float:
        """
        Maximum entry velocity for safe traversal (tidal forces ≤ g_limit × g_Earth).
        For Ellis drainhole: tidal acc ≈ c² b₀² / r³ at throat for radial geodesic.
        g_tidal = c² / b₀  → limit v such that Δτ × g_tidal ≤ g_limit × g_Earth.
        Returns maximum v/c for comfortable traversal.
        """
        g_earth = 9.81   # m s⁻²
        g_max   = g_limit_earth * g_earth
        b0      = self.throat_radius_m
        # Tidal acceleration at throat for radial geodesic: a_t ≈ c² Δl / b₀²
        # For human: Δl ≈ 1.8 m, a_t = C_SI² × 1.8 / b₀²
        a_tidal = C_SI**2 * 1.8 / b0**2
        if a_tidal < g_max:
            return 1.0   # completely comfortable at any speed
        # v_max such that traversal time gives tolerable impulse
        # tau_cross = b0 / (v_max) → impulse ~ a_t × tau_cross ≤ g_max × tau
        v_max = C_SI * math.sqrt(a_tidal / g_max * b0 / C_SI)
        return float(min(v_max / C_SI, 0.9999))

    def quantum_inequality_energy(self) -> float:
        """
        Ford-Roman quantum inequality: the exotic energy must satisfy
        |E_exotic| ≤ (ℏ c)/(b₀² τ) for sampling time τ ~ b₀/c.
        Returns the quantum inequality bound in Joules.
        """
        b0  = self.throat_radius_m
        tau = b0 / C_SI
        return float(HBAR * C_SI / (b0**2 * tau))


@dataclass
class OrbitalElements:
    """Keplerian orbital elements (J2000 epoch)."""
    semi_major_axis_m:  float           # a (metres)
    eccentricity:       float           # e [0,1)
    inclination_deg:    float           # i (degrees)
    raan_deg:           float           # Ω — right ascension of ascending node
    arg_periapsis_deg:  float           # ω — argument of periapsis
    mean_anomaly_deg:   float           # M₀ — mean anomaly at epoch
    central_mass_kg:    float           # M_central

    @property
    def semi_latus_rectum_m(self) -> float:
        return self.semi_major_axis_m * (1 - self.eccentricity**2)

    @property
    def period_s(self) -> float:
        """Keplerian period T = 2π sqrt(a³/μ)"""
        mu = G_SI * self.central_mass_kg
        return float(2 * math.pi * math.sqrt(self.semi_major_axis_m**3 / mu))

    @property
    def period_yr(self) -> float:
        return self.period_s / YEAR_S

    @property
    def mean_motion_rad_s(self) -> float:
        return 2 * math.pi / self.period_s

    @property
    def periapsis_m(self) -> float:
        return self.semi_major_axis_m * (1 - self.eccentricity)

    @property
    def apoapsis_m(self) -> float:
        return self.semi_major_axis_m * (1 + self.eccentricity)

    @property
    def orbital_velocity_circular_m_s(self) -> float:
        """v_c = sqrt(μ/a) for circular approximation."""
        mu = G_SI * self.central_mass_kg
        return float(math.sqrt(mu / self.semi_major_axis_m))

    @property
    def escape_velocity_periapsis_m_s(self) -> float:
        """v_esc = sqrt(2μ/r_p)"""
        mu = G_SI * self.central_mass_kg
        return float(math.sqrt(2 * mu / self.periapsis_m))

    def solve_kepler(self, mean_anomaly_deg: float,
                      tol: float = 1e-10) -> float:
        """
        Solve Kepler's equation M = E - e sin(E) for eccentric anomaly E.
        Newton-Raphson iteration.
        """
        M = math.radians(mean_anomaly_deg)
        e = self.eccentricity
        E = M   # initial guess
        for _ in range(100):
            dE = (M - E + e * math.sin(E)) / (1 - e * math.cos(E))
            E += dE
            if abs(dE) < tol:
                break
        return float(E)

    def true_anomaly_rad(self, mean_anomaly_deg: float) -> float:
        """Convert mean anomaly to true anomaly ν via eccentric anomaly."""
        E = self.solve_kepler(mean_anomaly_deg)
        e = self.eccentricity
        cos_nu = (math.cos(E) - e) / (1 - e * math.cos(E))
        sin_nu = (math.sqrt(1 - e**2) * math.sin(E)) / (1 - e * math.cos(E))
        return float(math.atan2(sin_nu, cos_nu))

    def position_velocity(self, mean_anomaly_deg: float
                           ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return position (m) and velocity (m/s) vectors in inertial frame.
        Uses perifocal → ECI rotation via Euler angles (Ω, i, ω).
        """
        nu  = self.true_anomaly_rad(mean_anomaly_deg)
        p   = self.semi_latus_rectum_m
        e   = self.eccentricity
        mu  = G_SI * self.central_mass_kg
        r   = p / (1 + e * math.cos(nu))
        # Perifocal coordinates
        pos_p = r * np.array([math.cos(nu), math.sin(nu), 0.0])
        vel_p = math.sqrt(mu / p) * np.array(
            [-math.sin(nu), e + math.cos(nu), 0.0])
        # Rotation matrix (ω, i, Ω)
        omega = math.radians(self.arg_periapsis_deg)
        inc   = math.radians(self.inclination_deg)
        Omega = math.radians(self.raan_deg)
        R = self._rotation_matrix(omega, inc, Omega)
        return R @ pos_p, R @ vel_p

    @staticmethod
    def _rotation_matrix(omega: float, inc: float, Omega: float) -> np.ndarray:
        co, so = math.cos(omega), math.sin(omega)
        ci, si = math.cos(inc),   math.sin(inc)
        cO, sO = math.cos(Omega), math.sin(Omega)
        return np.array([
            [cO*co - sO*so*ci, -cO*so - sO*co*ci,  sO*si],
            [sO*co + cO*so*ci, -sO*so + cO*co*ci, -cO*si],
            [so*si,             co*si,              ci   ],
        ])


@dataclass
class PlanetData:
    """Physical and orbital properties of a planet in the Gargantua system or Solar System."""
    planet_id:          PlanetID
    name:               str
    mass_kg:            float
    radius_m:           float
    surface_gravity_m_s2: float
    orbital_elements:   OrbitalElements
    time_dilation_factor: float = 1.0     # γ_total relative to Earth
    description:        str = ""
    surface_conditions: str = ""
    discovered_by:      str = ""

    @property
    def escape_velocity_m_s(self) -> float:
        return math.sqrt(2 * G_SI * self.mass_kg / self.radius_m)

    @property
    def hill_sphere_m(self) -> float:
        """Hill sphere approximation: r_H = a (m/(3M))^(1/3)"""
        M_central = self.orbital_elements.central_mass_kg
        return (self.orbital_elements.semi_major_axis_m *
                (self.mass_kg / (3 * M_central))**(1/3))


# ─────────────────────────────────────────────────────────────────────────────
# SOLAR SYSTEM REFERENCE DATA
# ─────────────────────────────────────────────────────────────────────────────

def build_solar_system_planets() -> Dict[str, OrbitalElements]:
    """Reference orbital elements for solar system bodies (J2000)."""
    M_sol = 1.989e30
    planets = {
        "Earth": OrbitalElements(
            semi_major_axis_m=1.000 * AU, eccentricity=0.0167,
            inclination_deg=0.0, raan_deg=0.0, arg_periapsis_deg=102.94,
            mean_anomaly_deg=100.46, central_mass_kg=M_sol),
        "Saturn": OrbitalElements(
            semi_major_axis_m=9.5826 * AU, eccentricity=0.0565,
            inclination_deg=2.485, raan_deg=113.64, arg_periapsis_deg=339.39,
            mean_anomaly_deg=317.02, central_mass_kg=M_sol),
        "Jupiter": OrbitalElements(
            semi_major_axis_m=5.2044 * AU, eccentricity=0.0489,
            inclination_deg=1.305, raan_deg=100.46, arg_periapsis_deg=273.87,
            mean_anomaly_deg=20.02, central_mass_kg=M_sol),
        "Mars": OrbitalElements(
            semi_major_axis_m=1.5237 * AU, eccentricity=0.0934,
            inclination_deg=1.850, raan_deg=49.56, arg_periapsis_deg=286.50,
            mean_anomaly_deg=19.37, central_mass_kg=M_sol),
    }
    return planets


# ─────────────────────────────────────────────────────────────────────────────
# GARGANTUA PLANETARY SYSTEM
# ─────────────────────────────────────────────────────────────────────────────

def build_gargantua_system(bh_mass_solar: float = GARGANTUA_MASS_SOLAR
                            ) -> List[PlanetData]:
    """
    Canonical Gargantua planetary system from Kip Thorne's analysis.
    All orbits are equatorial (prograde) around Gargantua.
    """
    M_G    = bh_mass_solar * M_SUN
    M_G_geo = G_SI * M_G / C_SI**2   # geometric mass in metres

    # Kerr ISCO for a* = 1-1e-14 ≈ 1.0 (prograde)
    # r_ISCO → M (event horizon) for extreme Kerr
    # Thorne: Miller r ≈ 1.001 r_H for a*→1
    r_H_approx = M_G_geo           # r_+ ≈ M for extreme Kerr
    r_miller   = M_G_geo * 1.0027  # Thorne canonical
    r_mann     = M_G_geo * 50.0    # much further out
    r_edmunds  = M_G_geo * 100.0   # furthest, near habitable zone

    planets = [
        PlanetData(
            planet_id=PlanetID.MILLER,
            name="Miller's Planet",
            mass_kg=5.972e24 * 1.2,      # slightly heavier than Earth
            radius_m=6.371e6 * 1.3,
            surface_gravity_m_s2=14.0,   # ~1.4g
            orbital_elements=OrbitalElements(
                semi_major_axis_m=r_miller,
                eccentricity=0.0,          # circular (tidal locking)
                inclination_deg=0.0,
                raan_deg=0.0, arg_periapsis_deg=0.0, mean_anomaly_deg=0.0,
                central_mass_kg=M_G),
            time_dilation_factor=61_320.0,  # 1 h = 7 yr
            description=(
                "Shallow ocean world, ~10 cm average depth. Enormous "
                "tidal waves (hundreds of metres) driven by Gargantua tidal forces. "
                "The 1-hour surface mission costs Cooper 23 years aboard Endurance."),
            surface_conditions="Liquid water, ~1 atm, 1.4g surface gravity. "
                                "Continuous 100m+ tidal bore waves. No dry land.",
            discovered_by="Dr. Miller (deceased — wave)"
        ),
        PlanetData(
            planet_id=PlanetID.MANN,
            name="Mann's Planet",
            mass_kg=5.972e24 * 0.9,
            radius_m=6.371e6 * 0.95,
            surface_gravity_m_s2=8.5,
            orbital_elements=OrbitalElements(
                semi_major_axis_m=r_mann,
                eccentricity=0.02,
                inclination_deg=3.0,
                raan_deg=45.0, arg_periapsis_deg=90.0, mean_anomaly_deg=180.0,
                central_mass_kg=M_G),
            time_dilation_factor=1.3,    # minimal dilation at large r
            description=(
                "Frozen ammonia-methane cloud layers over rocky core. "
                "Habitable zone only in thin stratospheric layer. "
                "Dr. Mann falsified viability data to trigger rescue. "
                "Surface shows banded ice structure, extreme cold."),
            surface_conditions="Frozen surface, ammonia ice, -40°C average. "
                                "Stratosphere: 0.8 atm N₂/O₂ mix. ~0.87g.",
            discovered_by="Dr. Mann"
        ),
        PlanetData(
            planet_id=PlanetID.EDMUNDS,
            name="Edmunds' Planet",
            mass_kg=5.972e24 * 1.05,
            radius_m=6.371e6 * 1.02,
            surface_gravity_m_s2=10.2,
            orbital_elements=OrbitalElements(
                semi_major_axis_m=r_edmunds,
                eccentricity=0.05,
                inclination_deg=5.0,
                raan_deg=120.0, arg_periapsis_deg=200.0, mean_anomaly_deg=60.0,
                central_mass_kg=M_G),
            time_dilation_factor=1.1,
            description=(
                "Rocky, oxygen-bearing atmosphere. Most Earth-like of the three. "
                "Where Amelia Brand sets up permanent human colony per Plan B. "
                "Cooper's data from the tesseract eventually reaches Brand here."),
            surface_conditions="Rocky terrain, thin O₂ atmosphere, ~1.04g, "
                                "-5°C mean temperature. Small liquid water bodies.",
            discovered_by="Dr. Edmunds (deceased — accident)"
        ),
    ]
    return planets


# ─────────────────────────────────────────────────────────────────────────────
# HOHMANN & ORBITAL TRANSFER CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────

class OrbitalMechanics:
    """
    Keplerian orbital mechanics: Hohmann transfers, gravity assists,
    Lagrange points, escape trajectories, Δv budgets.
    """

    @staticmethod
    def hohmann_transfer(r1_m: float, r2_m: float,
                          central_mass_kg: float
                          ) -> Dict[str, float]:
        """
        Hohmann transfer from circular orbit r₁ to r₂.
        Δv₁ = v_c1 (sqrt(2r₂/(r₁+r₂)) - 1)
        Δv₂ = v_c2 (1 - sqrt(2r₁/(r₁+r₂)))
        """
        mu    = G_SI * central_mass_kg
        v_c1  = math.sqrt(mu / r1_m)
        v_c2  = math.sqrt(mu / r2_m)
        r_t   = (r1_m + r2_m) / 2         # semi-major axis of transfer ellipse
        v_t1  = math.sqrt(mu * (2/r1_m - 1/r_t))
        v_t2  = math.sqrt(mu * (2/r2_m - 1/r_t))
        dv1   = abs(v_t1 - v_c1)
        dv2   = abs(v_c2 - v_t2)
        T_half= math.pi * math.sqrt(r_t**3 / mu)   # half-period = transfer time
        return {
            "dv1_m_s":        float(dv1),
            "dv2_m_s":        float(dv2),
            "dv_total_m_s":   float(dv1 + dv2),
            "transfer_time_s":float(T_half),
            "transfer_time_yr":float(T_half / YEAR_S),
            "a_transfer_m":   float(r_t),
            "v_periapsis_m_s":float(v_t1),
            "v_apoapsis_m_s": float(v_t2),
            "v_c1_m_s":       float(v_c1),
            "v_c2_m_s":       float(v_c2),
        }

    @staticmethod
    def gravity_assist_delta_v(v_inf_m_s: float,
                                 flyby_body_mass_kg: float,
                                 flyby_radius_m: float,
                                 deflection_angle_deg: float) -> float:
        """
        Gravity assist Δv: change in heliocentric speed due to flyby.
        Δv = 2 v_∞ sin(δ/2) where δ is deflection angle.
        Deflection angle limited by: sin(δ_max/2) = 1/(1 + r_p v_∞²/(GM_planet))
        """
        mu_planet = G_SI * flyby_body_mass_kg
        v_esc_sq  = 2 * mu_planet / flyby_radius_m
        # Max deflection
        eps    = (flyby_radius_m * v_inf_m_s**2) / mu_planet  # hyperbolic excess
        delta_max = 2 * math.asin(1 / (1 + eps))
        delta = math.radians(min(deflection_angle_deg,
                                  math.degrees(delta_max)))
        return float(2 * v_inf_m_s * math.sin(delta / 2))

    @staticmethod
    def lagrange_points(r_orbit_m: float, M_primary_kg: float,
                         M_secondary_kg: float) -> Dict[str, float]:
        """
        Lagrange point distances L1–L5 for circular restricted 3-body problem.
        Returns distances from secondary body.
        μ = M₂/(M₁+M₂)
        """
        mu_r = M_secondary_kg / (M_primary_kg + M_secondary_kg)  # mass ratio
        r    = r_orbit_m   # orbital radius of secondary
        # L1: between bodies, distance from secondary ≈ r (μ/3)^(1/3)
        d_L1 = r * (mu_r / 3)**(1/3)
        # L2: beyond secondary ≈ same
        d_L2 = r * (mu_r / 3)**(1/3)
        # L3: opposite side, distance from primary ≈ r (1 - 5μ/12)
        d_L3 = r * (1 - 5*mu_r/12)
        # L4, L5: equilateral triangle (distance = r from both)
        d_L4 = r
        d_L5 = r
        return {
            "L1_from_secondary_m":  float(d_L1),
            "L2_from_secondary_m":  float(d_L2),
            "L3_from_primary_m":    float(d_L3),
            "L4_distance_m":        float(d_L4),
            "L5_distance_m":        float(d_L5),
        }

    @staticmethod
    def tsiolkovsky_rocket(dv_m_s: float,
                            specific_impulse_s: float,
                            payload_mass_kg: float) -> Dict[str, float]:
        """
        Tsiolkovsky rocket equation: Δv = v_e ln(m₀/m_f)
        v_e = Isp × g₀, m₀ = initial mass, m_f = final (dry) mass.
        """
        g0   = 9.81   # m/s²
        v_e  = specific_impulse_s * g0
        mass_ratio = math.exp(dv_m_s / v_e)
        propellant_mass = payload_mass_kg * (mass_ratio - 1)
        total_mass      = payload_mass_kg * mass_ratio
        return {
            "mass_ratio":        float(mass_ratio),
            "propellant_mass_kg":float(propellant_mass),
            "total_initial_kg":  float(total_mass),
            "v_exhaust_m_s":     float(v_e),
        }

    @staticmethod
    def vis_viva(r_m: float, a_m: float, mu: float) -> float:
        """Vis-viva equation: v² = μ(2/r - 1/a)"""
        return float(math.sqrt(abs(mu * (2/r_m - 1/a_m))))

    @staticmethod
    def orbital_period(a_m: float, central_mass_kg: float) -> float:
        """T = 2π sqrt(a³/μ)"""
        mu = G_SI * central_mass_kg
        return float(2 * math.pi * math.sqrt(a_m**3 / mu))

    @staticmethod
    def escape_velocity(r_m: float, mass_kg: float) -> float:
        """v_esc = sqrt(2GM/r)"""
        return float(math.sqrt(2 * G_SI * mass_kg / r_m))

    @staticmethod
    def circular_orbit_velocity(r_m: float, mass_kg: float) -> float:
        return float(math.sqrt(G_SI * mass_kg / r_m))

    @staticmethod
    def synodic_period(T1_yr: float, T2_yr: float) -> float:
        """Synodic period: 1/T_syn = |1/T1 - 1/T2|"""
        if abs(T1_yr - T2_yr) < 1e-10:
            return float("inf")
        return float(1.0 / abs(1/T1_yr - 1/T2_yr))


# ─────────────────────────────────────────────────────────────────────────────
# ENDURANCE MISSION TRAJECTORY
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class MissionLeg:
    phase:          TrajectoryPhase
    origin:         str
    destination:    str
    delta_v_m_s:    float
    duration_s:     float
    local_years:    float       # crew experienced time
    earth_years:    float       # Earth elapsed time
    dilation_factor: float
    notes:          str = ""

    @property
    def duration_yr(self) -> float:
        return self.duration_s / YEAR_S


class EnduranceMission:
    """
    Reconstructed Endurance mission trajectory with relativistic time accounting.
    Based on Kip Thorne's canonical timeline (The Science of Interstellar, 2014).
    """

    # Mission constants
    ENDURANCE_DRY_MASS_KG    = 2.0e5     # 200 tonnes (estimate)
    RANGER_MASS_KG           = 3.0e4
    LANDER_MASS_KG           = 2.0e4
    ISP_CHEMICAL_S           = 450       # chemical rocket Isp (LOX/LH2)
    ISP_NUCLEAR_S            = 900       # nuclear thermal Isp

    MISSION_START_YEAR       = 2067      # canonical (film implied ~2067)
    SATURN_TRANSIT_YR        = 2.0       # Earth-to-Saturn travel time (yr)

    def build_trajectory(self) -> List[MissionLeg]:
        """
        Reconstruct the complete Endurance mission trajectory
        with proper time accounting.
        """
        M_sol = M_SUN
        mu_sun = G_SI * M_sol

        # Leg 1: Earth → Saturn (Hohmann, 2 years)
        h = OrbitalMechanics.hohmann_transfer(1.0*AU, 9.58*AU, M_sol)
        leg1 = MissionLeg(
            phase=TrajectoryPhase.TRANS_SATURN,
            origin="Earth Orbit (LEO)",
            destination="Saturn Vicinity",
            delta_v_m_s=h["dv_total_m_s"],
            duration_s=h["transfer_time_s"],
            local_years=h["transfer_time_yr"],
            earth_years=h["transfer_time_yr"],
            dilation_factor=1.000_001,   # negligible at v ~ 5 km/s
            notes=f"Hohmann transfer. Δv={h['dv_total_m_s']/1e3:.2f} km/s"
        )

        # Leg 2: Wormhole transit (1 hour ship-frame)
        wh = WormholeGeometry(WORMHOLE_THROAT_M)
        t_wh = wh.transit_time_proper(v_over_c=0.5)
        leg2 = MissionLeg(
            phase=TrajectoryPhase.WORMHOLE_TRANSIT,
            origin="Saturn Wormhole Entry",
            destination="Gargantua System",
            delta_v_m_s=0.0,
            duration_s=t_wh,
            local_years=t_wh / YEAR_S,
            earth_years=t_wh / YEAR_S,   # traversable wormhole: no dilation if Φ=0
            dilation_factor=1.0,
            notes=f"Morris-Thorne transit at v=0.5c. τ={t_wh:.0f} s ≈ {t_wh/3600:.2f} h"
        )

        # Leg 3: Gargantua approach (film timeline: several months ship)
        leg3 = MissionLeg(
            phase=TrajectoryPhase.GARGANTUA_APPROACH,
            origin="Wormhole Exit",
            destination="Miller's Planet Approach",
            delta_v_m_s=5e3,
            duration_s=6 * 30 * DAY_S,
            local_years=0.5,
            earth_years=0.5,
            dilation_factor=1.05,
            notes="Deceleration into Gargantua system, orbital insertion."
        )

        # Leg 4: Miller's Planet (1 hour local = 7 years Earth)
        leg4 = MissionLeg(
            phase=TrajectoryPhase.PLANETARY_DESCENT,
            origin="Endurance Parking Orbit",
            destination="Miller's Planet Surface",
            delta_v_m_s=8e3,
            duration_s=1.0 * 3600,          # 1 hour local
            local_years=1.0 / 8760,
            earth_years=7.0,                 # 7 years Earth
            dilation_factor=61_320.0,
            notes="CATASTROPHIC DILATION: 1 h local = 7 Earth years. Wave event."
        )

        # Leg 5: Return to Endurance + Mann approach (23 years lost)
        leg5 = MissionLeg(
            phase=TrajectoryPhase.ASCENT_RENDEZVOUS,
            origin="Miller's Planet",
            destination="Mann's Planet Trajectory",
            delta_v_m_s=6e3,
            duration_s=0.5 * YEAR_S,
            local_years=0.5,
            earth_years=0.5,
            dilation_factor=1.1,
            notes="23 years elapsed on Endurance during Miller mission."
        )

        # Leg 6: Mann's Planet + betrayal (several weeks)
        leg6 = MissionLeg(
            phase=TrajectoryPhase.PLANETARY_DESCENT,
            origin="En route",
            destination="Mann's Planet",
            delta_v_m_s=7e3,
            duration_s=21 * DAY_S,
            local_years=21/365,
            earth_years=21/365 * 1.3,
            dilation_factor=1.3,
            notes="Dr. Mann sabotage. Ranger destroyed. Cooper EVA recovery."
        )

        # Leg 7: Gargantua slingshot (Brand to Edmunds, Cooper into BH)
        leg7 = MissionLeg(
            phase=TrajectoryPhase.ASCENT_RENDEZVOUS,
            origin="Mann's Planet",
            destination="Gargantua Penrose Slingshot",
            delta_v_m_s=0.0,
            duration_s=2 * DAY_S,
            local_years=2/365,
            earth_years=2/365,
            dilation_factor=1.0,
            notes="Penrose process slingshot: extracts rotational energy from Gargantua."
        )

        # Leg 8: Cooper into Tesseract (timeless)
        leg8 = MissionLeg(
            phase=TrajectoryPhase.PLANETARY_DESCENT,
            origin="Event Horizon",
            destination="Tesseract / 5D Bulk",
            delta_v_m_s=0.0,
            duration_s=0.0,
            local_years=0.0,
            earth_years=0.0,
            dilation_factor=float("inf"),
            notes="Cooper crosses event horizon. TARS transmits quantum gravity data. "
                  "Tesseract constructed by future humans in bulk. Cooper extracts data."
        )

        return [leg1, leg2, leg3, leg4, leg5, leg6, leg7, leg8]

    def total_earth_elapsed(self, legs: List[MissionLeg]) -> float:
        return sum(l.earth_years for l in legs if l.earth_years != float("inf"))

    def total_crew_elapsed(self, legs: List[MissionLeg]) -> float:
        return sum(l.local_years for l in legs if l.local_years != float("inf"))

    def delta_v_budget(self, legs: List[MissionLeg]) -> float:
        return sum(l.delta_v_m_s for l in legs)

    def trajectory_dataframe(self, legs: List[MissionLeg]) -> pd.DataFrame:
        rows = []
        cumulative_earth = 0.0
        cumulative_crew  = 0.0
        for i, leg in enumerate(legs):
            if leg.earth_years != float("inf"):
                cumulative_earth += leg.earth_years
                cumulative_crew  += leg.local_years
            rows.append({
                "Leg":           i + 1,
                "Phase":         leg.phase.value.replace("_"," "),
                "Origin":        leg.origin,
                "Destination":   leg.destination,
                "Δv (km/s)":     round(leg.delta_v_m_s / 1e3, 2),
                "Local (yr)":    f"{leg.local_years:.4f}",
                "Earth (yr)":    f"{leg.earth_years:.3f}" if leg.earth_years != float("inf") else "∞",
                "Dilation":      (f"×{leg.dilation_factor:,.0f}"
                                  if leg.dilation_factor < 1e10 else "∞"),
                "Cumul. Earth":  round(cumulative_earth, 3),
                "Cumul. Crew":   round(cumulative_crew, 4),
                "Notes":         leg.notes[:60],
            })
        return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────────
# WORMHOLE TRANSIT SIMULATOR
# ─────────────────────────────────────────────────────────────────────────────

class WormholeTransit:
    """
    Simulate the traversal trajectory through the wormhole,
    tracking proper time, tidal forces, and coordinate position.
    """

    def __init__(self, wh: WormholeGeometry, v_entry_over_c: float = 0.5):
        self.wh = wh
        self.v  = v_entry_over_c * C_SI
        self.beta = v_entry_over_c
        self.gamma = 1.0 / math.sqrt(1 - v_entry_over_c**2)

    def simulate(self, n_steps: int = 500) -> pd.DataFrame:
        """
        Simulate proper time, coordinate time, tidal forces along transit.
        """
        b0 = self.wh.throat_radius_m
        # Total coordinate length of wormhole: traverse from -5b₀ to +5b₀
        r_vals = np.linspace(b0 * 5, b0 * 1.00001, n_steps // 2)
        r_vals = np.concatenate([r_vals, r_vals[::-1]])   # approach + recede
        l_vals = np.array([self.wh.proper_radial_distance(r) for r in r_vals])

        rows = []
        tau_cumul = 0.0
        t_cumul   = 0.0
        for i in range(len(r_vals)):
            r    = r_vals[i]
            l    = l_vals[i]
            dl   = abs(l_vals[i] - l_vals[max(0, i-1)])
            # Proper time increment
            dtau = dl / (self.gamma * self.v) if self.v > 0 else 0.0
            dt   = dl / self.v if self.v > 0 else 0.0
            tau_cumul += dtau
            t_cumul   += dt
            # Tidal acceleration at this r
            b  = self.wh.shape_function(r)
            # For Ellis drainhole: radial tidal acc ≈ C² b₀²/r³ × Δl
            a_tidal = C_SI**2 * b0**2 / max(r,b0)**3 * 1.8 if r > 0 else 0.0
            rows.append({
                "proper_radial_m":   float(l),
                "coord_r_m":         float(r),
                "proper_time_s":     float(tau_cumul),
                "coord_time_s":      float(t_cumul),
                "tidal_acc_m_s2":    float(a_tidal),
                "b_r_m":             float(b),
                "phase":             "approach" if i < n_steps//2 else "recede",
            })
        return pd.DataFrame(rows)

    def summary(self) -> Dict[str, float]:
        b0 = self.wh.throat_radius_m
        t_proper = self.wh.transit_time_proper(self.beta)
        t_coord  = t_proper * self.gamma
        a_max    = C_SI**2 * b0**2 / (b0**3) * 1.8
        return {
            "proper_time_s":        t_proper,
            "proper_time_h":        t_proper / 3600,
            "coordinate_time_s":    t_coord,
            "coordinate_time_h":    t_coord / 3600,
            "entry_speed_m_s":      self.v,
            "lorentz_factor":       self.gamma,
            "peak_tidal_m_s2":      a_max,
            "peak_tidal_g":         a_max / 9.81,
            "exotic_energy_J":      self.wh.total_exotic_energy_J(),
            "QI_bound_J":           self.wh.quantum_inequality_energy(),
            "v_safe_max_c":         self.wh.tidal_constraint_velocity(10.0),
        }


# ─────────────────────────────────────────────────────────────────────────────
# VISUALISER
# ─────────────────────────────────────────────────────────────────────────────

class WormholeVisualizer:
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
        "gold":   "#ffd700",
    }
    _IST_COLOURS = [
        (0.02, 0.01, 0.04), (0.05, 0.03, 0.12), (0.12, 0.06, 0.30),
        (0.25, 0.15, 0.55), (0.45, 0.35, 0.80), (0.70, 0.60, 0.95),
        (0.90, 0.85, 1.00),
    ]
    IST_CMAP = LinearSegmentedColormap.from_list("wormhole", _IST_COLOURS)

    def _style(self, ax, title=""):
        ax.set_facecolor(self.PAL["bg"])
        for sp in ax.spines.values():
            sp.set_edgecolor(self.PAL["dim"])
        ax.tick_params(colors=self.PAL["axis"], labelsize=6)
        ax.grid(True, color=self.PAL["grid"], alpha=0.4, ls=":")
        if title:
            ax.set_title(title, color=self.PAL["fg"], fontsize=8,
                         loc="left", pad=4, fontfamily="monospace")

    def plot_embedding_diagram(self, wh: WormholeGeometry,
                                figsize=(10, 5)) -> plt.Figure:
        """
        3D-style embedding diagram of wormhole throat geometry.
        Shows the spatial curvature of the equatorial slice.
        """
        b0     = wh.throat_radius_m
        r_vals = np.linspace(b0 * 1.0001, b0 * 8, 300)
        r_AU   = r_vals / AU
        b0_AU  = b0 / AU
        _, z_vals = wh.embedding_coordinates(r_vals)
        z_AU = z_vals / AU

        fig = plt.figure(figsize=figsize, facecolor=self.PAL["bg"])
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection="polar")

        # 2D cross-section
        # Upper universe
        ax1.plot(r_AU, z_AU,   color=self.PAL["acc"],  lw=1.5, label="Upper universe")
        ax1.plot(r_AU, -z_AU,  color=self.PAL["blue"], lw=1.5, label="Lower universe")
        ax1.fill_between(r_AU, z_AU, -z_AU, alpha=0.06, color=self.PAL["purple"])
        ax1.axvline(b0_AU, color=self.PAL["red"], lw=0.9, ls="--",
                     label=f"Throat b₀ = {b0_AU:.2f} AU")
        ax1.axhline(0, color=self.PAL["dim"], lw=0.5)
        self._style(ax1, "WORMHOLE EMBEDDING DIAGRAM — CROSS-SECTION")
        ax1.set_xlabel("Radial coord r (AU)", fontsize=6, color=self.PAL["fg"])
        ax1.set_ylabel("Embedding height z (AU)", fontsize=6, color=self.PAL["fg"])
        ax1.legend(fontsize=6, facecolor=self.PAL["bg"],
                   edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"])

        # Polar view: shape of throat
        theta_vals = np.linspace(0, 2*math.pi, 300)
        radii_polar = np.ones(300) * b0_AU + z_AU[0]   # approximate equatorial
        ax2.plot(theta_vals, np.abs(z_AU[0]) * np.ones(300) + b0_AU,
                  color=self.PAL["acc"], lw=1.2)
        ax2.set_facecolor(self.PAL["bg"])
        ax2.tick_params(colors=self.PAL["axis"], labelsize=5)
        ax2.set_title("THROAT CROSS-SECTION", color=self.PAL["fg"],
                       fontsize=7, fontfamily="monospace", pad=8)
        ax2.spines["polar"].set_edgecolor(self.PAL["dim"])
        ax2.grid(color=self.PAL["grid"], alpha=0.4)

        plt.tight_layout(pad=0.5)
        return fig

    def plot_exotic_matter(self, wh: WormholeGeometry,
                            figsize=(9, 4)) -> plt.Figure:
        """Plot exotic matter density and cumulative energy vs radius."""
        b0     = wh.throat_radius_m
        r_vals = np.linspace(b0 * 1.001, b0 * 15, 400)
        r_AU   = r_vals / AU
        rho_vals = np.array([wh.exotic_matter_density(r) for r in r_vals])

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize,
                                        facecolor=self.PAL["bg"])
        ax1.semilogy(r_AU, np.abs(rho_vals), color=self.PAL["purple"], lw=1.2)
        ax1.axvline(b0/AU, color=self.PAL["red"], lw=0.8, ls="--",
                     label=f"Throat b₀ = {b0/AU:.2f} AU")
        self._style(ax1, "EXOTIC MATTER ENERGY DENSITY |ρ| (kg/m³)")
        ax1.set_xlabel("r (AU)", fontsize=6, color=self.PAL["fg"])
        ax1.set_ylabel("|ρ_exotic| (kg m⁻³)", fontsize=6, color=self.PAL["fg"])
        ax1.legend(fontsize=6, facecolor=self.PAL["bg"],
                   edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"])

        # Cumulative energy
        rho_arr = np.array([abs(wh.exotic_matter_density(r)) for r in r_vals])
        vol_arr = 4 * math.pi * r_vals**2 * np.gradient(r_vals)
        cum_E   = np.cumsum(rho_arr * vol_arr) * C_SI**2
        ax2.semilogy(r_AU, cum_E + 1, color=self.PAL["orange"], lw=1.2)
        ax2.axhline(wh.quantum_inequality_energy(), color=self.PAL["green"],
                     lw=0.8, ls="--", label="Quantum inequality bound")
        self._style(ax2, "CUMULATIVE EXOTIC ENERGY (J)")
        ax2.set_xlabel("r (AU)", fontsize=6, color=self.PAL["fg"])
        ax2.set_ylabel("E_exotic (J)", fontsize=6, color=self.PAL["fg"])
        ax2.legend(fontsize=6, facecolor=self.PAL["bg"],
                   edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"])
        plt.tight_layout(pad=0.5)
        return fig

    def plot_mission_timeline(self, legs: List[MissionLeg],
                               figsize=(12, 5)) -> plt.Figure:
        """
        Visual timeline comparing Earth time vs crew experienced time
        for each mission leg.
        """
        fig, (ax_e, ax_c) = plt.subplots(2, 1, figsize=figsize,
                                           facecolor=self.PAL["bg"],
                                           sharex=False)
        earth_vals  = [l.earth_years for l in legs if l.earth_years < 1e9]
        crew_vals   = [l.local_years for l in legs if l.local_years < 1e9]
        labels      = [f"Leg {i+1}\n{l.phase.value[:8]}"
                       for i, l in enumerate(legs) if l.earth_years < 1e9]
        x           = np.arange(len(labels))

        cols_e = [self.PAL["acc"] if v < 1 else
                  self.PAL["warn"] if v < 5 else
                  self.PAL["red"] for v in earth_vals]
        cols_c = [self.PAL["green"] if v < 1 else
                  self.PAL["blue"] for v in crew_vals]

        ax_e.bar(x, earth_vals, color=cols_e, alpha=0.82, width=0.65)
        for i, v in enumerate(earth_vals):
            ax_e.text(i, v + 0.05, f"{v:.2f}", ha="center", va="bottom",
                       fontsize=6, color=self.PAL["fg"], fontfamily="monospace")
        self._style(ax_e, "EARTH ELAPSED TIME PER LEG (years)")
        ax_e.set_xticks(x)
        ax_e.set_xticklabels(labels, fontsize=5, color=self.PAL["axis"])
        ax_e.set_ylabel("Earth years", fontsize=6, color=self.PAL["fg"])

        ax_c.bar(x, crew_vals, color=cols_c, alpha=0.82, width=0.65)
        for i, v in enumerate(crew_vals):
            ax_c.text(i, v + 0.001, f"{v:.3f}", ha="center", va="bottom",
                       fontsize=6, color=self.PAL["fg"], fontfamily="monospace")
        self._style(ax_c, "CREW EXPERIENCED TIME PER LEG (years)")
        ax_c.set_xticks(x)
        ax_c.set_xticklabels(labels, fontsize=5, color=self.PAL["axis"])
        ax_c.set_ylabel("Crew years", fontsize=6, color=self.PAL["fg"])

        plt.tight_layout(pad=0.5)
        return fig

    def plot_orbital_map(self, planets: List[PlanetData],
                          figsize=(9, 9)) -> plt.Figure:
        """Top-down map of Gargantua planetary system."""
        fig, ax = plt.subplots(figsize=figsize, facecolor=self.PAL["bg"],
                                subplot_kw={"projection": "polar"})
        ax.set_facecolor(self.PAL["bg"])

        # Gargantua at centre
        ax.plot(0, 0, "o", color=self.PAL["acc"], markersize=14,
                 zorder=5, label="Gargantua")

        planet_colours = {
            PlanetID.MILLER:  self.PAL["blue"],
            PlanetID.MANN:    self.PAL["red"],
            PlanetID.EDMUNDS: self.PAL["green"],
        }
        for planet in planets:
            r_M = planet.orbital_elements.semi_major_axis_m
            e   = planet.orbital_elements.eccentricity
            col = planet_colours.get(planet.planet_id, self.PAL["fg"])
            # Draw orbit ellipse (parametric)
            nu_vals = np.linspace(0, 2*math.pi, 300)
            p       = r_M * (1 - e**2)
            r_orbit = p / (1 + e * np.cos(nu_vals))
            # Normalise by some reference (Miller radius)
            r_ref = planets[0].orbital_elements.semi_major_axis_m
            ax.plot(nu_vals, r_orbit / r_ref, color=col, lw=1.0,
                     alpha=0.6, ls="--")
            # Planet position at mean anomaly 0
            ax.plot(0, r_M / r_ref, "o", color=col, markersize=8, zorder=4,
                     label=planet.name)
            ax.text(0.1, r_M / r_ref, f"  {planet.name}", color=col,
                     fontsize=6, fontfamily="monospace", va="center")

        ax.set_title("GARGANTUA PLANETARY SYSTEM — TOP VIEW",
                      color=self.PAL["acc"], fontsize=8,
                      fontfamily="monospace", pad=12)
        ax.tick_params(colors=self.PAL["axis"], labelsize=5)
        ax.spines["polar"].set_edgecolor(self.PAL["dim"])
        ax.grid(color=self.PAL["grid"], alpha=0.4)
        ax.legend(fontsize=6, facecolor=self.PAL["bg"],
                  edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"],
                  loc="upper right")
        plt.tight_layout(pad=0.5)
        return fig

    def plot_transit_simulation(self, df: pd.DataFrame,
                                 figsize=(10, 5)) -> plt.Figure:
        """Visualise the wormhole transit: tidal forces, proper time."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize,
                                        facecolor=self.PAL["bg"])
        l_vals  = df["proper_radial_m"].values / AU
        tau_vals= df["proper_time_s"].values
        a_vals  = df["tidal_acc_m_s2"].values / 9.81   # in g

        ax1.plot(l_vals, a_vals, color=self.PAL["red"], lw=0.9)
        ax1.fill_between(l_vals, a_vals, 0, alpha=0.15, color=self.PAL["red"])
        ax1.axhline(10, color=self.PAL["orange"], lw=0.7, ls="--",
                     label="10g tidal limit")
        self._style(ax1, "TIDAL FORCES ALONG TRANSIT (g)")
        ax1.set_xlabel("Proper radial coord l (AU)", fontsize=6, color=self.PAL["fg"])
        ax1.set_ylabel("Tidal acc (g)", fontsize=6, color=self.PAL["fg"])
        ax1.legend(fontsize=6, facecolor=self.PAL["bg"],
                   edgecolor=self.PAL["dim"], labelcolor=self.PAL["fg"])

        ax2.plot(l_vals, tau_vals, color=self.PAL["acc"], lw=1.1)
        self._style(ax2, "PROPER TIME ACCUMULATION (s)")
        ax2.set_xlabel("Proper radial coord l (AU)", fontsize=6, color=self.PAL["fg"])
        ax2.set_ylabel("Proper time τ (s)", fontsize=6, color=self.PAL["fg"])

        plt.tight_layout(pad=0.5)
        return fig


# ─────────────────────────────────────────────────────────────────────────────
# STREAMLIT PAGE
# ─────────────────────────────────────────────────────────────────────────────

def wormhole_navigator_page() -> None:
    st.markdown("""
    <style>
    .worm-header {
        font-family:'Share Tech Mono','Courier New',monospace;
        color:#9b59b6;
        font-size:0.80rem;
        letter-spacing:0.13em;
        border-bottom:1px solid rgba(155,89,182,0.30);
        padding-bottom:0.4rem;
        margin-bottom:1rem;
        text-transform:uppercase;
    }
    .worm-label {
        font-family:'Share Tech Mono','Courier New',monospace;
        color:rgba(232,213,163,0.65);
        font-size:0.65rem;
        letter-spacing:0.08em;
        text-transform:uppercase;
        margin-top:0.5rem;
        margin-bottom:0.2rem;
    }
    .worm-card {
        background:rgba(10,8,15,0.78);
        border:1px solid rgba(155,89,182,0.25);
        border-radius:3px;
        padding:0.4rem 0.6rem;
        font-family:'Share Tech Mono','Courier New',monospace;
        font-size:0.64rem;
        color:rgba(232,213,163,0.72);
        margin:0.2rem 0;
        backdrop-filter:blur(8px);
    }
    .planet-card {
        background:rgba(8,8,18,0.80);
        border:1px solid rgba(74,158,255,0.25);
        border-radius:3px;
        padding:0.45rem 0.65rem;
        font-family:'Share Tech Mono','Courier New',monospace;
        font-size:0.62rem;
        color:rgba(232,213,163,0.70);
        margin:0.25rem 0;
        backdrop-filter:blur(8px);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="worm-header">🌀 WORMHOLE PHYSICS & INTERSTELLAR NAVIGATION ENGINE</div>',
                unsafe_allow_html=True)

    viz    = WormholeVisualizer()
    mech   = OrbitalMechanics()
    mission= EnduranceMission()
    planets= build_gargantua_system()

    col_ctrl, col_main = st.columns([1, 2.5])

    with col_ctrl:
        st.markdown('<div class="worm-label">— WORMHOLE PARAMETERS —</div>',
                    unsafe_allow_html=True)
        throat_AU = st.number_input("Throat radius b₀ (AU)", 0.01, 10.0, 1.0, 0.01)
        shape_exp = st.slider("Shape exponent n (b=b₀ⁿ/rⁿ⁻¹)", 1.5, 4.0, 2.0, 0.1)
        redshift  = st.selectbox("Redshift function Φ(r)", ["zero", "logarithmic"])
        wh_type   = st.selectbox("Wormhole type",
                                  [w.value for w in WormholeType], index=1)
        v_entry   = st.slider("Entry velocity (v/c)", 0.05, 0.99, 0.50, 0.01)

        wh = WormholeGeometry(
            throat_radius_m=throat_AU * AU,
            shape_exponent=shape_exp,
            redshift_fn=redshift,
            wormhole_type=WormholeType(wh_type),
        )

        st.markdown('<div class="worm-label">— WORMHOLE PROPERTIES —</div>',
                    unsafe_allow_html=True)
        transit_s = wh.transit_time_proper(v_entry)
        transit   = WormholeTransit(wh, v_entry)
        summary   = transit.summary()
        props = [
            ("Throat b₀",        f"{wh.throat_radius_m/AU:.3f} AU"),
            ("Transit τ",        f"{summary['proper_time_h']:.3f} h"),
            ("Transit t_coord",  f"{summary['coordinate_time_h']:.3f} h"),
            ("Lorentz γ",        f"{summary['lorentz_factor']:.4f}"),
            ("Peak tidal",       f"{summary['peak_tidal_g']:.3f} g"),
            ("Safe v_max",       f"{summary['v_safe_max_c']:.4f} c"),
            ("Exotic energy",    f"{abs(summary['exotic_energy_J']):.3e} J"),
            ("QI bound",         f"{summary['QI_bound_J']:.3e} J"),
            ("Flare-out OK",     "YES" if wh.flare_out_condition(wh.throat_radius_m * 1.01) > 0 else "NO"),
        ]
        for k, v in props:
            st.markdown(f'<div class="worm-card">{k:<18} {v}</div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="worm-label">— PLANET REFERENCE —</div>',
                    unsafe_allow_html=True)
        for planet in planets:
            st.markdown(
                f'<div class="planet-card">'
                f'<b style="color:#4a9eff">{planet.name}</b><br>'
                f'  Dilation ×{planet.time_dilation_factor:,.0f}<br>'
                f'  r = {planet.orbital_elements.semi_major_axis_m/AU:.2f} AU<br>'
                f'  g = {planet.surface_gravity_m_s2:.1f} m/s²<br>'
                f'  P = {planet.orbital_elements.period_yr:.3f} yr'
                f'</div>', unsafe_allow_html=True)

    with col_main:
        tabs = st.tabs(["[ EMBEDDING ]", "[ EXOTIC MATTER ]",
                        "[ TRANSIT ]", "[ ORBITAL MAP ]",
                        "[ MISSION TIMELINE ]", "[ Δv BUDGET ]",
                        "[ PLANET DATA ]"])

        with tabs[0]:
            if st.button("▶ RENDER EMBEDDING DIAGRAM", use_container_width=True):
                with st.spinner("Computing wormhole geometry..."):
                    fig = viz.plot_embedding_diagram(wh)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                b0 = wh.throat_radius_m
                l_throat = wh.proper_radial_distance(b0 * 5)
                e1, e2, e3 = st.columns(3)
                e1.metric("Throat radius", f"{b0/AU:.3f} AU")
                e2.metric("Proper length (to 5b₀)", f"{l_throat/AU:.3f} AU")
                e3.metric("Shape function b(2b₀)",
                           f"{wh.shape_function(2*b0)/b0:.3f} b₀")

        with tabs[1]:
            if st.button("▶ ANALYSE EXOTIC MATTER", use_container_width=True):
                with st.spinner("Computing exotic matter requirements..."):
                    fig = viz.plot_exotic_matter(wh)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                rho_throat = wh.exotic_matter_density(wh.throat_radius_m * 1.001)
                ex1, ex2, ex3 = st.columns(3)
                ex1.metric("|ρ| at throat", f"{abs(rho_throat):.3e} kg/m³")
                ex2.metric("Total exotic E", f"{abs(wh.total_exotic_energy_J()):.3e} J")
                ex3.metric("QI bound", f"{wh.quantum_inequality_energy():.3e} J")

                st.markdown(
                    f'<div class="worm-card">'
                    f'For comparison: Solar mass energy = {M_SUN * C_SI**2:.2e} J. '
                    f'The exotic energy required is '
                    f'{abs(wh.total_exotic_energy_J()) / (M_SUN * C_SI**2):.3e} solar masses '
                    f'of negative energy density.</div>',
                    unsafe_allow_html=True)

        with tabs[2]:
            if st.button("▶ SIMULATE TRANSIT", use_container_width=True):
                with st.spinner("Simulating wormhole traversal..."):
                    df_transit = transit.simulate(n_steps=400)
                    fig = viz.plot_transit_simulation(df_transit)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                t1, t2, t3, t4 = st.columns(4)
                t1.metric("Proper time τ", f"{summary['proper_time_h']:.3f} h")
                t2.metric("Coord time",    f"{summary['coordinate_time_h']:.3f} h")
                t3.metric("Peak tidal",    f"{summary['peak_tidal_g']:.3f} g")
                t4.metric("Lorentz γ",     f"{summary['lorentz_factor']:.4f}")
                st.dataframe(df_transit.round(4), use_container_width=True,
                              hide_index=True)

        with tabs[3]:
            if st.button("▶ RENDER ORBITAL MAP", use_container_width=True):
                with st.spinner("Computing Gargantua system orbits..."):
                    fig = viz.plot_orbital_map(planets)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)
                for planet in planets:
                    orb = planet.orbital_elements
                    st.markdown(
                        f'<div class="planet-card">'
                        f'<b>{planet.name}</b>: '
                        f'a={orb.semi_major_axis_m/AU:.3f} AU, '
                        f'e={orb.eccentricity:.3f}, '
                        f'T={orb.period_yr:.3f} yr, '
                        f'v_c={orb.orbital_velocity_circular_m_s/1e3:.2f} km/s'
                        f'</div>', unsafe_allow_html=True)

        with tabs[4]:
            legs = mission.build_trajectory()
            if st.button("▶ PLOT MISSION TIMELINE", use_container_width=True):
                with st.spinner("Computing relativistic trajectory..."):
                    fig = viz.plot_mission_timeline(legs)
                    st.pyplot(fig, use_container_width=True)
                    plt.close(fig)

            df_legs = mission.trajectory_dataframe(legs)
            st.dataframe(df_legs, use_container_width=True, hide_index=True)

            s1, s2, s3 = st.columns(3)
            s1.metric("Total Earth elapsed",
                       f"{mission.total_earth_elapsed(legs):.2f} yr")
            s2.metric("Total crew elapsed",
                       f"{mission.total_crew_elapsed(legs):.3f} yr")
            s3.metric("Total Δv",
                       f"{mission.delta_v_budget(legs)/1e3:.1f} km/s")

        with tabs[5]:
            st.markdown('<div class="worm-label">— HOHMANN TRANSFER CALCULATOR —</div>',
                        unsafe_allow_html=True)
            c1h, c2h = st.columns(2)
            with c1h:
                r1_AU = st.number_input("Origin orbit r₁ (AU)", 0.1, 100.0, 1.0, 0.1)
                r2_AU = st.number_input("Target orbit r₂ (AU)", 0.1, 100.0, 9.58, 0.1)
                body  = st.selectbox("Central body", ["Sun", "Earth", "Gargantua"])
                M_body = {"Sun": M_SUN, "Earth": M_EARTH,
                           "Gargantua": GARGANTUA_MASS_SOLAR * M_SUN}[body]

            if st.button("▶ COMPUTE HOHMANN TRANSFER", use_container_width=True):
                h = OrbitalMechanics.hohmann_transfer(r1_AU*AU, r2_AU*AU, M_body)
                st.markdown(
                    f'<div class="worm-card">'
                    f'Δv₁ = {h["dv1_m_s"]/1e3:.4f} km/s<br>'
                    f'Δv₂ = {h["dv2_m_s"]/1e3:.4f} km/s<br>'
                    f'Δv total = {h["dv_total_m_s"]/1e3:.4f} km/s<br>'
                    f'Transfer time = {h["transfer_time_yr"]:.4f} yr<br>'
                    f'v_periapsis = {h["v_periapsis_m_s"]/1e3:.3f} km/s<br>'
                    f'v_apoapsis  = {h["v_apoapsis_m_s"]/1e3:.3f} km/s'
                    f'</div>', unsafe_allow_html=True)

                st.markdown('<div class="worm-label">— TSIOLKOVSKY PROPELLANT BUDGET —</div>',
                            unsafe_allow_html=True)
                isp   = st.number_input("Specific impulse (s)", 200, 100000, 450, 10)
                m_pay = st.number_input("Payload mass (kg)", 100, 1e7, 2e5, 1000,
                                         format="%.0f")
                tz = OrbitalMechanics.tsiolkovsky_rocket(
                    h["dv_total_m_s"], isp, m_pay)
                t1, t2, t3 = st.columns(3)
                t1.metric("Mass ratio m₀/mf", f"{tz['mass_ratio']:.3f}")
                t2.metric("Propellant (kg)", f"{tz['propellant_mass_kg']:.2e}")
                t3.metric("Total initial (kg)", f"{tz['total_initial_kg']:.2e}")

        with tabs[6]:
            st.markdown('<div class="worm-label">— PLANETARY DATA — GARGANTUA SYSTEM —</div>',
                        unsafe_allow_html=True)
            for planet in planets:
                with st.expander(f"◈ {planet.name} (×{planet.time_dilation_factor:,.0f} dilation)"):
                    c1p, c2p = st.columns(2)
                    with c1p:
                        st.markdown(
                            f'<div class="planet-card">'
                            f'<b>Physical</b><br>'
                            f'Mass   = {planet.mass_kg:.3e} kg<br>'
                            f'Radius = {planet.radius_m/R_EARTH:.3f} R_Earth<br>'
                            f'g      = {planet.surface_gravity_m_s2:.2f} m/s²<br>'
                            f'v_esc  = {planet.escape_velocity_m_s/1e3:.2f} km/s<br>'
                            f'Hill r = {planet.hill_sphere_m/AU:.4f} AU'
                            f'</div>', unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="planet-card">'
                            f'<b>Orbital</b><br>'
                            f'a    = {planet.orbital_elements.semi_major_axis_m/AU:.4f} AU<br>'
                            f'e    = {planet.orbital_elements.eccentricity:.4f}<br>'
                            f'i    = {planet.orbital_elements.inclination_deg:.2f}°<br>'
                            f'T    = {planet.orbital_elements.period_yr:.4f} yr<br>'
                            f'v_c  = {planet.orbital_elements.orbital_velocity_circular_m_s/1e3:.2f} km/s'
                            f'</div>', unsafe_allow_html=True)
                    with c2p:
                        st.markdown(
                            f'<div class="planet-card">'
                            f'<b>Description</b><br>'
                            f'{planet.description}'
                            f'</div>', unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="planet-card">'
                            f'<b>Surface conditions</b><br>'
                            f'{planet.surface_conditions}'
                            f'</div>', unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="planet-card">'
                            f'<b>Discovered by</b><br>'
                            f'{planet.discovered_by}'
                            f'</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    wormhole_navigator_page()
