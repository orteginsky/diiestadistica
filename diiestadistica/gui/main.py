from ..utils.archivo_utils import renombrar_archivos
from ..utils.os_utils import limpiar_descargas
from ..utils.os_utils import crear_directorio
from ..utils.os_utils import mover_archivos
from ..procesamiento.procesamiento_maestro import procesamiento_aplanamiento
from ..procesamiento.procesamiento_maestro import procesamiento_limpieza
from ..procesamiento.procesar_subtotales import procesar_subtotales
from ..informes.arch_maestro import informes_mapre

from .ventana_base import ventana_base
from .ventana_base import agregar_boton
from .ventana_base import agregar_periodo_box
from .ventana_base import agregar_ciclo_box
from .ventana_base import estilizar_pestañas
from .ventana_base import activar_descarga_intranet
from .ventana_base import seleccionar_carpeta
from .ventana_base import agregar_textbox
from .ventana_base import boton_carpeta

import tkinter as tk
from tkinter import ttk

def quitar():
    notebook.destroy()
    root.destroy()
def ir_a_pestaña_n(n):
    notebook.select(notebook.tabs()[n])
def iniciar():
    print("se ha iniciao")
    ir_a_pestaña_n(1)
def limpiar():
    print("se ha limpao")
    ir_a_pestaña_n(2)
    limpiar_descargas()

def descargar(ciclos, periodos):
    print("se ha confirmado y se empezara a descargar tio")
    ir_a_pestaña_n(3)
    ciclo = ciclos.get()
    periodo = periodos.get()
    print(ciclo,periodo)
    activar_descarga_intranet(ciclo,periodo)

def generar_ruta(seleccion_textbox, ciclos, periodos):
    carpeta = seleccion_textbox.get()
    ciclo = ciclos.get()
    periodo = periodos.get()
    ruta_base = f"{carpeta}/periodo_{ciclo}_{periodo}"
    return ruta_base


def depurar(ruta_base, bolean = False):
    if bolean:
        print(f"se depuro en{ruta_base}")
    else:
        print("se depuro")


def crear_directorio_gui(seleccion_textbox, ciclos, periodos, pestaña):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    crear_directorio(ruta_base)
    ir_a_pestaña_n(pestaña)

def renombrar_archivos_gui(seleccion_textbox, ciclos, periodos, boolean= True):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    renombrar_archivos(ruta_base, boolean)

def mover_archivos_gui(seleccion_textbox, ciclos, periodos, boolean= True):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    mover_archivos(ruta_base, boolean)
    
def depurar_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    procesamiento_aplanamiento(ruta_base)

def homologar_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    procesamiento_limpieza(ruta_base)


def archivo_maestro_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    informes_mapre(ruta_base)
def errores_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
def mapre_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
def zip_gui(seleccion_textbox, ciclos, periodos):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)

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
        print(f"Error en la función {idx + 1}: {e}")

    # Llamar a la siguiente función después de terminar
    frame.after(100, lambda: ejecutar_funciones(frame, labels, funciones, idx + 1))

root = tk.Tk()
root = ventana_base(root,"I N I C I O")

# Crear el estilo
style = ttk.Style()
style.configure("Vertical.TNotebook", tabposition="wn")
style.configure(
    "Vertical.TNotebook.Tab",
    width=35,
    background="#F1F1F1",
    foreground="#333333",
    padding=[10, 20],
    font=("Arial", 16)
)

# Color cuando está seleccionada
style.map("Vertical.TNotebook.Tab",
          background=[("selected", "#F1F1F1")],
          foreground=[("selected", "#5A1236")])

notebook = ttk.Notebook(root, style="Vertical.TNotebook")
notebook.pack(expand=True, fill="both")

# Pestaña Inicio
frame_inicio = ttk.Frame(notebook)
frame_inicio.config()
label_inicio = tk.Label(frame_inicio, text="Bienvenido a la aplicación\nAquí puedes automatizar procesos estadísticos.", font=("Arial", 14))
label_inicio.pack(pady=20)
inicio_cerrar = agregar_boton(frame_inicio,"Cerrar")
inicio_iniciar = agregar_boton(frame_inicio,"Iniciar")
inicio_cerrar.config(command=quitar)
inicio_iniciar.config(command=iniciar)
notebook.add(frame_inicio, text="Inicio")

# Pestaña Eliminación de Descargas
frame_limpieza = ttk.Frame(notebook)
limpieza_regresar = agregar_boton(frame_limpieza,"Regresar")
limpieza_regresar.config(command=lambda: ir_a_pestaña_n(0))
limpieza_limpiar = agregar_boton(frame_limpieza,"Limpiar")
limpieza_limpiar.config(command=limpiar)
notebook.add(frame_limpieza, text="Limpieza Descargas")

# Pestaña Ingreso de Datos
frame_datos = ttk.Frame(notebook)
ciclos = agregar_ciclo_box(frame_datos)
periodos = agregar_periodo_box(frame_datos)
datos_regresar = agregar_boton(frame_datos,"Regresar")
datos_regresar.config(command=lambda: ir_a_pestaña_n(1))
datos_Confirmar = agregar_boton(frame_datos,"Confirmar Selección")
datos_Confirmar.config(command=lambda: descargar(ciclos,periodos))
notebook.add(frame_datos, text="Selección del Periodo Escolar")


