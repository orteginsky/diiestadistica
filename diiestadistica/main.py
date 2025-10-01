from diiestadistica.utils.archivo_utils import renombrar_archivos
from diiestadistica.utils.os_utils import limpiar_descargas
from diiestadistica.utils.os_utils import crear_directorio
from diiestadistica.utils.os_utils import comprimir_carpeta
from diiestadistica.procesamiento.procesamiento_maestro import procesamiento_aplanamiento
from diiestadistica.procesamiento.procesamiento_maestro import procesamiento_limpieza
from diiestadistica.procesamiento.procesar_subtotales import procesar_subtotales
from diiestadistica.informes.arch_maestro import informes_mapre
from diiestadistica.informes.errores import informe_errores
from diiestadistica.informes.mapre import mapre
from diiestadistica.conexion.email import enviar_correo

from diiestadistica.gui.ventana_base import ventana_base
from diiestadistica.gui.ventana_base import agregar_boton
from diiestadistica.gui.ventana_base import agregar_periodo_box
from diiestadistica.gui.ventana_base import agregar_ciclo_box
from diiestadistica.gui.ventana_base import estilizar_pestañas
from diiestadistica.gui.ventana_base import activar_descarga_intranet
from diiestadistica.gui.ventana_base import seleccionar_carpeta
from diiestadistica.gui.ventana_base import agregar_textbox
from diiestadistica.gui.ventana_base import boton_carpeta
from diiestadistica.core.settings import settings

import tkinter as tk
from tkinter import ttk
import os

from diiestadistica.core.logging_config import setup_logger

logger = setup_logger(__name__)

def quitar():
    logger.info("quitar en ejecucion")
    notebook.destroy()
    root.destroy()
def ir_a_pestaña_n(n):
    logger.info(f"navegando a la pestaña {n}")
    notebook.select(notebook.tabs()[n])
def iniciar():
    logger.info("se ha iniciado")
    ir_a_pestaña_n(1)
def limpiar():
    logger.info("se ha limpiado")
    ir_a_pestaña_n(2)
    limpiar_descargas()

def generar_ruta(seleccion_textbox, ciclos, periodos):
    carpeta = seleccion_textbox.get()
    ciclo = ciclos.get()
    periodo = periodos.get()
    ruta_base = os.path.normpath(os.path.join(carpeta, f"periodo_{ciclo}_{periodo}"))
    logger.info(f"se ha generado la siguiente ruta:{ruta_base}")
    return ruta_base

