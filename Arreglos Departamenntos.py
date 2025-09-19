import numpy as np
import pandas as pd

class Ventas:
    def __init__(self):
        self.departamentos = ["Ropa", "Deportes", "Juguetería"]
        self.meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        #Generar arreglo con valores aleatorios entre 100 y 5000
        self.ventas = np.random.randint(100, 5000, size=(len(self.departamentos), len(self.meses)))

    def insertar_venta(self, depto, mes, monto):
        """ Inserta o actualiza una venta """
        try:
            d_index = self.departamentos.index(depto)
            m_index = self.meses.index(mes)
            self.ventas[d_index, m_index] = monto
            print(f"Venta registrada/modificada: {depto} - {mes} = {monto}")
        except ValueError:
            print("Error: Departamento o mes no válido.")

    def buscar_venta(self, depto, mes):
        """ Busca una venta """
        try:
            d_index = self.departamentos.index(depto)
            m_index = self.meses.index(mes)
            venta = self.ventas[d_index, m_index]
            print(f"Venta encontrada: {depto} - {mes} = {venta}")
            return venta
        except ValueError:
            print("Error: Departamento o mes no válido.")
            return None

    def eliminar_venta(self, depto, mes):
        """ Elimina una venta (pone en 0) """
        try:
            d_index = self.departamentos.index(depto)
            m_index = self.meses.index(mes)
            self.ventas[d_index, m_index] = 0
            print(f"Venta eliminada: {depto} - {mes}")
        except ValueError:
            print("Error: Departamento o mes no válido.")

    def mostrar_tabla(self):
        """ Muestra la tabla completa """
        df = pd.DataFrame(self.ventas, index=self.departamentos, columns=self.meses)
        print("\nReporte de Ventas:")
        print(df)
        return df

# PROGRAMA PRINCIPAL CON MENÚ
if __name__ == "__main__":
    sistema = Ventas()

    while True:
        print("\n===== MENÚ DE OPCIONES =====")
        print("1. Mostrar tabla de ventas")
        print("2. Insertar/Modificar venta")
        print("3. Buscar venta")
        print("4. Eliminar venta")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            sistema.mostrar_tabla()

        elif opcion == "2":
            depto = input("Departamento (Ropa, Deportes, Juguetería): ")
            mes = input("Mes (Enero-Diciembre): ")
            try:
                monto = int(input("Monto de la venta: "))
                sistema.insertar_venta(depto, mes, monto)
            except ValueError:
                print("El monto debe ser un número.")

        elif opcion == "3":
            depto = input("Departamento (Ropa, Deportes, Juguetería): ")
            mes = input("Mes (Enero-Diciembre): ")
            sistema.buscar_venta(depto, mes)

        elif opcion == "4":
            depto = input("Departamento (Ropa, Deportes, Juguetería): ")
            mes = input("Mes (Enero-Diciembre): ")
            sistema.eliminar_venta(depto, mes)

        elif opcion == "5":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")