import tkinter as tk
from tkinter import simpledialog, ttk
import random
import sqlite3

ANCHO_CANVAS = 400
ALTO_CANVAS = 500
TAM_BLOQUE = 40

class JuegoBreakout:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Breakout")

        # Crear el contenedor de pestañas
        self.notebook = ttk.Notebook(ventana)
        self.notebook.pack(expand=1, fill="both")

        # Crear la pestaña del juego
        self.frame_juego = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_juego, text='Juego')
        self.inicializar_juego()

        # Crear la pestaña de los mejores puntajes
        self.frame_mejores_puntajes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_mejores_puntajes, text='Mejores Puntajes')

        # Configurar el evento de cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def inicializar_juego(self):
        self.canvas = tk.Canvas(self.frame_juego, width=ANCHO_CANVAS, height=ALTO_CANVAS, bg="black")
        self.canvas.pack()

        self.puntos = 0
        self.etiqueta_puntos = tk.Label(self.frame_juego, text=f"Puntos: {self.puntos}", fg="white", bg="black")
        self.etiqueta_puntos.pack()

        self.bloques = []
        self.crear_bloques()

        self.paleta = self.canvas.create_rectangle(ANCHO_CANVAS / 2 - 50, ALTO_CANVAS - 20, ANCHO_CANVAS / 2 + 50, ALTO_CANVAS - 10, fill="white")

        self.pelota = self.canvas.create_oval(10, 10, 25, 25, fill="white")
        self.canvas.move(self.pelota, ANCHO_CANVAS / 2, ALTO_CANVAS / 2)

        self.dx = 2.5
        self.dy = -2.5

        self.canvas.bind_all("<KeyPress-Left>", self.mover_izquierda)
        self.canvas.bind_all("<KeyPress-Right>", self.mover_derecha)
        self.canvas.bind_all("<space>", self.iniciar_juego)

        self.juego_iniciado = False
        self.boton_reinicio = tk.Button(self.frame_juego, text="Reiniciar", command=self.reiniciar_juego)
        self.boton_reinicio.pack()

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
            pos_pelota = self.canvas.coords(self.pelota)
            pos_paleta = self.canvas.coords(self.paleta)

            if pos_pelota[1] <= 0:
                self.dy = -self.dy

            if pos_pelota[0] <= 0 or pos_pelota[2] >= ANCHO_CANVAS:
                self.dx = -self.dx

            if pos_pelota[3] >= ALTO_CANVAS:
                if pos_pelota[2] >= pos_paleta[0] and pos_pelota[0] <= pos_paleta[2] and pos_pelota[3] >= pos_paleta[1]:
                    self.dy = -self.dy
                else:
                    self.registrar_puntaje()
                    self.ventana.after_cancel(self.mover_pelota)
                    self.canvas.create_text(ANCHO_CANVAS / 2, ALTO_CANVAS / 2, text="¡Juego terminado!", fill="white", font=("Arial", 20))
                    self.juego_iniciado = False
                    self.dx = 0
                    self.dy = 0

            for bloque in self.bloques:
                if self.colision_pelota(bloque):
                    self.canvas.delete(bloque)
                    self.bloques.remove(bloque)
                    self.dy = -self.dy
                    self.puntos += 10
                    self.etiqueta_puntos.config(text=f"Puntos: {self.puntos}")
                    break

            if len(self.bloques) == 0:
                self.crear_bloques()  # Crear nuevos bloques cuando todos son eliminados

            self.ventana.after(10, self.mover_pelota)

    def colision_pelota(self, objeto):
        pos_pelota = self.canvas.coords(self.pelota)
        pos_objeto = self.canvas.coords(objeto)
        return pos_pelota[2] >= pos_objeto[0] and pos_pelota[0] <= pos_objeto[2] and pos_pelota[3] >= pos_objeto[1] and pos_pelota[1] <= pos_objeto[3]

    def reiniciar_juego(self):
        self.juego_iniciado = False
        self.canvas.delete(tk.ALL)
        self.puntos = 0
        self.etiqueta_puntos.config(text=f"Puntos: {self.puntos}")
        self.bloques = []
        self.crear_bloques()
        self.paleta = self.canvas.create_rectangle(ANCHO_CANVAS / 2 - 50, ALTO_CANVAS - 20, ANCHO_CANVAS / 2 + 50, ALTO_CANVAS - 10, fill="white")
        self.pelota = self.canvas.create_oval(10, 10, 25, 25, fill="white")
        self.canvas.move(self.pelota, ANCHO_CANVAS / 2, ALTO_CANVAS / 2)
        self.dx = 3
        self.dy = -3

    def iniciar_juego(self, event):
        if not self.juego_iniciado:
            self.juego_iniciado = True
            self.mover_pelota()

    def guardar_puntaje(self, nombre, puntaje):
        conn = sqlite3.connect('puntajes.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Puntajes (Nombre TEXT, Puntaje INTEGER)')
        cursor.execute('INSERT INTO Puntajes VALUES (?, ?)', (nombre, puntaje))
        conn.commit()
        conn.close()

    def registrar_puntaje(self):
        nombre = simpledialog.askstring("Perdiste", "Ingresa tu nombre para registrar tu puntaje:")
        if nombre:
            self.guardar_puntaje(nombre, self.puntos)

    def on_tab_change(self, event):
        # Si cambia a la pestaña de los mejores puntajes, actualizar los puntajes
        if self.notebook.index(self.notebook.select()) == 1:
            self.mostrar_mejores_puntajes()

    def mostrar_mejores_puntajes(self):
        conexion = sqlite3.connect('puntajes.db')
        cursor = conexion.cursor()

        cursor.execute("SELECT Nombre, Puntaje FROM Puntajes ORDER BY Puntaje DESC LIMIT 10")
        resultados = cursor.fetchall()

        conexion.close()

        # Limpiar la pestaña antes de mostrar nuevos puntajes
        for widget in self.frame_mejores_puntajes.winfo_children():
            widget.destroy()

        # Crear una etiqueta para mostrar los resultados
        etiqueta_resultados = tk.Label(self.frame_mejores_puntajes, text="Mejores Puntajes:")
        etiqueta_resultados.pack()

        # Mostrar los resultados en la pestaña
        for nombre, puntaje in resultados:
            etiqueta = tk.Label(self.frame_mejores_puntajes, text=f"{nombre}: {puntaje}")
            etiqueta.pack()

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoBreakout(root)
    root.mainloop()
