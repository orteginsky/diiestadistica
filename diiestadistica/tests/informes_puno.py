from ..gui.seleccion_archivos import seleccionar_carpeta
from ..informes.punoejecutadas import pu

ruta = seleccionar_carpeta()
pu(ruta)