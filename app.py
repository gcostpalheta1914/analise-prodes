import streamlit as st
import geopandas as gpd
import zipfile
import pyogrio

st.set_page_config(page_title="Analisador Geo-Pro", layout="wide")

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

# Lógica robusta para encontrar o .shp em qualquer subpasta
def ler_shp_seguro(uploaded_file):
    with zipfile.ZipFile(uploaded_file, 'r') as z:
        # Lista todos os arquivos e busca pelo .shp
        todos_arquivos = z.namelist()
        shp_file = next((f for f in todos_arquivos if f.endswith('.shp')), None)
        
        if not shp_file:
            raise Exception(f"Não achei nenhum .shp. Arquivos no ZIP: {todos_arquivos[:5]}...")
        
        # Lê usando a conexão VSI do GDAL/pyogrio
        return gpd.read_file(f"zip://{uploaded_file.name}!{shp_file}", engine='pyogrio')

if check_password():
    st.title("🌍 Analisador de Passivos Ambientais")
    
    with st.sidebar:
        f_c = st.file_uploader("Suba o arquivo CAR (ZIP)", type="zip")
        f_p = st.file_uploader("Suba o arquivo PRODES (ZIP)", type="zip")
        processar = st.button("🚀 Iniciar Processamento")

    if processar:
        if f_c and f_p:
            try:
                with st.spinner("Processando..."):
                    g_c = ler_shp_seguro(f_c)
                    g_p = ler_shp_seguro(f_p)
                    
                    if g_c.crs != g_p.crs:
                        g_c = g_c.to_crs(g_p.crs)
                    
                    inter = gpd.overlay(g_c, g_p, how='intersection')
                    st.success(f"Sucesso! {len(inter)} áreas cruzadas.")
                    st.dataframe(inter)
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.warning("Suba os arquivos.")
