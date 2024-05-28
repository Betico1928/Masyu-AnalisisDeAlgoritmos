from tkinter import messagebox

# Definimos los tipos de celdas y sus restricciones
class Celda:
    def __init__(self, fila, columna, tipo):
        self.fila = fila
        self.columna = columna
        self.tipo = tipo  # 0: vacío, 1: perla blanca, 2: perla negra

# Representación del puzzle de Masyu
class Puzzle:
    def __init__(self, tamano, perlas):
        self.tamano = tamano
        self.grid = [[0] * tamano for _ in range(tamano)]
        self.perlas = {}
        for fila, columna, tipo in perlas:
            self.grid[fila-1][columna-1] = tipo
            self.perlas[(fila-1, columna-1)] = tipo

    def es_valida(self, fila, columna):
        return 0 <= fila < self.tamano and 0 <= columna < self.tamano

    def obtener_tipo(self, fila, columna):
        if not self.es_valida(fila, columna):
            return None
        return self.grid[fila][columna]

# Solucionador del puzzle de Masyu
class SolucionadorMasyu:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Direcciones E, S, W, N
        self.solucion = []

    def resolver(self):
        # Iniciamos la búsqueda desde cada celda del tablero
        for fila in range(self.puzzle.tamano):
            for columna in range(self.puzzle.tamano):
                if self.buscar_ruta(fila, columna, [(fila, columna)], set()):
                    return self.solucion
        return None

    def buscar_ruta(self, fila, columna, ruta, visitadas):
        if len(ruta) > 1 and (fila, columna) == ruta[0] and len(visitadas) == self.puzzle.tamano * self.puzzle.tamano:
            self.solucion = ruta[:]
            return True

        for movimiento in self.movimientos:
            siguiente_fila, siguiente_columna = fila + movimiento[0], columna + movimiento[1]
            if self.puzzle.es_valida(siguiente_fila, siguiente_columna) and (siguiente_fila, siguiente_columna) not in visitadas:
                tipo_actual = self.puzzle.obtener_tipo(fila, columna)
                if tipo_actual == 1:  # Perla blanca
                    if len(ruta) > 1 and ruta[-2] != (siguiente_fila, siguiente_columna):
                        continue
                elif tipo_actual == 2:  # Perla negra
                    if len(ruta) > 1 and not self.es_giro(ruta[-2], (fila, columna), (siguiente_fila, siguiente_columna)):
                        continue

                ruta.append((siguiente_fila, siguiente_columna))
                visitadas.add((siguiente_fila, siguiente_columna))
                if self.buscar_ruta(siguiente_fila, siguiente_columna, ruta, visitadas):
                    return True
                ruta.pop()
                visitadas.remove((siguiente_fila, siguiente_columna))
        return False

    def es_giro(self, anterior, actual, siguiente):
        return (anterior[0] != actual[0] and siguiente[0] != actual[0]) or (anterior[1] != actual[1] and siguiente[1] != actual[1])

def verificar_solucion(ruta, perlas):
    if not es_ruta_continua(ruta):
        messagebox.showerror("Verificación", "La ruta no es continua.")
        return False

    perlas_blancas = {(fila, columna) for fila, columna, tipo in perlas if tipo == 1}
    if not perlas_blancas.issubset(set(ruta)):
        messagebox.showerror("Verificación", "No todas las perlas blancas están en la ruta.")
        return False

    perlas_negras = {(fila, columna) for fila, columna, tipo in perlas if tipo == 2}
    if not ruta_adyacente_a_perlas_negras(perlas_negras, ruta):
        messagebox.showerror("Verificación", "La ruta no cumple con las condiciones de las perlas negras.")
        return False

    messagebox.showinfo("Verificación", "¡La ruta está correcta!")
    return True

def es_ruta_continua(ruta):
    for i in range(len(ruta) - 1):
        fila_actual, columna_actual = ruta[i]
        fila_siguiente, columna_siguiente = ruta[i + 1]
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
        if not adyacente:
            return False
    return True

def resolver_puzzle(perlas, tamano_tablero):
    print("Resolviendo el puzzle...")
    puzzle = Puzzle(tamano_tablero, perlas)
    solucionador = SolucionadorMasyu(puzzle)
    ruta = solucionador.resolver()
    if ruta:
        print("Puzzle resuelto.")
        return ruta
    else:
        print("No se encontró una solución.")
        return None