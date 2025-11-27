import random
import time

# -------------------------------------------
# MÉTODOS DE ORDENAMIENTO
# -------------------------------------------

def burbuja(arr):
    a = arr.copy()
    n = len(a)
    pasos = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            pasos += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a, pasos


def insercion(arr):
    a = arr.copy()
    pasos = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        pasos += 1
        while j >= 0 and a[j] > key:
            pasos += 1
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a, pasos


def seleccion(arr):
    a = arr.copy()
    pasos = 0
    n = len(a)
    for i in range(n):
        min_idx = i
        pasos += 1
        for j in range(i + 1, n):
            pasos += 1
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a, pasos

# -------------------------------------------
# SIMULACIÓN DE 1000 PASOS
# -------------------------------------------
def simulacion_1000(metodo):
    total_pasos = 0
    total_tiempo = 0

    for _ in range(1000):
        datos = [random.randint(1, 1000) for _ in range(100)]  # lista aleatoria

        inicio = time.time()
        _, pasos = metodo(datos)
        fin = time.time()

        total_pasos += pasos
        total_tiempo += (fin - inicio)

    return total_pasos, total_tiempo


# -------------------------------------------
# MENÚ PRINCIPAL
# -------------------------------------------
def menu():
    while True:
        print("\n========== MÉTODOS DE ORDENAMIENTO ==========")
        print("1. Burbuja")
        print("2. Inserción")
        print("3. Selección")
        print("4. Simulación de 1000 pasos")
        print("5. Salir")
        opcion = input("Elige una opción: ")

        if opcion in ["1","2","3"]:
            lista = [int(x) for x in input("Ingresa números separados por espacios: ").split()]

            if opcion == "1":
                ordenado, pasos = burbuja(lista)
                print("\nResultado:", ordenado)
                print("Pasos realizados:", pasos)

            elif opcion == "2":
                ordenado, pasos = insercion(lista)
                print("\nResultado:", ordenado)
                print("Pasos realizados:", pasos)

            elif opcion == "3":
                ordenado, pasos = seleccion(lista)
                print("\nResultado:", ordenado)
                print("Pasos realizados:", pasos)

        elif opcion == "4":
            print("\n--- Simulación Burbuja ---")
            pasos, tiempo = simulacion_1000(burbuja)
            print(f"Pasos totales: {pasos}")
            print(f"Tiempo total: {tiempo:.4f} s")

            print("\n--- Simulación Inserción ---")
            pasos, tiempo = simulacion_1000(insercion)
            print(f"Pasos totales: {pasos}")
            print(f"Tiempo total: {tiempo:.4f} s")

            print("\n--- Simulación Selección ---")
            pasos, tiempo = simulacion_1000(seleccion)
            print(f"Pasos totales: {pasos}")
            print(f"Tiempo total: {tiempo:.4f} s")

        elif opcion == "5":
            print("Hasta luego 👋")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")


# Ejecutar el menú
menu()
