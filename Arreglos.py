import random
import time
import pandas as pd

num_alumnos = 500
num_materias = 6

# FORMA 1
matriz_alumnos = [[random.randint(0, 100) for _ in range(num_materias)] for _ in range(num_alumnos)]

# Convertir a DataFrame para visualizar bonito
df1 = pd.DataFrame(matriz_alumnos, 
                   index=[f"Alumno{i+1}" for i in range(num_alumnos)], 
                   columns=[f"Materia{j+1}" for j in range(num_materias)])

inicio1 = time.time()
calificacion1 = df1.iloc[320, 4]  
fin1 = time.time()

# FORMA 2
matriz_materias = [[random.randint(0, 100) for _ in range(num_alumnos)] for _ in range(num_materias)]

# Convertir a DataFrame para visualizar bonito
df2 = pd.DataFrame(matriz_materias, 
                   index=[f"Materia{j+1}" for j in range(num_materias)], 
                   columns=[f"Alumno{i+1}" for i in range(num_alumnos)])

inicio2 = time.time()
calificacion2 = df2.iloc[4, 320]  
fin2 = time.time()

# RESULTADOS

print("=== RESULTADOS ===")
print("\nFORMA 1 (Alumnos x Materias):")
print(f"\nAlumno 321 - Materia 5: {calificacion1}")
print(df1.head(10))  
print(f"Tiempo acceso: {fin1 - inicio1:.10f} seg")

print("\nFORMA 2 (Materias x Alumnos):")
print(f"\nAlumno 321 - Materia 5: {calificacion2}")
print(df1.head(10))  
print(f"Tiempo acceso: {fin2 - inicio2:.10f} seg")