import hashlib
import itertools
import string

def hash_sha256(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

class TablaHash:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]
        self.colisiones = 0

    # Función hash basada en ASCII
    def funcion_hash(self, cadena):
        return sum(ord(c) for c in cadena) % self.tamaño

    def insertar(self, correo, nombre, contraseña):
        indice = self.funcion_hash(correo)
        bucket = self.tabla[indice]

        # Verificar si existe
        for elemento in bucket:
            if elemento["correo"] == correo:
                print("Ya existe un usuario con ese correo.")
                return

        if len(bucket) > 0:
            self.colisiones += 1

        # Guardar contraseña como SHA-256
        elemento = {
            "correo": correo,
            "nombre": nombre,
            "hash_contraseña": hash_sha256(contraseña)
        }

        bucket.append(elemento)
        print("Usuario registrado correctamente.")

    def buscar(self, correo):
        indice = self.funcion_hash(correo)
        bucket = self.tabla[indice]

        for elemento in bucket:
            if elemento["correo"] == correo:
                return elemento
        return None

    def verificar_contraseña(self, correo, contraseña):
        usuario = self.buscar(correo)
        if not usuario:
            return False

        return usuario["hash_contraseña"] == hash_sha256(contraseña)


# -------------------------------
#   FUERZA BRUTA EDUCATIVA
# -------------------------------
def fuerza_bruta(hash_objetivo):
    caracteres = string.ascii_lowercase  # Solo letras minúsculas
    print("\nIntentando descubrir una contraseña SIMPLE de 1 a 3 letras...\n")

    for longitud in range(1, 4):
        for intento in itertools.product(caracteres, repeat=longitud):
            candidato = "".join(intento)
            if hash_sha256(candidato) == hash_objetivo:
                print(f"✔ Contraseña encontrada (solo demostración): {candidato}")
                return
    print("No se pudo encontrar la contraseña (era muy fuerte).")

tabla = TablaHash(10)

while True:
    print("\n===== MENÚ =====")
    print("1. Registrar usuario")
    print("2. Buscar usuario")
    print("3. Verificar contraseña")
    print("4. Fuerza bruta DEMOSTRATIVA (solo hashes simples)")
    print("5. Mostrar colisiones")
    print("6. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        correo = input("Correo: ")
        nombre = input("Nombre: ")
        contraseña = input("Contraseña: ")
        tabla.insertar(correo, nombre, contraseña)

    elif opcion == "2":
        correo = input("Correo a buscar: ")
        usuario = tabla.buscar(correo)
        if usuario:
            print("Usuario encontrado:")
            print(usuario)
        else:
            print("No existe ese usuario.")

    elif opcion == "3":
        correo = input("Correo: ")
        contraseña = input("Contraseña: ")
        if tabla.verificar_contraseña(correo, contraseña):
            print("Contraseña correcta.")
        else:
            print("Contraseña incorrecta.")

    elif opcion == "4":
        print("\n=== DEMOSTRACIÓN DE FUERZA BRUTA ===")
        texto = input("Ingresa una contraseña sencilla (solo minúsculas, 1-3 letras): ")
        h = hash_sha256(texto)
        print(f"Hash generado: {h}")
        fuerza_bruta(h)

    elif opcion == "5":
        print(f"Colisiones registradas: {tabla.colisiones}")

    elif opcion == "6":
        break

    else:
        print("Opción inválida.")