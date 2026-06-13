import streamlit as st
import geopandas as gpd
import zipfile
import io
import pandas as pd

st.set_page_config(page_title="Analisador Geo-Pro", layout="wide")

# --- Lógica de Login (Sua estrutura original) ---
if "auth" not in st.session_state: st.session_state["auth"] = False

def check_password():
    if not st.session_state["auth"]:
        with st.sidebar:
            user = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                if user == "gabriel.palheta" and password == "Gab1914":
                    st.session_state["auth"] = True
                    st.rerun()
        return False
    return True

# --- Função de Busca Profunda (Corrige o problema das pastas) ---
def carregar_shape_profundo(zip_file):
    gdfs = []
    with zipfile.ZipFile(zip_file, 'r') as z:
        for nome in z.namelist():
            if nome.endswith('.zip'):
                with z.open(nome) as sub:
                    # Lê o sub-zip na memória
                    sub_data = io.BytesIO(sub.read())
                    try:
                        gdf = gpd.read_file(sub_data)
                        gdfs.append(gdf)
                    except: continue
            elif nome.endswith('.shp'):
                # Caso o arquivo esteja solto ou no nível principal
                gdf = gpd.read_file(z.open(nome))
                gdfs.append(gdf)
    return pd.concat(gdfs) if gdfs else None

# --- Estrutura Original do Site ---
if check_password():
    st.title("🌍 Analisador de Passivos Ambientais")
    
    with st.sidebar:
        f_c = st.file_uploader("Upload do CAR (ZIP)", type="zip")
        f_p = st.file_uploader("Upload do PRODES (ZIP)", type="zip")
        processar = st.button("🚀 Processar Análise Exata")

    # A verificação deve ficar AQUI, depois dos objetos criados
    if processar:
        if f_c and f_p:
            with st.spinner("Processando..."):
                try:
                    # Carrega ambos usando a busca profunda
                    g_c = carregar_shape_profundo(f_c)
                    g_p = carregar_shape_profundo(f_p)
                    
                    if g_c.crs != g_p.crs: g_c = g_c.to_crs(g_p.crs)
                    
                    resultado = gpd.overlay(g_c, g_p, how='intersection')
                    st.success("Análise concluída com precisão!")
                    st.dataframe(resultado)
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
        else:
            st.warning("Por favor, suba os arquivos ZIP.")
