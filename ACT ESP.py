class Articulo: 
 
    def __init__(self, nombre, cantidad, precio): 
 
        self.nombre = nombre 
        self.cantidad = cantidad 
        self.precio = precio 
 
    def __str__(self): 
        return f" Se cuenta con: {self.nombre} y hay un total de {self.cantidad} piezas " 
 
class Inventario: 
    def __init__(self): 
 
        self.articulos = [] 
 
    def agregar_articulo(self, articulo): 
        self.articulos.append(articulo) 
        print(f"Artículo '{articulo.nombre}' agregado.") 
 
    def mostrar_inventario(self):
        if self.articulos: 
             
            print("Inventario actual:") 
            for articulo in self.articulos:  
                print(articulo) 
        else: 
            print("El inventario está vacío.") 
 
    def ventas(self, nombre, cantidad): 
         
        for articulo in self.articulos: 
             
            if articulo.nombre.casefold() == nombre.casefold(): 
                if articulo.cantidad >= cantidad: 
                    articulo.cantidad -= cantidad 
                    print(f"Venta realizada: {cantidad} {articulo.nombre}(s) por ${articulo.precio * cantidad}.") 
                 
                else: 
                    print("No hay suficiente cantidad.") 
                 
                return 
        print("No se encontró el producto.") 
 
    def valor_total(self): 

        total = sum(a.precio * a.cantidad for a in self.articulos) 
        print(f"\nValor total del inventario: ${total}") 
 
 
def main(): 
    inventario = Inventario() 
 
    productos = [ 
        ("manzana", 10, 5), 
        ("melon", 5, 10), 
        ("leche", 20, 25), 
        ("jabón", 7, 10), 
        ("papel higienico", 15, 30), 
        ("chicles", 12, 1) 
    ] 
 
    for nombre, cantidad, precio in productos: 
        inventario.agregar_articulo(Articulo(nombre, cantidad, precio)) 
 
 
    while True: 
 
        print("1. Ver inventario")  
        print("2. Agregar Artículo") 
        print("3. Realizar Venta") 
        print("4. Valor Total del Inventario")   
        print("5. Salir")      
        opcion = input("Seleccione opción: ") 
 
        if opcion == "1": 
            inventario.mostrar_inventario() 
         
        elif opcion == "2": 
            nombre = input("Nombre: ") 
            cantidad = int(input("Cantidad: ")) 
            precio = float(input("Precio: ")) 
            inventario.agregar_articulo(Articulo(nombre, cantidad, precio)) 
         
        elif opcion == "3": 
            nombre = input("Nombre del producto: ") 
            cantidad = int(input("Cantidad: ")) 
            inventario.ventas(nombre, cantidad) 
         
        elif opcion == "4": 
         
            inventario.valor_total() 
         
        elif opcion == "5": 
            print("Saliendo...") 
            break 
         
        else: 
            print("Opción no válida.") 
 
if __name__ == "__main__": 
 main() 