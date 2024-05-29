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

def es_punto_valido(tablero, punto, perlas, ruta):
    y, x = punto
    if tablero[y][x] != 0:
        return False

    # Simular la adición del punto a la ruta
    ruta.append(punto)
    es_valido = True
    for perla in perlas:
        py, px, tipo = perla
        py -= 1
        px -= 1
        if (py, px) == (y, x):
            if tipo == 1 and not verificar_perla_blanca(ruta, py, px):
                es_valido = False
                break
            if tipo == 2 and not verificar_perla_negra(ruta, py, px):
                es_valido = False
                break
    # Eliminar el punto simulado de la ruta
    ruta.pop()
    return es_valido

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

    mejor_ruta = ruta_inicial

    while cola_prioridad:
        _, actual = heapq.heappop(cola_prioridad)

        for vecino in obtener_vecinos(n_filas, n_columnas, actual):
            nueva_ruta = rutas[actual] + [vecino]

            if es_punto_valido(tablero, vecino, perlas, nueva_ruta):
                tablero[vecino[0]][vecino[1]] = 1
                nuevo_costo = costos[actual] + 1
                costos[vecino] = nuevo_costo
                prioridad = nuevo_costo + min(distancia_manhattan(vecino, meta) for meta in metas)
                heapq.heappush(cola_prioridad, (prioridad, vecino))
                rutas[vecino] = nueva_ruta

                if len(nueva_ruta) > len(mejor_ruta):
                    mejor_ruta = nueva_ruta

                # Comprobar si hemos alcanzado la meta
                if all(any(punto == meta for punto in nueva_ruta) for meta in metas):
                    return nueva_ruta

    return mejor_ruta