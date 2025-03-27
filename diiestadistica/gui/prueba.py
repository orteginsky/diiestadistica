import tkinter as tk
from tkinter import ttk

def ejecutar_funciones(frame, labels, funciones, idx=0):
    """
    Ejecuta funciones en orden, esperando que cada una termine antes de continuar con la siguiente.

    :param frame: ttk.Frame donde están los labels.
    :param labels: Lista de labels donde se mostrarán los resultados (✅ o ❌).
    :param funciones: Lista de funciones a ejecutar.
    :param idx: Índice de la función actual (para llamadas recursivas).
    """
    if idx >= len(funciones):
        return  # Detener si ya ejecutamos todas

    try:
        funciones[idx]()  # Ejecutar la función
        labels[idx].config(text="✅", fg="green")  # Marcar como éxito
    except Exception as e:
        labels[idx].config(text="❌", fg="red")  # Marcar error
        print(f"Error en la función {idx + 1}: {e}")

    # Llamar a la siguiente función después de terminar
    frame.after(100, lambda: ejecutar_funciones(frame, labels, funciones, idx + 1))

# Funciones de prueba (cada una tarda un tiempo distinto)
import time

def funcion1():
    print("Función 1 ejecutada")
    time.sleep(2)  # Simula que tarda 2 segundos

def funcion2():
    print("Función 2 ejecutada")
    time.sleep(1)  # Simula que tarda 1 segundo

def funcion3():
    print("Función 3 ejecutada")
    time.sleep(4)  # Simula que tarda 4 segundos

def funcion4():
    print("Función 4 ejecutada")
    time.sleep(3)  # Simula que tarda 3 segundos

# Crear la ventana
root = tk.Tk()
root.title("Ejecución Consecutiva")

# Crear frame donde estarán los labels
frame = ttk.Frame(root, padding=20)
frame.pack()

# Crear los labels y textos
labels = []
for i in range(4):
    tk.Label(frame, text=f"Función {i+1}").grid(row=i, column=0)
    label = tk.Label(frame, text="Esperando...")
    label.grid(row=i, column=1, padx=10)
    labels.append(label)

# Lista de funciones a ejecutar
funciones = [funcion1, funcion2, funcion3, funcion4]

# Botón para ejecutar
boton = tk.Button(frame, text="Ejecutar", command=lambda: ejecutar_funciones(frame, labels, funciones))
boton.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
