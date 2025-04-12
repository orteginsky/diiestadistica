from ..conexion.email import enviar_correo
from ..gui.seleccion_archivos import seleccionar_archivo

ruta= seleccionar_archivo()
enviar_correo(ruta)