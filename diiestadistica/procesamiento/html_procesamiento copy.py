# diiestadistica/scraping/html_utils.py

from typing import List, Any
from bs4 import BeautifulSoup, Tag
from diiestadistica.utils.coincidencia import uno
from diiestadistica.core.logging_config import setup_logger

logger = setup_logger(__name__)


def limpiar_html(tabla_html: Tag) -> Tag:
    """
    Limpia una tabla HTML (por ejemplo, un <tbody> o <table>),
    eliminando tablas anidadas y reorganizando su estructura.

    Args:
        tabla_html (Tag): Elemento BeautifulSoup (<table> o <tbody>) que contiene filas (<tr>).

    Returns:
        Tag: La misma tabla procesada, sin tablas anidadas y con estructura simplificada.
    """
    logger.info("Iniciando limpieza de tabla HTML anidada...")

    if not tabla_html or not isinstance(tabla_html, Tag):
        logger.warning("El argumento recibido no es un objeto Tag válido.")
        return tabla_html

    # Paso 1: Desanidar tablas dentro de <tr>
    for tr in tabla_html.find_all("tr", recursive=True):
        tablas_anidadas = tr.find_all("table", recursive=False)
        for tabla in tablas_anidadas:
            logger.debug(f"Encontrada tabla anidada dentro de <tr>: {tabla.name}")
            for sub_tr in tabla.find_all("tr", recursive=False):
                tr.insert_before(sub_tr)
            tabla.decompose()

    # Paso 2: Extraer contenido de tablas dentro de <td> o <th>
    for tr in tabla_html.find_all("tr", recursive=True):
        for celda in tr.find_all(["td", "th"]):
            tabla_interna = celda.find("table", recursive=False)
            if tabla_interna:
                filas_internas = tabla_interna.find_all("tr")
                logger.debug(f"Procesando tabla anidada en celda con {len(filas_internas)} filas")

                if filas_internas:
                    primera_fila = filas_internas.pop(0)

                    # Fusionar la primera fila dentro de la celda actual
                    for td_contenido in reversed(primera_fila.find_all(["td", "th"])):
                        celda.insert_after(td_contenido.extract())

                    # Insertar las filas restantes después del <tr> actual
                    for fila in reversed(filas_internas):
                        tr.insert_after(fila.extract())

                tabla_interna.decompose()
                celda.decompose()

    # Paso 3: Eliminar filas vacías
    filas_eliminadas = 0
    for tr in tabla_html.find_all("tr"):
        if not tr.get_text(strip=True):
            tr.decompose()
            filas_eliminadas += 1

    logger.info(f"Limpieza completada. Filas vacías eliminadas: {filas_eliminadas}")
    return tabla_html


def procesar_tabla_html(soup: Tag) -> List[List[List[Any]]]:
    """
    Convierte una tabla HTML en una matriz que conserva rowspan, colspan y texto.

    Args:
        soup (Tag): Elemento <table>, <thead>, o <tbody> con filas <tr>.

    Returns:
        list[list[list[Any]]]: Lista tridimensional con información de cada celda
                               en el formato [rowspan, colspan, valor].
    """
    logger.info("Procesando tabla HTML en estructura matricial...")

    lista_matrices: List[List[List[Any]]] = []
    filas = soup.find_all("tr", recursive=False)

    logger.debug(f"Número de filas detectadas: {len(filas)}")

    for idx, fila in enumerate(filas):
        celdas = fila.find_all(["td", "th"])
        matriz_fila: List[List[Any]] = []

        for celda in celdas:
            rowspan = int(celda.get("rowspan", 1))
            colspan = int(celda.get("colspan", 1))
            valor = celda.get_text().strip().replace("\n", "").replace("\t", "")
            matriz_fila.append([rowspan, colspan, valor])

        lista_matrices.append(matriz_fila)
        logger.debug(f"Fila {idx + 1} procesada con {len(celdas)} celdas.")

    logger.info(f"Procesamiento de tabla completado. Total de filas: {len(lista_matrices)}.")
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