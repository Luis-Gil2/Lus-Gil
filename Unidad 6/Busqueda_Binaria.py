import random

def busqueda_binaria(lista, objetivo):
    inicio = 0
    fin = len(lista) - 1
    pasos = 0

    while inicio <= fin:
        pasos += 1
        medio = (inicio + fin) // 2

        if lista[medio] == objetivo:
            return medio, pasos
        elif lista[medio] < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1

    return -1, pasos

# Se genera una lista ordenada de 1000 números aleatorios sin repetir
lista = sorted(random.sample(range(1, 5000), 1000))
print("Lista generada (primeros 20 elementos):", lista[:20])

num = int(input("Ingresa un número a buscar en la lista: "))

posicion, pasos = busqueda_binaria(lista, num)

if posicion != -1:
    print(f"\nNúmero encontrado en la posición {posicion}")
else:
    print("\nEl número no está en la lista")

print(f"Pasos realizados: {pasos}")
