import tkinter as tk
from tkinter import filedialog

def seleccionar_carpeta():
    root = tk.Tk()
    root.withdraw()
    ruta_carpeta = filedialog.askdirectory(title="Selecciona la carpeta correspondiente")
    if ruta_carpeta:
        print(f"Carpeta Selecionada: {ruta_carpeta}")
        return ruta_carpeta
    else:
        print("No se selecciono ninguna carpeta")
        return