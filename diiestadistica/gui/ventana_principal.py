#from tkinter import Tk, Label, Button, ttk
#import subprocess

import tkinter as tk
from .ventana_base import ventana_base, agregar_cerrar, agregar_selenium
from .ventana_base import agregar_ciclo_box, reemplazar_ventana

def Ventana_selecionar_ciclo(ventana_tk):
    nueva_ventana = reemplazar_ventana(ventana_tk,"Selecionar Ciclo","Intranet")
    agregar_ciclo_box(nueva_ventana)
    agregar_selenium(nueva_ventana)
    agregar_cerrar(nueva_ventana)
    nueva_ventana.mainloop()

root = ventana_base("I N I C I O", "M A P R E")

boton = tk.Button(
    root,
    text="Iniciar",
    font=("Arial", 12),
    command=lambda: Ventana_selecionar_ciclo(root),
    bg="#FFFFFF",
    fg="#5A1236"
)
boton.pack()

root.mainloop()

