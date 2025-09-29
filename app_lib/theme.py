# app_lib/theme.py
import streamlit as st

PALETTE = {
    "accent": "#F2600C",
    "accent_dark": "#A62F03",
    "bg": "#1F1F1F",
    "panel": "#000000",
    "text": "#F2F2F2",
    "muted": "#CFCFCF",
    "border": "#2A2A2A",
    "grid": "#2E2E2E",
}

def inject_base_css():
    st.markdown(
        f"""
        <style>
        :root {{
            --accent: {PALETTE["accent"]};
            --accent-dark: {PALETTE["accent_dark"]};
            --bg: {PALETTE["bg"]};
            --panel: {PALETTE["panel"]};
            --text: {PALETTE["text"]};
            --muted: {PALETTE["muted"]};
            --border: {PALETTE["border"]};
        }}
        header[data-testid="stHeader"] {{ display: none; }}
        .block-container {{ padding-top: 2.2rem; }}
        .stApp {{ background-color: var(--bg); color: var(--text); }}

        section[data-testid="stSidebar"] > div {{
            background: var(--panel);
            border-right: 1px solid var(--border);
        }}

        .stButton > button {{
            background: var(--accent);
            color: #fff;
            border: none;
            border-radius: 10px;
            font-weight: 800;
            letter-spacing: .2px;
            padding: .6rem 1rem;
            transition: all .15s ease-in-out;
        }}
        .stButton > button:hover {{
            background: var(--accent-dark);
            transform: translateY(-1px);
        }}

        [data-baseweb="tab-list"] {{ gap: .5rem; }}
        [data-baseweb="tab"] {{
            background: var(--panel);
            color: var(--text);
            border: 1px solid var(--border);
            border-bottom: none;
            border-radius: 10px 10px 0 0;
            padding: .5rem 1rem;
        }}
        [data-baseweb="tab"][aria-selected="true"] {{
            border-bottom: 3px solid var(--accent);
            color: #fff;
            font-weight: 800;
        }}

        .top-title {{
            font-size: 3.5rem;
            font-weight: 900;
            color: var(--text);
            margin: 0 0 .8rem 0;
            display: flex;
            align-items: center;
            gap: .6rem;
        }}
        .top-title::after {{
            content: "";
            width: 10px;
            height: 10px;
            background: var(--accent);
            display: inline-block;
            border-radius: 50%;
        }}

        /* ↑ fontes maiores dos subtítulos e labels */
        .block-container h2,
        .block-container h3 {{
          font-size: 1.85rem !important;
          line-height: 1.15 !important;
          font-weight: 900 !important;
        }}
        label[data-testid="stWidgetLabel"] > div > p {{
          font-size: 1.2rem !important;
          font-weight: 800 !important;
          color: var(--text) !important;
          margin-bottom: .25rem !important;
        }}

        .stDataFrame div::-webkit-scrollbar {{ height: 10px; width: 10px; }}
        .stDataFrame div::-webkit-scrollbar-thumb {{ background: #444; border-radius: 10px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
