import tkinter as tk
import random

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Breakout")
ventana.geometry("500x400")

# Configuración de la pelota
pelota = tk.Canvas(ventana, width=20, height=20)
pelota.create_oval(0, 0, 20, 20, fill="red")
pelota.pack()

# Posición inicial de la pelota
pelota_x = 250
pelota_y = 200
dx = 2
dy = 2

# Configuración de la paleta
paleta = tk.Canvas(ventana, width=80, height=10)
paleta.create_rectangle(0, 0, 80, 10, fill="blue")
paleta.pack()

# Posición inicial de la paleta
paleta_x = 210

# Mover la paleta
def mover_paleta(event):
    global paleta_x
    tecla = event.keysym
    if tecla == "Left" and paleta_x > 0:
        paleta_x -= 10
    elif tecla == "Right" and paleta_x < 420:
        paleta_x += 10
    paleta.place(x=paleta_x, y=350)

# Configuración de los bloques
bloques = []
for i in range(5):
    for j in range(3):
        x = i * 100
        y = j * 30
        bloque = tk.Canvas(ventana, width=80, height=20)
        bloque.create_rectangle(0, 0, 80, 20, fill="green")
        bloque.place(x=x, y=y)
        bloques.append((bloque, x, y))

# Colisiones
def colision():
    global pelota_x, pelota_y, dx, dy
    if pelota_x + dx < 0 or pelota_x + dx > 480:
        dx = -dx
    if pelota_y + dy < 0 or (pelota_y + dy > 350 and paleta_x < pelota_x < paleta_x + 80):
        dy = -dy

def colision_bloques():
    global pelota_x, pelota_y, dx, dy
    for bloque, x, y in bloques:
        if pelota_x + dx > x and pelota_x + dx < x + 80 and pelota_y + dy > y and pelota_y + dy < y + 20:
            dy = -dy
            bloque.config(fill="white")  # Cambia el color del bloque al golpearlo
            bloque.update()
            ventana.update()
            ventana.after(200, lambda b=bloque: b.destroy())  # Destruye el bloque después de un breve tiempo
            bloques.remove((bloque, x, y))
            actualizar_contador()

# Contador
contador = 0  # Inicializar el contador
contador_label = tk.Label(ventana, text="Contador: 0", font=("Helvetica", 12))
contador_label.pack()

def actualizar_contador():
    global contador
    contador += 1
    contador_label.config(text=f"Contador: {contador}")

# Mover la pelota
def mover_pelota():
    global pelota_x, pelota_y, dx, dy
    pelota_x += dx
    pelota_y += dy
    pelota.place(x=pelota_x, y=pelota_y)
    colision()
    colision_bloques()
    ventana.after(10, mover_pelota)

# Configurar movimiemtos
ventana.bind("<Left>", mover_paleta)
ventana.bind("<Right>", mover_paleta)

# Iniciar el juego
mover_pelota()

# Agregar estas líneas para ejecutar el juego
ventana.mainloop()
