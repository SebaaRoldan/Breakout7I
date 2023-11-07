import tkinter

#Configuracion de la ventana

ventana.tkinter.Tk()
ventana.geometry("500x500")
ventana.title("Breakout")

#Configuracion de la pelota
pelota = tkinter.Canvas(ventana, width = 20, height = 20)
pelota.create_oval(0, 0, 20, 20, fill = "blue")

#Configuracion de la paleta
paleta = tkinter.Canvas(ventana, width = 80, height = 10)
pelota.create_rectangle(0, 0, 80, 10, fill = "yellow")
xant = 50
yant = 50
paleta.place(x=xant, y=yant)

#Variable
xpos = 5
ypos = 5

#Movimiento
def mover_derecha(event):
    global xpos, xant

    xpos -= 5
    paleta.place(x=xant+xpos)

def mover_izquierda(event):
    global xpos, xant

    xpos += 5
    paleta.place(x=xant+xpos)


#Controles
window.bind("<Left>", mover_derecha)
window.bind("<Right>", mover_izquierda)

ventana.mainloop()




#Otra opcion para mover paleta
def presion_tecla(event):
    global paleta_x
    tecla = event.keysysm
    if tecla == "Left" and paleta_x > 0:
        paleta_x -= 10
    elif tecla == "Right" and paleta_x < 420:
        paleta_x += 10
    paleta.place(x=paleta_x, y=350)

def mover_pelota():
    global pelota_x
    global pelota_y
    pelota_x += dx
    pelota_y += dy
    pelota.place(x=pelota_x, y=paleta_y)
