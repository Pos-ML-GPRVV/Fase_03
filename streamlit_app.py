# streamlit_app.py
import os
import json
import streamlit as st

# --- NOSSAS LIBS (novo caminho) ---
from app_lib.theme import inject_base_css, PALETTE
from pages.overview import render_overview
from pages.decomposition import render_decomposition
from pages.whatif import render_whatif

st.set_page_config(page_title="IPCA Dashboard", layout="wide")
inject_base_css()  # mantém exatamente o visual anterior

# ===== título visível (não some) =====
st.markdown("<div class='top-title'>IPCA — Dashboard</div>", unsafe_allow_html=True)

# ===================== Sidebar =====================
with st.sidebar:
    st.markdown("### Configuração da API")
    api_url = st.text_input("API URL", value=os.getenv("API_URL", "http://127.0.0.1:8000"))
    api_key = st.text_input("Api-Key", value=os.getenv("API_KEY", "senha123"), type="password")
    if st.button("Salvar configuração"):
        st.session_state["API_URL"] = api_url.strip().rstrip("/")
        st.session_state["API_KEY"] = api_key.strip()
        st.success("Configuração salva nesta sessão.")
        st.rerun()

# ===================== Abas =====================
tab_overview, tab_features, tab_predict = st.tabs(["Visão Geral", "Decomposição", "Previsão"])

with tab_overview:
    render_overview()

with tab_features:
    render_decomposition()

with tab_predict:
    render_whatif()
