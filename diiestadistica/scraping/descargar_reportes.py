
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def descargar_reportes_nivel(driver, descarga):
    """
    Función para hacer clic en las imágenes de Excel dentro de los divs con IDs específicos.

    :param driver: WebDriver de Selenium
    :param descarga: Lista de IDs de los reportes a descargar
    """
    try:
        for i in descarga:
            # Encuentra el div por su ID
            xpath_div = f"//div[@id='{i}']"
            reporte_elemento = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath_div))
            )

            # Dentro de ese div, busca la imagen de Excel
            excel_img = reporte_elemento.find_element(By.XPATH, ".//img[@src='/images/excel.png']")  

            # Hace clic en la imagen
            excel_img.click()
            print(f"Descargando reporte: {i}")

            # Espera un poco antes de continuar con el siguiente
            time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")


def descargar_reportes(driver):
    """
    Hace clic en todas las imágenes <img src='/images/excel.png'> que estén visibles en la página.

    :param driver: WebDriver de Selenium
    """
    try:
        # Encuentra todas las imágenes con src="/images/excel.png"
        imagenes = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//img[@src='/images/excel.png']"))
        )

        # Filtra solo las imágenes visibles
        imagenes_visibles = [img for img in imagenes if img.is_displayed()]

        if not imagenes_visibles:
            print("No hay exceles visibles para descargar.")
            return

        for img in imagenes_visibles:
            img.click()
            print("Clic en una imagen de Excel")
            time.sleep(2)  # Pequeña espera entre clics

    except Exception as e:
        print(f"Error al hacer al hacer click en descarga: {e}")


