from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime, date
import os

# -------------------------- Cliente --------------------------
class Cliente:
    contador_turno = 1
    def __init__(self, nombre, tipo, movimiento=None):
        self.nombre = nombre
        self.tipo = tipo.lower()
        self.turno = f"T{Cliente.contador_turno:03d}"
        Cliente.contador_turno += 1
        self.movimiento = movimiento

    def __str__(self):
        return f"{self.turno} - {self.nombre} ({self.tipo}) | {self.movimiento or ''}"

# -------------------------- Cola Banco --------------------------
class ColaBanco:
    def __init__(self):
        self.cola_prioritarios = deque()
        self.cola_normales = deque()
        self.contador_prioritarios = 0

    def agregar_cliente(self, cliente):
        if cliente.tipo == "prioritario":
            self.cola_prioritarios.append(cliente)
        else:
            self.cola_normales.append(cliente)

    def atender_cliente(self):
        if self.cola_prioritarios:
            if self.contador_prioritarios < 5 or len(self.cola_normales) < 2:
                cli = self.cola_prioritarios.popleft()
                self.contador_prioritarios += 1
                return cli
        if self.cola_normales:
            self.contador_prioritarios = 0
            return self.cola_normales.popleft()
        return None

    def hay_clientes(self):
        return bool(self.cola_prioritarios or self.cola_normales)

