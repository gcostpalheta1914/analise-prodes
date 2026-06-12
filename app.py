import streamlit as st
import geopandas as gpd
import zipfile

st.set_page_config(page_title="Analisador Geo-Pro", layout="wide", page_icon="🌍")

# --- LÓGICA DE LOGIN ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False

    if not st.session_state["auth"]:
        # Exibe o login apenas se NÃO estiver logado
        with st.sidebar:
            st.header("🔐 Acesso Restrito")
            user = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                if user == "gabriel.palheta" and password == "Gab1914":
                    st.session_state["auth"] = True
                    st.rerun() # Recarrega a página para sumir com os campos
                else:
                    st.error("Dados incorretos.")
        return False
    return True

# --- ÁREA PRINCIPAL ---
if check_password():
    # O conteúdo abaixo só aparece se estiver logado
    st.title("🌍 Analisador de Passivos Ambientais")
    
    with st.sidebar:
        st.header("📂 Configurações")
        st.write("Bem-vindo, Gabriel Palheta.")
        if st.button("Sair"): # Botão para deslogar
            st.session_state["auth"] = False
            st.rerun()
            
        f_c = st.file_uploader("Upload do CAR (ZIP)", type="zip")
        f_p = st.file_uploader("Upload do PRODES (ZIP)", type="zip")
        processar = st.button("🚀 Iniciar Processamento")

    if processar and f_c and f_p:
        # (Seu código de processamento aqui)
        st.success("Pronto para processar!")
