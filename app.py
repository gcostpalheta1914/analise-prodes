import os

def ler(f):
    with zipfile.ZipFile(f, 'r') as z:
        # Busca recursiva: encontra qualquer arquivo .shp, não importa a subpasta
        shp_files = [name for name in z.namelist() if name.endswith('.shp')]
        if not shp_files:
            raise FileNotFoundError("Nenhum arquivo .shp encontrado dentro deste ZIP.")
        
        # Pega o primeiro que encontrar
        shp_name = shp_files[0]
        
        # Lê usando a sintaxe de zip do geopandas
        return gpd.read_file(f"zip://{f.name}!{shp_name}", engine='pyogrio')
