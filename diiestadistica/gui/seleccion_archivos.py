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

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    ruta_archivo = filedialog.askopenfilename(title="Selecciona la carpeta correspondiente")
    if ruta_archivo:
        print(f"Archivo Selecionado: {ruta_archivo}")
        return ruta_archivo
    else:
        print("No se selecciono ninguna archivo")
        return
    
if __name__ == "__main__":
    import os
    ruta=seleccionar_archivo()
    print(ruta)
    _, nombre_archivo =os.path.split(ruta)
    print(nombre_archivo)