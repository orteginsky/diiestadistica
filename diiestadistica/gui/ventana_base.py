import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ..scraping.credenciales import credenciales
from selenium import webdriver
from tkinter.ttk import *
from ..scraping.descarga_selenium import descarga_selenium

from tkinter import filedialog
import re
import os
import shutil
import platform

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

def limpiar_descargas():
    # Detectar la carpeta de Descargas según el sistema operativo
    descarga_dir = ruta_descargas()
    # Recorrer todos los archivos y carpetas en Descargas
    for item in os.listdir(descarga_dir):
        item_path = os.path.join(descarga_dir, item)

        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
            print(f"Eliminado: {item_path}")
        except Exception as e:
            print(f"Error al eliminar {item_path}: {e}")

    print("Carpeta de Descargas limpiada correctamente.")

def ventana_base(nueva_ventana,titulo="M A P R E"):
    nueva_ventana.title(titulo)
    nueva_ventana.geometry("900x400")
    color_fondo = "#5A1236"
    nueva_ventana.configure(bg=color_fondo)
    return nueva_ventana

def colores(ventana):
    s = Style()
    s.configure('new.TFrame', background='#5A1236')
    ventana = Frame(ventana, style='new.TFrame')
    ventana.pack(pady=20)
    return ventana

def agregar_boton(nueva_ventana,nombre):
    color_fondo = "#5A1236"
    boton_cerrar = tk.Button(nueva_ventana, text=nombre, font=("Arial", 12), 
                             bg="#FFFFFF", fg=color_fondo)
    boton_cerrar.pack(pady=10)
    return boton_cerrar

def agregar_ciclo_box(nueva_ventana):
    año_actual = datetime.now().year
    ciclos_anuales = [f"{a}-{a+1}" for a in range(2010, año_actual + 1)]
    ciclo_var = tk.StringVar()
    combobox = ttk.Combobox(nueva_ventana, textvariable=ciclo_var, values=ciclos_anuales, state="readonly")
    combobox.pack(pady=10)
    combobox.current(len(ciclos_anuales) - 1)
    return combobox

def agregar_periodo_box(nueva_ventana):
    periodo_var = tk.StringVar()
    combobox_1 = ttk.Combobox(
        nueva_ventana,
        textvariable=periodo_var,
        values=[1,2],
        state="readonly"
        )
    combobox_1.pack(pady=10)
    combobox_1.current(1)
    return combobox_1

def reemplazar_ventana(ventana_actual,titulo,subtitulo):
    ventana_actual.destroy() 
    ventana = ventana_base(titulo,subtitulo)
    return ventana

def activar_descarga_intranet(ciclo,periodo):
    anio_actual = datetime.now().year
    mes_actual = datetime.now().month
    anio_coincidencia = re.search(r"\d+", ciclo)
    periodo_coincidencia = re.search(r"\d",periodo)
    if anio_coincidencia:
        if periodo_coincidencia:
            anio_inicio = int(anio_coincidencia.group())
            semestre_inicio = int(periodo_coincidencia.group())
            if (anio_inicio!=anio_actual or (mes_actual>=8 and semestre_inicio==1 and anio_inicio==anio_actual)):
                print("todo bien")
                descarga_selenium(anio_inicio,semestre_inicio)
            else:
                print("Nada bien")
                return
        else:
            return            
    else:
        print("No se encontró ningún número en el elemento.")
        return

def limpiar_pestaña(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def agregar_label(nueva_ventana):
    color_fondo = "#5A1236"
    color_texto= "#FFFFFF"
    sub_label="Automatización"
    label = tk.Label(nueva_ventana, text=sub_label, 
                     font=("Arial", 40, "bold"), fg=color_texto, bg=color_fondo)
    label.pack(pady=20)


def estilizar_pestañas(notebook, bg_color="#5A1236", fg_color="white", padding=10):
    """
    Aplica un estilo profesional a cada pestaña en un ttk.Notebook.

    Parámetros:
    - notebook: El objeto ttk.Notebook al que se le aplicará el estilo.
    - bg_color: Color de fondo de las pestañas (por defecto: #5A1236).
    - fg_color: Color del texto de las pestañas (por defecto: blanco).
    - padding: Espaciado interno de las pestañas.
    """
    style = ttk.Style()

    # Cambiar color de fondo del Notebook (el contenedor de las pestañas)
    style.configure("TNotebook", background=bg_color)

    # Cambiar el estilo de las pestañas
    style.configure("TNotebook.Tab",
                    font=("Arial", 12, "bold"),
                    padding=[padding, padding],
                    foreground=fg_color)

    # Cambiar color cuando la pestaña está seleccionada
    style.map("TNotebook.Tab",
              background=[("selected", "#75204D")],  # Color cuando está seleccionada
              foreground=[("selected", "white")])
    
def seleccionar_carpeta(entry):
    carpeta = filedialog.askdirectory()
    if carpeta:
        entry.delete(0, tk.END)
        entry.insert(0, carpeta)

def agregar_textbox(frame):
    entry_ruta = ttk.Entry(frame, width=50)
    entry_ruta.pack(padx=5, pady=5, fill="x")
    return entry_ruta

def boton_carpeta(frame):
    boton_carpeta = ttk.Button(
        frame, text="📁")
    boton_carpeta.pack(pady=10)
    return boton_carpeta





