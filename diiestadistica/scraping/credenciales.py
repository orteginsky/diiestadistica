from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def credenciales(driver,d_usuario="cglara",d_contraseña="ZyK8nEEA"):

    try:
        
        # Abre la página de inicio de sesión
        driver.get("https://intranet.sge.ipn.mx/")

        # Espera a que la página cargue
        time.sleep(2)

        # Ingresa las credenciales
        usuario = driver.find_element(By.NAME, "j_username")
        usuario.send_keys(d_usuario)

        contraseña = driver.find_element(By.NAME, "j_password")
        contraseña.send_keys(d_contraseña)

        # Envía el formulario
        contraseña.send_keys(Keys.RETURN)

        # Espera a que la página cargue después del inicio de sesión
        time.sleep(2)

        # Navega a la página deseada
        pagina_deseada = "https://intranet.sge.ipn.mx/principal.cfm"
        driver.get(pagina_deseada)

        # Espera a que el contenido dinámico se cargue
        time.sleep(2)
        return(driver)
    except Exception:
        print("Se produjo un Error")
        return(driver)
