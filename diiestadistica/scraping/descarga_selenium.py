# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10  2025

@author: Luis Alberto Ortega Ramirez
Nombre del archivo: descargar_selenium.py

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
from diiestadistica.scraping.seleccionar_opcion import seleccionar_opcion, seleccionar_opcion_combo_descarga
from diiestadistica.scraping.seleccionar_opcion import seleccionar_opcion_egresados
from diiestadistica.scraping.seleccionar_opcion import seleccionar_opcion_combo
from diiestadistica.scraping.credenciales import credenciales

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from typing import Optional 


import time
import pandas as pd
import os

from diiestadistica.core.logging_config import setup_logger

logger = setup_logger(__name__)

def descarga_selenium(
        año_inicio: int = 2023,
        semestre:int  = 2,
        download_path: Optional[str] = None) -> Optional[webdriver.Chrome]:
    #"""
    # Configurar las opciones de Chrome
    if not download_path:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    logger.info(f"Archivos se descargarán en: {download_path}")
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    #"""

    # Crear lista de conceptos que se van a descargar
    conceptos = ['Aprovechamiento Escolar por Sexo',
                'Egresados',
                'Matrícula Inscrita Medio Superior',
                'Matrícula Inscrita Nivel Superior',
                'Matrícula Inscrita Nivel Posgrado',
                'Matrícula Inscrita Por Grupos De Edad',
                'Titulación']
    #driver = webdriver.Chrome()
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

    df = df[df['text'].isin(conceptos)]

    ciclo_incio = str(año_inicio) + " - " + str((año_inicio+1))
    semestre_inicio = "/" + str(semestre) 

    if semestre == 2:
        ciclo_fin = ciclo_incio
        semestre_fin = "/1"
    elif semestre == 1:
        ciclo_fin = str((año_inicio - 1)) + " - " + str((año_inicio))
        semestre_fin = "/2"
    else:
        logger.warning("Selección de periodo fuera de rango") 



    for index, row in df.iterrows():
        pagina = f"{row['href']}"
        text = f"{row['text']}"
        driver.get(pagina)
        time.sleep(2)
        if text == "Aprovechamiento Escolar por Sexo":
            seleccionar_opcion(driver, "Ciclo Escolar:", ciclo_fin)
            time.sleep(2)
            seleccionar_opcion(driver, "Periodo:", semestre_fin)
            time.sleep(2)
            descarga = ["concentrado"]
            seleccionar_opcion_combo_descarga(driver, "Nivel:", descarga)
            time.sleep(1)
        elif text == "Egresados":
            seleccionar_opcion(driver, "Ciclo Escolar:", ciclo_fin)
            time.sleep(2)
            seleccionar_opcion(driver, "Periodo:", semestre_fin)
            time.sleep(2)
            seleccionar_opcion_egresados(driver,"Nivel:")
            time.sleep(1)
        elif text == "Titulación":
            seleccionar_opcion(driver, "Ciclo Escolar:", ciclo_fin)
            time.sleep(2)
            seleccionar_opcion(driver, "Periodo:", semestre_fin)
            time.sleep(2)
            descarga = ["concentrado"]
            seleccionar_opcion_combo_descarga(driver, "Nivel:", descarga)
            time.sleep(1)
        elif text=="Matrícula Inscrita Medio Superior":
            seleccionar_opcion(driver, "Ciclo Escolar:", ciclo_incio)
            time.sleep(2)
            seleccionar_opcion(driver, "Periodo:", semestre_inicio)
            time.sleep(2)
            descarga = ["concentradoMatriculaInscrita","concentradoPASemestreSexo","concentradoTurno"]
            seleccionar_opcion_combo_descarga(driver, "Nivel:", descarga)
        elif text=="Matrícula Inscrita Nivel Superior":
            seleccionar_opcion(driver, "Ciclo Escolar:", ciclo_incio)
            time.sleep(2)
            seleccionar_opcion(driver, "Periodo:", semestre_inicio)
            time.sleep(2)
            descarga = ["concentradoMatriculaEducativa","concentradoPASemestreSexo","concentradoTurno"]
            seleccionar_opcion_combo_descarga(driver, "Nivel:", descarga)
        elif text=="Matrícula Inscrita Nivel Posgrado":
            seleccionar_opcion(driver, "Ciclo Escolar:", ciclo_incio)
            time.sleep(2)
            seleccionar_opcion(driver, "Periodo:", semestre_inicio)
            time.sleep(2)
            descarga = ["concentradoMatriculaSuperior","concentrado2","concentradoTurno"]
            seleccionar_opcion_combo_descarga(driver, "Nivel:", descarga)
        elif text=="Matrícula Inscrita Por Grupos De Edad":
            seleccionar_opcion(driver, "Ciclo Escolar:", ciclo_incio)
            time.sleep(3)
            seleccionar_opcion(driver, "Periodo:", semestre_inicio)
            time.sleep(3)
            seleccionar_opcion_combo(driver, "Nivel:")
            time.sleep(3)
            logger.info("ok")
        else:
            logger.info("error concepto fuera de rango")
        
    # Cierra el navegador
    time.sleep(140)
    driver.quit()

#_________________________T O D O ____ B I E N______A R R I B A_____________

if __name__ == "__main__":
    from diiestadistica.gui.seleccion_archivos import seleccionar_carpeta
    download_path = seleccionar_carpeta()
    if download_path is not None:
        descarga_selenium(download_path=download_path)
    else:
        descarga_selenium()