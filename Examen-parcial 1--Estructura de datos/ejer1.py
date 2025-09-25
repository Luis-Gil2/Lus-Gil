nombres = []
longitudes = []
x = "a"
while True:
    try:
        x = int(input("Ingresa la cantidad de nombres que vas a ingresar: "))
    except ValueError:
        print("Solo se admiten números enteros")
    if type(x) == int:
        break

for i in range(x):
    nombre = input("Inserte el primer nombre:")
    nombres.append(nombre)
    longitudes.append(len(nombre))

for i in range(x):
    print(f"{nombres[i]} - {longitudes[i]}")
