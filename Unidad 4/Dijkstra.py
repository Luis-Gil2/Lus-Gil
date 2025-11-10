import heapq

def dijkstra(grafo, origen):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    cola = [(0, origen)]

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(cola, (distancia, vecino))

    return distancias


# Ejemplo de uso
grafo = {
    'A': {'B': 4, 'C': 2},
    'B': {'C': 5, 'D': 10},
    'C': {'E': 3},
    'D': {'F': 11},
    'E': {'D': 4},
    'F': {}
}

print("Distancias mínimas desde A:", dijkstra(grafo, 'A'))