def descargar(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    logger.info(f"se ha generado la siguiente ruta:{ruta_base}")
    crear_directorio(ruta_base)
    ir_a_pestaña_n(2)
    ciclo = ciclos.get()
    periodo = periodos.get() 
    logger.info(f"ciclo selecionado:{ciclo} y perido selecionado:{periodo}")
    logger.info(f"se descargara en base al siguiente {ruta_base}")
    download_path = os.path.normpath(os.path.join(ruta_base, "archivos_originales"))
    logger.info(download_path)
    activar_descarga_intranet(ciclo, periodo, download_path)

def zip_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    ruta_informes = os.path.normpath(os.path.join(ruta_base, "reportes"))
    comprimir_carpeta(ruta_informes)

def enviar_correo_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    ruta_zip = os.path.normpath(os.path.join(ruta_base, "reportes"))
    logger.info(ruta_zip)
    lista_correos = settings.emails_destinatarios
    logger.info(f"se enviara a los siguientes correos:{lista_correos}")
    for correo in lista_correos:
        enviar_correo(ruta_zip, correo)

def depurar(ruta_base, bolean = False):
    if bolean:
        logger.info(f"se depuro en{ruta_base}")
    else:
        logger.info("se depuro")

def renombrar_archivos_gui(seleccion_textbox, ciclos, periodos, boolean= True):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    renombrar_archivos(ruta_base, boolean)

    
def depurar_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    procesamiento_aplanamiento(ruta_base)

def homologar_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    procesamiento_limpieza(ruta_base)

def procesar_subtotales_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    procesar_subtotales(ruta_base)

def archivo_maestro_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    informes_mapre(ruta_base)

def errores_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    informe_errores(ruta_base)

def mapre_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    mapre(ruta_base)

def ejecutar_funciones(frame, labels, funciones, idx=0):
    """
    Ejecuta funciones en orden con sus respectivos parámetros, esperando que cada una termine antes de continuar con la siguiente.

    :param frame: ttk.Frame donde están los labels.
    :param labels: Lista de labels donde se mostrarán los resultados (✅ o ❌).
    :param funciones: Lista de tuplas (función, argumentos).
    :param idx: Índice de la función actual (para llamadas recursivas).
    """
    if idx >= len(funciones):
        return
    func, args = funciones[idx]
    try:
        func(*args)
        labels[idx].config(text="✅", fg="green")
    except Exception as e:
        labels[idx].config(text="❌", fg="red")
        logger.info(f"Error en la función {idx + 1}: {e}")

    # Llamar a la siguiente función después de terminar
    frame.after(100, lambda: ejecutar_funciones(frame, labels, funciones, idx + 1))

root = tk.Tk()
root = ventana_base(root,"I N I C I O")

# Crear el estilo
style = ttk.Style()
style.configure(
    "TNotebook.Tab",
    width=35,
    background="#F1F1F1",
    foreground="#333333",
    padding=[10, 20],
    font=("Arial", 16)
)

# Color cuando está seleccionada
style.map("TNotebook.Tab",
          background=[("selected", "#F1F1F1")],
          foreground=[("selected", "#5A1236")])

notebook = ttk.Notebook(root, style="TNotebook")
notebook.pack(expand=True, fill="both")

# Pestaña Selección de carpeta pestaña(0)
frame_seleccion = ttk.Frame(notebook)
label_inicio = tk.Label(frame_seleccion,
                        text="Bienvenido a la aplicación\n\nAquí puedes realizar el proceso de estadística básica.\n\nSelecciona la carpeta donde guardaras la información",
                        font=("Arial", 14))
label_inicio.pack(pady=20)
seleccion_textbox = agregar_textbox(frame_seleccion)
seleccion_seleccion = boton_carpeta(frame_seleccion)
seleccion_seleccion.config(command=lambda: seleccionar_carpeta(seleccion_textbox))
seleccion_aceptar = agregar_boton(frame_seleccion,"Aceptar")
seleccion_aceptar.config(command=lambda: ir_a_pestaña_n(1))
notebook.add(frame_seleccion, text="Selección de carpeta")

# Pestaña Ingreso de Datos pestaña(1)
frame_datos = ttk.Frame(notebook)
ciclos = agregar_ciclo_box(frame_datos)
periodos = agregar_periodo_box(frame_datos)
datos_regresar = agregar_boton(frame_datos,"Regresar")
datos_regresar.config(command=lambda: ir_a_pestaña_n(0))
datos_Confirmar = agregar_boton(frame_datos,"Confirmar Selección")
datos_Confirmar.config(command=lambda: descargar(seleccion_textbox, ciclos, periodos))
notebook.add(frame_datos, text="Selección del Periodo")

# Pestaña Procesamiento de datos pestaña (2)
frame_procesamiento = ttk.Frame(notebook)
frame_procesamiento.grid()

crudo_regresar = tk.Button(
    frame_procesamiento,
    text="Regresar",
    font=("Arial", 12),
    bg="#FFFFFF",
    fg="#5A1236")
crudo_regresar.grid(row=0, column=1)
crudo_Generar = tk.Button(
    frame_procesamiento,
    text="Procesar",
    font=("Arial", 12),
    bg="#FFFFFF",
    fg="#5A1236")
crudo_Generar.grid(row=0, column=2)

labels_definidos = [
    tk.Label(
        frame_procesamiento,
        text="Generando Nombres",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_procesamiento,
        text="Depurando y limpiando archivos",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_procesamiento,
        text="Homologando Archivos",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_procesamiento,
        text="Procesar subtotales",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_procesamiento,
        text="Archivo Maestro",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_procesamiento,
        text="Errores",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_procesamiento,
        text="Matricula preliminar",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_procesamiento,
        text="Compresion de informes",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_procesamiento,
        text="Envio de informes",
        font=("Arial", 14)
        )
    ]

espacio_izquierdo = tk.Label(
        frame_procesamiento,
        text="_____________________",
        font=("Arial", 14)
        )
espacio_derecho = tk.Label(
        frame_procesamiento,
        text="_____________________",
        font=("Arial", 14)
        )

for i, label in enumerate(labels_definidos):
    espacio_izquierdo.grid(row=i+1, column=0)
    espacio_derecho.grid(row=i+1, column=3)
    

labels = []
for i, label in enumerate(labels_definidos):
    label.grid(row=i+1, column=1)
    status_label = tk.Label(frame_procesamiento, text="Esperando...")
    status_label.grid(row=i+1, column=2, padx=10)
    labels.append(status_label)

funciones = [
    (renombrar_archivos_gui,[seleccion_textbox, ciclos, periodos, True]),
    (depurar_gui,[seleccion_textbox, ciclos, periodos]),
    (homologar_gui,[seleccion_textbox, ciclos, periodos]),
    (procesar_subtotales_gui,[seleccion_textbox, ciclos, periodos]),
    (archivo_maestro_gui,[seleccion_textbox, ciclos, periodos]),
    (errores_gui,[seleccion_textbox, ciclos, periodos]),
    (mapre_gui,[seleccion_textbox, ciclos, periodos]),
    (zip_gui,[seleccion_textbox, ciclos, periodos]),
    (enviar_correo_gui,[seleccion_textbox, ciclos, periodos])
    ]

crudo_regresar.config(
    command=lambda: ir_a_pestaña_n(1))
crudo_Generar.config(
    command=lambda: ejecutar_funciones(frame_procesamiento, labels, funciones))

notebook.add(frame_procesamiento, text="Procesamiento")

estilizar_pestañas(notebook)
notebook.select(notebook.tabs()[0])
root.mainloop()

