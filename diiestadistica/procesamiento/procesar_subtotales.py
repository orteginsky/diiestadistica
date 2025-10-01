from ..utils.archivo_utils import eliminar_xlsx_vacios
from ..utils.archivo_utils import crear_subdirectorios

import pandas as pd
import os

from diiestadistica.core.logging_config import setup_logger

logger = setup_logger(__name__)
ruta_catalogos = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def homologar_subtotales(ruta_subtotales,ruta_unidades):
	unidades = pd.read_excel(ruta_unidades)
	for nombre_archivo in os.listdir(ruta_subtotales):
		try:
			if nombre_archivo.endswith("xlsx"):
				ruta_archivo = os.path.normpath(os.path.join(ruta_subtotales,nombre_archivo))
				dataframe = pd.read_excel(ruta_archivo)
				if "Sexo" in dataframe.columns:
					dataframe = dataframe[dataframe['Sexo']!='H..M']
					left_on = [col for col in dataframe.columns if col not in ['Sexo','Datos']]
					columnas_agrupacion = [col for col in dataframe.columns if col not in ['Sexo','Datos']]
					ceros = dataframe.groupby(columnas_agrupacion, as_index=False)['Datos'].sum()
					ceros = ceros[ceros['Datos']==0]
					sin_ceros = dataframe.merge(ceros[left_on], on=left_on, how='left', indicator=True)
					dataframe = sin_ceros[sin_ceros['_merge'] == 'left_only'].drop(columns=['_merge'])
					dataframe = dataframe[~dataframe["Sexo"].str.contains("Subt", na=False)]
					dataframe["Sexo"] = dataframe["Sexo"].replace({
						"^H$": "Hombres",
						"^M$": "Mujeres",
						"^Hom$": "Hombres",
						"^Muj$": "Mujeres"
					}, regex=True)
				elif "Concepto" in dataframe.columns:
					left_on = [col for col in dataframe.columns if col not in ['Concepto','Datos']]
					columnas_agrupacion = [col for col in dataframe.columns if col not in ['Concepto','Datos']]
					ceros = dataframe.groupby(columnas_agrupacion, as_index=False)['Datos'].sum()
					ceros = ceros[ceros['Datos']==0]
					sin_ceros = dataframe.merge(ceros[left_on], on=left_on, how='left', indicator=True)
					dataframe = sin_ceros[sin_ceros['_merge'] == 'left_only'].drop(columns=['_merge'])
				else:
					logger.warning("Sin columnas a homologar")
					return

				if "Concepto" in dataframe.columns:
					dataframe["Concepto"] = dataframe["Concepto"].astype(str)
					dataframe = dataframe[~dataframe["Concepto"].str.contains("Subt", na=False)]
					dataframe["Concepto"] = dataframe["Concepto"].replace({
						"^V$": "Vespertino",
						"^M$": "Matutino",
						"^Ves$": "Vespertino",
						"^Mix$": "Mixto",
						"^Mat$": "Matutino",
						"^Primer Ingreso$": "Nuevo Ingreso",
						"\\.": " "
					}, regex=True)
				
				if "Turno" in dataframe.columns:
					dataframe["Turno"] = dataframe["Turno"].astype(str)
					dataframe = dataframe[~dataframe["Turno"].str.contains("Subt", na=False)]
					dataframe["Turno"] = dataframe["Turno"].replace({
						"^V$": "Vespertino",
						"^M$": "Matutino",
						"^Ves$": "Vespertino",
						"^Mix$": "Mixto",
						"^Mat$": "Matutino",
						"\\.": " "
					}, regex=True)
				dataframe = dataframe.merge(unidades, left_on="Unidad.Academica", right_on="nombre_intranet", how="left")
				dataframe.to_excel(ruta_archivo, index=False)
		except:
			logger.error(nombre_archivo)

