#from tkinter import Tk, Label, Button, ttk
#import subprocess

import tkinter as tk
from tkinter import ttk
from .ventana_base import ventana_base, agregar_boton
from .ventana_base import agregar_ciclo_box, limpiar_descargas, agregar_periodo_box
from .ventana_base import estilizar_pestañas
from .ventana_base import activar_descarga_intranet
from .ventana_base import seleccionar_carpeta
from .ventana_base import agregar_textbox
from .ventana_base import boton_carpeta
from .ventana_base import crear_directorio
from .ventana_base import mover_archivos

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

def mover(seleccion_textbox,ciclos, periodos):
    mover_archivos(seleccion_textbox,ciclos, periodos)

root = tk.Tk()
root = ventana_base(root,"I N I C I O")

notebook = ttk.Notebook(root)
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
seleccion_aceptar.config(command=lambda: crear_directorio(seleccion_textbox,ciclos, periodos))
seleccion_regresar = agregar_boton(frame_seleccion,"Regresar")
seleccion_regresar.config(command=lambda: ir_a_pestaña_n(2))
notebook.add(frame_seleccion, text="Selección de carpeta")

# Pestaña Procesamiento de datos
frame_procesamiento_crudo = ttk.Frame(notebook)
crudo_regresar = agregar_boton(frame_procesamiento_crudo,"Regresar")
crudo_regresar.config(command=lambda: ir_a_pestaña_n(3))
crudo_Generar = agregar_boton(frame_procesamiento_crudo,"Procesar datos")
crudo_Generar.config(command=lambda: mover(seleccion_textbox,ciclos, periodos))
notebook.add(frame_procesamiento_crudo, text="Procesamiento")

# Pestaña Procesamiento de Informes
frame_procesamiento = ttk.Frame(notebook)
procesamiento_regresar = agregar_boton(frame_procesamiento,"Regresar")
procesamiento_regresar.config(command=lambda: ir_a_pestaña_n(1))
procesamiento_Generar = agregar_boton(frame_procesamiento,"Generar MAPRE")
procesamiento_Generar.config(command=mapre)
notebook.add(frame_procesamiento, text="Procesamiento")

estilizar_pestañas(notebook)
notebook.select(notebook.tabs()[0])
root.mainloop()

