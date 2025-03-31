import re

def coincidencia(patron, valor):
    if re.search(patron, valor):
        return True
    else:
        return False

def uno(n):
    if isinstance(n,int) and n>0:
        return 1
    else:
        return 0