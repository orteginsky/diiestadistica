from ..procesamiento.procesamiento_maestro import procesamiento_aplanamiento
from ..gui.seleccion_archivos import seleccionar_carpeta

ruta = seleccionar_carpeta()

procesamiento_aplanamiento(ruta)