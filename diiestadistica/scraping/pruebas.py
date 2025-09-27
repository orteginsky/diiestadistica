from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

"""(myenv) kaliuser@kali:~/Documentos/diiestadistica$ /home/kaliuser/Documentos/diiestadistica/myenv/bin/python /home/kaliuser/Documentos/diiestadistica/diiestadistica/scraping/pruebas.py
Traceback (most recent call last):
  File "/home/kaliuser/Documentos/diiestadistica/diiestadistica/scraping/pruebas.py", line 4, in <module>
    driver = webdriver.Chrome(ChromeDriverManager().install())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/kaliuser/Documentos/diiestadistica/myenv/lib/python3.12/site-packages/selenium/webdriver/chrome/webdriver.py", line 45, in __init__
    super().__init__(
  File "/home/kaliuser/Documentos/diiestadistica/myenv/lib/python3.12/site-packages/selenium/webdriver/chromium/webdriver.py", line 50, in __init__
    if finder.get_browser_path():
       ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/kaliuser/Documentos/diiestadistica/myenv/lib/python3.12/site-packages/selenium/webdriver/common/driver_finder.py", line 47, in get_browser_path
    return self._binary_paths()["browser_path"]
           ^^^^^^^^^^^^^^^^^^^^
  File "/home/kaliuser/Documentos/diiestadistica/myenv/lib/python3.12/site-packages/selenium/webdriver/common/driver_finder.py", line 56, in _binary_paths
    browser = self._options.capabilities["browserName"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'capabilities'"""