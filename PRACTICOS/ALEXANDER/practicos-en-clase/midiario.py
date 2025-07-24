nombre_archivo = "mi_diario_alex.txt"

with open(nombre_archivo, 'w') as diario_file:
    diario_file.write("Querido diario,\n")
    diario_file.write("Hoy aprendí sobre archivos txt en Python.\n")
    diario_file.write("El modo 'w' borra todo antes de escribir. ¡Qué miedo!\n")

print("¡Listo, se escribió el diario")
