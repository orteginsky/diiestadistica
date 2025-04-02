import pandas as pd
import os

def informes_mapre(ruta_carpeta):
    ruta_homo = f"{ruta_carpeta}/archivos_homologados"
    ruta_informe = f"{ruta_carpeta}/reportes/archivo_maestro.xlsx"
    archivos_xlsx = [f for f in os.listdir(ruta_homo) if f.endswith(".xlsx")]
    
    if not archivos_xlsx:
        print("No se encontraron archivos .xlsx en la carpeta.")
        return None
    
    dataframes = [pd.read_excel(os.path.join(ruta_homo, archivo)) for archivo in archivos_xlsx]
    df_final = pd.concat(dataframes, ignore_index=True)
    df_final.to_excel(ruta_informe,index=False)



