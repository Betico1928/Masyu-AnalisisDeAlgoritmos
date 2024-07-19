import tkinter as tk
from tkinter import messagebox
from verificaciones import verificar_solucion
from supersolver import completar_ruta

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

    def completar_ruta_automatica(self):
        nueva_ruta = completar_ruta(self.n_filas, self.n_columnas, self.perlas, self.linea_actual)
        if nueva_ruta:
            self.linea_actual = nueva_ruta
            self.dibujar_linea()
            self.imprimir_ruta()
        else:
            messagebox.showinfo("Resultado", "No se encontró una ruta completa, mostrando la mejor ruta encontrada.")
            self.linea_actual = nueva_ruta
            self.dibujar_linea()
            self.imprimir_ruta()

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
            if (x < self.n_columnas - 1):
                self.linea_actual.append((y, x + 1))
                self.dibujar_linea()
                self.imprimir_ruta()

    def dibujar_linea(self):
        self.canvas.delete("linea")
        for i in range(len(self.linea_actual) - 1):
            y1, x1 = self.linea_actual[i]
            y2, x2 = self.linea_actual[i + 1]
            self.canvas.create_line(x1 * 40 + 20, y1 * 40 + 20, x2 * 40 + 20, y2 * 40 + 20, fill="red", width=2, tag="linea")

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



if __name__ == "__main__":
    n_filas, n_columnas, perlas = leer_archivo_entrada('inputt.txt')

    root = tk.Tk()
    root.title("Juego Masyu")
    juego = Masyu(root, n_filas, n_columnas, perlas)
    root.mainloop()