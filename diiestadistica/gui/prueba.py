import tkinter as tk
from tkinter import ttk

# Importaciones organizadas
from ..utils.archivo_utils import renombrar_archivos
from ..utils.os_utils import limpiar_descargas, crear_directorio, mover_archivos
from ..procesamiento.procesamiento_maestro import procesamiento_aplanamiento

from .ventana_base import (
    ventana_base, agregar_boton, agregar_periodo_box, agregar_ciclo_box, estilizar_pestañas,
    activar_descarga_intranet, seleccionar_carpeta, agregar_textbox, boton_carpeta
)

# Funciones de control de interfaz
def quitar():
    root.destroy()

def ir_a_pestaña(n):
    notebook.select(notebook.tabs()[n])

def iniciar():
    print("Se ha iniciado")
    ir_a_pestaña(1)

def limpiar():
    print("Se ha limpiado")
    ir_a_pestaña(2)
    limpiar_descargas()

def descargar(ciclos, periodos):
    print("Inicio de descarga")
    ir_a_pestaña(3)
    activar_descarga_intranet(ciclos.get(), periodos.get())

def generar_ruta(seleccion_textbox, ciclos, periodos):
    return f"{seleccion_textbox.get()}/periodo_{ciclos.get()}_{periodos.get()}"

def crear_directorio_gui(seleccion_textbox, ciclos, periodos, pestaña):
    crear_directorio(generar_ruta(seleccion_textbox, ciclos, periodos))
    ir_a_pestaña(pestaña)

def procesar_archivos_gui(seleccion_textbox, ciclos, periodos, funcion, boolean=True):
    funcion(generar_ruta(seleccion_textbox, ciclos, periodos), boolean)

def depurar_gui(seleccion_textbox, ciclos, periodos):
    procesamiento_aplanamiento(generar_ruta(seleccion_textbox, ciclos, periodos))

def homologar_archivos(ruta, boolean):
    if boolean:
        print(f"se ha homologado tio ruta: {ruta}")
    else:
        print("no tio")

def ejecutar_funciones(frame, labels, funciones, idx=0):
    if idx >= len(funciones):
        return
    
    func, args = funciones[idx]
    try:
        func(*args)
        labels[idx].config(text="✅", fg="green")
    except Exception as e:
        labels[idx].config(text="❌", fg="red")
        print(f"Error en la función {idx + 1}: {e}")
    
    frame.after(100, lambda: ejecutar_funciones(frame, labels, funciones, idx + 1))

# Configuración de la ventana principal
root = ventana_base(tk.Tk(), "I N I C I O")
notebook = ttk.Notebook(root, style="Vertical.TNotebook")
notebook.pack(expand=True, fill="both")

# Creación de pestañas
def crear_pestaña(titulo, frame, botones=[]):
    for texto, comando in botones:
        btn = agregar_boton(frame, texto)
        btn.config(command=comando)
    notebook.add(frame, text=titulo)

crear_pestaña("Inicio", ttk.Frame(notebook), [("Cerrar", quitar), ("Iniciar", iniciar)])
crear_pestaña("Limpieza Descargas", ttk.Frame(notebook), [("Regresar", lambda: ir_a_pestaña(0)), ("Limpiar", limpiar)])

frame_datos = ttk.Frame(notebook)
ciclos, periodos = agregar_ciclo_box(frame_datos), agregar_periodo_box(frame_datos)
crear_pestaña("Selección del Periodo Escolar", frame_datos, [("Regresar", lambda: ir_a_pestaña(1)), ("Confirmar", lambda: descargar(ciclos, periodos))])

frame_seleccion = ttk.Frame(notebook)
seleccion_textbox = agregar_textbox(frame_seleccion)
crear_pestaña("Selección de carpeta", frame_seleccion, [
    ("Seleccionar Carpeta", lambda: seleccionar_carpeta(seleccion_textbox)),
    ("Aceptar", lambda: crear_directorio_gui(seleccion_textbox, ciclos, periodos, 3)),
    ("Regresar", lambda: ir_a_pestaña(2))
])

frame_procesamiento = ttk.Frame(notebook)
labels_definidos = [
    tk.Label(frame_procesamiento, text=texto, font=("Arial", 14))
    for texto in ["Direccionando archivos", "Generando Nombres", "Depurando archivos", "Homologando Archivos"]
]
labels = [tk.Label(frame_procesamiento, text="Esperando...") for _ in labels_definidos]
for i, (label, status) in enumerate(zip(labels_definidos, labels)):
    label.grid(row=i+2, column=0)
    status.grid(row=i+2, column=1, padx=10)

funciones = [
    (lambda *args: procesar_archivos_gui(*args, renombrar_archivos), [seleccion_textbox, ciclos, periodos, True]),
    (lambda *args: procesar_archivos_gui(*args, mover_archivos), [seleccion_textbox, ciclos, periodos, True]),
    (depurar_gui, [seleccion_textbox, ciclos, periodos]),
    (lambda *args: procesar_archivos_gui(*args, homologar_archivos), [seleccion_textbox, ciclos, periodos, True])
]
crear_pestaña("Procesamiento", frame_procesamiento, [
    ("Regresar", lambda: ir_a_pestaña(3)),
    ("Procesar", lambda: ejecutar_funciones(frame_procesamiento, labels, funciones))
])

crear_pestaña("Informes", ttk.Frame(notebook), [("Regresar", lambda: ir_a_pestaña(1)), ("Generar MAPRE", quitar)])

estilizar_pestañas(notebook)
notebook.select(notebook.tabs()[0])
root.mainloop()
