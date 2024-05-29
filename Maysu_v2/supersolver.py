import heapq


# Definición de las reglas del juego Masyu
def es_valido(fila, columna, n_filas, n_columnas, visitados):
    return 0 <= fila < n_filas and 0 <= columna < n_columnas and (fila, columna) not in visitados


# Heurística de Manhattan
def distancia_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Algoritmo A* para encontrar la ruta
def a_star(n_filas, n_columnas, perlas, inicio, fin):
    open_set = []
    heapq.heappush(open_set, (0, inicio))
    came_from = {}
    g_score = {inicio: 0}
    f_score = {inicio: distancia_manhattan(inicio, fin)}
    visitados = set([inicio])

    while open_set:
        _, actual = heapq.heappop(open_set)

        if actual == fin:
            return reconstruir_camino(came_from, actual)

        for vecino in obtener_vecinos(actual, n_filas, n_columnas, visitados):
            tentative_g_score = g_score[actual] + 1

            if vecino not in g_score or tentative_g_score < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = tentative_g_score
                f_score[vecino] = tentative_g_score + distancia_manhattan(vecino, fin)
                heapq.heappush(open_set, (f_score[vecino], vecino))
                visitados.add(vecino)

    return []


def obtener_vecinos(posicion, n_filas, n_columnas, visitados):
    y, x = posicion
    vecinos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
    return [(ny, nx) for ny, nx in vecinos if es_valido(ny, nx, n_filas, n_columnas, visitados)]


def reconstruir_camino(came_from, actual):
    total_path = [actual]
    while actual in came_from:
        actual = came_from[actual]
        total_path.append(actual)
    return total_path[::-1]


# Función para completar la ruta utilizando A*
def completar_ruta(n_filas, n_columnas, perlas, ruta_parcial):
    inicio = ruta_parcial[-1]
    fin = ruta_parcial[0]
    visitados = set(ruta_parcial)

    # Asegurarse de pasar por todas las perlas
    perlas_no_visitadas = [(fila - 1, columna - 1) for fila, columna, _ in perlas if
                           (fila - 1, columna - 1) not in visitados]

    if not perlas_no_visitadas:
        return a_star(n_filas, n_columnas, perlas, inicio, fin)

    # Incluir todas las perlas en la ruta
    for perla in perlas_no_visitadas:
        camino_hasta_perla = a_star(n_filas, n_columnas, perlas, inicio, perla)
        if camino_hasta_perla:
            ruta_parcial += camino_hasta_perla[1:]
            visitados.update(camino_hasta_perla[1:])
            inicio = perla

    # Finalmente, volver al punto de inicio
    ruta_hasta_inicio = a_star(n_filas, n_columnas, perlas, inicio, fin)
    if ruta_hasta_inicio:
        ruta_parcial += ruta_hasta_inicio[1:]

    return ruta_parcial


# Ejemplo de uso
if __name__ == "__main__":
    n_filas = 10
    n_columnas = 10
    perlas = [
        (1, 3, 1), (1, 5, 1), (2, 5, 1), (2, 9, 2), (3, 3, 2),
        (3, 5, 2), (3, 7, 1), (4, 4, 1), (4, 7, 1), (5, 1, 2),
        (5, 6, 1), (5, 10, 1), (6, 3, 1), (6, 8, 1), (7, 3, 2),
        (7, 7, 1), (8, 1, 1), (8, 5, 2), (8, 10, 1), (9, 7, 1),
        (9, 8, 1), (10, 3, 2), (10, 10, 2)
    ]
    ruta_parcial = [(0, 0), (0, 1), (0, 2)]  # Ejemplo de ruta parcial

    ruta_completa = completar_ruta(n_filas, n_columnas, perlas, ruta_parcial)
    print("Ruta completa:", ruta_completa)