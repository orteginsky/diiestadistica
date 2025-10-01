from ..gui.seleccion_archivos import seleccionar_carpeta

import pandas as pd
from pathlib import Path

from diiestadistica.core.logging_config import setup_logger

logger = setup_logger(__name__)

def cambiar_extencion_carpeta(old_extension="xls", new_extension="html"):
    carpeta_str = seleccionar_carpeta()
    if carpeta_str is None:
        logger.info("No se seleccionó ninguna carpeta.")
        return
    carpeta = Path(carpeta_str)
    logger.info(f"Haz cambiado los archivos con extensión: {old_extension} por la extensión {new_extension}")

    for file_path in carpeta.iterdir():
        if file_path.suffix == f".{old_extension}":
            cambiar_extencion_archivo(file_path, new_extension)
        else:
            logger.info(f"Archivo conservado: {file_path.name}")


def cambiar_extencion_archivo(file_path: Path, new_extension: str):
    new_file = file_path.with_suffix(f".{new_extension}")
    file_path.rename(new_file)
    return new_file


def renombrar_archivos(ruta_carpeta, bolean=False):
    """
    Renombra los archivos en la carpeta dada según el diccionario de nombres.
    """
    diccionario_nombres = {
        "Concentrado_Matricula_Inscrita.xls": "NMS_Basica.xls",
        "Concentrado_Poblacion_Atendida_Mod_Escolariza_Superior.xls": "NS_Basica.xls",
        "Concentrado_Poblacion_Atendida.xls": "NP_Basica.xls",
        "Concentrado.xls": "NMS_Aprovechamiento.xls",
        "Concentrado (1).xls": "NS_Aprovechamiento.xls",
        "Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo (1).xls": "NMS_Turno.xls",
        "Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo (3).xls": "NS_Turno.xls",
        "Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo (4).xls": "NP_Turno.xls",
        "Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo.xls": "NMS_Semestre.xls",
        "Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo (2).xls": "NS_Semestre.xls",
        "Concentrado_Poblacion_Atendida__Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo.xls": "NP_Semestre.xls",
        "Concentrado_Matricula_Por_Grupos_Edad_NMS.xls": "NMS_Grupos.xls",
        "Concentrado_Matricula_Por_Grupos_Edad_NMS (1).xls": "NS_Grupos.xls",
        "Concentrado_Matricula_Por_Grupos_Edad_NMS (2).xls": "NP_Grupos.xls",
        "ConcentradoEgresadosMedioSuperior.xls": "NMS_Egresados.xls",
        "ConcentradoEgresadosSuperior.xls": "NS_Egresados.xls",
        "ConcentradoEgresadosPostgrado.xls": "NP_Egresados.xls",
        "ConcentradoTitulacion.xls": "NMS_Titulados.xls",
        "ConcentradoTitulacion (1).xls": "NS_Titulados.xls",
        "ConcentradoGraduadosPostgrado.xls": "NP_Titulados.xls"
    }

    ruta = Path(ruta_carpeta)
    if bolean:
        ruta = ruta / "archivos_originales"

    if not ruta.is_dir():
        logger.info(f"Error: La ruta '{ruta}' no es una carpeta válida.")
        return

    for file_path in ruta.iterdir():
        if file_path.name in diccionario_nombres:
            new_file = ruta / diccionario_nombres[file_path.name]
            if new_file.exists():
                logger.info(f"Advertencia: No se renombró '{file_path.name}' porque '{new_file.name}' ya existe.")
            else:
                file_path.rename(new_file)
                logger.info(f"Renombrado: '{file_path.name}' → '{new_file.name}'")
        else:
            logger.info(f"Sin cambio: '{file_path.name}' no está en el diccionario.")


def eliminar_xlsx_vacios(ruta_directorio):
    """
    Elimina archivos .xlsx que solo tienen encabezados sin datos desde un directorio dado.
    """
    ruta = Path(ruta_directorio)
    for file_path in ruta.glob("*.xlsx"):
        try:
            df = pd.read_excel(file_path)
            if df.empty or df.dropna(how="all").shape[0] == 0:
                file_path.unlink()
                logger.info(f"Archivo eliminado (sin datos): {file_path.name}")
        except Exception as e:
            logger.info(f"No se pudo procesar {file_path.name}: {e}")


def crear_subdirectorios(ruta_base, carpetas):
    """
    Crea carpetas dentro de un directorio dado.
    """
    base = Path(ruta_base)
    rutas_creadas = []
    for carpeta in carpetas:
        ruta_carpeta = base / carpeta
        try:
            ruta_carpeta.mkdir(parents=True, exist_ok=True)
            rutas_creadas.append(ruta_carpeta)
        except Exception as e:
            logger.info(f"No se pudo crear la carpeta '{carpeta}': {e}")
    return rutas_creadas
