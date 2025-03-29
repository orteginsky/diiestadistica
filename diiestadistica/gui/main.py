#from tkinter import Tk, Label, Button, ttk
#import subprocess

import tkinter as tk
from tkinter import ttk
from .ventana_base import ventana_base
from .ventana_base import agregar_boton
from .ventana_base import limpiar_descargas
from .ventana_base import agregar_periodo_box
from .ventana_base import agregar_ciclo_box
from .ventana_base import estilizar_pestañas
from .ventana_base import activar_descarga_intranet
from .ventana_base import seleccionar_carpeta
from .ventana_base import agregar_textbox
from .ventana_base import boton_carpeta
from ..procesamiento.nombrar import renombrar_archivos
import shutil
import os
import platform

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
def mapre():
    print("hostia tio ya esta generandose el mapre")
    quitar()


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

def generar_ruta(seleccion_textbox, ciclos, periodos):
    carpeta = seleccion_textbox.get()
    ciclo = ciclos.get()
    periodo = periodos.get()
    ruta_base = f"{carpeta}/periodo_{ciclo}_{periodo}"
    print(ruta_base)
    return ruta_base

def depurar(ruta_base, bolean = False):
    if bolean:
        print(f"se depuro en{ruta_base}")
    else:
        print("se depuro")

def homologar(ruta_base, bolean = False):
    if bolean:
        print(f"se homologo en{ruta_base}")
    else:
        print("se homologo")

def ruta_descargas():
    if platform.system() == "Windows":
        if os.path.isdir(os.path.join(os.environ["USERPROFILE"], "Downloads")):
            descarga_dir = os.path.join(os.environ["USERPROFILE"], "Downloads")
            return descarga_dir
        elif os.path.isdir(os.path.join(os.environ["USERPROFILE"], "Descargas")):
            descarga_dir = os.path.join(os.environ["USERPROFILE"], "Descargas")
            return descarga_dir
        else:
            return
    else:
        if os.path.isdir(os.path.join(os.path.expanduser("~"), "Downloads")):
            descarga_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            return descarga_dir
        elif os.path.isdir(os.path.join(os.path.expanduser("~"), "Descargas")):
            descarga_dir = os.path.join(os.path.expanduser("~"), "Descargas")
            return descarga_dir
        else:
            return

def crear_directorio(ruta_base):
    """
    Crea la estructura de carpetas necesaria para un ciclo y periodo específico.

    """
    
    # Lista de subdirectorios dentro del periodo
    subdirectorios = [
        "archivos_originales",
        "archivos_aplanados",
        "reportes",
        "archivos_homologados",
        "subtotales"
    ]

    try:
        # Crear la carpeta del periodo y sus subdirectorios
        os.makedirs(ruta_base, exist_ok=True)
        
        for sub in subdirectorios:
            os.makedirs(os.path.join(ruta_base, sub), exist_ok=True)

        print(f"Directorios creados exitosamente en '{ruta_base}'.")

    except Exception as e:
        print(f"❌ Error al crear la estructura de directorios: {e}")


def mover_archivos(ruta_base, bolean = False):

    if bolean:
        destino_final = f"{ruta_base}/archivos_originales"
    else:
        destino_final = ruta_base

    # Definir la ruta de la carpeta de "Descargas"
    path_descargas = ruta_descargas()
    
    # Verificar si la ruta de destino es válida
    if not os.path.exists(destino_final):
        print(f"La ruta de destino no existe: {destino_final}")
        return
    
    # Verificar si la carpeta de "Descargas" existe
    if not os.path.exists(path_descargas):
        print(f"La carpeta de 'Descargas' no existe: {path_descargas}")
        return

    # Obtener una lista de todos los archivos en la carpeta de "Descargas"
    archivos = os.listdir(path_descargas)

    # Mover cada archivo a la carpeta de destino final
    for archivo in archivos:
        ruta_origen = os.path.join(path_descargas, archivo)
        if os.path.isfile(ruta_origen):
            try:
                shutil.move(ruta_origen, destino_final)
                print(f"Archivo movido: {archivo}")
            except Exception as e:
                print(f"No se pudo mover el archivo {archivo}: {e}")



