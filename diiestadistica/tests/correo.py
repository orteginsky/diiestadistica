from ..conexion.email import enviar_correo
from ..gui.seleccion_archivos import seleccionar_carpeta

ruta= seleccionar_carpeta()
print(ruta)
enviar_correo(ruta)