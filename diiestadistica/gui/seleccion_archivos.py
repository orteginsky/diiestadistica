import os
import tkinter as tk
from tkinter import filedialog

def seleccionar_carpeta():
    root = tk.Tk()
    root.withdraw()
    ruta_carpeta = filedialog.askdirectory(title="Selecciona la carpeta correspondiente")
    if ruta_carpeta:
        ruta_carpeta = os.path.normpath(ruta_carpeta)  # 🔑 Normaliza a C:\Users\...
        print(f"Carpeta Seleccionada: {ruta_carpeta}")
        return ruta_carpeta
    else:
        print("No se seleccionó ninguna carpeta")
        return

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    ruta_archivo = filedialog.askopenfilename(title="Selecciona un archivo")
    if ruta_archivo:
        ruta_archivo = os.path.normpath(ruta_archivo)  # 🔑 Normaliza
        print(f"Archivo Seleccionado: {ruta_archivo}")
        return ruta_archivo
    else:
        print("No se seleccionó ningún archivo")
        return

if __name__ == "__main__":
    import os
    ruta = seleccionar_archivo()
    print(ruta)
    if ruta is not None:
        _, nombre_archivo = os.path.split(ruta)
        print(nombre_archivo)
    else:
        print("No se obtuvo ruta de archivo.")