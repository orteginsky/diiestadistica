import os
import tkinter as tk
from tkinter import filedialog

from diiestadistica.core.logging_config import setup_logger

logger = setup_logger(__name__)


def seleccionar_carpeta():
    root = tk.Tk()
    root.withdraw()
    ruta_carpeta = filedialog.askdirectory(title="Selecciona la carpeta correspondiente")
    if ruta_carpeta:
        ruta_carpeta = os.path.normpath(ruta_carpeta)  # 🔑 Normaliza a C:\Users\...
        logger.info(f"Carpeta Seleccionada: {ruta_carpeta}")
        return ruta_carpeta
    else:
        logger.warning("No se seleccionó ninguna carpeta")
        return

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    ruta_archivo = filedialog.askopenfilename(title="Selecciona un archivo")
    if ruta_archivo:
        ruta_archivo = os.path.normpath(ruta_archivo)  # 🔑 Normaliza
        logger.info(f"Archivo Seleccionado: {ruta_archivo}")
        return ruta_archivo
    else:
        logger.warning("No se seleccionó ningún archivo")
        return

if __name__ == "__main__":
    import os
    ruta = seleccionar_archivo()
    logger.info(ruta)
    if ruta is not None:
        _, nombre_archivo = os.path.split(ruta)
        logger.info(nombre_archivo)
    else:
        logger.warning("No se obtuvo ruta de archivo.")