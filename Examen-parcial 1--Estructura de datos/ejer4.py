import random 

longitud = int(input("Ingresa la longitud del vetor: "))

a = [None] * longitud
b = [None] * longitud
sumando = [None] * longitud
restando = [None] * longitud

for i in range(longitud):
    a[i]=random.randint (-100,100)

    b[i]=random.randint (-100,100)

for i in range(longitud):
    sumando[i] = a[i] + b[i]
    restando[i] = a[i] - b[i]

opciones = int(input("Seleccione que vector desea ver,elija entre 1=a, 2=b, 3=c sumando a y b, 4=c restando a y b: "))


if opciones == 1:
    print("vector A:",a)

elif opciones == 2:
    print("vector B:", b)

elif opciones == 3:
    print("vector c sumando a y b:", sumando)

elif opciones == 4:
    print("vector c restando a y b:", restando)
    exit()

else:
    print("no es valida esta opcion")
    exit()