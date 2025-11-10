from collections import deque
import random

class Cola:
    def __init__(self):
        self.items = deque()

    def esta_vacia(self):
        return len(self.items) == 0

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.popleft()
        else:
            return None

    def tamaño(self):
        return len(self.items)

    def __str__(self):
        return str(list(self.items))

def sumar_colas(cola1, cola2):
    resultado = Cola()
    while not cola1.esta_vacia() and not cola2.esta_vacia():
        a = cola1.desencolar()
        b = cola2.desencolar()
        suma = a + b
        print(f"Sumando {a} + {b} = {suma}")  
        resultado.encolar(suma)
    return resultado

colaA = Cola()
colaB = Cola()

for _ in range(5):
    colaA.encolar(random.randint(1, 20))
    colaB.encolar(random.randint(1, 20))

print("Cola A inicial:", colaA)
print("Cola B inicial:", colaB)

colaResultado = sumar_colas(colaA, colaB)
print("Cola Resultado:", colaResultado)
