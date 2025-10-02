#from ..utils.archivo_utils import eliminar_xlsx_vacios
from diiestadistica.gui.seleccion_archivos import seleccionar_carpeta
from diiestadistica.procesamiento.procesar_subtotales import homologar_subtotales

ruta_catalogos = "/media/sf_Y_DRIVE/Homologacion/Catalogos Programas/"
ruta_unidades = f"{ruta_catalogos}/unidades_academicas.xlsx"

ruta_archivo = seleccionar_carpeta()
homologar_subtotales(ruta_archivo, ruta_unidades)