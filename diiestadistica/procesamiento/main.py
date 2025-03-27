from .validacion_html import procesar_tabla_html
from .validacion_html import limpiar_html
from .validacion_html import procesar_tabla_html
from .seleccionar_carpeta import seleccionar_carpeta
from .depurar import expandir_tabla
from .depurar import eliminar_columnas_subtotales
from .depurar import reorganizar_datos
from .depurar import generar_columnas
from .depurar import coincidencia
from .creacion_tabla import definir_encabezados
from .validacion_datos import dividir_subtotales

from bs4 import BeautifulSoup
import os
import re


def procesamiento_aplanamiento(ruta_carpeta,ciclo,periodo):
	ruta_periodo = f"{ruta_carpeta}/periodo_{ciclo}_{periodo}"
	ruta_xml = f"{ruta_periodo}/archivos_originales"
	ruta_aplanada = f"{ruta_periodo}/archivos_originales"

	for nombre_archivo in os.listdir(ruta_xml):
		try:
			if nombre_archivo.endswith("xls"):
				ruta_archivo = f"{ruta_carpeta}/{nombre_archivo}"
				with open(ruta_archivo, "r", encoding="latin-1") as archivo_html:
					soup = BeautifulSoup(archivo_html, "html.parser")
				soup_encabezados = soup.find("thead")
				encabezados_matriz = procesar_tabla_html(soup_encabezados)
				encabezados_df = expandir_tabla(encabezados_matriz)
				nombres_encabezados = definir_encabezados(encabezados_df)
				datos_html = soup.find("tbody").find("tbody")
				if datos_html:
					print("ok")
				else:
					datos_html = soup.find("tbody")
				datos_html = limpiar_html(datos_html)
				datos_matriz = procesar_tabla_html(soup=datos_html)
				datos_exp = expandir_tabla(datos_matriz)
				datos_exp.columns = definir_encabezados(encabezados_df)
				if re.search('Egresados',nombre_archivo):
					datos_exp = reorganizar_datos(datos_exp)
					datos_exp.rename(columns={'col_2':'Sexo'}, inplace= True)
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
									coincidencia('NP_Basica',nombre_archivo) or \
										coincidencia('NS_Grupos',nombre_archivo) :
					datos_exp.rename(columns={'col_1':'Concepto','col_2':'Sexo'}, inplace= True)
				elif coincidencia('Semestre',nombre_archivo) or \
					coincidencia('NMS_Basica',nombre_archivo) or \
						coincidencia('NS_Basica',nombre_archivo) or \
							coincidencia('NMS_Grupos',nombre_archivo) or \
								coincidencia('NP_Grupos',nombre_archivo):
					datos_exp.rename(columns={'col_2':'Concepto','col_3':'Sexo'}, inplace= True)
				elif coincidencia('NP_Titulados',nombre_archivo):
					datos_exp.rename(columns={'col_2':'Sexo'}, inplace= True)

				datos_exp.rename(columns=lambda col: 'Unidad.Academica' if coincidencia('Dependencia', col) else col, inplace=True)
				datos_exp, subtotales = dividir_subtotales(datos_exp)

				ruta_guardar = f"C:/Users/Usuario/Desktop/diiestadistica/excel/{nombre_archivo_guardar}.xlsx"
				datos_exp.to_excel(ruta_guardar, index=False)
				ruta_guardar = f"C:/Users/Usuario/Desktop/diiestadistica/subtotales/{nombre_archivo_guardar}.xlsx"
				subtotales.to_excel(ruta_guardar, index=False)
		except:
			print(nombre_archivo)
