from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from diiestadistica.core.logging_config import setup_logger
from diiestadistica.core.settings import settings

logger = setup_logger(__name__)

def credenciales(driver):
    try:
        # Abre la página de inicio de sesión
        driver.get(settings.intranet_url)

        time.sleep(2)

        usuario = driver.find_element(By.NAME, "j_username")
        usuario.send_keys(settings.scraping_usuario)

        contraseña = driver.find_element(By.NAME, "j_password")
        contraseña.send_keys(settings.scraping_password)

        contraseña.send_keys(Keys.RETURN)
        time.sleep(2)

        driver.get(settings.intranet_home)
        time.sleep(2)

        return driver
    except Exception:
        logger.error("Se produjo un Error")
        return driver
