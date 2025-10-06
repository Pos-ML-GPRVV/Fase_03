import os
import streamlit as st

from app_lib.theme import inject_base_css, PALETTE
from pages.overview import render_overview
from pages.decomposition import render_decomposition
from pages.whatif import render_whatif

AWS_API_DEFAULT = "http://100.25.177.110:8000"   
API_KEY_DEFAULT = "senha123"                     

# Se existir variável de ambiente, ela tem prioridade sobre o default fixo
ENV_API_URL = os.getenv("API_URL", AWS_API_DEFAULT).rstrip("/")
ENV_API_KEY = os.getenv("API_KEY", API_KEY_DEFAULT)

# Inicializa valores na sessão (uma vez) para que os módulos usem st.session_state
if "API_URL" not in st.session_state:
    st.session_state["API_URL"] = ENV_API_URL
if "API_KEY" not in st.session_state:
    st.session_state["API_KEY"] = ENV_API_KEY

# ===================== Página =====================
st.set_page_config(page_title="IPCA Dashboard", layout="wide")
inject_base_css()  # mantém exatamente o visual anterior

st.markdown("<div class='top-title'>IPCA — Dashboard</div>", unsafe_allow_html=True)

# ===================== Sidebar =====================
with st.sidebar:
    st.markdown("### Configuração da API")
    api_url = st.text_input(
        "API URL",
        value=st.session_state["API_URL"], 
        help="Ex.: http://100.25.177.110:8000",
    )
    api_key = st.text_input(
        "Api-Key",
        value=st.session_state["API_KEY"],
        type="password",
    )
    if st.button("Salvar configuração"):
        st.session_state["API_URL"] = api_url.strip().rstrip("/")
        st.session_state["API_KEY"] = api_key.strip()
        st.success(f"Configuração salva para esta sessão: {st.session_state['API_URL']}")
        st.rerun()

# ===================== Abas =====================
tab_overview, tab_features, tab_predict = st.tabs(
    ["Visão Geral", "Decomposição", "Previsão"]
)

with tab_overview:
    render_overview()

with tab_features:
    render_decomposition()

with tab_predict:
    render_whatif()
