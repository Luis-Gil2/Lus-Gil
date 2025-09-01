calificaciones = []

for i in range(6):
    calificacion = float(input(f"Ingrese la calificación {i+1}: "))
    calificaciones.append(calificacion)

print("\nTus calificaciones son:")
print(calificaciones)

promedio = sum(calificaciones) / len(calificaciones)
print(f"\nPromedio: {promedio:.2f}")
print(f"Calificación más alta: {max(calificaciones)}")
print(f"Calificación más baja: {min(calificaciones)}")