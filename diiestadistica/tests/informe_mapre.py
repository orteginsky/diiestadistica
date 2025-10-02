from diiestadistica.gui.seleccion_archivos import seleccionar_carpeta
from diiestadistica.informes.mapre import mapre

ruta = seleccionar_carpeta()
mapre(ruta)