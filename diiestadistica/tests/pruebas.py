from ..procesamiento.procesamiento_maestro import procesamiento_limpieza
from ..gui.seleccion_archivos import seleccionar_carpeta

ruta = seleccionar_carpeta()

procesamiento_limpieza(ruta)