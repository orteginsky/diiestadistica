from ..utils.archivo_utils import eliminar_xlsx_vacios
from ..utils.archivo_utils import crear_subdirectorios

import pandas as pd
import os

def homologar_subtotales(ruta_subtotales,ruta_unidades):
	unidades = pd.read_excel(ruta_unidades)
	for nombre_archivo in os.listdir(ruta_subtotales):
		try:
			if nombre_archivo.endswith("xlsx"):
				ruta_archivo = f"{ruta_subtotales}/{nombre_archivo}"
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
					print("Sin columnas a homologar")
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
			print(nombre_archivo)

def sub_totales_unidad(ruta_global):
    ruta_homologado = f"{ruta_global}/archivos_homologados"
    ruta_subtotales = f"{ruta_global}/subtotales"
    for nombre_archivo in os.listdir(ruta_homologado):
        try:
            if nombre_archivo.endswith('xlsx'):
                dataframe = pd.read_excel(ruta_subtotales)
                columnas_importantes = [col for col in dataframe.columns if col not in ['Unidad.Academica','Programa']]
                dataframe.groupby(columnas_importantes, as_index=False)['Datos'].sum()
                print("se esta generando el subtotal de las ramas")
        except:
            print(nombre_archivo)
def sub_totales_rama(ruta_global):
    ruta_homologado = f"{ruta_global}/archivos_homologados"
    ruta_subtotales = f"{ruta_global}/subtotales"
    print("se esta generando el subtotal de las ramas")

def sub_totales_total(ruta_global):
    ruta_homologado = f"{ruta_global}/archivos_homologados"
    ruta_subtotales = f"{ruta_global}/subtotales"
    print("se esta generando el subtotal de las ramas")

def procesar_subtotales(ruta_global):
    ruta_catalogos = "/media/sf_Y_DRIVE/Homologacion/Catalogos Programas/"
    ruta_programas = f"{ruta_catalogos}/programas.xlsx"
    ruta_unidades = f"{ruta_catalogos}/unidades_academicas.xlsx"
    ruta_subtotales = f"{ruta_global}/subtotales"
    ruta_errores = f"{ruta_global}/errores"
    carpetas=["sub_totales_unidad","sub_totales_rama","totales"]
    eliminar_xlsx_vacios(ruta_subtotales)
    homologar_subtotales(ruta_subtotales,ruta_programas,ruta_unidades)
    #crear_subdirectorios(ruta_subtotales, carpetas)
    #sub_totales_unidad(ruta_global)
    #sub_totales_rama(ruta_global)
    #sub_totales_total(ruta_global)

