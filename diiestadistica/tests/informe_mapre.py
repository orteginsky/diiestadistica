from ..gui.seleccion_archivos import seleccionar_carpeta
from ..informes.mapre import mapre

ruta = seleccionar_carpeta()
mapre(ruta)