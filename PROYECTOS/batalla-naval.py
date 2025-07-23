import tkinter as tk
import random

TAMANO = 8
BARCOS = [2, 3, 3]

class BatallaNaval:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalla Naval")
        self.turno_jugador = True

        self.tablero_jugador = [["~"] * TAMANO for _ in range(TAMANO)]
        self.tablero_cpu = [["~"] * TAMANO for _ in range(TAMANO)]

        self.barcos_jugador = []
        self.barcos_cpu = []

        self.botones = []
        self.crear_tablero()
        self.colocar_barcos(self.barcos_jugador, self.tablero_jugador)
        self.colocar_barcos(self.barcos_cpu, self.tablero_cpu)
        self.mostrar_barcos_jugador()

        self.label = tk.Label(root, text="¡Tu turno!")
        self.label.grid(row=TAMANO + 1, column=0, columnspan=TAMANO)

        self.boton_reiniciar = tk.Button(root, text="Reiniciar", command=self.reiniciar)
        self.boton_reiniciar.grid(row=TAMANO + 2, column=0, columnspan=TAMANO)

    def crear_tablero(self):
        for i in range(TAMANO):
            fila = []
            for j in range(TAMANO):
                b = tk.Button(self.root, text=" ", width=2, command=lambda x=i, y=j: self.disparar(x,y))
                b.grid(row=i, column=j)
                fila.append(b)
            self.botones.append(fila)

    def colocar_barcos(self, barcos, tablero):
        for tamaño in BARCOS:
            while True:
                ori = random.choice(["H", "V"])
                fila = random.randint(0, TAMANO-1)
                col = random.randint(0, TAMANO-1)
                if ori == "H" and col + tamaño <= TAMANO and all(tablero[fila][col+i] == "~" for i in range(tamaño)):
                    for i in range(tamaño):
                        tablero[fila][col+i] = "B"
                    barcos.append([(fila,col+i) for i in range(tamaño)])
                    break
                elif ori == "V" and fila + tamaño <= TAMANO and all(tablero[fila+i][col] == "~" for i in range(tamaño)):
                    for i in range(tamaño):
                        tablero[fila+i][col] = "B"
                    barcos.append([(fila+i,col) for i in range(tamaño)])
                    break

    def mostrar_barcos_jugador(self):
        # Pinta los barcos del jugador en el tablero para que se vean
        for barco in self.barcos_jugador:
            for (fila, col) in barco:
                self.botones[fila][col].config(bg="gray")

    def disparar(self, fila, col):
        if not self.turno_jugador:
            return
        if self.botones[fila][col]["text"] != " ":
            return

        if self.tablero_cpu[fila][col] == "B":
            self.botones[fila][col].config(text="X", bg="red")
            self.remover_barco(self.barcos_cpu, fila, col)
            self.label.config(text="¡Le diste a un barco!")
            if not self.barcos_cpu:
                self.label.config(text="¡Ganaste!")
                self.fin_juego()
                return
        else:
            self.botones[fila][col].config(text="O", bg="blue")
            self.label.config(text="Fallaste.")
            self.turno_jugador = False
            self.root.after(1000, self.turno_cpu)

    def remover_barco(self, barcos, fila, col):
        for barco in barcos:
            if (fila,col) in barco:
                barco.remove((fila,col))
                if not barco:
                    barcos.remove(barco)
                break

    def turno_cpu(self):
        while True:
            fila = random.randint(0, TAMANO-1)
            col = random.randint(0, TAMANO-1)
            if self.tablero_jugador[fila][col] not in ("X", "O"):
                break

        if self.tablero_jugador[fila][col] == "B":
            self.tablero_jugador[fila][col] = "X"
            self.remover_barco(self.barcos_jugador, fila, col)
            self.botones[fila][col].config(bg="red", text="X")
            self.label.config(text=f"La computadora le dio en ({fila},{col})")
            if not self.barcos_jugador:
                self.label.config(text="¡Perdiste!")
                self.fin_juego()
                return
            self.root.after(1000, self.turno_cpu)  # CPU dispara de nuevo si acierta
        else:
            self.tablero_jugador[fila][col] = "O"
            self.botones[fila][col].config(bg="blue", text="O")
            self.label.config(text=f"La computadora falló en ({fila},{col})")
            self.turno_jugador = True

    def fin_juego(self):
        for fila in self.botones:
            for b in fila:
                b.config(state="disabled")

    def reiniciar(self):
        # Reinicia el juego
        self.turno_jugador = True
        self.tablero_jugador = [["~"] * TAMANO for _ in range(TAMANO)]
        self.tablero_cpu = [["~"] * TAMANO for _ in range(TAMANO)]
        self.barcos_jugador = []
        self.barcos_cpu = []
        for fila in self.botones:
            for b in fila:
                b.config(text=" ", bg="SystemButtonFace", state="normal")
        self.colocar_barcos(self.barcos_jugador, self.tablero_jugador)
        self.colocar_barcos(self.barcos_cpu, self.tablero_cpu)
        self.mostrar_barcos_jugador()
        self.label.config(text="¡Tu turno!")

if __name__ == "__main__":
    root = tk.Tk()
    juego = BatallaNaval(root)
    root.mainloop()
