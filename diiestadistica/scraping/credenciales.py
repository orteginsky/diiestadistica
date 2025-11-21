# diiestadistica/scraping/credenciales.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from diiestadistica.core.logging_config import setup_logger
from diiestadistica.core.settings import settings

logger = setup_logger(__name__)


def credenciales(driver, timeout: int = 10):
    """
    Inicia sesión en la intranet usando Selenium WebDriver.

    Args:
        driver: Instancia de Selenium WebDriver.
        timeout (int): Tiempo máximo de espera para encontrar elementos (segundos).

    Returns:
        driver: El WebDriver autenticado (o en el último estado alcanzado si hubo error).
    """
    try:
        logger.info("Navegando a la página de inicio de sesión: %s", settings.intranet_url)
        driver.get(settings.intranet_url)

        # Espera explícita para que aparezca el campo de usuario
        usuario = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.NAME, "j_username"))
        )
        usuario.send_keys(settings.scraping_usuario)
        logger.debug("Usuario ingresado correctamente.")

        contraseña = driver.find_element(By.NAME, "j_password")
        contraseña.send_keys(settings.scraping_password)
        logger.debug("Contraseña ingresada correctamente.")

        contraseña.send_keys(Keys.RETURN)
        logger.info("Formulario enviado, esperando redirección...")
        time.sleep(2)
        driver.get(settings.intranet_home)
        logger.info("Inicio de sesión exitoso, redirigido a: %s", driver.current_url)

        return driver

    except Exception as e:
        logger.error(f"❌ Error al iniciar sesión en la intranet. error: {e}", exc_info=True)
        return driver
