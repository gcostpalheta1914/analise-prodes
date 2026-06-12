import streamlit as st
import geopandas as gpd
import pandas as pd
import io
import zipfile

# Configuração de página profissional
st.set_page_config(page_title="Analisador Geo-Pro", layout="wide", page_icon="🌍")

# Estilização CSS para deixar os botões e tabelas mais bonitos
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #0083B8; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Lógica de Login na Sidebar
def check_password():
    with st.sidebar:
        st.header("🔐 Login")
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if user == "gabriel.palheta" and password == "Gab1914":
            st.session_state["auth"] = True
            return True
    return st.session_state.get("auth", False)

# --- ÁREA PRINCIPAL ---
if not check_password():
    st.title("Bem-vindo ao Analisador Geo-Pro")
    st.info("Por favor, faça login na barra lateral para acessar o sistema.")
else:
    st.title("🌍 Analisador de Passivos Ambientais")
    st.subheader("Cruzamento Espacial Automatizado: CAR vs PRODES")

    with st.sidebar:
        st.header("📂 Configurações")
        f_c = st.file_uploader("Upload do CAR (ZIP)", type="zip")
        f_p = st.file_uploader("Upload do PRODES (ZIP)", type="zip")
        processar = st.button("🚀 Iniciar Processamento")

    if processar and f_c and f_p:
        with st.spinner("Realizando cruzamento espacial complexo..."):
            try:
                # Função de leitura rápida
                def ler(f):
                    with zipfile.ZipFile(f, 'r') as z:
                        shp = [f for f in z.namelist() if f.endswith('.shp')][0]
                        with z.open(shp) as f: return gpd.read_file(f, engine='pyogrio')
                
                g_c, g_p = ler(f_c), ler(f_p)
                if g_c.crs != g_p.crs: g_c = g_c.to_crs(g_p.crs)
                
                res = gpd.overlay(g_c, g_p, how='intersection')
                
                # Exibição Profissional
                st.success(f"Cruzamento realizado com sucesso! {len(res)} intersecções encontradas.")
                
                tab1, tab2 = st.tabs(["📊 Dados", "🗺️ Mapa Visual"])
                with tab1:
                    st.dataframe(res.head(100), use_container_width=True)
                with tab2:
                    st.map(res)
                    
            except Exception as e:
                st.error(f"Erro no processamento: {e}")
    elif processar:
        st.warning("Envie ambos os arquivos para iniciar.")
