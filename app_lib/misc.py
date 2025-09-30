# app_lib/misc.py
import re
import pandas as pd
import streamlit as st
from app_lib.theme import PALETTE

def parse_month_any(x):
    if pd.isna(x):
        return pd.NaT
    s = str(x).strip()
    for fmt in ("%Y-%m", "%Y-%m-%d"):
        try:
            return pd.to_datetime(s, format=fmt)
        except Exception:
            pass
    for rx, fmt in [(r"\d{4}", "%Y-%m"), (r"\d{6}", "%Y%m"), (r"\d{8}", "%Y%m%d")]:
        if re.fullmatch(rx, s):
            try:
                base = s if fmt != "%Y-%m" else s + "-01"
                return pd.to_datetime(base, format=fmt)
            except Exception:
                pass
    return pd.to_datetime(s, errors="coerce")

def metric_card(title: str, value: str):
    st.markdown(
        f"""
        <div style="background: {PALETTE['panel']}; border:1px solid {PALETTE['border']};
                    border-radius:16px; padding:18px 20px; margin-bottom:12px;">
          <div style="color:{PALETTE['accent']}; font-weight:900; letter-spacing:.3px;
                      font-size:22px; margin-bottom:6px;">
            {title}
          </div>
          <div style="color:{PALETTE['text']}; font-weight:900; font-size:42px; line-height:1.1;">
            {value}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
