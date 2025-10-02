from diiestadistica.gui.seleccion_archivos import seleccionar_carpeta
from diiestadistica.informes.punoejecutadas import pu

ruta = seleccionar_carpeta()
pu(ruta)