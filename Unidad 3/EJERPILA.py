class Pila:
    def __init__(self):
        self.elementos = []

    # Apilar (push)
    def push(self, elemento):
        self.elementos.append(elemento)
        print(f"{elemento} agregado a la pila.")

    # Desapilar (pop)
    def pop(self):
        if not self.esta_vacia():
            elemento = self.elementos.pop()
            print(f"{elemento} eliminado de la pila.")
            return elemento
        else:
            print("La pila está vacía, no se puede desapilar.")
            return None

    # Ver el tope de la pila (peek)
    def peek(self):
        if not self.esta_vacia():
            return self.elementos[-1]
        else:
            return None

    # Verificar si está vacía
    def esta_vacia(self):
        return len(self.elementos) == 0

    # Mostrar pila completa
    def mostrar(self):
        print("Pila:", self.elementos)


# Programa principal
if __name__ == "__main__":
    pila = Pila()

    pila.push(10)
    pila.push(20)
    pila.push(30)
    pila.mostrar()

    print("Elemento en el tope:", pila.peek())

    pila.pop()
    pila.mostrar()

    pila.pop()
    pila.pop()
    pila.pop()  # Intento extra cuando ya está vacía