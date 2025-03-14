import os
from .seleccionar_carpeta import seleccionar_carpeta

def cambiar_extencion_carpeta(old_extension = "xls", new_extension = "html"):
    carpeta = seleccionar_carpeta()
    print(f'haz camiado los archivos con extension: {old_extension} por la extension {new_extension}')
    for name_file in os.listdir(carpeta):
        if name_file.endswith(old_extension):
            root_file = f"{carpeta}/{name_file}"
            cambiar_extencion_archivo(root_file,new_extension)
        else:
            print('archivo conservado') 

def cambiar_extencion_archivo(root_file,extension):
    only_name,_ = os.path.splitext(root_file)
    new_name = f"{only_name}" + "."+ f"{extension}"
    os.rename(root_file, new_name)
    #print(f"se ha cambiado la extencion tio del archivo {root_file} a la extension {extension} \n")
    #print(f"{new_name}")
    return new_name
if __name__=='__main__':
    cambiar_extencion_carpeta()