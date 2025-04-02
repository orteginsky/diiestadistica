import pandas as pd
import unicodedata
import re

def capitalizar(columna):
    # Convertir todo a minúsculas y luego a formato de título (capitalizar)
    columna = columna.str.lower().str.title()

    # Lista de palabras a mantener en minúsculas
    palabras = [" En ", " De ", " La ", " El ", " Y ", " E ", 
                " Con ", " Por ", " Los ", " Para ", " Sus ", 
                " Del ", " Más ", " Mas "]
    
    # Reemplazar las palabras dentro de la cadena
    for palabra in palabras:
        columna = columna.str.replace(palabra, palabra.lower(), regex=True)

    # Reemplazar dobles espacios por un solo espacio
    columna = columna.str.replace("  ", " ", regex=True)

    return columna

def limpiar_nombre_columna(nombre):
    # Normalizar texto y eliminar diacríticos (acentos)
    nombre = ''.join(
        c if not unicodedata.combining(c) else '' 
        for c in unicodedata.normalize('NFKD', nombre)
    )
    
    # Reemplazar espacios por "."
    nombre = re.sub(r'\s+', '.', nombre)

    # Eliminar caracteres no permitidos en nombres de columnas
    nombre = re.sub(r'[^a-zA-Z0-9_.]', '', nombre)

    return nombre

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
        r"^Maestría en Ciencia y Tecnología de Vacunas y Bioterapéuticos$": "Maestría en Ciencias y Tecnología de Vacunas y Bioterapéuticos",
        r"  ": " "
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

    if "Concepto" in dataframe.columns:
        dataframe = dataframe[~dataframe["Turno"].str.contains("Subt", na=False)]
        dataframe["Turno"] = dataframe["Turno"].replace({
            "^V$": "Vespertino",
            "^M$": "Matutino",
            "^Ves$": "Vespertino",
            "^Mix$": "Mixto",
            "^Mat$": "Matutino"
        }, regex=True)
        dataframe["Concepto"] = dataframe["Concepto"].replace({
            "^Primer Ingreso$": "Nuevo Ingreso"
        }, regex=True)
        
    return dataframe
