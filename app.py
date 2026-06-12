import streamlit as st
import geopandas as gpd
import zipfile
import io
import pyogrio

# Função que "fura" múltiplos níveis de ZIP
def abrir_zip_recursivo(uploaded_file):
    def buscar_shp_no_zip(z):
        for nome in z.namelist():
            # Se for um arquivo .shp, achamos!
            if nome.endswith('.shp'):
                # Retorna os bytes do .shp e os nomes necessários (dbf, shx, etc)
                return z.read(nome), nome
            # Se for outro ZIP dentro, abre ele também
            elif nome.endswith('.zip'):
                with z.open(nome) as sub_zip_file:
                    sub_zip_data = io.BytesIO(sub_zip_file.read())
                    with zipfile.ZipFile(sub_zip_data) as sub_z:
                        return buscar_shp_no_zip(sub_z)
        return None, None

    with zipfile.ZipFile(uploaded_file, 'r') as z:
        shp_bytes, shp_name = buscar_shp_no_zip(z)
        
        if not shp_bytes:
            raise Exception("Não encontrei .shp mesmo vasculhando as pastas.")
            
        # Carrega os bytes do shp no geopandas
        return gpd.read_file(io.BytesIO(shp_bytes), engine='pyogrio')
