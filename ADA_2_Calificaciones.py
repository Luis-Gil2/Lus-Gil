calificaciones = [0] * 5 

for i in range(5):
    calificaciones[i] = int(input(f"Captura la calificación {i+1}: "))

print("\nLas calificaciones capturadas son:")
for i in range(5):
    print(f"Calificación {i+1}: {calificaciones[i]}")
