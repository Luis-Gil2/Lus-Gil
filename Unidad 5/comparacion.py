def radix_demo(nums):
    datos = nums[:]   
    print("\n=== RADIX SORT — Trazo completo ===")
    print("Arreglo inicial:", datos)

    def ordenar_por_exp(arreglo, exp):
        n = len(arreglo)
        salida = [0] * n
        cuenta = [0] * 10


        for valor in arreglo:
            dig = (valor // exp) % 10
            cuenta[dig] += 1
        print(f"  Conteos base exp={exp}: {cuenta}")

        for i in range(1, 10):
            cuenta[i] += cuenta[i - 1]
        print(f"  Acumulados exp={exp}: {cuenta}")

        for i in range(n - 1, -1, -1):
            dig = (arreglo[i] // exp) % 10
            pos = cuenta[dig] - 1
            salida[pos] = arreglo[i]
            cuenta[dig] -= 1
            print(f"    Colocando {arreglo[i]} según el dígito {dig}: {salida}")

        return salida

    maximo = max(datos)
    exp = 1
    paso = 1
    while maximo // exp > 0:
        print(f"\n-- Ciclo {paso}: dígito exp={exp} --")
        datos = ordenar_por_exp(datos, exp)
        print("  Resultado parcial:", datos)
        exp *= 10
        paso += 1

    print("\n→ Resultado final RADIX:", datos)
    return datos


def quick_demo(nums):
    arr = nums[:]   
    pivotes_usados = []

    print("\n=== QUICK SORT — ejecución rastreada ===")
    print("Lista inicial:", arr)

    # ------------------- partición -------------------------
    def partir(ini, fin):
        piv = arr[fin]
        pivotes_usados.append(piv)
        print(f"\n  Partición en rango [{ini}, {fin}], pivote:", piv)

        i = ini - 1
        for j in range(ini, fin):
            print(f"    Comparando {arr[j]} con pivote {piv}")
            if arr[j] <= piv:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                print(f"      ↳ Intercambio => {arr}")
            else:
                print("      ↳ Sin movimiento")

        arr[i + 1], arr[fin] = arr[fin], arr[i + 1]
        print(f"  Pivote colocado en {i + 1}: {arr}")
        return i + 1

    # ------------------- quicksort -------------------------
    def ordenar(ini, fin, nivel=0):
        tab = "  " * nivel
        if ini < fin:
            print(tab + f"• quicksort([{ini}, {fin}])")
            piv = partir(ini, fin)
            ordenar(ini, piv - 1, nivel + 1)
            ordenar(piv + 1, fin, nivel + 1)
        else:
            if ini == fin:
                print(tab + f"• elemento solo en índice {ini}, sin acción")
            else:
                print(tab + f"• rango vacío [{ini}, {fin}], continuar")

    ordenar(0, len(arr) - 1)

    print("\n→ Resultado final QUICK:", arr)
    print("Pivotes usados en orden:", pivotes_usados)
    return arr, pivotes_usados


# ---------------------------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------------------------
def main():
    base = [45, 17, 23, 67, 21, 12, 40, 7]
    print("Datos de prueba:", base)

    print("\nEscoge el algoritmo:")
    print("1 - Radix Sort (pasos por cada dígito)")
    print("2 - Quick Sort (comparaciones y pivotes)")
    eleccion = input("Opción: ").strip()

    if eleccion == "1":
        resultado = radix_demo(base)
        print("\nNota: RADIX no utiliza pivotes.")
    elif eleccion == "2":
        ordenada, pivs = quick_demo(base)
        print("\nResumen QUICK:")
        print("  Lista original:", base)
        print("  Ordenada:", ordenada)
        print("  Pivotes:", pivs)
    else:
        print("Opción inválida.")

if __name__ == "__main__":
    main()