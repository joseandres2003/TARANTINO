import os
import glob
import time

# Ruta de los ejercicios
ruta_ejercicios = "PRACTICOS"

# Buscar todos los archivos .py en la carpeta
archivos_py = glob.glob(os.path.join(ruta_ejercicios, "*.py"))

# Filtrar __init__.py (opcional, por si no quieres ejecutarlo)
archivos_py = [f for f in archivos_py if not f.endswith("__init__.py")]

# Verificar que haya archivos
if not archivos_py:
    print("No hay archivos .py para ejecutar.")
    exit()

# Ordenar por fecha de modificación (último modificado al final)
archivo_reciente = max(archivos_py, key=os.path.getmtime)

# Mostrar cuál se ejecuta
print(f"Ejecutando el archivo más reciente: {archivo_reciente}")

# Ejecutar el archivo
os.system(f"python3 {archivo_reciente}")
