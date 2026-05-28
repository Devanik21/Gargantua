"""
INTERSTELLAR.py — INTERSTELLAR Control Frontend | Interstellar Science Platform v3.0.0
═══════════════════════════════════════════════════════════════════════════════
The INTERSTELLAR Control Interface — A complete science platform
built as a serious tribute to Christopher Nolan's Interstellar (2014).

Seven scientific backends, one unified command centre.

"Mankind was born on Earth. It was never meant to die here."
                                         — Cooper, 2067
═══════════════════════════════════════════════════════════════════════════════
"""
import streamlit as st
st.set_page_config(
    page_title="INTERSTELLAR",
    page_icon="♾️",
    layout="wide",
    initial_sidebar_state="expanded",
)

import os
import sys
import math
import time
import base64
import hashlib
import random
import warnings
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# §1  BACKEND IMPORTS — safe import with fallback UI
# ══════════════════════════════════════════════════════════════════════════════
BACKENDS_LOADED: Dict[str, bool] = {}
BACKEND_ERRORS:  Dict[str, str]  = {}

def _safe_import(module_name: str, attr: str = None):
    try:
        mod = __import__(module_name)
        BACKENDS_LOADED[module_name] = True
        return getattr(mod, attr) if attr else mod
    except Exception as e:
        BACKENDS_LOADED[module_name] = False
        BACKEND_ERRORS[module_name]  = str(e)
        return None

# Import all 8 backend page functions
gravity_engine_page      = _safe_import("gravity_engine",      "gravity_engine_page")
relativity_calculator_page=_safe_import("relativity_calculator","relativity_calculator_page")
planet_analyzer_page     = _safe_import("planet_analyzer",     "planet_analyzer_page")
wormhole_navigator_page  = _safe_import("wormhole_navigator",  "wormhole_navigator_page")
tesseract_decoder_page   = _safe_import("tesseract_decoder",   "tesseract_decoder_page")
crew_telemetry_page      = _safe_import("crew_telemetry",      "crew_telemetry_page")
mission_reporter_page    = _safe_import("mission_reporter",    "mission_reporter_page")
quantum_singularity_page = _safe_import("quantum_singularity", "quantum_singularity_page")

# ══════════════════════════════════════════════════════════════════════════════
# §2  CONSTANTS & MISSION DATA
# ══════════════════════════════════════════════════════════════════════════════
MISSION_START_YEAR   = 2067
CURRENT_MISSION_DAY  = 730
EARTH_POPULATION     = "3.5 Billion"
BLIGHT_SEVERITY      = "CRITICAL"
GARGANTUA_DIST_LY    = "10 Billion"
WORMHOLE_STATUS      = "STABLE"
PLAN_A_PCT           = 71.4
PLAN_B_EMBRYOS       = 5_000
TARS_HONESTY         = 90
TARS_HUMOUR          = 75

NAV_PAGES = [
    ("✦",  "MISSION OVERVIEW",    "overview"),
    ("⬡",  "GRAVITY ENGINE",      "gravity"),
    ("⏱",  "RELATIVITY CALC",     "relativity"),
    ("🪐",  "PLANET SCANNER",      "planets"),
    ("⟳",  "WORMHOLE NAVIGATOR",  "wormhole"),
    ("◈",  "TESSERACT DECODER",   "tesseract"),
    ("⛨",  "CREW TELEMETRY",      "crew"),
    ("▤",  "MISSION REPORTER",    "mission"),
    ("⚛",  "QUANTUM SINGULARITY", "quantum"),
    ("ℹ",  "SYSTEM STATUS",       "system"),
]

INTERSTELLAR_QUOTES = [
    ("We used to look up at the sky and wonder at our place in the stars.",
     "Cooper"),
    ("Love is the one thing we're capable of perceiving that transcends dimensions of time and space.",
     "Dr. Brand"),
    ("Do not go gentle into that good night.",
     "Prof. Brand"),
    ("Mankind was born on Earth. It was never meant to die here.",
     "Cooper"),
    ("We've always defined ourselves by the ability to overcome the impossible.",
     "Cooper"),
    ("Newton's third law — the only way humans have ever figured out how to get somewhere is to leave something behind.",
     "Cooper"),
    ("I'm not afraid of death. I'm an old physicist. I'm afraid of time.",
     "Prof. Brand"),
    ("Evolution has yet to transcend that simple barrier: we can care deeply, selflessly, about those we know — but our capacity to harm, to massacre, our capacity for evil — the people who are of no consequence to us — is vast.",
     "Prof. Brand"),
    ("TARS, what's your honesty parameter?  90%.  Ooh. Careful.",
     "Cooper & TARS"),
    ("They say once you grow crops somewhere, you have officially colonised it.",
     "Brand"),
    ("In the future, they won't say he made a choice. They'll say he went through a wormhole.",
     "TARS"),
    ("The truth is we go. Because we're explorers, pioneers — not caretakers.",
     "Cooper"),
    ("Every hour we spend on that planet will be seven years back on Earth.",
     "Brand"),
    ("Gravity is not just a force — it is a message.",
     "Cooper, Tesseract"),
    ("Somewhere, something incredible is waiting to be known.",
     "Carl Sagan"),
]

BOOT_LINES = [
    "INTERSTELLAR SYSTEM CONTROL",
    "Version 3.0.0 — Build 2067.730",
    "NASA Quantum Gravity Observatory — Deep Space Division",
    "",
    "Initialising Kerr metric computations...",
    "Loading Gargantua spacetime fabric...",
    "Calibrating gravitational wave detectors...",
    "Establishing wormhole telemetry link...",
    "Connecting to Lazarus probe archive...",
    "Syncing crew biometric sensors...",
    "Loading TARS personality matrix... [Humour: 75%] [Honesty: 90%]",
    "Decrypting TARS quantum data crystal...",
    "Importing Murphy's equation coefficients... 30/42",
    "Mapping accretion disk emissions...",
    "Calculating Miller's World time dilation... 1h = 7yr",
    "Plan A progress: 71.4%",
    "Plan B embryo bank: 5,000 profiles loaded",
    "Blight spread model: CRITICAL",
    "Loading Planck foam topology engine...",
    "Initialising LQG spin network — area gap: 4√3π γ ℓ_P²",
    "Calibrating BKL Kasner oscillation map...",
    "Quantum Singularity Lab: ONLINE",
    "",
    "ALL SYSTEMS NOMINAL — 8 BACKENDS ONLINE",
    "GARGANTUA SYSTEM ONLINE",
]

# ══════════════════════════════════════════════════════════════════════════════
# §3  MASTER CSS — dark space theme
# ══════════════════════════════════════════════════════════════════════════════
MASTER_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600;700&family=Exo+2:wght@200;300;400;600;700&display=swap');

/* ── CSS Variables ── */
:root {
  --gold:        #E8C46A;
  --gold2:       #C9A84C;
  --gold3:       #A07830;
  --blue:        #4FC3F7;
  --blue2:       #29B6F6;
  --blue3:       #0288D1;
  --purple:      #8060ff;
  --purple2:     #CE93D8;
  --green:       #81C784;
  --green2:      #4CAF50;
  --orange:      #FF8800;
  --red:         #D154FF;
  --bg0:         #020408;
  --bg1:         #04060c;
  --bg2:         #060a14;
  --bg3:         #080c18;
  --bg4:         #0a1020;
  --border:      rgba(232,196,106,0.15);
  --border2:     rgba(232,196,106,0.08);
  --glass:       rgba(4,6,12,0.88);
  --glass2:      rgba(6,10,20,0.92);
  --text:        #c8d0e0;
  --text-dim:    #6a7a9a;
  --text-bright: #e8eef8;
  --font-mono:   'Share Tech Mono', monospace;
  --font-head:   'Rajdhani', sans-serif;
  --font-body:   'Exo 2', sans-serif;
  --glow-gold:   0 0 12px rgba(232,196,106,0.25), 0 0 24px rgba(232,196,106,0.10);
  --glow-blue:   0 0 12px rgba(79,195,247,0.25),  0 0 24px rgba(79,195,247,0.10);
  --glow-purple: 0 0 12px rgba(128,96,255,0.30),  0 0 24px rgba(128,96,255,0.12);
}

/* ── Global reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body {
  color: var(--text) !important;
  font-family: var(--font-body) !important;
}

[data-testid="stAppViewContainer"] > .main {
  background: transparent !important;
}

/* ── Background image support ── */
.bg-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: -1;
  background:
    linear-gradient(180deg,
      rgba(2,4,8,0.96)  0%,
      rgba(4,6,12,0.92) 40%,
      rgba(2,4,8,0.97)  100%);
  pointer-events: none;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg1); }
::-webkit-scrollbar-thumb {
  background: var(--gold3);
  border-radius: 2px;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] {
  background: transparent !important;
  pointer-events: none;
}
[data-testid="collapsedControl"] {
  pointer-events: auto;
}

/* ── Sidebar Toggle / Collapse Buttons ── */
[data-testid="collapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button {
  color: var(--gold) !important;
  background-color: rgba(232, 196, 106, 0.05) !important;
  border: 1px solid rgba(232, 196, 106, 0.20) !important;
  border-radius: 3px !important;
  transition: all 0.2s ease !important;
}
[data-testid="collapsedControl"] button:hover,
[data-testid="stSidebarCollapseButton"] button:hover {
  background-color: rgba(232, 196, 106, 0.15) !important;
  border-color: var(--gold) !important;
  box-shadow: var(--glow-gold) !important;
}
[data-testid="collapsedControl"] button svg,
[data-testid="stSidebarCollapseButton"] button svg {
  fill: var(--gold) !important;
  color: var(--gold) !important;
}

.block-container {
  padding: 0.5rem 1.2rem 2rem 1.2rem !important;
  max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg,
    rgba(2,4,10,0.98) 0%,
    rgba(4,6,14,0.98) 100%) !important;
  border-right: 1px solid rgba(232,196,106,0.12) !important;
  box-shadow: 4px 0 20px rgba(0,0,0,0.5) !important;
}

[data-testid="stSidebar"] > div:first-child {
  padding-top: 0 !important;
}

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg,
    rgba(232,196,106,0.12) 0%,
    rgba(232,196,106,0.06) 100%) !important;
  color: var(--gold) !important;
  border: 1px solid rgba(232,196,106,0.30) !important;
  border-radius: 3px !important;
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.08em !important;
  padding: 0.45rem 0.8rem !important;
  transition: all 0.25s ease !important;
  text-transform: uppercase !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg,
    rgba(232,196,106,0.22) 0%,
    rgba(232,196,106,0.12) 100%) !important;
  border-color: rgba(232,196,106,0.60) !important;
  box-shadow: var(--glow-gold) !important;
  transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg,
    rgba(232,196,106,0.22) 0%,
    rgba(201,168,76,0.15) 100%) !important;
  border-color: rgba(232,196,106,0.50) !important;
}

/* ── Sliders ── */
.stSlider > div > div > div > div {
  background: var(--gold) !important;
}
.stSlider > div > div > div {
  background: rgba(232,196,106,0.15) !important;
}

/* ── Select boxes ── */
.stSelectbox > div > div {
  background: var(--glass2) !important;
  border: 1px solid var(--border) !important;
  color: var(--gold) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.70rem !important;
  border-radius: 3px !important;
}

/* ── Number inputs ── */
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--glass2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-bright) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.70rem !important;
  border-radius: 3px !important;
}
.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: rgba(232,196,106,0.50) !important;
  box-shadow: var(--glow-gold) !important;
  outline: none !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid rgba(232,196,106,0.12) !important;
  gap: 0px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-dim) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.62rem !important;
  letter-spacing: 0.08em !important;
  border-bottom: 2px solid transparent !important;
  padding: 0.5rem 0.9rem !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom: 2px solid var(--gold) !important;
  background: rgba(232,196,106,0.05) !important;
}
.stTabs [data-baseweb="tab"]:hover {
  color: var(--gold) !important;
  background: rgba(232,196,106,0.04) !important;
}
.stTabs [data-baseweb="tab-panel"] {
  padding: 0.8rem 0 0 0 !important;
}

/* ── Dataframes ── */
.stDataFrame, [data-testid="stDataFrame"] {
  border: 1px solid rgba(232,196,106,0.12) !important;
  border-radius: 3px !important;
  background: var(--glass2) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.60rem !important;
}
.stDataFrame table {
  background: transparent !important;
  color: var(--text) !important;
}
.stDataFrame th {
  background: rgba(232,196,106,0.08) !important;
  color: var(--gold) !important;
  font-size: 0.58rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
  border-bottom: 1px solid rgba(232,196,106,0.20) !important;
}
.stDataFrame td {
  border-bottom: 1px solid rgba(232,196,106,0.05) !important;
  color: var(--text) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
  background: rgba(232,196,106,0.04) !important;
  border: 1px solid var(--border2) !important;
  color: var(--gold) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.65rem !important;
  border-radius: 3px !important;
  letter-spacing: 0.06em !important;
}
.streamlit-expanderContent {
  background: var(--glass2) !important;
  border: 1px solid var(--border2) !important;
  border-top: none !important;
}

