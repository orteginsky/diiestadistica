from .validacion_html import procesar_tabla_html
from .validacion_html import limpiar_html
from .validacion_html import procesar_tabla_html
from .seleccionar_carpeta import seleccionar_carpeta
from .depurar import expandir_tabla
from .depurar import eliminar_columnas_subtotales
from .depurar import reorganizar_datos
from .creacion_tabla import definir_encabezados

from bs4 import BeautifulSoup
import os
import re
if __name__ == "__main__":
	ruta_carpeta = seleccionar_carpeta()
	for i in range(19):
		nombre_archivo = os.listdir(ruta_carpeta)[i]
		try:
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
			"""
			for i in range(int(len(datos_matriz)/200)):
				print("\n")
				for j in datos_matriz[i]:
					print(j)"
			"""
			datos_exp = expandir_tabla(datos_matriz)
			datos_exp.columns = definir_encabezados(encabezados_df)
			datos_exp = reorganizar_datos(datos_exp)
			nombre_archivo_guardar = re.sub('.xls','',nombre_archivo)
			ruta_guardar = f"C:/Users/Usuario/Desktop/diiestadistica/excel/{nombre_archivo_guardar}.xlsx"
			#print(nombre_archivo)
			#print(datos_exp.head())
			datos_exp.to_excel(ruta_guardar, index=False)
		except:
			print(i)
			print(nombre_archivo)
