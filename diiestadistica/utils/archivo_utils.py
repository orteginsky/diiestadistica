from ..gui.seleccion_archivos import seleccionar_carpeta

import os
import pandas as pd


def cambiar_extencion_carpeta(old_extension = "xls", new_extension = "html"):
    carpeta = seleccionar_carpeta()
    print(f'haz camiado los archivos con extension: {old_extension} por la extension {new_extension}')
    for name_file in os.listdir(carpeta):
        if name_file.endswith(old_extension):
            root_file = f"{carpeta}/{name_file}"
            cambiar_extencion_archivo(root_file,new_extension)
        else:
            print('archivo conservado')


def cambiar_extencion_archivo(root_file,extension):
    only_name,_ = os.path.splitext(root_file)
    new_name = f"{only_name}" + "."+ f"{extension}"
    os.rename(root_file, new_name)
    #print(f"se ha cambiado la extencion tio del archivo {root_file} a la extension {extension} \n")
    #print(f"{new_name}")
    return new_name
if __name__=='__main__':
    cambiar_extencion_carpeta()


def renombrar_archivos(ruta_carpeta, bolean=False):
    """
    Renombra los archivos en la carpeta dada según el diccionario de nombres.

    :param ruta_carpeta: str - Ruta de la carpeta que contiene los archivos.
    :param diccionario_nombres: dict - Diccionario con los nombres actuales como claves y los nuevos nombres como valores.
    """

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
	"ConcentradoEgresadosSuperior.xls":"NS_Egresados.xls",
	"ConcentradoEgresadosPostgrado.xls":"NP_Egresados.xls",
	"ConcentradoTitulacion.xls":"NMS_Titulados.xls",
	"ConcentradoTitulacion (1).xls":"NS_Titulados.xls",
	"ConcentradoGraduadosPostgrado.xls":"NP_Titulados.xls"
	}

    if bolean:
        ruta_carpeta = f"{ruta_carpeta}/archivos_originales"


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



def eliminar_xlsx_vacios(ruta_directorio):
    """
    Elimina archivos .xlsx que solo tienen encabezados sin datos desde un directorio dado.

    Parámetros:
    ruta_directorio (str): Ruta absoluta del directorio que contiene archivos .xlsx
    """
    for archivo in os.listdir(ruta_directorio):
        if archivo.endswith(".xlsx"):
            ruta_archivo = os.path.join(ruta_directorio, archivo)
            try:
                df = pd.read_excel(ruta_archivo)
                if df.empty or df.dropna(how='all').shape[0] == 0:
                    os.remove(ruta_archivo)
                    print(f"Archivo eliminado (sin datos): {archivo}")
            except Exception as e:
                print(f"No se pudo procesar {archivo}: {e}")


def crear_subdirectorios(ruta_base, carpetas):
    """
    Crea carpetas dentro de un directorio dado.

    Parámetros:
        ruta_base (str): Ruta del directorio principal donde se crearán las carpetas.
        carpetas (list): Lista de nombres de carpetas a crear.

    Retorna:
        list: Lista de rutas completas de las carpetas creadas o existentes.
    """
    rutas_creadas = []
    for carpeta in carpetas:
        ruta_carpeta = os.path.join(ruta_base, carpeta)
        try:
            os.makedirs(ruta_carpeta, exist_ok=True)
            rutas_creadas.append(ruta_carpeta)
        except Exception as e:
            print(f"No se pudo crear la carpeta '{carpeta}': {e}")
    return rutas_creadas
