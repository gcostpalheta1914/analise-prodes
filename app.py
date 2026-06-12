import streamlit as st
import geopandas as gpd
import pyogrio
import zipfile

def ler_prodes_otimizado(uploaded_file, car_bounds):
    """
    Lê o arquivo PRODES apenas dentro dos limites do seu CAR (Bounding Box).
    Isso reduz a carga na RAM drasticamente e acelera o processamento.
    """
    with zipfile.ZipFile(uploaded_file, 'r') as z:
        # Encontra o arquivo .shp automaticamente
        shp_name = [f for f in z.namelist() if f.endswith('.shp')][0]
        
        # Lê apenas o que intercepta o Bounding Box do CAR
        # engine='pyogrio' garante a velocidade máxima (leitura via C++)
        gdf = gpd.read_file(
            f"zip://{uploaded_file.name}!{shp_name}", 
            engine='pyogrio',
            bbox=car_bounds 
        )
        return gdf

# Na lógica do seu botão processar:
if processar and f_c and f_p:
    with st.spinner("Processando com alta precisão..."):
        # 1. Lê o CAR primeiro (que é pequeno)
        g_c = gpd.read_file(f_c, engine='pyogrio')
        
        # 2. Pega a caixa delimitadora do CAR para usar como filtro
        bounds = g_c.total_bounds
        
        # 3. Lê o PRODES filtrando pelo limite do CAR
        g_p = ler_prodes_otimizado(f_p, bounds)
        
        # 4. Garante que os sistemas de referência (CRS) sejam iguais
        if g_c.crs != g_p.crs:
            g_c = g_c.to_crs(g_p.crs)
            
        # 5. Cruzamento preciso (Intersection)
        resultado = gpd.overlay(g_c, g_p, how='intersection')
