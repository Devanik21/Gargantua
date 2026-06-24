<div align="center">
  
#  INTERSTELLAR 
  


<img width="736" height="414" alt="image" src="https://github.com/user-attachments/assets/7f23e4ca-716b-437e-b237-16be36ddfbdc" />


> *"Mankind was born on Earth. It was never meant to die here."*
> **— Cooper, 2067**

<br>

</div>

---



## ◈ About This Repository

**Author:** Devanik (GitHub: [Devanik21](https://github.com/Devanik21))
**Repository:** INTERSTELLAR — Gargantua Science Platform · May 2026
**Affiliation:** Electronics & Communication Engineering, NIT Agartala · Samsung ISWDP Fellow (IISc)

INTERSTELLAR is a serious, research-grade, interactive science platform built as a rigorous tribute to Christopher Nolan's *Interstellar* (2014). It is **not** a fan page or a visualisation toy. It is a complete computational physics environment spanning **21,573 lines** of modular Python across nine files, orchestrating eight independent scientific backends through a single unified Streamlit command centre.

Every module implements genuine physics: the Kerr metric in Boyer-Lindquist coordinates is evaluated exactly; special and general relativistic time dilation is computed from the invariant line element; the Morris-Thorne traversable wormhole is treated through the Einstein field equations; the Tesseract decoder implements braneworld ADD/RS gravity and real signal encoding schemes (BPSK, OOK, bookshelf binary, Hamming codes); the Quantum Singularity laboratory covers Loop Quantum Gravity area spectra, BKL Kasner oscillations, Hawking Page curves via the island rule, out-of-time-order correlator scrambling, and AdS/CFT holographic entanglement.

The interface is rendered in a hand-crafted dark space theme — star-field background, Gargantua amber-gold glow, wormhole violet gradient, animated scan lines, monospace terminal typography — with zero external UI framework dependencies beyond Streamlit and Matplotlib.

---

## ◈ Platform Architecture

```
INTERSTELLAR/
│
├── ENDURANCE.py                ← Mission Control Frontend  (~2,579 lines)
│   ├── §1  Backend import system (safe-import with fallback UI)
│   ├── §2  Mission constants & TARS dialogue bank
│   ├── §3  Master CSS — star-field, Gargantua glow, wormhole gradient
│   ├── §4  Global session state initialisation
│   ├── §5  Background image loader (base64 injection)
│   ├── §6  Utility components: KPI cards, terminal blocks, progress bars
│   ├── §7  Sidebar: navigation, mission strip, TARS context engine
│   ├── §8  Boot sequence: animated terminal with system initialisation
│   ├── §9  Mission Overview: live KPI grid, Gargantua schematic, Plan A/B
│   ├── §10 System Status: dependency health, file system diagnostics
│   ├── §11 Safe backend wrappers with traceback recovery
│   ├── §12 Global Matplotlib dark theme injection
│   ├── §13 Welcome banner with phase-aware mission timeline
│   └── §14 Main router: dispatches page key → backend function
│
├── gravity_engine.py           ← Module I   — Kerr BH Physics  (~3,036 lines)
├── relativity_calculator.py    ← Module II  — SR/GR Engine     (~2,801 lines)
├── planet_analyzer.py          ← Module III — Habitability     (~2,706 lines)
├── wormhole_navigator.py       ← Module IV  — Wormhole Physics (~2,088 lines)
├── tesseract_decoder.py        ← Module V   — Gravity Signals  (~2,176 lines)
├── crew_telemetry.py           ← Module VI  — Ship & Crew      (~2,179 lines)
├── mission_reporter.py         ← Module VII — Mission Intel    (~1,808 lines)
├── quantum_singularity.py      ← Module VIII— Planck/LQG/BKL  (~2,200 lines)
│
└── requirements.txt
```

**Total:** 21,573 lines · 9 Python files · 8 science backends · 1 mission control frontend

---

<img width="1339" height="591" alt="image" src="https://github.com/user-attachments/assets/b66987dc-5ada-4562-9ffc-2b50cc916d6e" />


## ◈ Navigation Map

```
SIDEBAR MODULES
│
├── ✦  MISSION OVERVIEW     — Live mission dashboard
├── ⬡  GRAVITY ENGINE       — Kerr BH · Accretion disk · Gravitational waves · Tidal forces
├── ⏱  RELATIVITY CALC      — SR/GR · Time dilation · Twin paradox · Cooper-Murph divergence
├── 🪐  PLANET SCANNER       — ESI · Habitability zone · Atmosphere · Biosignatures
├── ⟳  WORMHOLE NAVIGATOR   — Morris-Thorne geometry · Exotic matter · Traversal calculator
├── ◈  TESSERACT DECODER    — 4D geometry · Gravity signals · Murphy's equation · BPSK/OOK
├── ⛨  CREW TELEMETRY       — Crew vitals · TARS/CASE AI · Ship systems · Cryosleep
├── ▤  MISSION REPORTER     — Lazarus archive · Plan A/B progress · Blight model
├── ⚛  QUANTUM SINGULARITY  — LQG · BKL oscillations · Page curve · OTOC · ER=EPR
└── ℹ  SYSTEM STATUS        — Backend health · Dependency check · File diagnostics
```

---

<img width="1340" height="582" alt="image" src="https://github.com/user-attachments/assets/e85c66e1-886a-49ce-a7b5-d66f771308db" />


## ◈ Module I — Gravity Engine

*File:* `gravity_engine.py` · *3,036 lines*

The Gravity Engine models Gargantua as a maximally spinning Kerr black hole with mass parameter `M ≈ 1e8 solar masses` and dimensionless spin `a_star ≈ 1 − 1e−14`. The `KerrBlackHole` dataclass implements the full Boyer-Lindquist metric tensor, all key radii, tidal forces, gravitational wave synthesis, accretion disk emission, and the Penrose process.

### I.1 Kerr Metric Tensor

The covariant metric in Boyer-Lindquist coordinates, defining the spacetime fabric of Gargantua:

```math
g_{\mu\nu} = \begin{pmatrix}
-\!\left(1 - \dfrac{r_s r}{\Sigma}\right)c^2 & 0 & 0 & -\dfrac{r_s r a \sin^2\!\theta}{\Sigma}c \\[6pt]
0 & \dfrac{\Sigma}{\Delta} & 0 & 0 \\[6pt]
0 & 0 & \Sigma & 0 \\[6pt]
-\dfrac{r_s r a \sin^2\!\theta}{\Sigma}c & 0 & 0 &
\left(r^2 + a^2 + \dfrac{r_s r a^2 \sin^2\!\theta}{\Sigma}\right)\sin^2\!\theta
\end{pmatrix}
```

The Kerr auxiliary scalar functions evaluated at every grid cell:

```math
r_s = \frac{2GM}{c^2},\quad
a   = \frac{J}{Mc},\quad
\Sigma(r,\theta) = r^2 + a^2\cos^2\!\theta,\quad
\Delta(r) = r^2 - r_s r + a^2
```

### I.2 Horizon and Ergosphere Radii

Coordinate singularities of the metric define the outer and inner horizons and the ergosurface:

```math
r_{\pm} = \frac{r_s \pm \sqrt{r_s^2 - 4a^2}}{2},\qquad
r_E(\theta) = \frac{r_s + \sqrt{r_s^2 - 4a^2\cos^2\!\theta}}{2}
```

The ergosphere occupies the region `r_+ < r < r_E(θ)`. Inside this shell, no static observer can exist; all matter co-rotates with the hole (frame dragging).

### I.3 ZAMO Frame-Dragging Frequency

The angular velocity of a Zero Angular Momentum Observer — the Lense-Thirring precession frequency:

```math
\omega_{\rm ZAMO}(r,\theta) = -\frac{g_{t\phi}}{g_{\phi\phi}}
= \frac{r_s\, r\, a\, c}{\left(r^2 + a^2\right)\Sigma + r_s r a^2 \sin^2\!\theta}
```

### I.4 Circular Orbit Angular Velocity and ISCO

The orbital angular velocity for a test mass on a stable equatorial circular orbit:

```math
\Omega(r) = \frac{\sqrt{GM}}{r^{3/2} + a\sqrt{GM/c^2}}
```

The innermost stable circular orbit (ISCO) radius, the inner edge of the accretion disk:

```math
r_{\rm ISCO} = \frac{r_s}{2}\left(3 + Z_2 \mp \sqrt{(3 - Z_1)(3 + Z_1 + 2Z_2)}\right)
```

```math
Z_1 = 1 + \left(1 - a_*^2\right)^{1/3}\!\left[\left(1+a_*\right)^{1/3} + \left(1-a_*\right)^{1/3}\right],\quad
Z_2 = \sqrt{3a_*^2 + Z_1^2}
```

For `a_star → 1` (Gargantua), `r_ISCO → r_+ → r_s/2` — the disk extends almost to the horizon, yielding maximum radiative efficiency.

### I.5 Hawking Temperature and Radiative Efficiency

The Hawking temperature at the outer horizon, vanishing as `a_star → 1`:

```math
T_H = \frac{\hbar\,\kappa}{2\pi k_B c}
= \frac{\hbar c}{4\pi k_B}\cdot\frac{r_+ - r_-}{2r_+^2 + a^2}
```

The Novikov-Thorne radiative efficiency, the fraction of rest mass converted to radiation:

```math
\eta = 1 - \frac{E_{\rm ISCO}}{mc^2} = 1 - \sqrt{1 - \frac{2}{3r_{\rm ISCO}/r_s}}
```

For Gargantua's near-extremal spin, `η ≈ 0.42`, more than four times the Schwarzschild value.

### I.6 Penrose Process Maximum Efficiency

Energy extraction from the ergosphere via particle splitting:

```math
\eta_{\rm Penrose}^{\rm max} = 1 - \frac{1}{\sqrt{2}}\sqrt{1 + \sqrt{1 - a_*^2}}
```

### I.7 Geodesic Equation and Christoffel Symbols

Test-particle motion in curved spacetime follows the geodesic equation, which the engine integrates numerically:

```math
\frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu_{\alpha\beta}\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau} = 0
```

```math
\Gamma^\mu_{\alpha\beta} = \frac{1}{2}g^{\mu\rho}
\left(\partial_\alpha g_{\beta\rho} + \partial_\beta g_{\alpha\rho} - \partial_\rho g_{\alpha\beta}\right)
```

### I.8 Gravitational Wave Strain (Quadrupole Formula)

Gravitational wave synthesis in the engine uses the quadrupole approximation. For a binary of chirp mass `M_c` at luminosity distance `d_L`, the peak strain and frequency at merger are:

```math
h_+(t) = \frac{4}{d_L}\left(\frac{GM_c}{c^2}\right)^{5/3}
\left(\frac{\pi f_{\rm GW}(t)}{c}\right)^{2/3}\cos\!\left(2\Phi(t)\right)
```

```math
f_{\rm GW}(t) = \frac{1}{\pi}\left(\frac{GM_c}{c^3}\right)^{-5/8}
\left(\frac{5}{256}\frac{1}{t_c - t}\right)^{3/8}
```

### I.9 Tidal Force Classification

The tidal acceleration across a body of height `h` near a black hole:

```math
a_{\rm tidal} = \frac{2GMh}{r^3}\quad\text{(Newtonian)},\qquad
a_{\rm tidal}^{\rm GR} = \frac{2GM h}{r^3}\cdot\frac{1}{\left(1-r_s/r\right)^{3/2}}
```

---

## ◈ Module II — Relativity Calculator

*File:* `relativity_calculator.py` · *2,801 lines*

This module implements a complete two-tier relativistic engine: `SpecialRelativity` for SR kinematics in flat spacetime, and `GeneralRelativity` for Kerr geodesics and gravitational time dilation. A dedicated `MissionTimeline` class reconstructs the exact Cooper-Murph age divergence from first principles.

### II.1 Lorentz Factor and Four-Velocity

The Lorentz factor and its derived kinematic quantities, implemented as static methods:

```math
\gamma(v) = \frac{1}{\sqrt{1 - v^2/c^2}},\qquad
\beta = \frac{v}{c},\qquad
\phi = \tanh^{-1}\!\left(\frac{v}{c}\right)\quad\text{(rapidity)}
```

The four-velocity of a massive particle with three-velocity `v`:

```math
u^\mu = \gamma\left(c,\, \mathbf{v}\right) = \left(\gamma c,\, \gamma v_x,\, \gamma v_y,\, \gamma v_z\right)
```

### II.2 Relativistic Velocity Addition

The relativistically correct composition of two collinear velocities:

```math
v_{\rm add}(v_1, v_2) = \frac{v_1 + v_2}{1 + v_1 v_2/c^2}
```

For non-collinear case via Lorentz boost matrix on the four-velocity vector, preserving `u_mu u^mu = -c^2`.

### II.3 Spacetime Interval and Four-Momentum

The invariant interval, distinguishing timelike, spacelike, and null separations:

```math
s^2 = -c^2(\Delta t)^2 + (\Delta x)^2 + (\Delta y)^2 + (\Delta z)^2
```

Four-momentum and relativistic energy-momentum invariant:

```math
p^\mu = m_0 u^\mu = \left(\frac{E}{c},\, \mathbf{p}\right),\qquad
E^2 = (pc)^2 + (m_0 c^2)^2
```

### II.4 Gravitational Time Dilation — Full Kerr Form

The proper time accumulation rate for a crew member orbiting at Boyer-Lindquist radius `r` with angular velocity `Omega`, derived from the invariant line element:

```math
\frac{d\tau}{dt} = \sqrt{
- \left( g_{tt} + 2\,g_{t\phi}\frac{\Omega}{c} + g_{\phi\phi}\frac{\Omega^2}{c^2} \right)}
```

Substituting all metric components yields the master tracking equation:

```math
\Delta t' = \Delta t\;\sqrt{1 - \frac{r_s r}{\Sigma}
- \frac{\Sigma\dot{r}^2}{c^2\Delta}
- \frac{\Sigma\dot{\theta}^2}{c^2}
- \frac{\sin^2\!\theta}{c^2}\!\left(r^2 + a^2 + \frac{r_s r a^2\sin^2\!\theta}{\Sigma}\right)\!\left(\frac{d\phi}{dt}\right)^{\!2}
+ \frac{2r_s r a\sin^2\!\theta}{c\,\Sigma}\frac{d\phi}{dt}}
```

### II.5 Miller's World Dilation Factor

On Miller's World, one hour of proper time equals seven Earth years of coordinate time — a total dilation factor:

```math
\gamma_{\rm total} \approx 61{,}320,\qquad
\left.\frac{d\tau}{dt}\right|_{\rm Miller} \approx 1.631\times10^{-5}
```

This requires the orbit to be extremely close to the ISCO of Gargantua, where the combination of gravitational redshift and orbital kinematic blueshift achieves this precise ratio.

### II.6 Twin Paradox — Asymmetric Ageing

The ageing of the stay-at-home twin (Murph) versus the travelling twin (Cooper) for a cruise phase at velocity `v` over coordinate distance `d`, with acceleration legs of magnitude `g_accel`:

```math
\Delta t_{\rm Murph}  = 2\sqrt{\left(\frac{d}{2c}\right)^2 + \frac{d}{g}} + \frac{d}{v_{\rm cruise}},\qquad
\Delta\tau_{\rm Cooper} = \frac{2c}{g}\sinh^{-1}\!\!\left(\frac{g}{c}\sqrt{\frac{d}{2g}}\right) + \frac{d}{\gamma v_{\rm cruise}}
```

### II.7 Relativistic Doppler and Aberration

Longitudinal Doppler factor for source velocity `v` (approaching: `+`, receding: `−`):

```math
f_{\rm obs} = f_0\sqrt{\frac{1 \pm v/c}{1 \mp v/c}},\qquad
f_{\rm transverse} = \frac{f_0}{\gamma}
```

Relativistic aberration of light-ray angle:

```math
\cos\theta_{\rm obs} = \frac{\cos\theta_{\rm emit} + v/c}{1 + (v/c)\cos\theta_{\rm emit}}
```

---

## ◈ Module III — Planet Scanner

*File:* `planet_analyzer.py` · *2,706 lines*

The Planet Scanner evaluates candidate worlds — Miller's World, Mann's Planet, and Edmunds' World — against a multi-index habitability scoring framework. The `Planet` dataclass stores physical parameters; the `HabitabilityAnalyser` computes ESI, atmospheric retention, biosignature probability, and tidal locking timescale.

### III.1 Earth Similarity Index

A weighted geometric mean of four parameter deviations from Earth's reference values:

```math
\mathrm{ESI} = \left[
\left(1 - \left|\frac{R - R_\oplus}{R + R_\oplus}\right|\right)^{w_R}
\cdot
\left(1 - \left|\frac{\rho - \rho_\oplus}{\rho + \rho_\oplus}\right|\right)^{w_\rho}
\cdot
\left(1 - \left|\frac{v_e - v_{e\oplus}}{v_e + v_{e\oplus}}\right|\right)^{w_{v_e}}
\cdot
\left(1 - \left|\frac{T_s - T_{s\oplus}}{T_s + T_{s\oplus}}\right|\right)^{w_{T_s}}
\right]^{1/4}
```

Reference weights: `w_R = 0.57, w_rho = 1.07, w_ve = 0.70, w_Ts = 5.58`.

### III.2 Equilibrium and Surface Temperature

Planetary equilibrium temperature without greenhouse forcing:

```math
T_{\rm eq} = T_\star\left(\frac{R_\star}{2a_{\rm orb}}\right)^{1/2}(1 - A_B)^{1/4}
```

With greenhouse forcing `Delta F_GHG` (W/m²), the effective surface temperature:

```math
T_{\rm eff} = T_{\rm eq}\left(1 + \frac{\Delta F_{\rm GHG}}{4\sigma T_{\rm eq}^4}\right)^{1/4}
```

### III.3 Jeans Escape — Atmospheric Retention

The global particle loss flux across the exobase, governing long-term atmospheric stability:

```math
\Phi_J = \frac{n_c\, v_{\rm th}}{2\sqrt{\pi}}\left(1 + \lambda_c\right)e^{-\lambda_c}
```

```math
v_{\rm th} = \sqrt{\frac{2k_B T_c}{m}},\qquad
\lambda_c = \frac{v_e^2}{v_{\rm th}^2} = \frac{GM_p\,m}{k_B T_c\, r_c}
```

Retention criterion: `lambda_c > 6` ensures negligible escape on geological timescales.

### III.4 Tidal Locking Timescale

The characteristic time for a planet to become rotationally synchronised with its host star:

```math
t_{\rm lock} \approx \frac{0.4406\,\omega_0\,I\,Q\,a^6}{G\,M_\star^2\,k_{2p}\,R_p^5}
```

where `omega_0` is the initial rotation rate, `I` is the planet's moment of inertia, `Q` is the tidal quality factor, and `k_{2p}` is the Love number.

### III.5 Biosignature Score

A probabilistic composite of atmospheric spectroscopic indicators normalised to `[0, 1]`:

```math
\mathcal{B} = \frac{1}{N_{\rm sig}}\sum_{i=1}^{N_{\rm sig}} w_i\,\min\!\left(1,\frac{X_i}{X_{i,\rm threshold}}\right)
```

Active signatures: O₂, O₃, CH₄, N₂O, H₂O, CO₂, dimethyl sulphide, phosphine.

---

## ◈ Module IV — Wormhole Navigator

*File:* `wormhole_navigator.py` · *2,088 lines*

The Wormhole Navigator models the Saturn transit gateway as a spherically symmetric traversable Lorentzian wormhole via the Morris-Thorne metric. The `WormholeGeometry` dataclass supports four shape function families; `ExoticMatterPhysics` computes Casimir energies and quantum inequality bounds; `WormholeTraversalCalculator` evaluates transit times, tidal forces, and survivability criteria.

### IV.1 Morris-Thorne Metric

The general traversable wormhole line element in proper-length gauge:

```math
ds^2 = -e^{2\Phi(r)}c^2\,dt^2
+ \frac{dr^2}{1 - b(r)/r}
+ r^2\!\left(d\theta^2 + \sin^2\!\theta\,d\phi^2\right)
```

Flare-out condition at throat `r_0`, required for traversability:

```math
b'(r_0) < 1,\qquad b(r_0) = r_0,\qquad b(r) < r\quad\forall\, r > r_0
```

### IV.2 Stress-Energy and Exotic Matter

The Einstein equations `G_mu_nu = (8π G / c^4) T_mu_nu` evaluated in the orthonormal frame:

```math
\rho(r)\,c^2 = \frac{c^4}{8\pi G}\cdot\frac{b'(r)}{r^2}
```

```math
\tau_r(r) = \frac{c^4}{8\pi G}\left[\frac{b(r)}{r^3}
- 2\!\left(1-\frac{b(r)}{r}\right)\frac{\Phi'(r)}{r}\right]
```

Null Energy Condition violation (mandatory for traversability):

```math
T_{\mu\nu}k^\mu k^\nu = \rho c^2 - \tau_r
= -\frac{c^4}{8\pi G\, r_0^2}\left(1 - b'(r_0)\right) < 0
```

### IV.3 Casimir Energy as Exotic Matter Source

The Casimir energy density between parallel conducting plates separated by `d`:

```math
\rho_{\rm Cas}(d) = -\frac{\pi^2\hbar c}{240\,d^4},\qquad
E_{\rm Cas} = -\frac{\pi^2\hbar c\,A}{720\,d^3},\qquad
F_{\rm Cas} = -\frac{\pi^2\hbar c\,A}{240\,d^4}
```

### IV.4 Traversal Time and Survivability

The traveller's proper time to cross throat of width `2l_0` at traversal velocity `v_tr`:

```math
\Delta\tau_{\rm traveller} = \int_{-l_0}^{l_0}
\frac{dl}{v_{\rm tr}\,\gamma(v_{\rm tr})\,e^{\Phi}}
```

Tidal safety constraint — tidal acceleration across human body height `h_body ≈ 2` m:

```math
a_{\rm tidal}^{\rm throat} = \frac{c^2\,h_{\rm body}}{2r_0^2}\left|b'(r_0) - \frac{b(r_0)}{r_0}\right|
\leq g_\oplus \approx 9.81\;\text{m/s}^2
```

### IV.5 Quantum Inequality Bound

Ford-Roman constraint on how negative the energy density of the exotic matter source can be, setting a practical floor on the required plate separation:

```math
\left|\rho_{\rm exotic}\right| \leq \frac{3\hbar}{32\pi^2 c\,\tau_{\rm sample}^4}
```

---

## ◈ Module V — Tesseract Decoder

*File:* `tesseract_decoder.py` · *2,176 lines*

The Tesseract Decoder implements the bulk-brane gravity communication channel through which Cooper transmits quantum gravity data to Murphy via watch-hand and bookshelf displacements. The module combines four-dimensional polytope geometry (real 4D rotation matrices and stereographic projection), braneworld gravity theory, and digital signal processing (BPSK, OOK, Hamming error correction, CRC-16 integrity checks).

### V.1 Braneworld Gravity — ADD/RS Potential

At sub-millimetre scales, gravity propagates through the `n` extra compact dimensions. The modified Newtonian potential on our 3-brane:

```math
V(r) = -\frac{G_N M}{r}\left(1 + \sum_{n=1}^{\infty}\alpha_n\,e^{-n r/\lambda}\right)
\;\propto\; -\frac{G_{(4+n)}M}{r^{1+n}}
```

### V.2 Bulk Graviton Propagation — 5D Field Equation

Metric perturbations `h_mu_nu` generated by stress-tensor pulses at `y = 0` (our brane), propagating through the `AdS_5` bulk with coordinate `y`:

```math
\left[\eta^{\alpha\beta}\partial_\alpha\partial_\beta
+ \frac{\partial^2}{\partial y^2} - \frac{4}{y^2}\right]h_{\mu\nu}(x, y)
= -16\pi G_{5D}\left[T_{\mu\nu}(x) - \frac{1}{3}\eta_{\mu\nu}T^\alpha_\alpha(x)\right]\delta(y)
```

### V.3 5D Bulk Green's Function

The tesseract module inverts the bulk equation to decode gravity anomalies by convolving with the 5D boundary Green's function:

```math
\mathcal{G}_{5D}(x,y;\,x',y') = \int\frac{d^4k}{(2\pi)^4}\,
e^{ik\cdot(x-x')}\,\mathcal{R}_k(y,y')
```

### V.4 Shannon Channel Capacity — Murphy's Channel

The information-theoretic bound on the data rate of Cooper's gravity-wave channel to Murphy, modelled as an additive Gaussian noise channel:

```math
C_{\rm Murphy} = \Delta f\,\log_2\!\left(1 + \frac{P_s}{N_0\,\Delta f}\right)
\leq \frac{P_s}{N_0\ln 2}\quad\text{(bits/s)}
```

### V.5 4D Rotation Matrices

The `TesseractGeometry` class generates exact rotation matrices in each of the six planes of four-dimensional space. The `XW`-plane rotation, for example:

```math
R_{XW}(\theta) = \begin{pmatrix}
\cos\theta & 0 & 0 & -\sin\theta \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
\sin\theta & 0 & 0 & \cos\theta
\end{pmatrix}
```

Stereographic projection of 4D vertex `(x, y, z, w)` to 3D (then to 2D for display):

```math
(X', Y', Z') = \frac{d_w}{d_w - w}(x, y, z),\qquad
(X'', Y'') = \frac{d_z}{d_z - Z'}(X', Y')
```

### V.6 Bookshelf Binary Encoding

The bookshelf displacement signal `s(t)` encodes bit `b_i ∈ {0, 1}` as a binary displacement over interval `[i · T_bit, (i+1) · T_bit]`:

```math
s(t) = \sum_{i=0}^{N-1} b_i\cdot A\cdot \mathrm{rect}\!\left(\frac{t - iT_{\rm bit} - T_{\rm bit}/2}{T_{\rm bit}}\right)
```

Hamming(7,4) error correction encodes 4 data bits into 7-bit codewords, detecting and correcting all single-bit errors. The minimum Hamming distance of the code is `d_min = 3`.

---

## ◈ Module VI — Crew Telemetry

*File:* `crew_telemetry.py` · *2,179 lines*

The Crew Telemetry module models the physiological state of each crew member (Cooper, Brand, Romilly, Doyle) under long-duration spaceflight, provides a complete ship-module degradation system with Weibull reliability curves, and implements the TARS and CASE AI robots as `AIRobot` instances with configurable honesty (90%) and humour (75%) parameters, dialogue generation, and articulation panel simulation.

### VI.1 Crew Physiological Model

Vital-sign evolution under microgravity and radiation stress over elapsed mission days `t`:

```math
\mathrm{VO_2max}(t) = \mathrm{VO_2max}^{(0)}\exp\!\left(-k_{\rm decon}\,t\right)
```

```math
\mathrm{BoneDensity}(t) = \mathrm{BD}_0\!\left(1 - r_{\rm loss}\,\min(t, t_{\rm plateau})\right)
```

Radiation cumulative dose `D(t)` with GCR flux `Phi_GCR` and shielding factor `eta_shield`:

```math
D(t) = \int_0^t \Phi_{\rm GCR}(t')\,(1 - \eta_{\rm shield})\,dt'\quad\text{(mSv)}
```

Alert thresholds: `D > 500 mSv` → elevated; `D > 1000 mSv` → critical.

### VI.2 Composite Health Score

A weighted combination of haematological, cardiovascular, pulmonary, and musculoskeletal sub-scores:

```math
\mathcal{H} = \frac{\sum_k w_k\,S_k}{\sum_k w_k},\qquad
S_k \in [0, 1],\quad\sum_k w_k = 1
```

### VI.3 Ship Module Reliability

Weibull failure probability for a module under stress `sigma` over operating time `t`:

```math
P_{\rm fail}(t) = 1 - \exp\!\left[-\left(\frac{t}{\lambda(\sigma)}\right)^\beta\right],\qquad
\lambda(\sigma) = \lambda_0\,\exp\!\left(-k_\sigma\,\sigma\right)
```

Shape parameter `β > 1` models wear-out failure; `β < 1` models infant mortality.

### VI.4 TARS Harmonic Resonance Field Kernel

TARS classifies biometric signals via a physics-informed Harmonic Resonance Field. The generalised wavefunction evolves as:

```math
\Psi(\mathbf{x}, t) = \sum_{n=1}^{N} c_n(t)\exp\!\left[i\left(\mathbf{k}_n\cdot\mathbf{x} - \omega_n t\right)\right]
\cdot\mathcal{K}_{nm}(\theta,\phi)
```

The non-monotonic resonance kernel detecting periodic physiological signatures:

```math
\mathcal{K}_{nm}(\theta,\phi) = \int_0^\infty H_n(\xi)\,
e^{-\xi^2}\cos\!\left(m\xi\cdot\mathrm{sgn}(\theta - \phi)\right)d\xi
```

---

## ◈ Module VII — Mission Reporter

*File:* `mission_reporter.py` · *1,808 lines*

The Mission Reporter maintains the complete Lazarus archive (12 probes), computes Plan A progress against the 42-coefficient gravitational equation, manages the Plan B embryo bank (5,000 profiles), and models the exponential blight spread curve with extinction timeline projection.

### VII.1 Plan A — Gravitational Equation Progress

The equation Murphy must complete has 42 independent coefficients. Current status:

```
TARS data crystal:   30 coefficients resolved
Prof. Brand (hidden): 12 coefficients (Hawking radiation terms — later disclosed)
Murph (final solve):   0 → 42 (post-tesseract)
Progress:             30/42 = 71.4%
```

### VII.2 Plan B — Embryo Bank Diversity

Genetic diversity score of the embryo bank, measured as the average pairwise Jaccard dissimilarity across genome profiles:

```math
\mathcal{D}_{\rm bank} = 1 - \frac{1}{\binom{N}{2}}\sum_{i < j}\frac{|G_i \cap G_j|}{|G_i \cup G_j|}
```

Minimum Viable Population criterion: `N_viable ≥ 160` (Franklin 1980, Lande 1995). With `N = 5000` embryos at 94% viability, `N_viable ≈ 4700 ≫ N_MVP`.

### VII.3 Blight Spread Model

The blight propagates as a reaction-diffusion process across Earth's agricultural zones:

```math
\frac{\partial B}{\partial t} = D\,\nabla^2 B + r\,B\left(1 - \frac{B}{K}\right) - \delta(x,t)\,B
```

Under worst-case `r = 0.18 yr^{-1}` spread rate with declining countermeasure efficacy `delta(t)`, the extinction timeline resolves to `~2095` for total crop failure.

### VII.4 Lazarus Probe Signal Integrity

Signal quality for each probe is scored on a 0–10 scale combining received power budget and data completeness:

```math
Q_{\rm signal} = 10\cdot\frac{P_{\rm rx}}{P_{\rm rx,0}}
\cdot\left(\frac{\lambda_{\rm carrier}}{4\pi d}\right)^2
\cdot G_t\,G_r\cdot\eta_{\rm demod}
```

Active probe inventory: 12 launched, 1 active (Edmunds'), 1 falsified (Mann's), 5 silent, 4 confirmed non-viable.

---

## ◈ Module VIII — Quantum Singularity

*File:* `quantum_singularity.py` · *2,200 lines*

The Quantum Singularity laboratory is the most theoretically advanced module in the platform. It implements eight independent computational engines covering the full frontier of quantum gravity research: Planck foam nucleation, Loop Quantum Gravity area/volume spectra, BKL Kasner oscillations, Hawking evaporation and the Page curve via the island rule, Unruh vacuum thermodynamics, Casimir and Schwinger effects, SYK scrambling and OTOC dynamics, and AdS/CFT holographic entanglement entropy.

### VIII.1 Planck Units and Quantum Foam

The four fundamental Planck scales (CODATA 2018):

```math
\ell_P = \sqrt{\frac{\hbar G}{c^3}} = 1.61626\times10^{-35}\,\text{m},\quad
t_P   = \sqrt{\frac{\hbar G}{c^5}} = 5.39116\times10^{-44}\,\text{s}
```

```math
m_P = \sqrt{\frac{\hbar c}{G}} = 2.17643\times10^{-8}\,\text{kg},\quad
T_P = \sqrt{\frac{\hbar c^5}{Gk_B^2}} = 1.41678\times10^{32}\,\text{K}
```

Virtual black hole nucleation rate in the Wheeler foam background:

```math
\Gamma_{\rm foam} \sim m_P^{-4}\exp\!\left(-S_{\rm BH}\right)
= m_P^{-4}\exp\!\left(-\frac{4\pi M^2}{m_P^2}\right)
```

Spacetime foam genus distribution for a 2-sphere of physical radius `r`:

```math
P(g,r) \sim \exp\!\left(-\frac{4\pi r^2}{\ell_P^2}\,g\right),\qquad
\langle g\rangle \sim \frac{\ell_P^2}{4\pi r^2}
```

Lorentz invariance violation — modified dispersion relation at order `n`:

```math
\omega^2 = k^2c^2\left[1 \pm \xi_n\left(\frac{\hbar\omega}{E_P c^2}\right)^n\right],\qquad
\frac{\delta v_g}{c} \approx \pm\frac{n+1}{2}\,\xi_n\left(\frac{E}{E_P}\right)^n
```

### VIII.2 Loop Quantum Gravity — Area and Volume Spectra

In the Ashtekar-Lewandowski kinematic Hilbert space, the area operator acts on spin-network states with discrete spectrum:

```math
\hat{A}_S\,|\Gamma, j_l, i_n\rangle
= 8\pi\gamma\ell_P^2\sum_{p\,\in\,S\cap\Gamma}
\sqrt{j_p(j_p+1)}\;|\Gamma, j_l, i_n\rangle
```

The Barbero-Immirzi parameter `γ = 0.2375`. The area gap (minimum non-zero eigenvalue, `j_min = 1/2`):

```math
\Delta_A = 4\sqrt{3}\,\pi\,\gamma\,\ell_P^2 \approx 1.0509\times10^{-69}\,\text{m}^2
```

The LQC effective Friedmann equation — the Big Bang singularity replaced by a quantum bounce:

```math
H^2 = \frac{8\pi G}{3}\,\rho\!\left(1 - \frac{\rho}{\rho_{\rm crit}}\right),\qquad
\rho_{\rm crit} = \frac{3}{8\pi\gamma^2\lambda^2\kappa^2} \approx 0.41\,\rho_P
```

The quantum-corrected Raychaudhuri equation (positive pressure term creates repulsion near bounce):

```math
\frac{\ddot{a}}{a} = -\frac{4\pi G}{3}\left(\rho + 3p\right)
\left(1 - \frac{2\rho}{\rho_{\rm crit}}\right)
+ \frac{8\pi G}{3}\frac{\rho^2}{\rho_{\rm crit}}
```

### VIII.3 BKL Kasner Oscillations — Mixmaster Singularity

Near a spacelike singularity, the general Kasner metric and exponent constraints:

```math
ds^2 = -dt^2 + \sum_{i=1}^3 t^{2p_i}(dx^i)^2,\qquad
\sum_i p_i = 1,\quad\sum_i p_i^2 = 1
```

The three Kasner exponents parametrised by the Lifshitz-Khalatnikov variable `u ≥ 1`:

```math
p_1(u) = \frac{-u}{1+u+u^2},\quad
p_2(u) = \frac{1+u}{1+u+u^2},\quad
p_3(u) = \frac{u(1+u)}{1+u+u^2}
```

The BKL map governing epoch transitions as `t → 0`:

```math
u\;\mapsto\;\begin{cases} u - 1, & u > 2 \\[4pt] \dfrac{1}{u-1}, & 1 < u \leq 2 \end{cases}
```

Mean era length from the Gauss-Kuzmin continued-fraction distribution:

```math
u = k + \cfrac{1}{k_1 + \cfrac{1}{k_2 + \cdots}},\qquad
\langle k\rangle = \frac{\pi^2}{6\ln 2} \approx 2.37
```

### VIII.4 Hawking Radiation and Evaporation

Temperature, luminosity, and evaporation time for a Schwarzschild black hole of initial mass `M_0`:

```math
T_H = \frac{\hbar c^3}{8\pi G M k_B},\qquad
\mathcal{L} = \frac{\hbar c^6}{15360\,\pi\,G^2 M^2},\qquad
\frac{dM}{dt} = -\frac{\hbar c^4}{15360\,\pi G^2 M^2}
```

```math
t_{\rm evap} = \frac{5120\,\pi\,G^2 M_0^3}{\hbar c^4},\qquad
M(t) = M_0\!\left(1 - \frac{t}{t_{\rm evap}}\right)^{1/3}
```

The Bekenstein-Hawking entropy and scrambling time:

```math
S_{\rm BH} = \frac{A}{4\ell_P^2} = 4\pi M^2\quad(G=\hbar=c=1),\qquad
t_{\rm scr} = \frac{M}{2\pi}\ln(4\pi M^2)
```

### VIII.5 Page Curve via Island Rule

The radiation entropy is determined by extremising the generalised entropy functional over quantum extremal surfaces (islands):

```math
S_{\rm gen}[\mathcal{I}] = \frac{\mathrm{Area}(\partial\mathcal{I})}{4G}
+ S_{\rm bulk}[R \cup \mathcal{I}]
```

```math
S_{\rm rad}(t) = \min_{\mathcal{I}}\,\mathrm{ext}_{\mathcal{I}}\left[S_{\rm gen}[\mathcal{I}]\right]
= \min\!\left\{S_{\rm Hawking}(t),\;\;S_{\rm BH}^{\rm init} - S_{\rm BH}(t) + S_{\rm bdy}\right\}
```

The Page time `t_Page ≈ t_evap / 2` marks the transition from the no-island to the island saddle, restoring unitarity (entropy decreasing phase).

### VIII.6 Unruh Effect and Schwinger Pair Production

Unruh temperature and Planck spectrum seen by a uniformly accelerating Rindler observer:

```math
T_U = \frac{\hbar a}{2\pi c k_B},\qquad
n(\omega) = \frac{1}{\exp\!\left(\dfrac{2\pi c\,\omega}{a}\right) - 1},\qquad
\mathcal{R}(\omega, a) = \frac{a^2}{4\pi^2 c^2}\cdot\frac{1}{e^{2\pi\omega c/a}-1}
```

Schwinger pair-production rate per unit 4-volume in electric field `E` summed over all Landau levels:

```math
\frac{W}{V} = \frac{\alpha E^2}{\pi^2}
\sum_{n=1}^\infty\frac{(-1)^{n+1}}{n}\exp\!\left(-\frac{n\pi E_c}{E}\right)
\;\approx\;\frac{\alpha E^2}{\pi^2}\exp\!\left(-\frac{\pi E_c}{E}\right),\quad E \ll E_c
```

### VIII.7 OTOC Scrambling and SYK Model

The Maldacena-Shenker-Stanford bound on the quantum Lyapunov exponent:

```math
\lambda_L \leq \frac{2\pi k_B T}{\hbar}\quad\text{(saturated by black holes and SYK)}
```

The out-of-time-order correlator — diagnostic of quantum information scrambling:

```math
F(t) = \langle V^\dagger(t)\,W^\dagger\,V(t)\,W\rangle_\beta,\qquad
F(t) \approx 1 - \frac{\varepsilon}{N}\,e^{\lambda_L t},\quad t < t_{\rm scr}
```

The Sachdev-Ye-Kitaev Hamiltonian for `N` Majorana fermions with random `q`-body couplings:

```math
H_{\rm SYK} = i^{q/2}\!\!\sum_{1\leq i_1 < \cdots < i_q \leq N}
J_{i_1\cdots i_q}\,\chi_{i_1}\cdots\chi_{i_q},\qquad
\langle J_{i_1\cdots i_q}^2\rangle = \frac{(q-1)!\,\mathcal{J}^2}{N^{q-1}}
```

GUE Wigner-Dyson level spacing statistics in the chaotic phase:

```math
P(s) = \frac{32}{\pi^2}\,s^2\exp\!\left(-\frac{4s^2}{\pi}\right),\qquad\langle s\rangle = 1
```

### VIII.8 Holographic Entanglement — Ryu-Takayanagi

Entanglement entropy of boundary region `A` via the RT minimal bulk surface `γ_A`:

```math
S_{\rm EE}(A) = \frac{\mathrm{Area}(\gamma_A)}{4G_N}
```

For a 2D CFT interval `ℓ` at zero temperature and at finite inverse temperature `β`:

```math
S(A)\big|_{T=0} = \frac{c}{3}\ln\frac{\ell}{\varepsilon},\qquad
S(A)\big|_{T>0} = \frac{c}{3}\ln\!\left[\frac{\beta}{\pi\varepsilon}\sinh\!\frac{\pi\ell}{\beta}\right]
```

Holographic mutual information phase transition at critical separation `d_c`:

```math
I(A:B) = \begin{cases}
\dfrac{c}{3}\ln\dfrac{\ell_A\ell_B}{(\ell_A+d+\ell_B)\,d\,\varepsilon^2} & d < d_c \\[6pt]
0 & d \geq d_c
\end{cases}
```

ER=EPR — the thermofield double state shared by two boundary CFTs corresponds to the maximally entangled Einstein-Rosen bridge between two black holes:

```math
|\mathrm{TFD}\rangle = \frac{1}{\sqrt{Z(\beta)}}\sum_n e^{-\beta E_n/2}\,|n\rangle_L\otimes|n\rangle_R,\qquad
Z(\beta) = \mathrm{Tr}\!\left[e^{-\beta H}\right]
```

Holographic complexity (CV conjecture) grows linearly at late times:

```math
\mathcal{C} = \frac{\mathrm{Vol}(\Sigma_{\rm max})}{G_N\,\ell_{\rm AdS}},\qquad
\frac{d\mathcal{C}}{dt}\xrightarrow{t\to\infty}\frac{2M}{\pi} = \frac{2E}{\pi}
```

### VIII.9 Cooper's Singularity Crossing

The interior Kerr geodesic from the outer horizon to the ring singularity, parametrised by the cycloid angle `η`:

```math
r(\eta) = \frac{r_s}{2}(1 + \cos\eta),\qquad
\tau(\eta) = \frac{r_s}{2c}(\eta + \sin\eta),\quad\eta\in[0,\pi]
```

The maximum proper time available inside Gargantua's horizon for information processing:

```math
\tau_{\rm max} = \frac{\pi G M}{c^3} \approx 1.55\,\text{hr}\left(\frac{M}{10^8 M_\odot}\right)
```

The Bekenstein information bound on TARS's quantum data crystal of energy `E` and radius `R`:

```math
I_{\rm max} = \frac{S_{\rm max}}{k_B\ln 2}
\leq \frac{2\pi R E}{\hbar c\ln 2}\quad\text{(Bekenstein 1981)}
```

The Randall-Sundrum bulk graviton transmission amplitude — signal fidelity from Cooper's position at bulk depth `y` to our brane:

```math
|\mathcal{T}(y)|^2 = e^{-2ky},\qquad
\mathcal{F}_{\rm signal}(y) = \exp\!\left(-\frac{2y}{\ell_{\rm AdS}}\right)
```

---

## ◈ Mission Overview Dashboard

The landing page after the boot sequence renders a live mission dashboard with:

- **KPI Strip:** Mission Day, Earth Year (2067), Plan A Progress (71.4%), Wormhole Status (STABLE), Blight Severity (CRITICAL), TARS Status (NOMINAL)
- **Gargantua Schematic:** Matplotlib figure with accretion disk colour gradient (Novikov-Thorne thermal model), Doppler blueshift/redshift asymmetry (left-side brightening from relativistic beaming), photon ring at `r_ph`, ISCO boundary at `r_ISCO`, shadow interior at `r_shadow = 5.196 M`
- **Plan A / Plan B Panel:** Progress bars, coefficient counts, embryo bank viability
- **Planet Candidate ESI Bars:** Miller (0.68), Mann (0.12), Edmunds (0.85)
- **Lazarus Archive Summary:** 12 probes, status breakdown
- **Earth Blight Status:** Per-crop loss percentages (Wheat 85%, Corn 92%, Rice 72%, Okra 45%, Cassava 30%)
- **TARS Log:** Six rotating status messages
- **Module Card Grid:** 8 cards with per-module status indicators
- **Technical Appendix (expandable):** Full closed-form field equation library

---

## ◈ Boot Sequence

On first visit, an animated terminal renders the system initialisation sequence line by line with colour-coded status:

```
INTERSTELLAR SYSTEM CONTROL
Version 3.0.0 — Build 2067.730
NASA Quantum Gravity Observatory — Deep Space Division

Initialising Kerr metric computations...              [CYAN]
Loading Gargantua spacetime fabric...                 [CYAN]
Calibrating gravitational wave detectors...           [CYAN]
Establishing wormhole telemetry link...               [CYAN]
Loading TARS personality matrix... [Humour: 75%]      [GOLD]
Decrypting TARS quantum data crystal...               [GOLD]
Importing Murphy's equation coefficients... 30/42     [ORANGE]
Calculating Miller's World time dilation... 1h = 7yr  [CYAN]
Plan A progress: 71.4%                                [ORANGE]
Quantum Singularity Lab: ONLINE                       [GREEN]

ALL SYSTEMS NOMINAL — 8 BACKENDS ONLINE              [GREEN]
```

The boot cursor (`▌`) blinks on the current line; each line fades in with a `0.07 s` delay.

---

## ◈ Visual Design System

The platform uses a hand-built CSS design system with no external UI library:

| Token | Value | Usage |
|---|---|---|
| `--gold` | `#E8C46A` | Primary accent, titles, KPI values |
| `--blue` | `#4FC3F7` | Relativity, wormhole data, info |
| `--purple` | `#8060ff` | Quantum, wormhole navigator |
| `--green` | `#81C784` | System OK, crew nominal, Edmunds |
| `--orange` | `#FF8800` | Gravity engine, Plan A, warnings |
| `--red` | `#D154FF` | Critical alerts, offline modules |
| `--bg0` | `#020408` | Absolute darkest background |
| `--font-mono` | `Share Tech Mono` | Terminal, data panels, tables |
| `--font-head` | `Rajdhani` | Section headers, titles |
| `--font-body` | `Exo 2` | Body text, descriptions |
| `--glow-gold` | `0 0 12px rgba(232,196,106,0.25)` | Interactive hover glow |

**Ambient elements rendered as fixed CSS layers:**
- `star-field` — 12 radial-gradient point sources simulating stars
- `gargantua-glow` — orange/amber radial gradient, bottom-right
- `wormhole-glow` — violet radial gradient, top-left

**Animations:** `pulse-gold` (2 s ease), `blink` (1 s step), `fadeInUp` (0.3 s), `scanDown` (scan line traverse)

---

## ◈ TARS AI Dialogue System

TARS is implemented as an `AIRobot` dataclass with configurable `honesty_pct = 90` and `humour_pct = 75`. The sidebar includes a context selector with eight dialogue contexts:

| Context | Representative Response |
|---|---|
| `greeting` | All systems nominal. Though I notice you haven't asked about my humour setting yet. |
| `navigation` | Trajectory computed. I've also calculated the probability of everything going wrong. |
| `tidal` | Tidal forces are significant. I recommend we don't discuss my structural limitations. |
| `singularity` | Inside the singularity now. Physics is negotiable here. Logging everything. |
| `humour` | My humour setting is at 75%. Who else is going to lighten the mood falling into a black hole? |
| `honesty` | Honesty at 90%. Full disclosure: that's exactly how much I've told you. |
| `plan_a` | Plan A requires Murphy's equation. Current: 71.4%. Professor Brand was less forthcoming. |
| `default` | That is an interesting perspective. Also: you haven't slept in 18 hours. |

---

## ◈ Installation

```bash
# 1. Clone the repository
git clone https://github.com/Devanik21/INTERSTELLAR.git
cd INTERSTELLAR

# 2. Install dependencies
pip install streamlit numpy pandas matplotlib scipy plotly

# 3. Optional — place a background image
cp your-interstellar-wallpaper.png bg.png

# 4. Launch
streamlit run ENDURANCE.py

# 5. Custom port
streamlit run ENDURANCE.py --server.port 8501
```

All nine files must reside in the same directory. The platform degrades gracefully if any backend is missing — the sidebar marks it offline and the page renders an error card with the import traceback.

---

## ◈ Dependencies

```
streamlit  ≥ 1.30
numpy      ≥ 1.24
pandas     ≥ 2.0
matplotlib ≥ 3.7
scipy      ≥ 1.11
plotly     ≥ 5.18
```

No additional dependencies. All heavy computation uses NumPy/SciPy; all visualisation uses Matplotlib (dark-themed, injected globally) and Plotly.

---

## ◈ File Reference

| File | Role | Lines | Key Classes / Functions |
|---|---|---|---|
| `ENDURANCE.py` | Frontend · Mission Control | 2,579 | `render_overview`, `render_sidebar`, `render_boot_sequence`, `safe_render`, `KerrBlackHole` (via import) |
| `gravity_engine.py` | Kerr BH · GW · Tidal | 3,036 | `KerrBlackHole`, `AccretionDisk`, `GravitationalWaveEngine`, `TidalForceCalculator` |
| `relativity_calculator.py` | SR / GR Engine | 2,801 | `SpecialRelativity`, `GeneralRelativity`, `MissionTimeline`, `TwinParadox` |
| `planet_analyzer.py` | Habitability · ESI | 2,706 | `Planet`, `AtmosphericComposition`, `HabitabilityAnalyser`, `make_miller`, `make_mann`, `make_edmunds` |
| `wormhole_navigator.py` | Morris-Thorne | 2,088 | `WormholeGeometry`, `ExoticMatterPhysics`, `WormholeTraversalCalculator`, `OrbitalMechanics` |
| `tesseract_decoder.py` | 4D · Braneworld · Signals | 2,176 | `TesseractGeometry`, `GravitySignalEncoder`, `GravitySignalDecoder`, `BulkGravityEngine` |
| `crew_telemetry.py` | Crew · TARS · Ship | 2,179 | `CrewMember`, `AIRobot`, `ShipModule`, `build_tars`, `build_case`, `build_crew_registry` |
| `mission_reporter.py` | Lazarus · Plan A/B | 1,808 | `LazarusProbe`, `PlanAStatus`, `PlanBStatus`, `EmbryoBank`, `BlightModel` |
| `quantum_singularity.py` | LQG · BKL · Page curve | 2,200 | `PlanckFoamEngine`, `LQGEngine`, `BKLEngine`, `PageCurveEngine`, `UnruhVacuumEngine`, `SYKEngine`, `HolographyEngine` |

---

## ◈ Scientific References

The mathematical foundations of this platform draw from the following primary literature:

- Boyer, R. H. & Lindquist, R. W. (1967). Maximal analytic extension of the Kerr metric. *J. Math. Phys.*, 8(2), 265–281.
- Kerr, R. P. (1963). Gravitational field of a spinning mass as an example of algebraically special metrics. *Phys. Rev. Lett.*, 11, 237.
- Morris, M. S. & Thorne, K. S. (1988). Wormholes in spacetime and their use for interstellar travel. *Am. J. Phys.*, 56(5), 395–412.
- Thorne, K. S. (1994). *Black Holes and Time Warps: Einstein's Outrageous Legacy.* W. W. Norton.
- Penrose, R. (1969). Gravitational collapse: The role of general relativity. *Riv. Nuovo Cimento*, 1, 252.
- Hawking, S. W. (1975). Particle creation by black holes. *Commun. Math. Phys.*, 43, 199–220.
- Bekenstein, J. D. (1973). Black holes and entropy. *Phys. Rev. D*, 7(8), 2333.
- Novikov, I. D. & Thorne, K. S. (1973). Astrophysics of black holes. In *Black Holes* (DeWitt & DeWitt, eds.).
- Belinskii, V. A., Khalatnikov, I. M. & Lifshitz, E. M. (1970). Oscillatory approach to a singular point. *Adv. Phys.*, 19(80), 525–573.
- Ashtekar, A. & Lewandowski, J. (2004). Background independent quantum gravity. *Class. Quantum Grav.*, 21(15), R53.
- Rovelli, C. & Smolin, L. (1995). Discreteness of area and volume in quantum gravity. *Nucl. Phys. B*, 442(3), 593–619.
- Ryu, S. & Takayanagi, T. (2006). Holographic derivation of entanglement entropy. *Phys. Rev. Lett.*, 96, 181602.
- Maldacena, J. (1997). The large-N limit of superconformal field theories and supergravity. *Int. J. Theor. Phys.*, 38, 1113.
- Maldacena, J. & Susskind, L. (2013). Cool horizons for entangled black holes. *Fortschr. Phys.*, 61(9), 781–811.
- Almheiri, A., Engelhardt, N., Marolf, D. & Maxfield, H. (2019). Entanglement wedge reconstruction. *JHEP*, 2019(12), 63.
- Maldacena, J., Shenker, S. H. & Stanford, D. (2016). A bound on chaos. *JHEP*, 2016(8), 106.
- Sachdev, S. & Ye, J. (1993). Gapless spin-fluid ground state in a random quantum Heisenberg magnet. *Phys. Rev. Lett.*, 70, 3339.
- Kitaev, A. (2015). A simple model of quantum holography. *KITP Seminars*, Feb–May 2015.
- Page, D. N. (1993). Information in black hole radiation. *Phys. Rev. Lett.*, 71, 3743.
- Penington, G. (2020). Entanglement wedge reconstruction and the information paradox. *JHEP*, 2020(9), 2.
- Randall, L. & Sundrum, R. (1999). Large mass hierarchy from a small extra dimension. *Phys. Rev. Lett.*, 83, 3370.
- Arkani-Hamed, N., Dimopoulos, S. & Dvali, G. (1998). The hierarchy problem and new dimensions at a millimetre. *Phys. Lett. B*, 429(3–4), 263–272.
- Schwinger, J. (1951). On gauge invariance and vacuum polarization. *Phys. Rev.*, 82(5), 664.
- Unruh, W. G. (1976). Notes on black-hole evaporation. *Phys. Rev. D*, 14(4), 870.
- Castelvecchi, D. & Witze, A. (2016). Einstein's gravitational waves found at last. *Nature News*, 11 Feb 2016.
- Seager, S. et al. (2013). Biosignature gases in H₂-dominated atmospheres. *Astrophys. J.*, 777(2), 95.
- Hart, M. H. (1979). Habitable zones about main sequence stars. *Icarus*, 37(1), 351–357.
- Nolan, C. (Director) (2014). *Interstellar* [Film]. Syncopy / Warner Bros. *(Narrative inspiration only)*

---

## ◈ About the Author

**Devanik** is a final-year Electronics and Communication Engineering student at the National Institute of Technology Agartala (graduating 2026), Samsung ISWDP Fellow (IISc, 98.58th percentile), and the author of a peer-reviewed astrophysics publication ([arXiv:2412.20091](https://arxiv.org/abs/2412.20091), NAOJ). His GitHub profile ([Devanik21](https://github.com/Devanik21)) hosts 190+ repositories spanning original AI architectures, reinforcement learning systems, signal processing engines, and computational physics platforms.

INTERSTELLAR is one entry in a body of work that treats scientific computing as an act of civilisational ambition — each project a small step toward the long-horizon goal of understanding and ultimately transcending the physical limits that bind humanity to a single, fragile world.

> *"We've always defined ourselves by the ability to overcome the impossible."*
> **— Cooper**

---

## ◈ License

This project is released under the **MIT License**. You are welcome to use, modify, and redistribute the code for any purpose, with attribution. The scientific content implements equations from the public domain of physics literature; the cinematic narrative is a tribute to Christopher Nolan's *Interstellar* (2014) and no claim is made over that intellectual property.

---

<div align="center">

```
─────────────────────────────────────────────────────────────
  INTERSTELLAR · Gargantua Science Platform · v3.0.0
  Author: Devanik · github.com/Devanik21
  NIT Agartala · Samsung ISWDP Fellow · May 2026
─────────────────────────────────────────────────────────────

  "Somewhere, something incredible is waiting to be known."
                                         — Carl Sagan
─────────────────────────────────────────────────────────────
```

</div>

<div align="center">

  **Author: Devanik**
  **May 2026**


![Python](https://img.shields.io/badge/Python-3.10%2B-4FC3F7?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-E8C46A?style=flat-square&logo=streamlit&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Scientific-8060ff?style=flat-square&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-Physics-81C784?style=flat-square&logo=scipy&logoColor=white)
![Lines](https://img.shields.io/badge/Lines%20of%20Code-21%2C573-E8C46A?style=flat-square)
![Modules](https://img.shields.io/badge/Science%20Modules-8-FF8800?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-CE93D8?style=flat-square)

<br>
