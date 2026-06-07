import streamlit as st
import base64
import html
import re
from pathlib import Path

st.set_page_config(
    page_title="AI-MV PDCA Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
:root {
    --bg: #020617;
    --panel: rgba(15, 23, 42, 0.90);
    --panel2: rgba(30, 41, 59, 0.82);
    --border: rgba(148, 163, 184, 0.22);
    --text: #F8FAFC;
    --muted: #CBD5E1;
    --blue: #38BDF8;
    --red: #EF4444;
    --youtube: #FF0033;
    --green: #22C55E;
    --yellow: #F59E0B;
    --pink: #F472B6;
    --white: #FFFFFF;
    --ink: #020617;
}

.stApp {
    position: relative;
    background:
        radial-gradient(circle at 8% 0%, rgba(56,189,248,0.22), transparent 30%),
        radial-gradient(circle at 94% 4%, rgba(255,0,51,0.20), transparent 31%),
        linear-gradient(135deg, #020617 0%, #0F172A 48%, #111827 100%) !important;
    overflow-x: hidden;
}

/* Animated ambient background: subtle heartbeat-like gradient glows */
.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    inset: -12%;
    pointer-events: none;
    z-index: 0;
    opacity: 0.60;
    filter: blur(2px);
    will-change: transform, opacity, background-position;
}

.stApp::before {
    background:
        radial-gradient(circle at 16% 20%, rgba(56,189,248,0.24), transparent 15%),
        radial-gradient(circle at 78% 16%, rgba(255,0,51,0.18), transparent 14%),
        radial-gradient(circle at 64% 72%, rgba(168,85,247,0.16), transparent 16%),
        radial-gradient(circle at 22% 82%, rgba(34,197,94,0.12), transparent 13%);
    animation: ambientPulseA 9.5s ease-in-out infinite;
}

.stApp::after {
    background:
        radial-gradient(circle at 42% 28%, rgba(244,114,182,0.12), transparent 13%),
        radial-gradient(circle at 88% 70%, rgba(56,189,248,0.18), transparent 16%),
        radial-gradient(circle at 10% 58%, rgba(245,158,11,0.10), transparent 12%);
    animation: ambientPulseB 13s ease-in-out infinite;
    animation-delay: -4.2s;
    opacity: 0.55;
}

@keyframes ambientPulseA {
    0%, 100% {
        transform: scale(1) translate3d(0, 0, 0);
        opacity: 0.54;
        background-position: 0% 0%;
    }
    18% {
        transform: scale(1.025) translate3d(1.2%, -0.6%, 0);
        opacity: 0.76;
    }
    41% {
        transform: scale(0.995) translate3d(-0.8%, 0.8%, 0);
        opacity: 0.50;
    }
    63% {
        transform: scale(1.04) translate3d(0.6%, 1%, 0);
        opacity: 0.82;
    }
}

@keyframes ambientPulseB {
    0%, 100% {
        transform: scale(1) translate3d(0, 0, 0) rotate(0deg);
        opacity: 0.42;
    }
    24% {
        transform: scale(1.035) translate3d(-1%, 0.7%, 0) rotate(0.4deg);
        opacity: 0.64;
    }
    52% {
        transform: scale(0.99) translate3d(1.1%, -0.8%, 0) rotate(-0.25deg);
        opacity: 0.38;
    }
    79% {
        transform: scale(1.05) translate3d(0.4%, 0.5%, 0) rotate(0.15deg);
        opacity: 0.70;
    }
}



/* Keep every Streamlit UI element above the animated background layer */
.stApp > * {
    position: relative;
    z-index: 1;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.block-container {
    position: relative;
    z-index: 2;
}

[data-testid="stHeader"] {
    background: transparent !important;
    position: relative;
    z-index: 3;
}

@media (prefers-reduced-motion: reduce) {
    .stApp::before,
    .stApp::after {
        animation: none !important;
        opacity: 0.42;
    }
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4, p, span, label, .stMarkdown, li {
    color: var(--text) !important;
}

p, li {
    line-height: 1.85;
}

b, strong {
    color: var(--pink) !important;
}

/* =========================
   Streamlit basic widgets
   ========================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 22px !important;
    padding: 22px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.32) !important;
}

.stNumberInput input, .stTextInput input, .stTextArea textarea {
    background-color: #F8FAFC !important;
    color: #020617 !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 700 !important;
}

.stTextArea textarea {
    min-height: 92px;
}

/* Selectbox / popover visibility fix */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div {
    background: #F8FAFC !important;
    color: #020617 !important;
    border: 1px solid rgba(148,163,184,0.45) !important;
    border-radius: 12px !important;
    min-height: 46px !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
div[data-baseweb="select"] *,
div[data-baseweb="popover"] *,
ul[role="listbox"] *,
li[role="option"] * {
    color: #020617 !important;
    fill: #020617 !important;
}

div[data-baseweb="popover"],
ul[role="listbox"],
li[role="option"] {
    background: #F8FAFC !important;
    color: #020617 !important;
}

li[role="option"] {
    white-space: normal !important;
    line-height: 1.55 !important;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
}

/* Multiselect tags are not used, but keep this just in case */
.stMultiSelect [data-baseweb="tag"] {
    height: auto !important;
    min-height: 36px !important;
    max-width: 100% !important;
    white-space: normal !important;
    align-items: flex-start !important;
    border-radius: 10px !important;
    padding: 7px 10px !important;
    margin: 4px 6px 4px 0 !important;
}
.stMultiSelect [data-baseweb="tag"] span {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.45 !important;
    color: #020617 !important;
}

div[data-testid="stSlider"] {
    background: rgba(15,23,42,0.68) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 16px 22px 22px !important;
}

button[kind="secondary"], .stDownloadButton button {
    border-radius: 999px !important;
    font-weight: 900 !important;
}

/* Checkbox / radio: long label wrapping */
.stCheckbox label,
.stRadio label {
    align-items: flex-start !important;
}
.stCheckbox label p,
.stRadio label p {
    color: #F8FAFC !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.65 !important;
    font-size: 15px !important;
}
.stCheckbox, .stRadio {
    margin-bottom: 4px !important;
}

/* =========================
   Tabs: straight lower corners + aligned underline
   ========================= */
div[data-testid="stTabs"] [role="tablist"] {
    display: flex !important;
    align-items: flex-end !important;
    gap: 0 !important;
    border-bottom: 2px solid rgba(148, 163, 184, 0.28) !important;
    margin-bottom: 22px !important;
}

div[data-testid="stTabs"] button,
div[data-testid="stTabs"] [role="tab"] {
    background: rgba(15, 23, 42, 0.72) !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    border-bottom: 0 !important;
    border-radius: 14px 14px 0 0 !important; /* lower corners are straight */
    padding: 12px 20px !important;
    margin: 0 6px 0 0 !important;
    font-weight: 900 !important;
    box-shadow: none !important;
}

div[data-testid="stTabs"] button[aria-selected="true"],
div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #FF0033, #FF5A5F) !important;
    color: white !important;
    border-color: rgba(255,255,255,0.20) !important;
    border-bottom: 2px solid #FF5A5F !important;
    margin-bottom: -2px !important;
    box-shadow: 0 10px 32px rgba(255, 0, 51, 0.28) !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-highlight-bar"] {
    display: none !important;
}

/* =========================
   Navigation: stable button tab UI
   ========================= */
.nav-button-note {
    color: var(--muted) !important;
    font-size: 12px;
    margin: -6px 0 8px;
}

/* =========================
   V47: zero-padding external header image
   Rendered via a plain HTML img tag instead of st.image()
   ========================= */
.header-image-wrap {
    margin: -2px 0 8px 0 !important;
    padding: 0 !important;
    line-height: 0 !important;
    font-size: 0 !important;
    display: block !important;
    width: 100% !important;
}

.header-image-wrap img {
    display: block !important;
    width: 100% !important;
    height: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    vertical-align: top !important;
    border-radius: 5px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    box-shadow: 0 14px 34px rgba(0,0,0,0.24) !important;
    box-sizing: border-box !important;
}

/* Keep Streamlit's own image wrapper neutral if it appears elsewhere */
div[data-testid="stImage"],
div[data-testid="stImageContainer"] {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    line-height: 0 !important;
}

.nav-tabbar-separator {
    margin-top: 8px !important;
}

.nav-tabbar-separator {
    height: 2px;
    background: rgba(148, 163, 184, 0.30);
    margin: -2px 0 24px;
}

/* Navigation buttons are rendered with st.button. This avoids URL links and radio/checkbox UI. */
div[data-testid="stButton"] > button {
    min-height: 48px !important;
    border-radius: 9px 9px 0 0 !important;
    border: 1px solid rgba(148, 163, 184, 0.24) !important;
    border-bottom: 0 !important;
    background: rgba(15, 23, 42, 0.78) !important;
    color: #CBD5E1 !important;
    font-weight: 900 !important;
    box-shadow: none !important;
    white-space: normal !important;
    line-height: 1.35 !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(255,0,51,0.96), rgba(255,90,95,0.96)) !important;
    color: #FFFFFF !important;
    border-color: rgba(255,255,255,0.24) !important;
    box-shadow: 0 12px 34px rgba(255, 0, 51, 0.30) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px);
    border-color: rgba(255,255,255,0.28) !important;
}

@media (max-width: 760px) {
    .nav-tabbar-separator {
        display: none;
    }
    div[data-testid="stButton"] > button {
        border-radius: 8px !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.24) !important;
        margin-bottom: 6px !important;
    }
}



/* Navigation label refinement: image header matching style */
div[data-testid="stButton"] > button {
    min-height: 54px !important;
    letter-spacing: 0.035em !important;
    font-size: 14px !important;
    text-transform: none !important;
    background:
        linear-gradient(180deg, rgba(31,41,55,0.96), rgba(15,23,42,0.92)) !important;
    border-color: rgba(255,255,255,0.14) !important;
    color: #E5E7EB !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background:
        linear-gradient(135deg, rgba(255,0,0,0.98), rgba(185,28,28,0.96)) !important;
    color: #FFFFFF !important;
    border-color: rgba(255,255,255,0.20) !important;
    box-shadow: 0 10px 24px rgba(255,0,0,0.22) !important;
}
div[data-testid="stButton"] > button p {
    font-weight: 950 !important;
    color: inherit !important;
    margin: 0 !important;
    line-height: 1.25 !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: rgba(255,255,255,0.30) !important;
    filter: brightness(1.06);
}

/* Metrics */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(56,189,248,0.16), rgba(255,255,255,0.04));
    border: 1px solid rgba(56,189,248,0.25);
    padding: 18px;
    border-radius: 18px;
}
div[data-testid="stMetricLabel"] p { color: var(--muted) !important; }
div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; }

/* =========================
   Original UI components
   ========================= */
