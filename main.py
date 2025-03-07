from diiestadistica.pruebas.hola_mundo import hola_mundo
from selenium import webdriver

if __name__ == "__main__":
    # Configura el navegador
    driver = webdriver.Chrome()
    hola_mundo()