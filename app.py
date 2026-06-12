import streamlit as st
import geopandas as gpd
import zipfile
import pyogrio

st.set_page_config(page_title="Analisador Geo-Pro", layout="wide")

# Lógica de Login
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

# Função de leitura "à prova de falhas" para arquivos com subpastas
def ler_shp_seguro(uploaded_file):
    with zipfile.ZipFile(uploaded_file, 'r') as z:
        # Encontra o primeiro arquivo .shp em qualquer lugar do zip
        shp_files = [f for f in z.namelist() if f.endswith('.shp')]
        if not shp_files:
            raise Exception("Não encontrei arquivo .shp no ZIP.")
        
        # Lê usando a sintaxe vsi (necessária para ler dentro de zips)
        return gpd.read_file(f"zip://{uploaded_file.name}!{shp_files[0]}", engine='pyogrio')

# Interface Principal
if check_password():
    st.title("🌍 Analisador de Passivos Ambientais")
    
    with st.sidebar:
        st.write("Bem-vindo, Gabriel Palheta.")
        f_c = st.file_uploader("Suba o arquivo CAR (ZIP)", type="zip")
        f_p = st.file_uploader("Suba o arquivo PRODES (ZIP)", type="zip")
        processar = st.button("🚀 Iniciar Processamento")

    if processar:
        if f_c and f_p:
            with st.spinner("Processando..."):
                try:
                    g_c = ler_shp_seguro(f_c)
                    g_p = ler_shp_seguro(f_p)
                    
                    if g_c.crs != g_p.crs: g_c = g_c.to_crs(g_p.crs)
                    
                    inter = gpd.overlay(g_c, g_p, how='intersection')
                    st.success(f"Cruzamento concluído! {len(inter)} registros encontrados.")
                    st.dataframe(inter)
                except Exception as e:
                    st.error(f"Erro no processamento: {e}")
        else:
            st.warning("Por favor, suba os dois arquivos para começar.")
