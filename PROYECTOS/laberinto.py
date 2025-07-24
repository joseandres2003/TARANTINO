import tkinter as tk
import time

# Laberinto fijo con camino hasta la meta (1 = pared, 0 = camino)
LABERINTO = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,0,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ANCHO_CELDA = 30
ALTO_CELDA = 30
VISIBILIDAD = 2  # muestra un área de 5x5

class LaberintoJuego:
    def __init__(self, root):
        self.root = root
        self.root.title("Laberinto Misterioso 🌌")

        self.canvas = tk.Canvas(root, width=5*ANCHO_CELDA, height=5*ALTO_CELDA, bg="black")
        self.canvas.pack()

        self.jugador_x = 1
        self.jugador_y = 1
        self.meta_x = 18
        self.meta_y = 18

        self.movimientos = 0
        self.inicio_tiempo = time.time()
        self.juego_terminado = False

        self.label_info = tk.Label(root, text="Movimientos: 0 | Tiempo: 0s | Score: 0", font=("Arial", 12))
        self.label_info.pack()

        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.mover_jugador)

        self.actualizar_tiempo()
        self.dibujar_laberinto()

    def dibujar_laberinto(self):
        self.canvas.delete("all")
        for dy in range(-VISIBILIDAD, VISIBILIDAD + 1):
            for dx in range(-VISIBILIDAD, VISIBILIDAD + 1):
                x = self.jugador_x + dx
                y = self.jugador_y + dy
                if 0 <= x < len(LABERINTO[0]) and 0 <= y < len(LABERINTO):
                    celda = LABERINTO[y][x]
                    color = "black"
                    if celda == 1:
                        color = "gray"
                    elif celda == 0:
                        color = "white"
                    if x == self.meta_x and y == self.meta_y:
                        color = "green"
                    cx = (dx + VISIBILIDAD) * ANCHO_CELDA
                    cy = (dy + VISIBILIDAD) * ALTO_CELDA
                    self.canvas.create_rectangle(cx, cy, cx + ANCHO_CELDA, cy + ALTO_CELDA, fill=color, outline="black")

        # Jugador (siempre al centro)
        centro_x = VISIBILIDAD * ANCHO_CELDA + ANCHO_CELDA // 2
        centro_y = VISIBILIDAD * ALTO_CELDA + ALTO_CELDA // 2
        self.canvas.create_oval(
            centro_x - 10, centro_y - 10,
            centro_x + 10, centro_y + 10,
            fill="blue"
        )

    def mover_jugador(self, event):
        if self.juego_terminado:
            return

        dx, dy = 0, 0
        if event.keysym == "Up": dy = -1
        elif event.keysym == "Down": dy = 1
        elif event.keysym == "Left": dx = -1
        elif event.keysym == "Right": dx = 1

        nuevo_x = self.jugador_x + dx
        nuevo_y = self.jugador_y + dy

        if 0 <= nuevo_x < 20 and 0 <= nuevo_y < 20 and LABERINTO[nuevo_y][nuevo_x] == 0:
            self.jugador_x = nuevo_x
            self.jugador_y = nuevo_y
            self.movimientos += 1
            self.dibujar_laberinto()
            self.actualizar_tiempo()

            if self.jugador_x == self.meta_x and self.jugador_y == self.meta_y:
                self.juego_terminado = True
                self.mostrar_ganador()

    def actualizar_tiempo(self):
        if not self.juego_terminado:
            tiempo_actual = int(time.time() - self.inicio_tiempo)
            score = self.calcular_score(tiempo_actual, self.movimientos)
            self.label_info.config(text=f"Movimientos: {self.movimientos} | Tiempo: {tiempo_actual}s | Score: {score}")
            self.root.after(1000, self.actualizar_tiempo)

    def calcular_score(self, tiempo, movimientos):
        return max(0, 1000 - (tiempo * 5 + movimientos * 3))

    def mostrar_ganador(self):
        tiempo_total = int(time.time() - self.inicio_tiempo)
        score_final = self.calcular_score(tiempo_total, self.movimientos)
        self.canvas.create_text(75, 75, text=f"¡Ganaste! 🏁\nMovs: {self.movimientos}\nTiempo: {tiempo_total}s\nScore: {score_final}",
                                font=("Arial", 12), fill="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    juego = LaberintoJuego(root)
    root.mainloop()
