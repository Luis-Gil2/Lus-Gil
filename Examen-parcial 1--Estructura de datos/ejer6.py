class Terreno:
    def __init__(self, superficie_inicial, generaciones, herederos):
        self.superficie_inicial = superficie_inicial
        self.generaciones = generaciones
        self.herederos = herederos

    def calcular_final(self):
        return self.superficie_inicial / (self.herederos ** self.generaciones)

    def calcular_por_generacion(self):
        superficies = []
        superficie = self.superficie_inicial
        for g in range(self.generaciones + 1):
            superficies.append((g, superficie))
            superficie /= self.herederos
        return superficies

def main():
    superficie_inicial = float(input("Superficie inicial del terreno: "))
    generaciones = int(input("Número de generaciones (máx. 50): "))
    herederos = int(input("Número de herederos por generación: "))

    if generaciones < 0 or generaciones > 50:
        print("El número de generaciones debe estar entre 0 y 50.")
        return
    if herederos <= 0:
        print("El número de herederos debe ser mayor que 0.")
        return

    terreno = Terreno(superficie_inicial, generaciones, herederos)

    final = terreno.calcular_final()
    print(f"\nDespués de {generaciones} generaciones, "
          f"cada heredero recibe: {final:.6f} unidades.")

    print("\n--- Superficie por generación ---")
    for gen, sup in terreno.calcular_por_generacion():
        print(f"Generación {gen}: {sup:.6f} unidades")

if __name__ == "__main__":
    main()