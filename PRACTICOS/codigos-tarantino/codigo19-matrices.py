# --- MATRIZ DE NÚMEROS ---
# Definimos una matriz de 3 filas y 4 columnas
matriz = [
    [10, 20, 30, 40],  # Fila 0
    [50, 60, 70, 80],  # Fila 1
    [90, 91, 92, 93]   # Fila 2
]

# Acceder al número 70
valor = matriz[1][2]
print(f"El valor es: {valor}")  # Resultado: 70

# Modificar el valor 90 por un 0
matriz[2][0] = 0

print("\n--- Recorrido con índices ---")
num_filas = len(matriz)
num_columnas = len(matriz[0])
for i in range(num_filas):
    for j in range(num_columnas):
        elemento = matriz[i][j]
        print(f"Elemento en ({i},{j}) es {elemento}")

print("\n--- Recorrido Pythonico ---")
for fila_actual in matriz:
    for elemento in fila_actual:
        print(elemento, end=" ")
    print()  # Salto de línea entre filas

# --- TABLERO DE TRES EN RAYA ---
print("\n--- Tablero de Tres en Raya ---")
tablero = [
    ['X', 'O', 'X'],
    [' ', 'X', 'O'],
    ['O', ' ', ' ']
]

for fila in tablero:
    print(" | ".join(fila))
    print("-" * 9)
print ("fin del programa tarantino")