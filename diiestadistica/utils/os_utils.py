import os
import shutil
import platform

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

