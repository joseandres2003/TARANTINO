import tkinter as tk
from tkinter import messagebox, simpledialog

# Configuración global
FILAS, COLUMNAS = 5, 8
PRECIOS_FILAS = {0: 30, 1: 30, 2: 25, 3: 25, 4: 20}

PELICULAS = {
    "Avengers (13+)": {"nombre": "Avengers", "edad_minima": 13},
    "Mario Bros (7+)": {"nombre": "Mario Bros", "edad_minima": 7},
    "Spider-Man (13+)": {"nombre": "Spider-Man", "edad_minima": 13},
    "Intensamente 2 (5+)": {"nombre": "Intensamente 2", "edad_minima": 5},
    "Deadpool (18+)": {"nombre": "Deadpool", "edad_minima": 18}
}

# Crear estructura de salas
salas = {info["nombre"]: [['L' for _ in range(COLUMNAS)] for _ in range(FILAS)] for info in PELICULAS.values()}

# Crear ventana
ventana = tk.Tk()
ventana.title("🎬 Cine - Tarantino")

# Variables
pelicula_actual = tk.StringVar()
pelicula_actual.set(list(PELICULAS.keys())[0])
asientos_seleccionados = []
botones = []
edad_usuario = None

# Funciones
def pedir_edad():
    global edad_usuario
    while True:
        edad = simpledialog.askinteger("Edad del usuario", "Por favor, ingresa tu edad:")
        if edad is None:
            return
        if edad >= 0:
            edad_usuario = edad
            mostrar_sala()
            break

def cambiar_edad():
    pedir_edad()

def mostrar_sala():
    global botones
    seleccion = pelicula_actual.get()
    edad_minima = PELICULAS[seleccion]["edad_minima"]

    for widget in frame_sala.winfo_children():
        widget.destroy()

    if edad_usuario is None:
        return

    if edad_usuario < edad_minima:
        label_info.config(text=f"Edad insuficiente para ver esta película. Requiere {edad_minima}+ años.")
        return

    botones.clear()
    nombre_pelicula = PELICULAS[seleccion]["nombre"]
    sala = salas[nombre_pelicula]

    for i in range(FILAS):
        fila_botones = []
        for j in range(COLUMNAS):
            estado = sala[i][j]
            color = 'green' if estado == 'L' else 'red'
            btn = tk.Button(frame_sala, text=estado, width=4, height=2, bg=color,
                            command=lambda i=i, j=j: seleccionar_asiento(i, j))
            btn.grid(row=i, column=j, padx=2, pady=2)
            fila_botones.append(btn)
        botones.append(fila_botones)

    actualizar_info()

def seleccionar_asiento(fila, columna):
    nombre_pelicula = PELICULAS[pelicula_actual.get()]["nombre"]
    sala = salas[nombre_pelicula]
    if sala[fila][columna] == 'O':
        messagebox.showwarning("Asiento ocupado", "Ese asiento ya está ocupado.")
        return

    asiento = (fila, columna)
    if asiento in asientos_seleccionados:
        asientos_seleccionados.remove(asiento)
        botones[fila][columna].configure(bg='green')
    else:
        asientos_seleccionados.append(asiento)
        botones[fila][columna].configure(bg='yellow')

    actualizar_info()

def actualizar_info():
    total = sum(PRECIOS_FILAS[f] for f, _ in asientos_seleccionados)
    lista = ", ".join([f"F{f+1}-C{c+1}" for f, c in asientos_seleccionados])
    label_info.config(text=f"Asientos seleccionados: {lista}\nTotal: {total} Bs")

def confirmar_compra():
    if not asientos_seleccionados:
        messagebox.showinfo("Sin selección", "No has seleccionado asientos.")
        return

    nombre_pelicula = PELICULAS[pelicula_actual.get()]["nombre"]
    sala = salas[nombre_pelicula]
    for fila, columna in asientos_seleccionados:
        sala[fila][columna] = 'O'

    messagebox.showinfo("Compra realizada", f"¡Compra confirmada para {nombre_pelicula}!")
    asientos_seleccionados.clear()
    mostrar_sala()

# GUI
frame_superior = tk.Frame(ventana)
frame_superior.pack(pady=10)

tk.Label(frame_superior, text="Selecciona una película:").pack(side=tk.LEFT)
menu_peliculas = tk.OptionMenu(frame_superior, pelicula_actual, *PELICULAS.keys(), command=lambda _: mostrar_sala())
menu_peliculas.pack(side=tk.LEFT, padx=10)

btn_cambiar_edad = tk.Button(frame_superior, text="Cambiar Edad", command=cambiar_edad)
btn_cambiar_edad.pack(side=tk.LEFT)

frame_sala = tk.Frame(ventana)
frame_sala.pack()

label_info = tk.Label(ventana, text="Asientos seleccionados: \nTotal: 0 Bs", font=('Arial', 12))
label_info.pack(pady=10)

btn_comprar = tk.Button(ventana, text="Confirmar Compra", bg='blue', fg='white', command=confirmar_compra)
btn_comprar.pack(pady=5)

# Pedimos la edad al inicio
ventana.after(100, pedir_edad)

ventana.mainloop()