# -------------------------- Interfaz Banco --------------------------
class BancoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Banco SOFTREX - Gestión de Turnos")
        self.root.geometry("1200x750")
        self.color_fondo = "#0D1B2A"
        self.color_secundario = "#1B263B"
        self.color_acento = "#E94560"
        self.color_verde = "#00FFAB"
        self.color_texto = "#FFFFFF"
        self.color_tarjeta = "#162447"
        self.root.configure(bg=self.color_fondo)
        self.banco_manual = ColaBanco()
        self.clientes_atendidos_manual = {"prioritario": 0, "normal": 0}
        self.ultimo_dia_manual = date.today()
        self.crear_registro_txt()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=6, background=self.color_acento, foreground="white")
        style.configure("TLabel", background=self.color_fondo, foreground=self.color_texto, font=("Segoe UI", 12))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), background=self.color_fondo, foreground=self.color_verde)

        # Logo
        logo_frame = tk.Frame(self.root, bg=self.color_fondo)
        logo_frame.pack(pady=15)
        tk.Label(logo_frame, text="🏦 SOFTREX BANK", font=("Segoe UI", 28, "bold"), fg="#FFD166", bg=self.color_fondo).pack()

        # Menú principal
        frame_menu = tk.Frame(self.root, bg=self.color_secundario, padx=40, pady=40, relief="ridge", bd=4)
        frame_menu.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(frame_menu, text="Selecciona un modo 🎛️", background=self.color_secundario,
                  foreground="white", font=("Segoe UI", 16, "bold")).pack(pady=10)
        ttk.Button(frame_menu, text="🧠 Simulación Automática", command=self.abrir_simulacion, width=25).pack(pady=12)
        ttk.Button(frame_menu, text="👥 Modo Manual", command=self.abrir_manual, width=25).pack(pady=12)
        ttk.Button(frame_menu, text="🚪 Salir", command=self.root.quit, width=25).pack(pady=12)

    # ---------------- Crear registro ----------------
    def crear_registro_txt(self):
        if not os.path.exists("registro_softrex.txt"):
            with open("registro_softrex.txt", "w", encoding="utf-8") as f:
                f.write("Registro de Atención - Banco SOFTREX\n")
                f.write("Fecha y Hora | Turno | Cliente | Tipo | Movimiento | Total Atendidos | Prioritarios Hoy | Normales Hoy\n")
                f.write("-"*100+"\n")

    # ---------------- Ventanillas ----------------
    def crear_ventanillas(self, parent):
        frame_ventanillas = tk.Frame(parent, bg=self.color_fondo)
        frame_ventanillas.pack(fill="x", pady=10)
        self.ventanillas_labels = []
        for i in range(5):
            lbl = tk.Label(frame_ventanillas, text=f"🏦 Ventanilla {i+1}: Libre", font=("Segoe UI", 11, "bold"),
                           bg=self.color_tarjeta, fg="#FFFFFF", width=22, relief="ridge", padx=5, pady=5)
            lbl.pack(side="left", padx=5, pady=5)
            self.ventanillas_labels.append(lbl)

    def actualizar_ventanilla(self, index, texto):
        self.ventanillas_labels[index].config(text=f"🏦 Ventanilla {index+1}: {texto}")
        self.root.update_idletasks()

    # ---------------- Simulación ----------------
    def abrir_simulacion(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Simulación Automática - SOFTREX")
        ventana.geometry("900x600")
        ventana.configure(bg=self.color_fondo)
        ttk.Label(ventana, text="🧠 Simulación Automática del Banco", style="Title.TLabel").pack(pady=20)
        frame_sim = tk.Frame(ventana, bg=self.color_secundario, padx=10, pady=10)
        frame_sim.pack(pady=10, fill="both", expand=True)
        self.lista_sim = tk.Listbox(frame_sim, font=("Consolas", 11), bg="#DDE6ED", fg="black", height=20)
        self.lista_sim.pack(fill="both", expand=True)
        self.crear_ventanillas(ventana)
        ttk.Button(ventana, text="▶️ Iniciar Simulación", command=lambda: self.iniciar_simulacion(self.lista_sim)).pack(pady=10)
        ttk.Button(ventana, text="↩️ Volver", command=ventana.destroy).pack(pady=5)

    def iniciar_simulacion(self, lista_widget):
        lista_widget.delete(0, tk.END)
        banco = ColaBanco()
        clientes = [
            Cliente("Ana", "normal", "Depósito 💰"), Cliente("Carlos", "prioritario", "Retiro 🏧"),
            Cliente("Lucía", "normal", "Transferencia 🔄"), Cliente("Pedro", "prioritario", "Depósito 💰"),
            Cliente("Sofía", "normal", "Retiro 🏧"), Cliente("Miguel", "prioritario", "Transferencia 🔄"),
            Cliente("Laura", "normal", "Depósito 💰"), Cliente("José", "normal", "Retiro 🏧"),
            Cliente("Elena", "prioritario", "Transferencia 🔄"), Cliente("Raúl", "normal", "Depósito 💰")
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
                ventanillas = []
                for i in range(5):
                    if banco.hay_clientes():
                        cli = banco.atender_cliente()
                        if cli:
                            ventanillas.append((i, cli))
                            self.actualizar_ventanilla(i, f"Atendiendo: {cli} 🚀")
                time.sleep(1)
                for i, v in ventanillas:
                    lista_widget.insert(tk.END, f"   {contador}. ✅ {v}")
                    self.guardar_registro(v)
                    contador += 1
                    self.actualizar_ventanilla(i, "Libre 🏦")
                    lista_widget.yview(tk.END)
                    time.sleep(0.5)
            lista_widget.insert(tk.END, "\n🎉 Simulación completada.\n")
        threading.Thread(target=simular, daemon=True).start()

    # ---------------- Modo Manual ----------------
    def abrir_manual(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Modo Manual - SOFTREX")
        ventana.geometry("1400x850")
        ventana.configure(bg=self.color_fondo)

        ttk.Label(ventana, text="👥 Modo Manual de Atención", style="Title.TLabel").pack(pady=20)

        # Contadores diarios
        self.frame_contadores_manual = tk.Frame(ventana, bg="#081F3C", bd=2, relief="ridge")
        self.frame_contadores_manual.pack(pady=10, fill="x", padx=20)
        self.lbl_contadores_manual = tk.Label(
            self.frame_contadores_manual,
            text=self.obtener_texto_contadores_manual(),
            font=("Segoe UI", 14, "bold"),
            bg="#081F3C",
            fg="#00FFAB",
            padx=10,
            pady=5
        )
        self.lbl_contadores_manual.pack()

        # Formulario de ingreso
        frame_top = tk.Frame(ventana, bg=self.color_secundario, padx=20, pady=20)
        frame_top.pack(fill="x", pady=10, padx=20)

        ttk.Label(frame_top, text="👤 Nombre:", background=self.color_secundario, foreground="white").grid(row=0, column=0, padx=5, pady=5)
        entry_nombre = ttk.Entry(frame_top, font=("Segoe UI", 12), width=20)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_top, text="🎯 Tipo:", background=self.color_secundario, foreground="white").grid(row=0, column=2, padx=5, pady=5)
        tipo_combo = ttk.Combobox(frame_top, values=["normal", "prioritario"], state="readonly", width=15)
        tipo_combo.grid(row=0, column=3, padx=5, pady=5)
        tipo_combo.current(0)
        ttk.Label(frame_top, text="💳 Movimiento:", background=self.color_secundario, foreground="white").grid(row=0, column=4, padx=5, pady=5)
        movimiento_combo = ttk.Combobox(frame_top, values=["Depósito 💰", "Retiro 🏧", "Transferencia 🔄"], state="readonly", width=20)
        movimiento_combo.grid(row=0, column=5, padx=5, pady=5)

        # Botones
        botones = [
            ("➕ Agregar", lambda: self.agregar_manual(entry_nombre, tipo_combo, movimiento_combo)),
            ("✅ Atender", self.atender_manual_con_ventanillas),
            ("🔄 Reiniciar", self.reiniciar_manual),
            ("📜 Ver Registro", self.abrir_registro),
            ("🗑️ Borrar Registro", self.borrar_registro),
            ("↩️ Volver", ventana.destroy)
        ]
        for i, (text, cmd) in enumerate(botones):
            ttk.Button(frame_top, text=text, command=cmd, width=15).grid(row=0, column=6+i, padx=5, pady=5)

        # Listas de clientes
        frame_listas = tk.Frame(ventana, bg=self.color_fondo)
        frame_listas.pack(expand=True, fill="both", pady=20, padx=20)
        frame_listas.columnconfigure(0, weight=1)
        frame_listas.columnconfigure(1, weight=1)
        frame_listas.rowconfigure(0, weight=1)

        frame_p = tk.LabelFrame(frame_listas, text="👑 Prioritarios", fg=self.color_texto, bg=self.color_secundario, font=("Segoe UI", 14, "bold"))
        frame_p.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.list_prioritarios = tk.Listbox(frame_p, bg="#FFE5EC", fg="black", font=("Consolas", 13))
        self.list_prioritarios.pack(expand=True, fill="both", padx=5, pady=5)

        frame_n = tk.LabelFrame(frame_listas, text="🙋 Normales", fg=self.color_texto, bg=self.color_secundario, font=("Segoe UI", 14, "bold"))
        frame_n.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.list_normales = tk.Listbox(frame_n, bg="#E3F2FD", fg="black", font=("Consolas", 13))
        self.list_normales.pack(expand=True, fill="both", padx=5, pady=5)

        self.crear_ventanillas(ventana)

    # ---------- Funciones contadores ----------
    def obtener_texto_contadores_manual(self):
        return f"👑 Prioritarios hoy: {self.clientes_atendidos_manual['prioritario']}   🙋 Normales hoy: {self.clientes_atendidos_manual['normal']}"

    def actualizar_contadores_manual(self, tipo):
        hoy = date.today()
        if hoy != self.ultimo_dia_manual:
            self.clientes_atendidos_manual = {"prioritario": 0, "normal": 0}
            self.ultimo_dia_manual = hoy
        self.clientes_atendidos_manual[tipo] += 1
        self.lbl_contadores_manual.config(text=self.obtener_texto_contadores_manual())

    # ---------- Agregar y atender ----------
    def agregar_manual(self, entry, combo_tipo, combo_mov):
        nombre = entry.get().strip()
        tipo = combo_tipo.get().lower()
        movimiento = combo_mov.get()
        if not nombre:
            messagebox.showwarning("⚠️ Error", "Debes ingresar un nombre.")
            return
        self.banco_manual.agregar_cliente(Cliente(nombre, tipo, movimiento))
        self.actualizar_listas()
        entry.delete(0, tk.END)

    def atender_manual_con_ventanillas(self):
        def atender():
            ventanillas = []
            for i in range(5):
                cli = self.banco_manual.atender_cliente()
                if cli:
                    ventanillas.append((i, cli))
                    self.actualizar_ventanilla(i, f"Atendiendo: {cli} 🚀")
            if ventanillas:
                for i, c in ventanillas:
                    self.guardar_registro(c)
                    self.actualizar_contadores_manual(c.tipo)
                    time.sleep(1)
                    self.actualizar_ventanilla(i, "Libre 🏦")
                self.actualizar_listas()
            else:
                messagebox.showinfo("ℹ️ Sin clientes", "No hay clientes en espera.")
        threading.Thread(target=atender, daemon=True).start()

    def reiniciar_manual(self):
        self.banco_manual = ColaBanco()
        self.clientes_atendidos_manual = {"prioritario": 0, "normal": 0}
        self.ultimo_dia_manual = date.today()
        self.lbl_contadores_manual.config(text=self.obtener_texto_contadores_manual())
        self.actualizar_listas()

    def actualizar_listas(self):
        self.list_prioritarios.delete(0, tk.END)
        self.list_normales.delete(0, tk.END)
        for c in self.banco_manual.cola_prioritarios:
            self.list_prioritarios.insert(tk.END, f"👑 {c}")
        for c in self.banco_manual.cola_normales:
            self.list_normales.insert(tk.END, f"🙋 {c}")

    def guardar_registro(self, cliente):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_atendidos = Cliente.contador_turno - 1
        with open("registro_softrex.txt", "a", encoding="utf-8") as f:
            f.write(f"{fecha_hora} | {cliente.turno} | {cliente.nombre} | {cliente.tipo} | Movimiento: {cliente.movimiento or ''} | Total atendidos: {total_atendidos} | Prioritarios Hoy: {self.clientes_atendidos_manual['prioritario']} | Normales Hoy: {self.clientes_atendidos_manual['normal']}\n")

    def abrir_registro(self):
        if not os.path.exists("registro_softrex.txt"):
            messagebox.showinfo("ℹ️ Registro vacío", "Aún no se ha registrado ninguna atención.")
            return
        ventana_reg = tk.Toplevel(self.root)
        ventana_reg.title("📜 Registro de Atenciones - SOFTREX")
        ventana_reg.geometry("800x500")
        ventana_reg.configure(bg=self.color_fondo)
        ttk.Label(ventana_reg, text="📜 Registro de Atenciones", style="Title.TLabel").pack(pady=10)
        frame_list = tk.Frame(ventana_reg, bg=self.color_secundario, padx=5, pady=5)
        frame_list.pack(expand=True, fill="both", padx=10, pady=10)
        scroll = tk.Scrollbar(frame_list)
        scroll.pack(side="right", fill="y")
        list_registro = tk.Listbox(frame_list, font=("Consolas", 11), bg="#F5F5F5", fg="black", yscrollcommand=scroll.set)
        list_registro.pack(expand=True, fill="both")
        scroll.config(command=list_registro.yview)
        with open("registro_softrex.txt", "r", encoding="utf-8") as f:
            for linea in f.readlines()[3:]:
                list_registro.insert(tk.END, linea.strip())

    def borrar_registro(self):
        if os.path.exists("registro_softrex.txt"):
            if messagebox.askyesno("🗑️ Borrar Registro", "¿Estás seguro de borrar todo el registro?"):
                with open("registro_softrex.txt", "w", encoding="utf-8") as f:
                    f.write("Registro de Atención - Banco SOFTREX\n")
                    f.write("Fecha y Hora | Turno | Cliente | Tipo | Movimiento | Total Atendidos | Prioritarios Hoy | Normales Hoy\n")
                    f.write("-"*100+"\n")
                messagebox.showinfo("✅ Registro Borrado", "El registro se ha borrado correctamente.")

# -------------------------- Inicio --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BancoUI(root)
    root.mainloop()
