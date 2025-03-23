from .validacion_html import validar_rectangulo, uno
from .capitalizar import capitalizar
from .seleccionar_carpeta import seleccionar_carpeta
from .creacion_tabla import expandir_tabla, definir_encabezados

from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import os
import re
import unicodedata

import pandas as pd

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


def limpiar_nombres_programas(dataframe, columna):
    """
    Limpia y estandariza los nombres de los programas académicos en una columna específica de un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        columna (str): Nombre de la columna a limpiar.

    Returns:
        pd.DataFrame: DataFrame con la columna de programas académicos limpia.
    """

    # Diccionario con las reglas de reemplazo
    reemplazos = {
        r"^Ing\. ": "Ingeniería ",
        r"^Lic\. ": "Licenciatura ",
        r"^Maestria": "Maestría",
        r"^M en C en Ing ": "Maestría en Ciencias en Ingeniería ",
        r"^Dr en C en Ing ": "Doctorado en Ciencias en Ingeniería ",
        r" Mec$": " Mecánica",
        r"^M en C y Tec de Vac y Bio$": "Maestría en Ciencias y Tecnología de Vacunas y Bioterapéuticos",
        r"^Dr en C y Tec de Vacunas y Bioterapéuticos$": "Doctorado en Ciencias y Tecnología de Vacunas y Bioterapéuticos",
        r"^Ingeniería en Mecatrónica$": "Ingeniería Mecatrónica",
        r"^Maestría en Ciencia y Tecnología de Vacunas y Bioterapéuticos$": "Maestría en Ciencias y Tecnología de Vacunas y Bioterapéuticos"
    }

    # Aplicar los reemplazos con expresiones regulares
    dataframe[columna] = dataframe[columna].astype(str).str.strip()

    for patron, reemplazo in reemplazos.items():
        dataframe[columna] = dataframe[columna].str.replace(patron, reemplazo, regex=True)

    return dataframe

def correccion_conceptos(dataframe):
    if "Sexo" in dataframe.columns:
        dataframe = dataframe[~dataframe["Sexo"].str.contains("Subt", na=False)]
        dataframe["Sexo"] = dataframe["Sexo"].replace({
            "^H$": "Hombres",
            "^M$": "Mujeres",
            "^Hom$": "Hombres",
            "^Muj$": "Mujeres"
        }, regex=True)

    if "Turno" in dataframe.columns:
        dataframe = dataframe[~dataframe["Turno"].str.contains("Subt", na=False)]
        dataframe["Turno"] = dataframe["Turno"].replace({
            "^V$": "Vespertino",
            "^M$": "Matutino",
            "^Ves$": "Vespertino",
            "^Mix$": "Mixto",
            "^Mat$": "Matutino"
        }, regex=True)

    if "Concepto" in dataframe.columns:
        dataframe["Concepto"] = dataframe["Concepto"].replace({
            "^Primer Ingreso$": "Nuevo Ingreso"
        }, regex=True)
    
    return dataframe


def anti_join(df1, df2, left_on, right_on):
    inner_join = pd.merge(df1, df2, left_on=left_on, right_on=right_on, how='inner')
    return df1[~df1[left_on].isin(inner_join[left_on])]


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


def renombrar_columnas(dataframe):
    df = dataframe.copy()
    sexo = {"H","M"}
    print("ok")

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


def coincidencia(patron, valor):
    if re.search(patron, valor):
        return True
    else:
        return False