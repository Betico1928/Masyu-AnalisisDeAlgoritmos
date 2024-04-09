import tkinter as tk
from tkinter import filedialog, Canvas, messagebox

# Variables globales para el canvas, el tamaño de cada celda, la última posición clickada y la ruta
canvas = None
tamano_celda = 50
ultima_pos_click = None
ruta = []  # Almacenará la ruta como una lista de tuplas (fila, columna)
perlas = []  # Almacenará las posiciones de las perlas


def cargar_tablero():
    global canvas, ultima_pos_click, ruta, perlas
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
    canvas.bind("<Button-1>", click_en_tablero)

    ultima_pos_click = None
    ruta = []
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
        if tipo == 1:  # Perla blanca
            color_fondo = "white"
            color_borde = "gray"
        else:  # Perla negra
            color_fondo = "black"
            color_borde = "black"
        # Dibujar la perla con un efecto tridimensional
        canvas.create_oval(centro_x - 20, centro_y - 20, centro_x + 20, centro_y + 20, fill=color_fondo,
                           outline=color_borde, width=2)
        # Sombreado para el efecto tridimensional
        if tipo == 1:  # Sólo las perlas blancas necesitan un sombreado visible
            canvas.create_arc(centro_x - 20, centro_y - 20, centro_x + 20, centro_y + 20, start=45, extent=180,
                              style=tk.ARC, outline="gray", width=2)

def click_en_tablero(event):
    global ultima_pos_click, ruta
    columna = event.x // tamano_celda + 1
    fila = event.y // tamano_celda + 1
    if ultima_pos_click:
        dibujar_linea(ultima_pos_click, (fila, columna))
        ruta.append((fila, columna))
    else:
        ruta.append((fila, columna))
    ultima_pos_click = (fila, columna)


def dibujar_linea(pos_inicio, pos_final):
    x_inicio = (pos_inicio[1] - 1) * tamano_celda + tamano_celda // 2
    y_inicio = (pos_inicio[0] - 1) * tamano_celda + tamano_celda // 2
    x_final = (pos_final[1] - 1) * tamano_celda + tamano_celda // 2
    y_final = (pos_final[0] - 1) * tamano_celda + tamano_celda // 2
    canvas.create_line(x_inicio, y_inicio, x_final, y_final, fill="red", width=2)


def verificar_solucion():
    # Verificar que la ruta sea continua
    if not es_ruta_continua(ruta):
        messagebox.showerror("Verificación", "La ruta no es continua.")
        return

    # Verificar que todas las perlas blancas estén en la ruta
    perlas_blancas = {(fila, columna) for fila, columna, tipo in perlas if tipo == 1}
    if not perlas_blancas.issubset(set(ruta)):
        messagebox.showerror("Verificación", "No todas las perlas blancas están en la ruta.")
        return

    # Verificar que la ruta pase al lado de todas las perlas negras sin pasar por ellas
    perlas_negras = {(fila, columna) for fila, columna, tipo in perlas if tipo == 2}
    if not ruta_adyacente_a_perlas_negras(perlas_negras, ruta):
        messagebox.showerror("Verificación", "La ruta no cumple con las condiciones de las perlas negras.")
        return

    messagebox.showinfo("Verificación", "¡La ruta está correcta!")


def es_ruta_continua(ruta):
    for i in range(len(ruta) - 1):
        fila_actual, columna_actual = ruta[i]
        fila_siguiente, columna_siguiente = ruta[i + 1]
        # La ruta es continua si cada paso es adyacente al anterior
        if abs(fila_actual - fila_siguiente) + abs(columna_actual - columna_siguiente) != 1:
            return False
    return True


def ruta_adyacente_a_perlas_negras(perlas_negras, ruta):
    for perla_negra in perlas_negras:
        fila_pn, columna_pn = perla_negra
        adyacente = False
        for fila_r, columna_r in ruta:
            if abs(fila_pn - fila_r) + abs(columna_pn - columna_r) == 1:
                adyacente = True
                break
        # Si alguna perla negra no es adyacente a la ruta, retorna False
        if not adyacente:
            return False
    return True


root = tk.Tk()
root.title("Juego de Maysu")

btn_cargar = tk.Button(root, text="Cargar Tablero", command=cargar_tablero)
btn_cargar.pack()

btn_verificar = tk.Button(root, text="Verificar Solución", command=verificar_solucion)
btn_verificar.pack()

root.mainloop()
