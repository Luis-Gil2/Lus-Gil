import tkinter as tk
import time

class Pila:
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        else:
            raise IndexError("La pila está vacía")

    def esta_vacia(self):
        return len(self.items) == 0

# ---------------- FUNCIONES TORRES ----------------
def mover_disco_animado(origen, destino, canvas, posiciones, velocidad=0.01):
    disco = origen.desapilar()
    x_origen = posiciones[origen.nombre]
    y_origen = 250 - len(origen.items)*20

    # Subir disco
    for dy in range(0, 50, 2):
        actualizar_canvas(canvas, posiciones, origen, auxiliar, destino, mover=(disco, x_origen, y_origen - dy))
        time.sleep(velocidad)

    # Movimiento horizontal
    x_destino = posiciones[destino.nombre]
    paso = 2 if x_destino > x_origen else -2
    for dx in range(0, x_destino - x_origen, paso):
        actualizar_canvas(canvas, posiciones, origen, auxiliar, destino, mover=(disco, x_origen + dx, y_origen - 50))
        time.sleep(velocidad)

    # Bajar disco
    y_destino = 250 - len(destino.items)*20
    for dy in range(0, y_destino - (y_origen - 50), 2):
        actualizar_canvas(canvas, posiciones, origen, auxiliar, destino, mover=(disco, x_destino, y_origen - 50 + dy))
        time.sleep(velocidad)

    # Apilar disco en destino
    destino.apilar(disco)
    actualizar_canvas(canvas, posiciones, origen, auxiliar, destino)

def hanoi_animado(n, origen, auxiliar, destino, canvas, posiciones, velocidad=0.01):
    if n == 1:
        mover_disco_animado(origen, destino, canvas, posiciones, velocidad)
    else:
        hanoi_animado(n-1, origen, destino, auxiliar, canvas, posiciones, velocidad)
        mover_disco_animado(origen, destino, canvas, posiciones, velocidad)
        hanoi_animado(n-1, auxiliar, origen, destino, canvas, posiciones, velocidad)

# ---------------- FUNCIONES GRAFICAS ----------------
def actualizar_canvas(canvas, posiciones, *pilas, mover=None):
    canvas.delete("all")
    ancho_disco = 20
    alto_disco = 20

    # Dibujar torres y discos fijos
    for torre in pilas:
        x = posiciones[torre.nombre]
        canvas.create_rectangle(x-10, 150, x+10, 250, fill="brown")
        for j, disco in enumerate(torre.items):
            x0 = x - (disco * ancho_disco // 2)
            y0 = 250 - (j+1) * alto_disco
            x1 = x + (disco * ancho_disco // 2)
            y1 = 250 - j * alto_disco
            canvas.create_rectangle(x0, y0, x1, y1, fill="skyblue")
            canvas.create_text((x0+x1)//2, (y0+y1)//2, text=str(disco), fill="black")

    # Dibujar disco en movimiento si existe
    if mover:
        disco_val, x, y = mover
        x0 = x - (disco_val * ancho_disco // 2)
        y0 = y
        x1 = x + (disco_val * ancho_disco // 2)
        y1 = y + alto_disco
        canvas.create_rectangle(x0, y0, x1, y1, fill="orange")
        canvas.create_text((x0+x1)//2, (y0+y1)//2, text=str(disco_val), fill="black")

    # Mostrar nombres de torres
    for torre in pilas:
        x = posiciones[torre.nombre]
        canvas.create_text(x, 260, text=torre.nombre, font=("Arial", 12))

    canvas.update()

# ---------------- PROGRAMA PRINCIPAL ----------------
if __name__ == "__main__":
    # Crear torres como pilas
    origen = Pila("Origen")
    auxiliar = Pila("Auxiliar")
    destino = Pila("Destino")

    # Inicializar torre de origen con 3 discos
    for disco in [3,2,1]:
        origen.apilar(disco)

    # Crear ventana
    root = tk.Tk()
    root.title("Torres de Hanoi Animadas")
    canvas = tk.Canvas(root, width=400, height=300, bg="white")
    canvas.pack()

    # Posiciones X de las torres
    posiciones = {"Origen":100, "Auxiliar":200, "Destino":300}

    # Mostrar estado inicial
    actualizar_canvas(canvas, posiciones, origen, auxiliar, destino)
    time.sleep(0.5)

    # Resolver Torres de Hanoi con animación más rápida
    hanoi_animado(3, origen, auxiliar, destino, canvas, posiciones, velocidad=0.010)

    root.mainloop()