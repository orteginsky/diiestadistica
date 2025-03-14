import os
from bs4 import BeautifulSoup
from .seleccionar_carpeta import seleccionar_carpeta

def procesar_tabla_html(soup):
    lista_matrices = []
    filas = soup.find_all("tr")
    for fila in filas:
        celdas = fila.find_all(["td", "th"])
        matriz_interada = []
        for celda in celdas:
            rowspan = int(celda.get("rowspan", 1))
            colspan = int(celda.get("colspan", 1))
            matriz_interada.append([rowspan, colspan])
            
        lista_matrices.append(matriz_interada)
    
    return lista_matrices

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


if __name__ == "__main__":
    ruta_carpeta = seleccionar_carpeta()
    nombre_archivo = os.listdir(ruta_carpeta)[11]
    ruta_archivo = f"{ruta_carpeta}/{nombre_archivo}"
    print(ruta_archivo)

    with open(ruta_archivo, "r", encoding="latin-1") as archivo_html:
        soup = BeautifulSoup(archivo_html, "html.parser")

    encabezados = soup.find("thead")
    print(validar_rectangulo(procesar_tabla_html(encabezados)))
    
#with open("C:/Users/HoneyAnimeOtaku/Desktop/archivo.txt","w", encoding="latin-1") as txt_guardar:
#    txt_guardar.write(encabezados.prettify())


