import streamlit as st
import geopandas as gpd
import zipfile

# Configuração da página
st.set_page_config(page_title="Analisador Geo-Pro", layout="wide", page_icon="🌍")

# --- LÓGICA DE LOGIN ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

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
                else:
                    st.error("Dados incorretos.")
        return False
    return True

# --- ÁREA PRINCIPAL ---
if check_password():
    st.title("🌍 Analisador de Passivos Ambientais")
    
    with st.sidebar:
        st.header("📂 Configurações")
        st.write("Usuário: Gabriel Palheta")
        if st.button("Sair"):
            st.session_state["auth"] = False
            st.rerun()
            
        f_c = st.file_uploader("Upload do CAR (ZIP)", type="zip")
        f_p = st.file_uploader("Upload do PRODES (ZIP)", type="zip")
        # Definimos o botão AQUI, dentro do bloco que só roda se logado
        processar = st.button("🚀 Iniciar Processamento")

    # A verificação agora acontece após a definição do botão
    if processar:
        if f_c and f_p:
            with st.spinner("Processando..."):
                try:
                    # Função de leitura
                    def ler(f):
                        with zipfile.ZipFile(f, 'r') as z:
                            shp = [name for name in z.namelist() if name.endswith('.shp')][0]
                            with z.open(shp) as file:
                                return gpd.read_file(file, engine='pyogrio')
                    
                    g_c = ler(f_c)
                    g_p = ler(f_p)
                    
                    if g_c.crs != g_p.crs:
                        g_c = g_c.to_crs(g_p.crs)
                    
                    resultado = gpd.overlay(g_c, g_p, how='intersection')
                    st.success(f"Concluído! {len(resultado)} intersecções.")
                    st.dataframe(resultado)
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.warning("Por favor, envie ambos os arquivos ZIP.")
