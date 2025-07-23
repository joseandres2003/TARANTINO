# clase05_operaciones_listas.py
# Ejercicio 1: Función para sumar elementos de una lista
def sumar_elementos(lista_numeros):
    """
    Función que recibe una lista de números y retorna la suma total de los elementos.
    Parámetro:
        lista_numeros: Lista de números a sumar
    Retorna:
        La suma total de todos los elementos de la lista (puede ser un número negativo)     """
    # Implementa el algoritmo que diseñamos:
    # Crea una variable acumulador_suma inicializada en 0
    acumulador_suma = 0
    # Usa un bucle for para recorrer lista_numeros
    for elemento_actual in lista_numeros:
        # En cada iteración, acumulador_suma += elemento_actual
        acumulador_suma += elemento_actual
    # Al final, return acumulador_suma
    return acumulador_suma
# Casos de Prueba con assert
print("Probando sumar_elementos...")
assert sumar_elementos([1, 2, 3, 4, 5]) == 15
assert sumar_elementos([10, -2, 5]) == 13
assert sumar_elementos([]) == 0  # ¡Importante probar con una lista vacía!
assert sumar_elementos([100]) == 100
print("¡Pruebas para sumar_elementos pasaron! ✅")
# Pruebas adicionales para verificar que funciona correctamente
print("\n--- Pruebas adicionales ---")
print(f"Suma de [1, 2, 3, 4, 5]: {sumar_elementos([1, 2, 3, 4, 5])}")
print(f"Suma de [10, -2, 5]: {sumar_elementos([10, -2, 5])}")
print(f"Suma de lista vacía []: {sumar_elementos([])}")
print(f"Suma de [100]: {sumar_elementos([100])}")
print(f"Suma de [-1, -2, -3]: {sumar_elementos([-1, -2, -3])}")
print(f"Suma de [0, 0, 0, 0]: {sumar_elementos([0, 0, 0, 0])}")
print("\nJIMMY REQUENA - FIN DEL PROGRAMA SUMA DE ELEMENTOS")

# Ejercicio 2: Función para encontrar el mayor elemento de una lista
# Definición de la función encontrar_mayor

def encontrar_mayor(lista_numeros):
    """
    Recibe una lista de números y retorna el número más grande.
    Si la lista está vacía, retorna None.
    """
    # Caso especial: lista vacía
    if not lista_numeros:
        return None

    # Inicializar con el primer elemento
    mayor_temporal = lista_numeros[0]

    # Recorrer el resto de la lista
    for elemento_actual in lista_numeros[1:]:
        if elemento_actual > mayor_temporal:
            mayor_temporal = elemento_actual

    # Devolver el mayor encontrado
    return mayor_temporal

# Pruebas de la función con impresión de resultados
print("\nProbando encontrar_mayor...\n")

listas_de_prueba = [
    [1, 9, 2, 8, 3, 7],
    [-1, -9, -2, -8],
    [42, 42, 42],
    [],
    [5]
]

# Ejecutar cada prueba y mostrar resultados
for lista in listas_de_prueba:
    resultado = encontrar_mayor(lista)
    print(f"Lista: {lista} -> Mayor encontrado: {resultado}")

# Verificar que los resultados son correctos con assert
assert encontrar_mayor([1, 9, 2, 8, 3, 7]) == 9
assert encontrar_mayor([-1, -9, -2, -8]) == -1
assert encontrar_mayor([42, 42, 42]) == 42
assert encontrar_mayor([]) == None
assert encontrar_mayor([5]) == 5

print("\n¡Pruebas para encontrar_mayor pasaron! ✅")

print("\nJIMMY REQUENA - FIN DEL PROGRAMA ENCUENTRA EL MAYOR ELEMENTO")

# Ejercicio 3: Función para contar cuántas veces aparece un elemento en una lista.
# Definición de la función contar_apariciones
def contar_apariciones(lista, elemento_buscado):
    """
    Cuenta cuántas veces aparece un elemento en una lista.

    Parámetros:
        lista: La lista en la que se buscará.
        elemento_buscado: El elemento que queremos contar.

    Retorna:
        El número de veces que el elemento aparece en la lista.
    """
    # Inicialización del contador
    contador = 0

    # Iteración y comparación
    for elemento in lista:
        if elemento == elemento_buscado:
            contador += 1

    # Resultado final
    return contador

# Pruebas del programa
print("\nProbando contar_apariciones...\n")

# Lista de ejemplo
lista_ejemplo = [4, 2, 4, 3, 4, 5, 6, 2, 4, 7, 8, 4]

# Elementos a buscar
elementos_a_buscar = [4, 2, 9, 7]

# Ejecutar pruebas e imprimir resultados
for elemento in elementos_a_buscar:
    resultado = contar_apariciones(lista_ejemplo, elemento)
    print(f"Elemento '{elemento}' aparece {resultado} veces en la lista: {lista_ejemplo}")
print("\nJIMMY REQUENA - FIN DEL PROGRAMA QUE CUENTA LAS VECES QUE APARECE UN ELEMENTO")

# Ejercicio 4: Función para invertir la posiciòn de los elementos de una lista
# Definición de la función invertir_lista
def invertir_lista(lista_original):
    """
    Recibe una lista y retorna una nueva lista con los elementos en orden inverso.
    No modifica la lista original.
    """
    lista_invertida = []

    # Recorrer la lista original de atrás hacia adelante
    for i in range(len(lista_original) - 1, -1, -1):
        lista_invertida.append(lista_original[i])

    return lista_invertida

# Pruebas de la función
print("\nProbando invertir_lista...\n")

# Lista de prueba
lista_prueba = [1, 2, 3, 4, 5]
lista_resultante = invertir_lista(lista_prueba)

# Imprimir resultados
print(f"Lista original: {lista_prueba}")
print(f"Lista invertida: {lista_resultante}")

# Asserts para verificar comportamiento correcto
assert lista_resultante == [5, 4, 3, 2, 1]
assert lista_prueba == [1, 2, 3, 4, 5]  # La lista original no debe cambiar
assert invertir_lista(["a", "b", "c"]) == ["c", "b", "a"]
assert invertir_lista([]) == []

print("¡Pruebas para invertir_lista pasaron! ✅")
print("\ntarantino - FIN DEL PROGRAMA QUE INVIERTE LOS ELEMENTOS DE UNA LISTA")