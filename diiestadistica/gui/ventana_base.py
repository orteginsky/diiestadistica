import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ..scraping.credenciales import credenciales
from selenium import webdriver

def ventana_base(titulo="M A P R E",sub_label="Automatización"):
    nueva_ventana = tk.Tk()
    nueva_ventana.title(titulo)
    nueva_ventana.geometry("800x533")
    
    color_fondo = "#5A1236"
    color_texto = "#FFFFFF"
    
    nueva_ventana.configure(bg=color_fondo)
    
    label = tk.Label(nueva_ventana, text=sub_label, 
                     font=("Arial", 40, "bold"), fg=color_texto, bg=color_fondo)
    label.pack(pady=20)
    return nueva_ventana

def agregar_cerrar(nueva_ventana):
    color_fondo = "#5A1236"
    boton_cerrar = tk.Button(nueva_ventana, text="Cerrar", font=("Arial", 12), 
                             command=nueva_ventana.destroy, bg="#FFFFFF", fg=color_fondo)
    boton_cerrar.pack(pady=10)

def agregar_ciclo_box(nueva_ventana):
    año_actual = datetime.now().year
    ciclos_anuales = [f"{a}-{a+1}" for a in range(2010, año_actual + 1)]
    ciclo_var = tk.StringVar()
    combobox = ttk.Combobox(nueva_ventana, textvariable=ciclo_var, values=ciclos_anuales, state="readonly")
    combobox.pack(pady=10)
    combobox.current(len(ciclos_anuales) - 1) 

def reemplazar_ventana(ventana_actual,titulo,subtitulo):
    ventana_actual.destroy() 
    ventana = ventana_base(titulo,subtitulo)
    return ventana

def activar_descarga_intranet():
    driver=webdriver.Chrome()
    credenciales(driver)

def agregar_selenium(nueva_ventana):
    color_fondo = "#5A1236"
    boton_cerrar = tk.Button(nueva_ventana, text="Inciar Descarga", font=("Arial", 12), 
                             command=activar_descarga_intranet, bg="#FFFFFF", fg=color_fondo)
    boton_cerrar.pack(pady=10)
    