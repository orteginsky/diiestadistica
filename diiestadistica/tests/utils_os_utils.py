from ..utils.os_utils import comprimir_archivo
from ..gui.seleccion_archivos import seleccionar_archivo

ruta_archivo = seleccionar_archivo()
comprimir_archivo(ruta_archivo)