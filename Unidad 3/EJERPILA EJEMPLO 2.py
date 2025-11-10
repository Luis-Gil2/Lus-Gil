class Pila:
    def __init__(self):
        self.elementos = []

    def push(self, elemento):
        self.elementos.append(elemento)
        print(f"{elemento} agregado a la pila.")

    def pop(self):
        if not self.esta_vacia():
            elemento = self.elementos.pop()
            print(f"{elemento} eliminado de la pila.")
            return elemento
        else:
            print("La pila está vacía, no se puede desapilar.")
            return None

    def peek(self):
        if not self.esta_vacia():
            return self.elementos[-1]
        else:
            return None

    def esta_vacia(self):
        return len(self.elementos) == 0

    def mostrar(self):
        if self.esta_vacia():
            print("La pila está vacía.")
        else:
            print("Pila:", self.elementos)

if __name__ == "__main__":
    pila = Pila()

    while True:
        print("\n--- MENÚ DE PILA ---")
        print("1. Apilar (push)")
        print("2. Desapilar (pop)")
        print("3. Ver tope (peek)")
        print("4. Mostrar pila")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            valor = input("Ingresa el valor a apilar: ")
            pila.push(valor)

        elif opcion == "2":
            pila.pop()

        elif opcion == "3":
            tope = pila.peek()
            if tope is not None:
                print(f"Elemento en el tope: {tope}")
            else:
                print("La pila está vacía.")

        elif opcion == "4":
            pila.mostrar()

        elif opcion == "5":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")