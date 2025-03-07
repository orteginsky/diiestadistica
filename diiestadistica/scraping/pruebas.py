from .credenciales import credenciales
from selenium import webdriver

driver = webdriver.Chrome()
credenciales(driver)
