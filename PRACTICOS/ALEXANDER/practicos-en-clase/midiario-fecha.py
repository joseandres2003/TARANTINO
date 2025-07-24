from datetime import datetime

nombre_archivo = "mi_diario_alex.txt"

fecha_actual = datetime.now().strftime("%Y-%m-%d")

with open(nombre_archivo, 'w') as diario_file:
    
    diario_file.write(f"Fecha: {fecha_actual}\n\n")

   
    diario_file.write("Querido diario,\n")
    diario_file.write("Hoy aprendí sobre archivos en Python.\n")
    diario_file.write("El modo 'w' borra todo antes de escribir. ¡Qué miedo!\n")

print("¡Listo, se escribió el diario")
