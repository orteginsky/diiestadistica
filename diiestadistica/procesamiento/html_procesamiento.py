from ..utils.coincidencia import uno
from bs4 import BeautifulSoup

def limpiar_html(soup):
    # Paso 1: Eliminar las tablas anidadas en <tr> y mover su contenido
    for tr in soup.find_all('tr'):
        tables = tr.find_all('table', recursive=False)
        for table in tables:
            for sub_tr in table.find_all('tr', recursive=False):
                tr.insert_before(sub_tr)
            table.decompose()

    # Paso 2: Extraer contenido de tablas dentro de <td>
    for tr in soup.find_all('tr'):
        for td in tr.find_all(["td", "th"]):
            table = td.find('table', recursive=False)
            if table:
                #"""
                # Obtener el número de <tr> dentro de la tabla
                num_tr_inside = len(table.find_all('tr'))

                # Buscar el <td> anterior en la misma fila
                previous_td = td.find_previous_sibling('td')

                # Modificar el rowspan del <td> anterior
                if previous_td:
                    previous_td['rowspan'] = str(num_tr_inside)

                #"""
                # Obtener filas de la tabla
                filas = table.find_all('tr')

                # Verificar que haya al menos una fila antes de hacer pop
                if filas:
                    first_row = filas.pop(0)

                    # Fusionar con la fila actual
                    for td_content in reversed(first_row.find_all(["td", "th"])):
                        td.insert_after(td_content.extract())

                    # Agregar las demás filas después del <tr> actual
                    for row in reversed(filas):
                        tr.insert_after(row.extract())

                # Eliminar tabla original
                table.decompose()
                td.decompose()

    for tr in soup.find_all('tr'):
        if not tr.text.strip(): 
            tr.decompose()

    return soup


def procesar_tabla_html(soup):
    lista_matrices = []
    filas = soup.find_all("tr", recursive = False)
    for fila in filas:
        celdas = fila.find_all(["td", "th"])
        matriz_interada = []
        for celda in celdas:
            rowspan = int(celda.get("rowspan", 1))
            colspan = int(celda.get("colspan", 1))
            valor = celda.get_text().strip().replace("\n", "").replace("\t", "")
            matriz_interada.append([rowspan, colspan,valor])
            
        lista_matrices.append(matriz_interada)
    
    return lista_matrices




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
            for i in range(len(matriz[a])):
                if isinstance(matriz[a][i][0],int) and isinstance(matriz[a][i][1],int): 
                    sum2 += uno(matriz[a][i][0]+a-j)*matriz[a][i][1]
        suma = sum1 + sum2
        if suma!=vk:
            rectangulo = False
        j+=1
    return rectangulo