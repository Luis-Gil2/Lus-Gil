class UnionFind:
    def __init__(self, n):
        self.padre = list(range(n))

    def encontrar(self, i):
        if self.padre[i] != i:
            self.padre[i] = self.encontrar(self.padre[i])
        return self.padre[i]

    def unir(self, i, j):
        raiz_i = self.encontrar(i)
        raiz_j = self.encontrar(j)
        if raiz_i != raiz_j:
            self.padre[raiz_j] = raiz_i


def kruskal(n, aristas):
    aristas.sort(key=lambda x: x[2])
    uf = UnionFind(n)
    mst = []

    for u, v, peso in aristas:
        if uf.encontrar(u) != uf.encontrar(v):
            uf.unir(u, v)
            mst.append((u, v, peso))

    return mst


# Ejemplo
n = 4
aristas = [
    (0, 1, 10),
    (0, 2, 6),
    (0, 3, 5),
    (1, 3, 15),
    (2, 3, 4)
]

mst = kruskal(n, aristas)
print("Aristas del árbol de expansión mínima:", mst)