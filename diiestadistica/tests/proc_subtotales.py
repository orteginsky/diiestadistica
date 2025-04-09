from ..procesamiento.procesar_subtotales import crear_subdirectorios
from ..procesamiento.procesar_subtotales import sub_totales_unidad
from ..procesamiento.procesar_subtotales import sub_totales_rama
from ..procesamiento.procesar_subtotales import sub_totales_total
from ..procesamiento.procesar_subtotales import procesar_subtotales
from ..gui.seleccion_archivos import seleccionar_carpeta

ruta = seleccionar_carpeta()
#carpetas=["sub_totales_unidad","sub_totales_rama","totales"]
#crear_subdirectorios(ruta, carpetas)
procesar_subtotales(ruta)