.hero {
    text-align: center;
    padding: 36px 22px 30px;
    border-radius: 30px;
    background: linear-gradient(135deg, rgba(255,0,51,0.18), rgba(56,189,248,0.12));
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 24px 80px rgba(0,0,0,0.35);
    margin-bottom: 28px;
}
.hero-kicker {
    font-size: 13px;
    color: var(--muted) !important;
    font-weight: 900;
    letter-spacing: 0.16em;
}
.hero h1, .hero-title {
    margin: 8px 0 8px;
    font-size: 2.5rem;
    letter-spacing: -0.04em;
    font-weight: 900;
    color: #FFFFFF !important;
}
.hero p { color: #CBD5E1 !important; margin-bottom: 0; }

/* Header image loaded as an external PNG file */
div[data-testid="stImage"] img {
    border-radius: 5px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    box-shadow: 0 18px 42px rgba(0,0,0,0.28) !important;
}
.header-image-note {
    margin-bottom: 24px;
}

.section-heading {
    position: relative;
    font-size: 20px !important;
    font-weight: 900 !important;
    letter-spacing: -0.01em;
    background:
        linear-gradient(135deg, rgba(56,189,248,0.18), rgba(255,0,51,0.08)),
        rgba(15,23,42,0.72) !important;
    border: 1px solid rgba(148,163,184,0.18) !important;
    border-left: 0 !important;
    padding: 15px 18px 15px 22px !important;
    margin-top: 24px !important;
    margin-bottom: 14px !important;
    border-radius: 18px !important;
    box-shadow: 0 14px 36px rgba(0,0,0,0.24);
    overflow: hidden;
}
.section-heading::before {
    content: "";
    position: absolute;
    left: 0;
    top: 10px;
    bottom: 10px;
    width: 6px;
    border-radius: 999px;
    background: linear-gradient(180deg, var(--blue), var(--youtube));
}
.section-heading::after {
    content: "";
    position: absolute;
    right: -40px;
    top: -40px;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: rgba(56,189,248,0.08);
}

.advice-card {
    background: var(--panel);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 24px;
    padding: 24px;
    margin: 24px 0;
    box-shadow: 0 18px 50px rgba(0,0,0,0.32);
    overflow: visible !important;
}
.advice-kicker {
    color: var(--blue) !important;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 0.14em;
    margin-bottom: 6px;
}
.advice-title {
    color: #FFFFFF !important;
    font-size: 22px;
    line-height: 1.45;
    font-weight: 900;
    letter-spacing: -0.02em;
    margin: 0 0 16px 0;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.result-badge {
    padding: 14px 16px;
    border-radius: 15px;
    font-weight: 900;
    margin: 14px 0 20px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.28);
    overflow-wrap: anywhere;
}
.success { background: linear-gradient(135deg, #22C55E, #047857); }
.warning { background: linear-gradient(135deg, #F59E0B, #B45309); }
.danger { background: linear-gradient(135deg, #EF4444, #991B1B); }
.neutral { background: linear-gradient(135deg, #64748B, #334155); }
.legendary { background: linear-gradient(135deg, #A855F7, #FF0033); }

.diagnosis-section {
    margin-top: 18px;
    padding: 2px 0 2px 16px;
    border-left: 4px solid rgba(56,189,248,0.78);
}
.section-label {
    display: inline-block;
    color: var(--pink) !important;
    font-weight: 900;
    margin-bottom: 6px;
}
.diagnosis-section ul,
ul.clean-list {
    margin: 8px 0 0 0 !important;
    padding-left: 22px !important;
    list-style-position: outside !important;
}
.diagnosis-section li,
ul.clean-list li {
    margin-bottom: 8px !important;
    overflow-wrap: break-word !important;
}

.alert-highlight {
    background: rgba(239, 68, 68, 0.14) !important;
    border: 1px solid rgba(239, 68, 68, 0.45) !important;
    border-radius: 14px !important;
    padding: 14px 16px !important;
    color: #FEE2E2 !important;
    font-weight: 800;
    margin-top: 18px;
}

.mission-box {
    background: linear-gradient(135deg, rgba(56,189,248,0.16), rgba(255,0,51,0.10));
    border: 1px solid rgba(56,189,248,0.30);
    border-radius: 22px;
    padding: 22px;
    margin: 22px 0;
    overflow: visible !important;
}

/* Stylish status dashboard cards */
.status-panel {
    position: relative;
    background:
        linear-gradient(135deg, rgba(56,189,248,0.10), rgba(255,0,51,0.07)),
        rgba(15,23,42,0.76);
    border: 1px solid rgba(148,163,184,0.24);
    border-radius: 10px;
    padding: 16px;
    margin: 16px 0 22px;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    overflow: visible !important;
    box-shadow: 0 16px 44px rgba(0,0,0,0.24), 0 0 0 1px rgba(255,255,255,0.03) inset;
}
.status-panel-header {
    grid-column: 1 / -1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 2px 2px 4px;
}
.status-panel-title {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-weight: 900;
    font-size: 15px;
    letter-spacing: 0.03em;
    color: #FFFFFF !important;
}
.status-panel-title::before {
    content: "";
    width: 9px;
    height: 9px;
    background: linear-gradient(135deg, var(--blue), var(--youtube));
    border-radius: 2px;
    box-shadow: 0 0 16px rgba(56,189,248,0.55);
}
.status-panel-subtitle {
    color: var(--muted) !important;
    font-size: 12px;
    font-weight: 800;
    white-space: nowrap;
}
.status-item {
    position: relative;
    background:
        linear-gradient(135deg, rgba(255,255,255,0.09), rgba(255,255,255,0.035)),
        rgba(15,23,42,0.55);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 8px;
    padding: 15px 15px 14px;
    min-width: 0;
    width: 100%;
    box-sizing: border-box;
    overflow: hidden !important;
    display: grid;
    grid-template-columns: 38px minmax(0, 1fr);
    gap: 12px;
    align-items: start;
}
.status-item::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: var(--blue);
    opacity: 0.95;
}
.status-item::after {
    content: "";
    position: absolute;
    right: -26px;
    top: -26px;
    width: 72px;
    height: 72px;
    background: rgba(255,255,255,0.045);
    transform: rotate(18deg);
}
.status-icon {
    position: relative;
    z-index: 1;
    width: 34px;
    height: 34px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 7px;
    font-size: 18px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18);
}
.status-content {
    position: relative;
    z-index: 1;
    min-width: 0;
}
.status-label {
    color: var(--muted) !important;
    font-weight: 900;
    font-size: 12px;
    letter-spacing: 0.08em;
    margin-bottom: 5px;
    text-transform: uppercase;
}
.status-value {
    color: #FFFFFF !important;
    font-weight: 900;
    font-size: 18px;
    line-height: 1.55;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
    max-width: 100%;
}
.status-item-small .status-value {
    font-size: 17px;
}
.status-item-problem {
    grid-column: 1 / -1;
    border: 1px solid rgba(255,0,51,0.32);
    background:
        linear-gradient(135deg, rgba(255,0,51,0.16), rgba(56,189,248,0.07)),
        rgba(15,23,42,0.68);
}
.status-item-problem::before {
    background: linear-gradient(180deg, var(--youtube), var(--yellow));
}
.status-item-problem .status-value {
    font-size: 16px;
    line-height: 1.75;
    font-weight: 800;
}
.status-youtube::before { background: #FF0033; }
.status-external::before { background: #38BDF8; }
.status-ctr::before { background: #F472B6; }
.status-retention::before { background: #A855F7; }
.status-views::before { background: #22C55E; }
.status-warning::before { background: #F59E0B; }

.action-list-box {
    background:
        linear-gradient(135deg, rgba(34,197,94,0.18), rgba(56,189,248,0.10)),
        rgba(15,23,42,0.82);
    border: 1px solid rgba(34,197,94,0.35);
    border-left: 6px solid var(--green);
    border-radius: 20px;
    padding: 18px 20px;
    margin-top: 16px;
    margin-bottom: 10px;
    box-shadow: 0 16px 42px rgba(0,0,0,0.26), 0 0 0 1px rgba(255,255,255,0.03) inset;
    overflow: visible !important;
}
.action-list-title {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #FFFFFF !important;
    font-weight: 900;
    font-size: 15px;
    letter-spacing: 0.02em;
    background: rgba(34,197,94,0.18);
    border: 1px solid rgba(34,197,94,0.36);
    border-radius: 999px;
    padding: 7px 12px;
    margin-bottom: 12px;
}
.action-list-box ul {
    margin: 8px 0 0 0 !important;
    padding-left: 0 !important;
    list-style: none !important;
}
.action-list-box li {
    position: relative;
    margin-bottom: 9px;
    padding: 10px 12px 10px 38px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    white-space: normal !important;
    overflow-wrap: break-word !important;
    line-height: 1.65;
}
.action-list-box li::before {
    content: "✓";
    position: absolute;
    left: 13px;
    top: 10px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--green);
    color: #052E16;
    font-size: 12px;
    font-weight: 900;
}

/* V9: grouped checkbox headings and selected summaries */
.group-heading {
    margin: 18px 0 8px;
    padding: 12px 14px;
    border-radius: 8px 8px 0 0;
    background:
        linear-gradient(135deg, rgba(56,189,248,0.16), rgba(255,0,51,0.07)),
        rgba(15,23,42,0.74);
    border: 1px solid rgba(148,163,184,0.18);
    border-bottom: 0;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
}
.group-title {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #FFFFFF !important;
    font-size: 15px;
    font-weight: 900;
    letter-spacing: 0.02em;
}
.group-desc {
    color: #CBD5E1 !important;
    font-size: 12px;
    font-weight: 700;
    margin-top: 4px;
    line-height: 1.6;
}
.selected-group {
    margin-top: 12px;
    padding: 12px 14px;
    border-radius: 8px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.08);
}
.selected-group-title {
    color: #FFFFFF !important;
    font-size: 13px;
    font-weight: 900;
    margin-bottom: 8px;
}
.selected-group ul {
    margin: 0 !important;
    padding-left: 0 !important;
    list-style: none !important;
}
.selected-group li {
    position: relative;
    padding: 7px 8px 7px 26px;
    margin-bottom: 6px;
    border-radius: 6px;
    background: rgba(15,23,42,0.48);
    line-height: 1.65;
}
.selected-group li::before {
    content: "✓";
    position: absolute;
    left: 8px;
    top: 7px;
    color: var(--green);
    font-weight: 900;
}


.sub-heading {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 17px;
    font-weight: 900;
    color: #FFFFFF !important;
    margin: 4px 0 14px;
    padding: 11px 13px;
    border-left: 4px solid var(--blue);
    background: rgba(255,255,255,0.055);
    border-radius: 7px;
    letter-spacing: -0.01em;
}
.sub-heading .sub-heading-kicker {
    display: inline-flex;
    width: 8px;
    height: 8px;
    border-radius: 2px;
    background: linear-gradient(135deg, var(--blue), var(--youtube));
    box-shadow: 0 0 14px rgba(56,189,248,0.45);
    flex: 0 0 auto;
}

.small-note {
    color: var(--muted) !important;
    font-size: 13px;
    margin: 10px 0 0 !important;
}

@media (max-width: 720px) {
    .status-panel {
        padding: 14px;
        gap: 10px;
    }
    .status-item {
        padding: 13px 14px;
    }
    .hero h1 { font-size: 2rem; }
}

/* =========================
   V6: subtle radius tuning
   角丸を控えめにし、section-headingは下角を直線化
   ========================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 10px !important;
}

.stNumberInput input,
.stTextInput input,
.stTextArea textarea,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div {
    border-radius: 7px !important;
}

.stMultiSelect [data-baseweb="tag"] {
    border-radius: 6px !important;
}

div[data-testid="stSlider"] {
    border-radius: 10px !important;
}

button[kind="secondary"],
.stDownloadButton button {
    border-radius: 8px !important;
}

/* keep navigation buttons tab-like after global button radius override */
div[data-testid="stButton"] > button {
    border-radius: 9px 9px 0 0 !important;
}

div[data-testid="stTabs"] button,
div[data-testid="stTabs"] [role="tab"] {
    border-radius: 8px 8px 0 0 !important;
}

div[data-testid="stMetric"] {
    border-radius: 10px !important;
}

.hero {
    border-radius: 14px !important;
}

.section-heading {
    border-radius: 10px 10px 0 0 !important;
    margin-top: 18px !important;
    margin-bottom: -1px !important;
    padding: 14px 18px 14px 22px !important;
    border-bottom: 0 !important;
    box-shadow: 0 10px 28px rgba(0,0,0,0.18) !important;
    z-index: 2;
}

.section-heading::before {
    top: 0 !important;
    bottom: 0 !important;
    border-radius: 0 !important;
}

.section-heading::after {
    width: 86px !important;
    height: 86px !important;
    border-radius: 0 !important;
    opacity: 0.55;
}

.advice-card,
.mission-box,
.status-panel,
.action-list-box {
    border-radius: 10px !important;
}

.status-item,
.result-badge,
.alert-highlight,
.action-list-box li {
    border-radius: 8px !important;
}

.action-list-title {
    border-radius: 8px !important;
}

.action-list-box li::before {
    border-radius: 4px !important;
}

/* V8: status panel responsive polish */
@media (max-width: 820px) {
    .status-panel {
        grid-template-columns: 1fr !important;
    }
    .status-panel-header {
        flex-direction: column;
        align-items: flex-start;
    }
    .status-panel-subtitle {
        white-space: normal;
    }
}




/* V23: free-form Plan input note */
.learning-note-box {
    background:
        linear-gradient(135deg, rgba(56,189,248,0.13), rgba(255,255,255,0.035)),
        rgba(15,23,42,0.72);
    border: 1px solid rgba(56,189,248,0.28);
    border-left: 5px solid var(--blue);
    border-radius: 10px;
    padding: 14px 16px;
    margin: 10px 0 16px;
    color: #E2E8F0 !important;
    line-height: 1.85;
}
.free-plan-box {
    background:
        linear-gradient(135deg, rgba(56,189,248,0.16), rgba(168,85,247,0.08)),
        rgba(15,23,42,0.82) !important;
    border-color: rgba(56,189,248,0.32) !important;
    border-left-color: var(--blue) !important;
}
.free-plan-box .action-list-title {
    background: rgba(56,189,248,0.16) !important;
    border-color: rgba(56,189,248,0.34) !important;
}
.free-plan-box li::before {
    content: "✎";
    background: var(--blue);
    color: #082F49;
}


/* V24: Check結果連動のおすすめ改善アクション */
.recommend-panel {
    background:
        linear-gradient(135deg, rgba(255,0,51,0.13), rgba(56,189,248,0.10)),
        rgba(15,23,42,0.86);
    border: 1px solid rgba(148,163,184,0.22);
    border-left: 5px solid var(--youtube);
    border-radius: 10px;
    padding: 18px 18px 16px;
    margin: 8px 0 22px;
    box-shadow: 0 16px 42px rgba(0,0,0,0.22);
}
.recommend-kicker {
    color: #93C5FD !important;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 0.12em;
    margin-bottom: 6px;
}
.recommend-title {
    color: #FFFFFF !important;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 8px;
}
.recommend-reason {
    color: #CBD5E1 !important;
    font-size: 14px;
    line-height: 1.8;
    margin-bottom: 14px;
}
.recommend-card-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    margin-top: 12px;
}
.recommend-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    border-left: 4px solid rgba(56,189,248,0.75);
    border-radius: 8px;
    padding: 12px 13px;
}
.recommend-card.high {
    border-left-color: var(--youtube);
    background: linear-gradient(135deg, rgba(255,0,51,0.14), rgba(255,255,255,0.045));
}
.recommend-card.medium {
    border-left-color: var(--yellow);
}
.recommend-badge {
    display: inline-block;
    color: #020617 !important;
    background: #F8FAFC;
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 900;
    margin-bottom: 7px;
}
.recommend-card.high .recommend-badge {
    background: #FCA5A5;
}
.recommend-card.medium .recommend-badge {
    background: #FCD34D;
}
.recommend-action-title {
    color: #FFFFFF !important;
    font-weight: 900;
    line-height: 1.55;
    margin-bottom: 5px;
}
.recommend-action-reason {
    color: #CBD5E1 !important;
    font-size: 13px;
    line-height: 1.65;
}
.action-choice-note {
    background: rgba(56,189,248,0.10);
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: 8px;
    padding: 12px 14px;
    margin: 12px 0 18px;
    color: #E0F2FE !important;
    line-height: 1.75;
}
@media (max-width: 820px) {
    .recommend-card-grid {
        grid-template-columns: 1fr;
    }
}


/* =========================
   V25: YouTube palette + subtle radius + focus visibility polish
   ========================= */
:root {
    --blue: #FF0033;
    --youtube: #FF0000;
    --yt-red: #FF0000;
    --yt-red-soft: #FF4B4B;
    --yt-dark: #0F0F0F;
    --yt-panel: rgba(18, 18, 18, 0.86);
    --yt-panel2: rgba(33, 33, 33, 0.78);
    --pink: #FF6B6B;
    --muted: #CFCFCF;
}

.stApp {
    background:
        radial-gradient(circle at 10% 4%, rgba(255,0,0,0.18), transparent 28%),
        radial-gradient(circle at 92% 8%, rgba(255,255,255,0.055), transparent 30%),
        radial-gradient(circle at 68% 78%, rgba(255,75,75,0.11), transparent 28%),
        linear-gradient(135deg, #050505 0%, #0F0F0F 48%, #181818 100%) !important;
}
.stApp::before {
    background:
        radial-gradient(circle at 16% 20%, rgba(255,0,0,0.20), transparent 15%),
        radial-gradient(circle at 78% 16%, rgba(255,75,75,0.15), transparent 14%),
        radial-gradient(circle at 64% 72%, rgba(255,255,255,0.055), transparent 16%),
        radial-gradient(circle at 22% 82%, rgba(255,0,0,0.08), transparent 13%) !important;
}
.stApp::after {
    background:
        radial-gradient(circle at 42% 28%, rgba(255,255,255,0.045), transparent 13%),
        radial-gradient(circle at 88% 70%, rgba(255,0,0,0.13), transparent 16%),
        radial-gradient(circle at 10% 58%, rgba(255,75,75,0.08), transparent 12%) !important;
}

/* さりげない角丸へ統一 */
div[data-testid="stVerticalBlockBorderWrapper"],
.advice-card,
.mission-box,
.status-panel,
.status-item,
.action-list-box,
.selected-group,
.recommend-panel,
.recommend-card,
.learning-note-box,
.free-plan-box,
.action-choice-note,
.alert-highlight,
.group-heading,
.result-badge,
div[data-testid="stMetric"],
div[data-testid="stSlider"] {
    border-radius: 5px !important;
}
.hero {
    border-radius: 6px !important;
    background:
        linear-gradient(135deg, rgba(255,0,0,0.20), rgba(255,255,255,0.045)),
        rgba(15,15,15,0.72) !important;
}
.stNumberInput input,
.stTextInput input,
.stTextArea textarea,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div,
.action-list-title,
.recommend-badge,
.status-icon,
.action-list-box li,
.selected-group li,
.stMultiSelect [data-baseweb="tag"] {
    border-radius: 5px !important;
}
.action-list-box li::before {
    border-radius: 3px !important;
}
button[kind="secondary"],
.stDownloadButton button {
    border-radius: 5px !important;
}
div[data-testid="stButton"] > button,
div[data-testid="stTabs"] button,
div[data-testid="stTabs"] [role="tab"] {
    border-radius: 5px 5px 0 0 !important;
}

/* 入力中フォームをわかりやすく */
.stNumberInput input,
.stTextInput input,
.stTextArea textarea {
    border: 1px solid rgba(255,255,255,0.22) !important;
    transition: box-shadow 0.18s ease, border-color 0.18s ease, transform 0.18s ease !important;
}
.stNumberInput input:focus,
.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus-visible,
.stTextInput input:focus-visible,
.stTextArea textarea:focus-visible {
    border: 2px solid var(--yt-red) !important;
    outline: none !important;
    box-shadow:
        0 0 0 4px rgba(255,0,0,0.20),
        0 0 28px rgba(255,0,0,0.18) !important;
    background: #FFFFFF !important;
    transform: translateY(-1px);
}
div[data-baseweb="select"] > div:focus-within,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border: 2px solid var(--yt-red) !important;
    box-shadow: 0 0 0 4px rgba(255,0,0,0.18) !important;
}
.stCheckbox:focus-within,
.stRadio:focus-within {
    background: rgba(255,0,0,0.075) !important;
    outline: 1px solid rgba(255,0,0,0.24) !important;
    border-radius: 5px !important;
    padding: 2px 6px !important;
}
div[data-testid="stSlider"]:focus-within {
    border-color: rgba(255,0,0,0.50) !important;
    box-shadow: 0 0 0 3px rgba(255,0,0,0.12) !important;
}

/* section-heading：上だけ控えめ角丸、下は直線で接続感 */
.section-heading {
    border-radius: 5px 5px 0 0 !important;
    margin-top: 14px !important;
    margin-bottom: -1px !important;
    padding: 13px 16px !important;
    background:
        linear-gradient(135deg, rgba(255,0,0,0.20), rgba(255,255,255,0.035)),
        rgba(15,15,15,0.78) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-bottom: 0 !important;
    box-shadow: 0 10px 24px rgba(0,0,0,0.22) !important;
}
.section-heading::before {
    top: 0 !important;
    bottom: 0 !important;
    width: 4px !important;
    background: var(--yt-red) !important;
    border-radius: 0 !important;
}
.section-heading::after {
    background: rgba(255,0,0,0.08) !important;
    border-radius: 0 !important;
}

/* sub-heading：kickerを消し、アイコンと文字を読みやすく */
.sub-heading {
    gap: 0 !important;
    padding: 10px 12px !important;
    border-left: 0 !important;
    border-top: 2px solid rgba(255,0,0,0.66) !important;
    border-radius: 5px 5px 0 0 !important;
    background:
        linear-gradient(135deg, rgba(255,0,0,0.12), rgba(255,255,255,0.035)),
        rgba(18,18,18,0.72) !important;
}
.sub-heading .sub-heading-kicker {
    display: none !important;
}

/* border-leftの重なりを減らし、YouTube赤系の控えめアクセントへ */
.diagnosis-section,
.learning-note-box,
.free-plan-box,
.recommend-card,
.action-list-box,
.recommend-panel {
    border-left: 0 !important;
}
.diagnosis-section {
    padding-left: 0 !important;
    border-top: 2px solid rgba(255,0,0,0.48) !important;
    padding-top: 12px !important;
}
.learning-note-box,
.free-plan-box,
.recommend-panel,
.action-list-box {
    box-shadow:
        inset 4px 0 0 rgba(255,0,0,0.68),
        0 14px 34px rgba(0,0,0,0.20) !important;
}
.recommend-card {
    box-shadow: inset 4px 0 0 rgba(255,0,0,0.58) !important;
}
.recommend-card.medium {
    box-shadow: inset 4px 0 0 rgba(255,193,7,0.70) !important;
}
.recommend-card.high {
    box-shadow: inset 4px 0 0 var(--yt-red) !important;
}

/* YouTubeカラーへ統一：青系アクセントを赤/白/グレーへ */
.status-panel,
.mission-box,
.free-plan-box,
.learning-note-box,
.action-choice-note,
.group-heading {
    background:
        linear-gradient(135deg, rgba(255,0,0,0.12), rgba(255,255,255,0.035)),
        rgba(15,15,15,0.78) !important;
    border-color: rgba(255,255,255,0.12) !important;
}
.status-panel-title::before {
    background: var(--yt-red) !important;
    box-shadow: 0 0 14px rgba(255,0,0,0.48) !important;
}
.status-item::before,
.status-youtube::before,
.status-external::before,
.status-ctr::before,
.status-retention::before,
.status-views::before {
    background: var(--yt-red) !important;
    border-radius: 0 !important;
}
.status-warning::before { background: #F59E0B !important; }
.status-item-problem::before { background: linear-gradient(180deg, var(--yt-red), #FF4B4B) !important; }
.status-icon {
    background: rgba(255,0,0,0.12) !important;
    border-color: rgba(255,0,0,0.22) !important;
}
.status-item-problem {
    background:
        linear-gradient(135deg, rgba(255,0,0,0.17), rgba(255,255,255,0.035)),
        rgba(15,15,15,0.74) !important;
    border-color: rgba(255,0,0,0.32) !important;
}
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,0,0,0.14), rgba(255,255,255,0.04)) !important;
    border-color: rgba(255,0,0,0.25) !important;
}
.group-heading {
    border-bottom: 0 !important;
}
.action-list-title,
.free-plan-box .action-list-title {
    background: rgba(255,0,0,0.14) !important;
    border-color: rgba(255,0,0,0.30) !important;
    border-radius: 5px !important;
}
.action-list-box li::before,
.free-plan-box li::before {
    background: var(--yt-red) !important;
    color: #FFFFFF !important;
}
.recommend-kicker,
.advice-kicker {
    color: #FFB4B4 !important;
}

.advice-title {
    color: #FFFFFF !important;
    font-size: 21px !important;
    line-height: 1.45 !important;
    font-weight: 900 !important;
    letter-spacing: -0.02em !important;
    margin: 2px 0 14px 0 !important;
    padding: 0 0 12px 0 !important;
    border-bottom: 1px solid rgba(255,255,255,0.10) !important;
}
.action-choice-note {
    color: #FFE4E4 !important;
}

/* lower-corner straightness for connected heading/content blocks */
.section-heading + div[data-testid="stVerticalBlockBorderWrapper"],
.section-heading + .status-panel,
.section-heading + .advice-card {
    border-top-left-radius: 0 !important;
    border-top-right-radius: 0 !important;
}

/* V27: section-heading を advice-kicker 系の二段見出しに調整 */
.section-heading {
    display: block !important;
    position: relative !important;
    padding: 12px 16px 13px 18px !important;
    min-height: auto !important;
}
.section-heading-inner {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.section-kicker {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    width: fit-content;
    color: #FFB4B4 !important;
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 0.15em;
    line-height: 1.2;
    text-transform: uppercase;
    padding-left: 10px;
    position: relative;
}
.section-kicker::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    width: 5px;
    height: 5px;
    transform: translateY(-50%);
    background: var(--yt-red);
    box-shadow: 0 0 12px rgba(255,0,0,0.65);
}
.section-title-main {
    color: #FFFFFF !important;
    font-size: 19px;
    font-weight: 900;
    line-height: 1.45;
    letter-spacing: -0.02em;
}
.section-heading::after {
    right: -34px !important;
    top: -34px !important;
    width: 82px !important;
    height: 82px !important;
}


/* V28: section-heading を落ち着いたグレー系に調整 */
.section-heading {
    background:
        linear-gradient(135deg, rgba(255,255,255,0.085), rgba(255,255,255,0.025)),
        linear-gradient(180deg, rgba(38,38,38,0.94), rgba(22,22,22,0.94)) !important;
    border: 1px solid rgba(255,255,255,0.13) !important;
    border-bottom: 0 !important;
    box-shadow:
        0 10px 24px rgba(0,0,0,0.22),
        inset 0 1px 0 rgba(255,255,255,0.055) !important;
}
.section-heading::after {
    background: rgba(255,255,255,0.045) !important;
}
.section-kicker {
    color: #D1D5DB !important;
}
.section-kicker::before {
    background: var(--yt-red) !important;
    box-shadow: 0 0 10px rgba(255,0,0,0.52) !important;
}
.section-title-main {
    color: #F9FAFB !important;
}


/* V30: section layout refinements */
.plain-paragraph-block {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 2px 0 12px !important;
    margin: 2px 0 14px !important;
    color: #D4D4D4 !important;
    line-height: 1.85 !important;
}
.plain-paragraph-block b {
    color: #FFFFFF !important;
}
.status-advice-card .status-panel {
    margin: 0 !important;
    border-radius: 5px !important;
    background: transparent !important;
    border: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
}
.status-advice-card .advice-title {
    margin-bottom: 16px !important;
}
.status-advice-card .status-item {
    background:
        linear-gradient(135deg, rgba(255,255,255,0.075), rgba(255,255,255,0.028)),
        rgba(18,18,18,0.70) !important;
}
.decision-panel {
    background:
        linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,0,0,0.06)),
        rgba(15,15,15,0.84) !important;
    border-color: rgba(255,255,255,0.13) !important;
    box-shadow:
        inset 4px 0 0 rgba(255,0,0,0.72),
        0 14px 34px rgba(0,0,0,0.22) !important;
    margin-top: 18px !important;
    margin-bottom: 18px !important;
}
.decision-panel .recommend-title {
    margin-bottom: 10px !important;
}
.decision-panel .recommend-reason {
    margin-bottom: 0 !important;
}



/* V31: Action画面の区切りを整理 */
.decision-compact {
    margin-top: 4px !important;
    margin-bottom: 16px !important;
    padding-bottom: 14px !important;
    border-bottom: 1px solid rgba(255,255,255,0.10) !important;
}
.decision-compact .recommend-title {
    font-size: 19px !important;
    margin-bottom: 8px !important;
}
.decision-compact .recommend-reason {
    margin-bottom: 0 !important;
}


/* V32: 優先課題パネルをすっきり表示 */
.recommend-panel {
    background:
        linear-gradient(135deg, rgba(255,255,255,0.055), rgba(255,255,255,0.022)),
        rgba(16,16,16,0.82) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-left: 1px solid rgba(255,255,255,0.12) !important;
    box-shadow: none !important;
}
.recommend-panel .recommend-title {
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    padding-bottom: 10px !important;
    margin-bottom: 10px !important;
}
.recommend-panel .recommend-reason {
    margin-bottom: 12px !important;
}
.recommend-panel .recommend-card {
    background:
        linear-gradient(135deg, rgba(255,255,255,0.055), rgba(255,255,255,0.024)),
        rgba(22,22,22,0.78) !important;
    border: 1px solid rgba(255,255,255,0.105) !important;
    border-left: 1px solid rgba(255,255,255,0.105) !important;
    box-shadow: none !important;
}
.recommend-panel .recommend-card.high,
.recommend-panel .recommend-card.medium {
    box-shadow: none !important;
}
.recommend-panel .recommend-card.high {
    background:
        linear-gradient(135deg, rgba(255,0,0,0.075), rgba(255,255,255,0.028)),
        rgba(22,22,22,0.80) !important;
    border-color: rgba(255,255,255,0.13) !important;
}
.recommend-panel .recommend-card.medium {
    background:
        linear-gradient(135deg, rgba(245,158,11,0.07), rgba(255,255,255,0.026)),
        rgba(22,22,22,0.80) !important;
    border-color: rgba(255,255,255,0.12) !important;
}
.recommend-panel .recommend-badge {
    border-radius: 4px !important;
}




/* =========================
   V42: geometric pattern removed / enhanced ambient gradient animation
   - No geometric pattern, no extra layer, no SVG/base64.
   - Uses only soft moving glows behind the UI.
   ========================= */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.block-container {
    background: transparent !important;
}

.stApp {
    position: relative !important;
    overflow-x: hidden !important;
    background:
        radial-gradient(circle at 12% 4%, rgba(255,0,0,0.22), transparent 29%),
        radial-gradient(circle at 88% 7%, rgba(255,255,255,0.075), transparent 28%),
        radial-gradient(circle at 68% 84%, rgba(255,42,42,0.15), transparent 34%),
        linear-gradient(135deg, #050505 0%, #0F0F0F 46%, #191919 100%) !important;
}

.stApp::before,
.stApp::after {
    content: "" !important;
    position: fixed !important;
    inset: -22% !important;
    pointer-events: none !important;
    z-index: 0 !important;
    will-change: transform, opacity;
}

.stApp::before {
    background:
        radial-gradient(circle at 14% 22%, rgba(255,0,0,0.34), transparent 18%),
        radial-gradient(circle at 82% 16%, rgba(255,75,75,0.22), transparent 17%),
        radial-gradient(circle at 70% 78%, rgba(255,255,255,0.075), transparent 20%),
        radial-gradient(circle at 24% 82%, rgba(255,0,0,0.13), transparent 18%);
    filter: blur(8px);
    opacity: 0.78 !important;
    animation: ytAmbientDriftStrong 15s ease-in-out infinite !important;
}

.stApp::after {
    background:
        radial-gradient(circle at 42% 26%, rgba(255,255,255,0.070), transparent 17%),
        radial-gradient(circle at 90% 72%, rgba(255,0,0,0.24), transparent 19%),
        radial-gradient(circle at 8% 58%, rgba(255,75,75,0.16), transparent 16%),
        radial-gradient(circle at 52% 92%, rgba(255,0,0,0.10), transparent 24%);
    filter: blur(14px);
    opacity: 0.56 !important;
    mix-blend-mode: screen;
    animation: ytAmbientBreathStrong 9s ease-in-out infinite !important;
    animation-delay: -2.5s !important;
}

@keyframes ytAmbientDriftStrong {
    0%, 100% {
        transform: translate3d(0, 0, 0) scale(1);
        opacity: 0.66;
    }
    22% {
        transform: translate3d(2.8%, -1.8%, 0) scale(1.05);
        opacity: 0.88;
    }
    48% {
        transform: translate3d(-2.2%, 2.0%, 0) scale(0.985);
        opacity: 0.58;
    }
    74% {
        transform: translate3d(1.8%, 2.4%, 0) scale(1.065);
        opacity: 0.92;
    }
}

@keyframes ytAmbientBreathStrong {
    0%, 100% {
        transform: translate3d(0, 0, 0) scale(1) rotate(0deg);
        opacity: 0.40;
    }
    28% {
        transform: translate3d(-2.4%, 1.4%, 0) scale(1.06) rotate(0.35deg);
        opacity: 0.66;
    }
    55% {
        transform: translate3d(2.2%, -1.6%, 0) scale(0.98) rotate(-0.2deg);
        opacity: 0.36;
    }
    82% {
        transform: translate3d(1.0%, 1.1%, 0) scale(1.075) rotate(0.15deg);
        opacity: 0.72;
    }
}

/* Keep the UI above the animated background. */
.stApp > *,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.block-container,
[data-testid="stHeader"] {
    position: relative !important;
    z-index: 2 !important;
}

@media (max-width: 760px) {
    .stApp::before { opacity: 0.58 !important; }
    .stApp::after { opacity: 0.38 !important; }
}

@media (prefers-reduced-motion: reduce) {
    .stApp::before,
    .stApp::after {
        animation: none !important;
        opacity: 0.40 !important;
    }
}



/* =========================
   V46: header image spacing refinement
   ========================= */
.block-container {
    padding-top: 0.65rem !important;
}

/* Tighten the vertical whitespace around the external title image */
div[data-testid="stImage"] {
    margin-top: -4px !important;
    margin-bottom: 10px !important;
    padding: 0 !important;
    line-height: 0 !important;
}

div[data-testid="stImage"] figure,
div[data-testid="stImage"] > div {
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stImage"] img {
    display: block !important;
    margin: 0 !important;
    border-radius: 5px !important;
}

.header-image-note {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

.nav-tabbar-separator {
    margin-top: -1px !important;
    margin-bottom: 18px !important;
}



/* V49: kicker付き見出しのアイコンを外した前提で余白を再調整 */
.section-heading {
    padding: 11px 16px 12px 18px !important;
}
.section-heading-inner {
    gap: 2px !important;
}
.section-kicker {
    font-size: 10px !important;
    letter-spacing: 0.17em !important;
    margin-bottom: 1px !important;
    line-height: 1.15 !important;
}
.section-title-main {
    font-size: 18px !important;
    line-height: 1.35 !important;
    letter-spacing: -0.015em !important;
}
.advice-kicker,
.recommend-kicker {
    font-size: 10px !important;
    letter-spacing: 0.17em !important;
    margin-bottom: 4px !important;
    line-height: 1.15 !important;
}
.advice-title,
.recommend-title {
    font-size: 19px !important;
    line-height: 1.38 !important;
    margin-top: 0 !important;
    margin-bottom: 10px !important;
    padding-bottom: 9px !important;
}
.recommend-panel {
    padding-top: 16px !important;
}
</style>

""", unsafe_allow_html=True)

# =========================
# 初回表示用：軽量ローディング演出
# =========================
# Streamlitは操作のたびに再実行されるため、ローディング演出を毎回出すと
# 入力作業の邪魔になります。session_stateで「初回だけ」表示します。
if "_intro_loader_seen" not in st.session_state:
    st.session_state["_intro_loader_seen"] = True
    st.markdown("""
    <style>
    body::before {
        content: "AI-MV PDCA Dashboard";
        position: fixed;
        inset: 0;
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
        background:
            radial-gradient(circle at 35% 35%, rgba(56,189,248,0.18), transparent 28%),
            radial-gradient(circle at 65% 60%, rgba(255,0,51,0.16), transparent 30%),
            linear-gradient(135deg, #020617 0%, #0F172A 55%, #111827 100%);
        color: #F8FAFC;
        font-size: clamp(22px, 4vw, 42px);
        font-weight: 900;
        letter-spacing: -0.04em;
        pointer-events: none;
        animation: introLoaderFade 1.05s ease-out forwards;
    }
    body::after {
        content: "";
        position: fixed;
        left: 50%;
        top: calc(50% + 58px);
        width: 34px;
        height: 34px;
        margin-left: -17px;
        z-index: 1000000;
        border: 3px solid rgba(248,250,252,0.22);
        border-top-color: #38BDF8;
        border-right-color: #FF0033;
        border-radius: 50%;
        pointer-events: none;
        animation:
            introSpin 0.7s linear infinite,
            introSpinnerFade 1.05s ease-out forwards;
    }
    @keyframes introLoaderFade {
        0% { opacity: 1; visibility: visible; }
        58% { opacity: 1; visibility: visible; }
        100% { opacity: 0; visibility: hidden; }
    }
    @keyframes introSpinnerFade {
        0% { opacity: 1; visibility: visible; }
        58% { opacity: 1; visibility: visible; }
        100% { opacity: 0; visibility: hidden; }
    }
    @keyframes introSpin {
        to { transform: rotate(360deg); }
    }
    @media (prefers-reduced-motion: reduce) {
        body::before,
        body::after {
            animation-duration: 0.25s !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# =========================
# Persistent state defaults
# =========================
# タブ風ナビゲーションでは現在表示中のセクションだけを描画するため、
# 入力値がページ移動で消えないように session_state に保持します。
PERSISTENT_DEFAULTS = {
    "student_name": "",
    "video_title": "",
    "target_audience": "",
    "hypothesis": "",
    "target_views": 300,
    "target_ctr": 5.0,
    "target_retention": 35.0,
    "planned_actions_text": "",
    "act_views": 0,
    "likes": 0,
    "act_imp": 0,
    "comments": 0,
    "act_ctr": 0.0,
    "subs": 0,
    "retention": 0.0,
    "short_views": 0,
    "sns_posts": 0,
    "next_kpi": "インプレッションのクリック率（CTR）",
    "next_goal": "",
    "action_reason": "",
    "reflection": "",
    "next_hypothesis": "",
    "_planned_actions_cache": [],
    "_next_actions_cache": [],
}

for _state_key, _default_value in PERSISTENT_DEFAULTS.items():
    if _state_key not in st.session_state:
        st.session_state[_state_key] = _default_value

# v22: 以前のデモ用デフォルト値（視聴回数300回など）が残っている場合は、
# 実績未入力として扱えるように0へリセットします。
# 実際に入力した値まで消さないよう、旧デモ値と完全一致する場合のみ実行します。
_OLD_DEMO_ACTUALS = {
    "act_views": 300,
    "likes": 12,
    "act_imp": 6000,
    "comments": 2,
    "act_ctr": 5.0,
    "subs": 1,
    "retention": 35.0,
    "short_views": 500,
    "sns_posts": 2,
}
if not st.session_state.get("_actual_defaults_zeroed_v22", False):
    if all(st.session_state.get(k) == v for k, v in _OLD_DEMO_ACTUALS.items()):
        for _actual_key in _OLD_DEMO_ACTUALS:
            st.session_state[_actual_key] = 0.0 if _actual_key in {"act_ctr", "retention"} else 0
    st.session_state["_actual_defaults_zeroed_v22"] = True

# v24: 旧版で自動選択していた改善アクションが残っている場合は、
# 「学生が自分で選ぶ」設計に合わせて初回だけクリアします。
if not st.session_state.get("_action_defaults_cleared_v24", False):
    _old_auto_actions = [
        "概要欄・タグ・歌詞を修正する",
        "既存MVからショート動画を切り出して新しく投稿する",
    ]
    if st.session_state.get("_next_actions_cache") == _old_auto_actions:
        st.session_state["_next_actions_cache"] = []
    st.session_state["_action_defaults_cleared_v24"] = True



# v28: 条件分岐型の疑似タブでは、非表示になったウィジェットの値が
# Streamlitのウィジェットクリーンアップで消えることがあります。
# 下記のフォーム用キーだけを毎回自分自身へ再保存し、タブ移動後も入力値を保持します。
# button系のキーは対象外にしているため、StreamlitValueAssignmentNotAllowedErrorを避けられます。
_PERSISTENT_FORM_KEYS = [
    "student_name", "video_title", "target_audience", "hypothesis",
    "target_views", "target_ctr", "target_retention", "planned_actions_text",
    "act_views", "likes", "act_imp", "comments", "act_ctr", "subs",
    "retention", "short_views", "sns_posts",
    "next_kpi", "next_goal", "action_reason", "reflection", "next_hypothesis",
    "presentation_work_intro", "presentation_posting_tips", "presentation_success", "team_learning",
]
for _keep_key in _PERSISTENT_FORM_KEYS:
    if _keep_key in st.session_state:
        st.session_state[_keep_key] = st.session_state[_keep_key]

# 注意：st.button など一部ウィジェットのキーは、session_state に値を再代入すると
# StreamlitValueAssignmentNotAllowedError が発生します。
# そのため、全キーを一括で再代入する処理は行いません。
# 入力値の保持は、PERSISTENT_DEFAULTSで定義したキーと各ウィジェットのkeyに任せます。

# =========================
# Helper functions
# =========================
def badge_class(level: str) -> str:
    return {
        "success": "success",
        "warning": "warning",
        "danger": "danger",
        "neutral": "neutral",
        "legendary": "legendary",
    }.get(level, "neutral")


def render_card(kicker, title, badge, level, status, reason, actions, alert=None, mission=None):
    """診断カードを安全に組み立てて表示する。

    以前の版ではHTMLテンプレート内の差し込み用変数が、そのまま文字として
    表示される環境があったため、ここでは大きなf文字列にまとめず、
    HTMLパーツをリストで組み立てます。
    """
    action_items = "".join([f"<li>{item}</li>" for item in actions])

    card_parts = [
        '<div class="advice-card">',
        f'<div class="advice-kicker">{kicker}</div>',
        f'<div class="advice-title">{html.escape(str(title), quote=True)}</div>',
        f'<div class="result-badge {badge_class(level)}">{badge}</div>',
        '<div class="diagnosis-section">',
        '<span class="section-label">🎮 今の状態</span>',
        f'<p>{status}</p>',
        '</div>',
        '<div class="diagnosis-section">',
        '<span class="section-label">🧠 原因の見立て</span>',
        f'<p>{reason}</p>',
        '</div>',
        '<div class="diagnosis-section">',
        '<span class="section-label">🔥 次の一手</span>',
        f'<ul class="clean-list">{action_items}</ul>',
        '</div>',
    ]

    if mission:
        mission_items = "".join([f"<li>{item}</li>" for item in mission])
        card_parts.extend([
            '<div class="diagnosis-section mission-section">',
            '<span class="section-label">🎯 今日のミッション</span>',
            f'<ul class="clean-list">{mission_items}</ul>',
            '</div>',
        ])

    if alert:
        card_parts.append(f'<div class="alert-highlight">{alert}</div>')

    card_parts.append('</div>')
    st.markdown("\n".join(card_parts), unsafe_allow_html=True)


def ctr_rank(ctr):
    """CTRを、サムネイル・タイトルの入口設計として評価する。"""
    if ctr >= 10:
        return "👑 神サムネ級：一瞬で押したくなる入口", "legendary"
    if ctr >= 7:
        return "🔥 強サムネ級：視線を止める入口", "success"
    if ctr >= 4:
        return "✅ 合格サムネ：クリックされる土台あり", "success"
    return "🛠️ 改善サムネ：見せ方の再設計チャンス", "warning"


def retention_rank(retention):
    if retention >= 55:
        return "👑 沼らせ成功", "legendary"
    if retention >= 40:
        return "🔥 しっかり聴かれている", "success"
    if retention >= 25:
        return "🟨 途中離脱あり", "warning"
    return "🟥 見せ方・導線の改善が必要", "danger"


def short_rank(short_views):
    """連動ショートの最高視聴回数を、授業用の目安として評価する。"""
    if short_views <= 0:
        return "🟨 未投稿・未検証", "warning", "まだ無料広告チラシを配っていない状態"
    if short_views < 500:
        return "🌱 火種フェーズ", "warning", "小さな反応は出ています。別パターン検証で伸びる余地あり"
    if short_views < 2000:
        return "🔥 入口として機能中", "success", "本編MVを知らない人に届く入口が作れています"
    if short_views < 10000:
        return "🚀 強い入口に成長中", "success", "ショートが本編への導線としてかなり期待できます"
    return "👑 ショート覚醒", "legendary", "本編MVへ視聴者を連れてくる強力な広告塔です"


def choose_main_problem(imp, ctr, retention, short_views, external_ratio):
    if imp < 1000:
        return "インプレッション不足", "インプレッション数が少ないため、SEO・ショート・外部SNSで入口を増やすのが最優先です。"
    if ctr < 4:
        return "サムネイル・タイトル訴求不足", "インプレッションはあるのにクリックされていない状態です。サムネイル・タイトルの入口設計を見直すのが最優先です。"
    if retention < 30:
        return "平均再生率不足", "クリックは取れていますが、途中離脱が多い可能性があります。既存MVを作り直すのではなく、視聴者維持率グラフで離脱ポイントを確認し、固定コメント・概要欄・ショートの切り出し・告知文で期待値を整えましょう。"
    if short_views == 0:
        return "ショート未活用", "本編MVだけでは新規チャンネルの拡散力が足りません。既存MVから魅力的な場面を切り出し、ショートを無料広告として使いましょう。"
    if short_views < 500:
        return "ショート導線の再検証", "ショートは投稿できていますが、まだ本編MVへの入口としては火種フェーズです。切り出し場面・タイトル・固定コメントを変えて、別パターンでもう一度試す価値があります。"
    if external_ratio < 15:
        return "外部トラフィック不足", "トラフィックソースがYouTube内に偏っています。SNS告知とチーム拡散で外部からの初動を作りましょう。"
    return "総合的に良好", "大きな弱点は少ない状態です。成功要因を言語化し、次回の投稿で再現しましょう。"




def build_action_recommendations(has_data, data_error, imp, ctr, retention, short_views, external_ratio):
    """投稿後Checkの結果から、Action画面で提示するおすすめ対策を作る。"""
    if not has_data:
        return {
            "priority": "実績データ未入力",
            "reason": "投稿後CheckにYouTubeアナリティクスの数値を入力すると、結果に応じたおすすめ改善アクションが表示されます。",
            "recommendations": [],
            "recommended_map": {},
        }
    if data_error:
        return {
            "priority": "入力データ確認",
            "reason": "視聴回数とインプレッション由来の推定視聴回数に矛盾があります。先に期間・動画・桁数を確認してください。",
            "recommendations": [
                {
                    "action": "YouTubeアナリティクスの対象期間・対象動画・桁数を確認する",
                    "level": "高",
                    "reason": "データがずれていると、改善判断そのものがズレてしまうためです。",
                }
            ],
            "recommended_map": {"YouTubeアナリティクスの対象期間・対象動画・桁数を確認する": "高"},
        }

    priority, reason = choose_main_problem(imp, ctr, retention, short_views, external_ratio)
    recommendations = []

    def add(action, level, why):
        if not any(r["action"] == action for r in recommendations):
            recommendations.append({"action": action, "level": level, "reason": why})

    if imp < 1000:
        add("概要欄・タグ・歌詞を修正する", "高", "YouTubeの検索とおすすめ機能に動画ジャンルや内容を伝え、インプレッション機会を増やすためです。")
        add("既存MVからショート動画を切り出して新しく投稿する", "高", "新規チャンネルでは本編MVだけだと見つけてもらいにくいため、入口を増やします。")
        add("X / Instagram / TikTokで告知する", "中", "YouTube外から初動を作ると、インプレッション拡大のきっかけになります。")
        add("終了画面・カード・再生リストを設定する", "中", "少ない視聴者をチャンネル内で回遊させ、次のインプレッションにつなげます。")

    if ctr < 4 and imp >= 300:
        add("サムネイルを変更する", "高", "インプレッションは出ているのにクリックされていないため、入口の見た目改善が最優先です。")
        add("タイトルを変更する", "高", "タイトル冒頭の言葉で視聴者の期待値を作り、クリック理由を強くします。")
        add("他メンバーの高CTRサムネイルと比較する", "中", "成功している見た目の共通点を見つけ、自分の動画に転用しやすくなります。")

    if retention < 30 and (ctr >= 4 or imp >= 1000):
        add("視聴者維持率グラフで離脱ポイントを確認する", "高", "どこで離脱しているかを見ないと、次の改善仮説が立てにくいためです。")
        add("固定コメント・概要欄でMVの見どころを補足する", "高", "MV本体を作り直さずに、視聴者の期待値と見どころを整えられます。")
        add("ショート動画の切り出し部分を見直す", "中", "本編で魅力が伝わる部分を入口にすると、期待ズレを減らせます。")

    if short_views == 0:
        add("既存MVからショート動画を切り出して新しく投稿する", "高", "ショート未活用なら、まず無料広告チラシとして入口を作る効果が大きいためです。")
        add("ショートの固定コメント・概要欄から本編MVへ誘導する", "中", "ショート単体で終わらせず、本編MVへ移動する道を作るためです。")
    elif short_views < 500:
        add("ショート動画の切り出し部分を見直して別パターンを投稿する", "高", "反応は出始めています。サビ・強い歌詞・見せ場など別の入口を試すと伸びる可能性があります。")
        add("ショートのタイトル・固定コメントから本編MVへ誘導する", "高", "少ない視聴でも、本編リンクへの導線を整えることで再生回数につなげやすくなります。")
    elif short_views < 2000:
        add("伸びたショートの固定コメント・概要欄から本編MVへ誘導する", "高", "ショートが入口として機能し始めています。本編リンクを強化して視聴回数へつなげましょう。")
        add("伸びたショートの別バージョンを追加投稿する", "中", "反応が良かった切り口を横展開すると、本編への入口を増やせます。")
    else:
        add("伸びたショートを本編MVへの導線として強化する", "高", "ショートが強い広告塔になっています。固定コメント・概要欄・チャンネル導線で本編視聴へ接続しましょう。")
        add("伸びたショートの続編・別切り出しを投稿する", "中", "勢いがあるうちに第2波を作ると、本編MVへの流入をさらに増やせます。")

    if external_ratio < 15 and imp >= 300:
        add("X / Instagram / TikTokで告知する", "高", "YouTube内だけに頼らず、外部トラフィックから初動を作るためです。")
        add("チーム内で相互視聴・コメント・引用リポストを行う", "中", "初動の熱量を作り、コメントや視聴維持のきっかけを増やします。")

    if not recommendations:
        add("成功要因を言語化して次回の投稿に再利用する", "高", "大きな弱点がない時こそ、なぜ良かったのかを再現可能なノウハウにすることが重要です。")
        add("コメント返信・固定コメントでファン化する", "中", "良い反応を次回の視聴や登録につなげるためです。")
        add("終了画面・カード・再生リストを設定する", "中", "伸びている動画から他の動画へ回遊させることで、チャンネル全体の評価につなげます。")

    recommended_map = {r["action"]: r["level"] for r in recommendations}
    return {
        "priority": priority,
        "reason": reason,
        "recommendations": recommendations,
        "recommended_map": recommended_map,
    }


def render_action_recommendation_panel(result):
    priority = html.escape(str(result.get("priority", "未判定")), quote=True)
    reason = html.escape(str(result.get("reason", "")), quote=True)
    recommendations = result.get("recommendations", [])

    parts = [
        '<div class="recommend-panel">',
        '<div class="recommend-kicker">CHECK RESULT LINKED ACTION</div>',
        f'<div class="recommend-title">今回の優先課題：{priority}</div>',
        f'<div class="recommend-reason">{reason}</div>',
    ]

    if recommendations:
        parts.append('<div class="recommend-card-grid">')
        for rec in recommendations:
            action = html.escape(str(rec.get("action", "")), quote=True)
            level = html.escape(str(rec.get("level", "中")), quote=True)
            why = html.escape(str(rec.get("reason", "")), quote=True)
            level_class = "high" if level == "高" else "medium"
            parts.extend([
                f'<div class="recommend-card {level_class}">',
                f'<div class="recommend-badge">おすすめ度：{level}</div>',
                f'<div class="recommend-action-title">{action}</div>',
                f'<div class="recommend-action-reason">{why}</div>',
                '</div>',
            ])
        parts.append('</div>')
    else:
        parts.append('<div class="action-choice-note">先に「2. 投稿後 Check」で実績値を入力してください。おすすめは、入力されたKPIに応じて表示されます。</div>')

    parts.append('</div>')
    st.markdown("\n".join(parts), unsafe_allow_html=True)


def render_student_decision_panel():
    """おすすめ提示後に、学生自身が判断するゾーンをコンパクトに表示する。"""
    st.markdown(
        """
        <div class="plain-paragraph-block decision-compact">
            <div class="recommend-kicker">ACTION STRATEGY</div>
            <div class="recommend-title">改善アクション選択カルテ</div>
            <div class="recommend-reason">
                システムのおすすめは“考えるための補助線”です。おすすめ度が高いものを必ず選ぶ必要はありません。<br>
                自分たちの作品・ターゲット・投稿前の仮説を踏まえて、次に本当に実行する改善アクションを選んでください。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_panel(rows):
    """総合ステータスを他の診断カードと同じHTML構造で表示する。"""
    def status_meta(label):
        label_str = str(label)
        if "総視聴" in label_str or "視聴回数" == label_str:
            return "🎬", "status-views"
        if "YouTube" in label_str or "インプレッション由来" in label_str:
            return "📥", "status-youtube"
        if "外部" in label_str or "SNS" in label_str:
            return "🌐", "status-external"
        if "CTR" in label_str or "クリック率" in label_str or "サムネイル" in label_str:
            return "📊", "status-ctr"
        if "維持" in label_str or "平均再生率" in label_str:
            return "🎧", "status-retention"
        if "ショート" in label_str:
            return "📱", "status-external"
        if "課題" in label_str or "最大" in label_str:
            return "🚨", "status-item-problem"
        return "✨", "status-warning"

    panel_parts = [
        '<div class="advice-card status-advice-card compact-status-card">',
        '<div class="status-panel">',
    ]

    for label, value in rows:
        icon, class_name = status_meta(label)
        label_text = html.escape(str(label), quote=True)
        value_text = html.escape(str(value), quote=True).replace("\n", "<br>")
        small_class = " status-item-small" if len(str(value)) > 14 else ""
        panel_parts.extend([
            f'<div class="status-item {class_name}{small_class}">',
            f'<div class="status-icon">{icon}</div>',
            '<div class="status-content">',
            f'<div class="status-label">{label_text}</div>',
            f'<div class="status-value">{value_text}</div>',
            '</div>',
            '</div>',
        ])

    panel_parts.extend(['</div>', '</div>'])
    st.markdown("\n".join(panel_parts), unsafe_allow_html=True)


def render_empty_status_panel():
    """実績データ未入力時の案内を、他の診断カードと同じHTML構造で表示する。"""
    st.markdown(
        """
        <div class="advice-card status-advice-card compact-status-card empty-status-panel">
            <div class="status-panel">
                <div class="status-item status-warning status-item-problem">
                    <div class="status-icon">📝</div>
                    <div class="status-content">
                        <div class="status-label">まだ実績データが未入力です</div>
                        <div class="status-value">YouTubeアナリティクスの数値を入力すると、視聴回数・インプレッション・CTR・平均再生率をもとに診断が表示されます。</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_selected_list(title, items):
    safe_title = html.escape(str(title), quote=True)
    if not items:
        st.markdown(
            f"""
            <div class="action-list-box">
                <div class="action-list-title">✅ {safe_title}</div>
                <p class="small-note">まだ選択されていません。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    selected_html = "".join([f"<li>{html.escape(str(item), quote=True)}</li>" for item in items])
    st.markdown(
        f"""
        <div class="action-list-box">
            <div class="action-list-title">✅ {safe_title}</div>
            <ul>{selected_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def checkbox_group(label, options, default_selected=None, key_prefix="check", columns=1):
    default_selected = default_selected or []
    st.markdown(f"**{label}**")
    selected = []
    if columns <= 1:
        for i, option in enumerate(options):
            if st.checkbox(option, value=option in default_selected, key=f"{key_prefix}_{i}"):
                selected.append(option)
    else:
        cols = st.columns(columns)
        for i, option in enumerate(options):
            with cols[i % columns]:
                if st.checkbox(option, value=option in default_selected, key=f"{key_prefix}_{i}"):
                    selected.append(option)
    return selected


def checkbox_grouped(label, groups, default_selected=None, key_prefix="group_check", recommendation_map=None):
    """カテゴリごとにチェックボックスを分けて表示する。返り値は選択項目のフラットなリスト。"""
    default_selected = default_selected or []
    recommendation_map = recommendation_map or {}
    st.markdown(f"**{label}**")
    selected = []

    for group_index, group in enumerate(groups):
        group_title = html.escape(str(group.get("title", "グループ")), quote=True)
        group_desc = html.escape(str(group.get("desc", "")), quote=True)
        group_html = (
            '<div class="group-heading">'
            f'<div class="group-title">{group_title}</div>'
            f'<div class="group-desc">{group_desc}</div>'
            '</div>'
        )
        st.markdown(group_html, unsafe_allow_html=True)
        for item_index, option in enumerate(group.get("items", [])):
            key = f"{key_prefix}_{group_index}_{item_index}"
            rec_level = recommendation_map.get(option)
            label_text = f"🔥 おすすめ度{rec_level}｜{option}" if rec_level else option
            if st.checkbox(label_text, value=option in default_selected, key=key):
                selected.append(option)
    return selected


def render_selected_grouped_list(title, groups, selected_items):
    safe_title = html.escape(str(title), quote=True)
    selected_set = set(selected_items or [])

    if not selected_set:
        no_items_html = (
            '<div class="action-list-box">'
            f'<div class="action-list-title">✅ {safe_title}</div>'
            '<p class="small-note">まだ選択されていません。</p>'
            '</div>'
        )
        st.markdown(no_items_html, unsafe_allow_html=True)
        return

    parts = [
        '<div class="action-list-box">',
        f'<div class="action-list-title">✅ {safe_title}</div>',
    ]

    for group in groups:
        group_items = [item for item in group.get("items", []) if item in selected_set]
        if not group_items:
            continue
        group_title = html.escape(str(group.get("title", "グループ")), quote=True)
        item_html = "".join([f"<li>{html.escape(str(item), quote=True)}</li>" for item in group_items])
        parts.extend([
            '<div class="selected-group">',
            f'<div class="selected-group-title">{group_title}</div>',
            f'<ul>{item_html}</ul>',
            '</div>',
        ])

    parts.append('</div>')
    st.markdown("\n".join(parts), unsafe_allow_html=True)




def strip_leading_icon(text):
    """kicker付き見出しの本文から、先頭の絵文字・装飾記号だけを外す。"""
    value = str(text).strip()
    # 先頭にある絵文字、記号、Variation Selector、空白をまとめて除去
    return re.sub(r"^[\s\ufe0f\u200d\U0001F300-\U0001FAFF\u2600-\u27BF]+", "", value).strip()


def render_section_heading(kicker, title):
    """大きな区切り見出しを、advice-kicker風のラベル付きで描画する。"""
    safe_kicker = html.escape(str(kicker), quote=True)
    safe_title = html.escape(strip_leading_icon(title), quote=True)
    section_html = (
        '<div class="section-heading">'
        '<div class="section-heading-inner">'
        f'<div class="section-kicker">{safe_kicker}</div>'
        f'<div class="section-title-main">{safe_title}</div>'
        '</div>'
        '</div>'
    )
    st.markdown(section_html, unsafe_allow_html=True)

def render_subheading(text):
    """StreamlitのMarkdown見出しを使わず、小見出しをHTMLで描画する。

    Markdown見出し（###）を使うと、Streamlitが見出しアンカー用の内部HTML
    （stHeaderActionElements）を付与します。一部環境でその内部HTMLが文字として
    表示されることがあるため、アプリ内の小見出しはこの関数に統一します。
    """
    safe_text = html.escape(str(text), quote=True)
    st.markdown(
        f'<div class="sub-heading"><span>{safe_text}</span></div>',
        unsafe_allow_html=True,
    )



def parse_plan_actions(text):
    """自由記入された投稿前施策を、レポート用のリストに整形する。"""
    if not text:
        return []
    actions = []
    for line in str(text).splitlines():
        cleaned = line.strip().strip("・-−—* ").strip()
        if cleaned:
            actions.append(cleaned)
    return actions


def render_free_plan_preview(text):
    """自由記入された投稿前施策をレポート用に整形して返す。

    入力欄の直後に同じ内容をプレビュー表示すると冗長になるため、
    画面表示は行わず、レポート生成用のリスト化だけを担当する。
    """
    return parse_plan_actions(text)

def make_report(student_name, video_title, hypothesis, target_audience, planned_actions, target_views, target_ctr,
                act_views, act_imp, act_ctr, retention, likes, comments, subs, short_views,
                external_views, external_ratio, main_problem, next_actions, next_kpi, next_goal, action_reason, reflection, next_hypothesis):
    name_part = f"{student_name}さんの" if student_name else "今回の"
    action_part = "、".join(planned_actions) if planned_actions else "未設定"
    next_action_part = "、".join(next_actions) if next_actions else "未設定"
    short_label, _, short_reason = short_rank(short_views)
    return f"""【AI-MV YouTube運用 PDCAレポート】

■ 対象作品
{name_part}MV「{video_title or '未入力'}」について、投稿前には「{hypothesis or '未入力'}」という仮説を立て、主なターゲットを「{target_audience or '未入力'}」に設定した。投稿前の目標は、視聴回数 {target_views:,} 回、インプレッションのクリック率（CTR） {target_ctr:.1f}% であり、実施施策は「{action_part}」である。

■ 実績確認（Check）
投稿後の実績は、視聴回数 {act_views:,} 回、インプレッション {act_imp:,} 回、インプレッションのクリック率（CTR） {act_ctr:.1f}%、平均再生率 {retention:.1f}% となった。高評価数は {likes:,} 件、コメント数は {comments:,} 件、チャンネル登録者増加は {subs:,} 人、連動ショートの最高視聴回数は {short_views:,} 回である。ショート評価は「{short_label}」であり、{short_reason}。計算上、外部・その他トラフィックの推定視聴回数は約 {external_views:,} 回、外部トラフィック比率は {external_ratio:.1f}% と考えられる。

■ 診断
今回の最大課題は「{main_problem}」である。{choose_main_problem(act_imp, act_ctr, retention, short_views, external_ratio)[1]}

■ 次回の改善（Action）
次回は「{next_action_part}」を重点施策として実行する。これを選んだ理由は「{action_reason or '未入力'}」である。検証するKPIは「{next_kpi}」、次回目標は「{next_goal or '未入力'}」とする。

■ 振り返り
今回わかったこと：{reflection or '未入力'}
次回の仮説：{next_hypothesis or '未入力'}
"""


def make_presentation_summary(student_name, video_title, presentation_work_intro, presentation_posting_tips,
                              planned_actions, act_views, act_imp, act_ctr, retention, likes, comments,
                              subs, short_views, external_ratio, main_problem, reflection,
                              presentation_success, team_learning, next_actions):
    """再来週のチーム発表に使える共有メモを自動生成する。"""
    action_part = "、".join(planned_actions) if planned_actions else "未入力"
    next_action_part = "、".join(next_actions) if next_actions else "未入力"
    short_label, _, short_reason = short_rank(short_views)
    presenter = f"{student_name}さん / チーム" if student_name else "チーム"

    return f"""【最終発表用 共有メモ】

1. 作品紹介
・発表者：{presenter}
・作品名：{video_title or '未入力'}
・作品の推しポイント：{presentation_work_intro or '未入力'}

2. チャンネル・投稿の工夫
・投稿時に意識したこと：{presentation_posting_tips or '未入力'}
・投稿前に立てた施策：{action_part}

3. 再生回数を伸ばすために試したこと
・実際に行った / 次に行う改善アクション：{next_action_part}
・今回の優先課題：{main_problem}

4. 数字の結果
・視聴回数：{act_views:,} 回
・インプレッション：{act_imp:,} 回
・インプレッションのクリック率（CTR）：{act_ctr:.1f}%
・平均再生率：{retention:.1f}%
・高評価数：{likes:,} 件 / コメント数：{comments:,} 件 / 登録者増加：{subs:,} 人
・ショート最高視聴回数：{short_views:,} 回（{short_label}：{short_reason}）
・外部トラフィック比率：{external_ratio:.1f}%

5. 数字を見て分かったこと
・{reflection or '未入力'}

6. 成功事例・共有したい工夫
・うまくいったこと / 他チームにも共有したいこと：{presentation_success or '未入力'}

7. チームで学んだこと
・{team_learning or '未入力'}

8. 次に活かすこと
・今回の結果から、次回は「数字を見る → 原因を考える → 改善を選ぶ → もう一度検証する」の流れをさらに意識する。
"""

# =========================
# Header
# =========================
HEADER_IMAGE_PATH = Path(__file__).resolve().parent / "header_ai_mv_pdca.png"

if HEADER_IMAGE_PATH.exists():
    # st.image()のラッパー余白を避けるため、PNGをHTML imgとして直接表示します。
    # SVGではなくPNGなので、前回のような表示崩れを起こしにくい方式です。
    header_b64 = base64.b64encode(HEADER_IMAGE_PATH.read_bytes()).decode("utf-8")
    st.markdown(
        f"""
        <div class="header-image-wrap">
            <img src="data:image/png;base64,{header_b64}" alt="AI-MV配信分析システム ヘッダー画像">
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # 画像ファイルが見つからない場合の安全なフォールバック
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">AI MUSIC VIDEO / YOUTUBE PDCA DASHBOARD</div>
        <div class="hero-title">🎬 AI-MV配信分析システム</div>
        <p>生成AI音楽 × MV制作 × YouTube運用を、仮説・実行・分析・改善まで一気通貫で学ぶ実習ツール</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Navigation
# =========================
# 入力操作で先頭画面に戻らないよう、現在の画面をsession_stateで保持します。
NAV_STEPS = [
    ("plan", "［1］ PLAN／投稿前"),
    ("check", "［2］ CHECK／投稿後分析"),
    ("action", "［3］ ACTION／改善レポート"),
]
NAV_OPTIONS = [label for _, label in NAV_STEPS]
NAV_LABEL_BY_KEY = dict(NAV_STEPS)
NAV_KEY_BY_LABEL = {label: key for key, label in NAV_STEPS}

if "active_step_key" not in st.session_state:
    # 旧バージョンで ?step=... がURLに残っている場合だけ初期値として拾います。
    try:
        initial_step = st.query_params.get("step", "plan")
    except Exception:
        try:
            params = st.experimental_get_query_params()
            raw = params.get("step", ["plan"])
            initial_step = raw[0] if isinstance(raw, list) else raw
        except Exception:
            initial_step = "plan"
    if isinstance(initial_step, list):
        initial_step = initial_step[0] if initial_step else "plan"
    st.session_state["active_step_key"] = initial_step if initial_step in NAV_LABEL_BY_KEY else "plan"

current_nav_key = st.session_state.get("active_step_key", "plan")
if current_nav_key not in NAV_LABEL_BY_KEY:
    current_nav_key = "plan"
    st.session_state["active_step_key"] = "plan"

def set_active_step(step_key: str):
    """タブクリック時に、描画前のタイミングで現在タブを更新する。"""
    if step_key in NAV_LABEL_BY_KEY:
        st.session_state["active_step_key"] = step_key

# st.button はクリック時に全体が再実行されます。
# clicked の戻り値を見て後から active_step_key を変えると、
# ボタン色だけが1回遅れて反映されることがあります。
# そのため on_click コールバックで、再描画前に現在タブを更新します。
current_nav_key = st.session_state.get("active_step_key", "plan")
if current_nav_key not in NAV_LABEL_BY_KEY:
    current_nav_key = "plan"
    st.session_state["active_step_key"] = "plan"

st.session_state["active_step"] = NAV_LABEL_BY_KEY[current_nav_key]
current_step = st.session_state["active_step"]

# URLリンク・radio・segmented_controlを使わず、st.buttonだけで同一画面内のタブ切り替えを行います。
# これにより「新しいブラウザタブが開く」「ラジオ/チェックボックスに見える」問題を避けます。
nav_cols = st.columns(len(NAV_STEPS), gap="small")
for idx, (step_key, step_label) in enumerate(NAV_STEPS):
    with nav_cols[idx]:
        is_active = step_key == current_nav_key
        # buttonのキーに対応する値はsession_stateへ直接代入しないこと。
        # 現在タブの状態は active_step_key だけで管理します。
        try:
            st.button(
                step_label,
                key=f"_nav_btn_{step_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                on_click=set_active_step,
                args=(step_key,),
            )
        except TypeError:
            fallback_label = ("▶ " if is_active else "") + step_label
            st.button(
                fallback_label,
                key=f"_nav_btn_{step_key}",
                use_container_width=True,
                on_click=set_active_step,
                args=(step_key,),
            )

st.markdown('<div class="nav-tabbar-separator"></div>', unsafe_allow_html=True)

current_nav_key = st.session_state.get("active_step_key", "plan")
current_step = NAV_LABEL_BY_KEY.get(current_nav_key, NAV_OPTIONS[0])
st.session_state["active_step"] = current_step

# 現在表示していないセクションの値もレポートで使えるよう、
# session_state から常に最新値を取り出します。
student_name = st.session_state.get("student_name", "")
video_title = st.session_state.get("video_title", "")
target_audience = st.session_state.get("target_audience", "")
hypothesis = st.session_state.get("hypothesis", "")
target_views = st.session_state.get("target_views", 300)
target_ctr = st.session_state.get("target_ctr", 5.0)
target_retention = st.session_state.get("target_retention", 35.0)
planned_actions_text = st.session_state.get("planned_actions_text", "")
planned_actions = parse_plan_actions(planned_actions_text)

act_views = st.session_state.get("act_views", 0)
likes = st.session_state.get("likes", 0)
act_imp = st.session_state.get("act_imp", 0)
comments = st.session_state.get("comments", 0)
act_ctr = st.session_state.get("act_ctr", 0.0)
subs = st.session_state.get("subs", 0)
retention = st.session_state.get("retention", 0.0)
short_views = st.session_state.get("short_views", 0)
sns_posts = st.session_state.get("sns_posts", 0)

yt_internal_views = int(act_imp * (act_ctr / 100))
has_actual_data_global = any([
    act_views > 0, act_imp > 0, act_ctr > 0, retention > 0, likes > 0,
    comments > 0, subs > 0, short_views > 0, sns_posts > 0,
])
is_data_error = has_actual_data_global and act_views < yt_internal_views
external_views = 0 if is_data_error else max(act_views - yt_internal_views, 0)
external_ratio = 0 if act_views == 0 or is_data_error else external_views / act_views * 100

next_actions = st.session_state.get("_next_actions_cache", PERSISTENT_DEFAULTS["_next_actions_cache"])
next_kpi = st.session_state.get("next_kpi", "インプレッションのクリック率（CTR）")
next_goal = st.session_state.get("next_goal", "")
action_reason = st.session_state.get("action_reason", "")
reflection = st.session_state.get("reflection", "")
next_hypothesis = st.session_state.get("next_hypothesis", "")

# =========================
# PLAN
# =========================
if current_step == NAV_OPTIONS[0]:
    render_section_heading('PLAN SETUP', '投稿前：仮説とKPIを決める')
    col_a, col_b = st.columns([1, 1])
    with col_a:
        with st.container():
            render_subheading("🎵 作品情報")
            student_name = st.text_input("学生名・チーム名（任意）", placeholder="例：NVCチームA", key="student_name")
            video_title = st.text_input("MVタイトル", placeholder="例：電波の向こうへ", key="video_title")
            target_audience = st.text_area("狙うターゲット", placeholder="例：ボカロ好き、AI音楽に興味がある高校生、作業用BGMを探している人", key="target_audience")
            hypothesis = st.text_area("今回の仮説", placeholder="例：サムネを明るくし、タイトルにSunoAIとボカロを入れればCTRが上がるはず", key="hypothesis")
    with col_b:
        with st.container():
            render_subheading("📈 目標KPI")
            target_views = st.number_input("目標視聴回数（回）", min_value=50, step=50, key="target_views")
            target_ctr = st.slider("目標インプレッションのクリック率（CTR %）", min_value=1.0, max_value=20.0, step=0.1, key="target_ctr")
            target_retention = st.slider("目標平均再生率（%）", min_value=5.0, max_value=100.0, step=1.0, key="target_retention")
            required_imp = target_views / (target_ctr / 100)
            st.metric("必要インプレッション数の目安", f"{int(required_imp):,} 回")

    with st.container():
        render_subheading("🚀 実施予定の施策（自由記入）")
        st.markdown(
            """
            <div class="plain-paragraph-block">
                <b>まずは自分たちで作戦を立てるゾーンです。</b><br>
                ここでは選択肢から選ぶのではなく、チームで考えた投稿前の施策を自由に書いてください。<br>
                きれいな正解を書くより、<b>「なぜそれをやるのか」</b>まで書けると、投稿後のPDCAがかなり強くなります。
            </div>
            """,
            unsafe_allow_html=True,
        )
        planned_actions_text = st.text_area(
            "投稿前に実施する予定の施策",
            placeholder=(
                "例：サムネイルをスマホで見て、文字が読めるか確認する\n"
                "例：投稿当日にXで15秒の動画付き告知をする\n"
                "例：概要欄に歌詞と制作クレジットを書く"
            ),
            height=180,
            key="planned_actions_text",
        )
        planned_actions = render_free_plan_preview(planned_actions_text)
        st.session_state["_planned_actions_cache"] = planned_actions


    ctr_label, ctr_level = ctr_rank(target_ctr)
    if target_views >= 1000:
        view_badge = "🔥 総力戦フェーズ：メガヒットを狙うラスボス級ミッション！"
        view_level = "legendary"
        view_status = "新規チャンネルとしてはかなり挑戦的な目標です。チーム内再生だけでは届きにくく、外部SNSとショートの総動員が必要です。"
    elif target_views >= 300:
        view_badge = "🚀 スマッシュヒットフェーズ：一般視聴者を巻き込む拡張ミッション！"
        view_level = "success"
        view_status = "身内だけではなく、ボカロ・AI音楽・作業用BGMなどに興味がある第三者へ届ける設計が必要です。"
    else:
        view_badge = "🌱 ファーストフォロワー獲得フェーズ：初動づくりの基礎ミッション！"
        view_level = "warning"
        view_status = "まずは初期視聴と平均再生率を作り、YouTubeに『この動画は見られている』と伝える段階です。"

    render_card(
        "PLAN STRATEGY",
        "投稿前 戦略カルテ",
        view_badge,
        view_level,
        view_status,
        f"サムネイル・タイトルの目標CTRは <b>{target_ctr:.1f}%</b>。入口設計の目安は <b>{ctr_label}</b> です。MVでは、音と映像の世界観がクリック前にどれだけ伝わるかが勝負です。",
        [
            "このMVは、誰に最初に見つけてほしい作品か？",
            "視聴者がクリックする前に、サムネイルとタイトルだけで世界観は伝わるか？",
            "投稿後にどのKPIを見ると、自分たちの仮説が当たったか判断できるか？",
            "YouTube内だけでなく、外部SNSやショートからの入口をどう作るか？",
        ],
        alert="⚠️ これは答え合わせではなく、作戦会議用の観点です。先に自分たちの施策を書いてから、このカルテで抜け漏れを確認してください。",
        mission=["自由記入欄に自分たちの作戦を書く", "その施策でどのKPIが変わるか予想する", "投稿後に検証するポイントを1つ決める"]
    )

# =========================
# CHECK
# =========================
if current_step == NAV_OPTIONS[1]:
    render_section_heading('ANALYTICS CHECK', '投稿後：YouTubeアナリティクスを入力する')
    with st.container():
        render_subheading("🎬 MV本体の実績")
        c1, c2, c3 = st.columns(3)
        with c1:
            act_views = st.number_input("視聴回数（回）", min_value=0, step=10, key="act_views")
            likes = st.number_input("高評価数", min_value=0, step=1, key="likes")
        with c2:
            act_imp = st.number_input("インプレッション数（回）", min_value=0, step=100, key="act_imp")
            comments = st.number_input("コメント数", min_value=0, step=1, key="comments")
        with c3:
            act_ctr = st.number_input("CTR（%）", min_value=0.0, max_value=100.0, step=0.1, key="act_ctr")
            subs = st.number_input("登録者増加数", min_value=0, step=1, key="subs")
        retention = st.slider("平均再生率（%）", min_value=0.0, max_value=100.0, step=1.0, key="retention")

    with st.container():
        render_subheading("📱 ショート・外部導線")
        c4, c5 = st.columns(2)
        with c4:
            short_views = st.number_input("連動ショートの最高視聴回数", min_value=0, step=50, key="short_views")
        with c5:
            sns_posts = st.number_input("SNS告知投稿数", min_value=0, step=1, key="sns_posts")

    yt_internal_views = int(act_imp * (act_ctr / 100))
    has_actual_data = any([
        act_views > 0,
        act_imp > 0,
        act_ctr > 0,
        retention > 0,
        likes > 0,
        comments > 0,
        subs > 0,
        short_views > 0,
        sns_posts > 0,
    ])
    is_data_error = has_actual_data and act_views < yt_internal_views
    external_views = 0 if is_data_error else max(act_views - yt_internal_views, 0)
    external_ratio = 0 if act_views == 0 or is_data_error else external_views / act_views * 100

    render_section_heading('KPI SNAPSHOT', '総合ステータス')

    if not has_actual_data:
        render_empty_status_panel()
        st.markdown(
            """
            <div class="advice-card">
                <div class="advice-kicker">START CHECK</div>
                <div class="advice-title">まずはYouTubeアナリティクスの実績数値を入力してください</div>
                <div class="result-badge neutral">入力前なので診断はまだ発動していません</div>
                <p>視聴回数・インプレッション数・インプレッションのクリック率（CTR）・平均再生率を入力すると、原因診断と次の一手が表示されます。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        main_problem = "実績データ未入力"
    elif is_data_error:
        st.markdown(f"""
        <div class="advice-card">
            <div class="advice-kicker">DATA CHECK</div>
            <div class="advice-title">⚠️ 入力データに矛盾があります</div>
            <div class="result-badge danger">視聴回数より、計算上のYouTube内視聴数が大きくなっています</div>
            <p>インプレッション <b>{act_imp:,}</b> × CTR <b>{act_ctr:.1f}%</b> = 推定 <b>{yt_internal_views:,}</b> 回です。視聴回数 <b>{act_views:,}</b> 回より大きいため、桁数・期間・別動画の数値混在を確認してください。</p>
        </div>
        """, unsafe_allow_html=True)
        main_problem = "入力データ確認"
    else:
        ctr_label, ctr_level = ctr_rank(act_ctr)
        ret_label, ret_level = retention_rank(retention)
        short_label, short_level, short_reason = short_rank(short_views)
        main_problem, main_reason = choose_main_problem(act_imp, act_ctr, retention, short_views, external_ratio)
        render_status_panel([
            ("視聴回数", f"{act_views:,} 回"),
            ("インプレッション由来の推定視聴回数", f"{yt_internal_views:,} 回"),
            ("外部・その他トラフィックの推定視聴回数", f"{external_views:,} 回（外部トラフィック比率：{external_ratio:.1f}%）"),
            ("サムネイル・タイトル訴求ランク", ctr_label),
            ("平均再生率ランク", ret_label),
            ("ショート視聴回数ランク", f"{short_label}：{short_reason}"),
            ("最大課題", f"{main_problem}：{main_reason}"),
        ])

        # Impression card
        if act_imp < 1000:
            render_card(
                "IMPRESSION CHECK", "1. インプレッション診断",
                "🟨 新規チャンネルの壁、出現中！まずはインプレッション数を増やすミッションです", "warning",
                "動画の魅力以前に、まだYouTube上で十分にインプレッションが発生していない状態です。",
                "YouTubeの検索とおすすめ機能に、動画のジャンルや内容がまだ十分に伝わっていない、または初期導線が弱くインプレッション機会が少ない可能性があります。",
                ["タイトルと概要欄に検索される言葉を追加する", "概要欄にフル歌詞と制作クレジットを書く", "ショート・SNS・再生リストから入口を増やす", "終了画面とカードでチャンネル内回遊を作る"],
                "⚠️ 半角#タグ、歌詞、クレジットは、YouTubeの検索・おすすめ機能に動画内容を伝えるための名刺です。ここが空欄だと、作品のジャンルや魅力が伝わりにくくなります。",
                ["概要欄を修正", "既存MVからショートを1本投稿", "終了画面を設定"]
            )
        else:
            render_card(
                "IMPRESSION CHECK", "1. インプレッション診断",
                "🟩 インプレッションは順調！検索・おすすめ機能で見つかる機会が増えています", "success",
                "インプレッション数は新規チャンネルとして十分に取れています。次はインプレッションのクリック率と平均再生率の勝負です。",
                "タイトル・概要欄・初動の反応により、YouTube上で視聴者に見つけてもらう機会が増え始めています。",
                ["インプレッションのクリック率（CTR）が低ければサムネイル改善", "視聴者維持率が低ければショートの切り出し位置や固定コメントを改善", "関連動画・プレイリストで回遊を伸ばす"],
                mission=["成功した流入元を確認", "次回のタイトル・タグ設計に反映"]
            )

        # CTR card
        if act_ctr >= 10:
            render_card(
                "THUMBNAIL CHECK", "2. サムネイル・タイトル診断（CTR）",
                "👑 神サムネ級！視聴者の親指を一瞬で止める入口設計です", "legendary",
                "CTRは非常に高く、サムネイルとタイトルが“見る前の期待”をうまく作れています。",
                "サムネイルの主役・文字量・色のコントラスト・タイトル冒頭の引きがうまく噛み合っています。これは入口設計の成功事例です。",
                ["なぜクリックされたのかを言語化する", "他メンバーのサムネ改善に横展開する", "このデザイン法則を次回のテンプレにする"],
                mission=["成功サムネの共通点を3つ書く", "チーム内で共有"]
            )
        elif act_ctr >= 4:
            render_card(
                "THUMBNAIL CHECK", "2. サムネイル・タイトル診断（CTR）",
                "🔥 強サムネ級！音楽ファンが押したくなる入口は作れています", "success",
                "インプレッションを受けた人のうち、一定数がクリックしています。サムネイルとタイトルは“押される入口”として機能しています。",
                "スマホ画面での視認性や、タイトル冒頭の分かりやすさが機能しています。次はクリック後の平均再生率やコメントなど、見た後の反応を伸ばす段階です。",
                ["良かったサムネ要素を維持する", "タイトルのキーワードを微調整する", "維持率が低ければショートの切り出し位置や固定コメントを改善する"],
                mission=["成功要素を1つ残す", "改善要素を1つだけ変える"]
            )
        else:
            render_card(
                "THUMBNAIL CHECK", "2. サムネイル・タイトル診断（CTR）",
                "🟥 サムネ改善チャンス！表示されているのに押されにくい状態です", "danger",
                "インプレッションは出ていますが、サムネイルとタイトルだけでは、視聴者にクリックする理由が伝わり切っていない状態です。",
                "サムネイルの文字が小さい、主役が小さい、色のコントラストが弱い、タイトル冒頭の引きが弱い、右下の時間表示に重要要素が被っている可能性があります。",
                ["サムネイルの文字を太く・短くする", "人物・キャラ・象徴的な絵を大きく配置する", "タイトル冒頭に強いキーワードを入れる", "伸びているメンバーのサムネと横比較する"],
                "⚠️ サムネの右下は再生時間表示に隠れます。重要な顔・文字・ロゴは中央〜左寄せがおすすめです。",
                ["サムネイルを差し替え", "タイトルを1案改善", "スマホサイズで再確認"]
            )

        # Retention card
        if retention >= 40:
            render_card(
                "RETENTION CHECK", "3. 視聴者維持率診断",
                f"{ret_label}！押した後もしっかり聴かれています", ret_level,
                "クリック後の離脱が少なく、曲やMVの構成が視聴者を引き留めています。",
                "MVそのものの見せ方や曲の世界観が、視聴者の期待と合っている可能性があります。",
                ["離脱が少ない場面を分析する", "サビ前後の演出をショートに切り出す", "成功した見せ方を次回MVにも応用する"],
                mission=["維持率が高い場面をメモ", "ショート化する候補を選ぶ"]
            )
        else:
            render_card(
                "RETENTION CHECK", "3. 視聴者維持率診断",
                f"{ret_label}。既存MVの見せ方・導線を整えるミッションです", ret_level,
                "サムネで興味を持たれても、視聴者の期待と動画内容にズレがある可能性があります。",
                "ここではMVを作り直すのではなく、アナリティクスで離脱ポイントを確認し、固定コメント・概要欄・ショート切り出し・SNS告知文で魅力の伝え方を調整します。",
                ["視聴者維持率グラフで離脱が大きい場面を確認する", "ショートではサビや強いフレーズを中心に切り出す", "固定コメントで本編の見どころや聴きどころを補足する", "タイトル・概要欄で曲の魅力が伝わる説明を足す"],
                mission=["離脱ポイントを1つ確認", "ショートで使うサビ部分を選ぶ", "固定コメントで見どころを補足"]
            )

        # Shorts card
        if short_views == 0:
            render_card(
                "SHORTS CHECK", "4. ショート視聴回数診断",
                "🟨 ショート未着手！無料広告チラシをまだ配っていません", "warning",
                "本編MVだけで新規チャンネルを伸ばすのは難易度高めです。ショートは認知の入口になります。",
                "YouTubeショート、TikTok、Instagramリールに既存MVの魅力的な部分を切り出すことで、まだチャンネルを知らない人に届く可能性が上がります。",
                ["サビなど印象的な15秒を縦型に切り出す", "固定テロップで『AIでMV作ってみた』などのフックを入れる", "固定コメントや概要欄から本編へ誘導する"],
                mission=["既存MVからサビ15秒を切り出す", "縦型9:16で書き出す", "本編リンクを固定コメントに入れる"]
            )
        elif short_views < 500:
            render_card(
                "SHORTS CHECK", "4. ショート視聴回数診断",
                f"🌱 ショート火種フェーズ！{short_views:,}回の反応は次の実験材料です", "warning",
                "まだ大爆発ではありませんが、ショート経由で見てもらえる可能性は見えています。ここで終わりではなく、切り口を変えてもう一度試す価値があります。",
                "ショートは一発勝負ではなく、サビ・強い歌詞・印象的な映像・タイトル違いなどを試して、どの入口が本編MVへつながるかを探す実験です。",
                ["切り出し位置を変えた別パターンを投稿する", "ショートのタイトルをより具体的にする", "固定コメントに本編MVリンクと一言おすすめ文を入れる", "投稿後24時間の反応を見て、次の切り出し候補を決める"],
                mission=["別の15秒候補を1つ選ぶ", "本編リンク付き固定コメントを作る", "次回のショート目標を設定する"]
            )
        elif short_views < 2000:
            render_card(
                "SHORTS CHECK", "4. ショート視聴回数診断",
                f"🔥 ショートが入口として機能中！{short_views:,}回はかなり良い火力です", "success",
                "本編MVをまだ知らない人に、ショート経由で作品が届き始めています。ここはしっかり喜んでOKです。",
                "次の勝負は、ショートで止まった視聴者を本編MVへ移動させる導線です。固定コメント・概要欄・チャンネル内の導線を整えると、再生回数アップにつながります。",
                ["伸びたショートの固定コメントに本編MVリンクを置く", "概要欄冒頭に『フルMVはこちら』を入れる", "同じ見どころの別尺・別テロップ版を投稿する", "伸びた理由をチーム内で共有する"],
                mission=["本編リンク導線を追加", "伸びた理由を1つ言語化", "第2弾ショートを企画"]
            )
        elif short_views < 10000:
            render_card(
                "SHORTS CHECK", "4. ショート視聴回数診断",
                f"🚀 ショート強いです！{short_views:,}回は本編MVへの強力な入口です", "success",
                "ショートがかなり広がっています。新規チャンネルとしては、これはかなりテンションを上げていい成果です。",
                "ここまで伸びたショートは、単なるおまけではなく本編MVへの広告塔です。導線を整え、続編や別切り出しで第2波を作りましょう。",
                ["固定コメント・概要欄・プロフィールから本編へ誘導する", "同じ曲の別シーンで続編ショートを投稿する", "伸びたショートをX・Instagramにも展開する", "コメント欄で本編の見どころを案内する"],
                mission=["本編誘導を3か所に設置", "続編ショートを1本企画", "SNSにも再展開"]
            )
        else:
            render_card(
                "SHORTS CHECK", "4. ショート視聴回数診断",
                f"👑 ショート覚醒！{short_views:,}回は完全に広告塔レベルです", "legendary",
                "このショートは、本編MVを知らない人を連れてくる強力な入口になっています。チーム内でも成功事例として共有したいレベルです。",
                "勢いがあるうちに本編MVへの導線を最大化し、続編・制作裏話・別サビ版で第2波、第3波を作るとチャンネル全体の伸びにつながります。",
                ["固定コメントで本編MVへ強く誘導する", "続編ショート・制作裏話ショートを投稿する", "チャンネル内の再生リストに本編MVを置く", "成功要因をテンプレ化して次回作品に使う"],
                mission=["本編導線を最優先で整備", "成功要因を3つ書く", "第2波ショートを投稿"]
            )

        # External traffic card
        if external_ratio < 15:
            render_card(
                "SNS CHECK", "5. 外部トラフィック診断",
                "🟨 外部トラフィックが弱め。YouTube内の検索・おすすめ頼みから一歩広げるタイミングです", "warning",
                "視聴の多くがYouTube内に偏っており、SNSからの初動ブーストが弱い状態です。",
                "XやInstagramでリンクだけを貼ると流れにくいため、動画付き投稿・制作裏話・引用リポストなどの工夫が必要です。ショートの素材も外部SNSに再利用できます。",
                ["XにはYouTubeリンクだけでなく動画ファイルも添付する", "チーム全員で引用リポストしてお祭り感を作る", "制作秘話やプロンプト紹介で第2波投稿をする", "伸びたショートをTikTok・Instagramリールにも展開する"],
                mission=["動画付き告知を1本投稿", "メンバー同士で引用リポスト", "本編URLをプロフィールか固定投稿に設置"]
            )
        else:
            render_card(
                "SNS CHECK", "5. 外部トラフィック診断",
                "👑 外部トラフィックが効いています！自力集客の導線が動き始めています", "legendary",
                "SNSや口コミから視聴者を呼び込めています。これはYouTube内の検索・おすすめ機能に頼りすぎない強い状態です。",
                "外部から来た視聴者がコメントや高評価を残すと、YouTube内での反応として次の発見機会にもつながる可能性があります。ショートで伸びた素材も、本編への入口としてさらに活用できます。",
                ["コメントには必ず返信する", "第2波投稿で制作裏話を出す", "次回予告を固定コメントに置く", "伸びたショートの続編を外部SNSにも出す"],
                mission=["コメント返信", "制作裏話をSNS投稿", "次回投稿への導線を作る"]
            )

# =========================
# ACTION & REPORT
# =========================
if current_step == NAV_OPTIONS[2]:
    render_section_heading('ACTION DESIGN', '改善アクションとPDCAレポート')

    action_recommendation = build_action_recommendations(
        has_actual_data_global,
        is_data_error,
        act_imp,
        act_ctr,
        retention,
        short_views,
        external_ratio,
    )

    with st.container(border=True):
        render_action_recommendation_panel(action_recommendation)

    with st.container(border=True):
        render_student_decision_panel()

        action_groups = [
            {
                "title": "📊 インプレッションのクリック率（CTR）改善：押される見た目に直す",
                "desc": "インプレッションはあるのにクリックされない時に、サムネイルとタイトルの入口設計を見直す改善です。",
                "items": [
                    "サムネイルを変更する",
                    "タイトルを変更する",
                    "他メンバーの高CTRサムネイルと比較する",
                ],
            },
            {
                "title": "🔎 インプレッション・SEO改善：検索・関連動画に強くする",
                "desc": "YouTubeの検索・おすすめ機能にジャンルや内容を伝え、インプレッション機会を増やす改善です。",
                "items": [
                    "概要欄・タグ・歌詞を修正する",
                    "終了画面・カード・再生リストを設定する",
                ],
            },
            {
                "title": "🎧 平均再生率改善：期待値と見どころを整える",
                "desc": "MVを作り直さず、視聴者維持率グラフや固定コメントで見せ方・導線を改善します。",
                "items": [
                    "視聴者維持率グラフで離脱ポイントを確認する",
                    "固定コメント・概要欄でMVの見どころを補足する",
                    "ショート動画の切り出し部分を見直す",
                    "ショート動画の切り出し部分を見直して別パターンを投稿する",
                    "ショートのタイトル・固定コメントから本編MVへ誘導する",
                ],
            },
            {
                "title": "📱 ショート活用：既存MVから入口を増やす",
                "desc": "MVを作り直さず、既存MVから見どころを切り出して新規視聴者に届けます。",
                "items": [
                    "既存MVからショート動画を切り出して新しく投稿する",
                    "ショートの固定コメント・概要欄から本編MVへ誘導する",
                    "伸びたショートの固定コメント・概要欄から本編MVへ誘導する",
                    "伸びたショートを本編MVへの導線として強化する",
                    "伸びたショートの別バージョンを追加投稿する",
                    "伸びたショートの続編・別切り出しを投稿する",
                ],
            },
            {
                "title": "🌐 外部トラフィック改善：YouTube外から視聴者を呼ぶ",
                "desc": "YouTube内の検索・おすすめ機能だけに頼らず、SNSやチーム拡散から初動を作る改善です。",
                "items": [
                    "X / Instagram / TikTokで告知する",
                    "チーム内で相互視聴・コメント・引用リポストを行う",
                ],
            },
            {
                "title": "🔁 回遊・ファン化改善：見た後の行動を増やす",
                "desc": "1本見て終わりにせず、次の動画・コメント・登録につなげる改善です。",
                "items": [
                    "コメント返信・固定コメントでファン化する",
                    "成功要因を言語化して次回の投稿に再利用する",
                ],
            },
            {
                "title": "🧪 データ確認：正しい数値で判断する",
                "desc": "数値の期間や桁に矛盾がある時に先に行う確認です。",
                "items": [
                    "YouTubeアナリティクスの対象期間・対象動画・桁数を確認する",
                ],
            },
        ]
        next_actions = checkbox_grouped(
            "おすすめを参考に、実際に行う改善アクションを複数選んでください",
            action_groups,
            default_selected=[],
            key_prefix="next_action_grouped_v24",
            recommendation_map=action_recommendation.get("recommended_map", {}),
        )
        st.session_state["_next_actions_cache"] = next_actions
        render_selected_grouped_list("選択中の改善アクション", action_groups, next_actions)

        render_subheading("🧠 選んだ理由")
        action_reason = st.text_area(
            "なぜその改善アクションを選びましたか？",
            placeholder="例：インプレッションはあるのにCTRが低かったため、まずはサムネイルとタイトルの入口改善を優先する。",
            key="action_reason",
        )

        render_subheading("📌 次回検証するKPI")
        kpi_options = [
            "インプレッションのクリック率（CTR）",
            "インプレッション",
            "平均再生率",
            "視聴回数",
            "コメント数",
            "登録者増加数",
            "外部トラフィック比率",
            "ショート視聴回数",
        ]
        next_kpi = st.radio(
            "次回、重点的に見るKPIを選んでください",
            kpi_options,
            horizontal=False,
            key="next_kpi",
        )
        next_goal = st.text_input("次回目標", placeholder="例：CTR 4.5% → 6.0%", key="next_goal")
        reflection = st.text_area("今回わかったこと", placeholder="例：サムネの文字が小さいとスマホで目立たず、CTRが下がるとわかった", key="reflection")
        next_hypothesis = st.text_area("次回の仮説", placeholder="例：サムネの文字を太くして、タイトル冒頭に『AI MV』を入れればCTRが上がるはず", key="next_hypothesis")

    try:
        if is_data_error:
            main_problem = "入力データ確認"
        elif not has_actual_data_global:
            main_problem = "実績データ未入力"
        else:
            main_problem, _ = choose_main_problem(act_imp, act_ctr, retention, short_views, external_ratio)
        report_text = make_report(
            student_name, video_title, hypothesis, target_audience, planned_actions, target_views, target_ctr,
            act_views, act_imp, act_ctr, retention, likes, comments, subs, short_views,
            external_views, external_ratio, main_problem, next_actions, next_kpi, next_goal, action_reason, reflection, next_hypothesis
        )
    except NameError:
        report_text = "先に『投稿前 Plan』と『投稿後 Check』の数値を入力してください。"

    render_section_heading('REPORT OUTPUT', '自動生成PDCAレポート')
    st.text_area("コピーして提出用レポートに使えます", value=report_text, height=420)
    st.download_button(
        "📥 PDCAレポートをテキストで保存",
        data=report_text.encode("utf-8"),
        file_name="ai_mv_pdca_report.txt",
        mime="text/plain"
    )

    render_section_heading('FINAL SHARE', '最終発表用まとめ')
    st.markdown(
        """
        <div class="plain-paragraph-block">
            長期間使う場合は、このセクションだけ見れば発表準備ができるように、
            <b>発表用メモの入力</b>と<b>発表用まとめの出力</b>をここに集約しています。<br>
            発表項目は、<b>作品紹介 → 工夫 → 試したこと → 数字 → 分かったこと → 学び</b>の順で整理すると伝わりやすくなります。
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_subheading("📝 発表用メモ入力")
    presentation_work_intro = st.text_area(
        "作品紹介で伝えたいこと",
        placeholder="例：明るいシティポップ調のAI楽曲に、放課後の映像を合わせた青春系MVです。",
        key="presentation_work_intro",
    )
    presentation_posting_tips = st.text_area(
        "チャンネル・投稿の工夫",
        placeholder="例：タイトルの冒頭にAI MVと入れ、サムネイルでは曲の世界観が一目で伝わるようにした。",
        key="presentation_posting_tips",
    )
    presentation_success = st.text_area(
        "成功事例・共有したい工夫",
        placeholder="例：ショートの固定コメントに本編URLを置いたことで、本編への導線を作れた。",
        key="presentation_success",
    )
    team_learning = st.text_area(
        "チームで学んだこと",
        placeholder="例：再生回数だけでなく、インプレッションやCTRを見ると改善すべき場所が分かると学んだ。",
        key="team_learning",
    )

    try:
        presentation_text = make_presentation_summary(
            student_name, video_title, presentation_work_intro, presentation_posting_tips,
            planned_actions, act_views, act_imp, act_ctr, retention, likes, comments,
            subs, short_views, external_ratio, main_problem, reflection,
            presentation_success, team_learning, next_actions
        )
    except NameError:
        presentation_text = "先に『投稿前 Plan』『投稿後 Check』『改善 Action』の内容を入力してください。"

    render_subheading("📋 発表用まとめ出力")
    st.text_area("発表スライド作成の下書きに使えます", value=presentation_text, height=520)
    st.download_button(
        "📥 最終発表メモをテキストで保存",
        data=presentation_text.encode("utf-8"),
        file_name="ai_mv_final_presentation_memo.txt",
        mime="text/plain"
    )
