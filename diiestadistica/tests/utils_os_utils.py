from diiestadistica.utils.os_utils import comprimir_carpeta
from diiestadistica.gui.seleccion_archivos import seleccionar_carpeta

ruta_archivo = seleccionar_carpeta()
comprimir_carpeta(ruta_archivo)