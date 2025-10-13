from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class Cliente:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo.lower()
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class ColaBanco:
    def __init__(self):
        self.cola_prioritarios = deque()
        self.cola_normales = deque()
    def agregar_cliente(self, cliente):
        if cliente.tipo == "prioritario":
            self.cola_prioritarios.append(cliente)
        else:
            self.cola_normales.append(cliente)
    def atender_cliente(self):
        if self.cola_prioritarios:
            return self.cola_prioritarios.popleft()
        elif self.cola_normales:
            return self.cola_normales.popleft()
        else:
            return None
    def hay_clientes(self):
        return bool(self.cola_prioritarios or self.cola_normales)

class BancoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Sistema de Gestión de Turnos - Banco")
        self.root.state('zoomed')
        self.banco = ColaBanco()
        self.color_fondo = "#0A2647"
        self.color_secundario = "#144272"
        self.color_acento = "#FF6B35"
        self.color_verde = "#00C49A"
        self.color_texto = "#FFFFFF"
        self.root.configure(bg=self.color_fondo)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 13, "bold"), padding=10, background=self.color_acento, foreground="white")
        style.configure("TLabel", background=self.color_fondo, foreground=self.color_texto, font=("Segoe UI", 13))
        style.configure("Title.TLabel", font=("Segoe UI", 26, "bold"), background=self.color_fondo, foreground=self.color_verde)
        ttk.Label(self.root, text="🏦 Sistema de Gestión de Turnos Bancarios", style="Title.TLabel").pack(pady=25)
        frame_menu = tk.Frame(self.root, bg=self.color_secundario, padx=40, pady=40, relief="ridge", bd=5)
        frame_menu.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(frame_menu, text="Selecciona un modo 🎛️", background=self.color_secundario, foreground="white",
                  font=("Segoe UI", 16, "bold")).pack(pady=10)
        ttk.Button(frame_menu, text="🧠 Simulación Automática", command=self.abrir_simulacion).pack(pady=15, ipadx=30)
        ttk.Button(frame_menu, text="👥 Modo Manual", command=self.abrir_manual).pack(pady=15, ipadx=30)
        ttk.Button(frame_menu, text="🚪 Salir", command=self.root.quit).pack(pady=15, ipadx=30)

    def abrir_simulacion(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Simulación Automática")
        ventana.state('zoomed')
        ventana.configure(bg=self.color_fondo)
        ttk.Label(ventana, text="🧠 Simulación Automática del Banco", style="Title.TLabel").pack(pady=25)
        frame_sim = tk.Frame(ventana, bg=self.color_secundario, padx=20, pady=20)
        frame_sim.pack(pady=10, fill="both", expand=True)
        self.lista_sim = tk.Listbox(frame_sim, font=("Consolas", 14), bg="#DDE6ED", fg="black", height=20)
        self.lista_sim.pack(fill="both", expand=True)
        ttk.Button(ventana, text="▶️ Iniciar Simulación", command=lambda: self.iniciar_simulacion(self.lista_sim)).pack(pady=10)
        ttk.Button(ventana, text="↩️ Volver", command=ventana.destroy).pack(pady=10)

    def iniciar_simulacion(self, lista_widget):
        lista_widget.delete(0, tk.END)
        banco = ColaBanco()
        clientes = [
            Cliente("Ana", "normal"),
            Cliente("Carlos", "prioritario"),
            Cliente("Lucía", "normal"),
            Cliente("Pedro", "prioritario"),
            Cliente("Sofía", "normal"),
            Cliente("Miguel", "prioritario"),
            Cliente("Laura", "normal"),
            Cliente("José", "normal"),
            Cliente("Elena", "prioritario"),
            Cliente("Raúl", "normal")
        ]
        def simular():
            lista_widget.insert(tk.END, "📥 Llegada de clientes al banco:\n")
            for c in clientes:
                lista_widget.insert(tk.END, f"   ➕ {c}")
                banco.agregar_cliente(c)
                lista_widget.yview(tk.END)
                time.sleep(0.5)
            lista_widget.insert(tk.END, "\n🏦 Orden de atención:\n")
            contador = 1
            while banco.hay_clientes():
                cli = banco.atender_cliente()
                lista_widget.insert(tk.END, f"   {contador}. ✅ {cli}")
                lista_widget.yview(tk.END)
                contador += 1
                time.sleep(1)
            lista_widget.insert(tk.END, "\n🎉 Simulación completada.\n")
        threading.Thread(target=simular, daemon=True).start()

    def abrir_manual(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Modo Manual")
        ventana.state('zoomed')
        ventana.configure(bg=self.color_fondo)
        self.banco_manual = ColaBanco()
        ttk.Label(ventana, text="👥 Modo Manual de Atención", style="Title.TLabel").pack(pady=25)
        frame_top = tk.Frame(ventana, bg=self.color_secundario, padx=20, pady=20)
        frame_top.pack(fill="x", pady=20)
        ttk.Label(frame_top, text="👤 Nombre:", background=self.color_secundario, foreground="white").grid(row=0, column=0, padx=10)
        entry_nombre = ttk.Entry(frame_top, font=("Segoe UI", 12), width=25)
        entry_nombre.grid(row=0, column=1, padx=10)
        ttk.Label(frame_top, text="🎯 Tipo:", background=self.color_secundario, foreground="white").grid(row=0, column=2, padx=10)
        tipo_combo = ttk.Combobox(frame_top, values=["normal", "prioritario"], state="readonly", width=15)
        tipo_combo.grid(row=0, column=3, padx=10)
        tipo_combo.current(0)
        ttk.Button(frame_top, text="➕ Agregar", command=lambda: self.agregar_manual(entry_nombre, tipo_combo)).grid(row=0, column=4, padx=15)
        ttk.Button(frame_top, text="✅ Atender", command=lambda: self.atender_manual(ventana)).grid(row=0, column=5, padx=15)
        ttk.Button(frame_top, text="🔄 Reiniciar", command=self.reiniciar_manual).grid(row=0, column=6, padx=15)
        ttk.Button(frame_top, text="↩️ Volver", command=ventana.destroy).grid(row=0, column=7, padx=15)
        frame_listas = tk.Frame(ventana, bg=self.color_fondo)
        frame_listas.pack(expand=True, fill="both", pady=10)
        frame_p = tk.LabelFrame(frame_listas, text="👑 Prioritarios", fg=self.color_texto, bg=self.color_secundario, font=("Segoe UI", 14, "bold"))
        frame_p.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        self.list_prioritarios = tk.Listbox(frame_p, bg="#FFE5EC", fg="black", font=("Consolas", 13))
        self.list_prioritarios.pack(expand=True, fill="both")
        frame_n = tk.LabelFrame(frame_listas, text="🙋 Normales", fg=self.color_texto, bg=self.color_secundario, font=("Segoe UI", 14, "bold"))
        frame_n.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        self.list_normales = tk.Listbox(frame_n, bg="#E3F2FD", fg="black", font=("Consolas", 13))
        self.list_normales.pack(expand=True, fill="both")

    def agregar_manual(self, entry, combo):
        nombre = entry.get().strip()
        tipo = combo.get().lower()
        if not nombre:
            messagebox.showwarning("⚠️ Error", "Debes ingresar un nombre.")
            return
        self.banco_manual.agregar_cliente(Cliente(nombre, tipo))
        self.actualizar_listas()
        entry.delete(0, tk.END)

    def atender_manual(self, ventana):
        cli = self.banco_manual.atender_cliente()
        if cli:
            messagebox.showinfo("✅ Cliente Atendido", f"Se ha atendido a: {cli}")
            self.actualizar_listas()
            ventana.lift()
        else:
            messagebox.showinfo("ℹ️ Sin clientes", "No hay clientes en espera.")
            ventana.lift()

    def reiniciar_manual(self):
        self.banco_manual = ColaBanco()
        self.actualizar_listas()

    def actualizar_listas(self):
        self.list_prioritarios.delete(0, tk.END)
        self.list_normales.delete(0, tk.END)
        for c in self.banco_manual.cola_prioritarios:
            self.list_prioritarios.insert(tk.END, f"👑 {c}")
        for c in self.banco_manual.cola_normales:
            self.list_normales.insert(tk.END, f"🙋 {c}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BancoUI(root)
    root.mainloop()