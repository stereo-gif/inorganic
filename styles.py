"""
Styling & Mobile-Responsive UI Helpers for Inorganic Chemistry Isomerism Solver
"""

import streamlit as st

LIGAND_COLORS = [
    "#E15759",
    "#4E79A7",
    "#59A14F",
    "#F28E2B",
    "#B07AA1",
    "#76B7B2",
    "#EDC948",
    "#FF9DA7",
]

OPTICAL_BADGE_COLOR = "#B45309"
ACHIRAL_BADGE_COLOR = "#0369A1"

CHELATE_ARC_PRIMARY = "#7C3AED"
CHELATE_ARC_SECONDARY = "#DB2777"

BG_PAGE = "#f8fafc"
BG_CARD = "#ffffff"
BG_HERO = "linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%)"
BORDER_COL = "#e2e8f0"
TEXT_MAIN = "#0f172a"
TEXT_MUTED = "#475569"
PILL_OPT_BG = "#fef3c7"
PILL_OPT_TEXT = "#92400e"
PILL_OPT_BORDER = "#fcd34d"
PILL_ACH_BG = "#e0f2fe"
PILL_ACH_text = "#075985"
PILL_ACH_BORDER = "#7dd3fc"


def apply_styles():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {BG_PAGE};
            color: {TEXT_MAIN};
        }}
        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 2.5rem;
            padding-left: 1.1rem;
            padding-right: 1.1rem;
            max-width: 1120px;
        }}
        .hero-card {{
            background: {BG_HERO};
            border: 1px solid {BORDER_COL};
            border-radius: 18px;
            padding: 1.15rem 1.3rem;
            margin-bottom: 0.9rem;
        }}
        .hero-title {{
            font-size: 1.45rem;
            font-weight: 800;
            color: {TEXT_MAIN};
            margin: 0;
        }}
        .legend-strip {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            background: {BG_CARD};
            border: 1px solid {BORDER_COL};
            border-radius: 14px;
            padding: 0.65rem 0.9rem;
            margin-bottom: 1rem;
            font-size: 0.8rem;
            color: {TEXT_MUTED};
        }}
        .legend-item {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.15rem 0.5rem;
            border-radius: 999px;
            background: {BG_PAGE};
            border: 1px solid {BORDER_COL};
            color: {TEXT_MAIN};
            font-weight: 600;
        }}
        .dot-chelate {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: {CHELATE_ARC_PRIMARY};
            display: inline-block;
        }}
        [data-testid="stMetric"] {{
            background-color: {BG_CARD};
            border: 1px solid {BORDER_COL};
            border-radius: 14px;
            padding: 0.75rem 0.9rem;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 0.78rem !important;
            color: {TEXT_MUTED} !important;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: {TEXT_MAIN} !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 16px !important;
            border-color: {BORDER_COL} !important;
            background-color: {BG_CARD} !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
            padding: 0.45rem !important;
        }}
        .type-pill-opt {{
            display: inline-block;
            background-color: {PILL_OPT_BG};
            color: {PILL_OPT_TEXT};
            border: 1px solid {PILL_OPT_BORDER};
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }}
        .type-pill-ach {{
            display: inline-block;
            background-color: {PILL_ACH_BG};
            color: {PILL_ACH_text};
            border: 1px solid {PILL_ACH_BORDER};
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }}
        div[role="radiogroup"] label {{
            background: {BG_CARD};
            border: 1px solid {BORDER_COL};
            border-radius: 12px;
            padding: 0.45rem 0.8rem;
            margin-right: 0.4rem;
        }}
        @media (max-width: 640px) {{
            .block-container {{
                padding-top: 0.9rem;
                padding-left: 0.75rem;
                padding-right: 0.75rem;
            }}
            .hero-title {{
                font-size: 1.22rem;
            }}
            [data-testid="stMetricValue"] {{
                font-size: 1.15rem !important;
            }}
            [data-testid="stHorizontalBlock"] {{
                flex-direction: column !important;
                gap: 0.65rem !important;
            }}
            [data-testid="stHorizontalBlock"] > div {{
                width: 100% !important;
                flex: 1 1 100% !important;
            }}
            div[role="radiogroup"] {{
                display: flex;
                flex-direction: column;
                gap: 0.4rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div class="hero-card">
            <p class="hero-title">🧪 Inorganic Chemistry Isomerism Solver</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_legend_strip():
    st.markdown(
        """
        <div class="legend-strip">
            <span class="legend-item"><b>M</b> Central metal</span>
            <span class="legend-item"><span class="dot-chelate"></span> Chelate arc connecting bidentate donor ends</span>
            <span class="legend-item">Optical = Chiral (has a mirror-image enantiomer)</span>
            <span class="legend-item">Achiral = No non-superimposable mirror image</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_type_pill(is_optical, pair_label=None):
    if is_optical:
        suffix = f" · {pair_label}" if pair_label else ""
        return f'<span class="type-pill-opt">Optical Isomer{suffix}</span>'
    return '<span class="type-pill-ach">Achiral Isomer (No Optical Enantiomer)</span>'
    
