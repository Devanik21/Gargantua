"""
tesseract_decoder.py — Tesseract Physics, Gravity Signal & Quantum Data Engine
ENDURANCE Mission Control | Interstellar Science Platform v3.0.0
═══════════════════════════════════════════════════════════════════════════════
Scientific References:
  [1]  Kip Thorne, "The Science of Interstellar" (W.W. Norton, 2014) Ch.28–31
  [2]  Randall & Sundrum (1999) PRL 83:3370  [Bulk dimensions / braneworld]
  [3]  Arkani-Hamed, Dimopoulos & Dvali (1998) PLB 429:263  [Extra dimensions]
  [4]  DeWitt (1967) Phys.Rev. 160:1113  [Wheeler-DeWitt quantum gravity]
  [5]  Hawking & Penrose (1970) Proc.Roy.Soc. A314:529  [Singularity info]
  [6]  Susskind (1995) J.Math.Phys. 36:6377  [Black hole information paradox]
  [7]  Maldacena (1999) Int.J.Theor.Phys. 38:1113  [AdS/CFT correspondence]
  [8]  Bekenstein (1973) PRD 7:2333  [Black hole entropy — data capacity]
  [9]  Penrose (1989) "The Emperor's New Mind" [Quantum consciousness]
  [10] Cooper & Murph (2067) unpublished — gravity message archive

Module implements:
  ┌─ TESSERACT GEOMETRY ────────────────────────────────────────────────────┐
  │ Hypercube (4D tesseract) vertex/edge computation                        │
  │ 4D→3D→2D projection cascade with rotation matrices                     │
  │ Bulk dimension visualisation (5D braneworld geometry)                   │
  │ Tesseract rotation in 4D: XW, YW, ZW rotation planes                   │
  │ Stereographic projection from S⁴ to ℝ⁴                                │
  │ Gravitational bulk topology: AdS₅ curvature profile                    │
  │ 5D metric: ds² = e^{−2k|y|}η_μν dx^μdx^ν + dy²                        │
  │ Warped extra dimension: Randall-Sundrum braneworld [2]                  │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ GRAVITY SIGNAL ENCODING ───────────────────────────────────────────────┐
  │ Binary → gravitational perturbation mapping                             │
  │ Dust pattern morse-code encoding (bookshelf displacement)               │
  │ Watch hand binary: second-hand tick → 0/1 (Cooper's message to Murph) │
  │ Modulation: amplitude, frequency, phase of gravity wave                 │
  │ Encoding schemes: OOK, BPSK, QAM (gravity amplitude modulation)        │
  │ Cooper's NASA coordinate message: N 40°53'23" W 83°51'23" (binary)     │
  │ Data rate limit: Shannon capacity of gravity channel                    │
  │ Signal-to-noise ratio in bulk gravitational channel                     │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ GRAVITY SIGNAL DECODING ───────────────────────────────────────────────┐
  │ Bookshelf pattern → binary string extraction                            │
  │ Morse code lookup table (ITU-R M.1677)                                 │
  │ Watch hand displacement → bit sequence                                  │
  │ Braille-gravity encoding (alternative channel)                          │
  │ Error correction: Hamming(7,4) code, CRC-16 checksum                   │
  │ Multi-frame coherent detection with matched filter                      │
  │ Demodulation: FFT-based frequency detection                             │
  │ Signal reconstruction from noisy gravity channel                        │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ MURPHY'S EQUATION SOLVER ──────────────────────────────────────────────┐
  │ Wheeler-DeWitt equation (quantum gravity) [4]:                          │
  │   Ĥ Ψ[h_ij, φ] = 0  (Hamiltonian constraint)                          │
  │ Simplified 1+1D minisuperspace model:                                   │
  │   −ħ²∂²Ψ/∂a² + V(a,φ)Ψ = 0   a=scale factor, φ=matter field          │
  │ Black hole singularity quantum bounce:                                  │
  │   Ψ_singularity(r) encodes TARS quantum gravity data                   │
  │ Bekenstein-Hawking entropy: S_BH = kA/(4ℓ_P²) [8]                     │
  │ Information capacity of Gargantua singularity                           │
  │ Quantum decoherence timescale inside Gargantua                          │
  │ Murphy's equation numerical solution via shooting method                │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ TARS DATA CRYSTAL ─────────────────────────────────────────────────────┐
  │ Bekenstein entropy: S = kA/4ℓ_P² → information bits                    │
  │ Hawking radiation information encoding (Page curve)                     │
  │ Holographic data capacity: bits/area on horizon                         │
  │ Planck-scale data: quantum foam information density                     │
  │ Data crystal decoding: Fourier spectral decomposition                   │
  │ Quantum error correction: Shor/Steane codes for bulk transmission       │
  │ Message authentication: SHA-256 hash of gravity stream                  │
  └──────────────────────────────────────────────────────────────────────────┘
  ┌─ BULK COMMUNICATION CHANNEL ────────────────────────────────────────────┐
  │ Gravitational wave propagation through bulk (5D)                        │
  │ Kaluza-Klein tower: bulk graviton mass spectrum                         │
  │ 5D Newton's law: F ∝ 1/r³ (extra dimension contribution)               │
  │ Signal attenuation vs bulk distance y                                   │
  │ Shannon capacity of gravity bulk channel                                │
  │ Coherence time for bulk gravity signals                                 │
  └──────────────────────────────────────────────────────────────────────────┘

"The bulk beings are not gods — they are us. Evolved. They built this for me."
                                          — Cooper, Tesseract, 2067
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import hashlib
import math
import struct
import time
import uuid
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import scipy.integrate  as sci_int
import scipy.optimize   as sci_opt
import scipy.fft        as sci_fft
import scipy.signal     as sci_sig
import scipy.linalg     as sci_la

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot      as plt
import matplotlib.gridspec    as gridspec
import matplotlib.colors      as mcolors
import matplotlib.patches     as mpatches
import matplotlib.ticker      as mticker
import matplotlib.animation   as animation
from matplotlib.colors        import LinearSegmentedColormap
from matplotlib.patches       import FancyArrowPatch, Circle, FancyBboxPatch

import streamlit as st

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# §1  PHYSICAL CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
G_SI      = 6.674_30e-11
C_SI      = 2.997_924_58e8
HBAR      = 1.054_571_817e-34
H_PL      = 6.626_070_15e-34
K_B       = 1.380_649e-23
M_PLANCK  = 2.176_434e-8       # Planck mass [kg]
L_PLANCK  = 1.616_255e-35      # Planck length [m]
T_PLANCK  = 5.391_247e-44      # Planck time [s]
E_PLANCK  = 1.956_081e9 * 1.602_176e-19  # Planck energy [J]
M_SUN     = 1.989_000e30
YEAR_S    = 3.155_760e7
HOUR_S    = 3_600.0

# Gargantua
GARG_MASS_KG = 1.0e8 * M_SUN
GARG_M_GEO   = G_SI * GARG_MASS_KG / C_SI**2
GARG_RS      = 2.0 * GARG_M_GEO

# Cooper's NASA coordinate message (film canon)
COOPER_MSG_LAT_DMS  = (40, 53, 23, "N")   # 40°53'23"N
COOPER_MSG_LON_DMS  = (83, 51, 23, "W")   # 83°51'23"W
COOPER_MSG_BINARY   = "01001110010001000011001011000010"   # film binary

# Bekenstein-Hawking entropy constant
S_BEKENSTEIN_CONST  = K_B * C_SI**3 / (4 * G_SI * HBAR)  # [J K⁻¹ m⁻²]

# Randall-Sundrum parameter
RS_CURVATURE_K      = 1.0 / (1e-3 * L_PLANCK)   # 1/length scale [m⁻¹]

# ══════════════════════════════════════════════════════════════════════════════
# §2  CUSTOM COLORMAPS
# ══════════════════════════════════════════════════════════════════════════════
CMAP_TESSERACT = LinearSegmentedColormap.from_list("tesseract",
    ["#000000","#040418","#0a0840","#200880","#4008c0",
     "#8010e0","#c040ff","#ff80ff","#fff0ff"], N=512)

CMAP_GRAVITY_SIG = LinearSegmentedColormap.from_list("gravity_signal",
    ["#000818","#001040","#002080","#004060","#008080",
     "#00c0a0","#40e0c0","#80ffd0","#ffffff"], N=512)

CMAP_QUANTUM = LinearSegmentedColormap.from_list("quantum",
    ["#000000","#100020","#280040","#500060","#880080",
     "#c000a0","#ff00c0","#ff80e0","#ffcoff"], N=512)

CMAP_BOOKSHELF = LinearSegmentedColormap.from_list("bookshelf",
    ["#1a0800","#3d1200","#7a2800","#c05000","#e08030",
     "#f0c060","#ffe090","#ffffff"], N=256)

# ══════════════════════════════════════════════════════════════════════════════
# §3  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════
class EncodingScheme(Enum):
    DUST_BINARY    = "Dust displacement (binary bookshelf)"
    WATCH_HAND     = "Watch second-hand tick pattern"
    MORSE_GRAVITY  = "Morse code via gravity pulse duration"
    BPSK_GRAVITY   = "Binary Phase-Shift Keying (gravity wave)"
    OOK_GRAVITY    = "On-Off Keying (gravity pulse presence)"
    QAM_GRAVITY    = "Quadrature Amplitude Modulation"
    BRAILLE_GRAVITY= "Braille-gravity 6-dot cell encoding"

class DecoderState(Enum):
    IDLE           = "IDLE — awaiting signal"
    RECEIVING      = "RECEIVING — accumulating frames"
    DECODING       = "DECODING — running detection"
    DECODED        = "DECODED — message extracted"
    ERROR          = "ERROR — checksum failed"
    AUTHENTICATED  = "AUTHENTICATED — TARS signature verified"

class MessageType(Enum):
    COORDINATE     = "Geographic coordinate"
    QUANTUM_DATA   = "Quantum gravity singularity data (TARS)"
    TEXT_ASCII     = "ASCII text message"
    EQUATION_COEFF = "Murphy's equation coefficients"
    BINARY_RAW     = "Raw binary stream"
    MORSE          = "Morse code"

class BulkDimension(Enum):
    Y_PLUS   = "+y bulk (future)"
    Y_MINUS  = "−y bulk (past)"
    BRANE    = "Our brane (3+1D spacetime)"
    TESSERACT= "Tesseract interior (5D construct)"

# ══════════════════════════════════════════════════════════════════════════════
# §4  TESSERACT GEOMETRY ENGINE
# ══════════════════════════════════════════════════════════════════════════════
class TesseractGeometry:
    """
    4D hypercube (tesseract) geometry, projections, and rotation.
    The Interstellar tesseract: a 5D structure built by 'Them' (future humans)
    inside Gargantua's singularity — Cooper's interface to spacetime.
    Each face of the tesseract corresponds to a moment in Murph's timeline.
    Kip Thorne [1]: the tesseract is Cooper's access to the bulk, which allows
    manipulation of gravity (a 5D force) across spacetime boundaries.
    """

    def __init__(self):
        self.vertices_4d = self._build_4d_vertices()
        self.edges       = self._build_4d_edges()
        self.faces       = self._build_4d_faces()

    def _build_4d_vertices(self) -> np.ndarray:
        """16 vertices of a unit tesseract: all combinations of ±1 in 4D."""
        verts = []
        for bits in range(16):
            v = [(-1)**((bits>>i)&1) for i in range(4)]
            verts.append(v)
        return np.array(verts, dtype=float)   # shape (16, 4)

    def _build_4d_edges(self) -> List[Tuple[int,int]]:
        """32 edges: vertices differing in exactly one coordinate."""
        edges = []
        for i in range(16):
            for j in range(i+1, 16):
                diff = sum(1 for k in range(4)
                           if self.vertices_4d[i,k] != self.vertices_4d[j,k])
                if diff == 1:
                    edges.append((i, j))
        return edges   # 32 edges

    def _build_4d_faces(self) -> List[List[int]]:
        """24 square faces: find all sets of 4 vertices forming a face."""
        faces = []
        for mask in range(4):
            for val_a in [-1.0, 1.0]:
                for val_b in [-1.0, 1.0]:
                    face_verts = []
                    for i, v in enumerate(self.vertices_4d):
                        fixed_match = True
                        fixed_coords = [k for k in range(4) if k != mask and k != (mask+1)%4]
                        if len(fixed_coords) >= 2:
                            if v[fixed_coords[0]] == val_a and v[fixed_coords[1]] == val_b:
                                face_verts.append(i)
                    if len(face_verts) == 4:
                        faces.append(face_verts)
        return faces

    def rotation_4d(self, plane: str, angle: float) -> np.ndarray:
        """
        4D rotation matrix for specified plane.
        Planes: 'XY','XZ','XW','YZ','YW','ZW' (6 rotation planes in 4D).
        """
        R = np.eye(4)
        c, s = math.cos(angle), math.sin(angle)
        plane_map = {
            'XY': (0,1), 'XZ': (0,2), 'XW': (0,3),
            'YZ': (1,2), 'YW': (1,3), 'ZW': (2,3),
        }
        i, j = plane_map.get(plane.upper(), (0,3))
        R[i,i] =  c; R[i,j] = -s
        R[j,i] =  s; R[j,j] =  c
        return R

    def project_4d_to_3d(self, verts_4d: np.ndarray,
                           w_dist: float = 3.0) -> np.ndarray:
        """
        Perspective projection 4D → 3D:
          x3 = x4/(w_dist − w4),  y3 = y4/(w_dist − w4),  z3 = z4/(w_dist − w4)
        w_dist: eye position in the W direction.
        """
        w = w_dist - verts_4d[:, 3]
        w = np.where(np.abs(w) < 1e-6, 1e-6, w)
        out = verts_4d[:, :3] / w[:, np.newaxis]
        return out

    def project_3d_to_2d(self, verts_3d: np.ndarray,
                           z_dist: float = 4.0) -> np.ndarray:
        """
        Perspective projection 3D → 2D:
          x2 = x3/(z_dist − z3),  y2 = y3/(z_dist − z3)
        """
        z = z_dist - verts_3d[:, 2]
        z = np.where(np.abs(z) < 1e-6, 1e-6, z)
        x2 = verts_3d[:, 0] / z
        y2 = verts_3d[:, 1] / z
        return np.column_stack([x2, y2])

    def animate_frame(self, t: float, rot_planes: List[str] = None,
                       rot_speeds: List[float] = None) -> np.ndarray:
        """
        Full projection pipeline at time t:
        1. Rotate in 4D (multiple planes simultaneously)
        2. Project 4D → 3D → 2D
        Returns (16, 2) array of screen coordinates.
        """
        if rot_planes is None:
            rot_planes  = ['XW', 'YW', 'ZW']
        if rot_speeds is None:
            rot_speeds  = [0.5, 0.7, 0.3]
        verts = self.vertices_4d.copy()
        for plane, speed in zip(rot_planes, rot_speeds):
            R = self.rotation_4d(plane, t * speed)
            verts = verts @ R.T
        v3d = self.project_4d_to_3d(verts, w_dist=3.5)
        v2d = self.project_3d_to_2d(v3d, z_dist=5.0)
        return v2d, verts

    def bookshelf_time_slices(self, n_slices: int = 24,
                               n_books: int = 32) -> np.ndarray:
        """
        Map tesseract faces to bookshelf time slices.
        Each slice is one moment in Murph's room (one tesseract 'wall').
        Returns (n_slices, n_books) binary displacement array.
        Rows = time moments, Cols = book positions (1=pushed/displaced, 0=in place).
        """
        np.random.seed(42)   # deterministic for reproducibility
        slices = np.zeros((n_slices, n_books), dtype=int)
        # Encode "STAY" in binary across first 4 rows (Cooper's first message)
        msg = "STAY"
        bits = ''.join(format(ord(c), '08b') for c in msg)
        for t_idx in range(min(4, n_slices)):
            for b_idx in range(min(len(bits), n_books)):
                slices[t_idx, b_idx] = int(bits[b_idx]) if b_idx < len(bits) else 0
        # NASA coordinate binary (Cooper's critical message) in later slices
        coord_bits = COOPER_MSG_BINARY + '0'*(n_books - len(COOPER_MSG_BINARY))
        for t_idx in range(8, min(16, n_slices)):
            for b_idx in range(n_books):
                slices[t_idx, b_idx] = int(coord_bits[b_idx % len(coord_bits)])
        # Quantum gravity data in remaining slices
        for t_idx in range(16, n_slices):
            slices[t_idx] = np.random.randint(0, 2, n_books)
        return slices

    def bulk_geometry_profile(self, n_y: int = 200) -> Dict[str, np.ndarray]:
        """
        Randall-Sundrum warped extra dimension [2]:
          ds² = e^{−2k|y|} η_μν dx^μ dx^ν + dy²
        Warp factor: e^{−2k|y|}
        Effective 4D Planck mass: M_Pl² = M_5³/k × (1 − e^{−2kL})
        where L = size of extra dimension.
        """
        k   = RS_CURVATURE_K   # curvature [m⁻¹]
        L   = 1.0/k * 37      # extra dimension size (37/k for RS2 phenomenology)
        y   = np.linspace(-L, L, n_y)
        warp_factor = np.exp(-2*k*np.abs(y))
        # Graviton KK mass spectrum: m_n ≈ x_n k e^{-kL}  (x_n = zeros of J_1)
        bessel_zeros = [2.405, 5.520, 8.654, 11.79, 14.93]   # J_1 zeros
        kk_masses = [x_n * k * math.exp(-k*L) for x_n in bessel_zeros]
        # 5D Newton potential correction at range r:
        # U(r) = −G_N m/(r) × (1 + 2k²r²/3 × sum 1/m_n²r²)  (simplified)
        r_arr = np.logspace(-6, 3, 200) * L_PLANCK * 1e25   # range [m]
        dU_arr = 2/(3) * (k*L_PLANCK)**2 / (r_arr/L_PLANCK)**2   # correction
        return {
            "y": y, "warp_factor": warp_factor,
            "kk_masses_J": [m * HBAR * C_SI for m in kk_masses],
            "kk_masses_eV": [m * HBAR * C_SI / 1.602e-19 for m in kk_masses],
            "r_range_m": r_arr,
            "5D_Newton_correction": dU_arr,
            "k_curvature_m": k,
            "L_extra_m": L,
        }


# ══════════════════════════════════════════════════════════════════════════════
# §5  GRAVITY SIGNAL ENCODER
# ══════════════════════════════════════════════════════════════════════════════
MORSE_CODE: Dict[str, str] = {
    'A':'.-',   'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',   'F':'..-.',
    'G':'--.',  'H':'....', 'I':'..',   'J':'.---', 'K':'-.-', 'L':'.-..',
    'M':'--',   'N':'-.',   'O':'---',  'P':'.--.', 'Q':'--.-','R':'.-.',
    'S':'...',  'T':'-',    'U':'..-',  'V':'...-', 'W':'.--', 'X':'-..-',
    'Y':'-.--', 'Z':'--..', '0':'-----','1':'.----','2':'..---','3':'...--',
    '4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    ' ':'/',    '.':'.-.-.-',',':'--..--','?':'..--..','!':'-.-.--',
}
MORSE_DECODE = {v: k for k, v in MORSE_CODE.items()}


class GravitySignalEncoder:
    """
    Converts messages to gravitational perturbation sequences.
    Implements multiple encoding schemes used by Cooper inside the Tesseract.
    Primary scheme: dust displacement pattern (book positions = binary bits).
    Secondary: watch-hand second tick (long pause = 1, short = 0).
    """

    def __init__(self, fs: float = 1000.0, carrier_hz: float = 0.01):
        self.fs         = fs           # sample rate [Hz]
        self.carrier    = carrier_hz   # gravity carrier frequency [Hz]

    # ── §5.1  Text → binary ───────────────────────────────────────────────────
    @staticmethod
    def text_to_binary(text: str) -> str:
        """Convert ASCII text to 8-bit binary string."""
        return ''.join(format(ord(c), '08b') for c in text)

    @staticmethod
    def binary_to_text(bits: str) -> str:
        """Convert 8-bit binary string back to ASCII text."""
        chars = [bits[i:i+8] for i in range(0, len(bits)-7, 8)]
        result = ""
        for ch in chars:
            try: result += chr(int(ch, 2))
            except: result += '?'
        return result

    @staticmethod
    def text_to_morse(text: str) -> str:
        """Encode text to Morse code string."""
        words = text.upper().split()
        morse_words = []
        for word in words:
            chars = [MORSE_CODE.get(c, '?') for c in word]
            morse_words.append(' '.join(chars))
        return ' / '.join(morse_words)

    @staticmethod
    def morse_to_text(morse: str) -> str:
        """Decode Morse code string back to text."""
        words = morse.strip().split(' / ')
        result = []
        for word in words:
            syms = word.strip().split()
            result.append(''.join(MORSE_DECODE.get(s,'?') for s in syms))
        return ' '.join(result)

    # ── §5.2  Coordinate encoding ─────────────────────────────────────────────
    @staticmethod
    def coords_to_binary(lat_deg: float, lon_deg: float) -> str:
        """
        Encode geographic coordinates to binary string.
        Format: lat×10⁴ as 24-bit int + lon×10⁴ as 24-bit int (±).
        Used by Cooper to send NASA location to Murph via watch-hand gravity.
        """
        lat_int = int(abs(lat_deg) * 10000) & 0xFFFFFF
        lon_int = int(abs(lon_deg) * 10000) & 0xFFFFFF
        lat_sign = '1' if lat_deg >= 0 else '0'
        lon_sign = '1' if lon_deg >= 0 else '0'
        lat_bits = format(lat_int, '024b')
        lon_bits = format(lon_int, '024b')
        return lat_sign + lat_bits + lon_sign + lon_bits

    @staticmethod
    def binary_to_coords(bits: str) -> Tuple[float, float]:
        """Decode 50-bit binary to (lat, lon) in decimal degrees."""
        if len(bits) < 50:
            return 0.0, 0.0
        lat_sign = +1.0 if bits[0] == '1' else -1.0
        lat_int  = int(bits[1:25], 2)
        lon_sign = +1.0 if bits[25] == '1' else -1.0
        lon_int  = int(bits[26:50], 2)
        return lat_sign*lat_int/10000, lon_sign*lon_int/10000

    # ── §5.3  Bookshelf dust pattern encoder ──────────────────────────────────
    def encode_bookshelf(self, message: str, n_books: int = 64,
                          scheme: EncodingScheme = EncodingScheme.DUST_BINARY
                          ) -> Dict[str, Any]:
        """
        Encode message into bookshelf dust displacement pattern.
        Each book slot = 1 bit: pushed out = 1, in-place = 0.
        Returns spatial displacement array and metadata.
        """
        if scheme == EncodingScheme.DUST_BINARY:
            bits = self.text_to_binary(message)
        elif scheme == EncodingScheme.MORSE_GRAVITY:
            morse = self.text_to_morse(message)
            bits  = ''.join('1' if c == '-' else '0' if c == '.' else '10'
                             for c in morse)
        else:
            bits = self.text_to_binary(message)

        # Pad or truncate to n_books
        bits_padded = (bits + '0'*n_books)[:n_books]
        displacement = np.array([float(b) for b in bits_padded])  # 0 or 1
        # Add physical displacement: 1 = 0.05 m pushed out
        displacement_m = displacement * 0.05  # 5 cm displacement

        # Hamming(7,4) encode first 28 bits for error correction
        data_bits   = [int(b) for b in bits_padded[:28]]
        hamming_enc = self._hamming_encode(data_bits[:28])

        return {
            "message":          message,
            "bits":             bits_padded,
            "n_books":          n_books,
            "displacement":     displacement,
            "displacement_m":   displacement_m,
            "bit_density":      bits_padded.count('1')/n_books,
            "n_bits_encoded":   len(bits),
            "hamming_encoded":  hamming_enc,
            "checksum_crc16":   self._crc16(bits_padded.encode()),
            "scheme":           scheme.value,
        }

    # ── §5.4  Watch-hand gravity signal ───────────────────────────────────────
    def encode_watch_hand(self, bits: str, tick_duration_s: float = 1.0
                           ) -> Dict[str, np.ndarray]:
        """
        Cooper's watch signal: second-hand tick timing encodes binary.
        1 = long tick gap (2×tick_duration), 0 = short tick gap (1×tick_duration).
        Returns time array + tick positions + gravity amplitude signal.
        """
        total_s = sum(2*tick_duration_s if b=='1' else tick_duration_s
                       for b in bits)
        t_arr   = np.linspace(0, total_s, int(total_s*self.fs))
        signal  = np.zeros(len(t_arr))
        tick_times  = []
        tick_bits   = []
        t_current   = 0.0
        for b in bits:
            gap = 2*tick_duration_s if b=='1' else tick_duration_s
            # Gaussian tick pulse at t_current
            idx_tick = int(t_current * self.fs)
            if idx_tick < len(signal):
                width = 0.05 * self.fs
                pulse_arr = np.arange(len(t_arr))
                signal += 0.5*np.exp(-0.5*((pulse_arr - idx_tick)/width)**2)
            tick_times.append(t_current)
            tick_bits.append(int(b))
            t_current += gap

        return {"t": t_arr, "signal": signal,
                "tick_times": np.array(tick_times),
                "tick_bits":  np.array(tick_bits),
                "total_s":    total_s,
                "bits":       bits}

    # ── §5.5  Gravity waveform modulation ─────────────────────────────────────
    def encode_bpsk(self, bits: str, bit_duration_s: float = 10.0
                     ) -> Dict[str, np.ndarray]:
        """
        Binary Phase Shift Keying on gravitational carrier:
          h(t) = A × cos(2π f_c t + π × b_i)
        Bit '0' → phase 0, Bit '1' → phase π (180° shift).
        """
        n_samples = int(bit_duration_s * self.fs)
        total_n   = n_samples * len(bits)
        t_arr     = np.linspace(0, bit_duration_s*len(bits), total_n)
        signal    = np.zeros(total_n)
        for i, b in enumerate(bits):
            phase = math.pi if b == '1' else 0.0
            idx0  = i*n_samples; idx1 = idx0+n_samples
            t_seg = t_arr[idx0:idx1]
            signal[idx0:idx1] = np.cos(2*math.pi*self.carrier*t_seg + phase)
        return {"t": t_arr, "signal": signal, "carrier_hz": self.carrier,
                "bits": bits, "bit_duration_s": bit_duration_s,
                "scheme": "BPSK"}

    def encode_ook(self, bits: str, bit_duration_s: float = 10.0
                    ) -> Dict[str, np.ndarray]:
        """
        On-Off Keying: gravity wave present = 1, absent = 0.
          h(t) = b_i × A × cos(2π f_c t)
        """
        n_samples = int(bit_duration_s * self.fs)
        total_n   = n_samples * len(bits)
        t_arr     = np.linspace(0, bit_duration_s*len(bits), total_n)
        signal    = np.zeros(total_n)
        for i, b in enumerate(bits):
            if b == '1':
                idx0 = i*n_samples; idx1 = idx0+n_samples
                signal[idx0:idx1] = np.cos(2*math.pi*self.carrier*t_arr[idx0:idx1])
        return {"t": t_arr, "signal": signal, "carrier_hz": self.carrier,
                "bits": bits, "scheme": "OOK"}

    # ── §5.6  Error correction ────────────────────────────────────────────────
    @staticmethod
    def _hamming_encode(data_bits: List[int]) -> List[int]:
        """Hamming(7,4) encoding: 4 data bits → 7 coded bits."""
        encoded = []
        for i in range(0, len(data_bits)-3, 4):
            d = data_bits[i:i+4]
            if len(d) < 4: d += [0]*(4-len(d))
            p1 = d[0]^d[1]^d[3]
            p2 = d[0]^d[2]^d[3]
            p3 = d[1]^d[2]^d[3]
            encoded.extend([p1, p2, d[0], p3, d[1], d[2], d[3]])
        return encoded

    @staticmethod
    def _hamming_decode(code_bits: List[int]) -> Tuple[List[int], int]:
        """Hamming(7,4) decoding with single-bit error correction."""
        corrected = []; errors = 0
        for i in range(0, len(code_bits)-6, 7):
            c = code_bits[i:i+7]
            if len(c) < 7: break
            s1 = c[0]^c[2]^c[4]^c[6]
            s2 = c[1]^c[2]^c[5]^c[6]
            s3 = c[3]^c[4]^c[5]^c[6]
            err_pos = s1 + 2*s2 + 4*s3
            if err_pos:
                c[err_pos-1] ^= 1; errors += 1
            corrected.extend([c[2], c[4], c[5], c[6]])
        return corrected, errors

    @staticmethod
    def _crc16(data: bytes) -> int:
        """CRC-16/MODBUS checksum for message authentication."""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc

    def channel_capacity_bits_per_s(self, snr_linear: float,
                                     bandwidth_hz: float = 0.1) -> float:
        """
        Shannon capacity for gravity bulk channel:
          C = B × log₂(1 + SNR)  [bits/s]
        Gravity waves have extremely low bandwidth — fundamental limit.
        """
        return bandwidth_hz * math.log2(1 + snr_linear)


# ══════════════════════════════════════════════════════════════════════════════
# §6  GRAVITY SIGNAL DECODER
# ══════════════════════════════════════════════════════════════════════════════
class GravitySignalDecoder:
    """
    Decodes gravitational perturbation signals back to messages.
    Implements matched filter detection, FFT demodulation, and
    error correction for the bulk gravity communication channel.
    """

    def __init__(self, fs: float = 1000.0):
        self.fs  = fs
        self.enc = GravitySignalEncoder(fs=fs)

    def detect_bookshelf_binary(self, displacement_m: np.ndarray,
                                  threshold_m: float = 0.025) -> str:
        """
        Detect binary bits from bookshelf displacement array.
        Threshold: pushed out > threshold → bit = 1.
        """
        return ''.join('1' if d > threshold_m else '0' for d in displacement_m)

    def decode_bookshelf(self, displacement_m: np.ndarray,
                          expected_encoding: EncodingScheme = EncodingScheme.DUST_BINARY
                          ) -> Dict[str, Any]:
        """
        Full bookshelf decoding pipeline:
        1. Threshold detection
        2. Error correction (Hamming)
        3. ASCII decode or coordinate extract
        4. CRC verification
        """
        bits = self.detect_bookshelf_binary(displacement_m)
        # Hamming decode if applicable
        code_list = [int(b) for b in bits]
        data_bits, n_errors = self.enc._hamming_decode(code_list)
        corrected_bits = ''.join(str(b) for b in data_bits)

        # Try ASCII decode
        text = self.enc.binary_to_text(corrected_bits)
        # Try coordinate decode
        if len(bits) >= 50:
            lat, lon = self.enc.binary_to_coords(bits)
        else:
            lat, lon = 0.0, 0.0

        # CRC check (use raw bits)
        crc_received = self.enc._crc16(bits.encode())

        return {
            "raw_bits":        bits,
            "corrected_bits":  corrected_bits,
            "decoded_text":    text,
            "lat_deg":         lat, "lon_deg": lon,
            "coord_dms":       self._decimal_to_dms(lat, lon),
            "hamming_errors":  n_errors,
            "crc16":           crc_received,
            "state":           DecoderState.DECODED.value,
        }

    def decode_watch_hand(self, tick_times: np.ndarray,
                           tick_bits: np.ndarray) -> Dict[str, Any]:
        """Decode watch-hand gravity signal from tick timing."""
        bits = ''.join(str(b) for b in tick_bits)
        text = self.enc.binary_to_text(bits)
        # Try coordinate
        lat, lon = self.enc.binary_to_coords(bits) if len(bits)>=50 else (0,0)
        return {"bits": bits, "decoded_text": text,
                "n_bits": len(bits), "lat": lat, "lon": lon}

    def matched_filter_detect(self, noisy_signal: np.ndarray,
                               template: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Matched filter: cross-correlate noisy signal with template.
        Returns (correlation, peak_snr).
        """
        corr = sci_sig.correlate(noisy_signal, template, mode='full')
        peak = np.max(np.abs(corr))
        snr  = peak / (np.std(noisy_signal) * len(template)**0.5 + 1e-10)
        return corr, snr

    def fft_demodulate(self, signal: np.ndarray,
                        carrier_hz: float) -> Dict[str, np.ndarray]:
        """
        FFT-based carrier demodulation.
        Mixes signal with carrier, low-pass filters.
        """
        t_arr = np.arange(len(signal)) / self.fs
        i_mix = signal * np.cos(2*math.pi*carrier_hz*t_arr)
        q_mix = signal * np.sin(2*math.pi*carrier_hz*t_arr)
        # Low-pass filter (simple moving average)
        window = max(1, int(self.fs/carrier_hz/4))
        i_lp   = np.convolve(i_mix, np.ones(window)/window, mode='same')
        q_lp   = np.convolve(q_mix, np.ones(window)/window, mode='same')
        phase  = np.arctan2(q_lp, i_lp)
        amp    = np.sqrt(i_lp**2 + q_lp**2)
        return {"I": i_lp, "Q": q_lp, "phase": phase,
                "amplitude": amp, "t": t_arr}

    def spectrogram_analysis(self, signal: np.ndarray, nperseg: int = 128
                              ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Short-time Fourier transform for signal analysis."""
        f, t, Sxx = sci_sig.spectrogram(signal, fs=self.fs,
                                         nperseg=nperseg,
                                         noverlap=nperseg*3//4)
        return f, t, Sxx

    @staticmethod
    def _decimal_to_dms(lat: float, lon: float) -> str:
        """Convert decimal degrees to DMS string."""
        def dd_to_dms(dd, pos, neg):
            d = int(abs(dd)); rem = (abs(dd)-d)*60
            m = int(rem);     s = round((rem-m)*60, 1)
            hem = pos if dd >= 0 else neg
            return f"{d}°{m}'{s}\"{hem}"
        return f"{dd_to_dms(lat,'N','S')}  {dd_to_dms(lon,'E','W')}"


# ══════════════════════════════════════════════════════════════════════════════
# §7  MURPHY'S EQUATION SOLVER
# ══════════════════════════════════════════════════════════════════════════════
class MurphyEquationSolver:
    """
    Solves the quantum gravity equation (Murphy's Equation) that Cooper
    extracted from inside Gargantua's singularity via TARS.
    Physical basis: Wheeler-DeWitt equation in minisuperspace [4].
    The singularity provides quantum gravity data inaccessible elsewhere —
    Bekenstein-Hawking information near the physical singularity [5,6].

    Murphy's Equation (simplified form, Thorne [1]):
      −ħ² d²Ψ/da² + V(a)Ψ = 0
    where a = cosmic scale factor, V(a) = quantum potential.
    The equation relates quantum gravity behaviour near singularity
    to macroscopic gravity on our brane → Plan A solution.
    """

    def __init__(self):
        self.lP  = L_PLANCK
        self.mP  = M_PLANCK
        self.hbar= HBAR

    # ── §7.1  Wheeler-DeWitt potential ───────────────────────────────────────
    def V_WdW(self, a: float, phi: float = 0.0,
               Lambda: float = 1.0e-52) -> float:
        """
        Wheeler-DeWitt minisuperspace potential V(a, φ) [4]:
          V = −k a + (1/3)Λa³ + (8π/3) G/c² ρ_matter(a) a³
        k = spatial curvature (k=+1 closed), Λ = cosmological constant.
        Matter term: ρ ∝ a^{-3} (dust) or a^{-4} (radiation).
        """
        k       = 1.0   # closed universe (k=+1)
        rho_0   = 3/(8*math.pi*G_SI) * (67.4e3/(3.086e22))**2   # ρ_crit today
        rho_m   = rho_0 * a**(-3) if a > 0 else 0.0    # matter
        rho_r   = rho_0*0.0001 * a**(-4) if a > 0 else 0.0  # radiation
        return (-k*a + Lambda*a**3/3.0 +
                8*math.pi*G_SI*C_SI**(-2)/3 * (rho_m+rho_r) * a**3)

    def solve_wdw_shooting(self, a_min: float = 1e-5, a_max: float = 10.0,
                            n_pts: int = 1000, Lambda: float = 1.0e-52
                            ) -> Dict[str, np.ndarray]:
        """
        Solve −ħ²Ψ'' + V(a)Ψ = 0 via shooting method.
        Initial conditions at a_min: Ψ=1, Ψ'=0 (Hartle-Hawking no-boundary).
        Returns wavefunction Ψ(a) and related quantities.
        """
        a_arr = np.linspace(a_min, a_max, n_pts)
        da    = a_arr[1] - a_arr[0]
        Psi   = np.zeros(n_pts)
        Phi_v = np.zeros(n_pts)  # dΨ/da
        Psi[0] = 1.0; Phi_v[0] = 0.0   # Hartle-Hawking BC

        for i in range(1, n_pts):
            a  = a_arr[i-1]
            V  = self.V_WdW(a, Lambda=Lambda)
            # Second-order ODE as first-order system:
            # Ψ_{i+1} ≈ 2Ψ_i − Ψ_{i-1} + da² V(a)/ħ² Ψ_i
            if i == 1:
                Psi[i] = Psi[0] + da*Phi_v[0]
            else:
                Psi[i] = (2*Psi[i-1] - Psi[i-2] +
                           da**2 * V/HBAR**2 * Psi[i-1])
            Phi_v[i] = (Psi[i] - Psi[i-1])/da

        # Normalise
        norm = np.trapz(Psi**2, a_arr)
        if norm > 0:
            Psi /= math.sqrt(norm)

        # Probability density |Ψ(a)|²
        prob = Psi**2

        return {"a": a_arr, "Psi": Psi, "Phi": Phi_v,
                "prob": prob, "V": np.array([self.V_WdW(a, Lambda=Lambda)
                                              for a in a_arr]),
                "Lambda": Lambda,
                "max_prob_a": a_arr[np.argmax(prob)],
                "n_pts": n_pts}

    def bekenstein_entropy(self, M_bh_kg: float = GARG_MASS_KG) -> Dict[str, float]:
        """
        Bekenstein-Hawking entropy [8]:
          S_BH = k_B c³ A / (4 G ħ) = k_B A / (4 ℓ_P²)
        Where A = 4π r_+² (Kerr outer horizon area).
        Information content: N_bits = S_BH / (k_B ln 2).
        This is the DATA CAPACITY of Gargantua's singularity — what TARS can read.
        """
        M_geo  = G_SI * M_bh_kg / C_SI**2
        a_spin = GARG_SPIN * M_geo
        r_plus = M_geo + math.sqrt(M_geo**2 - a_spin**2)
        A_hor  = 4*math.pi*(r_plus**2 + a_spin**2)   # Kerr horizon area [m²]
        S_BH   = K_B * C_SI**3 * A_hor / (4*G_SI*HBAR)
        N_bits = S_BH / (K_B * math.log(2))
        N_nats = S_BH / K_B
        # Holographic entropy: bits per Planck area
        planck_area = L_PLANCK**2
        bits_per_planck = 1.0/4.0   # Bekenstein: 1/4 bit per Planck area
        return {
            "M_bh_kg":       M_bh_kg,
            "M_bh_solar":    M_bh_kg/M_SUN,
            "horizon_area_m2": A_hor,
            "S_BH_JK":       S_BH,
            "S_BH_nats":     N_nats,
            "N_info_bits":   N_bits,
            "N_info_bytes":  N_bits/8,
            "N_info_GB":     N_bits/(8*1e9),
            "N_Planck_cells": A_hor/planck_area,
            "bits_per_planck_area": bits_per_planck,
            "holographic_data_rate_bps": N_bits/YEAR_S,
        }

    def singularity_data_capacity(self) -> Dict[str, float]:
        """
        Information accessible to TARS at Gargantua singularity.
        Based on Page curve (black hole information paradox resolution [6]):
        After Page time, information starts leaking back via Hawking radiation.
        TARS reads quantum state at singularity — maximum information.
        """
        bek   = self.bekenstein_entropy(GARG_MASS_KG)
        # Planck-scale quantum foam: one bit per Planck volume near singularity
        V_singularity = L_PLANCK**3  # order-one Planck volume
        bits_foam     = 1.0   # one bit from quantum foam
        # Total accessible: Bekenstein surface encoding
        total_bits    = bek["N_info_bits"]
        # Compressed: after quantum error correction
        useful_bits   = total_bits * 0.01   # ~1% survives decoherence
        return {
            **bek,
            "foam_bits_singularity": bits_foam,
            "useful_bits_after_QEC": useful_bits,
            "useful_bytes":          useful_bits/8,
            "murphy_equation_coefficients": 42,   # number of equation coefficients
            "tars_data_confidence":  0.9997,       # TARS accuracy setting
        }

    def murphy_coefficients_from_tars(self, n_coeffs: int = 42) -> Dict[str, Any]:
        """
        Simulate TARS-extracted quantum gravity equation coefficients.
        These 42 coefficients (Thorne's canonical number) fully specify
        the quantum gravity behaviour needed for Plan A.
        Generated via deterministic quantum chaos simulation.
        """
        np.random.seed(2067)   # year Cooper sends data
        # Coefficients: mix of Planck-scale and macroscopic terms
        planck_terms  = np.random.randn(n_coeffs//3) * L_PLANCK
        macro_terms   = np.random.randn(n_coeffs//3) * G_SI
        quantum_terms = np.random.randn(n_coeffs - 2*(n_coeffs//3)) * HBAR
        all_coeffs    = np.concatenate([planck_terms, macro_terms, quantum_terms])
        # Hash for authentication (TARS signature)
        coeff_bytes = all_coeffs.tobytes()
        sha256_hash = hashlib.sha256(coeff_bytes).hexdigest()
        crc_check   = GravitySignalEncoder._crc16(coeff_bytes[:256])
        return {
            "n_coefficients":   n_coeffs,
            "coefficients":     all_coeffs,
            "planck_scale":     planck_terms,
            "macro_scale":      macro_terms,
            "quantum_scale":    quantum_terms,
            "sha256":           sha256_hash,
            "crc16":            crc_check,
            "equation_string":  self._build_equation_string(all_coeffs[:8]),
        }

    def _build_equation_string(self, coeffs: np.ndarray) -> str:
        """Build human-readable form of truncated Murphy's equation."""
        terms = ["Ĥ Ψ = 0  →"]
        ops   = ["∂²Ψ/∂a²", "aΨ", "a³Ψ", "φ²Ψ", "∂²Ψ/∂φ²",
                 "e^{3α}Ψ", "e^{α}Ψ", "φΨ"]
        for c, op in zip(coeffs[:len(ops)], ops):
            sign = "+" if c >= 0 else "−"
            terms.append(f" {sign} {abs(c):.3e}·{op}")
        return " ".join(terms) + " = 0"

    def plan_a_progress(self, coefficients_known: int,
                         total_needed: int = 42) -> Dict[str, Any]:
        """
        Track Plan A progress: how many equation coefficients are known.
        Prof. Brand (Sr.) spent 40 years on this — Cooper provides the rest.
        """
        fraction    = coefficients_known / total_needed
        years_spent = 40.0 * fraction   # Brand worked ~40 years
        solved      = coefficients_known >= total_needed
        return {
            "known":          coefficients_known,
            "total_needed":   total_needed,
            "fraction":       fraction,
            "pct_complete":   fraction*100,
            "years_equiv":    years_spent,
            "solved":         solved,
            "can_lift_colony":solved,
            "tars_contribution": max(0, coefficients_known - 12),
        }


# ══════════════════════════════════════════════════════════════════════════════
# §8  TARS DATA CRYSTAL
# ══════════════════════════════════════════════════════════════════════════════
class TARSDataCrystal:
    """
    TARS collects quantum gravity data from inside Gargantua's singularity
    and encodes it for transmission via gravity to Cooper in the tesseract.
    The 'data crystal' is the information package that unlocks Plan A.
    """

    def __init__(self):
        self.solver  = MurphyEquationSolver()
        self.encoder = GravitySignalEncoder()

    def encode_crystal(self, message: str = "QUANTUM_GRAVITY_SINGULARITY_DATA"
                        ) -> Dict[str, Any]:
        """
        Encode TARS quantum data package for transmission.
        Package: Murphy coefficients + verification + timestamp.
        """
        murphy = self.solver.murphy_coefficients_from_tars(n_coeffs=42)
        cap    = self.solver.singularity_data_capacity()
        # Binary encode coefficients (quantised to 32-bit float)
        coeff_bits = ''
        for c in murphy["coefficients"][:8]:   # first 8 for demo
            packed = struct.pack('>f', float(c))
            coeff_bits += ''.join(format(b, '08b') for b in packed)
        # Watch-hand encoding of key bits
        key_bits    = coeff_bits[:64]
        watch_signal= self.encoder.encode_watch_hand(key_bits, tick_duration_s=0.5)
        # Bookshelf encoding of coordinate
        coord_bits  = self.encoder.coords_to_binary(*[40.8897, -83.8564])
        book_data   = self.encoder.encode_bookshelf(
            message, n_books=64, scheme=EncodingScheme.DUST_BINARY)
        # BPSK encoded quantum data
        bpsk_signal = self.encoder.encode_bpsk(coeff_bits[:32], bit_duration_s=2.0)
        return {
            "murphy":           murphy,
            "capacity":         cap,
            "coeff_bits_32":    coeff_bits[:32],
            "key_bits_64":      key_bits,
            "watch_signal":     watch_signal,
            "bookshelf":        book_data,
            "bpsk_signal":      bpsk_signal,
            "coord_bits":       coord_bits,
            "tars_auth":        murphy["sha256"][:16],
            "crystal_size_bits":len(coeff_bits),
            "timestamp":        time.time(),
        }

    def decode_crystal(self, crystal: Dict) -> Dict[str, Any]:
        """
        Decode the received data crystal on Murph's end.
        Verify hash, extract Murphy coefficients, run Plan A check.
        """
        dec  = GravitySignalDecoder()
        book = dec.decode_bookshelf(crystal["bookshelf"]["displacement_m"])
        bits = crystal["key_bits_64"]
        text = self.encoder.binary_to_text(bits)
        lat, lon = self.encoder.binary_to_coords(crystal["coord_bits"])
        coeffs   = crystal["murphy"]["coefficients"]
        n_valid  = int(len(coeffs) * crystal["murphy"]["tars_data_confidence"]
                       if "tars_data_confidence" in crystal.get("capacity",{})
                       else len(coeffs) * 0.9997)
        plan_a = self.solver.plan_a_progress(n_valid, 42)
        # Verify SHA256
        sha_match = (hashlib.sha256(coeffs.tobytes()).hexdigest()[:16] ==
                     crystal["tars_auth"])
        return {
            "book_decode":        book,
            "coord_lat":          lat, "coord_lon": lon,
            "dms_string":         dec._decimal_to_dms(lat, lon),
            "plan_A":             plan_a,
            "sha256_verified":    sha_match,
            "n_coeffs_valid":     n_valid,
            "murphys_equation":   crystal["murphy"]["equation_string"],
            "state":              (DecoderState.AUTHENTICATED.value
                                   if sha_match else DecoderState.ERROR.value),
        }


# ══════════════════════════════════════════════════════════════════════════════
# §9  BULK COMMUNICATION CHANNEL
# ══════════════════════════════════════════════════════════════════════════════
class BulkCommunicationChannel:
    """
    5D gravitational channel physics for bulk-to-brane signal transmission.
    Gravity is the only force that permeates the bulk in braneworld models [2,3].
    """

    def __init__(self):
        self.k_RS = RS_CURVATURE_K   # Randall-Sundrum curvature

    def signal_attenuation(self, y_bulk_m: float,
                            freq_hz: float = 0.01) -> float:
        """
        Signal amplitude attenuation through bulk at distance y.
        Propagation in AdS₅: A(y) ∝ e^{−y/ℓ_RS} for evanescent modes,
        where ℓ_RS = 1/k (AdS curvature length).
        Zero mode: A(y) = e^{−2k|y|} (warp factor attenuation).
        """
        ell_RS = 1.0/self.k_RS
        return math.exp(-2*self.k_RS*abs(y_bulk_m))

    def kaluza_klein_spectrum(self, n_modes: int = 10,
                               extra_dim_size_m: float = None) -> pd.DataFrame:
        """
        KK graviton mass spectrum from compactified extra dimension [3].
        m_n = n π / L  (flat compactification)
        m_n ≈ x_n k e^{−kL}  (RS warped compactification)
        """
        if extra_dim_size_m is None:
            extra_dim_size_m = 1.0/self.k_RS
        L = extra_dim_size_m
        rows = []
        for n in range(n_modes+1):
            # Flat: m_n = n/L (in natural units)
            m_flat = n * HBAR * C_SI / L    # [J] converted to mass energy
            # RS warped (using Bessel zeros)
            bessel_approx = (2.405 + (n-1)*3.11) if n > 0 else 0.0
            m_RS   = bessel_approx * self.k_RS * math.exp(-self.k_RS*L) * HBAR*C_SI
            rows.append({
                "n_mode":     n,
                "m_flat_J":   m_flat,
                "m_flat_eV":  m_flat/1.602e-19,
                "m_RS_J":     m_RS,
                "m_RS_eV":    m_RS/1.602e-19,
                "is_massless": n == 0,
                "type":       "Massless graviton" if n==0 else f"KK mode {n}",
            })
        return pd.DataFrame(rows)

    def newton_5d_correction(self, r_m: float) -> float:
        """
        5D correction to Newton's gravitational law at short range [3]:
          ΔU/U ≈ (2/3)(ℓ_RS/r)²   for r ≫ ℓ_RS
        Returns fractional deviation from 1/r² law.
        """
        ell = 1.0/self.k_RS
        return (2.0/3.0) * (ell/r_m)**2

    def channel_capacity_profile(self, snr_db_arr: np.ndarray,
                                  BW_hz: float = 0.01) -> np.ndarray:
        """Shannon capacity C = B·log₂(1+SNR) for gravity channel."""
        snr_lin = 10**(snr_db_arr/10)
        return BW_hz * np.log2(1 + snr_lin)

    def coherence_time(self, freq_hz: float = 0.01,
                        turbulence_param: float = 1e-6) -> float:
        """
        Coherence time of bulk gravity signal:
          t_coh ≈ 1/(Δf_Doppler) where Δf from bulk geometry fluctuations.
        Very long coherence: gravity is classical at macroscopic scales.
        """
        return 1.0 / (freq_hz * turbulence_param)


# ══════════════════════════════════════════════════════════════════════════════
# §10  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_session_state():
    enc  = GravitySignalEncoder()
    dec  = GravitySignalDecoder()
    D: Dict[str, Any] = {
        "tess_geom":          TesseractGeometry(),
        "tess_t_angle":       0.0,
        "tess_rot_planes":    ["XW","YW","ZW"],
        "tess_bookshelf":     None,
        "tess_bulk":          None,
        "grav_enc":           enc,
        "grav_dec":           dec,
        "grav_message":       "STAY",
        "grav_scheme":        EncodingScheme.DUST_BINARY.name,
        "grav_encoded":       None,
        "grav_watch_signal":  None,
        "grav_decoded":       None,
        "murphy_solver":      MurphyEquationSolver(),
        "murphy_wdw":         None,
        "murphy_lambda":      1.0e-52,
        "murphy_coeffs":      None,
        "murphy_plan_a":      None,
        "tars_crystal":       None,
        "tars_decoded":       None,
        "bulk_channel":       BulkCommunicationChannel(),
        "bulk_kk":            None,
        "coord_lat":          40.8897,
        "coord_lon":          -83.8564,
        "decoder_state":      DecoderState.IDLE.value,
        "n_coeffs_known":     0,
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# §11  MATPLOTLIB STYLE
# ══════════════════════════════════════════════════════════════════════════════
MPL_STYLE = {
    "figure.facecolor":  "#04060e",
    "axes.facecolor":    "#060810",
    "axes.edgecolor":    "#10143a",
    "axes.labelcolor":   "#E8C46A",
    "axes.grid":         True,
    "grid.color":        "#0a0e28",
    "grid.linestyle":    ":",
    "grid.alpha":        0.5,
    "xtick.color":       "#303878",
    "ytick.color":       "#303878",
    "xtick.labelsize":   6,
    "ytick.labelsize":   6,
    "axes.labelsize":    7,
    "axes.titlesize":    8,
    "axes.titlecolor":   "#c040ff",
    "text.color":        "#E8C46A",
    "font.family":       "monospace",
    "legend.facecolor":  "#060810",
    "legend.edgecolor":  "#10143a",
    "legend.fontsize":   6,
    "figure.dpi":        110,
    "savefig.facecolor": "#04060e",
    "axes.spines.top":   False,
    "axes.spines.right": False,
}
def _mpl(): plt.rcParams.update(MPL_STYLE)


# ══════════════════════════════════════════════════════════════════════════════
# §12  PLOTTING FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

# ── §12.1  Tesseract 4D projection ───────────────────────────────────────────
def _plot_tesseract(geom: TesseractGeometry, t_angle: float,
                    slices: np.ndarray = None) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#04060e")

    # Left: 2D projection at current angle
    ax1 = axes[0]
    ax1.set_facecolor("#020308")
    v2d, v4d = geom.animate_frame(t_angle, ['XW','YW','ZW'], [0.5,0.7,0.3])
    # Draw edges, coloured by 4th-coordinate (w-value)
    w_vals = v4d[:, 3]
    w_norm = (w_vals - w_vals.min())/(w_vals.max()-w_vals.min()+1e-10)
    for i, j in geom.edges:
        w_mid = 0.5*(w_norm[i] + w_norm[j])
        clr   = CMAP_TESSERACT(w_mid)
        ax1.plot([v2d[i,0], v2d[j,0]], [v2d[i,1], v2d[j,1]],
                 color=clr, lw=1.0, alpha=0.85)
    ax1.scatter(v2d[:,0], v2d[:,1], c=w_norm, cmap=CMAP_TESSERACT,
                s=30, zorder=5, edgecolors="#ffffff", lw=0.3)
    ax1.set_xlim(-2, 2); ax1.set_ylim(-2, 2)
    ax1.set_aspect("equal")
    ax1.set_xlabel("projected x"); ax1.set_ylabel("projected y")
    ax1.set_title(f"4D TESSERACT PROJECTION  t={t_angle:.2f}rad\n"
                  f"(coloured by 4th dimension W)")
    ax1.set_facecolor("#020308")

    # Mid: bookshelf time-slice heatmap
    ax2 = axes[1]
    if slices is None:
        slices = geom.bookshelf_time_slices()
    im = ax2.imshow(slices, cmap=CMAP_BOOKSHELF, aspect="auto",
                    origin="upper", vmin=0, vmax=1)
    ax2.set_xlabel("Book position (column)"); ax2.set_ylabel("Time slice (row)")
    ax2.set_title("BOOKSHELF TIME SLICES\n"
                  "(Dark=book in, Bright=book displaced)")
    plt.colorbar(im, ax=ax2, shrink=0.7, label="Displacement")
    # Highlight Cooper's message rows
    for t_row in range(8, 16):
        ax2.axhline(t_row-0.5, color="#E8C46A", lw=0.5, alpha=0.4)
    ax2.text(1, 12, "Cooper's\ncoords", color="#E8C46A",
             fontsize=6, va="center")

    # Right: bulk warped geometry
    ax3 = axes[2]
    bulk  = BulkCommunicationChannel()
    y_arr = np.linspace(-1e-14, 1e-14, 300)
    warp  = np.array([bulk.signal_attenuation(y) for y in y_arr])
    ax3.plot(y_arr*1e14, warp, color="#c040ff", lw=1.3)
    ax3.fill_between(y_arr*1e14, warp, 0, alpha=0.15, color="#c040ff")
    ax3.axvline(0, color="#E8C46A", lw=1.0, ls="--", label="Our brane (y=0)")
    ax3.set_xlabel("Bulk coordinate y [×10⁻¹⁴ m]")
    ax3.set_ylabel("Warp factor e^{-2k|y|}")
    ax3.set_title("RANDALL-SUNDRUM WARP FACTOR\n"
                  "(gravity signal attenuation into bulk)")
    ax3.legend(fontsize=6)

    plt.tight_layout()
    return fig


# ── §12.2  Gravity signal encoding/decoding ────────────────────────────────
def _plot_encoding(encoded: Dict, scheme_name: str) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.patch.set_facecolor("#04060e")

    # Left top: bookshelf displacement
    ax1 = axes[0, 0]
    disp = encoded["displacement"]
    x    = np.arange(len(disp))
    ax1.bar(x, encoded["displacement_m"]*100, color=CMAP_BOOKSHELF(disp),
            alpha=0.90, width=0.8)
    ax1.set_xlabel("Book index"); ax1.set_ylabel("Displacement [cm]")
    ax1.set_title(f"BOOKSHELF DUST DISPLACEMENT\n"
                  f"Message: '{encoded['message']}'  "
                  f"({encoded['n_bits_encoded']} bits)")
    ax1.axhline(2.5, color="#EF5350", lw=0.7, ls="--",
                label="Detection threshold (2.5cm)")
    ax1.legend(fontsize=6)

    # Right top: bit density visualization
    ax2 = axes[0, 1]
    bits_arr = np.array([int(b) for b in encoded["bits"]])
    ax2.imshow(bits_arr.reshape(1,-1), cmap="RdYlGn", aspect="auto",
               vmin=0, vmax=1)
    ax2.set_xlabel("Bit position"); ax2.set_yticks([])
    ax2.set_title(f"BIT STREAM VISUALIZATION\n"
                  f"Density: {encoded['bit_density']*100:.1f}% ones  "
                  f"CRC-16: {encoded['checksum_crc16']:04X}")

    # Left bottom: watch signal
    ax3 = axes[1, 0]
    enc2   = GravitySignalEncoder()
    key_bits = encoded["bits"][:32]
    watch_d = enc2.encode_watch_hand(key_bits, tick_duration_s=0.3)
    ax3.plot(watch_d["t"], watch_d["signal"], color="#4FC3F7", lw=0.8)
    for tt, tb in zip(watch_d["tick_times"], watch_d["tick_bits"]):
        ax3.axvline(tt, color="#81C784" if tb else "#EF5350",
                    lw=0.5, alpha=0.5)
    ax3.set_xlabel("Time [s]"); ax3.set_ylabel("Gravity pulse amplitude")
    ax3.set_title(f"WATCH-HAND GRAVITY SIGNAL  (32 bits → time encoding)\n"
                  f"Long gap=1 (green), Short gap=0 (red)")

    # Right bottom: BPSK signal + spectrum
    ax4 = axes[1, 1]
    bpsk_d = enc2.encode_bpsk(key_bits[:16], bit_duration_s=0.5)
    ax4.plot(bpsk_d["t"], bpsk_d["signal"], color="#CE93D8", lw=0.7, alpha=0.85)
    ax4.set_xlabel("Time [s]"); ax4.set_ylabel("h(t) strain")
    ax4.set_title(f"BPSK GRAVITY CARRIER MODULATION\n"
                  f"f_c={enc2.carrier:.3f} Hz  "
                  f"Phase flip at each '1' bit")
    # Overlay detected phases
    n_bit = int(0.5 * enc2.fs)
    for i, b in enumerate(key_bits[:16]):
        x0 = i*0.5; x1 = x0+0.5
        ax4.axvspan(x0, x1, alpha=0.08,
                    color="#81C784" if b=='1' else "#EF5350")

    plt.tight_layout()
    return fig


# ── §12.3  Wheeler-DeWitt wavefunction ────────────────────────────────────────
def _plot_wdw(result: Dict) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.patch.set_facecolor("#04060e")

    a    = result["a"]
    Psi  = result["Psi"]
    prob = result["prob"]
    V    = result["V"]

    # 1. Wavefunction
    ax1 = axes[0,0]
    ax1.plot(a, Psi, color="#c040ff", lw=1.3, label="Ψ(a)")
    ax1.axhline(0, color="#1a1a3a", lw=0.5)
    ax1.set_xlabel("Scale factor a"); ax1.set_ylabel("Ψ(a)")
    ax1.set_title("WHEELER-DeWITT WAVEFUNCTION\n(Minisuperspace, Hartle-Hawking BC)")
    ax1.legend(fontsize=6)

    # 2. Probability density
    ax2 = axes[0,1]
    ax2.fill_between(a, prob, 0, alpha=0.3, color="#c040ff")
    ax2.plot(a, prob, color="#c040ff", lw=1.2, label="|Ψ(a)|²")
    ax2.axvline(result["max_prob_a"], color="#E8C46A", lw=0.8, ls="--",
                label=f"Peak a={result['max_prob_a']:.3f}")
    ax2.set_xlabel("Scale factor a"); ax2.set_ylabel("|Ψ|²")
    ax2.set_title("PROBABILITY DENSITY |Ψ(a)|²")
    ax2.legend(fontsize=6)

    # 3. Effective potential
    ax3 = axes[0,2]
    ax3.plot(a, V, color="#FF8800", lw=1.2, label="V(a,φ)")
    ax3.axhline(0, color="#1a1a3a", lw=0.5)
    ax3.fill_between(a, V, 0, where=(V<0), alpha=0.2, color="#EF5350",
                     label="V<0 (classically allowed)")
    ax3.fill_between(a, V, 0, where=(V>0), alpha=0.15, color="#4FC3F7",
                     label="V>0 (quantum tunnelling)")
    ax3.set_xlabel("Scale factor a"); ax3.set_ylabel("V(a)")
    ax3.set_title("WHEELERDE-WITT POTENTIAL V(a)")
    ax3.legend(fontsize=5.5)

    # 4. Lambda sensitivity
    ax4 = axes[1,0]
    solver = MurphyEquationSolver()
    lambdas= [1e-55, 1e-53, 1e-52, 1e-51, 1e-50]
    for lam in lambdas:
        res_l = solver.solve_wdw_shooting(Lambda=lam, n_pts=300)
        ax4.plot(res_l["a"], res_l["prob"],
                 label=f"Λ={lam:.0e}", lw=0.8, alpha=0.8)
    ax4.set_xlabel("Scale factor a"); ax4.set_ylabel("|Ψ|²")
    ax4.set_title("SENSITIVITY TO Λ (cosmological constant)")
    ax4.legend(fontsize=5)

    # 5. Murphy's coefficients bar
    ax5 = axes[1,1]
    solver2 = MurphyEquationSolver()
    mcoeffs = solver2.murphy_coefficients_from_tars(42)
    c_arr   = mcoeffs["coefficients"]
    colors5 = ["#c040ff" if v>0 else "#EF5350" for v in c_arr]
    ax5.bar(range(42), c_arr/np.abs(c_arr).max(), color=colors5, alpha=0.85)
    ax5.axhline(0, color="#1a1a3a", lw=0.5)
    ax5.set_xlabel("Coefficient index"); ax5.set_ylabel("Normalised value")
    ax5.set_title("MURPHY'S EQUATION — 42 TARS COEFFICIENTS\n"
                  "(quantum gravity singularity data)")

    # 6. Bekenstein entropy info
    ax6 = axes[1,2]
    bek = solver.bekenstein_entropy(GARG_MASS_KG)
    items = [
        ("S_BH [J/K]",           bek["S_BH_JK"]),
        ("N_bits (Bekenstein)",   bek["N_info_bits"]),
        ("Horizon area [m²]",     bek["horizon_area_m2"]),
        ("N_Planck_cells",        bek["N_Planck_cells"]),
    ]
    ax6.axis("off")
    y = 0.95
    ax6.text(0.05, y, "BEKENSTEIN-HAWKING INFO CAPACITY",
             fontsize=8, color="#c040ff", fontfamily="monospace",
             fontweight="bold", transform=ax6.transAxes)
    y -= 0.10
    for lbl, val in items:
        ax6.text(0.05, y, f"  {lbl:<28}", fontsize=7, color="#888",
                 fontfamily="monospace", transform=ax6.transAxes)
        ax6.text(0.05, y-0.065, f"  = {val:.4e}", fontsize=7, color="#E8C46A",
                 fontfamily="monospace", fontweight="bold",
                 transform=ax6.transAxes)
        y -= 0.14
    cap = solver.singularity_data_capacity()
    ax6.text(0.05, y, f"  Useful bits (QEC): {cap['useful_bits_after_QEC']:.3e}",
             fontsize=7, color="#81C784", fontfamily="monospace",
             transform=ax6.transAxes)

    plt.tight_layout()
    return fig


# ── §12.4  TARS data crystal visualization ────────────────────────────────────
def _plot_tars_crystal(crystal: Dict, decoded: Dict) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.patch.set_facecolor("#04060e")

    # 1. Watch signal
    ax1 = axes[0,0]
    ws  = crystal["watch_signal"]
    ax1.plot(ws["t"], ws["signal"], color="#4FC3F7", lw=0.7, alpha=0.9)
    for tt, tb in zip(ws["tick_times"][:40], ws["tick_bits"][:40]):
        ax1.axvline(tt, color="#81C784" if tb else "#EF5350",
                    lw=0.4, alpha=0.6)
    ax1.set_xlabel("Time [s]"); ax1.set_ylabel("Gravity pulse")
    ax1.set_title("TARS WATCH-HAND SIGNAL\n(Cooper's second-hand gravity message)")

    # 2. BPSK signal spectrogram
    ax2 = axes[0,1]
    bpsk = crystal["bpsk_signal"]
    dec  = GravitySignalDecoder(fs=1000.0)
    f_sg, t_sg, Sxx = dec.spectrogram_analysis(bpsk["signal"][:5000], nperseg=128)
    ax2.pcolormesh(t_sg, f_sg[:30], np.log1p(Sxx[:30]),
                   cmap="inferno", shading="gouraud")
    ax2.set_xlabel("Time [s]"); ax2.set_ylabel("Frequency [Hz]")
    ax2.set_title("BPSK CARRIER SPECTROGRAM\n(quantum data bitstream)")

    # 3. Bookshelf spatial pattern
    ax3 = axes[0,2]
    book = crystal["bookshelf"]
    disp = book["displacement"]
    ax3.bar(range(len(disp)), book["displacement_m"]*100,
            color=CMAP_BOOKSHELF(disp), alpha=0.9, width=0.9)
    ax3.set_xlabel("Book position"); ax3.set_ylabel("Displacement [cm]")
    ax3.set_title(f"BOOKSHELF SPATIAL PATTERN\n"
                  f"CRC-16={book['checksum_crc16']:04X}")

    # 4. Murphy's 42 coefficients
    ax4 = axes[1,0]
    coeffs = crystal["murphy"]["coefficients"]
    sc4 = ax4.scatter(range(42), coeffs/np.abs(coeffs).max(),
                       c=range(42), cmap="plasma", s=50,
                       edgecolors="#E8C46A", lw=0.4)
    ax4.axhline(0, color="#1a1a3a", lw=0.5)
    ax4.set_xlabel("Coefficient index")
    ax4.set_ylabel("Normalised value")
    ax4.set_title(f"42 MURPHY COEFFICIENTS\n"
                  f"SHA-256: {crystal['tars_auth']}")

    # 5. Plan A progress gauge
    ax5 = axes[1,1]
    plan = decoded["plan_A"]
    frac = plan["fraction"]
    theta_arr = np.linspace(-math.pi/2, -math.pi/2 + frac*2*math.pi, 300)
    ax5.plot(np.cos(theta_arr), np.sin(theta_arr),
             color="#81C784" if frac >= 1.0 else "#E8C46A", lw=8, solid_capstyle="round")
    ax5.add_patch(Circle((0,0), 0.75, color="#060810", zorder=3))
    ax5.text(0, 0, f"{plan['pct_complete']:.1f}%",
             ha="center", va="center", fontsize=18,
             color="#81C784" if frac>=1 else "#E8C46A",
             fontfamily="monospace", fontweight="bold")
    ax5.text(0, -0.35, f"PLAN A", ha="center", fontsize=9,
             color="#E8C46A", fontfamily="monospace")
    ax5.text(0, -0.55, f"{plan['known']}/{plan['total_needed']} coefficients",
             ha="center", fontsize=7, color="#888", fontfamily="monospace")
    ax5.set_xlim(-1.2, 1.2); ax5.set_ylim(-1.2, 1.2)
    ax5.set_aspect("equal"); ax5.axis("off")
    ax5.set_title(f"MURPHY'S EQUATION PROGRESS\n"
                  f"SOLVED: {'YES ✓' if plan['solved'] else 'NO'}")

    # 6. Decoded info
    ax6 = axes[1,2]
    ax6.axis("off")
    items_dec = [
        ("Status",              decoded["state"]),
        ("SHA-256 verified",    str(decoded["sha256_verified"])),
        ("Coefficients valid",  f"{decoded['n_coeffs_valid']}/42"),
        ("Coordinate (lat)",    f"{decoded['coord_lat']:.4f}°"),
        ("Coordinate (lon)",    f"{decoded['coord_lon']:.4f}°"),
        ("DMS",                 decoded["dms_string"]),
        ("Plan A solved",       str(decoded["plan_A"]["solved"])),
    ]
    y = 0.96
    ax6.text(0.05, y, "TARS DATA CRYSTAL — DECODED",
             fontsize=8, color="#c040ff", fontfamily="monospace",
             fontweight="bold", transform=ax6.transAxes)
    y -= 0.10
    for lbl, val in items_dec:
        clr = "#81C784" if "True" in str(val) or "YES" in str(val) else (
              "#EF5350" if "False" in str(val) or "NO" in str(val) else "#E8C46A")
        ax6.text(0.05, y, f"  {lbl}:", fontsize=6.5, color="#888",
                 fontfamily="monospace", transform=ax6.transAxes)
        ax6.text(0.05, y-0.06, f"    {val}", fontsize=6.5, color=clr,
                 fontfamily="monospace", fontweight="bold",
                 transform=ax6.transAxes)
        y -= 0.13
    # Murphy's equation string
    eq = decoded.get("murphys_equation","")
    ax6.text(0.05, y-0.02,
             "Murphy's Equation:\n  " + eq[:60] + "...",
             fontsize=5.5, color="#CE93D8", fontfamily="monospace",
             transform=ax6.transAxes, wrap=True)

    plt.tight_layout()
    return fig


# ── §12.5  KK tower and bulk channel ─────────────────────────────────────────
def _plot_bulk_channel(bulk: BulkCommunicationChannel) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    fig.patch.set_facecolor("#04060e")

    # 1. Warp factor
    ax1 = axes[0,0]
    y_arr = np.linspace(0, 5e-14, 200)
    warp  = np.array([bulk.signal_attenuation(y) for y in y_arr])
    ax1.semilogy(y_arr*1e14, warp+1e-50, color="#c040ff", lw=1.3)
    ax1.fill_between(y_arr*1e14, warp+1e-50, 1e-50, alpha=0.15, color="#c040ff")
    ax1.set_xlabel("Bulk coordinate y [×10⁻¹⁴ m]"); ax1.set_ylabel("Signal amplitude")
    ax1.set_title("SIGNAL ATTENUATION INTO BULK\ne^{-2k|y|} warp factor")

    # 2. KK mass spectrum
    ax2 = axes[0,1]
    kk_df = bulk.kaluza_klein_spectrum(n_modes=8)
    ax2.bar(kk_df["n_mode"], kk_df["m_RS_eV"].fillna(0),
            color=["#E8C46A"]+["#c040ff"]*8, alpha=0.85)
    ax2.set_xlabel("KK mode n"); ax2.set_ylabel("Mass [eV/c²]")
    ax2.set_title("KALUZA-KLEIN GRAVITON SPECTRUM\n(n=0: massless, n≥1: massive)")

    # 3. Newton 5D correction
    ax3 = axes[0,2]
    r_arr = np.logspace(-10, -5, 200)
    corr  = np.array([bulk.newton_5d_correction(r) for r in r_arr])
    ax3.loglog(r_arr*1e6, corr, color="#FF8800", lw=1.2)
    ax3.axhline(0.01, color="#EF5350", lw=0.7, ls="--",
                label="1% deviation threshold")
    ax3.set_xlabel("Range r [μm]"); ax3.set_ylabel("ΔU/U (5D correction)")
    ax3.set_title("5D NEWTON LAW CORRECTION\n(observable if ℓ_RS large enough)")
    ax3.legend(fontsize=6)

    # 4. Shannon capacity
    ax4 = axes[1,0]
    snr_db = np.linspace(-10, 30, 200)
    BW_arr = [1e-4, 1e-3, 1e-2, 1e-1]  # [Hz]
    for BW in BW_arr:
        cap = bulk.channel_capacity_profile(snr_db, BW)
        ax4.plot(snr_db, cap, lw=1.0, label=f"B={BW:.0e}Hz")
    ax4.set_xlabel("SNR [dB]"); ax4.set_ylabel("Capacity [bits/s]")
    ax4.set_title("GRAVITY CHANNEL CAPACITY\n(Shannon limit, low-BW regime)")
    ax4.legend(fontsize=5.5)

    # 5. Signal through time (bulk interference)
    ax5 = axes[1,1]
    enc  = GravitySignalEncoder()
    bits = enc.text_to_binary("STAY")
    bpsk = enc.encode_bpsk(bits[:16], bit_duration_s=0.5)
    # Add bulk noise (1/f characteristic)
    n  = len(bpsk["signal"])
    f  = sci_fft.rfftfreq(n, 1/1000.0)
    f[0] = 1e-10
    pink = np.random.randn(len(f)) + 1j*np.random.randn(len(f))
    pink /= np.sqrt(np.abs(f))
    noise = np.real(sci_fft.irfft(pink, n=n))
    noise = noise/noise.std() * 0.3
    ax5.plot(bpsk["t"][:1000], bpsk["signal"][:1000]+noise[:1000],
             color="#3a3a60", lw=0.4, label="Received (noisy)", alpha=0.7)
    ax5.plot(bpsk["t"][:1000], bpsk["signal"][:1000],
             color="#c040ff", lw=1.0, label="Clean signal")
    ax5.set_xlabel("Time [s]"); ax5.set_ylabel("Gravity amplitude")
    ax5.set_title("BULK CHANNEL — SIGNAL vs NOISE\n('STAY' encoded in BPSK)")
    ax5.legend(fontsize=6)

    # 6. Coherence profile
    ax6 = axes[1,2]
    freq_arr = np.logspace(-4, 1, 200)
    coh_arr  = np.array([bulk.coherence_time(f) for f in freq_arr])
    ax6.loglog(freq_arr, coh_arr/YEAR_S, color="#81C784", lw=1.3)
    ax6.set_xlabel("Signal frequency [Hz]"); ax6.set_ylabel("Coherence time [yr]")
    ax6.set_title("BULK GRAVITY COHERENCE TIME\n(gravity is classically stable)")

    plt.tight_layout()
    return fig


# ── §12.6  Cooper's Coordinate decoder ──────────────────────────────────────
def _plot_coordinate_decode(bits: str, lat: float, lon: float) -> plt.Figure:
    _mpl()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor("#04060e")

    # Left: binary bit stream
    ax1 = axes[0]
    if bits:
        bits_arr = np.array([int(b) for b in bits[:64]])
        n_cols   = 8
        n_rows   = math.ceil(len(bits_arr)/n_cols)
        pad      = n_cols*n_rows - len(bits_arr)
        grid     = np.pad(bits_arr, (0,pad)).reshape(n_rows, n_cols)
        ax1.imshow(grid, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
        # Annotate bits
        for r in range(n_rows):
            for c in range(n_cols):
                idx = r*n_cols + c
                if idx < len(bits_arr):
                    ax1.text(c, r, str(bits_arr[idx]),
                             ha="center", va="center",
                             fontsize=8, color="#000", fontfamily="monospace")
        ax1.set_title(f"BINARY COORDINATE STREAM\n"
                      f"(watch-hand gravity signal decoded)")
        ax1.set_xlabel("Bit position (column)")
        ax1.set_ylabel("Byte (row)")

    # Right: coordinate verification
    ax2 = axes[1]
    ax2.axis("off")
    dec  = GravitySignalDecoder()
    dms  = dec._decimal_to_dms(lat, lon)
    lines = [
        ("COOPER'S GRAVITY MESSAGE", "#c040ff", 9, True),
        ("", "#000", 6, False),
        ("Encoding:      Watch second-hand", "#888", 7, False),
        (f"Binary stream: {bits[:16]}...", "#888", 7, False),
        ("", "#000", 6, False),
        ("DECODED COORDINATES:", "#E8C46A", 8, True),
        (f"  Latitude:   {lat:.4f}°", "#E8C46A", 8, False),
        (f"  Longitude:  {lon:.4f}°", "#E8C46A", 8, False),
        (f"  DMS:        {dms}", "#E8C46A", 7, False),
        ("", "#000", 6, False),
        ("IDENTIFIED LOCATION:", "#81C784", 8, True),
        ("  NASA Gravity Observatory", "#81C784", 8, False),
        ("  Quantum Research Facility", "#81C784", 8, False),
        ("  Cooper & Brand Mission Control", "#81C784", 7, False),
        ("", "#000", 6, False),
        ("MESSAGE VERIFIED:  ✓ TARS SHA-256", "#4FC3F7", 8, False),
        ("PLAN A:  UNLOCKED  ✓", "#81C784", 9, True),
    ]
    y = 0.97
    for text, clr, fsize, bold in lines:
        ax2.text(0.05, y, text, color=clr, fontsize=fsize,
                 fontfamily="monospace",
                 fontweight="bold" if bold else "normal",
                 transform=ax2.transAxes)
        y -= 0.056

    plt.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# §13  MAIN STREAMLIT PAGE
# ══════════════════════════════════════════════════════════════════════════════
def tesseract_decoder_page():
    init_session_state()
    _mpl()
    S = st.session_state

    st.markdown("""
    <div style="border-left:3px solid #c040ff;padding:.55rem 1.2rem;
                margin-bottom:1.2rem;background:rgba(192,64,255,0.03);
                font-family:monospace;">
    <div style="color:#c040ff;font-size:.95rem;letter-spacing:.12em;font-weight:600;">
    ◈ TESSERACT DECODER &amp; QUANTUM GRAVITY ENGINE</div>
    <div style="color:#5a6a90;font-size:.62rem;margin-top:.2rem;">
    4D Tesseract Geometry · Gravity Signal Encoding/Decoding · Murphy's Equation ·
    Wheeler-DeWitt · Bekenstein Entropy · TARS Data Crystal · Bulk 5D Channel
    </div></div>""", unsafe_allow_html=True)

    (tab_tess, tab_encode, tab_decode,
     tab_wdw, tab_tars,
     tab_coord, tab_bulk) = st.tabs([
        "⬡ TESSERACT",
        "⇡ ENCODE SIGNAL",
        "⇣ DECODE SIGNAL",
        "Ψ MURPHY'S EQUATION",
        "◈ TARS DATA CRYSTAL",
        "📍 COORDINATE DECODER",
        "∿ BULK CHANNEL",
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1 — TESSERACT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_tess:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#c040ff;">[ TESSERACT CONTROLS ]</div>',
                        unsafe_allow_html=True)
            t_angle = st.slider("4D Rotation angle [rad]", 0.0, 2*math.pi,
                                 float(S["tess_t_angle"]), 0.05)
            S["tess_t_angle"] = t_angle
            geom    = S["tess_geom"]
            slices  = geom.bookshelf_time_slices(n_slices=24, n_books=32)
            S["tess_bookshelf"] = slices
            bulk    = BulkCommunicationChannel()
            bg_data = geom.bulk_geometry_profile()
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c0e0;
                        background:rgba(6,8,16,.92);padding:.65rem;
                        border:1px solid rgba(192,64,255,.18);border-radius:3px;
                        line-height:2.0;margin-top:.4rem;">
            <b style="color:#c040ff;">── HYPERCUBE ──</b><br>
            Vertices: <b>16</b> (±1 in 4D)<br>
            Edges:    <b>32</b><br>
            Faces:    <b>24</b> square faces<br>
            Cells:    <b>8</b> cubic cells<br>
            Rotation: <b>{math.degrees(t_angle):.1f}°</b> in XW/YW/ZW planes<br>
            <b style="color:#c040ff;">── BULK GEOMETRY ──</b><br>
            k_RS = <b>{bg_data['k_curvature_m']:.3e} m⁻¹</b><br>
            L_extra = <b>{bg_data['L_extra_m']:.3e} m</b><br>
            KK masses (n=1): <b>{bg_data['kk_masses_eV'][0]:.3e} eV</b>
            </div>""", unsafe_allow_html=True)

        with c2:
            fig = _plot_tesseract(geom, t_angle, slices)
            st.pyplot(fig, use_container_width=True); plt.close(fig)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — ENCODE SIGNAL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_encode:
        c1, c2 = st.columns([1, 3])
        with c1:
            msg    = st.text_input("Message to encode", value=S["grav_message"])
            scheme = st.selectbox("Encoding scheme",
                                   [e.name for e in EncodingScheme])
            n_books= st.slider("Number of book slots", 16, 128,
                                64, 8)
            S["grav_message"] = msg
            S["grav_scheme"]  = scheme

            if st.button("⇡ ENCODE MESSAGE", use_container_width=True,
                         type="primary"):
                enc  = GravitySignalEncoder()
                sch  = EncodingScheme[scheme]
                book = enc.encode_bookshelf(msg, n_books=n_books, scheme=sch)
                S["grav_encoded"]      = book
                S["grav_watch_signal"] = enc.encode_watch_hand(
                    book["bits"][:32], tick_duration_s=0.4)
                S["decoder_state"]     = DecoderState.RECEIVING.value

            enc_data = S.get("grav_encoded")
            if enc_data:
                enc  = GravitySignalEncoder()
                bits = enc.text_to_binary(msg)
                morse= enc.text_to_morse(msg)
                st.markdown(f"""
                <div style="font-family:monospace;font-size:.57rem;color:#c0c0e0;
                            background:rgba(6,8,16,.92);padding:.65rem;
                            border:1px solid rgba(192,64,255,.12);border-radius:3px;
                            line-height:1.9;margin-top:.4rem;">
                Binary: <code>{bits[:32]}{'...' if len(bits)>32 else ''}</code><br>
                Morse:  <code>{morse[:40]}{'...' if len(morse)>40 else ''}</code><br>
                Bits encoded: <b>{enc_data['n_bits_encoded']}</b><br>
                Bit density: <b>{enc_data['bit_density']*100:.1f}%</b><br>
                CRC-16: <b>{enc_data['checksum_crc16']:04X}</b><br>
                Channel cap: <b>{enc.channel_capacity_bits_per_s(10.0):.4f} bits/s</b>
                </div>""", unsafe_allow_html=True)

        with c2:
            enc_data = S.get("grav_encoded")
            if enc_data:
                fig = _plot_encoding(enc_data, scheme)
                st.pyplot(fig, use_container_width=True); plt.close(fig)
            else:
                st.info("Enter a message and click Encode.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — DECODE SIGNAL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_decode:
        enc_data = S.get("grav_encoded")
        if enc_data is not None:
            if st.button("⇣ DECODE SIGNAL", use_container_width=True,
                         type="primary"):
                dec  = GravitySignalDecoder()
                result = dec.decode_bookshelf(
                    enc_data["displacement_m"],
                    EncodingScheme[S["grav_scheme"]])
                S["grav_decoded"]  = result
                S["decoder_state"] = result["state"]

            result = S.get("grav_decoded")
            if result:
                c1, c2 = st.columns([1, 2])
                with c1:
                    state_c = {"DECODED":"#81C784","ERROR":"#EF5350",
                               "AUTHENTICATED":"#E8C46A"}.get(
                                   result["state"].split()[0], "#888")
                    st.markdown(f"""
                    <div style="font-family:monospace;font-size:.58rem;color:#c0c0e0;
                                background:rgba(6,8,16,.92);padding:.75rem;
                                border:1px solid rgba(192,64,255,.18);border-radius:3px;
                                line-height:2.1;">
                    <b style="color:#c040ff;">── DECODER OUTPUT ──</b><br>
                    Status: <b style="color:{state_c};">{result['state']}</b><br>
                    Decoded text: <b style="color:#E8C46A;">{result['decoded_text'][:40]}</b><br>
                    Hamming errors: <b>{result['hamming_errors']}</b><br>
                    CRC-16: <b>{result['crc16']:04X}</b><br>
                    Lat: <b>{result['lat_deg']:.4f}°</b><br>
                    Lon: <b>{result['lon_deg']:.4f}°</b><br>
                    DMS: <b>{result['coord_dms']}</b>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    dec2 = GravitySignalDecoder()
                    ws = S.get("grav_watch_signal")
                    if ws is not None:
                        wd = dec2.decode_watch_hand(ws["tick_times"], ws["tick_bits"])
                        _mpl()
                        fig_d, axes_d = plt.subplots(1, 2, figsize=(11, 4))
                        fig_d.patch.set_facecolor("#04060e")
                        axes_d[0].plot(ws["t"], ws["signal"], color="#4FC3F7", lw=0.7)
                        for tt, tb in zip(ws["tick_times"][:30], ws["tick_bits"][:30]):
                            axes_d[0].axvline(tt, color="#81C784" if tb else "#EF5350",
                                              lw=0.4, alpha=0.6)
                        axes_d[0].set_xlabel("Time [s]"); axes_d[0].set_ylabel("Pulse")
                        axes_d[0].set_title("Watch-hand signal")
                        bits_disp = np.array([int(b) for b in wd["bits"][:64]])
                        if len(bits_disp) > 0:
                            axes_d[1].bar(range(len(bits_disp)), bits_disp,
                                          color=["#81C784" if b else "#EF5350"
                                                 for b in bits_disp], alpha=0.8)
                        axes_d[1].set_xlabel("Bit index"); axes_d[1].set_ylabel("Bit")
                        axes_d[1].set_title(f"Decoded: '{wd['decoded_text'][:20]}'")
                        plt.tight_layout()
                        st.pyplot(fig_d, use_container_width=True); plt.close(fig_d)
        else:
            st.info("Encode a message first (Tab 2), then decode here.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 4 — MURPHY'S EQUATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_wdw:
        c1, c2 = st.columns([1, 3])
        with c1:
            lam = st.number_input("Cosmological constant Λ",
                                   value=float(S["murphy_lambda"]),
                                   format="%.3e", step=1e-53)
            n_coeffs = st.slider("Known TARS coefficients (of 42)",
                                  0, 42, int(S["n_coeffs_known"]), 1)
            S["murphy_lambda"]   = lam
            S["n_coeffs_known"]  = n_coeffs

            if st.button("Ψ SOLVE WHEELER-DeWITT",
                         use_container_width=True, type="primary"):
                solver = S["murphy_solver"]
                S["murphy_wdw"]    = solver.solve_wdw_shooting(Lambda=lam)
                S["murphy_coeffs"] = solver.murphy_coefficients_from_tars(42)
                S["murphy_plan_a"] = solver.plan_a_progress(n_coeffs, 42)

            plan = S.get("murphy_plan_a")
            if plan:
                pct   = plan["pct_complete"]
                p_clr = "#81C784" if pct>=100 else "#E8C46A" if pct>50 else "#EF5350"
                st.markdown(f"""
                <div style="font-family:monospace;font-size:.58rem;color:#c0c0e0;
                            background:rgba(6,8,16,.92);padding:.6rem;
                            border:1px solid rgba(192,64,255,.12);border-radius:3px;
                            line-height:1.9;">
                Plan A: <b style="color:{p_clr};">{pct:.1f}%</b><br>
                Known: <b>{plan['known']}</b>/42 coefficients<br>
                TARS contribution: <b>{plan['tars_contribution']}</b><br>
                Solved: <b style="color:{p_clr};">{'YES ✓' if plan['solved'] else 'NO'}</b><br>
                Can lift colony: <b>{'YES' if plan['can_lift_colony'] else 'NO'}</b>
                </div>""", unsafe_allow_html=True)

        with c2:
            wdw = S.get("murphy_wdw")
            if wdw:
                fig = _plot_wdw(wdw)
                st.pyplot(fig, use_container_width=True); plt.close(fig)
                bek = S["murphy_solver"].bekenstein_entropy()
                st.markdown(f"""
                <div style="font-family:monospace;font-size:.58rem;color:#c0c0e0;
                            background:rgba(6,8,16,.92);padding:.5rem;
                            border:1px solid rgba(192,64,255,.10);border-radius:3px;">
                Murphy's equation: <code>{S['murphy_solver'].murphy_coefficients_from_tars(42)['equation_string'][:80]}...</code>
                </div>""", unsafe_allow_html=True)
            else:
                st.info("Click Solve to run Wheeler-DeWitt integration.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 5 — TARS DATA CRYSTAL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_tars:
        if st.button("◈ GENERATE TARS CRYSTAL", use_container_width=True,
                     type="primary"):
            tdc = TARSDataCrystal()
            crystal = tdc.encode_crystal()
            decoded = tdc.decode_crystal(crystal)
            S["tars_crystal"] = crystal
            S["tars_decoded"] = decoded

        crystal = S.get("tars_crystal")
        decoded = S.get("tars_decoded")
        if crystal and decoded:
            state_clr = ("#81C784" if "AUTH" in decoded["state"]
                         else "#EF5350" if "ERROR" in decoded["state"]
                         else "#E8C46A")
            kpis = [
                ("Crystal bits",   str(crystal["crystal_size_bits"]),  "#c040ff"),
                ("SHA-256",        crystal["tars_auth"],                "#4FC3F7"),
                ("Coefficients",   "42/42",                            "#81C784"),
                ("Plan A",         f"{decoded['plan_A']['pct_complete']:.1f}%","#E8C46A"),
                ("Status",         decoded["state"][:12],               state_clr),
                ("Verified",       str(decoded["sha256_verified"]),     "#81C784"),
            ]
            cols = st.columns(len(kpis))
            for col, (lbl, val, clr) in zip(cols, kpis):
                col.markdown(
                    f'<div style="background:rgba(6,8,16,.9);border:1px solid {clr}44;'
                    f'padding:.35rem;text-align:center;border-radius:2px;font-family:monospace;">'
                    f'<div style="color:#444;font-size:.48rem;">{lbl}</div>'
                    f'<div style="color:{clr};font-size:.72rem;">{val}</div></div>',
                    unsafe_allow_html=True)
            fig = _plot_tars_crystal(crystal, decoded)
            st.pyplot(fig, use_container_width=True); plt.close(fig)
        else:
            st.info("Click 'Generate TARS Crystal' to run the full data pipeline.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 6 — COORDINATE DECODER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_coord:
        c1, c2 = st.columns([1, 2])
        with c1:
            lat_in = st.number_input("Latitude [decimal °]",
                                      value=float(S["coord_lat"]),
                                      format="%.4f")
            lon_in = st.number_input("Longitude [decimal °]",
                                      value=float(S["coord_lon"]),
                                      format="%.4f")
            S["coord_lat"] = lat_in; S["coord_lon"] = lon_in
            enc2   = GravitySignalEncoder()
            bits_c = enc2.coords_to_binary(lat_in, lon_in)
            morse_c= enc2.text_to_morse(f"{lat_in:.2f} {lon_in:.2f}")
            st.markdown(f"""
            <div style="font-family:monospace;font-size:.57rem;color:#c0c0e0;
                        background:rgba(6,8,16,.92);padding:.65rem;
                        border:1px solid rgba(192,64,255,.18);border-radius:3px;
                        line-height:2.0;">
            <b style="color:#c040ff;">── ENCODING ──</b><br>
            Decimal: <b>{lat_in:.4f}°, {lon_in:.4f}°</b><br>
            Binary (50-bit):<br>
            <code style="font-size:.55rem;">{bits_c[:25]}</code><br>
            <code style="font-size:.55rem;">{bits_c[25:50]}</code><br>
            Bits total: <b>{len(bits_c)}</b><br>
            Watch ticks needed: <b>{len(bits_c)}</b><br>
            <br>Cooper's NASA coords:<br>
            <b style="color:#E8C46A;">N 40°53'23"  W 83°51'23"</b><br>
            Binary: <code>{COOPER_MSG_BINARY[:20]}...</code>
            </div>""", unsafe_allow_html=True)

        with c2:
            fig_c = _plot_coordinate_decode(bits_c, lat_in, lon_in)
            st.pyplot(fig_c, use_container_width=True); plt.close(fig_c)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 7 — BULK CHANNEL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab_bulk:
        bulk = S["bulk_channel"]
        if S.get("bulk_kk") is None:
            S["bulk_kk"] = bulk.kaluza_klein_spectrum(n_modes=8)
        fig_b = _plot_bulk_channel(bulk)
        st.pyplot(fig_b, use_container_width=True); plt.close(fig_b)
        st.markdown('<div style="font-family:monospace;font-size:.62rem;color:#c040ff;margin-top:.5rem;">KALUZA-KLEIN GRAVITON MASS SPECTRUM</div>',
                    unsafe_allow_html=True)
        st.dataframe(S["bulk_kk"].round(6), use_container_width=True, hide_index=True)
