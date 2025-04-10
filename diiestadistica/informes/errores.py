import pandas as pd
import os
import re

def anti_join(df1, df2, on):
    filas_repetidas = pd.merge(df1, df2[on], on=on, how='inner')
    condicion = ~df1.set_index(on).index.isin(filas_repetidas.set_index(on).index)
    return df1.loc[condicion].reset_index(drop=True)


def informe_errores(ruta_global,lista=['Datos']):
    ruta_subtotales = f"{ruta_global}/subtotales"
    ruta_errores = f"{ruta_global}/errores"
    lista_dataframes=[]
    nombre_hojas=[]
    archivos = [f for f in os.listdir(ruta_subtotales) if f.endswith('.xlsx') and os.path.isfile(os.path.join(ruta_subtotales, f))]
    carpetas = [d for d in os.listdir(ruta_subtotales) if os.path.isdir(os.path.join(ruta_subtotales, d))]
    for nombre_archivo in archivos:
        ruta_total = os.path.join(ruta_subtotales,nombre_archivo)
        try:
            dataframe_base = pd.read_excel(ruta_total)
            for carpeta in carpetas:
                ruta_carpeta = os.path.join(ruta_subtotales,carpeta)
                ruta_anti = os.path.join(ruta_carpeta, nombre_archivo)
                if os.path.exists(ruta_anti):
                    dataframe = pd.read_excel(ruta_anti)
                    dataframe_base = anti_join(dataframe_base, dataframe, lista)
            if dataframe_base.empty or dataframe_base.dropna(how='all').shape[0] == 0:
                print("subtotal bien")
            else:
                lista_dataframes.append(dataframe_base)
                nombre_hojas.append(re.sub('\\.xlsx','',nombre_archivo))

        except Exception as e:
            print(f"No se pudo abrir {nombre_archivo}: {e}")
            continue
    
    if lista_dataframes:
        ruta_archivo_errores = f"{ruta_errores}/informe.xlsx"
        with pd.ExcelWriter(ruta_archivo_errores, engine='openpyxl') as writer:
            for df, hoja in zip(lista_dataframes, nombre_hojas):
                df.to_excel(writer, sheet_name=hoja, index=False)
    else:
        print("✅ No se encontraron errores para reportar.")

