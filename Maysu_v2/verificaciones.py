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
    indices = [i for i, punto in enumerate(linea) if punto == (fila, columna)]
    if len(indices) != 1:
        return False
    indice = indices[0]
    if indice == 0 or indice == len(linea) - 1:
        return False
    y1, x1 = linea[indice - 1]
    y2, x2 = linea[indice + 1]

    if not ((y1 == fila and x2 == columna and abs(x1 - columna) == 1 and abs(y2 - fila) == 1) or
            (x1 == columna and y2 == fila and abs(y1 - fila) == 1 and abs(x2 - columna) == 1)):
        return False

    if indice + 2 < len(linea):
        y3, x3 = linea[indice + 2]
        if (y2 == fila and x2 != columna and y3 != fila) or (x2 == columna and y2 != fila and x3 != columna):
            return False

    return True

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