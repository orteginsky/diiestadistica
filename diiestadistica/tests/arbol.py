import os

def mostrar_arbol(directorio, prefijo=''):
    for nombre in sorted(os.listdir(directorio)):
        ruta = os.path.join(directorio, nombre)
        print(prefijo + '├── ' + nombre)
        if os.path.isdir(ruta):
            mostrar_arbol(ruta, prefijo + '│   ')



mostrar_arbol('/home/kaliuser/Documentos/diiestadistica/diiestadistica/')
