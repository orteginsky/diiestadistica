import pandas as pd

def dividir_subtotales(dataframe):
    """
    Divide un DataFrame en dos:
    - df_suma: Contiene filas donde alguna celda tiene las palabras clave ("total", "subt", "subtotal").
    - df_restante: Contiene las demás filas.
    
    Parámetros:
        df (pd.DataFrame): DataFrame de entrada.
    
    Retorna:
        tuple(pd.DataFrame, pd.DataFrame): (df_restante, df_suma)
    """
    palabras_clave = ["total", "subt", "subtotal"]
    
    # Convertir todas las celdas a string y verificar si contienen alguna palabra clave
    mascara_filas_a_mover = dataframe.apply(lambda fila: fila.astype(str).str.lower().str.contains('|'.join(palabras_clave)).any(), axis=1)
    
    # Dividir el DataFrame
    df_totales = dataframe[mascara_filas_a_mover]
    df = dataframe[~mascara_filas_a_mover]
    
    return df, df_totales


def eliminar_sin_afectar(df, columnas_excluir, columna_numerica='Datos'):
    """
    Agrupa un DataFrame por todas las columnas excepto las de 'columnas_excluir',
    y resume los valores de la 'columna_numerica' con una suma.

    Parámetros:
        df (pd.DataFrame): DataFrame de entrada.
        columna_numerica (str): Nombre de la columna numérica a sumar.
        columnas_excluir (list o tuple): Lista o tupla con nombres de columnas a excluir de la agrupación.

    Retorna:
        pd.DataFrame: DataFrame agrupado y resumido.
    """
    # Determinar las columnas a usar en la agrupación
    columnas_agrupacion = [col for col in df.columns if col not in columnas_excluir + [columna_numerica]]

    # Realizar la agrupación y sumar la columna numérica
    df_agrupado = df.groupby(columnas_agrupacion, as_index=False)[columna_numerica].sum()

    return df_agrupado