def sub_totales_unidad(ruta_global, ruta_unidades, ruta_programas):
	programas = pd.read_excel(ruta_programas)
	unidades = pd.read_excel(ruta_unidades)
	lista_filtro = [col for col in unidades.columns]
	lista_filtro.append('Programa')
	lista_filtro.append('Datos')
	for col in programas.columns:
		lista_filtro.append(col)
	ruta_homologado = os.path.normpath(os.path.join(ruta_global,"archivos_homologados"))
	ruta_subunidades = os.path.normpath(os.path.join(os.path.join(ruta_global,"subtotales"),"sub_totales_unidad"))
	for nombre_archivo in os.listdir(ruta_homologado):
		try:
			if nombre_archivo.endswith('xlsx'):
				ruta_archivo = os.path.normpath(os.path.join(ruta_homologado,nombre_archivo))
				dataframe = pd.read_excel(ruta_archivo)
				columnas_importantes = [col for col in dataframe.columns if col not in lista_filtro]
				dataframe = dataframe.groupby(columnas_importantes, as_index=False)['Datos'].sum()
				write_root = os.path.normpath(os.path.join(ruta_subunidades,nombre_archivo))
				dataframe.to_excel(write_root, index=False)
		except:
			logger.error(nombre_archivo)


def sub_totales_rama(ruta_global, ruta_unidades, ruta_programas):
	programas = pd.read_excel(ruta_programas)
	unidades = pd.read_excel(ruta_unidades)
	lista_filtro = [col for col in unidades.columns if col not in ['Rama_intranet']]
	lista_filtro.append('Programa')
	lista_filtro.append('Datos')
	lista_filtro.append('Unidad.Academica')
	for col in programas.columns:
		lista_filtro.append(col)
	ruta_homologado = os.path.normpath(os.path.join(ruta_global,"archivos_homologados"))
	ruta_sub = os.path.normpath(os.path.join(os.path.join(ruta_global,"subtotales"),"sub_totales_rama")) 
	for nombre_archivo in os.listdir(ruta_homologado):
		try:
			if nombre_archivo.endswith('xlsx'):
				ruta_archivo = os.path.normpath(os.path.join(ruta_homologado,nombre_archivo))
				dataframe = pd.read_excel(ruta_archivo)
				columnas_importantes = [col for col in dataframe.columns if col not in lista_filtro]
				dataframe = dataframe.groupby(columnas_importantes, as_index=False)['Datos'].sum()
				write_root = os.path.normpath(os.path.join(ruta_sub,nombre_archivo))
				dataframe.to_excel(write_root, index=False)
		except:
			logger.error(nombre_archivo)

def sub_totales_total(ruta_global, ruta_unidades, ruta_programas):
	programas = pd.read_excel(ruta_programas)
	unidades = pd.read_excel(ruta_unidades)
	lista_filtro = [col for col in unidades.columns]
	lista_filtro.append('Programa')
	lista_filtro.append('Datos')
	lista_filtro.append('Unidad.Academica')
	for col in programas.columns:
		lista_filtro.append(col)
	ruta_homologado = os.path.normpath(os.path.join(ruta_global,"archivos_homologados"))
	ruta_sub = os.path.normpath(os.path.join(os.path.join(ruta_global,"subtotales"),"totales"))
	for nombre_archivo in os.listdir(ruta_homologado):
		try:
			if nombre_archivo.endswith('xlsx'):
				ruta_archivo = os.path.normpath(os.path.join(ruta_homologado,nombre_archivo))
				dataframe = pd.read_excel(ruta_archivo)
				columnas_importantes = [col for col in dataframe.columns if col not in lista_filtro]
				dataframe = dataframe.groupby(columnas_importantes, as_index=False)['Datos'].sum()
				write_root = os.path.normpath(os.path.join(ruta_sub,nombre_archivo))
				dataframe.to_excel(write_root, index=False)
		except:
			logger.error(nombre_archivo)

def procesar_subtotales(ruta_global):
    ruta_catalogos = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    ruta_programas = os.path.normpath(os.path.join(ruta_catalogos,"programas.xlsx"))
    ruta_unidades = os.path.normpath(os.path.join(ruta_catalogos,"unidades_academicas.xlsx"))
    ruta_subtotales = os.path.normpath(os.path.join(ruta_global,"subtotales"))
    ruta_errores = os.path.normpath(os.path.join(ruta_global,"errores"))
    carpetas=["sub_totales_unidad","sub_totales_rama","totales"]
    eliminar_xlsx_vacios(ruta_subtotales)
    homologar_subtotales(ruta_subtotales,ruta_unidades)
    crear_subdirectorios(ruta_subtotales, carpetas)
    sub_totales_unidad(ruta_global, ruta_unidades, ruta_programas)
    sub_totales_rama(ruta_global, ruta_unidades, ruta_programas)
    sub_totales_total(ruta_global, ruta_unidades, ruta_programas)

