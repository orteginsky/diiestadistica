from diiestadistica.utils.coincidencia import uno
from bs4 import BeautifulSoup, Tag

from diiestadistica.core.logging_config import setup_logger
from typing import List, Any

logger = setup_logger(__name__)


def limpiar_html(soup):
    """
    Limpia una tabla HTML (por ejemplo, un <tbody> o <table>),
    eliminando tablas anidadas y reorganizando su estructura.

    Args:
        tabla_html (Tag): Elemento BeautifulSoup (<table> o <tbody>) que contiene filas (<tr>).

    Returns:
        Tag: La misma tabla procesada, sin tablas anidadas y con estructura simplificada.
    """
    logger.info("Iniciando limpieza de tabla HTML anidada...")

    # Paso 1: Eliminar las tablas anidadas en <tr> y mover su contenido
    for tr in soup.find_all('tr'):
        tables = tr.find_all('table', recursive=False)
        for table in tables:
            logger.debug(f"Encontrada tabla anidada dentro de <tr>: {table.name}")
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

    # Paso 2: Extraer contenido de tablas dentro de <td> o <th>
    for tr in soup.find_all("tr"):
        for td in tr.find_all(["td", "th"]):
            table = td.find("table", recursive=False)
            if table:
                filas = table.find_all('tr')
                # Obtener el número de <tr> dentro de la tabla
                num_tr_inside = len(filas)
                logger.debug(f"Procesando tabla anidada en celda con {num_tr_inside} filas")
                # Buscar el <td> anterior en la misma fila
                previous_td = td.find_previous_sibling('td')
                # Modificar el rowspan del <td> anterior
                if previous_td:
                    previous_td['rowspan'] = str(num_tr_inside)
                if filas:
                    first_row = filas.pop(0)
                    # Fusionar la primera fila dentro de la celda actual
                    for td_content in reversed(first_row.find_all(["td", "th"])):
                        td.insert_after(td_content.extract())

                    # Insertar las filas restantes después del <tr> actual
                    for row in reversed(filas):
                        tr.insert_after(row.extract())
                # Eliminar tabla original
                table.decompose()
                td.decompose()
    
    # Paso 3: Eliminar filas vacías
    filas_eliminadas = 0
    for tr in soup.find_all("tr"):
        if not tr.text.strip():
            tr.decompose()
            filas_eliminadas += 1

    logger.info(f"Limpieza completada. Filas vacías eliminadas: {filas_eliminadas}")
    return soup



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

def validar_rectangulo(matriz: List[List[List[Any]]]) -> bool:
    """
    Valida si la matriz derivada de una tabla HTML forma un rectángulo válido,
    considerando rowspan y colspan.

    Args:
        matriz (list[list[list[Any]]]): Matriz tridimensional con [rowspan, colspan, valor].

    Returns:
        bool: True si la tabla representa un rectángulo válido, False en caso contrario.
    """
    logger.info("Validando estructura rectangular de la tabla...")

    try:
        if not matriz:
            logger.warning("Matriz vacía, no se puede validar.")
            return False

        ancho_referencia = sum(celda[1] for celda in matriz[0])
        logger.debug(f"Ancho base de la primera fila: {ancho_referencia}")

        for j in range(1, len(matriz)):
            ancho_fila = sum(celda[1] for celda in matriz[j] if isinstance(celda[1], int))
            ancho_extra = sum(
                uno(celda[0] + a - j) * celda[1]
                for a in range(j)
                for celda in matriz[a]
                if isinstance(celda[0], int) and isinstance(celda[1], int)
            )
            ancho_total = ancho_fila + ancho_extra

            if ancho_total != ancho_referencia:
                logger.warning(f"Diferencia detectada en fila {j + 1}: esperado={ancho_referencia}, obtenido={ancho_total}")
                return False

        logger.info("La matriz tiene una estructura rectangular válida.")
        return True

    except Exception as e:
        logger.exception(f"Error durante la validación de rectángulo: {e}")
        return False