root = tk.Tk()
root = ventana_base(root,"I N I C I O")


# Crear el estilo
style = ttk.Style()
style.configure("Vertical.TNotebook", tabposition="wn")
style.configure("Vertical.TNotebook.Tab", width=40, padding=[10, 20])

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
notebook.add(frame_datos, text="Ingreso de Datos")


# Pestaña Selección de carpeta
frame_seleccion = ttk.Frame(notebook)
seleccion_textbox = agregar_textbox(frame_seleccion)
seleccion_seleccion = boton_carpeta(frame_seleccion)
seleccion_seleccion.config(command=lambda: seleccionar_carpeta(seleccion_textbox))
seleccion_aceptar = agregar_boton(frame_seleccion,"Aceptar")

seleccion_aceptar.config(command=lambda: crear_directorio(generar_ruta(seleccion_textbox, ciclos, periodos)))
seleccion_regresar = agregar_boton(frame_seleccion,"Regresar")
seleccion_regresar.config(command=lambda: print(generar_ruta(seleccion_textbox, ciclos, periodos))) #ir_a_pestaña_n(2)
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
crudo_Generar.grid(row=1, column=0)

labels_definidos = [
    tk.Label(frame_procesamiento, text="Direccionando archivos", font=("Arial", 14)),
    tk.Label(frame_procesamiento, text="Generando Nombres", font=("Arial", 14)),
    tk.Label(frame_procesamiento, text="Depurando y limpiando archivos", font=("Arial", 14)),
    tk.Label(frame_procesamiento, text="Homologando Archivos", font=("Arial", 14)),
]

labels = []
for i, label in enumerate(labels_definidos):
    label.grid(row=i+2, column=0)
    status_label = tk.Label(frame_procesamiento, text="Esperando...")
    status_label.grid(row=i+2, column=1, padx=10)
    labels.append(status_label)

"""
funciones = [
    (renombrar_archivos, [generar_ruta(seleccion_textbox, ciclos, periodos), True]),
    (mover_archivos, [generar_ruta(seleccion_textbox, ciclos, periodos), True]),
    (depurar, [generar_ruta(seleccion_textbox, ciclos, periodos), True]),
    (homologar, [generar_ruta(seleccion_textbox, ciclos, periodos), True])
]
"""
def renombrar_archivos_gui(seleccion_textbox, ciclos, periodos, boolean= True):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    renombrar_archivos(ruta_base, boolean)
def mover_archivos_gui(seleccion_textbox, ciclos, periodos, boolean= True):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    mover_archivos(ruta_base, boolean)

def depurar_gui(seleccion_textbox, ciclos, periodos, boolean= True):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    depurar(ruta_base, boolean)

def homologar_gui(seleccion_textbox, ciclos, periodos, boolean= True):
    ruta_base = generar_ruta(seleccion_textbox, ciclos, periodos)
    homologar(ruta_base, boolean)

funciones = [
    (renombrar_archivos_gui,[seleccion_textbox, ciclos, periodos, True]),
    (mover_archivos_gui,[seleccion_textbox, ciclos, periodos, True]),
    (depurar_gui,[seleccion_textbox, ciclos, periodos, True]),
    (homologar_gui,[seleccion_textbox, ciclos, periodos, True])
    ]

crudo_regresar.config(
    command=lambda: ir_a_pestaña_n(3))
crudo_Generar.config(
    command=lambda: ejecutar_funciones(frame_procesamiento, labels, funciones))

notebook.add(frame_procesamiento, text="Procesamiento")




# Pestaña Generacion de Informes
frame_generacion = ttk.Frame(notebook)
generacion_regresar = agregar_boton(frame_generacion,"Regresar")
generacion_regresar.config(command=lambda: ir_a_pestaña_n(1))
generacion_Generar = agregar_boton(frame_generacion,"Generar MAPRE")
generacion_Generar.config(command=mapre)
notebook.add(frame_generacion, text="Informes")

estilizar_pestañas(notebook)
notebook.select(notebook.tabs()[0])
root.mainloop()

