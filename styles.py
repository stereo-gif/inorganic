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


def apply_styles(dark_mode: bool = False):
    if dark_mode:
        bg_page = "#0b1120"
        bg_card = "#111827"
        bg_hero = "linear-gradient(135deg, #111827 0%, #1e1b4b 100%)"
        border_col = "#1f2937"
        text_main = "#f8fafc"
        text_muted = "#94a3b8"
        pill_opt_bg = "rgba(245, 158, 11, 0.16)"
        pill_opt_text = "#fbbf24"
        pill_opt_border = "rgba(251, 191, 36, 0.35)"
        pill_ach_bg = "rgba(14, 165, 233, 0.16)"
        pill_ach_text = "#38bdf8"
        pill_ach_border = "rgba(56, 189, 248, 0.35)"
    else:
        bg_page = "#f8fafc"
        bg_card = "#ffffff"
        bg_hero = "linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%)"
        border_col = "#e2e8f0"
        text_main = "#0f172a"
        text_muted = "#475569"
        pill_opt_bg = "#fef3c7"
        pill_opt_text = "#92400e"
        pill_opt_border = "#fcd34d"
        pill_ach_bg = "#e0f2fe"
        pill_ach_text = "#075985"
        pill_ach_border = "#7dd3fc"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {bg_page};
            color: {text_main};
        }}
        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 2.5rem;
            padding-left: 1.1rem;
            padding-right: 1.1rem;
            max-width: 1120px;
        }}
        .hero-card {{
            background: {bg_hero};
            border: 1px solid {border_col};
            border-radius: 18px;
            padding: 1.15rem 1.3rem;
            margin-bottom: 0.9rem;
        }}
        .hero-title {{
            font-size: 1.45rem;
            font-weight: 800;
            color: {text_main};
            margin: 0 0 0.25rem 0;
        }}
        .hero-sub {{
            font-size: 0.92rem;
            color: {text_muted};
            margin: 0;
            line-height: 1.55;
        }}
        .legend-strip {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            background: {bg_card};
            border: 1px solid {border_col};
            border-radius: 14px;
            padding: 0.65rem 0.9rem;
            margin-bottom: 1rem;
            font-size: 0.8rem;
            color: {text_muted};
        }}
        .legend-item {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.15rem 0.5rem;
            border-radius: 999px;
            background: {bg_page};
            border: 1px solid {border_col};
            color: {text_main};
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
            background-color: {bg_card};
            border: 1px solid {border_col};
            border-radius: 14px;
            padding: 0.75rem 0.9rem;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 0.78rem !important;
            color: {text_muted} !important;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: {text_main} !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 16px !important;
            border-color: {border_col} !important;
            background-color: {bg_card} !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
            padding: 0.45rem !important;
        }}
        .type-pill-opt {{
            display: inline-block;
            background-color: {pill_opt_bg};
            color: {pill_opt_text};
            border: 1px solid {pill_opt_border};
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }}
        .type-pill-ach {{
            display: inline-block;
            background-color: {pill_ach_bg};
            color: {pill_ach_text};
            border: 1px solid {pill_ach_border};
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }}
        div[role="radiogroup"] label {{
            background: {bg_card};
            border: 1px solid {border_col};
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
            .hero-sub {{
                font-size: 0.85rem;
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
            <p class="hero-sub">
                حساب الأيزومرات الهندسية والبصرية وعرض أسمائها وتسمياتها ورسومها ثلاثية الأبعاد بوضوح على الموبايل والكمبيوتر.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_legend_strip():
    st.markdown(
        """
        <div class="legend-strip">
            <span class="legend-item"><b>M</b> الفلز المركزي</span>
            <span class="legend-item"><span class="dot-chelate"></span> قوس Chelate يربط طرفي Bidentate</span>
            <span class="legend-item">Optical = كيرالي (له نظير مرآتي)</span>
            <span class="legend-item">Achiral = غير كيرالي</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_type_pill(is_optical, pair_label=None):
    if is_optical:
        suffix = f" · {pair_label}" if pair_label else ""
        return f'<span class="type-pill-opt">Optical Isomer{suffix}</span>'
    return '<span class="type-pill-ach">Achiral Isomer (No Optical Enantiomer)</span>'
