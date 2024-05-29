import heapq

# Función heurística basada en la distancia de Manhattan
def distancia_manhattan(fila1, columna1, fila2, columna2):
    return abs(fila1 - fila2) + abs(columna1 - columna2)

# Función para obtener los vecinos de una posición
def obtener_vecinos(fila, columna, n_filas, n_columnas):
    vecinos = []
    if fila > 0:
        vecinos.append((fila - 1, columna))
    if fila < n_filas - 1:
        vecinos.append((fila + 1, columna))
    if columna > 0:
        vecinos.append((fila, columna - 1))
    if columna < n_columnas - 1:
        vecinos.append((fila, columna + 1))
    return vecinos

# Función para encontrar la ruta entre dos puntos específicos usando A*
def encontrar_ruta(inicio, meta, n_filas, n_columnas, ruta_existente):
    open_set = []
    heapq.heappush(open_set, (0, inicio))
    came_from = {}
    g_score = {inicio: 0}
    f_score = {inicio: distancia_manhattan(*inicio, *meta)}

    while open_set:
        _, actual = heapq.heappop(open_set)

        if actual == meta:
            return reconstruir_camino(came_from, actual)

        for vecino in obtener_vecinos(*actual, n_filas, n_columnas):
            if vecino in ruta_existente:
                continue
            tentative_g_score = g_score[actual] + 1

            if vecino not in g_score or tentative_g_score < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = tentative_g_score
                f_score[vecino] = tentative_g_score + distancia_manhattan(*vecino, *meta)
                heapq.heappush(open_set, (f_score[vecino], vecino))

    return None  # No se encontró una ruta

# Función para completar la ruta pasando por todas las perlas
def completar_ruta(n_filas, n_columnas, perlas, ruta_actual):
    if not ruta_actual:
        return None

    puntos_clave = ruta_actual[:]  # Copia de la ruta actual
    perlas_ordenadas = sorted(perlas, key=lambda p: distancia_manhattan(p[0], p[1], ruta_actual[-1][0], ruta_actual[-1][1]))
    puntos_clave += [(p[0] - 1, p[1] - 1) for p in perlas_ordenadas if (p[0] - 1, p[1] - 1) not in puntos_clave]
    puntos_clave.append(ruta_actual[0])  # Añadir el inicio como meta final

    ruta_completa = []
    for i in range(len(puntos_clave) - 1):
        parte_ruta = encontrar_ruta(puntos_clave[i], puntos_clave[i + 1], n_filas, n_columnas, ruta_completa)
        if parte_ruta:
            ruta_completa += parte_ruta[1:]  # Evitar duplicar el punto de inicio de la siguiente parte
        else:
            return None  # Si no se encuentra una parte de la ruta, falla

    return ruta_completa

# Función para reconstruir el camino desde la meta hasta el inicio
def reconstruir_camino(came_from, actual):
    total_path = [actual]
    while actual in came_from:
        actual = came_from[actual]
        total_path.append(actual)
    return total_path[::-1]