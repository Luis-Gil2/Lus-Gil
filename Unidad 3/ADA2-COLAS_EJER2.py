import tkinter as tk
from tkinter import ttk

class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None

    def esta_vacia(self):
        return len(self.items) == 0

    def mostrar_cola(self):
        if self.esta_vacia():
            return "Vacía"
        return ", ".join(self.items)


class SistemaColasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Atención - Compañía de Seguros")
        self.root.geometry("750x500")
        self.root.configure(bg="#f5f5f5")

        # Prefijos para cada servicio
        self.prefijos = {1: "CD", 2: "CE", 3: "CF"}
        self.colas = {1: Cola(), 2: Cola(), 3: Cola()}
        self.contadores = {1: 0, 2: 0, 3: 0}

        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.root, text="Sistema de Atención de Clientes", font=("Segoe UI", 20, "bold"), bg="#f5f5f5", fg="#003366")
        titulo.pack(pady=15)

        # Marco de acción para agregar cliente
        marco_llegada = tk.Frame(self.root, bg="white", relief="groove", bd=2)
        marco_llegada.pack(pady=10, padx=20, fill="x")

        tk.Label(marco_llegada, text="Agregar Cliente al Servicio:", font=("Segoe UI", 12, "bold"), bg="white").pack(side="left", padx=5, pady=10)
        self.combo_servicio_llegada = ttk.Combobox(marco_llegada, values=[1, 2, 3], state="readonly", width=5, font=("Segoe UI", 11))
        self.combo_servicio_llegada.current(0)
        self.combo_servicio_llegada.pack(side="left", padx=5)
        btn_llegada = tk.Button(marco_llegada, text="Agregar Cliente", command=self.llegada_cliente, font=("Segoe UI", 12, "bold"), bg="#0066cc", fg="white")
        btn_llegada.pack(side="left", padx=10)

        # Marco de acción para atender cliente
        marco_atender = tk.Frame(self.root, bg="white", relief="groove", bd=2)
        marco_atender.pack(pady=10, padx=20, fill="x")

        tk.Label(marco_atender, text="Atender Cliente del Servicio:", font=("Segoe UI", 12, "bold"), bg="white").pack(side="left", padx=5, pady=10)
        self.combo_servicio_atender = ttk.Combobox(marco_atender, values=[1, 2, 3], state="readonly", width=5, font=("Segoe UI", 11))
        self.combo_servicio_atender.current(0)
        self.combo_servicio_atender.pack(side="left", padx=5)
        btn_atender = tk.Button(marco_atender, text="Atender Cliente", command=self.atender_cliente, font=("Segoe UI", 12, "bold"), bg="#009900", fg="white")
        btn_atender.pack(side="left", padx=10)

        # Salida de mensajes
        self.salida = tk.Text(self.root, height=15, font=("Consolas", 11), bg="#eef3f9", fg="#003366", wrap="word")
        self.salida.pack(padx=20, pady=15, fill="both", expand=True)

        # Mostrar colas iniciales
        self.mostrar_colas()

    def generar_codigo_cliente(self, servicio):
        self.contadores[servicio] += 1
        numero = f"{self.contadores[servicio]:02d}"  # Dos dígitos
        codigo = f"{self.prefijos[servicio]}{numero}"  # Ejemplo: CD01, CE02
        self.colas[servicio].encolar(codigo)
        return codigo

    def llegada_cliente(self):
        servicio = int(self.combo_servicio_llegada.get())
        codigo = self.generar_codigo_cliente(servicio)
        self.salida.insert(tk.END, f"Cliente agregado al servicio {servicio}: {codigo}\n")
        self.salida.see(tk.END)
        self.mostrar_colas()

    def atender_cliente(self):
        servicio = int(self.combo_servicio_atender.get())
        if self.colas[servicio].esta_vacia():
            self.salida.insert(tk.END, f"No hay clientes en la cola {servicio} para atender.\n")
        else:
            codigo = self.colas[servicio].desencolar()
            self.salida.insert(tk.END, f"Atendiendo cliente {codigo} del servicio {servicio}.\n")
        self.salida.see(tk.END)
        self.mostrar_colas()

    def mostrar_colas(self):
        self.salida.insert(tk.END, "\nColas actuales:\n")
        for servicio in self.colas:
            self.salida.insert(tk.END, f"Servicio {servicio}: {self.colas[servicio].mostrar_cola()}\n")
        self.salida.insert(tk.END, "-"*50 + "\n")
        self.salida.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaColasGUI(root)
    root.mainloop()
