from .seleccionar_carpeta import seleccionar_carpeta
import os


def renombrar_archivos(ruta_carpeta, diccionario_nombres):
    """
    Renombra los archivos en la carpeta dada según el diccionario de nombres.

    :param ruta_carpeta: str - Ruta de la carpeta que contiene los archivos.
    :param diccionario_nombres: dict - Diccionario con los nombres actuales como claves y los nuevos nombres como valores.
    """
	
    if not os.path.isdir(ruta_carpeta):
        print(f"Error: La ruta '{ruta_carpeta}' no es una carpeta válida.")
        return

    archivos = os.listdir(ruta_carpeta)

    for archivo in archivos:
        ruta_actual = os.path.join(ruta_carpeta, archivo)
        
        # Si el archivo está en el diccionario, renombrarlo
        if archivo in diccionario_nombres:
            nuevo_nombre = diccionario_nombres[archivo]
            nueva_ruta = os.path.join(ruta_carpeta, nuevo_nombre)
            
            # Verificar si ya existe un archivo con el nuevo nombre
            if os.path.exists(nueva_ruta):
                print(f"Advertencia: No se renombró '{archivo}' porque '{nuevo_nombre}' ya existe.")
            else:
                os.rename(ruta_actual, nueva_ruta)
                print(f"Renombrado: '{archivo}' → '{nuevo_nombre}'")
        else:
            print(f"Sin cambio: '{archivo}' no está en el diccionario.")


import pandas as pd

def generar_columnas(descripcion, columnas, dataframe):
    """
    Genera nuevas columnas en un DataFrame a partir de una cadena de texto y una tupla de nombres de columna.

    :param descripcion: str - Cadena con el formato "palabra1_palabra2".
    :param columnas: tuple - Tupla con los nombres de las nuevas columnas (columna_1, columna_2).
    :param dataframe: pd.DataFrame - DataFrame al que se agregarán las nuevas columnas.
    :return: pd.DataFrame - DataFrame con las nuevas columnas agregadas.
    """
    if not isinstance(descripcion, str) or "_" not in descripcion:
        raise ValueError("La descripción debe ser un string en formato 'palabra1_palabra2'.")

    if not isinstance(columnas, tuple) or len(columnas) != 2:
        raise ValueError("Las columnas deben ser una tupla con exactamente dos elementos.")

    palabra1, palabra2 = descripcion.split("_", 1)

    # Agregar las nuevas columnas al DataFrame
    dataframe[columnas[0]] = palabra1
    dataframe[columnas[1]] = palabra2

    return dataframe



if __name__=="__main__":
    diccionario_nombres = {
	"Concentrado_Matricula_Inscrita.xls":"NMS_Basica.xls",
	"Concentrado_Poblacion_Atendida_Mod_Escolariza_Superior.xls":"NS_Basica.xls",
	"Concentrado_Poblacion_Atendida.xls":"NP_Basica.xls",
	"Concentrado.xls": "NMS_Aprovechamiento.xls",
	"Concentrado (1).xls": "NS_Aprovechamiento.xls",
	"Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo (1).xls":"NMS_Turno.xls",
	"Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo (3).xls":"NS_Turno.xls",
	"Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo (4).xls":"NP_Turno.xls",
	"Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo.xls":"NMS_Semestre.xls",
	"Concentrado_Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo (2).xls":"NS_Semestre.xls",
	"Concentrado_Poblacion_Atendida__Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo.xls":"NP_Semestre.xls",
	"Concentrado_Matricula_Por_Grupos_Edad_NMS.xls":"NMS_Grupos.xls",
	"Concentrado_Matricula_Por_Grupos_Edad_NMS (1).xls":"NS_Grupos.xls",
	"Concentrado_Matricula_Por_Grupos_Edad_NMS (2).xls":"NP_Grupos.xls",
	"ConcentradoEgresadosMedioSuperior.xls":"NMS_Egresados.xls",
	"ConcentradoEgresadosMedioSuperior (1).xls":"NS_Egresados.xls",
	"ConcentradoEgresadosPostgrado.xls":"NP_Egresados.xls",
	"ConcentradoTitulacion.xls":"NMS_Titulados.xls",
	"ConcentradoTitulacion (1).xls":"NS_Titulados.xls",
	"ConcentradoGraduadosPostgrado.xls":"NP_Titulados.xls"
	}
    ruta = seleccionar_carpeta()
    renombrar_archivos(ruta, diccionario_nombres)
