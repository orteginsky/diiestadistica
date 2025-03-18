from .validacion_html import validar_rectangulo
from .capitalizar import capitalizar
from .seleccionar_carpeta import seleccionar_carpeta
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import os
import re
import unicodedata

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

    # Generar nombres de columnas: si todas las celdas de una fila son iguales, tomar solo la primera, sino concatenar
    nombres_columnas = datos_transpuesta.apply(lambda row: row.iloc[0] if iguales_a_primera_columna[row.name] 
                                               else '_'.join(row), axis=1)
    
    # Limpiar los nombres de columnas
    nombres_columnas = nombres_columnas.apply(limpiar_nombre_columna)

    return nombres_columnas

