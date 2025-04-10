import pandas as pd

def mapre(ruta_global, columna_agrupacion='Indice'):
    """
    Genera un libro de Excel con una hoja por cada valor único en la columna_agrupacion.
    En cada hoja realiza las operaciones de agrupación, pivotado y creación de columnas adicionales.

    :param ruta_global: Ruta del directorio principal donde están los archivos.
    :param columna_agrupacion: Columna por la que se desea agrupar las hojas en el Excel.
    """
    ruta_reportes = f"{ruta_global}/reportes"
    ruta_archivo_maestro = f"{ruta_reportes}/archivo_maestro.xlsx"
    ruta_salida = f"{ruta_reportes}/mapre.xlsx"
    
    try:
        dataframe = pd.read_excel(ruta_archivo_maestro)
        
        # Verifica si el DataFrame está vacío
        if dataframe.empty:
            # Crea un archivo con una hoja de mensaje
            with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
                pd.DataFrame({'Mensaje': ['El archivo maestro está vacío']}).to_excel(writer, sheet_name='Mensaje', index=False)
            print(f"Archivo creado con mensaje de advertencia en {ruta_salida}")
            return
        
        # Verifica si las columnas 'Sexo', 'Nivel' y 'Concepto' existen en el dataframe
        if ("Sexo" in dataframe.columns) and ("Nivel" in dataframe.columns) and ("Concepto" in dataframe.columns):
            # Crea un objeto ExcelWriter para guardar las hojas en un archivo de Excel
            with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
                # Variable para verificar si al menos una hoja tiene datos
                al_menos_una_hoja = False
                
                # Itera sobre cada grupo único de la columna de agrupación
                for valor in dataframe[columna_agrupacion].unique():
                    # Filtra el dataframe por cada grupo
                    df_agrupado = dataframe[dataframe[columna_agrupacion] == valor]
                    
                    df_agrupado = (
                        df_agrupado.groupby(['Nivel', 'Concepto', 'Sexo'], as_index=False)
                        .agg({'Datos': 'sum'})
                        .pivot_table(index=['Nivel', 'Concepto'], columns='Sexo', values='Datos', aggfunc='sum')
                        .reset_index()
                    )

                    # Asegura que las columnas 'Hombres' y 'Mujeres' existan, si no las crea
                    df_agrupado['Hombres'] = df_agrupado.get('Hombres', 0).astype(int)
                    df_agrupado['Mujeres'] = df_agrupado.get('Mujeres', 0).astype(int)

                    # Crea la columna 'Total' y 'Nivel'
                    df_agrupado['Total'] = df_agrupado['Hombres'] + df_agrupado['Mujeres']
                    df_agrupado['Nivel'] = df_agrupado['Nivel'].apply(
                        lambda x: 'Medio Superior' if x == 1 else ('Superior' if x == 2 else 'Posgrado')
                    )

                    # Selecciona las columnas que deseas para la hoja final
                    df_agrupado = df_agrupado[['Nivel', 'Concepto', 'Hombres', 'Mujeres', 'Total']]

                    # Si la hoja tiene datos, la escribe
                    if not df_agrupado.empty:
                        al_menos_una_hoja = True
                        df_agrupado.to_excel(writer, sheet_name=str(valor), index=False)
                    else:
                        # Si la hoja está vacía, escribe una hoja con un mensaje
                        df_vacia = pd.DataFrame({'Mensaje': ['No hay datos para este grupo']})
                        df_vacia.to_excel(writer, sheet_name=str(valor), index=False)
                
                # Si ninguna hoja tenía datos, asegúrate de tener al menos una visible
                if not al_menos_una_hoja:
                    pd.DataFrame({'Mensaje': ['No se encontraron datos válidos en ninguna agrupación']}).to_excel(
                        writer, sheet_name='Datos', index=False)
                
            print(f"Informe generado correctamente en {ruta_salida}")
        else:
            # Si faltan columnas, crea un archivo con mensaje de error
            with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
                pd.DataFrame({'Error': ['Faltan columnas requeridas (Sexo, Nivel, Concepto)']}).to_excel(
                    writer, sheet_name='Error', index=False)
            print(f"Archivo creado con mensaje de error en {ruta_salida}")
    
    except Exception as e:
        print(f"Se produjo un error: {e}")