# Pestaña Selección de carpeta
frame_seleccion = ttk.Frame(notebook)
seleccion_textbox = agregar_textbox(frame_seleccion)
seleccion_seleccion = boton_carpeta(frame_seleccion)
seleccion_seleccion.config(command=lambda: seleccionar_carpeta(seleccion_textbox))
seleccion_aceptar = agregar_boton(frame_seleccion,"Aceptar")
seleccion_aceptar.config(command=lambda: crear_directorio_gui(seleccion_textbox, ciclos, periodos,4))
seleccion_regresar = agregar_boton(frame_seleccion,"Regresar")
seleccion_regresar.config(command=lambda: ir_a_pestaña_n(2))
notebook.add(frame_seleccion, text="Selección de carpeta")


# Pestaña Procesamiento de datos
frame_procesamiento = ttk.Frame(notebook)
frame_procesamiento.grid()

crudo_regresar = tk.Button(
    frame_procesamiento,
    text="Regresar",
    font=("Arial", 12),
    bg="#FFFFFF",
    fg="#5A1236")
crudo_regresar.grid(row=0, column=0)
crudo_Generar = tk.Button(
    frame_procesamiento,
    text="Procesar",
    font=("Arial", 12),
    bg="#FFFFFF",
    fg="#5A1236")
crudo_Generar.grid(row=0, column=1)

labels_definidos = [
    tk.Label(frame_procesamiento, text="Direccionando archivos", font=("Arial", 14)),
    tk.Label(frame_procesamiento, text="Generando Nombres", font=("Arial", 14)),
    tk.Label(frame_procesamiento, text="Depurando y limpiando archivos", font=("Arial", 14)),
    tk.Label(frame_procesamiento, text="Homologando Archivos", font=("Arial", 14))
]

labels = []
for i, label in enumerate(labels_definidos):
    label.grid(row=i+1, column=0)
    status_label = tk.Label(frame_procesamiento, text="Esperando...")
    status_label.grid(row=i+1, column=1, padx=10)
    labels.append(status_label)



funciones = [
    (mover_archivos_gui,[seleccion_textbox, ciclos, periodos, True]),
    (renombrar_archivos_gui,[seleccion_textbox, ciclos, periodos, True]),
    (depurar_gui,[seleccion_textbox, ciclos, periodos]),
    (homologar_gui,[seleccion_textbox, ciclos, periodos])
    ]

crudo_regresar.config(
    command=lambda: ir_a_pestaña_n(3))
crudo_Generar.config(
    command=lambda: ejecutar_funciones(frame_procesamiento, labels, funciones))

notebook.add(frame_procesamiento, text="Procesamiento")

# Pestaña Generacion de Informes
frame_generacion = ttk.Frame(notebook)
frame_generacion.grid()

generacion_regresar = tk.Button(
    frame_generacion,
    text="Regresar",
    font=("Arial", 12),
    bg="#FFFFFF",
    fg="#5A1236")
generacion_regresar.grid(row=0, column=0)

generacion_Generar = tk.Button(
    frame_generacion,
    text="Generar Informes",
    font=("Arial", 12),
    bg="#FFFFFF",
    fg="#5A1236")
generacion_Generar.grid(row=0, column=1)

labels_definidos_generacion = [
    tk.Label(
        frame_generacion,
        text="Archivo Maestro",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_generacion,
        text="Errores",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_generacion,
        text="Matricula preliminar",
        font=("Arial", 14)
        ),
    tk.Label(
        frame_generacion,
        text="Compresion de informes",
        font=("Arial", 14)
        )
]

labels_generacion = []
for i, label in enumerate(labels_definidos_generacion):
    label.grid(row=i+1, column=0)
    status_label = tk.Label(frame_generacion, text="Esperando...")
    status_label.grid(row=i+1, column=1, padx=10)
    labels_generacion.append(status_label)


generacion_regresar.config(command=lambda: ir_a_pestaña_n(4))

funciones_generacion = [
    (archivo_maestro_gui,[seleccion_textbox, ciclos, periodos]),
    (errores_gui,[seleccion_textbox, ciclos, periodos]),
    (mapre_gui,[seleccion_textbox, ciclos, periodos]),
    (zip_gui,[seleccion_textbox, ciclos, periodos])
    ]

generacion_Generar.config(
    command=lambda: ejecutar_funciones(frame_generacion, labels_generacion, funciones_generacion))

notebook.add(frame_generacion, text="Informes")

# Pestaña enviar archivos
frame_enviar = ttk.Frame(notebook)
enviar_regresar = agregar_boton(frame_enviar,"Regresar")
enviar_regresar.config(command=lambda: ir_a_pestaña_n(5))
enviar_Generar = agregar_boton(frame_enviar,"Enviar Informes")
notebook.add(frame_enviar, text="Enviar Informes")

estilizar_pestañas(notebook)
notebook.select(notebook.tabs()[0])
root.mainloop()

