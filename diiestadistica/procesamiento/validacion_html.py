import os
from bs4 import BeautifulSoup
from .seleccionar_carpeta import seleccionar_carpeta
from .capitalizar import capitalizar
import pandas as pd
import numpy as np


def procesar_tabla_encabezados(soup):
    lista_matrices = []
    filas = soup.find_all("tr", recursive = False)
    for fila in filas:
        celdas = fila.find_all(["td", "th"], recursive = False)
        matriz_interada = []
        for celda in celdas:
            rowspan = int(celda.get("rowspan", 1))
            colspan = int(celda.get("colspan", 1))
            valor = celda.get_text().strip().replace("\n", "").replace("\t", "")
            matriz_interada.append([rowspan, colspan,valor])
            
        lista_matrices.append(matriz_interada)
    
    return lista_matrices


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


def uno(n):
    if isinstance(n,int) and n>0:
        return 1
    else:
        return 0

def validar_rectangulo(matriz):
    k = len(matriz)
    vk=0
    for sum in matriz[0]:
        vk+=sum[1]
    rectangulo = True
    j=1
    while(rectangulo and (j<k-1)):
        suma=0
        sum1=0
        sum2=0
        for i in range(len(matriz[j])):
            if isinstance(matriz[j][i][1], int):
                sum1 += matriz[j][i][1]
        for a in range(j):
            for i in range(len(matriz[j])):
                if isinstance(matriz[a][i][0],int) and isinstance(matriz[a][i][1],int): 
                    sum2 += uno(matriz[a][i][0]-j)*matriz[a][i][1]
        suma = sum1 + sum2
        if suma!=vk:
            rectangulo = False
        j+=1
    return rectangulo

def definir_encabezados(dataframe):
    # Transponer el dataframe
    datos_transpuesta = dataframe.T.copy()
    # Llenar valores faltantes hacia adelante
    datos_transpuesta.fillna(method='ffill', inplace=True)
    # Aplicar la función capitalizar a todas las columnas
    datos_transpuesta = datos_transpuesta.apply(capitalizar)
    return datos_transpuesta.astype(str).agg('_'.join, axis=1).iloc[3:]

if __name__ == "__main__":
    ruta_carpeta = seleccionar_carpeta()
    nombre_archivo = os.listdir(ruta_carpeta)[11]
    ruta_archivo = f"{ruta_carpeta}/{nombre_archivo}"
    print(ruta_archivo)

    with open(ruta_archivo, "r", encoding="latin-1") as archivo_html:
        soup = BeautifulSoup(archivo_html, "html.parser")

    encabezados = soup.find("thead")
    datos_html = soup.find_all("table")[1]
    
    tabla_matriz = procesar_tabla_encabezados(encabezados)
    tabla = expandir_tabla(tabla_matriz)
    ruta_guardar = f"{ruta_carpeta}/prueba.xlsx"
    tabla_encabezados = definir_encabezados(tabla)
    tabla_datos = expandir_tabla(procesar_tabla_encabezados(datos_html))
    print(tabla_encabezados)

#with open("C:/Users/HoneyAnimeOtaku/Desktop/archivo.txt","w", encoding="latin-1") as txt_guardar:
#    txt_guardar.write(encabezados.prettify())