/* ── Metric widget ── */
[data-testid="stMetric"] {
  background: var(--glass2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 3px !important;
  padding: 0.6rem !important;
}
[data-testid="stMetricLabel"] {
  color: var(--text-dim) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.58rem !important;
  text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
  color: var(--gold) !important;
  font-family: var(--font-mono) !important;
  font-size: 1.1rem !important;
}

/* ── Info / Success / Warning / Error ── */
.stAlert {
  font-family: var(--font-mono) !important;
  font-size: 0.65rem !important;
  border-radius: 3px !important;
  border-left-width: 3px !important;
}
div[data-baseweb="notification"] {
  background: var(--glass2) !important;
}

/* ── Checkboxes / Radio ── */
.stCheckbox label, .stRadio label {
  color: var(--text) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.65rem !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── Images ── */
.stImage { border-radius: 3px !important; }

/* ── Charts ── */
.js-plotly-plot {
  background: var(--bg2) !important;
}

/* ── Custom component classes ── */
.endurance-header {
  font-family: var(--font-head);
  letter-spacing: 0.25em;
  text-transform: uppercase;
  font-weight: 700;
}

.scan-line {
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(232,196,106,0.4) 20%,
    rgba(232,196,106,0.8) 50%,
    rgba(232,196,106,0.4) 80%,
    transparent 100%);
  margin: 0.4rem 0;
}

.data-panel {
  background: var(--glass2);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 0.75rem;
  font-family: var(--font-mono);
  font-size: 0.58rem;
  line-height: 1.85;
  color: var(--text);
}

.status-badge {
  display: inline-block;
  padding: 0.1rem 0.45rem;
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 0.54rem;
  letter-spacing: 0.08em;
  font-weight: 600;
  text-transform: uppercase;
}

.kpi-grid {
  display: grid;
  gap: 0.35rem;
}

.kpi-card {
  background: var(--glass2);
  border: 1px solid var(--border2);
  border-radius: 3px;
  padding: 0.5rem 0.7rem;
  font-family: var(--font-mono);
  text-align: center;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
  border-color: rgba(232,196,106,0.30);
  box-shadow: var(--glow-gold);
}

.kpi-label {
  font-size: 0.50rem;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.2rem;
}

.kpi-value {
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.1;
}

.kpi-sub {
  font-size: 0.48rem;
  color: var(--text-dim);
  margin-top: 0.15rem;
}

.terminal-block {
  background: rgba(2,4,8,0.95);
  border: 1px solid rgba(232,196,106,0.18);
  border-radius: 3px;
  padding: 0.8rem 1rem;
  font-family: var(--font-mono);
  font-size: 0.62rem;
  color: var(--green);
  line-height: 1.7;
  overflow-x: auto;
}

.terminal-line-gold   { color: var(--gold); }
.terminal-line-blue   { color: var(--blue); }
.terminal-line-purple { color: var(--purple2); }
.terminal-line-red    { color: var(--red); }
.terminal-line-dim    { color: var(--text-dim); }

.section-rule {
  height: 1px;
  background: linear-gradient(90deg,
    rgba(232,196,106,0.05) 0%,
    rgba(232,196,106,0.25) 30%,
    rgba(232,196,106,0.25) 70%,
    rgba(232,196,106,0.05) 100%);
  margin: 0.8rem 0;
}

.quote-block {
  border-left: 3px solid rgba(232,196,106,0.35);
  padding: 0.5rem 0.8rem;
  background: rgba(232,196,106,0.03);
  border-radius: 0 3px 3px 0;
  font-family: var(--font-body);
  font-size: 0.72rem;
  font-style: italic;
  color: rgba(232,196,106,0.75);
  margin: 0.5rem 0;
}

.quote-author {
  font-style: normal;
  font-family: var(--font-mono);
  font-size: 0.58rem;
  color: var(--text-dim);
  margin-top: 0.25rem;
}

.backend-unavailable {
  background: rgba(209,84,255,0.06);
  border: 1px solid rgba(209,84,255,0.20);
  border-radius: 3px;
  padding: 1.5rem;
  text-align: center;
  font-family: var(--font-mono);
  color: var(--red);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.45rem 0.8rem;
  border-radius: 3px;
  font-family: var(--font-mono);
  font-size: 0.62rem;
  color: var(--text-dim);
  cursor: pointer;
  transition: all 0.18s;
  border: 1px solid transparent;
  margin-bottom: 0.12rem;
  letter-spacing: 0.06em;
}
.nav-item:hover, .nav-item.active {
  background: rgba(232,196,106,0.08);
  border-color: rgba(232,196,106,0.20);
  color: var(--gold);
}
.nav-item.active {
  border-left: 2px solid var(--gold);
  box-shadow: inset 0 0 8px rgba(232,196,106,0.05);
}

.mission-log-entry {
  font-family: var(--font-mono);
  font-size: 0.57rem;
  color: var(--text-dim);
  padding: 0.12rem 0;
  border-bottom: 1px solid rgba(232,196,106,0.04);
}

.system-ok    { color: var(--green); }
.system-warn  { color: var(--orange); }
.system-crit  { color: var(--red); }
.system-info  { color: var(--blue); }

.progress-bar-outer {
  height: 4px;
  background: rgba(232,196,106,0.10);
  border-radius: 2px;
  overflow: hidden;
}
.progress-bar-inner {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

.module-card {
  background: var(--glass2);
  border: 1px solid var(--border2);
  border-radius: 4px;
  padding: 0.9rem;
  transition: all 0.2s;
  cursor: pointer;
  height: 100%;
}
.module-card:hover {
  border-color: rgba(232,196,106,0.30);
  box-shadow: var(--glow-gold);
  transform: translateY(-2px);
}
.module-card-icon {
  font-size: 1.6rem;
  margin-bottom: 0.4rem;
}
.module-card-title {
  font-family: var(--font-head);
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--gold);
  letter-spacing: 0.10em;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}
.module-card-desc {
  font-family: var(--font-mono);
  font-size: 0.54rem;
  color: var(--text-dim);
  line-height: 1.55;
}
.module-card-status {
  margin-top: 0.5rem;
  font-family: var(--font-mono);
  font-size: 0.50rem;
  letter-spacing: 0.08em;
}

.planet-card {
  background: var(--glass2);
  border-radius: 4px;
  padding: 0.7rem;
  text-align: center;
  font-family: var(--font-mono);
}

.tars-box {
  background: rgba(232,196,106,0.04);
  border: 1px solid rgba(232,196,106,0.18);
  border-radius: 4px;
  padding: 0.7rem 0.9rem;
  font-family: var(--font-mono);
  font-size: 0.62rem;
  color: var(--text-dim);
  font-style: italic;
  line-height: 1.7;
}
.tars-box b { color: var(--gold); font-style: normal; }

.endurance-ring {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px; height: 80px;
  border-radius: 50%;
  border: 2px solid rgba(232,196,106,0.30);
  box-shadow: var(--glow-gold);
  background: radial-gradient(circle,
    rgba(232,196,106,0.08) 0%,
    rgba(4,6,12,0.90) 70%);
  font-family: var(--font-mono);
  font-size: 0.50rem;
  color: var(--gold);
  text-align: center;
  line-height: 1.4;
}

.star-field {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  pointer-events: none;
  z-index: -2;
  background:
    radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1px 1px at 25% 60%, rgba(255,255,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 40% 10%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(1px 1px at 55% 80%, rgba(255,255,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 70% 35%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1px 1px at 85% 70%, rgba(255,255,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 15% 85%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1px 1px at 90% 15%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(2px 2px at 50% 50%, rgba(232,196,106,0.15) 0%, transparent 100%),
    radial-gradient(1px 1px at 30% 40%, rgba(255,255,255,0.2) 0%, transparent 100%),
    radial-gradient(1px 1px at 65% 25%, rgba(255,255,255,0.3) 0%, transparent 100%),
    var(--bg0);
}

/* ── Gargantua glow accent ── */
.gargantua-glow {
  position: fixed;
  bottom: -200px; right: -200px;
  width: 500px; height: 500px;
  border-radius: 50%;
  background: radial-gradient(circle,
    rgba(232,130,30,0.08) 0%,
    rgba(232,80,10,0.04) 40%,
    transparent 70%);
  pointer-events: none;
  z-index: -1;
}

/* ── Wormhole accent ── */
.wormhole-glow {
  position: fixed;
  top: -150px; left: -150px;
  width: 400px; height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle,
    rgba(128,96,255,0.06) 0%,
    rgba(64,32,200,0.03) 50%,
    transparent 70%);
  pointer-events: none;
  z-index: -1;
}

/* ── Animated scan line ── */
@keyframes scanDown {
  0%   { transform: translateY(-100%); opacity: 0; }
  10%  { opacity: 0.6; }
  90%  { opacity: 0.6; }
  100% { transform: translateY(100vh); opacity: 0; }
}

/* ── Pulse animation ── */
@keyframes pulse-gold {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}
.pulse { animation: pulse-gold 2s ease-in-out infinite; }

/* ── Blink cursor ── */
@keyframes blink { 50% { opacity: 0; } }
.cursor { animation: blink 1s step-end infinite; }

/* ── Boot text animation ── */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.boot-line {
  animation: fadeInUp 0.3s ease both;
  font-family: var(--font-mono);
  font-size: 0.62rem;
  line-height: 1.7;
}

/* ── Override streamlit column gaps ── */
[data-testid="column"] { padding: 0 0.25rem !important; }

/* ── Sidebar label ── */
[data-testid="stSidebar"] label {
  color: var(--text-dim) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.60rem !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
}

/* ── Make matplotlib figures seamless ── */
.stImage img { max-width: 100%; border-radius: 3px; }
[data-testid="stImage"] { border-radius: 3px; }
/* ── GLOBAL 15% TRANSPARENCY OVERRIDE ── */
    :root {
      --glass: rgba(6, 10, 20, 0.15) !important;
      --glass2: rgba(6, 10, 20, 0.15) !important;
      --bg2: rgba(6, 10, 20, 0.15) !important;
    }
    .terminal-block, .tars-box, .js-plotly-plot {
      background: rgba(6, 10, 20, 0.15) !important;
    }
    div[style*="background:rgba(4,6,12,0.90)"],
    div[style*="background:rgba(6,10,20,0.80)"],
    div[style*="background:rgba(4,6,12,0.80)"],
    div[style*="background:rgba(6,10,20,0.90)"],
    div[style*="background:rgba(6,10,20,.85)"],
    div[style*="background:rgba(2,4,8,0.96)"] {
      background: rgba(6, 10, 20, 0.15) !important;
    }

    /* ── STRIP NATIVE STREAMLIT WRAPPER BACKGROUNDS ── */
    [data-testid="stVerticalBlock"],
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stHorizontalBlock"],
    [data-testid="stElementContainer"],
    [data-testid="stMarkdownContainer"] {
        background: transparent !important;
        background-color: transparent !important;
    }
</style>

<!-- Ambient background elements -->
<div class="star-field"></div>
<div class="gargantua-glow"></div>
<div class="wormhole-glow"></div>
"""

# ══════════════════════════════════════════════════════════════════════════════
# §4  SESSION STATE INITIALISATION
# ══════════════════════════════════════════════════════════════════════════════
def init_global_state():
    defaults = {
        "page":            "overview",
        "boot_done":       False,
        "mission_day":     CURRENT_MISSION_DAY,
        "quote_idx":       random.randint(0, len(INTERSTELLAR_QUOTES)-1),
        "tars_dialogue":   "Systems nominal. All backends loaded. Ready for your command.",
        "last_page_time":  time.time(),
        "bg_image_b64":    None,
        "show_bg":         True,
        "theme_accent":    "gold",
        "system_checks":   {},
        "mission_alerts":  [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# §5  BACKGROUND IMAGE LOADER
# ══════════════════════════════════════════════════════════════════════════════
def load_background(path: str = "bg.png") -> Optional[str]:
    """Load background image and return base64 string."""
    for fname in [path, "bg.jpg", "background.png", "background.jpg",
                  "interstellar.png", "interstellar.jpg"]:
        if os.path.exists(fname):
            with open(fname, "rb") as f:
                ext = fname.split(".")[-1]
                mime = "image/jpeg" if ext in ("jpg","jpeg") else "image/png"
                return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
    return None

def inject_background(b64_str: Optional[str]):
    if not b64_str:
        return
    st.markdown(f"""
    <style>
    /* 1. Bind the background to the absolute root element with NO opacity overlay (full brightness) */
    html, body, .stApp {{
        background: url('{b64_str}') !important;
        background-size: cover !important;
        background-position: center 30% !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    
    /* 2. Make the main layout, sidebar container, and element blocks completely transparent */
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child,
    .block-container,
    [data-testid="column"] {{
        background: transparent !important;
        background-color: transparent !important;
    }}
    
    /* 3. Keep a clean aesthetic separation with a glass border on the sidebar */
    [data-testid="stSidebar"] {{
        border-right: 1px solid rgba(232, 196, 106, 0.15) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5) !important;
    }}

    /* 4. Kill the old pseudo-element to keep execution clean */
    .star-field::before {{
        display: none !important;
    }}
    </style>""", unsafe_allow_html=True)


  
# ══════════════════════════════════════════════════════════════════════════════
# §6  UTILITY COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════
def page_header(title: str, subtitle: str = "", accent: str = "#E8C46A",
                icon: str = "◈"):
    st.markdown(f"""
    <div style="margin-bottom:1.2rem;padding-bottom:0.6rem;
                border-bottom:1px solid rgba(232,196,106,0.12);">
      <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.2rem;">
        <span style="color:{accent};font-size:1.1rem;">{icon}</span>
        <span style="font-family:'Rajdhani',sans-serif;font-size:1.15rem;
                     font-weight:700;letter-spacing:0.18em;color:{accent};
                     text-transform:uppercase;">{title}</span>
      </div>
      {"" if not subtitle else f'<div style="font-family:monospace;font-size:0.60rem;color:#5a6a90;padding-left:1.7rem;">{subtitle}</div>'}
    </div>""", unsafe_allow_html=True)


def kpi_row(kpis: List[Tuple[str, str, str, str]]):
    """kpis: list of (label, value, color, sub)"""
    cols = st.columns(len(kpis))
    for col, (lbl, val, clr, sub) in zip(cols, kpis):
        col.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{lbl}</div>
          <div class="kpi-value" style="color:{clr};">{val}</div>
          {"" if not sub else f'<div class="kpi-sub">{sub}</div>'}
        </div>""", unsafe_allow_html=True)


def scan_line():
    st.markdown('<div class="scan-line"></div>', unsafe_allow_html=True)


def section_rule():
    st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)


def quote_banner(quote: str, author: str):
    st.markdown(f"""
    <div class="quote-block">
      "{quote}"
      <div class="quote-author">— {author}</div>
    </div>""", unsafe_allow_html=True)


def tars_says(text: str):
    st.markdown(f"""
    <div class="tars-box">
      <b>TARS:</b> {text}
    </div>""", unsafe_allow_html=True)


def status_badge(label: str, color: str = "#81C784") -> str:
    return (f'<span class="status-badge" '
            f'style="background:rgba({_hex_to_rgb(color)},0.12);'
            f'color:{color};border:1px solid rgba({_hex_to_rgb(color)},0.30);">'
            f'{label}</span>')


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"{r},{g},{b}"


def terminal_block(lines: List[Tuple[str, str]]):
    """lines: list of (text, css_class)"""
    inner = "\n".join(
        f'<div class="boot-line {cls}" '
        f'style="animation-delay:{i*0.04}s">{txt}</div>'
        for i, (txt, cls) in enumerate(lines)
    )
    st.markdown(f'<div class="terminal-block">{inner}</div>',
                unsafe_allow_html=True)


def backend_error_card(name: str, error: str):
    st.markdown(f"""
    <div class="backend-unavailable">
      <div style="font-size:1.5rem;margin-bottom:0.5rem;">⚠</div>
      <div style="font-size:0.75rem;font-weight:600;margin-bottom:0.3rem;">
        MODULE OFFLINE: {name.upper()}
      </div>
      <div style="font-size:0.58rem;color:rgba(209,84,255,0.6);
                  max-width:500px;margin:0 auto;">
        {error[:200]}
      </div>
      <div style="margin-top:0.5rem;font-size:0.55rem;color:#666;">
        Ensure {name}.py is in the same directory as ENDURANCE.py
      </div>
    </div>""", unsafe_allow_html=True)


def progress_bar(value: float, color: str = "#E8C46A", label: str = ""):
    pct = int(value * 100)
    st.markdown(f"""
    <div style="margin:.15rem 0;">
      {"" if not label else f'<div style="font-family:monospace;font-size:0.55rem;color:#6a7a9a;margin-bottom:0.1rem;">{label}</div>'}
      <div class="progress-bar-outer">
        <div class="progress-bar-inner"
             style="width:{pct}%;background:{color};"></div>
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §7  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    S = st.session_state
    with st.sidebar:
        # ── Logo / title ──────────────────────────────────────────────────
        st.markdown("""
        <div style="padding:1.2rem 0.5rem 0.8rem;
                    border-bottom:1px solid rgba(232,196,106,0.12);
                    margin-bottom:0.8rem;">
          <div style="font-family:'Rajdhani',sans-serif;
                      font-size:1.5rem;font-weight:700;
                      letter-spacing:0.30em;color:#E8C46A;
                      text-align:center;text-transform:uppercase;
                      text-shadow:0 0 20px rgba(232,196,106,0.30);">
            INTERSTELLAR
          </div>
          <div style="font-family:monospace;font-size:0.52rem;
                      color:#4a5a7a;text-align:center;
                      letter-spacing:0.15em;margin-top:0.2rem;">
            v3.0.0
          </div>
          <div style="height:1px;background:linear-gradient(90deg,
              transparent,rgba(232,196,106,0.30),transparent);
              margin-top:0.7rem;"></div>
        </div>""", unsafe_allow_html=True)

        # ── Mission status strip ──────────────────────────────────────────
        st.markdown(f"""
        <div style="font-family:monospace;font-size:0.55rem;
                    background:rgba(4,6,12,0.90);
                    border:1px solid rgba(232,196,106,0.10);
                    border-radius:3px;padding:0.5rem 0.6rem;
                    margin-bottom:0.8rem;line-height:2.0;">
          <span style="color:#5a6a80;">MISSION DAY</span>
          <span style="color:#E8C46A;float:right;">{S['mission_day']}</span><br>
          <span style="color:#5a6a80;">EARTH YEAR</span>
          <span style="color:#E8C46A;float:right;">{MISSION_START_YEAR}</span><br>
          <span style="color:#5a6a80;">PHASE</span>
          <span style="color:#4FC3F7;float:right;">GARGANTUA</span><br>
          <span style="color:#5a6a80;">WORMHOLE</span>
          <span style="color:#81C784;float:right;">STABLE</span><br>
          <span style="color:#5a6a80;">PLAN A</span>
          <span style="color:#FF8800;float:right;">{PLAN_A_PCT:.1f}%</span>
        </div>""", unsafe_allow_html=True)

        # ── Navigation ────────────────────────────────────────────────────
        st.markdown("""
        <div style="font-family:monospace;font-size:0.52rem;
                    color:#3a4a60;letter-spacing:0.12em;
                    text-transform:uppercase;
                    margin-bottom:0.4rem;padding-left:0.2rem;">
          ── MODULES ──
        </div>""", unsafe_allow_html=True)

        page_colors = {
            "overview":   "#E8C46A",
            "gravity":    "#FF8800",
            "relativity": "#4FC3F7",
            "planets":    "#81C784",
            "wormhole":   "#8060ff",
            "tesseract":  "#c040ff",
            "crew":       "#81C784",
            "mission":    "#FFD700",
            "system":     "#4FC3F7",
        }
        backend_map = {
            "gravity":    "gravity_engine",
            "relativity": "relativity_calculator",
            "planets":    "planet_analyzer",
            "wormhole":   "wormhole_navigator",
            "tesseract":  "tesseract_decoder",
            "crew":       "crew_telemetry",
            "mission":    "mission_reporter",
        }

        for icon, label, page_key in NAV_PAGES:
            is_active  = S["page"] == page_key
            clr        = page_colors.get(page_key, "#E8C46A")
            bmod       = backend_map.get(page_key)
            loaded_ok  = BACKENDS_LOADED.get(bmod, True)
            status_dot = "" if loaded_ok else "○"
            btn_style = (
                f"border-left:2px solid {clr};"
                f"background:rgba({_hex_to_rgb(clr)},0.08);"
                f"color:{clr};"
            ) if is_active else ""

            lbl = f"{icon}  {label}"
            if status_dot:
                lbl += f"  {status_dot}"

            if st.button(
                lbl,
                key=f"nav_{page_key}",
                width='stretch',
            ):
                S["page"] = page_key
                st.rerun()

        section_rule()

        # ── Quick controls ────────────────────────────────────────────────
        st.markdown("""
        <div style="font-family:monospace;font-size:0.52rem;
                    color:#3a4a60;letter-spacing:0.12em;
                    text-transform:uppercase;margin-bottom:0.4rem;">
          ── QUICK CONTROLS ──
        </div>""", unsafe_allow_html=True)

        S["mission_day"] = st.slider(
            "Mission day", 0, 3000, int(S["mission_day"]), 1,
            help="Advance mission timeline")

        S["show_bg"] = st.checkbox("Background image", value=bool(S["show_bg"]))

        # ── TARS quick dialogue ───────────────────────────────────────────
        section_rule()
        tars_contexts = ["greeting","navigation","tidal","singularity",
                         "humour","honesty","plan_a","default"]
        ctx = st.selectbox("TARS context", tars_contexts, label_visibility="collapsed")

        TARS_BANK = {
            "greeting":    "Good morning. All systems nominal. Though I notice you haven't asked about my humour setting yet.",
            "navigation":  "Trajectory computed. I've also calculated the probability of everything going wrong. Should I share that?",
            "tidal":       "Tidal forces are significant. I recommend we don't discuss my structural limitations right now.",
            "singularity": "Inside the singularity now. Physics is negotiable here. Logging everything.",
            "humour":      f"My humour setting is at {TARS_HUMOUR}%. Who else is going to lighten the mood when we're falling into a black hole?",
            "honesty":     f"Honesty at {TARS_HONESTY}%. Full disclosure: that's exactly how much I've told you.",
            "plan_a":      f"Plan A requires Murphy's equation. Current: {PLAN_A_PCT:.1f}%. Professor Brand was less forthcoming than expected.",
            "default":     "That is an interesting perspective. Also: you haven't slept in 18 hours.",
        }
        if st.button("◈ ASK TARS", width='stretch'):
            S["tars_dialogue"] = TARS_BANK.get(ctx, TARS_BANK["default"])

        if S.get("tars_dialogue"):
            st.markdown(f"""
            <div style="font-family:monospace;font-size:0.57rem;
                        background:rgba(232,196,106,0.04);
                        border:1px solid rgba(232,196,106,0.12);
                        border-radius:3px;padding:0.5rem 0.6rem;
                        color:#c0c0a0;font-style:italic;
                        line-height:1.7;margin-top:0.3rem;">
              <span style="color:#E8C46A;font-style:normal;">TARS: </span>
              {S['tars_dialogue']}
            </div>""", unsafe_allow_html=True)

        # ── Quote at bottom ───────────────────────────────────────────────
        section_rule()
        q_txt, q_auth = INTERSTELLAR_QUOTES[S["quote_idx"] % len(INTERSTELLAR_QUOTES)]
        st.markdown(f"""
        <div style="font-family:monospace;font-size:0.52rem;
                    color:#3a4a60;font-style:italic;
                    line-height:1.6;padding:0 0.2rem;">
          "{q_txt[:80]}{'...' if len(q_txt)>80 else ''}"
          <div style="color:#2a3a50;margin-top:0.15rem;">— {q_auth}</div>
        </div>""", unsafe_allow_html=True)

        if st.button("↻ New quote", width='stretch'):
            S["quote_idx"] = (S["quote_idx"] + 1) % len(INTERSTELLAR_QUOTES)
            st.rerun()

        st.markdown("""
        <div style="font-family:monospace;font-size:0.48rem;
                    color:#2a3050;text-align:center;
                    margin-top:0.8rem;padding-top:0.4rem;
                    border-top:1px solid rgba(232,196,106,0.06);">
          INTERSTELLAR<br>
          Gargantua Science Platform<br>
          Tribute to Christopher Nolan
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §8  BOOT SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════
def render_boot_sequence():
    S = st.session_state
    if S.get("boot_done"):
        return

    st.markdown(MASTER_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div style="min-height:100vh;display:flex;flex-direction:column;
                align-items:center;justify-content:center;
                background:var(--bg0);">
    </div>""", unsafe_allow_html=True)

    # Center boot content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # INTERSTELLAR logo
        st.markdown("""
        <div style="text-align:center;margin-bottom:2.5rem;">
          <div style="font-family:'Rajdhani',sans-serif;
                      font-size:3.5rem;font-weight:700;
                      letter-spacing:0.5em;
                      color:#E8C46A;
                      text-shadow:0 0 40px rgba(232,196,106,0.50),
                                  0 0 80px rgba(232,196,106,0.20);
                      text-transform:uppercase;
                      margin-bottom:0.3rem;">
            INTERSTELLAR
          </div>
          <div style="font-family:monospace;font-size:0.68rem;
                      color:#4a5a7a;letter-spacing:0.30em;
                      text-transform:uppercase;">
            GARGANTUA SYSTEM CONTROL  ·  v3.0.0
          </div>
          <div style="height:1px;background:linear-gradient(90deg,
              transparent,rgba(232,196,106,0.50),transparent);
              margin:1rem 0;"></div>
          <div style="font-family:monospace;font-size:0.58rem;
                      color:#3a4a60;letter-spacing:0.15em;">
            NASA QUANTUM GRAVITY OBSERVATORY  ·  DEEP SPACE DIVISION
          </div>
        </div>""", unsafe_allow_html=True)

        # Boot terminal
        boot_placeholder = st.empty()
        boot_lines_display = []
        for i, line in enumerate(BOOT_LINES):
            boot_lines_display.append(line)
            display = boot_lines_display[-18:]
            html_lines = ""
            for j, bl in enumerate(display):
                if not bl:
                    html_lines += "<br>"
                    continue
                if "NOMINAL" in bl or "ONLINE" in bl:
                    clr = "#81C784"
                elif "ERROR" in bl or "FAILED" in bl:
                    clr = "#D154FF"
                elif "Loading" in bl or "Initialising" in bl or "Calibrating" in bl:
                    clr = "#4FC3F7"
                elif "TARS" in bl or "CASE" in bl:
                    clr = "#E8C46A"
                elif "Plan" in bl or "Murphy" in bl:
                    clr = "#FF8800"
                elif bl.startswith("INTERSTELLAR") or bl.startswith("GARGANTUA") or bl.startswith("Version"):
                    clr = "#E8C46A"
                else:
                    clr = "#81C784"
                html_lines += (
                    f'<div style="font-family:monospace;font-size:0.62rem;'
                    f'color:{clr};line-height:1.65;'
                    f'animation:fadeInUp 0.2s ease both;">'
                    f'{bl}<span class="cursor" '
                    f'style="{"display:inline" if j==len(display)-1 else "display:none"}">▌</span>'
                    f'</div>')
            boot_placeholder.markdown(
                f'<div style="background:rgba(2,4,8,0.96);'
                f'border:1px solid rgba(232,196,106,0.18);'
                f'border-radius:4px;padding:1.2rem 1.4rem;'
                f'min-height:14rem;">{html_lines}</div>',
                unsafe_allow_html=True)
            time.sleep(0.07 if i > 4 else 0.05)

        time.sleep(0.5)

        # Launch button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("◉  ENTER INTERSTELLAR", width='stretch', type="primary"):
            S["boot_done"] = True
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# §9  OVERVIEW PAGE — Mission dashboard
# ══════════════════════════════════════════════════════════════════════════════
def render_overview():
    S = st.session_state

    page_header(
        "MISSION OVERVIEW",
        f"INTERSTELLAR · Day {S['mission_day']} · Gargantua System · "
        f"Earth Year {MISSION_START_YEAR}",
        accent="#E8C46A", icon="✦"
    )

    # ── Top KPI strip ──────────────────────────────────────────────────────
    kpi_row([
        ("Mission Day",      str(S["mission_day"]),     "#E8C46A", "since Earth departure"),
        ("Earth Year",       str(MISSION_START_YEAR),   "#4FC3F7", "coordinate time"),
        ("Plan A Progress",  f"{PLAN_A_PCT:.1f}%",      "#FF8800", "Murphy's equation"),
        ("Wormhole",         WORMHOLE_STATUS,            "#81C784", "Saturn vicinity"),
        ("Blight Severity",  BLIGHT_SEVERITY,            "#D154FF", "global food supply"),
        ("TARS Status",      "NOMINAL",                  "#81C784", "all systems green"),
    ])

    scan_line()

    # ── Main grid: 3 columns ───────────────────────────────────────────────
    col_left, col_mid, col_right = st.columns([1.2, 2, 1.2])

    with col_left:
        # Mission status panel
        st.markdown("""
        <div style="font-family:monospace;font-size:0.58rem;
                    color:#3a4a60;letter-spacing:0.12em;
                    text-transform:uppercase;margin-bottom:0.5rem;">
          ── MISSION STATUS ──
        </div>""", unsafe_allow_html=True)

        mission_items = [
            ("Phase",         "Gargantua Orbit",        "#4FC3F7"),
            ("Active Crew",   "4 (Cooper, Brand, Romilly, Doyle)", "#81C784"),
            ("TARS",          "Operational — Mode: NAV", "#E8C46A"),
            ("CASE",          "Operational — Mode: SCI", "#E8C46A"),
            ("Hull Integrity","98.7%",                   "#81C784"),
            ("Fuel Remaining","67.3% — 201,900 kg",     "#FF8800"),
            ("Δv Remaining",  "4.2 km/s",               "#FF8800"),
            ("Life Support",  "O₂: 380kg · H₂O: 1,640L","#81C784"),
            ("Power",         "38.2 kW (surplus: 6.8)", "#81C784"),
            ("Comms Lag",     "79 min one-way",          "#CE93D8"),
        ]

        for lbl, val, clr in mission_items:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;'
                f'font-family:monospace;font-size:0.57rem;'
                f'border-bottom:1px solid rgba(232,196,106,0.04);'
                f'padding:0.18rem 0;">'
                f'<span style="color:#5a6a80;">{lbl}</span>'
                f'<span style="color:{clr};">{val}</span></div>',
                unsafe_allow_html=True)

        section_rule()

        # Planet candidates
        st.markdown("""
        <div style="font-family:monospace;font-size:0.58rem;
                    color:#3a4a60;letter-spacing:0.12em;
                    text-transform:uppercase;margin-bottom:0.5rem;">
          ── PLANET CANDIDATES ──
        </div>""", unsafe_allow_html=True)

        planets_data = [
            ("Miller's World", "🌊", 0.68, "#4FC3F7",  "SURVEYED"),
            ("Mann's Planet",  "🧊", 0.12, "#CE93D8",  "FALSIFIED"),
            ("Edmunds' World", "🌿", 0.85, "#81C784",  "CONFIRMED ✓"),
        ]
        for name, emoji, esi, clr, status in planets_data:
            st.markdown(f"""
            <div style="background:rgba(6,10,20,0.80);
                        border:1px solid rgba(232,196,106,0.08);
                        border-left:2px solid {clr};
                        border-radius:3px;padding:0.4rem 0.6rem;
                        margin-bottom:0.25rem;font-family:monospace;">
              <div style="display:flex;justify-content:space-between;
                          font-size:0.60rem;">
                <span style="color:{clr};">{emoji} {name}</span>
                <span style="color:#5a6a80;">{status}</span>
              </div>
              <div style="margin-top:0.25rem;">
                <div class="progress-bar-outer">
                  <div class="progress-bar-inner"
                       style="width:{int(esi*100)}%;background:{clr};"></div>
                </div>
                <span style="font-size:0.50rem;color:#5a6a80;">
                  ESI: {esi:.2f}
                </span>
              </div>
            </div>""", unsafe_allow_html=True)

    with col_mid:
        # Central Gargantua visualisation
        _render_gargantua_overview()
        section_rule()
        # Plan A / B progress
        _render_plan_progress()

    with col_right:
        # Lazarus summary
        st.markdown("""
        <div style="font-family:monospace;font-size:0.58rem;
                    color:#3a4a60;letter-spacing:0.12em;
                    text-transform:uppercase;margin-bottom:0.5rem;">
          ── LAZARUS ARCHIVE ──
        </div>""", unsafe_allow_html=True)

        lazarus_summary = [
            ("Probes launched",   "12", "#E8C46A"),
            ("Active signals",    "1",  "#81C784"),
            ("Confirmed OK",      "1",  "#E8C46A"),
            ("Confirmed bad",     "4",  "#D154FF"),
            ("Data falsified",    "1",  "#CE93D8"),
            ("Silent",            "5",  "#555"),
            ("Unknown",           "1",  "#4FC3F7"),
        ]
        for lbl, val, clr in lazarus_summary:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;'
                f'font-family:monospace;font-size:0.57rem;'
                f'border-bottom:1px solid rgba(232,196,106,0.04);'
                f'padding:0.18rem 0;">'
                f'<span style="color:#5a6a80;">{lbl}</span>'
                f'<span style="color:{clr};font-weight:600;">{val}</span></div>',
                unsafe_allow_html=True)

        section_rule()

        # Blight status
        st.markdown("""
        <div style="font-family:monospace;font-size:0.58rem;
                    color:#3a4a60;letter-spacing:0.12em;
                    text-transform:uppercase;margin-bottom:0.5rem;">
          ── EARTH BLIGHT STATUS ──
        </div>""", unsafe_allow_html=True)

        crops_status = [
            ("Wheat",   0.85, "#D154FF"),
            ("Corn",    0.92, "#D154FF"),
            ("Rice",    0.72, "#FF8800"),
            ("Soy",     0.66, "#FF8800"),
            ("Okra",    0.45, "#FFB74D"),
            ("Potato",  0.40, "#FFB74D"),
            ("Cassava", 0.30, "#E8C46A"),
        ]
        for crop, severity, clr in crops_status:
            pct_str = f"{severity*100:.0f}%"
            st.markdown(
                f'<div style="font-family:monospace;font-size:0.54rem;'
                f'margin-bottom:0.2rem;">'
                f'<div style="display:flex;justify-content:space-between;'
                f'color:#5a6a80;margin-bottom:0.07rem;">'
                f'<span>{crop}</span><span style="color:{clr};">{pct_str} lost</span></div>'
                f'<div class="progress-bar-outer">'
                f'<div class="progress-bar-inner" '
                f'style="width:{int(severity*100)}%;background:{clr};"></div>'
                f'</div></div>',
                unsafe_allow_html=True)

        section_rule()

        # TARS dialogue
        st.markdown("""
        <div style="font-family:monospace;font-size:0.58rem;
                    color:#3a4a60;letter-spacing:0.12em;
                    text-transform:uppercase;margin-bottom:0.4rem;">
          ── TARS LOG ──
        </div>""", unsafe_allow_html=True)

        tars_log = [
            "All systems nominal.",
            "Gargantua proximity: SAFE at current orbit.",
            f"Plan A: {PLAN_A_PCT:.1f}% — 30/42 coefficients.",
            "Miller data crystal verified. SHA-256 match.",
            "Wormhole mouth remains stable near Saturn.",
            "Cooper's watch signal decoded — coordinates confirmed.",
        ]
        for entry in tars_log:
            st.markdown(
                f'<div class="mission-log-entry" style="color:#5a6a80;">'
                f'<span style="color:#E8C46A;">TARS ▸ </span>{entry}</div>',
                unsafe_allow_html=True)

    section_rule()

    # ── Module cards grid ──────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif;
                font-size:0.78rem;font-weight:600;
                letter-spacing:0.18em;color:#E8C46A;
                text-transform:uppercase;margin-bottom:0.8rem;">
      ◈ SCIENCE MODULES — Click sidebar to navigate
    </div>""", unsafe_allow_html=True)

    modules_info = [
        ("gravity",    "⬡", "GRAVITY ENGINE",
         "Kerr BH · Accretion disk · GW synthesis · Tidal forces · Hawking radiation",
         "#FF8800", "gravity_engine"),
        ("relativity", "◷", "RELATIVITY CALC",
         "SR/GR · Time dilation · Cooper-Murph divergence · Geodesics · Twin paradox",
         "#4FC3F7", "relativity_calculator"),
        ("planets",    "◓", "PLANET SCANNER",
         "ESI · HZ analysis · Atmosphere · Biosignatures · Miller/Mann/Edmunds",
         "#81C784", "planet_analyzer"),
        ("wormhole",   "⟳", "WORMHOLE NAV",
         "Morris-Thorne · Exotic matter · Traversal · Orbital mechanics · Δv budget",
         "#8060ff", "wormhole_navigator"),
        ("tesseract",  "◈", "TESSERACT DECODER",
         "4D geometry · Gravity signals · Murphy's equation · TARS crystal · Bulk channel",
         "#c040ff", "tesseract_decoder"),
        ("crew",       "⛨", "CREW TELEMETRY",
         "Vitals · TARS/CASE AI · Interstellar systems · Cryosleep · Communications",
         "#81C784", "crew_telemetry"),
        ("mission",    "▤", "MISSION REPORTER",
         "Lazarus archive · Plan A/B · Blight model · Achievements · NASA reports",
         "#FFD700", "mission_reporter"),
        ("quantum",    "⚛", "QUANTUM SINGULARITY",
         "Planck foam · LQG · BKL oscillations · Page curve · Unruh · Holography · ER=EPR",
         "#8060ff", "quantum_singularity"),
    ]

    cols_m = st.columns(4)
    for i, (pg, icon, title, desc, clr, backend) in enumerate(modules_info):
        col = cols_m[i % 4]
        loaded = BACKENDS_LOADED.get(backend, True)
        st_txt = ("" if loaded else "○ OFFLINE")
        st_clr = ("#81C784" if loaded else "#D154FF")
        with col:
            st.markdown(f"""
            <div class="module-card" style="border-top:2px solid {clr}44;">
              <div class="module-card-icon">{icon}</div>
              <div class="module-card-title" style="color:{clr};">{title}</div>
              <div class="module-card-desc">{desc}</div>
              <div class="module-card-status" style="color:{st_clr};">{st_txt}</div>
            </div>""", unsafe_allow_html=True)

    section_rule()

    # ── Quote ─────────────────────────────────────────────────────────────
    q_txt, q_auth = INTERSTELLAR_QUOTES[S["quote_idx"] % len(INTERSTELLAR_QUOTES)]
    quote_banner(q_txt, q_auth)


# ── Technical Appendix ────────────────────────────────────────────────
    section_rule()
    with st.expander("◈ TECHNICAL APPENDIX — SYSTEM CONTROL MATHEMATICS & CLOSED-FORM FIELD EQUATIONS (MAXIMAL EXPANSION)"):
        st.markdown(r"""
        <div class="data-panel" style="font-size: 0.65rem; line-height: 2.0; color: var(--text-dim);">
        
        <h2 style="color:var(--gold); font-family:var(--font-head); letter-spacing:0.15em; font-size:1.1rem; margin-bottom:1rem;">
          I. MATRICES OF GARGANTUA SPACETIME (KERR METRIC EXACT SOLUTION)
        </h2>
        
        The structural framework of the gravity engine models the gravitational field of a rotating, uncharged supermassive black hole ($M \approx 10^8 M_\odot$) with an extreme dimensionless angular momentum spin parameter ($a^* = a/M \approx 1 - 10^{-14}$). 
        In standard Boyer-Lindquist coordinates $(t, r, \theta, \phi)$, the covariant components of the metric tensor $g_{\mu\nu}$ are written as a fully continuous tensor field matrix:

        ```math
        g_{\mu\nu} = \begin{pmatrix} 
        -\left(1 - \frac{r_s r}{\Sigma}\right)c^2 & 0 & 0 & -\frac{r_s r a \sin^2\theta}{\Sigma}c \\ 
        0 & \frac{\Sigma}{\Delta} & 0 & 0 \\ 
        0 & 0 & \Sigma & 0 \\ 
        -\frac{r_s r a \sin^2\theta}{\Sigma}c & 0 & 0 & \left(r^2 + a^2 + \frac{r_s r a^2 \sin^2\theta}{\Sigma}\right)\sin^2\theta 
        \end{pmatrix}
        ```

        Where the topological scalar functions are explicitly calculated at every spatial cell using the auxiliary equations:

        ```math
        r_s = \frac{2GM}{c^2}, \quad a = \frac{J}{Mc}, \quad \Sigma(r, \theta) = r^2 + a^2 \cos^2\theta, \quad \Delta(r) = r^2 - r_s r + a^2
        ```

        The coordinate singularities occur at the roots of $\Delta(r) = 0$, giving the exact boundaries for the outer/inner event horizons ($r_\pm$) and the static limit ergosurface boundary ($r_E(\theta)$):

        ```math
        r_{\pm} = \frac{r_s \pm \sqrt{r_s^2 - 4a^2}}{2}
        ```

        ```math
        r_E(\theta) = \frac{r_s + \sqrt{r_s^2 - 4a^2 \cos^2\theta}}{2}
        ```

        Because Gargantua operates at an extreme mass configuration, the local Hawking evaporation rate is completely suppressed. The Hawking temperature $T_H$ and surface gravity $\kappa$ at the exterior horizon profile resolve to:

        ```math
        T_H = \frac{\hbar \kappa}{2\pi k_B c} = \frac{\hbar c}{4\pi k_B} \left( \frac{r_+ - r_-}{2r_+^2 + a^2} \right)
        ```

        <hr style="border: 1px solid rgba(232,196,106,0.1); margin: 1.5rem 0;">

        <h2 style="color:var(--gold); font-family:var(--font-head); letter-spacing:0.15em; font-size:1.1rem; margin-bottom:1rem;">
          II. KINEMATIC GEODESICS & EXACT TIME DILATION MATRIX
        </h2>
        
        The temporal slippage ratio experienced by the crew on Miller's Planet (where 1 hour matches 7 Earth years, a factor of exactly $\gamma_{\text{total}} \approx 61,320$) requires solving the total proper time metric tracking along a stable circular equatorial orbit ($\theta = \pi/2$, $\dot{r} = 0$). 
        The invariant line element derivation translates directly into the closed-form time dilation equation:

        ```math
        \frac{d\tau}{dt} = \sqrt{ -\left( g_{tt} + 2g_{t\phi}\frac{\Omega}{c} + g_{\phi\phi}\frac{\Omega^2}{c^2} \right) }
        ```

        Substituting the individual coordinate metric terms yields the full master tracking equation used by the relativity module:

        ```math
        \Delta t' = \Delta t \sqrt{ 1 - \frac{r_s r}{r^2 + a^2 \cos^2\theta} - \frac{\Sigma \dot{r}^2}{c^2 \Delta} - \frac{\Sigma \dot{\theta}^2}{c^2} - \frac{\sin^2\theta}{c^2}\left( r^2 + a^2 + \frac{r_s r a^2 \sin^2\theta}{\Sigma} \right) \left(\frac{d\phi}{dt}\right)^2 + \frac{2r_s r a \sin^2\theta}{c \Sigma}\left(\frac{d\phi}{dt}\right) }
        ```

        The angular orbital velocity $\Omega = \frac{d\phi}{dt}$ for a co-rotating equatorial particle at the innermost stable circular boundary is strictly constrained by the frame-dragging value of the Kerr background (Lense-Thirring frequency $\omega$):

        ```math
        \Omega = \frac{c}{e^{\psi - \nu} + \frac{g_{t\phi}}{g_{tt}}} = \frac{\sqrt{GM}}{r^{3/2} + a\sqrt{G M/c^2}}
        ```

        ```math
        \omega(r, \theta) = -\frac{g_{t\phi}}{g_{\phi\phi}} = \frac{r_s r a c}{(r^2 + a^2)\Sigma + r_s r a^2 \sin^2\theta}
        ```

        The integration tracking of the path uses the standard Christoffel symbol connection metrics to enforce total energy ($E$) and angular momentum ($L$) conservation parameters:

        ```math
        \frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\tau} \frac{dx^\beta}{d\tau} = 0
        ```

        ```math
        \Gamma^\mu_{\alpha\beta} = \frac{1}{2} g^{\mu\rho} \left( \partial_\alpha g_{\beta\rho} + \partial_\beta g_{\alpha\rho} - \frac{\partial g_{\alpha\beta}}{\partial x^\rho} \right)
        ```

        <hr style="border: 1px solid rgba(232,196,106,0.1); margin: 1.5rem 0;">

        <h2 style="color:var(--gold); font-family:var(--font-head); letter-spacing:0.15em; font-size:1.1rem; margin-bottom:1rem;">
          III. WORMHOLE TOPOLOGY & EXOTIC MATTER FLUID COMPUTATIONS
        </h2>
        
        The space layout for the Saturn transit gateway models a spherically symmetric, traversable Lorentzian wormhole via the exact Morris-Thorne metric formulation. To prevent immediate pinch-off and frame collapse, the throat must be artificially structured with an exotic matter fields profile that systematically violates the Null Energy Condition (NEC).

        ```math
        ds^2 = -e^{2\Phi(r)}c^2 dt^2 + \frac{dr^2}{1 - \frac{b(r)}{r}} + r^2 \left( d\theta^2 + \sin^2\theta d\phi^2 \right)
        ```

        The stress-energy tensor components $T_{\hat{\mu}\hat{\nu}}$ in the orthonormal static reference frame are derived by matching this geometry directly through the Einstein field equations $G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$:

        ```math
        \rho(r)c^2 = T_{\hat{t}\hat{t}} = \frac{1}{8\pi G} \frac{b'(r)}{r^2}
        ```

        ```math
        \tau_r(r) = -T_{\hat{r}\hat{r}} = \frac{1}{8\pi G} \left[ \frac{b(r)}{r^3} - 2\left(1 - \frac{b(r)}{r}\right)\frac{\Phi'(r)}{r} \right]
        ```

        ```math
        p_t(r) = T_{\hat{\theta}\hat{\theta}} = T_{\hat{\phi}\hat{\phi}} = \frac{1}{8\pi G} \left( 1 - \frac{b(r)}{r} \right) \left[ \Phi''(r) + (\Phi'(r))^2 + \frac{\Phi'(r)}{r} - \frac{b'(r)r - b(r)}{2r(r - b(r))} \left( \Phi'(r) + \frac{1}{r} \right) \right]
        ```

        To enforce cross-boundary navigation safety for the Endurance ship hull, the exotic matter flux constraint for any null vector $k^\mu$ evaluates to a strictly negative parameter matching:

        ```math
        T_{\mu\nu} k^\mu k^\nu = \rho c^2 - \tau_r < 0
        ```

        ```math
        \rho c^2 - \tau_r = -\frac{1}{8\pi G} \left[ \frac{b(r) - b'(r)r}{r^3} + 2\left(1 - \frac{b(r)}{r}\right)\frac{\Phi'(r)}{r} \right] \Big|_{r=r_0} = -\frac{1}{8\pi G r_0^2} (1 - b'(r_0))
        ```

        This directly proves that the flare-out condition requires $b'(r_0) < 1$ at the absolute coordinate throat radius $r_0$.

        <hr style="border: 1px solid rgba(232,196,106,0.1); margin: 1.5rem 0;">

        <h2 style="color:var(--gold); font-family:var(--font-head); letter-spacing:0.15em; font-size:1.1rem; margin-bottom:1rem;">
          IV. EXOPLANETARY HABITABILITY INDEXING & GAS KINETICS
        </h2>
        
        Candidate verification pipelines for Plan B apply an empirical multi-factor Earth Similarity Index (ESI) mapping vector deviation profiles across multiple macroscopic geometric targets:

        ```math
        ESI = \left[ \left(1 - \left|\frac{R - R_0}{R + R_0}\right|\right)^{w_R} \cdot \left(1 - \left|\frac{\rho - \rho_0}{\rho + \rho_0}\right|\right)^{w_\rho} \cdot \left(1 - \left|\frac{v_e - v_{e0}}{v_e + v_{e0}}\right|\right)^{w_{v_e}} \cdot \left(1 - \left|\frac{T_s - T_{s0}}{T_s + T_{s0}}\right|\right)^{w_{T_s}} \right]^{\frac{1}{4}}
        ```

        Atmospheric thermal stripping and core density depletion ratios are calculated dynamically against the Jeans escape criteria to ensure long-term ecosystem stability for the frozen embryos bank. The global particle loss flux $\Phi_J$ is derived as:

        ```math
        \Phi_J = \frac{n_c v_{\text{th}}}{2\sqrt{\pi}} (1 + \lambda_c) e^{-\lambda_c}
        ```

        ```math
        v_{\text{th}} = \sqrt{\frac{2 k_B T_c}{m}}, \quad \lambda_c = \frac{v_e^2}{v_{\text{th}}^2} = \frac{G M_p m}{k_B T_c r_c}
        ```

        <hr style="border: 1px solid rgba(232,196,106,0.1); margin: 1.5rem 0;">

        <h2 style="color:var(--gold); font-family:var(--font-head); letter-spacing:0.15em; font-size:1.1rem; margin-bottom:1rem;">
          V. TARS / CASE MACHINE INTELLIGENCE MATRIX (HARMONIC RESONANCE FIELDS)
        </h2>
        
        The cognitive processing architecture for TARS and CASE completely abandons standard statistical data-splitting models. Instead, classification tasks are mapped directly to physics-informed quantum states utilizing **Harmonic Resonance Fields (HRF)**, where decision boundaries are modeled as complex wave interference fields rather than linear separations. 
        
        Biometric profiles and cryogenic telemetry from the crew are monitored via a highly specialized **Holographic Soul Unit**, which deploys non-monotonic kernels to detect underlying periodic resonance signatures linked to complex physiological and consciousness states. The generalized field wavefunction $\Psi(\mathbf{x}, t)$ evolves under high-performance parallel computation:

        ```math
        \Psi(\mathbf{x}, t) = \sum_{n=1}^{N} c_n(t) \exp\left[ i \left( \mathbf{k}_n \cdot \mathbf{x} - \omega_n t \right) \right] \cdot \mathcal{K}_{nm}(\theta, \phi)
        ```

        The non-monotonic resonance detection kernel function $\mathcal{K}_{nm}$ calculates phase matches across highly nonlinear biological signals (such as EEG states) using the expansion:

        ```math
        \mathcal{K}_{nm}(\theta, \phi) = \int_{0}^{\infty} H_n(\xi) e^{-\xi^2} \cos(m \xi \cdot \text{sgn}(\theta - \phi)) \, d\xi
        ```

        This unique topological architecture guarantees absolute **Phase Jitter Robustness**, maintaining near 100% predictive tracking accuracy even under massive temporal shifts, temporal dilation discontinuities, and noise. All linear systems are parallelized via low-level GPU acceleration (CuPy/RAPIDS architecture) to avoid any risk of catastrophic forgetting during extreme gravitational wave operations.

        <hr style="border: 1px solid rgba(232,196,106,0.1); margin: 1.5rem 0;">

        <h2 style="color:var(--gold); font-family:var(--font-head); letter-spacing:0.15em; font-size:1.1rem; margin-bottom:1rem;">
          VI. BRANE COSMOLOGY FIELD MATRIX & TESSERACT SIGNAL EXTRACTION
        </h2>
        
        To establish communication paths across time layout coordinates, gravity is modeled as a bulk-propagating gauge field moving through a 5-dimensional anti-de Sitter ($AdS_5$) bulk background. Following the Arkani-Hamed-Dimopoulos-Dvali (ADD) and Randall-Sundrum (RS) braneworld framework models, the effective gravitational potential on our local 3-brane updates at short distances to:

        ```math
        V(r) = - \frac{G_N M}{r} \left( 1 + \sum_{n=1}^{\infty} \alpha_n e^{-\frac{n r}{\lambda}} \right) \propto - \frac{G_{(4+n)} M}{r^{1+n}}
        ```

        The spatial metric perturbations $h_{\mu\nu}$ tracking through the hyper-volume grid are systematically generated by feeding specific localized stress tensor pulses (actuated via the watch mechanics) directly into the bulk field equations:

        ```math
        \left[ \eta^{\alpha\beta} \partial_\alpha \partial_\beta + \frac{\partial^2}{\partial y^2} - \frac{4}{y^2} \right] h_{\mu\nu}(x, y) = -16\pi G_{5D} \left[ T_{\mu\nu}(x) - \frac{1}{3}\eta_{\mu\nu}T^\alpha_\alpha(x) \right] \delta(y)
        ```

        Solving this via the 5D boundary Green's function allows the tesseract module to extract discrete gravity anomalies, allowing data symbols to be decoded backward through the history matrix:

        ```math
        \mathcal{G}_{5D}(x, y; x', y') = \int \frac{d^4 k}{(2\pi)^4} e^{i k \cdot (x - x')} \mathcal{R}_k(y, y')
        ```

        <hr style="border: 1px solid rgba(232,196,106,0.1); margin: 1.5rem 0;">

        <h2 style="color:var(--gold); font-family:var(--font-head); letter-spacing:0.15em; font-size:1.1rem; margin-bottom:1rem;">
          VII. QUANTUM SINGULARITY LAB — PLANCK SCALE, LOOP QUANTUM GRAVITY, BKL OSCILLATIONS, HAWKING PAGE CURVE, UNRUH VACUUM PHYSICS, QUANTUM CHAOS & HOLOGRAPHY
        </h2>

        <b style="color:var(--blue); font-size:0.72rem;">A. PLANCK UNITS & QUANTUM FOAM NUCLEATION</b><br><br>

        The complete Planck unit system (CODATA 2018) defines the natural quantum gravity scale at which spacetime topology fluctuates. All four fundamental Planck constants emerge from dimensional analysis of $G$, $\hbar$, $c$, and $k_B$:

        ```math
        \ell_P = \sqrt{\frac{\hbar G}{c^3}} = 1.61626 \times 10^{-35}\,\text{m}, \quad
        t_P = \frac{\ell_P}{c} = \sqrt{\frac{\hbar G}{c^5}} = 5.39116 \times 10^{-44}\,\text{s}
        ```

        ```math
        m_P = \sqrt{\frac{\hbar c}{G}} = 2.17643 \times 10^{-8}\,\text{kg}, \quad
        T_P = \frac{m_P c^2}{k_B} = \sqrt{\frac{\hbar c^5}{G k_B^2}} = 1.41678 \times 10^{32}\,\text{K}
        ```

        Virtual black hole nucleation in the quantum foam background proceeds via the Euclidean path integral. The dominant saddle-point configuration is the Hawking-Gibbons instanton, yielding a nucleation rate per unit Planck 4-volume proportional to the exponential of the negative Bekenstein-Hawking entropy:

        ```math
        \Gamma_{\rm foam} \sim m_P^{-4} \exp\!\left(-S_{\rm BH}\right) = m_P^{-4} \exp\!\left(-\frac{4\pi M^2}{m_P^2}\right)
        ```

        Wheeler's spacetime foam topology undergoes genus fluctuations at scale $\ell_P$. The genus spectrum for a 2-sphere of radius $r$ follows the Planck-suppressed distribution:

        ```math
        P(g, r) \sim \exp\!\left(-\frac{4\pi r^2}{\ell_P^2}\,g\right), \quad \langle g \rangle \sim \frac{\ell_P^2}{4\pi r^2}
        ```

        Lorentz dispersion receives quantum gravity corrections at order $(E/E_P)^n$ where $n=1$ (linear, LQG-favoured) or $n=2$ (quadratic, string-favoured). The modified dispersion relation and induced photon group velocity shift are:

        ```math
        \omega^2 = k^2 c^2 \left[1 \pm \xi_n \left(\frac{\hbar\omega}{E_P c^2}\right)^n\right], \quad
        \frac{\delta v_g}{c} \approx \pm \frac{n+1}{2}\,\xi_n \left(\frac{E}{E_P}\right)^n
        ```

        <hr style="border: 1px solid rgba(128,96,255,0.12); margin: 1rem 0;">
        <b style="color:var(--blue); font-size:0.72rem;">B. LOOP QUANTUM GRAVITY — SPIN NETWORKS & AREA/VOLUME SPECTRA</b><br><br>

        In Loop Quantum Gravity (Ashtekar-Lewandowski formulation), geometric operators are promoted to well-defined self-adjoint operators on the kinematic Hilbert space $\mathcal{H}_{\rm kin}$. Spatial area is quantised with a discrete spectrum labelled by spin quantum numbers $j_i \in \{0, \tfrac{1}{2}, 1, \tfrac{3}{2}, \ldots\}$ intersecting a surface $S$:

        ```math
        \hat{A}_S \, |\Gamma, j_l, i_n\rangle = 8\pi\gamma\ell_P^2 \sum_{p\,\in\,S\cap\Gamma} \sqrt{j_p(j_p+1)}\; |\Gamma, j_l, i_n\rangle
        ```

        The Barbero-Immirzi parameter $\gamma = 0.2375$ (fixed by Domagala-Lewandowski black hole entropy counting) sets the absolute scale. The minimum non-zero area eigenvalue — the area gap — is:

        ```math
        \Delta_A = 4\sqrt{3}\,\pi\,\gamma\,\ell_P^2 \approx 1.0509 \times 10^{-69}\,\text{m}^2 \quad (j_{\rm min} = \tfrac{1}{2})
        ```

        Volume eigenvalues at a 4-valent node $n$ with intertwiners $i_n$ scale as:

        ```math
        V_n \sim (\gamma\,\ell_P^2)^{3/2}\,\sqrt{|i_n|}, \quad V_{\rm min} \sim \ell_P^3 \approx 4.22 \times 10^{-105}\,\text{m}^3
        ```

        The Loop Quantum Cosmology (LQC) effective Friedmann equation replaces the Big Bang singularity with a quantum bounce. The modified Hamiltonian constraint yields:

        ```math
        H^2 = \left(\frac{\dot{a}}{a}\right)^2 = \frac{8\pi G}{3}\,\rho\!\left(1 - \frac{\rho}{\rho_{\rm crit}}\right), \quad
        \rho_{\rm crit} = \frac{3}{8\pi\gamma^2\lambda^2\kappa^2} \approx 0.41\,\rho_P
        ```

        where $\lambda^2 = 4\sqrt{3}\pi\gamma\ell_P^2$ is the minimum area eigenvalue in Planck units. The quantum-corrected Raychaudhuri equation:

        ```math
        \frac{\ddot{a}}{a} = -\frac{4\pi G}{3}\left(\rho + 3p\right)\left(1 - \frac{2\rho}{\rho_{\rm crit}}\right) + \frac{8\pi G}{3}\frac{\rho^2}{\rho_{\rm crit}}
        ```

        The Wheeler-DeWitt equation in LQC minisuperspace (with $\alpha = \ln a$ as the internal clock) takes the form of a difference equation with step $\lambda$, whose continuum limit recovers:

        ```math
        -\frac{\partial^2 \Psi}{\partial\alpha^2} + V(\alpha)\,\Psi = 0, \quad V(\alpha) = e^{6\alpha}\!\left[V_{\rm matter} - k\,e^{-2\alpha} + \Lambda\,e^{4\alpha}/3\right]
        ```

        <hr style="border: 1px solid rgba(128,96,255,0.12); margin: 1rem 0;">
        <b style="color:var(--blue); font-size:0.72rem;">C. BKL OSCILLATIONS & KASNER SINGULARITY INTERIOR</b><br><br>

        Near a spacelike singularity, the BKL (Belinskii-Khalatnikov-Lifshitz) analysis shows that spatial gradients decouple and each point evolves independently through a sequence of Kasner epochs. The general Kasner metric and exponent constraints are:

        ```math
        ds^2 = -dt^2 + \sum_{i=1}^{3} t^{2p_i}\,(dx^i)^2, \quad \sum_{i=1}^{3} p_i = 1, \quad \sum_{i=1}^{3} p_i^2 = 1
        ```

        Parametrising by the Lifshitz-Khalatnikov variable $u \geq 1$, the three Kasner exponents take the exact closed-form values:

        ```math
        p_1(u) = \frac{-u}{1+u+u^2},\quad p_2(u) = \frac{1+u}{1+u+u^2},\quad p_3(u) = \frac{u(1+u)}{1+u+u^2}
        ```

        The BKL map governs transitions between Kasner epochs as $t\to 0$. Each "bounce" off a potential wall exchanges which direction contracts fastest and which two are expanding:

        ```math
        u \;\mapsto\; \begin{cases} u - 1, & u > 2 \\ \dfrac{1}{u-1}, & 1 < u \leq 2 \end{cases}
        ```

        The Misner Mixmaster universe (Bianchi IX) undergoes a chaotic sequence of Kasner eras, each containing an integer number of epochs. The era lengths $k_n$ follow an approximation related to the Gauss-Kuzmin distribution for continued fractions:

        ```math
        u = k + \frac{1}{k_1 + \dfrac{1}{k_2 + \cdots}}, \quad \langle k\rangle = \frac{\pi^2}{6\ln 2} \approx 2.37
        ```

        The anisotropy parameter $\Omega_{\rm Bianchi}$ for Bianchi IX scale factors $(a, b, c)$ satisfies:

        ```math
        \Omega_{\rm Bianchi} = \frac{a^4 + b^4 + c^4 - 2(a^2 b^2 + b^2 c^2 + c^2 a^2)}{2(abc)^{4/3}}, \quad \Omega_{\rm Bianchi} \to \infty \;\text{at singularity}
        ```

        <hr style="border: 1px solid rgba(128,96,255,0.12); margin: 1rem 0;">
        <b style="color:var(--blue); font-size:0.72rem;">D. HAWKING RADIATION, EVAPORATION & PAGE CURVE</b><br><br>

        A Schwarzschild black hole of mass $M$ emits thermal Hawking radiation at temperature $T_H$ with a luminosity $\mathcal{L}$ that drives complete evaporation over time $t_{\rm evap}$:

        ```math
        T_H = \frac{\hbar c^3}{8\pi G M k_B}, \quad
        \mathcal{L} = \frac{\hbar c^6}{15360\,\pi\, G^2 M^2}, \quad
        \frac{dM}{dt} = -\frac{\hbar c^4}{15360\,\pi\,G^2 M^2}
        ```

        ```math
        t_{\rm evap} = \frac{5120\,\pi\,G^2 M_0^3}{\hbar c^4}, \quad
        M(t) = M_0\!\left(1 - \frac{t}{t_{\rm evap}}\right)^{1/3}
        ```

        The Bekenstein-Hawking entropy (in Planck units where $G = \hbar = c = 1$) and the scrambling time at inverse temperature $\beta = 1/(k_B T_H)$ are:

        ```math
        S_{\rm BH} = \frac{A}{4\ell_P^2} = \frac{4\pi G M^2}{\hbar c} = 4\pi M^2, \quad
        t_{\rm Page} \approx \frac{t_{\rm evap}}{2}, \quad
        t_{\rm scr} = \frac{\beta}{2\pi}\ln S_{\rm BH} = \frac{M}{2\pi}\ln(4\pi M^2)
        ```

        The Page curve describes the entanglement entropy $S_{\rm rad}(t)$ of the radiation. Before the Page time it grows (naive Hawking), after it falls back to zero (unitarity). The island rule corrects the entropy using a quantum extremal surface:

        ```math
        S_{\rm gen}[\mathcal{I}] = \frac{{\rm Area}(\partial\mathcal{I})}{4G} + S_{\rm bulk}[R\cup\mathcal{I}], \quad
        S_{\rm rad}(t) = \min_{\mathcal{I}}\,{\rm ext}_{\mathcal{I}}\!\left[S_{\rm gen}[\mathcal{I}]\right]
        ```

        The two competing saddles (no-island and island) give the Page curve piecewise:

        ```math
        S_{\rm rad}(t) = \min\!\left\{ S_{\rm Hawking}(t),\; S_{\rm BH}^{\rm initial} - S_{\rm BH}(t) + S_{\rm bdy} \right\}
        ```

        <hr style="border: 1px solid rgba(128,96,255,0.12); margin: 1rem 0;">
        <b style="color:var(--blue); font-size:0.72rem;">E. UNRUH EFFECT, CASIMIR PRESSURE & SCHWINGER PAIR PRODUCTION</b><br><br>

        A uniformly accelerated observer (Rindler frame) perceives the Minkowski vacuum as a thermal bath at the Unruh temperature $T_U$. The full Planck spectrum seen by the Unruh-DeWitt detector with acceleration $a$ is:

        ```math
        T_U = \frac{\hbar a}{2\pi c k_B}, \quad
        n(\omega) = \frac{1}{\exp\!\left(\frac{2\pi c\,\omega}{a}\right) - 1}, \quad
        \mathcal{R}(\omega, a) = \frac{a^2}{4\pi^2 c^2}\,\frac{1}{e^{2\pi\omega c/a}-1}
        ```

        The Casimir effect between two perfectly conducting parallel plates of area $A$ separated by distance $d$ in vacuum gives an attractive pressure and energy:

        ```math
        P_{\rm Cas} = -\frac{\pi^2\hbar c}{240\,d^4}, \quad
        E_{\rm Cas} = -\frac{\pi^2\hbar c\,A}{720\,d^3}, \quad
        F_{\rm Cas} = -\frac{\partial E_{\rm Cas}}{\partial d} = -\frac{\pi^2\hbar c\,A}{240\,d^4}
        ```

        The Schwinger pair-production rate per unit 4-volume in an external electric field $E$ (with critical field $E_c = m_e^2 c^3/(e\hbar) \approx 1.32\times 10^{18}\,\text{V/m}$) summed over all Landau levels gives:

        ```math
        \frac{W}{V} = \frac{\alpha E^2}{\pi^2} \sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n} \exp\!\left(-\frac{n\pi E_c}{E}\right)
        \;\approx\; \frac{\alpha E^2}{\pi^2}\exp\!\left(-\frac{\pi E_c}{E}\right) \quad (E \ll E_c)
        ```

        <hr style="border: 1px solid rgba(128,96,255,0.12); margin: 1rem 0;">
        <b style="color:var(--blue); font-size:0.72rem;">F. QUANTUM CHAOS, OTOC SCRAMBLING & SYK MODEL</b><br><br>

        The Maldacena-Shenker-Stanford (MSS) chaos bound states that the quantum Lyapunov exponent $\lambda_L$ governing out-of-time-order correlator (OTOC) growth is universally bounded:

        ```math
        \lambda_L \leq \frac{2\pi k_B T}{\hbar} \quad (\text{saturated by black holes and SYK})
        ```

        The OTOC diagnostic of quantum scrambling uses two operators $V, W$ separated in time and is defined as:

        ```math
        F(t) = \langle V^\dagger(t)\,W^\dagger\,V(t)\,W \rangle_\beta, \quad
        F(t) \approx 1 - \frac{\varepsilon}{N}\,e^{\lambda_L t}, \quad t < t_{\rm scr}
        ```

        where $\varepsilon$ is an initial coupling strength and $N$ is the number of degrees of freedom. After the scrambling time $t_{\rm scr}$, $F(t)\to 0$ — information is fully scrambled.

        The Sachdev-Ye-Kitaev (SYK) model of $N$ Majorana fermions $\chi_i$ with random all-to-all $q$-body couplings $J_{i_1\ldots i_q}$ has the Hamiltonian:

        ```math
        H_{\rm SYK} = i^{q/2}\!\sum_{1\leq i_1 < \cdots < i_q \leq N} J_{i_1\cdots i_q}\,\chi_{i_1}\cdots\chi_{i_q}, \quad
        \langle J_{i_1\cdots i_q}^2\rangle = \frac{(q-1)!\,\mathcal{J}^2}{N^{q-1}}
        ```

        In the large-$q$ limit, the spectral density (Schwarzian/JT gravity regime) takes the exact semicircular-like form:

        ```math
        \rho(E) = \frac{1}{2\pi\tilde{\mathcal{J}}^2}\sqrt{4\tilde{\mathcal{J}}^2 - E^2}, \quad
        \tilde{\mathcal{J}} = \mathcal{J}\sqrt{\binom{N}{q/2}}\,2^{-N/2}
        ```

        Level spacing statistics in the chaotic phase obey the Gaussian Unitary Ensemble (GUE) Wigner-Dyson distribution:

        ```math
        P(s) = \frac{32}{\pi^2}\,s^2\,\exp\!\left(-\frac{4s^2}{\pi}\right), \quad \langle s\rangle = 1
        ```

        <hr style="border: 1px solid rgba(128,96,255,0.12); margin: 1rem 0;">
        <b style="color:var(--blue); font-size:0.72rem;">G. HOLOGRAPHIC ENTANGLEMENT ENTROPY & ER=EPR</b><br><br>

        The Ryu-Takayanagi (RT) formula computes the entanglement entropy of a boundary region $A$ in a holographic CFT via the area of the minimal bulk surface $\gamma_A$ homologous to $A$:

        ```math
        S_{\rm EE}(A) = \frac{{\rm Area}(\gamma_A)}{4G_N}, \quad \delta S_{\rm EE} = \frac{\delta{\rm Area}(\gamma_A)}{4G_N} \quad (\text{Faulkner-Lewkowycz-Maldacena})
        ```

        For a 2D CFT in vacuum with central charge $c$, a single interval of length $\ell$ with UV cutoff $\varepsilon$, and at finite inverse temperature $\beta$:

        ```math
        S(A)\big|_{T=0} = \frac{c}{3}\ln\!\frac{\ell}{\varepsilon}, \qquad
        S(A)\big|_{T>0} = \frac{c}{3}\ln\!\left[\frac{\beta}{\pi\varepsilon}\sinh\!\frac{\pi\ell}{\beta}\right]
        ```

        Holographic mutual information $I(A:B) = S_A + S_B - S_{A\cup B}$ undergoes a first-order phase transition (connected $\to$ disconnected RT surface) at a critical separation $d_c$:

        ```math
        I(A:B) = \begin{cases} \dfrac{c}{3}\ln\dfrac{\ell_A\ell_B}{(\ell_A+d+\ell_B)\,d\,\varepsilon^2} & d < d_c \\ 0 & d \geq d_c \end{cases}
        ```

        The Maldacena-Susskind ER=EPR conjecture identifies the maximally entangled Einstein-Rosen bridge between two black holes with the thermofield double state of two CFTs:

        ```math
        |\text{TFD}\rangle = \frac{1}{\sqrt{Z(\beta)}}\sum_n e^{-\beta E_n/2}\,|n\rangle_L\otimes|n\rangle_R, \quad
        Z(\beta) = \text{Tr}\!\left[e^{-\beta H}\right]
        ```

        Holographic complexity (CV conjecture) equates the complexity of the boundary state to the volume of the maximal Cauchy slice anchored to the boundary time slice, growing linearly at late times:

        ```math
        \mathcal{C} = \frac{{\rm Vol}(\Sigma_{\rm max})}{G_N\,\ell_{\rm AdS}}, \quad
        \frac{d\mathcal{C}}{dt} \xrightarrow{t\to\infty} \frac{2M}{\pi} = \frac{2E}{\pi}
        ```

        <hr style="border: 1px solid rgba(128,96,255,0.12); margin: 1rem 0;">
        <b style="color:var(--blue); font-size:0.72rem;">H. COOPER'S SINGULARITY CROSSING (KERR INTERIOR & BEKENSTEIN BOUND)</b><br><br>

        Inside the Kerr black hole, Cooper's geodesic from just inside the event horizon to the ring singularity follows the cycloid proper-time parameterisation (radial equatorial infall, $L=0$, $E=mc^2$):

        ```math
        r(\eta) = \frac{r_s}{2}(1 + \cos\eta), \quad
        \tau(\eta) = \frac{r_s}{2c}(\eta + \sin\eta), \quad \eta \in [0,\pi]
        ```

        The maximum proper time available from crossing at $r \approx r_s$ to encountering the singularity at $r=0$ provides the absolute upper bound on information processing and communication time inside the black hole:

        ```math
        \tau_{\rm max} = \frac{\pi r_s}{2c} = \frac{\pi G M}{c^3} \approx 1.55\,\text{hr} \left(\frac{M}{10^8 M_\odot}\right)
        ```

        Cauchy horizon mass-inflation instability at the inner horizon $r_-$ causes the Weyl curvature tensor component to diverge exponentially with advanced time $v$:

        ```math
        C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma} \sim e^{2\kappa_- v} \to \infty, \quad
        \kappa_- = \frac{c^2(r_+ - r_-)}{2(r_+^2 + a^2)}
        ```

        The Bekenstein information bound on the maximum entropy (number of bits $I_{\rm max}$) storable in the TARS quantum data crystal of radius $R$ and total energy $E$:

        ```math
        I_{\rm max} = \frac{S_{\rm max}}{k_B\ln 2} \leq \frac{2\pi R E}{\hbar c \ln 2} \quad (\text{Bekenstein 1981})
        ```

        The Randall-Sundrum bulk transmission amplitude for a graviton signal propagating a bulk transverse distance $y$ through the $AdS_5$ background with curvature scale $k = 1/\ell_{\rm AdS}$ determines the signal fidelity from Cooper's position to the brane:

        ```math
        |\mathcal{T}(y)|^2 = e^{-2ky}, \quad
        \mathcal{F}_{\rm signal}(y) = \exp\!\left(-\frac{2y}{\ell_{\rm AdS}}\right)
        ```

        The quantum decoherence timescale for Cooper's state inside the Gargantua interior (at local Hawking temperature $T_H$) sets the maximum coherence window for information encoding onto the singularity worldsheet:

        ```math
        \tau_{\rm dec} = \frac{\hbar}{k_B T_H} = \frac{8\pi G M}{c^3}, \quad
        \tau_{\rm dec}\big|_{\rm Gargantua} \approx 9.84 \times 10^{11}\,\text{yr} \quad (M = 10^8 M_\odot, a^* \approx 1)
        ```

        The Shannon capacity of the gravity wave channel through which Murphy decodes Cooper's message from the tesseract, modelled as an additive Gaussian noise channel with signal power $P_s$ and noise spectral density $N_0$, is bounded by:

        ```math
        C_{\rm Murphy} = \Delta f \log_2\!\left(1 + \frac{P_s}{N_0\,\Delta f}\right) \leq \frac{P_s}{N_0 \ln 2} \quad (\text{bits/s})
        ```

        </div>
        """, unsafe_allow_html=True)

        



def _render_gargantua_overview():
    """Render Gargantua schematic as matplotlib figure."""
    MPL_STYLE = {"figure.facecolor":"#04060c","axes.facecolor":"#04060c",
                 "text.color":"#E8C46A","font.family":"monospace"}
    plt.rcParams.update(MPL_STYLE)
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("#04060c")
    ax.set_facecolor("#020408")

    # Gargantua accretion disk (colour gradient)
    from matplotlib.colors import LinearSegmentedColormap
    disk_cmap = LinearSegmentedColormap.from_list("disk",
        ["#000","#200a00","#802000","#e05800","#ffaa00","#ffe060","#fff"], N=512)
    theta = np.linspace(0, 2*np.pi, 500)
    # Draw disk rings
    for r, alpha_mult in [(6.5,1.0),(7.5,0.7),(9.0,0.5),(11.0,0.3),(13.5,0.15)]:
        x  = r * np.cos(theta)
        y  = r * np.sin(theta) * 0.35   # flattened (inclined disk)
        ax.fill(x, y, color=disk_cmap(1-r/15), alpha=alpha_mult*0.85)

    # Doppler brightening: left side brighter
    for r in np.linspace(5.5, 14, 8):
        x = r * np.cos(theta); y = r * np.sin(theta)*0.35
        bright = np.exp(-0.5*((theta - np.pi)/1.5)**2) * 0.3
        ax.plot(x, y, color="#ffcc60", lw=0.4*bright.mean()*10,
                alpha=0.3, solid_capstyle="round")

    # Black hole shadow
    shadow = plt.Circle((0,0), 4.5, color="#000", zorder=10)
    ax.add_patch(shadow)
    # Photon ring
    ph_ring = plt.Circle((0,0), 5.0, fill=False, ec="#CE93D8",
                          lw=0.8, ls="--", zorder=11)
    ax.add_patch(ph_ring)
    # ISCO
    isco = plt.Circle((0,0), 5.8, fill=False, ec="#4FC3F7",
                       lw=0.6, ls=":", zorder=11)
    ax.add_patch(isco)

    # Labels
    ax.text(0, 0, "GARGANTUA\nM=10⁸M☉\na*≈1", ha="center", va="center",
            fontsize=5.5, color="#E8C46A", fontfamily="monospace", zorder=12)
    ax.text(5.5, 0.8, "r_ph", fontsize=5, color="#CE93D8", zorder=12)
    ax.text(6.5, 1.2, "r_ISCO", fontsize=5, color="#4FC3F7", zorder=12)
    ax.text(-12, 3.5, "Doppler\nblueshift", fontsize=5, color="#ffcc60",
            ha="center")
    ax.text(11, -3, "Doppler\nredshift", fontsize=5, color="#ff6600",
            ha="center")

    ax.set_xlim(-16, 16); ax.set_ylim(-7, 7)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("GARGANTUA — Kerr BH  a*≈1−10⁻¹⁴  ·  Accretion Disk (NT Model)",
                 fontsize=7, color="#E8C46A", pad=8)

    st.pyplot(fig, width='stretch')
    plt.close(fig)


def _render_plan_progress():
    """Render Plan A/B progress bars."""
    st.markdown("""
    <div style="font-family:monospace;font-size:0.58rem;
                color:#3a4a60;letter-spacing:0.12em;
                text-transform:uppercase;margin-bottom:0.5rem;">
      ── PLAN A / PLAN B STATUS ──
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style="background:rgba(255,136,0,0.06);
                    border:1px solid rgba(255,136,0,0.20);
                    border-radius:3px;padding:0.6rem;
                    font-family:monospace;text-align:center;">
          <div style="font-size:0.55rem;color:#5a6a80;
                      letter-spacing:0.10em;margin-bottom:0.3rem;">PLAN A</div>
          <div style="font-size:1.6rem;font-weight:700;color:#FF8800;">
            {PLAN_A_PCT:.0f}%
          </div>
          <div style="font-size:0.52rem;color:#5a6a80;">30/42 coefficients</div>
          <div style="margin-top:0.4rem;height:3px;
                      background:rgba(255,136,0,0.12);border-radius:2px;">
            <div style="height:100%;width:{PLAN_A_PCT:.0f}%;
                        background:#FF8800;border-radius:2px;"></div>
          </div>
          <div style="margin-top:0.3rem;font-size:0.50rem;color:#FF8800;">
            TARS: 30  Brand: 12  Murph: 0
          </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background:rgba(79,195,247,0.06);
                    border:1px solid rgba(79,195,247,0.20);
                    border-radius:3px;padding:0.6rem;
                    font-family:monospace;text-align:center;">
          <div style="font-size:0.55rem;color:#5a6a80;
                      letter-spacing:0.10em;margin-bottom:0.3rem;">PLAN B</div>
          <div style="font-size:1.6rem;font-weight:700;color:#4FC3F7;">
            {PLAN_B_EMBRYOS:,}
          </div>
          <div style="font-size:0.52rem;color:#5a6a80;">frozen embryos</div>
          <div style="margin-top:0.4rem;height:3px;
                      background:rgba(79,195,247,0.12);border-radius:2px;">
            <div style="height:100%;width:94%;
                        background:#4FC3F7;border-radius:2px;"></div>
          </div>
          <div style="margin-top:0.3rem;font-size:0.50rem;color:#4FC3F7;">
            94% viability · Diversity: 0.8842 · MVP: ✓
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:monospace;font-size:0.54rem;
                background:rgba(4,6,12,0.80);
                border:1px solid rgba(232,196,106,0.08);
                border-radius:3px;padding:0.5rem 0.6rem;
                margin-top:0.4rem;line-height:1.8;color:#5a6a80;">
      <span style="color:#D154FF;">BLIGHT EXTINCTION:</span>
      ~2095 at current spread rate  ·
      <span style="color:#FF8800;">URGENCY: CRITICAL</span><br>
      Extinction: ~{2095}  ·  Population: 3.5B → {0.8:.1f}B by 2090
      ·  Mission deadline: ACTIVE
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §10  SYSTEM STATUS PAGE
# ══════════════════════════════════════════════════════════════════════════════
def render_system_status():
    page_header(
        "SYSTEM STATUS",
        "Backend module health · Import diagnostics · Python environment",
        accent="#4FC3F7", icon="ℹ"
    )

    # Backend status table
    kpi_row([
        ("Total Modules",   str(len(NAV_PAGES)-2),
         "#E8C46A", "scientific backends"),
        ("Online",          str(sum(1 for v in BACKENDS_LOADED.values() if v)),
         "#81C784", "operational"),
        ("Offline",         str(sum(1 for v in BACKENDS_LOADED.values() if not v)),
         "#D154FF", "import failed"),
        ("Python",          f"{sys.version_info.major}.{sys.version_info.minor}",
         "#4FC3F7", "interpreter"),
    ])

    scan_line()

    backend_info = [
        ("gravity_engine",        "Gravity Engine",      "⬡", "#FF8800",
         "Kerr BH physics, GW synthesis, accretion disk, tidal forces"),
        ("relativity_calculator", "Relativity Calc",     "⏱", "#4FC3F7",
         "SR/GR time dilation, twin paradox, Cooper-Murph timeline"),
        ("planet_analyzer",       "Planet Scanner",      "🪐", "#81C784",
         "Habitability scoring, atmosphere, spectroscopy, biosignatures"),
        ("wormhole_navigator",    "Wormhole Navigator",  "⟳", "#8060ff",
         "Morris-Thorne geometry, exotic matter, orbital mechanics"),
        ("tesseract_decoder",     "Tesseract Decoder",   "◈", "#c040ff",
         "4D geometry, gravity signals, Murphy's equation, TARS crystal"),
        ("crew_telemetry",        "Crew Telemetry",      "⛨", "#81C784",
         "Crew health, TARS/CASE AI, Interstellar systems, cryosleep"),
        ("mission_reporter",      "Mission Reporter",    "▤", "#FFD700",
         "Lazarus archive, Plan A/B, blight model, achievements"),
    ]

    c1, c2 = st.columns(2)
    for i, (mod, name, icon, clr, desc) in enumerate(backend_info):
        col = c1 if i % 2 == 0 else c2
        loaded = BACKENDS_LOADED.get(mod, False)
        err    = BACKEND_ERRORS.get(mod, "")
        with col:
            status_clr = "#81C784" if loaded else "#D154FF"
            status_txt = "ONLINE" if loaded else "OFFLINE"
            st.markdown(f"""
            <div style="background:rgba(6,10,20,0.90);
                        border:1px solid rgba(232,196,106,0.08);
                        border-left:2px solid {clr if loaded else '#D154FF'};
                        border-radius:3px;padding:0.6rem 0.8rem;
                        margin-bottom:0.4rem;font-family:monospace;">
              <div style="display:flex;justify-content:space-between;
                          align-items:center;margin-bottom:0.2rem;">
                <span style="color:{clr};font-size:0.65rem;font-weight:600;">
                  {icon} {name}
                </span>
                <span style="color:{status_clr};font-size:0.55rem;
                             background:rgba({_hex_to_rgb(status_clr)},0.10);
                             border:1px solid rgba({_hex_to_rgb(status_clr)},0.25);
                             padding:0.08rem 0.35rem;border-radius:2px;">
                  {status_txt}
                </span>
              </div>
              <div style="font-size:0.54rem;color:#5a6a80;">{desc}</div>
              {"" if not err else f'<div style="font-size:0.52rem;color:#D154FF;margin-top:0.2rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="{err}">Error: {err[:80]}...</div>'}
            </div>""", unsafe_allow_html=True)

    section_rule()

    # Dependencies check
    st.markdown("""
    <div style="font-family:monospace;font-size:0.62rem;
                color:#3a4a60;letter-spacing:0.12em;
                text-transform:uppercase;margin-bottom:0.5rem;">
      ── PYTHON DEPENDENCIES ──
    </div>""", unsafe_allow_html=True)

    deps = [
        ("streamlit",     True),  ("numpy",       True),
        ("pandas",        True),  ("matplotlib",  True),
        ("scipy",         True),  ("plotly",      False),
    ]
    dep_cols = st.columns(6)
    for col, (dep, required) in zip(dep_cols, deps):
        try:
            mod = __import__(dep)
            ver = getattr(mod, "__version__", "?")
            status_c = "#81C784"; status_t = "✓ OK"
        except ImportError:
            ver = "MISSING"; status_c = "#D154FF"; status_t = "✗"
        col.markdown(
            f'<div style="background:rgba(6,10,20,.85);'
            f'border:1px solid rgba(232,196,106,0.08);'
            f'border-radius:3px;padding:0.4rem;'
            f'font-family:monospace;text-align:center;">'
            f'<div style="color:#E8C46A;font-size:0.58rem;">{dep}</div>'
            f'<div style="color:{status_c};font-size:0.55rem;">{status_t}</div>'
            f'<div style="color:#5a6a80;font-size:0.48rem;">{ver}</div>'
            f'</div>', unsafe_allow_html=True)

    section_rule()

    # File system check
    st.markdown("""
    <div style="font-family:monospace;font-size:0.62rem;
                color:#3a4a60;letter-spacing:0.12em;
                text-transform:uppercase;margin-bottom:0.5rem;">
      ── FILE SYSTEM CHECK ──
    </div>""", unsafe_allow_html=True)

    files_to_check = [
        ("ENDURANCE.py",            "Frontend (this file)"),
        ("gravity_engine.py",       "Backend 1"),
        ("relativity_calculator.py","Backend 2"),
        ("planet_analyzer.py",      "Backend 3"),
        ("wormhole_navigator.py",   "Backend 4"),
        ("tesseract_decoder.py",    "Backend 5"),
        ("crew_telemetry.py",       "Backend 6"),
        ("mission_reporter.py",     "Backend 7"),
        ("bg.png",                  "Background image (optional)"),
        ("requirements.txt",        "Dependencies list"),
    ]
    fc1, fc2 = st.columns(2)
    for i, (fname, desc) in enumerate(files_to_check):
        col = fc1 if i % 2 == 0 else fc2
        exists = os.path.exists(fname)
        fsize  = f"{os.path.getsize(fname)/1e3:.0f}KB" if exists else ""
        clr3   = "#81C784" if exists else ("#FFB74D" if "optional" in desc else "#D154FF")
        with col:
            st.markdown(
                f'<div style="font-family:monospace;font-size:0.57rem;'
                f'display:flex;justify-content:space-between;'
                f'border-bottom:1px solid rgba(232,196,106,0.04);'
                f'padding:0.18rem 0;">'
                f'<span style="color:{clr3};">{"✓" if exists else "✗"} {fname}</span>'
                f'<span style="color:#5a6a80;">{fsize or desc[:20]}</span></div>',
                unsafe_allow_html=True)

    section_rule()

    # Setup instructions
    with st.expander("◈ SETUP INSTRUCTIONS — How to run INTERSTELLAR"):
        st.markdown("""
        <div class="terminal-block">
        <div class="terminal-line-gold"># Install dependencies</div>
        <div>pip install streamlit numpy pandas matplotlib scipy plotly</div>
        <br>
        <div class="terminal-line-gold"># Place all files in same directory:</div>
        <div>ENDURANCE.py          ← Frontend (run this)</div>
        <div>gravity_engine.py     ← Backend 1: Kerr BH physics</div>
        <div>relativity_calculator.py ← Backend 2: SR/GR calculations</div>
        <div>planet_analyzer.py    ← Backend 3: Habitability engine</div>
        <div>wormhole_navigator.py ← Backend 4: Wormhole physics</div>
        <div>tesseract_decoder.py  ← Backend 5: Gravity signals</div>
        <div>crew_telemetry.py     ← Backend 6: Ship systems</div>
        <div>mission_reporter.py   ← Backend 7: Mission data</div>
        <div>bg.png                ← Optional: Interstellar wallpaper</div>
        <br>
        <div class="terminal-line-gold"># Launch the app</div>
        <div>streamlit run ENDURANCE.py</div>
        <br>
        <div class="terminal-line-blue"># Optional: custom port</div>
        <div>streamlit run ENDURANCE.py --server.port 8501</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §11  BACKEND PAGE WRAPPERS — safe rendering with error handling
# ══════════════════════════════════════════════════════════════════════════════
def safe_render(page_fn, backend_mod: str, title: str,
                accent: str = "#E8C46A", icon: str = "◈"):
    """Safely call a backend page function with error handling."""
    if not BACKENDS_LOADED.get(backend_mod, False):
        page_header(title, f"Module offline: {backend_mod}.py",
                    accent="#D154FF", icon="⚠")
        backend_error_card(backend_mod, BACKEND_ERRORS.get(backend_mod, "Import failed"))
        st.markdown("""
        <div style="font-family:monospace;font-size:0.62rem;
                    color:#5a6a80;margin-top:1rem;text-align:center;">
          Ensure all backend .py files are in the same directory as ENDURANCE.py<br>
          and all dependencies are installed (see System Status page).
        </div>""", unsafe_allow_html=True)
        return

    try:
        page_fn()
    except Exception as e:
        st.error(f"Runtime error in {backend_mod}: {str(e)[:200]}")
        with st.expander("◈ Full traceback"):
            st.code(traceback.format_exc(), language="python")


# ══════════════════════════════════════════════════════════════════════════════
# §12  GLOBAL MATPLOTLIB STYLE (applied before every backend)
# ══════════════════════════════════════════════════════════════════════════════
def apply_global_mpl_style():
    plt.rcParams.update({
        "figure.facecolor":  "#04060c",
        "axes.facecolor":    "#060a14",
        "axes.edgecolor":    "#101830",
        "axes.labelcolor":   "#E8C46A",
        "axes.grid":         True,
        "grid.color":        "#0c1020",
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
        "legend.facecolor":  "#06090f",
        "legend.edgecolor":  "#101830",
        "legend.fontsize":   6,
        "figure.dpi":        110,
        "savefig.facecolor": "#04060c",
        "axes.spines.top":   False,
        "axes.spines.right": False,
    })


# ══════════════════════════════════════════════════════════════════════════════
# §13  INTERSTELLAR INTRO CRAWL (one-time welcome)
# ══════════════════════════════════════════════════════════════════════════════
def render_welcome_banner():
    """Render the top mission banner shown on all science pages."""
    S = st.session_state
    day  = S["mission_day"]
    phase_map = {
        (0, 100):   ("EARTH LAUNCH",        "#E8C46A"),
        (100, 300): ("SATURN TRANSIT",       "#4FC3F7"),
        (300, 400): ("WORMHOLE TRANSIT",     "#8060ff"),
        (400, 600): ("MILLER APPROACH",      "#4FC3F7"),
        (600, 750): ("MANN PLANET",          "#CE93D8"),
        (750,1000): ("GARGANTUA ORBIT",      "#FF8800"),
        (1000,9999):("EDMUNDS / PLAN B",     "#81C784"),
    }
    phase_name  = "UNKNOWN"
    phase_color = "#E8C46A"
    for (lo, hi), (nm, cl) in phase_map.items():
        if lo <= day < hi:
            phase_name  = nm
            phase_color = cl
            break

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,
                  rgba(232,196,106,0.06) 0%,
                  rgba(4,6,12,0.90) 100%);
                border:1px solid rgba(232,196,106,0.12);
                border-radius:4px;padding:0.5rem 1rem;
                margin-bottom:0.8rem;
                display:flex;justify-content:space-between;
                align-items:center;font-family:monospace;">
      <div style="font-size:0.58rem;color:#5a6a80;">
        <span style="color:#E8C46A;">INTERSTELLAR</span>
        &nbsp;·&nbsp;Mission Day <span style="color:#E8C46A;">{day}</span>
        &nbsp;·&nbsp;Earth Year <span style="color:#E8C46A;">{MISSION_START_YEAR}</span>
      </div>
      <div style="font-size:0.58rem;">
        Phase:&nbsp;
        <span style="color:{phase_color};font-weight:600;">{phase_name}</span>
      </div>
      <div style="font-size:0.58rem;color:#5a6a80;">
        WORMHOLE <span style="color:#81C784;">STABLE</span>
        &nbsp;·&nbsp;PLAN A <span style="color:#FF8800;">{PLAN_A_PCT:.0f}%</span>
        &nbsp;·&nbsp;TARS <span style="color:#81C784;">NOMINAL</span>
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# §14  MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main():
    init_global_state()
    S = st.session_state

    # Inject master CSS
    st.markdown(MASTER_CSS, unsafe_allow_html=True)

    # Background image
    if S["show_bg"]:
        if S.get("bg_image_b64") is None:
            S["bg_image_b64"] = load_background()
        inject_background(S.get("bg_image_b64"))

    # Boot sequence (first visit)
    if not S["boot_done"]:
        render_boot_sequence()
        return

    # Render sidebar
    render_sidebar()

    # Apply global matplotlib style
    apply_global_mpl_style()

    # Welcome banner (on all science pages)
    page = S["page"]
    if page not in ("overview", "system"):
        render_welcome_banner()

    # ── Route to page ──────────────────────────────────────────────────────
    if page == "overview":
        render_overview()

    elif page == "gravity":
        safe_render(
            gravity_engine_page,
            "gravity_engine",
            "GRAVITY ENGINE",
            accent="#FF8800", icon="⬡"
        )

    elif page == "relativity":
        safe_render(
            relativity_calculator_page,
            "relativity_calculator",
            "RELATIVITY CALCULATOR",
            accent="#4FC3F7", icon="⏱"
        )

    elif page == "planets":
        safe_render(
            planet_analyzer_page,
            "planet_analyzer",
            "PLANET SCANNER",
            accent="#81C784", icon="🪐"
        )

    elif page == "wormhole":
        safe_render(
            wormhole_navigator_page,
            "wormhole_navigator",
            "WORMHOLE NAVIGATOR",
            accent="#8060ff", icon="⟳"
        )

    elif page == "tesseract":
        safe_render(
            tesseract_decoder_page,
            "tesseract_decoder",
            "TESSERACT DECODER",
            accent="#c040ff", icon="◈"
        )

    elif page == "crew":
        safe_render(
            crew_telemetry_page,
            "crew_telemetry",
            "CREW TELEMETRY",
            accent="#81C784", icon="⛨"
        )

    elif page == "mission":
        safe_render(
            mission_reporter_page,
            "mission_reporter",
            "MISSION REPORTER",
            accent="#FFD700", icon="▤"
        )

    elif page == "system":
        render_system_status()

    else:
        st.error(f"Unknown page: {page}")
        S["page"] = "overview"
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# §15  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
