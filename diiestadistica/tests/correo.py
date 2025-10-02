from diiestadistica.conexion.email import enviar_correo
from diiestadistica.gui.seleccion_archivos import seleccionar_carpeta

ruta= seleccionar_carpeta()
print(ruta)
enviar_correo(ruta)