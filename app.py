import streamlit as st
import geopandas as gpd
import zipfile
import io

st.set_page_config(page_title="Analisador Geo-Pro", layout="wide")

# (Mantenha aqui sua lógica de login)

def processar_arquivos(f_c, f_p):
    gdfs = []
    # Abre o ZIP principal (o que contém os zips dos imóveis)
    with zipfile.ZipFile(f_c, 'r') as z:
        for item in z.namelist():
            if item.endswith('.zip'):
                # Abre cada sub-zip individualmente
                with z.open(item) as sub_zip:
                    # Lê o sub-zip na memória
                    sub_zip_data = io.BytesIO(sub_zip.read())
                    with zipfile.ZipFile(sub_zip_data) as sub_z:
                        # Busca o .shp lá dentro
                        shp_name = next((f for f in sub_z.namelist() if f.endswith('.shp')), None)
                        if shp_name:
                            # Lê o imóvel individualmente
                            gdf = gpd.read_file(sub_z.open(shp_name))
                            gdfs.append(gdf)
    
    # Junta todos os imóveis em um só arquivo grande
    if gdfs:
        return gpd.pd.concat(gdfs)
    return None

if st.button("🚀 Processar"):
    try:
        with st.spinner("Lendo imóveis..."):
            g_c = processar_arquivos(f_c, None) # Adapte aqui para ler o PRODES também
            st.success("Arquivos lidos!")
            st.dataframe(g_c.head())
    except Exception as e:
        st.error(f"Erro: {e}")
