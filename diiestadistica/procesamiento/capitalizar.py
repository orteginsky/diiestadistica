import pandas as pd
import re

def capitalizar(columna):
    # Convertir todo a minúsculas y luego a formato de título (capitalizar)
    columna = columna.str.lower().str.title()

    # Lista de palabras a mantener en minúsculas
    palabras = [" En ", " De ", " La ", " El ", " Y ", " E ", 
                " Con ", " Por ", " Los ", " Para ", " Sus ", 
                " Del ", " Más ", " Mas "]
    
    # Reemplazar las palabras dentro de la cadena
    for palabra in palabras:
        columna = columna.str.replace(palabra, palabra.lower(), regex=True)

    # Reemplazar dobles espacios por un solo espacio
    columna = columna.str.replace("  ", " ", regex=True)

    return columna
