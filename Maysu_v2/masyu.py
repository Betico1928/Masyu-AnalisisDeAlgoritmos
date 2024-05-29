import tkinter as tk
from tkinter import messagebox


# Función para leer el archivo de entrada y extraer la configuración del tablero
def leer_archivo_entrada(ruta):
    with open(ruta, 'r') as file:
        lineas = file.readlines()

    n = int(lineas[0].strip())
    perlas = []

    for linea in lineas[1:]:
        fila, columna, tipo = map(int, linea.strip().split(','))
        perlas.append((fila, columna, tipo))

    return n, n, perlas


# Clase para manejar la lógica del juego y la interfaz gráfica
class Masyu:
    def __init__(self, master, n_filas, n_columnas, perlas):
        self.master = master
        self.n_filas = n_filas
        self.n_columnas = n_columnas
        self.perlas = perlas
        self.tablero = [[0 for _ in range(n_columnas)] for _ in range(n_filas)]

        self.canvas = tk.Canvas(master, width=n_columnas * 40, height=n_filas * 40)
        self.canvas.pack()

        self.dibujar_tablero()
        self.dibujar_perlas()

        self.linea_actual = []
        self.lineas_dibujadas = []

        self.canvas.bind("<Button-1>", self.iniciar_linea)
        master.bind("<Up>", self.mover_arriba)
        master.bind("<Down>", self.mover_abajo)
        master.bind("<Left>", self.mover_izquierda)
        master.bind("<Right>", self.mover_derecha)

        self.boton_verificar = tk.Button(master, text="Verificar Solución", command=self.verificar_solucion)
        self.boton_verificar.pack()

        # Agregar el botón para completar la ruta automáticamente
        self.boton_auto = tk.Button(master, text="Completar Ruta", command=self.completar_ruta_automatica)
        self.boton_auto.pack()

    # Método para completar la ruta automáticamente
    def completar_ruta_automatica(self):
        from supersolver import completar_ruta
        nueva_ruta = completar_ruta(self.n_filas, self.n_columnas, self.perlas, self.linea_actual)
        if nueva_ruta:
            self.linea_actual = nueva_ruta
            self.dibujar_linea()
            self.imprimir_ruta()
        else:
            messagebox.showerror("Error", "No se pudo completar la ruta.")


    def dibujar_tablero(self):
        for i in range(self.n_filas):
            for j in range(self.n_columnas):
                self.canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, outline="black")

    def dibujar_perlas(self):
        for fila, columna, tipo in self.perlas:
            x, y = (columna - 1) * 40 + 20, (fila - 1) * 40 + 20
            color = 'white' if tipo == 1 else 'black'
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color, outline="black")

    def iniciar_linea(self, event):
        self.linea_actual = [(event.y // 40, event.x // 40)]
        self.dibujar_linea()
        self.imprimir_ruta()

    def mover_arriba(self, event):
        if self.linea_actual:
            y, x = self.linea_actual[-1]
            if y > 0:
                self.linea_actual.append((y - 1, x))
                self.dibujar_linea()
                self.imprimir_ruta()

    def mover_abajo(self, event):
        if self.linea_actual:
            y, x = self.linea_actual[-1]
            if y < self.n_filas - 1:
                self.linea_actual.append((y + 1, x))
                self.dibujar_linea()
                self.imprimir_ruta()

    def mover_izquierda(self, event):
        if self.linea_actual:
            y, x = self.linea_actual[-1]
            if x > 0:
                self.linea_actual.append((y, x - 1))
                self.dibujar_linea()
                self.imprimir_ruta()

    def mover_derecha(self, event):
        if self.linea_actual:
            y, x = self.linea_actual[-1]
            if x < self.n_columnas - 1:
                self.linea_actual.append((y, x + 1))
                self.dibujar_linea()
                self.imprimir_ruta()

    def dibujar_linea(self):
        self.canvas.delete("linea")
        for i in range(len(self.linea_actual) - 1):
            y1, x1 = self.linea_actual[i]
            y2, x2 = self.linea_actual[i + 1]
            self.canvas.create_line(x1 * 40 + 20, y1 * 40 + 20, x2 * 40 + 20, y2 * 40 + 20, fill="red", width=2,
                                    tag="linea")

    def imprimir_ruta(self):
        print("Ruta actual:", self.linea_actual)

    def verificar_solucion(self):
        es_correcto, errores = verificar_solucion(self.linea_actual, self.perlas)
        if es_correcto:
            messagebox.showinfo("Resultado", "¡Solución correcta!")
        else:
            mensaje_error = "Solución incorrecta. Errores en las celdas:\n" + "\n".join(
                [f"Fila {e[0] + 1}, Columna {e[1] + 1}" for e in errores])
            messagebox.showerror("Resultado", mensaje_error)
            print("Errores en las celdas:", errores)
        # Aquí podrías agregar la lógica para mostrar la ruta correcta si se desea


# Función para verificar si la solución es correcta
def verificar_solucion(linea, perlas):
    errores = []
    if not verificar_linea_continua(linea):
        errores.append(("Línea no continua",))

    for fila, columna, tipo in perlas:
        if tipo == 1:  # Perla blanca
            if not verificar_perla_blanca(linea, fila - 1, columna - 1):
                errores.append((fila - 1, columna - 1))
        elif tipo == 2:  # Perla negra
            if not verificar_perla_negra(linea, fila - 1, columna - 1):
                errores.append((fila - 1, columna - 1))
    return len(errores) == 0, errores


def verificar_linea_continua(linea):
    if len(linea) < 2:
        return False
    for i in range(1, len(linea)):
        y1, x1 = linea[i - 1]
        y2, x2 = linea[i]
        if abs(y1 - y2) + abs(x1 - x2) != 1:
            return False
    return True


def verificar_perla_blanca(linea, fila, columna):
    # Verifica si la línea pasa por la perla blanca de forma recta con giros en las esquinas
    indices = [i for i, punto in enumerate(linea) if punto == (fila, columna)]
    if len(indices) != 1:
        return False
    indice = indices[0]
    if indice == 0 or indice == len(linea) - 1:
        return False
    y1, x1 = linea[indice - 1]
    y2, x2 = linea[indice + 1]
    if (y1 == fila and y2 == fila and x1 != columna and x2 != columna) or (
            x1 == columna and x2 == columna and y1 != fila and y2 != fila):
        return True
    return False


def verificar_perla_negra(linea, fila, columna):
    # Find the index of the black pearl in the line
    indices = [i for i, punto in enumerate(linea) if punto == (fila, columna)]
    
    # If there is not exactly one black pearl, return False
    if len(indices) != 1:
        return False
    
    indice = indices[0]
    
    # Ensure the black pearl is not at the ends of the line
    if indice == 0 or indice == len(linea) - 1:
        return False
    
    # Get the points before and after the black pearl
    y1, x1 = linea[indice - 1]
    y2, x2 = linea[indice + 1]
    
    # Check if the points form a horizontal or vertical line segment with the black pearl
    if (y1 == fila and y2 == fila and (x1 < columna < x2 or x2 < columna < x1)) or \
       (x1 == columna and x2 == columna and (y1 < fila < y2 or y2 < fila < y1)):
        return True
    
    return False


if __name__ == "__main__":
    n_filas, n_columnas, perlas = leer_archivo_entrada('inputt.txt')

    root = tk.Tk()
    root.title("Juego Masyu")
    juego = Masyu(root, n_filas, n_columnas, perlas)
    root.mainloop()