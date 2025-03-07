# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10  2025

@author: Luis Alberto Ortega Ramirez
Nombre del archivo: intranet_selenium.py

Contexto: 
    
Objetivo: Automatizar el proceso de estadística básica con la finalidad de reducir el tiempo
de espera, mantener la integridad de la información y detectar errores mediante el uso de 
otros scripts en R.
    
Estructura del Código:

Entradas:
    - Claves de acceso
    
Salidas:
    - lista de archivos de la estadistica básica descargados de intranet

Ejemplos de Uso:
    - Extraer la información del periodo correspondiente

Consideraciones Especiales:    

Dependencias:
- Selenium

Notas:
    
- Verificar las rutas de los archivos antes de ejecutar el código.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

from .seleccionar_opcion import seleccionar_opcion
from .seleccionar_opcion import seleccionar_opcion_nivel
from .seleccionar_opcion import seleccionar_opcion_combo
from .descargar_reportes import descargar_reportes
from .descargar_reportes import descargar_reportes_nivel
from .credenciales import credenciales

# Configura el navegador
driver = webdriver.Chrome()

# Ingresa a la página correspondiente e ingresa las credenciales
driver = credenciales(driver)

# Buscar todos los enlaces dentro del div con id "menuAux"
menu_aux = driver.find_element(By.ID, "menuAux")
links = menu_aux.find_elements(By.XPATH, ".//ul//li//a")

# Extraer href y texto del span
data = []
for link in links:
    href = link.get_attribute("href")
    span_text = link.get_attribute("text")
    data.append({"href": href, "text": span_text})

# Crear DataFrame
df = pd.DataFrame(data)

# Crear lista de conceptos
conceptos = ['Aprovechamiento Escolar',
             'Egresados',
             'Matrícula Inscrita Medio Superior',
             'Matrícula Inscrita Nivel Superior',
             'Matrícula Inscrita Nivel Posgrado',
             'Matrícula Inscrita Por Grupos De Edad',
             'Titulación']

df = df[df['text'].isin(conceptos)]


for index, row in df.iterrows():
    pagina = f"{row['href']}"
    text = f"{row['text']}"
    driver.get(pagina)
    time.sleep(2)
    if text == "Aprovechamiento Escolar" or text == "Egresados" or text == "Titulación":
        seleccionar_opcion(driver, "Ciclo Escolar:", 2)
        time.sleep(2)
        seleccionar_opcion(driver, "Periodo:", 1)
        time.sleep(2)
        seleccionar_opcion_combo(driver, "Nivel:")
        time.sleep(1)
    else:
        seleccionar_opcion(driver, "Ciclo Escolar:", 1)
        time.sleep(2)
        seleccionar_opcion(driver, "Periodo:", 1)
        time.sleep(2)
        if text != "Matrícula Inscrita Por Grupos De Edad":
            if text=="Matrícula Inscrita Medio Superior":
                descarga = ["concentradoMatriculaInscrita","concentradoMatInsSemestreGrupos_NMS","concentradoPASemestreSexo","concentradoTurno"]
            elif text=="Matrícula Inscrita Nivel Superior":
                descarga = ["concentradoMatriculaEducativa","concentradoPASemestreSexo","concentradoGruposPorSemestre","concentradoTurno"]
            elif text=="Matrícula Inscrita Nivel Posgrado":
                descarga = ["concentrado","concentradoMatriculaSuperior","concentrado2","concentradoTurno"]
            else:
                descarga = []    
            seleccionar_opcion_nivel(driver,"Nivel:",1)
            time.sleep(3)
            descargar_reportes_nivel(driver,descarga)
        else:
            seleccionar_opcion_combo(driver, "Nivel:")
            time.sleep(1)


# Cierra el navegador
driver.quit()