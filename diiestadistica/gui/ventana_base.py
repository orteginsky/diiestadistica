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

import os

def crear_directorio(directory_paths, ciclos, periodos):
    """
    Crea la estructura de carpetas necesaria para un ciclo y periodo específico.

    :param directory_path: Ruta base donde se crearán los directorios.
    :param ciclo: Ciclo académico (ej. "2024-2025").
    :param periodo: Periodo académico (ej. "01").
    """
    directory_path = directory_paths.get()
    ciclo = ciclos.get()
    periodo = periodos.get()
    ruta_periodo = os.path.join(directory_path, f"periodo_{ciclo}_{periodo}")
    
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
        os.makedirs(ruta_periodo, exist_ok=True)
        
        for sub in subdirectorios:
            os.makedirs(os.path.join(ruta_periodo, sub), exist_ok=True)

        print(f"Directorios creados exitosamente en '{ruta_periodo}'.")

    except Exception as e:
        print(f"❌ Error al crear la estructura de directorios: {e}")


def mover_archivos(destinos,ciclos, periodos):
    destino = destinos.get()
    ciclo = ciclos.get()
    periodo = periodos.get()
    # Definir la ruta de la carpeta de "Descargas"
    path_descargas = ruta_descargas()
    destino_final = f"{destino}/periodo_{ciclo}_{periodo}/archivos_originales"
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




def ejecutar_funciones(frame, labels, funciones, idx=0):
    """
    Ejecuta funciones en orden, esperando que cada una termine antes de continuar con la siguiente.

    :param frame: ttk.Frame donde están los labels.
    :param labels: Lista de labels donde se mostrarán los resultados (✅ o ❌).
    :param funciones: Lista de funciones a ejecutar.
    :param idx: Índice de la función actual (para llamadas recursivas).
    """
    if idx >= len(funciones):
        return

    try:
        funciones[idx]()
        labels[idx].config(text="✅", fg="green")
    except Exception as e:
        labels[idx].config(text="❌", fg="red")
        print(f"Error en la función {idx + 1}: {e}")

    # Llamar a la siguiente función después de terminar
    frame.after(100, lambda: ejecutar_funciones(frame, labels, funciones, idx + 1))

