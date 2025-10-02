from diiestadistica.procesamiento.procesar_subtotales import crear_subdirectorios
from diiestadistica.procesamiento.procesar_subtotales import sub_totales_unidad
from diiestadistica.procesamiento.procesar_subtotales import sub_totales_rama
from diiestadistica.procesamiento.procesar_subtotales import sub_totales_total
from diiestadistica.procesamiento.procesar_subtotales import procesar_subtotales
from diiestadistica.gui.seleccion_archivos import seleccionar_carpeta

ruta = seleccionar_carpeta()
#carpetas=["sub_totales_unidad","sub_totales_rama","totales"]
#crear_subdirectorios(ruta, carpetas)
procesar_subtotales(ruta)