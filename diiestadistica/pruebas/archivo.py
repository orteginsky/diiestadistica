from bs4 import BeautifulSoup
import os

ruta = 'C:/Users/Usuario/Desktop/diiestadistica/archivos/Formato 2/Concentrado_Poblacion_Atendida__Matricula_Inscrita_ProgramaAcademico_Semestre_Sexo.html'
with open(ruta, "r", encoding='utf-8') as file:
    soup = BeautifulSoup(file, "html.parser")

soup = soup.prettify()


with open(ruta, "w", encoding='utf-8') as file:
    file.write(soup)
