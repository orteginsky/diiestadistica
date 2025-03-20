from .validacion_html import procesar_tabla_html
from .validacion_html import limpiar_html
from .validacion_html import procesar_tabla_html_recursive, procesar_tabla_html
from .validacion_html import validar_rectangulo, uno
from .seleccionar_carpeta import seleccionar_carpeta
from .depurar import expandir_tabla
from .depurar import definir_encabezados
from .depurar import eliminar_columnas_subtotales
from .depurar import reorganizar_datos

from bs4 import BeautifulSoup
import os
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
			#with open('C:/Users/Usuario/Downloads/output.txt', 'w', encoding='latin-1') as file:
			#	file.write(datos_html.prettify())
			datos_matriz = procesar_tabla_html(soup=datos_html)
			datos_exp = expandir_tabla(datos_matriz)
            # Cambiar los colnames
			datos_exp.columns = definir_encabezados(encabezados_df)
            # Eliminar subtotales
			datos_exp = eliminar_columnas_subtotales(datos_exp)
            # pivotear datos
			#datos_exp = reorganizar_datos(datos_exp)

			"""
			for i in range(int(len(datos_matriz)/7)):
				print("\n")
				for j in datos_matriz[i]:
					print(j)
			"""

			"""
			k=len(datos_matriz)
			vk=0

			for sum in datos_matriz[0]:
				vk+=sum[1]
			rectangulo = True
			j=1
			while(rectangulo and (j<k-1)):
				suma=0
				sum1=0
				sum2=0
				for i in range(len(datos_matriz[j])):
					if isinstance(datos_matriz[j][i][1], int):
						sum1 += datos_matriz[j][i][1]
				for a in range(j):
					for i in range(len(datos_matriz[a])):
						if isinstance(datos_matriz[a][i][0],int) and isinstance(datos_matriz[a][i][1],int): 
							sum2 += uno(datos_matriz[a][i][0]+a-j)*datos_matriz[a][i][1]
				suma = sum1 + sum2
				print(suma)
				j +=1
            """


		except:
			print(i)
			print(nombre_archivo)



			
            
            
            
            # Extraer matriz de matrices de datos
            


            


			

"""
            
            for i in range(int(len(datos_matriz)/7)):
                print("\n")
                for j in datos_matriz[i]:
                    print(j)
            
            lista=[]            
            for fila in datos_matriz:
                sum=0
                for c in fila:
                    sum += c[1]
                lista.append(sum)
            columnas= max(lista)
            filas=len(datos_matriz)
            print(filas)
            print(columnas)
"""