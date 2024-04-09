import tkinter as tk
from tkinter import filedialog, Canvas

# Variables globales
canvas = None
tamano_celda = 50
linea_actual = None  # Para almacenar la referencia de la línea que se está dibujando


def cargar_tablero():
    global canvas
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filepath:
        return

    with open(filepath, 'r') as file:
        lineas = file.readlines()
        tamano_tablero = int(lineas[0].strip())
        perlas = [list(map(int, linea.strip().split(','))) for linea in lineas[1:]]

    if canvas is not None:
        canvas.destroy()
    canvas = Canvas(root, width=tamano_tablero * tamano_celda, height=tamano_tablero * tamano_celda, bg="#8B4513")
    canvas.pack()
    canvas.bind("<B1-Motion>", dibujar_linea)  # Evento para cuando se mueva el mouse con el botón izquierdo presionado
    canvas.bind("<ButtonRelease-1>", finalizar_linea)  # Evento para cuando se suelte el botón izquierdo del mouse

    dibujar_tablero(tamano_tablero, perlas)


def dibujar_tablero(tamano, perlas):
    for fila in range(tamano):
        for columna in range(tamano):
            x1 = columna * tamano_celda
            y1 = fila * tamano_celda
            x2 = x1 + tamano_celda
            y2 = y1 + tamano_celda
            canvas.create_rectangle(x1, y1, x2, y2, fill="#DEB887", outline="black", width=2)

    for perla in perlas:
        fila, columna, tipo = perla
        centro_x = (columna - 1) * tamano_celda + tamano_celda // 2
        centro_y = (fila - 1) * tamano_celda + tamano_celda // 2
        if tipo == 1:
            color_fondo = "white"
            color_borde = "gray"
        else:
            color_fondo = "black"
            color_borde = "black"
        canvas.create_oval(centro_x - 20, centro_y - 20, centro_x + 20, centro_y + 20, fill=color_fondo,
                           outline=color_borde, width=2)
        if tipo == 1:
            canvas.create_arc(centro_x - 20, centro_y - 20, centro_x + 20, centro_y + 20, start=45, extent=180,
                              style=tk.ARC, outline="gray", width=2)


def dibujar_linea(event):
    global linea_actual
    x, y = event.x, event.y
    if not linea_actual:
        linea_actual = canvas.create_line(x, y, x, y, fill="red", width=2)
    else:
        coords = canvas.coords(linea_actual)
        coords[-2:] = [x, y]  # Actualizar la posición final de la línea actual
        canvas.coords(linea_actual, *coords)


def finalizar_linea(event):
    global linea_actual
    linea_actual = None  # Resetear la línea actual para empezar una nueva la próxima vez


root = tk.Tk()
root.title("Juego de Maysu")

btn_cargar = tk.Button(root, text="Cargar Tablero", command=cargar_tablero)
btn_cargar.pack()

root.mainloop()
