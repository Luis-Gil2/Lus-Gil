def busqueda_producto(inventario, nombre):
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None

inventario = [
    {"id": 101, "nombre": "Laptop", "precio": 15000, "cantidad": 5},
    {"id": 102, "nombre": "Mouse",  "precio": 200,   "cantidad": 20},
    {"id": 103, "nombre": "Teclado", "precio": 350,  "cantidad": 15},
    {"id": 104, "nombre": "Monitor", "precio": 3200, "cantidad": 7},
]

nombre = input("Ingresa el nombre del producto: ")

resultado = busqueda_producto(inventario, nombre)

if resultado:
    print("\nProducto encontrado:")
    for clave, valor in resultado.items():
        print(f"  {clave}: {valor}")
else:
    print("El producto no se encuentra en el inventario.")
