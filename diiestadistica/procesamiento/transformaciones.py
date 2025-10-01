#funciones externas
from diiestadistica.procesamiento.html_procesamiento import validar_rectangulo
from diiestadistica.procesamiento.limpieza import capitalizar
from diiestadistica.procesamiento.limpieza import limpiar_nombre_columna

#importar librerias
import pandas as pd
import numpy as np
import re

from diiestadistica.core.logging_config import setup_logger

logger = setup_logger(__name__)


def expandir_tabla(lista_matrices):
    """
    Toma la salida de procesar_tabla_html y devuelve un DataFrame sin encabezado,
    expandiendo celdas con rowspan y colspan.
    """
    
    filas = len(lista_matrices)
    columnas = max(sum(c[1] for c in fila) for fila in lista_matrices)
    tabla_expandida = np.full((filas, columnas), None, dtype=object)
        
    rectangulo = validar_rectangulo(lista_matrices)
    if rectangulo:
        for i, fila in enumerate(lista_matrices):
            col = 0 
            for rowspan, colspan, valor in fila:
                
                while tabla_expandida[i, col] is not None:
                    col += 1
                
                
                for r in range(rowspan):
                    for c in range(colspan):
                        tabla_expandida[i + r, col + c] = valor

        return pd.DataFrame(tabla_expandida)
    else: 
        return pd.DataFrame(tabla_expandida)



def definir_encabezados(dataframe):
    # Transponer el DataFrame
    datos_transpuesta = dataframe.T.copy()

    # Rellenar valores faltantes hacia adelante
    datos_transpuesta.ffill(inplace=True)

    # Aplicar la función capitalizar
    datos_transpuesta = datos_transpuesta.apply(capitalizar)

    # Verificar si todas las columnas de una fila son iguales a la primera columna
    iguales_a_primera_columna = datos_transpuesta.eq(datos_transpuesta.iloc[:, 0], axis=0).all(axis=1)

    # Generar nombres de columnas
    nombres_columnas = datos_transpuesta.apply(
        lambda row: row.iloc[0] if iguales_a_primera_columna[row.name] 
        else '_'.join(row.map(str).map(str.strip)), axis=1
    )

    # Limpiar los nombres de columnas
    nombres_columnas = nombres_columnas.apply(limpiar_nombre_columna)

    # **Eliminar secuencias de "__", "___", etc., dejando un solo "_"**
    nombres_columnas = nombres_columnas.apply(lambda x: re.sub(r'_{2,}', '', x))

    return nombres_columnas

def eliminar_columnas_subtotales(dataframe):
    # Lista de palabras clave a eliminar si están contenidas en el nombre de la columna
    palabras_clave = ["sub", "total", "subt"]
    
    # Filtrar las columnas:
    # - Se eliminan si contienen alguna palabra clave (excepto "no")
    # - Se eliminan si la columna es exactamente "No" (ignorando mayúsculas)
    columnas_filtradas = [
        col for col in dataframe.columns 
        if not any(palabra.lower() in col.lower() for palabra in palabras_clave) and col.lower() != "no"
    ]
    
    # Retornar el dataframe solo con las columnas permitidas
    return dataframe[columnas_filtradas]

def reorganizar_datos(dataframe):
    """
    Junta todas las columnas que contienen "_" en su nombre, las pivotea a lo largo,
    y separa la columna generada en múltiples columnas usando "_" como delimitador.

    Args:
        df (pd.DataFrame): DataFrame de entrada.

    Returns:
        pd.DataFrame: DataFrame transformado.
    """
    columnas_fijas = [col for col in dataframe.columns if "_" not in col]

    # Seleccionar las columnas que contienen "_" en su nombre
    columnas_pivote = [col for col in dataframe.columns if "_" in col]

    # Realizar la transformación a formato largo
    df_long = dataframe.melt(id_vars=columnas_fijas, value_vars=columnas_pivote, var_name="dividir", value_name="Datos")

    # Separar la columna "dividir" en varias columnas usando "_"
    columnas_creadas = df_long["dividir"].str.split("_", expand=True)

    # Generar nombres dinámicos para las nuevas columnas
    nombres_columnas_creadas = [f"col_{i+1}" for i in range(columnas_creadas.shape[1])]
    
    # Asignar las columnas separadas al DataFrame
    df_long[nombres_columnas_creadas] = columnas_creadas

    # Convertir la columna "Datos" a entero
    df_long["Datos"] = df_long["Datos"].astype(str).str.replace(r"[\s,\.]", "", regex=True).str.extract(r"(\d+)").astype(float).astype("Int64")

    # Retornar el DataFrame reorganizado
    return df_long.drop(columns=["dividir"])

def renombrar_columna(nombre_columna, dataframe, conjunto_valores):
    """
    Cambia el nombre de la primera columna cuyos valores únicos sean un subconjunto de un conjunto dado.

    :param nombre_columna: Nuevo nombre para la columna que cumpla la condición.
    :param dataframe: DataFrame de entrada.
    :param conjunto_valores: Conjunto de valores que debe contener la columna.
    :return: DataFrame con la columna renombrada (si aplica).
    """
    df = dataframe.copy()
    
    for columna in df.columns:
        if set(df[columna].dropna().unique()).issubset(conjunto_valores):
            df = df.rename(columns={columna: nombre_columna})
            break
    
    return df

def generar_columnas(descripcion, columnas, dataframe):
    """
    Genera nuevas columnas en un DataFrame a partir de una cadena de texto y una tupla de nombres de columna.

    :param descripcion: str - Cadena con el formato "palabra1_palabra2".
    :param columnas: tuple - Tupla con los nombres de las nuevas columnas (columna_1, columna_2).
    :param dataframe: pd.DataFrame - DataFrame al que se agregarán las nuevas columnas.
    :return: pd.DataFrame - DataFrame con las nuevas columnas agregadas.
    """
    if not isinstance(descripcion, str) or "_" not in descripcion:
        raise ValueError("La descripción debe ser un string en formato 'palabra1_palabra2'.")

    if not isinstance(columnas, tuple) or len(columnas) != 2:
        raise ValueError("Las columnas deben ser una tupla con exactamente dos elementos.")

    palabra1, palabra2 = descripcion.split("_", 1)

    # Agregar las nuevas columnas al DataFrame
    dataframe[columnas[0]] = palabra1
    dataframe[columnas[1]] = palabra2

    return dataframe



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

def eliminar_ceros(dataframe):
    if "Datos" in dataframe.columns:
        
        if "Sexo" in dataframe.columns:
            left_on = [col for col in dataframe.columns if col not in ['Sexo','Datos']]
            right_on = left_on
            ceros = eliminar_sin_afectar(dataframe, ["Sexo"], "Datos")
            ceros = ceros[ceros['Datos']==0]
            inner_join = pd.merge(dataframe, ceros, left_on=left_on, right_on=right_on, how='inner')
            sin_ceros = dataframe[~dataframe[left_on].isin(inner_join[left_on])]
            return sin_ceros
        elif "Concepto" in dataframe.columns:
            left_on = [col for col in dataframe.columns if col not in ['Concepto','Datos']]
            right_on = left_on
            ceros = eliminar_sin_afectar(dataframe, ["Concepto"], "Datos")
            ceros = ceros[ceros['Datos']==0]
            inner_join = pd.merge(dataframe, ceros, left_on=left_on, right_on=right_on, how='inner')
            sin_ceros = dataframe[~dataframe[left_on].isin(inner_join[left_on])]
            return sin_ceros
        else:
            return dataframe
    else:
        return dataframe
