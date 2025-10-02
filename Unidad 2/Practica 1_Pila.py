CAPACIDAD_MAX = 8
pila = []
tope = 0  

def mostrar_pila():
    print("PILA:", pila, f"   TOPE={tope}")
    print("-" * 40)

def insertar(valor):
    global tope
    if tope < CAPACIDAD_MAX:
        pila.append(valor)
        tope += 1
        print(f"Insertar({valor})")
    else:
        print(f"ERROR: Desbordamiento (overflow) al intentar insertar {valor}")
    mostrar_pila()

def eliminar(nombre_variable):
    global tope
    if tope > 0:
        valor = pila.pop()
        tope -= 1
        print(f"Eliminar({nombre_variable}) → {nombre_variable} = {valor}")
    else:
        print(f"ERROR: Subdesbordamiento (underflow), pila vacía al intentar eliminar {nombre_variable}")
    mostrar_pila()

insertar("X")
insertar("Y")
eliminar("Z")
eliminar("T")
eliminar("U")
insertar("V")
insertar("W")
eliminar("p")
insertar("R")

print("=== RESULTADO FINAL ===")
print("PILA:", pila)
print("Elementos en la pila:", tope)