import streamlit as st
import geopandas as gpd
import zipfile
import io

st.set_page_config(page_title="Analisador Geo-Pro", layout="wide")

# 1. Login e Sidebar (Mantidos como você gosta)
if "auth" not in st.session_state: st.session_state["auth"] = False

def check_password():
    if not st.session_state["auth"]:
        with st.sidebar:
            st.header("🔐 Acesso Restrito")
            user = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                if user == "gabriel.palheta" and password == "Gab1914":
                    st.session_state["auth"] = True
                    st.rerun()
        return False
    return True

# 2. Função de leitura "à prova de erros"
def ler_shp_direto(uploaded_file):
    # Usa o caminho direto para ler dentro do zip sem extrair tudo na memória
    return gpd.read_file(f"zip://{uploaded_file.name}", engine='pyogrio')

# 3. Interface Principal
if check_password():
    st.title("🌍 Analisador de Passivos Ambientais")
    
    with st.sidebar:
        st.header("📂 Configurações")
        if st.button("Sair"):
            st.session_state["auth"] = False
            st.rerun()
        
        f_c = st.file_uploader("Upload do CAR (ZIP)", type="zip")
        f_p = st.file_uploader("Upload do PRODES (ZIP)", type="zip")
        processar = st.button("🚀 Iniciar Processamento")

    if processar:
        if f_c and f_p:
            with st.spinner("Processando dados geográficos..."):
                try:
                    # Tenta ler os arquivos diretamente via protocolo zip:// do Geopandas
                    g_c = ler_shp_direto(f_c)
                    g_p = ler_shp_direto(f_p)
                    
                    if g_c.crs != g_p.crs:
                        g_c = g_c.to_crs(g_p.crs)
                    
                    resultado = gpd.overlay(g_c, g_p, how='intersection')
                    st.success(f"Cruzamento concluído! {len(resultado)} intersecções.")
                    st.dataframe(resultado)
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
                    st.info("Dica: Se o arquivo for muito grande ou complexo, tente exportar um arquivo único (.parquet) pelo QGIS.")
        else:
            st.warning("Por favor, envie ambos os arquivos ZIP.")
