from ..utils.os_utils import comprimir_carpeta
from ..gui.seleccion_archivos import seleccionar_carpeta

ruta_archivo = seleccionar_carpeta()
comprimir_carpeta(ruta_archivo)