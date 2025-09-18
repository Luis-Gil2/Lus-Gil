# Programa para imprimir la serie de Fibonacci
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

num = int(input("¿Cuántos términos de la serie Fibonacci quieres? "))
fibonacci(num)


# Función recursiva para Fibonacci
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

num = int(input("¿Cuántos términos de la serie Fibonacci quieres? "))

print("Serie de Fibonacci:")
for i in range(num):
    print(fibonacci(i), end=" ")