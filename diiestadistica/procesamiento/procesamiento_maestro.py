#Funciones extra-externas
from ..utils.coincidencia import coincidencia
from ..utils.os_utils import extraer_periodo
#funciones externas
from .html_procesamiento import procesar_tabla_html
from .html_procesamiento import limpiar_html
from .transformaciones import expandir_tabla
from .transformaciones import definir_encabezados
from .transformaciones import eliminar_columnas_subtotales
from .transformaciones import reorganizar_datos
from .transformaciones import generar_columnas
from .transformaciones import dividir_subtotales
from .limpieza import limpiar_nombres_programas

#funciones particulares
from bs4 import BeautifulSoup
#librerias
import pandas as pd
import os
import re

from diiestadistica.core.logging_config import setup_logger

logger = setup_logger(__name__)


def procesamiento_aplanamiento(ruta_periodo):
	ruta_xml = os.path.normpath(os.path.join(ruta_periodo,"archivos_originales"))
	logger.info(ruta_xml)
	ruta_aplanada = os.path.normpath(os.path.join(ruta_periodo,"archivos_aplanados"))
	ruta_subtotales = os.path.normpath(os.path.join(ruta_periodo,"subtotales"))
	periodo = extraer_periodo(ruta_periodo)
	if periodo is not None:
		periodo = re.sub("_", "/", str(periodo))
	else:
		periodo = ""
	for nombre_archivo in os.listdir(ruta_xml):
		try:
			if nombre_archivo.endswith("xls"):
				ruta_archivo = os.path.normpath(os.path.join(ruta_xml,nombre_archivo))
				with open(ruta_archivo, "r", encoding="latin-1") as archivo_html:
					soup = BeautifulSoup(archivo_html, "html.parser")
				soup_encabezados = soup.find("thead")
				encabezados_matriz = procesar_tabla_html(soup_encabezados)
				encabezados_df = expandir_tabla(encabezados_matriz)
				datos_html = soup.find("tbody").find("tbody")
				if datos_html:
					logger.info("Tabla dentro de otro tabla")
				else:
					datos_html = soup.find("tbody")
				
				datos_html = limpiar_html(datos_html)
				datos_matriz = procesar_tabla_html(soup=datos_html)
				datos_exp = expandir_tabla(datos_matriz)
				datos_exp.columns = definir_encabezados(encabezados_df)
				
				if re.search('Egresados',nombre_archivo):
					if re.search('NMS',nombre_archivo):
						datos_exp = eliminar_columnas_subtotales(datos_exp)
						datos_exp = reorganizar_datos(datos_exp)
						datos_exp.rename(columns={'col_1':'Fin_periodo','col_2':'Sexo','col_3':'Turno'}, inplace= True)
					else:
						datos_exp = eliminar_columnas_subtotales(datos_exp)
						datos_exp = reorganizar_datos(datos_exp)
						datos_exp.rename(columns={'col_1':'Fin_periodo','col_2':'Sexo'}, inplace= True)
				else:
					datos_exp = eliminar_columnas_subtotales(datos_exp)
					datos_exp = reorganizar_datos(datos_exp)
				
				datos_exp = datos_exp.loc[:,datos_exp.nunique()>1]
				nombre_archivo_guardar = re.sub('.xls','',nombre_archivo)
				columnas = ("Nivel","Indice")
				datos_exp = generar_columnas(descripcion=nombre_archivo_guardar, columnas=columnas, dataframe=datos_exp)
				datos_exp = eliminar_columnas_subtotales(datos_exp)

				if coincidencia('Turno',nombre_archivo) or \
					  coincidencia('NMS_Titulados',nombre_archivo) or \
						  coincidencia('NS_Titulados',nombre_archivo) or \
							coincidencia('NMS_Aprovechamiento',nombre_archivo) or \
								coincidencia('NS_Aprovechamiento',nombre_archivo) or \
									coincidencia('NP_Basica',nombre_archivo):
					datos_exp.rename(columns={'col_1':'Concepto','col_2':'Sexo'}, inplace= True)
				elif coincidencia('Semestre',nombre_archivo) or \
					coincidencia('NMS_Basica',nombre_archivo) or \
						coincidencia('NS_Basica',nombre_archivo) or \
							coincidencia('NMS_Grupos',nombre_archivo) or \
								coincidencia('NP_Grupos',nombre_archivo) or \
									coincidencia('NS_Grupos',nombre_archivo):
					datos_exp.rename(columns={'col_2':'Concepto','col_3':'Sexo'}, inplace= True)
				elif coincidencia('NP_Titulados',nombre_archivo):
					datos_exp.rename(columns={'col_1':'Periodo','col_2':'Sexo'}, inplace= True)

				datos_exp.rename(columns=lambda col: 'Unidad.Academica' if coincidencia('Dependencia', col) else col, inplace=True)
				datos_exp.rename(columns=lambda col: 'Programa' if coincidencia('Programa', col) else col, inplace=True)
				datos_exp['Periodo'] = periodo
				datos_exp, subtotales = dividir_subtotales(datos_exp)

				ruta_guardar = os.path.normpath(os.path.join(ruta_aplanada,f"{nombre_archivo_guardar}.xlsx"))
				datos_exp.to_excel(ruta_guardar, index=False)
				ruta_guardar_subtotales = os.path.normpath(os.path.join(ruta_subtotales,f"{nombre_archivo_guardar}.xlsx"))
				subtotales.to_excel(ruta_guardar_subtotales, index=False)
				
		except Exception as e:
			logger.info(F"error en el archivo:{nombre_archivo} error:{e}")

