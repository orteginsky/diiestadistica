from ..gui.seleccion_archivos import seleccionar_carpeta
from ..informes.errores import informe_errores

ruta = seleccionar_carpeta()
informe_errores(ruta)