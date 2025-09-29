import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Pila:
    def __init__(self):
        self.items = []

    def apilar(self, elemento):
        self.items.append(elemento)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        else:
            return None

    def cima(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None

    def esta_vacia(self):
        return len(self.items) == 0

    def mostrar(self):
        return self.items
    
class PilaApp:
    def __init__(self, root):
        self.pila = Pila()

        # Ventana principal
        self.root = root
        self.root.title("Proyecto: Pila con menú gráfico")

        # Entrada para apilar
        self.entry = tk.Entry(root, width=20)
        self.entry.grid(row=0, column=0, padx=5, pady=5)

        # Botones del menú
        tk.Button(root, text="1. Apilar", command=self.apilar).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="2. Desapilar", command=self.desapilar).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="3. Ver cima", command=self.ver_cima).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(root, text="4. Mostrar pila", command=self.mostrar_pila).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(root, text="5. Salir", command=root.quit, bg="red", fg="white").grid(row=4, column=1, padx=5, pady=5)

        # Área gráfica con matplotlib embebido en Tkinter
        self.fig, self.ax = plt.subplots(figsize=(4, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=6, padx=10, pady=10)

        # Inicializar gráfica
        self.dibujar("Pila vacía")

    # -------------------------------
    # Método dibujar actualizado
    # -------------------------------
    def dibujar(self, accion=""):
        self.ax.clear()

        # Dibujar los elementos de la pila (último elemento agregado primero)
        for i, elem in enumerate(reversed(self.pila.items)):
            self.ax.barh(i, 1, color="skyblue", edgecolor="black")
            self.ax.text(0.5, i, str(elem), ha="center", va="center", fontsize=12, weight="bold")

        # Ajustar niveles (Nivel 1 abajo, cima arriba)
        niveles = [f"Nivel {i+1}" for i in range(len(self.pila.items))]
        self.ax.set_yticks(range(len(self.pila.items)))
        self.ax.set_yticklabels(niveles)

        # Invertir eje Y para que el último elemento aparezca arriba
        self.ax.invert_yaxis()

        self.ax.set_xticks([])
        self.ax.set_title(f"📊 Representación gráfica de la Pila\n{accion}")

        self.canvas.draw()

    def apilar(self):
        elemento = self.entry.get()
        if elemento:
            self.pila.apilar(elemento)
            self.dibujar(f"Apilado: {elemento}")
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Ingresa un elemento antes de apilar")

    def desapilar(self):
        elem = self.pila.desapilar()
        if elem is not None:
            self.dibujar(f"Desapilado: {elem}")
        else:
            messagebox.showinfo("Info", "La pila está vacía")

    def ver_cima(self):
        cima = self.pila.cima()
        if cima is not None:
            messagebox.showinfo("Elemento en cima", f"La cima es: {cima}")
            self.dibujar(f"Cima: {cima}")
        else:
            messagebox.showinfo("Info", "La pila está vacía")

    def mostrar_pila(self):
        contenido = self.pila.mostrar()
        messagebox.showinfo("Contenido de la pila", f"Pila: {contenido}")
        self.dibujar("Mostrar pila")

if __name__ == "__main__":
    root = tk.Tk()
    app = PilaApp(root)
    root.mainloop()