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


# Función para completar la ruta usando A*
def completar_ruta(n_filas, n_columnas, perlas, ruta_actual):
    if not ruta_actual:
        return None

    inicio = ruta_actual[0]
    meta = ruta_actual[-1]

    # Inicialización de estructuras de A*
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
            tentative_g_score = g_score[actual] + 1

            if vecino not in g_score or tentative_g_score < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = tentative_g_score
                f_score[vecino] = tentative_g_score + distancia_manhattan(*vecino, *meta)
                heapq.heappush(open_set, (f_score[vecino], vecino))

    return ruta_actual  # Devuelve la ruta más larga encontrada si no encuentra la solución


# Función para reconstruir el camino desde la meta hasta el inicio
def reconstruir_camino(came_from, actual):
    total_path = [actual]
    while actual in came_from:
        actual = came_from[actual]
        total_path.append(actual)
    return total_path[::-1]