def procesamiento_limpieza(ruta_periodo):
	ruta_aplanada = os.path.normpath(os.path.join(ruta_periodo,"archivos_aplanados"))
	ruta_homo = os.path.normpath(os.path.join(ruta_periodo,"archivos_homologados"))
	ruta_catalogos = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
	ruta_programas = os.path.normpath(os.path.join(ruta_catalogos,"programas.xlsx"))
	ruta_unidades = os.path.normpath(os.path.join(ruta_catalogos,"unidades_academicas.xlsx"))
	logger.info(ruta_catalogos)
	logger.info(ruta_programas)
	logger.info(ruta_unidades)
	programas = pd.read_excel(ruta_programas)
	unidades = pd.read_excel(ruta_unidades)
	for nombre_archivo in os.listdir(ruta_aplanada):
		try:
			if nombre_archivo.endswith("xlsx"):
				nombre_archivo_guardar = re.sub('.xlsx','',nombre_archivo)
				ruta_archivo = os.path.normpath(os.path.join(ruta_aplanada,nombre_archivo))
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
					logger.info("valio")
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
				
				dataframe = limpiar_nombres_programas(dataframe, 'Programa')

				duplicados = dataframe[dataframe["Programa"].isin(["Tronco Común", "Propedéutico"])]
				duplicados = duplicados.merge(unidades, left_on="Unidad.Academica", right_on="nombre_intranet", how="left")
				duplicados = duplicados.merge(programas, left_on=["Programa",'Rama_unidad'], right_on=['programa_intranet','Rama'], how="left")

				unicos = dataframe[~dataframe["Programa"].isin(["Tronco Común", "Propedéutico"])]
				unicos = unicos.merge(unidades, left_on="Unidad.Academica", right_on="nombre_intranet", how="left")
				unicos = unicos.merge(programas, left_on="Programa", right_on="programa_intranet", how="left")

				dataframe_final = pd.concat([duplicados, unicos], ignore_index=True)

				ruta_homo_guardar = os.path.normpath(os.path.join(ruta_homo,f"{nombre_archivo_guardar}.xlsx"))
				dataframe_final.to_excel(ruta_homo_guardar, index=False)
		except Exception as e:
			logger.info(f"error en el archivo:{nombre_archivo} error:{e}")



"""
				filtro = []
				if ("nombre_intranet" not in unidades.columns) and ("Rama_intranet" not in unidades.columns):
					filtro.append(True)
				else:
					filtro.append(False)
"""