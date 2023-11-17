import tkinter as tk
import random
import time

ANCHO_CANVAS = 400
ALTO_CANVAS = 300
TAM_BLOQUE = 40

class JuegoBreakout:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Breakout")
        self.canvas = tk.Canvas(ventana, width=ANCHO_CANVAS, height=ALTO_CANVAS, bg="black")
        self.canvas.pack()

        self.puntos = 0
        self.etiqueta_puntos = tk.Label(ventana, text=f"Puntos: {self.puntos}", fg="white", bg="black")
        self.etiqueta_puntos.pack()

        self.bloques = []
        self.crear_bloques()

        self.paleta = self.canvas.create_rectangle(ANCHO_CANVAS / 2 - 50, ALTO_CANVAS - 10, ANCHO_CANVAS / 2 + 50, ALTO_CANVAS - 5, fill="white")

        self.pelota = self.canvas.create_oval(10, 10, 25, 25, fill="white")
        self.canvas.move(self.pelota, ANCHO_CANVAS / 2, ALTO_CANVAS / 2)

        self.dx = 3
        self.dy = -3

        self.canvas.bind_all("<KeyPress-Left>", self.mover_izquierda)
        self.canvas.bind_all("<KeyPress-Right>", self.mover_derecha)

        self.juego_iniciado = False

    def crear_bloques(self):
        colores = ["red", "orange", "yellow", "green", "blue"]
        for fila in range(0, 3):
            for columna in range(0, ANCHO_CANVAS // TAM_BLOQUE):
                x1 = columna * TAM_BLOQUE
                y1 = fila * TAM_BLOQUE
                x2 = x1 + TAM_BLOQUE
                y2 = y1 + TAM_BLOQUE
                color = random.choice(colores)
                bloque = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                self.bloques.append(bloque)

    def mover_izquierda(self, event):
        if self.juego_iniciado:
            self.canvas.move(self.paleta, -20, 0)
            self.detectar_colision_paleta()

    def mover_derecha(self, event):
        if self.juego_iniciado:
            self.canvas.move(self.paleta, 20, 0)
            self.detectar_colision_paleta()

    def detectar_colision_paleta(self):
        pos_paleta = self.canvas.coords(self.paleta)
        pos_pelota = self.canvas.coords(self.pelota)

        if pos_pelota[2] >= pos_paleta[0] and pos_pelota[0] <= pos_paleta[2] and pos_pelota[3] >= pos_paleta[1]:
            self.dy = -self.dy

    def mover_pelota(self):
        if self.juego_iniciado:
            self.canvas.move(self.pelota, self.dx, self.dy)
            pos = self.canvas.coords(self.pelota)

            if pos[1] <= 0:
                self.dy = -self.dy

            if pos[0] <= 0 or pos[2] >= ANCHO_CANVAS:
                self.dx = -self.dx

            for bloque in self.bloques:
                if self.colision_pelota(bloque):
                    self.canvas.delete(bloque)
                    self.bloques.remove(bloque)
                    self.dy = -self.dy
                    self.puntos += 10
                    self.etiqueta_puntos.config(text=f"Puntos: {self.puntos}")
                    break

            if len(self.bloques) == 0:
                self.ventana.after_cancel(self.mover_pelota)
                self.canvas.create_text(ANCHO_CANVAS / 2, ALTO_CANVAS / 2, text="¡Has ganado!", fill="white", font=("Arial", 20))

            if pos[3] >= ALTO_CANVAS:
                self.ventana.after_cancel(self.mover_pelota)
                self.canvas.create_text(ANCHO_CANVAS / 2, ALTO_CANVAS / 2, text="¡Juego terminado!", fill="white", font=("Arial", 20))

            self.ventana.after(10, self.mover_pelota)

    def colision_pelota(self, objeto):
        pos = self.canvas.coords(self.pelota)
        objeto_pos = self.canvas.coords(objeto)
        return pos[2] >= objeto_pos[0] and pos[0] <= objeto_pos[2] and pos[3] >= objeto_pos[1] and pos[1] <= objeto_pos[3]

    def iniciar_juego(self):
        self.juego_iniciado = True
        self.mover_pelota()

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoBreakout(root)
    juego.iniciar_juego()
    root.mainloop()