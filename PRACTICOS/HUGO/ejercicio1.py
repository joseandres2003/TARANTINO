import getpass

# Constantes
MIN_NUM = 0
MAX_NUM = 99

def verificar_adivinanza(numero_secreto, intento):
    """Devuelve una pista según la diferencia entre el intento y el número secreto."""
    if intento < numero_secreto:
        return "Demasiado bajo"
    elif intento > numero_secreto:
        return "Demasiado alto"
    else:
        return "Correcto"

def solicitar_numero_secreto():
    """Solicita al usuario ingresar un número secreto válido (oculto)."""
    while True:
        try:
            entrada = getpass.getpass(f"🔐 Ingresa el número secreto (oculto, entre {MIN_NUM}-{MAX_NUM}): ")
            numero = int(entrada)
            if MIN_NUM <= numero <= MAX_NUM:
                return numero
            else:
                print(f"⚠️ El número debe estar entre {MIN_NUM} y {MAX_NUM}.")
        except ValueError:
            print("⚠️ Ingresa un número válido.")

def jugar_una_ronda():
    """Lógica de una ronda del juego."""
    numero_secreto = solicitar_numero_secreto()
    print(f"\n🎯 ¡Adivina el n