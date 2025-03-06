


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def ingresar_credenciales(driver,d_usuario,d_contraseña):
    if(d_usuario!=None and d_contraseña!=None):
        try:
            print("hay credenciales")
        except:
            print("Se produjo un error")    
    else:
        try:
            # Abre la página de inicio de sesión
            driver.get("https://intranet.sge.ipn.mx/")

            # Espera a que la página cargue
            time.sleep(2)

            # Ingresa las credenciales
            usuario = driver.find_element(By.NAME, "j_username")
            usuario.send_keys("cglara")

            contraseña = driver.find_element(By.NAME, "j_password")
            contraseña.send_keys("ZyK8nEEA")

            # Envía el formulario
            contraseña.send_keys(Keys.RETURN)

            # Espera a que la página cargue después del inicio de sesión
            time.sleep(2)

            # Navega a la página deseada
            pagina_deseada = "https://intranet.sge.ipn.mx/principal.cfm"
            driver.get(pagina_deseada)

            # Espera a que el contenido dinámico se cargue
            time.sleep(2)
        
        except:
            print("Se produjo un Error")
        
