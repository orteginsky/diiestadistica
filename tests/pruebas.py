
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

from ..diiestadistica.scraping.credenciales import ingresar_credenciales


driver = webdriver.Chrome()

ingresar_credenciales(driver)