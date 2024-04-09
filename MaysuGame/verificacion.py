from tkinter import messagebox

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
