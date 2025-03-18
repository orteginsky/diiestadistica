from .validacion_html import validar_rectangulo
from .capitalizar import capitalizar
from .seleccionar_carpeta import seleccionar_carpeta
from .creacion_tabla import expandir_tabla, definir_encabezados

from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import os
import re
import unicodedata

def eliminar_columnas_subtotales(dataframe):
    # Lista de palabras clave a eliminar (sin importar mayúsculas o minúsculas)
    palabras_clave = ["sub", "total", "subt"]
    
    # Filtrar las columnas que NO contienen las palabras clave
    columnas_filtradas = [col for col in dataframe.columns if not any(palabra.lower() in col.lower() for palabra in palabras_clave)]
    
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
    df_long = dataframe.melt(id_vars=columnas_fijas, value_vars=columnas_pivote, 
                      var_name="dividir", value_name="Datos")

    # Separar la columna "dividir" en varias columnas usando "_"
    columnas_creadas = df_long["dividir"].str.split("_", expand=True)

    # Generar nombres dinámicos para las nuevas columnas
    nombres_columnas_creadas = [f"col_{i+1}" for i in range(columnas_creadas.shape[1])]
    
    # Asignar las columnas separadas al DataFrame
    df_long[nombres_columnas_creadas] = columnas_creadas

    # Convertir la columna "Datos" a entero
    df_long["Datos"] = pd.to_numeric(df_long["Datos"], errors="coerce")

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


if __name__ == "__main__":
    # Seleccionar un archivo y abrirlo para procesarlo
    from .validacion_html import procesar_tabla_html
    ruta_carpeta = seleccionar_carpeta()
    nombre_archivo = os.listdir(ruta_carpeta)[11]
    ruta_archivo = f"{ruta_carpeta}/{nombre_archivo}"
    print(ruta_archivo)
    with open(ruta_archivo, "r", encoding="latin-1") as archivo_html:
        soup = BeautifulSoup(archivo_html, "html.parser")

    # Extraer los encabezados
    soup_encabezados = soup.find("thead")
    # Extraer matriz de matrices
    encabezados_matriz = procesar_tabla_html(soup_encabezados)
    # Expandir tabla de encabezados
    encabezados_df = expandir_tabla(encabezados_matriz)

    # Extraer los datos
    datos_html = soup.find("tbody", {"border": "1"})
    # Extraer matriz de matrices de datos
    datos_matriz = procesar_tabla_html(soup=datos_html)
    # Expandir datos
    datos_exp = expandir_tabla(datos_matriz)
    # Cambiar los colnames
    datos_exp.columns = definir_encabezados(encabezados_df)
    # Eliminar subtotales
    datos_exp = eliminar_columnas_subtotales(datos_exp)
    # pivotear datos
    datos_exp = reorganizar_datos(datos_exp)
    # Depurar programas
    datos_exp = limpiar_nombres_programas(datos_exp, "Programas.Academicos")
    # depurar conceptos
    datos_exp = correccion_conceptos(datos_exp)
    print(datos_exp)
    #ruta_guardar = f"{ruta_carpeta}/prueba.xlsx"