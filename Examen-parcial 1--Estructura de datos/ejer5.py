def es_palindromo(palabra):
    return palabra == palabra[::-1]

n = int(input("¿Cuántas palabras deseas ingresar?: "))
palabras = []

for i in range(n):
    palabra = input(f"Palabra {i+1}: ").lower()
    palabras.append(palabra)

print("\nPalabras palíndromas encontradas:")
for palabra in palabras:
    if es_palindromo(palabra):
        print(palabra)
