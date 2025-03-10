import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ..scraping.credenciales import credenciales
from selenium import webdriver
from tkinter.ttk import *

import os
import shutil
import platform
def limpiar_descargas():
    # Detectar la carpeta de Descargas según el sistema operativo
    if platform.system() == "Windows":
        descarga_dir = os.path.join(os.environ["USERPROFILE"], "Downloads")
    else:  # macOS y Linux
        descarga_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    # Verificar si la carpeta existe
    if not os.path.exists(descarga_dir):
        print(f"La carpeta de Descargas no existe: {descarga_dir}")
        return

    # Recorrer todos los archivos y carpetas en Descargas
    for item in os.listdir(descarga_dir):
        item_path = os.path.join(descarga_dir, item)

        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)  # Eliminar archivos y enlaces
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Eliminar carpetas y su contenido
            print(f"Eliminado: {item_path}")
        except Exception as e:
            print(f"Error al eliminar {item_path}: {e}")

    print("🗑️ Carpeta de Descargas limpiada correctamente.")

def ventana_base(nueva_ventana,titulo="M A P R E"):
    nueva_ventana.title(titulo)
    nueva_ventana.geometry("800x533")
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

def reemplazar_ventana(ventana_actual,titulo,subtitulo):
    ventana_actual.destroy() 
    ventana = ventana_base(titulo,subtitulo)
    return ventana

def activar_descarga_intranet():
    driver=webdriver.Chrome()
    driver=credenciales(driver)

def agregar_selenium(nueva_ventana):
    color_fondo = "#5A1236"
    boton_cerrar = tk.Button(nueva_ventana, text="Inciar Descarga", font=("Arial", 12), 
                             command=activar_descarga_intranet, bg="#FFFFFF", fg=color_fondo)
    boton_cerrar.pack(pady=10)

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