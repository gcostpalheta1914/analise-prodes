import streamlit as st
import geopandas as gpd
import zipfile
import io
import os

st.set_page_config(page_title="Analisador Geo-Pro", layout="wide")

# --- Função de Busca Profunda (O "Furo" nas pastas) ---
def extrair_shp_profundo(zip_path):
    """
    Entra em zips aninhados até encontrar um .shp.
    """
    gdfs = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        for nome_arquivo in z.namelist():
            # Se encontrar um .zip dentro, entra nele recursivamente
            if nome_arquivo.endswith('.zip'):
                with z.open(nome_arquivo) as sub_zip:
                    sub_zip_data = io.BytesIO(sub_zip.read())
                    # Chama a função novamente para o nível interno
                    gdf = extrair_shp_profundo(sub_zip_data)
                    if gdf is not None:
                        gdfs.append(gdf)
            # Se encontrar o .shp diretamente, processa
            elif nome_arquivo.endswith('.shp'):
                with z.open(nome_arquivo) as f:
                    # Lê o shp e garante que o crs seja lido
                    gdf = gpd.read_file(io.BytesIO(f.read()))
                    gdfs.append(gdf)
                    
    if gdfs:
        return gpd.pd.concat(gdfs, ignore_index=True)
    return None

# --- Interface Principal ---
if "auth" not in st.session_state: st.session_state["auth"] = False

# [Manter sua lógica de check_password aqui...]

if st.button("🚀 Processar Análise Exata"):
    if f_c and f_p:
        with st.spinner("Navegando nas pastas e processando..."):
            try:
                # 1. Carrega todos os CARs encontrados na estrutura aninhada
                g_c = extrair_shp_profundo(f_c)
                # 2. Carrega o PRODES (que está em uma camada só)
                g_p = extrair_shp_profundo(f_p)
                
                # 3. Cruzamento Geométrico Exato
                if g_c is not None and g_p is not None:
                    if g_c.crs != g_p.crs: g_c = g_c.to_crs(g_p.crs)
                    
                    resultado = gpd.overlay(g_c, g_p, how='intersection')
                    st.success("Análise concluída com precisão!")
                    st.dataframe(resultado)
                else:
                    st.error("Não foi possível encontrar arquivos .shp dentro dos zips fornecidos.")
            except Exception as e:
                st.error(f"Erro técnico: {e}")
