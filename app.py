import streamlit as st
import geopandas as gpd
import io
import zipfile

# --- CONFIGURAÇÃO DE LOGIN ---
def check_password():
    """Retorna True se o usuário digitou a senha correta."""
    def password_entered():
        if st.session_state["user"] == "gabriel.palheta" and st.session_state["pass"] == "Gab1914":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Usuário", key="user")
        st.text_input("Senha", type="password", key="pass", on_change=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Usuário", key="user")
        st.text_input("Senha", type="password", key="pass", on_change=password_entered)
        st.error("Usuário ou senha incorretos")
        return False
    else:
        return True

st.set_page_config(page_title="Analisador PRODES", layout="wide")

# --- EXECUÇÃO DO APP ---
if check_password():
    st.title("🗺️ Analisador de Passivos: CAR vs PRODES")
    
    def ler_shp_do_zip(uploaded_file):
        with zipfile.ZipFile(uploaded_file, 'r') as z:
            shp_file = [f for f in z.namelist() if f.endswith('.shp')][0]
            with z.open(shp_file) as f:
                return gpd.read_file(f, engine='pyogrio')

    col1, col2 = st.columns(2)
    with col1: f_c = st.file_uploader("Suba o arquivo dos CARs (ZIP)", type="zip")
    with col2: f_p = st.file_uploader("Suba o arquivo do PRODES (ZIP)", type="zip")

    if st.button("🚀 Processar Cruzamento"):
        if f_c and f_p:
            try:
                with st.spinner("Processando..."):
                    g_c = ler_shp_do_zip(f_c)
                    g_p = ler_shp_do_zip(f_p)
                    if g_c.crs != g_p.crs: g_c = g_c.to_crs(g_p.crs)
                    inter = gpd.overlay(g_c, g_p, how='intersection')
                    st.success("Cruzamento concluído!")
                    st.dataframe(inter)
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.warning("Suba os dois arquivos.")
