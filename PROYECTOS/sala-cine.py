import tkinter as tk
import tkinter as tk
from tkinter import messagebox

# Configuración global
FILAS, COLUMNAS = 5, 8
PRECIOS_FILAS = {0: 30, 1: 30, 2: 25, 3: 25, 4: 20}
PELICULAS = ["Avengers", "Mario Bros", "Spider-Man", "Intensamente 2","Proyecto X"]

# Crear estructura de salas para cada película
salas = {pelicula: [['L' for _ in range(COLUMNAS)] for _ in range(FILAS)] for pelicula in PELICULAS}

# Crear ventana principal (debe ir antes de StringVar)
ventana = tk.Tk()
ventana.title("🎬 Cine - Gestión de Asientos")

# Variables que dependen de Tk
pelicula_actual = tk.StringVar()
pelicula_actual.set(PELICULAS[0])
asientos_seleccionados = []
botones = []

# Funciones
def mostrar_sala():
    global botones
    for widget in frame_sala.winfo_children():
        widget.destroy()

    botones.clear()
    sala = salas[pelicula_actual.get()]

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
    sala = salas[pelicula_actual.get()]
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

    sala = salas[pelicula_actual.get()]
    for fila, columna in asientos_seleccionados:
        sala[fila][columna] = 'O'

    messagebox.showinfo("Compra realizada", f"¡Compra confirmada para {pelicula_actual.get()}!")
    asientos_seleccionados.clear()
    mostrar_sala()

# GUI
frame_superior = tk.Frame(ventana)
frame_superior.pack(pady=10)

tk.Label(frame_superior, text="Selecciona una película:").pack(side=tk.LEFT)
menu_peliculas = tk.OptionMenu(frame_superior, pelicula_actual, *PELICULAS, command=lambda _: mostrar_sala())
menu_peliculas.pack(side=tk.LEFT)

frame_sala = tk.Frame(ventana)
frame_sala.pack()

label_info = tk.Label(ventana, text="Asientos seleccionados: \nTotal: 0 Bs", font=('Arial', 12))
label_info.pack(pady=10)

btn_comprar = tk.Button(ventana, text="Confirmar Compra", bg='blue', fg='white', command=confirmar_compra)
btn_comprar.pack(pady=5)

mostrar_sala()
ventana.mainloop()
