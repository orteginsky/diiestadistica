from ..informes.arch_maestro import informes_mapre
from ..gui.seleccion_archivos import seleccionar_carpeta

ruta = seleccionar_carpeta()
informes_mapre(ruta)