def D_B(n):
    if n == 0:
        return ""
    return D_B(n // 2) + str(n % 2)

print("=" * 30)
print("Conversor de decimal a binario (solo enteros positivos)")
num = int(input("\nIntroduce un número entero positivo: "))

if num < 0:
    print("\nPor favor, introduce un número entero positivo.")
elif num == 0:
    print("\nEquivalente en binario: 0")
else:
    print("\nEquivalente en binario:", D_B(num))
print("=" * 30)
