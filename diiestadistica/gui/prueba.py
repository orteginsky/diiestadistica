import tkinter as tk
from tkinter import ttk

def ventana_base(nueva_ventana,titulo="M A P R E"):
    nueva_ventana.title(titulo)
    nueva_ventana.geometry("900x400")
    color_fondo = "#5A1236"
    nueva_ventana.configure(bg=color_fondo)
    return nueva_ventana

root = tk.Tk()
root = ventana_base(root,"I N I C I O")

# Crear el estilo
style = ttk.Style()
style.configure("Vertical.TNotebook", tabposition="wn")  # Pestañas a la izquierda
style.configure("Vertical.TNotebook.Tab", width=40, padding=[10, 20])  # Ajustar tamaño
#style.configure("Custom.TNotebook.Tab", padding=[10, 5], background="lightgray", foreground="black", borderwidth=2)

# Crear el Notebook con estilo
notebook = ttk.Notebook(root, style="Vertical.TNotebook")
notebook.pack(expand=True, fill="both")

# Crear pestañas (Frames)
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)

notebook.add(frame1, text="Inicio")
notebook.add(frame2, text="Configuración")
notebook.add(frame3, text="Acerca de")

root.mainloop()
