from ..procesamiento.procesar_subtotales import crear_subdirectorios
from ..procesamiento.procesar_subtotales import sub_totales_unidad
from ..gui.seleccion_archivos import seleccionar_carpeta

ruta = seleccionar_carpeta()
#carpetas=["sub_totales_unidad","sub_totales_rama","totales"]
#crear_subdirectorios(ruta, carpetas)
sub_totales_unidad(ruta)