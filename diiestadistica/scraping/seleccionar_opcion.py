
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from .descargar_reportes import descargar_reportes, descargar_reportes_nivel, primer_reporte

niveles=["MEDIO SUPERIOR","SUPERIOR","POSGRADO"]
########################################################################################
def seleccionar_opcion(driver, palabra, concepto):
    """
    Función para seleccionar una opción de un combo box en base a una palabra clave.
    
    :param driver: WebDriver de Selenium
    :param palabra: Texto dentro del <td> que identifica el combo box (ej. "Periodo:")
    :param numero: Índice desde el final de la lista de opciones (1 para la última, 2 para la penúltima, etc.)
    """
    try:
        # Encuentra el <td> que contiene la palabra clave
        xpath_td = f"//td[@class='backgroundtableForm' and strong[text()='{palabra}']]"
        td_element = driver.find_element(By.XPATH, xpath_td)

        # Selecciona el <div> dentro del mismo tr
        div_combo = td_element.find_element(By.XPATH, "./following-sibling::td//div[@class='dhx_combo_box']")
        
        # Haz clic en el <div> para desplegar las opciones
        div_combo.click()
        time.sleep(1)

        # Encuentra las opciones disponibles
        opciones = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'dhx_combo_list')]/div"))
        )

        # Filtra las opciones eliminando elementos vacíos
        opciones_validas = [opcion for opcion in opciones if opcion.text.strip()]

        for i in opciones_validas:
            if concepto in i.text.strip():
                i.click()
    except Exception as e:
        print(f"Error al seleccionar la opción: {e}")

########################################################################################
def seleccionar_opcion_nivel(driver, palabra, numero=1):
    """
    Función para seleccionar una opción de un combo box en base a una palabra clave.
    
    :param driver: WebDriver de Selenium
    :param palabra: Texto dentro del <td> que identifica el combo box (ej. "Nivel:")
    :param numero: Índice desde el final de la lista de opciones (1 para la última, 2 para la penúltima, etc.)
    """
    try:
        # Encuentra el <td> que contiene la palabra clave
        xpath_td = f"//td[@class='backgroundtableForm' and text()='{palabra}']"
        td_element = driver.find_element(By.XPATH, xpath_td)

        # Selecciona el <div> dentro del mismo tr
        div_combo = td_element.find_element(By.XPATH, "./following-sibling::td//div[@class='dhx_combo_box']")
        
        # Haz clic en el <div> para desplegar las opciones
        div_combo.click()
        time.sleep(1)

        # Encuentra las opciones disponibles
        opciones = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'dhx_combo_list')]/div"))
        )

        # Filtra las opciones eliminando elementos vacíos
        opciones_validas = [opcion for opcion in opciones if opcion.text.strip()]

        if opciones_validas and numero <= len(opciones_validas):
            opciones_validas[-numero].click()
        else:
            print("No hay opciones válidas o el número es demasiado grande")

    except Exception as e:
        print(f"Error al seleccionar la opción: {e}")

########################################################################################
def seleccionar_opcion_combo(driver, palabra):
    """
    Encuentra y selecciona una opción en un combo box basado en un <td> que contiene una palabra clave.

    :param driver: WebDriver de Selenium
    :param palabra: Texto dentro del <td> que identifica el combo box
    """
    try:
        # Encuentra el <td> que contiene la palabra clave
        xpath_td = f"//td[@class='backgroundtableForm' and text()='{palabra}']"
        td_elemento = driver.find_element(By.XPATH, xpath_td)

        # Selecciona el <div> dentro del mismo <tr> que contiene el combo box
        div_combo = td_elemento.find_element(By.XPATH, "./following-sibling::td//div[@class='dhx_combo_box']")

        # Haz clic en el combo box para desplegar las opciones
        div_combo.click()

        # Espera hasta que aparezcan las opciones del combo
        opciones = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'dhx_combo_list')]/div"))
        )

        # Encuentra la primera opción válida y haz clic
        for opcion in opciones:
            if opcion.text.strip():
                if opcion.text.strip() in niveles:
                    opcion.click()
                    print(f"Seleccionada la opción: {opcion.text.strip()}")
                    descargar_reportes(driver)
                    time.sleep(4)
                    div_combo.click()

    except Exception as e:
        print(f"Error al seleccionar el combo box con la palabra '{palabra}': {e}")


########################################################################################

def seleccionar_opcion_combo_descarga(driver, palabra, descarga):
    """
    Encuentra y selecciona una opción en un combo box basado en un <td> que contiene una palabra clave.

    :param driver: WebDriver de Selenium
    :param palabra: Texto dentro del <td> que identifica el combo box
    """
    try:
        # Encuentra el <td> que contiene la palabra clave
        xpath_td = f"//td[@class='backgroundtableForm' and text()='{palabra}']"
        td_elemento = driver.find_element(By.XPATH, xpath_td)

        # Selecciona el <div> dentro del mismo <tr> que contiene el combo box
        div_combo = td_elemento.find_element(By.XPATH, "./following-sibling::td//div[@class='dhx_combo_box']")

        # Haz clic en el combo box para desplegar las opciones
        div_combo.click()

        # Espera hasta que aparezcan las opciones del combo
        opciones = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'dhx_combo_list')]/div"))
        )

        # Encuentra la primera opción válida y haz clic
        for opcion in opciones:
            if opcion.text.strip():
                if opcion.text.strip() in niveles:
                    opcion.click()
                    print(f"Seleccionada la opción: {opcion.text.strip()}")
                    descargar_reportes_nivel(driver, descarga)
                    time.sleep(4)
                    div_combo.click()

    except Exception as e:
        print(f"Error al seleccionar el combo box con la palabra '{palabra}': {e}")

########################################################################################
def seleccionar_opcion_egresados(driver, palabra):
    """
    Encuentra y selecciona una opción en un combo box basado en un <td> que contiene una palabra clave.

    :param driver: WebDriver de Selenium
    :param palabra: Texto dentro del <td> que identifica el combo box
    """
    try:
        # Encuentra el <td> que contiene la palabra clave
        xpath_td = f"//td[@class='backgroundtableForm' and text()='{palabra}']"
        td_elemento = driver.find_element(By.XPATH, xpath_td)

        # Selecciona el <div> dentro del mismo <tr> que contiene el combo box
        div_combo = td_elemento.find_element(By.XPATH, "./following-sibling::td//div[@class='dhx_combo_box']")

        # Haz clic en el combo box para desplegar las opciones
        div_combo.click()

        # Espera hasta que aparezcan las opciones del combo
        opciones = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'dhx_combo_list')]/div"))
        )

        for opcion in opciones:
            if opcion.text.strip():
                if opcion.text.strip() == "POSGRADO":
                    opcion.click()
                    descargar_reportes(driver)
                    time.sleep(4)
                else:
                    opcion.click()
                    primer_reporte(driver)
                    time.sleep(4)
                div_combo.click()

    except Exception as e:
        print(f"Error al seleccionar el combo box con la palabra '{palabra}': {e}")
