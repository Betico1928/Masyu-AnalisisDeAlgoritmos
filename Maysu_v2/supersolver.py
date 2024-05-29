import heapq
from verificaciones import verificar_linea_continua, verificar_perla_blanca, verificar_perla_negra

def distancia_manhattan(punto1, punto2):
    return abs(punto1[0] - punto2[0]) + abs(punto1[1] - punto2[1])

def obtener_vecinos(n_filas, n_columnas, punto):
    vecinos = []
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for movimiento in movimientos:
        nuevo_punto = (punto[0] + movimiento[0], punto[1] + movimiento[1])
        if 0 <= nuevo_punto[0] < n_filas and 0 <= nuevo_punto[1] < n_columnas:
            vecinos.append(nuevo_punto)
    return vecinos

def es_punto_valido(tablero, punto, perlas):
    y, x = punto
    if tablero[y][x] != 0:
        return False
    for perla in perlas:
        if perla[0] == y + 1 and perla[1] == x + 1:
            return True
    return True

def verificar_solucion_parcial(linea, perlas):
    for fila, columna, tipo in perlas:
        if tipo == 1:  # Perla blanca
            if not verificar_perla_blanca(linea, fila - 1, columna - 1):
                return False
        elif tipo == 2:  # Perla negra
            if not verificar_perla_negra(linea, fila - 1, columna - 1):
                return False
    return True

def completar_ruta(n_filas, n_columnas, perlas, ruta_inicial):
    # Inicializar el tablero con la ruta inicial
    tablero = [[0 for _ in range(n_columnas)] for _ in range(n_filas)]
    for y, x in ruta_inicial:
        tablero[y][x] = 1

    # Inicializar los nodos de inicio y fin
    inicio = ruta_inicial[-1]
    metas = [(perla[0] - 1, perla[1] - 1) for perla in perlas]

    # Cola de prioridad para el algoritmo A*
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, inicio))

    # Diccionarios para rastrear costos y rutas
    costos = {inicio: 0}
    rutas = {inicio: ruta_inicial}

    while cola_prioridad:
        _, actual = heapq.heappop(cola_prioridad)

        if actual in metas:
            ruta_completa = rutas[actual]
            if verificar_solucion_parcial(ruta_completa, perlas):
                return ruta_completa

        for vecino in obtener_vecinos(n_filas, n_columnas, actual):
            nuevo_costo = costos[actual] + 1
            nueva_ruta = rutas[actual] + [vecino]
            if vecino not in costos or nuevo_costo < costos[vecino]:
                if es_punto_valido(tablero, vecino, perlas):
                    costos[vecino] = nuevo_costo
                    prioridad = nuevo_costo + min(distancia_manhattan(vecino, meta) for meta in metas)
                    heapq.heappush(cola_prioridad, (prioridad, vecino))
                    rutas[vecino] = nueva_ruta

    return None