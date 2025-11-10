from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime, date
import os
import math

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

# -------------------------- UI Helpers (rounded cards + shadows) --------------------------
class Card(tk.Canvas):
    def __init__(self, parent, width=300, height=150, radius=16, bg="#162447", shadow=True, **kwargs):
        tk.Canvas.__init__(self, parent, width=width, height=height, highlightthickness=0, bg=parent['bg'], **kwargs)
        self.width = width
        self.height = height
        self.radius = radius
        self.bg = bg
        self.shadow = shadow
        self.draw_card()

    def draw_card(self):
       self.delete("all")

       if self.shadow:
        for i, off in enumerate([(6, 6), (4, 4), (2, 2)]):
            xoff, yoff = off
            shade = 10 + i * 8
            color = self._darken(self.bg, shade)
            self._rounded_rect(xoff, yoff, self.width, self.height, self.radius, fill=color, outline=color)

       self._rounded_rect(
        0, 0, self.width - 6, self.height - 6, self.radius,
        fill=self.bg, outline=self._darken(self.bg, 20)
    )

    def _rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1,
                  x1+r, y1,
                  x2-r, y1,
                  x2-r, y1,
                  x2, y1,
                  x2, y1+r,
                  x2, y1+r,
                  x2, y2-r,
                  x2, y2-r,
                  x2, y2,
                  x2-r, y2,
                  x2-r, y2,
                  x1+r, y2,
                  x1+r, y2,
                  x1, y2,
                  x1, y2-r,
                  x1, y2-r,
                  x1, y1+r,
                  x1, y1+r,
                  x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _darken(self, hexcolor, amount=10):
        hexcolor = hexcolor.lstrip('#')
        r = int(hexcolor[0:2],16)
        g = int(hexcolor[2:4],16)
        b = int(hexcolor[4:6],16)
        r = max(0, r-amount)
        g = max(0, g-amount)
        b = max(0, b-amount)
        return f"#{r:02x}{g:02x}{b:02x}"

# -------------------------- Interfaz Banco (rediseñada) --------------------------
class BancoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Banco SOFTREX - Gestión de Turnos")
        try:
            self.root.state('zoomed')
        except Exception:
            self.root.attributes('-zoomed', True)

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
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 12, 'bold'), padding=6)
        style.configure('TLabel', background=self.color_fondo, foreground=self.color_texto, font=('Segoe UI',12))
        style.configure('Title.TLabel', font=('Segoe UI',22,'bold'), background=self.color_fondo, foreground=self.color_verde)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = tk.Frame(self.root, bg=self.color_fondo)
        main_frame.grid(sticky='nsew')
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        header = tk.Frame(main_frame, bg=self.color_fondo)
        header.grid(row=0, column=0, sticky='ew', pady=(12,6))
        header.columnconfigure(0, weight=1)
        tk.Label(header, text="🏦 SOFTREX BANK", font=("Segoe UI", 30, 'bold'), fg="#FFD166", bg=self.color_fondo).grid(row=0,column=0)

        content = tk.Frame(main_frame, bg=self.color_fondo)
        content.grid(row=1, column=0, sticky='nsew', padx=20, pady=12)
        content.columnconfigure(0, weight=1, uniform='a')
        content.columnconfigure(1, weight=2, uniform='a')
        content.rowconfigure(0, weight=1)

        left_panel = tk.Frame(content, bg=self.color_fondo)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0,10))
        left_panel.rowconfigure(0, weight=0)
        left_panel.rowconfigure(1, weight=1)

        menu_card = Card(left_panel, width=380, height=420, radius=18, bg=self.color_tarjeta)
        menu_card.pack(fill='both', expand=True)

        menu_inner = tk.Frame(menu_card, bg=self.color_tarjeta)
        menu_card.create_window(8,8, anchor='nw', window=menu_inner, width=menu_card.width-18, height=menu_card.height-18)
        menu_inner.columnconfigure(0, weight=1)

        tk.Label(menu_inner, text="Selecciona un modo 🎛️", bg=self.color_tarjeta, fg='white', font=("Segoe UI",16,'bold')).grid(row=0, column=0, pady=(20,8))
        self.btn_auto = ttk.Button(menu_inner, text="🧠 Simulación Automática", command=self.abrir_simulacion, width=24)
        self.btn_manual = ttk.Button(menu_inner, text="👥 Modo Manual", command=self.abrir_manual, width=24)
        self.btn_salir = ttk.Button(menu_inner, text="🚪 Salir", command=self.root.quit, width=24)
        self.btn_auto.grid(row=1, column=0, pady=12)
        self.btn_manual.grid(row=2, column=0, pady=12)
        self.btn_salir.grid(row=3, column=0, pady=12)

        right_panel = tk.Frame(content, bg=self.color_fondo)
        right_panel.grid(row=0, column=1, sticky='nsew')
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)

        stats_card = Card(right_panel, width=800, height=180, radius=18, bg=self.color_tarjeta)
        stats_card.pack(fill='x', pady=(0,12))
        stats_inner = tk.Frame(stats_card, bg=self.color_tarjeta)
        stats_card.create_window(8,8, anchor='nw', window=stats_inner, width=stats_card.width-18, height=stats_card.height-18)
        stats_inner.columnconfigure((0,1,2), weight=1)

        self.lbl_total = tk.Label(stats_inner, text="Total Turnos: 0", bg=self.color_tarjeta, fg=self.color_verde, font=("Segoe UI",16,'bold'))
        self.lbl_prio = tk.Label(stats_inner, text="Prioritarios hoy: 0", bg=self.color_tarjeta, fg='white', font=("Segoe UI",14))
        self.lbl_norm = tk.Label(stats_inner, text="Normales hoy: 0", bg=self.color_tarjeta, fg='white', font=("Segoe UI",14))
        self.lbl_total.grid(row=0, column=0, padx=12, pady=18)
        self.lbl_prio.grid(row=0, column=1, padx=12)
        self.lbl_norm.grid(row=0, column=2, padx=12)

        vent_card = Card(right_panel, width=800, height=300, radius=18, bg=self.color_tarjeta)
        vent_card.pack(fill='both', expand=True)
        vent_inner = tk.Frame(vent_card, bg=self.color_tarjeta)
        vent_card.create_window(8,8, anchor='nw', window=vent_inner, width=vent_card.width-18, height=vent_card.height-18)
        vent_inner.columnconfigure(tuple(range(5)), weight=1)

        self.ventanillas_labels = []
        for i in range(5):
            lbl = tk.Label(vent_inner, text=f"🏦 Ventanilla {i+1}: Libre", font=("Segoe UI",11,'bold'), bg=self.color_tarjeta, fg='white', bd=0, relief='flat')
            lbl.grid(row=0, column=i, padx=6, pady=20, sticky='nsew')
            self.ventanillas_labels.append(lbl)

        self._animate_entrance()

    def crear_registro_txt(self):
        if not os.path.exists("registro_softrex.txt"):
            with open("registro_softrex.txt", "w", encoding="utf-8") as f:
                f.write("Registro de Atención - Banco SOFTREX\n")
                f.write("Fecha y Hora | Turno | Cliente | Tipo | Movimiento | Total Atendidos | Prioritarios Hoy | Normales Hoy\n")
                f.write("-"*100+"\n")

    # ---------------- Ventanillas ----------------
    def actualizar_ventanilla(self, index, texto):
        lbl = self.ventanillas_labels[index]
        lbl.config(text=f"🏦 Ventanilla {index+1}: {texto}")
        orig_bg = lbl['bg']
        def pulse(count=0):
            if count>6:
                lbl.config(bg=orig_bg)
                return
            if count%2==0:
                lbl.config(bg=self._lighten(self.color_tarjeta, 18))
            else:
                lbl.config(bg=self.color_tarjeta)
            self.root.after(120, lambda: pulse(count+1))
        pulse()
        self.root.update_idletasks()

    def _lighten(self, hexcolor, amount=20):
        hexcolor = hexcolor.lstrip('#')
        r = int(hexcolor[0:2],16)
        g = int(hexcolor[2:4],16)
        b = int(hexcolor[4:6],16)
        r = min(255, r+amount)
        g = min(255, g+amount)
        b = min(255, b+amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _animate_entrance(self):
        for i, btn in enumerate((self.btn_auto, self.btn_manual, self.btn_salir)):
            btn.place_info_backup = btn.place_info()
            btn.grid_forget()
            btn.place(in_=btn.master, relx=0.5, rely=1.2+i*0.08, anchor='s')
            self._slide_widget(btn, start_y=1.2+i*0.08, end_y=0.3+i*0.08, steps=18, delay=15)

    def _slide_widget(self, widget, start_y, end_y, steps=20, delay=20):
        dy = (end_y - start_y)/steps
        pos = start_y
        def step(cnt=0):
            nonlocal pos
            pos += dy
            widget.place_configure(relx=0.5, rely=pos)
            if cnt<steps:
                self.root.after(delay, lambda: step(cnt+1))
            else:
                widget.place_forget()
                widget.grid()
        step()

    def abrir_simulacion(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Simulación Automática - SOFTREX")
        try:
            ventana.state('zoomed')
        except Exception:
            pass
        ventana.configure(bg=self.color_fondo)
        ventana.columnconfigure(0, weight=1)
        ttk.Label(ventana, text="🧠 Simulación Automática del Banco", style="Title.TLabel").grid(row=0, column=0, pady=18)

        frame_sim = tk.Frame(ventana, bg=self.color_secundario, padx=12, pady=12)
        frame_sim.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        frame_sim.columnconfigure(0, weight=1)
        frame_sim.rowconfigure(0, weight=1)

        self.lista_sim = tk.Listbox(frame_sim, font=("Consolas", 12), bg="#DDE6ED", fg="black")
        self.lista_sim.grid(row=0, column=0, sticky='nsew')

        vent_frame = tk.Frame(ventana, bg=self.color_fondo)
        vent_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(10,20))
        vent_frame.columnconfigure(tuple(range(5)), weight=1)
        self.sim_vent_labels = []
        for i in range(5):
            lbl = tk.Label(vent_frame, text=f"Ventanilla {i+1}: Libre", bg=self.color_tarjeta, fg='white', font=("Segoe UI",11,'bold'))
            lbl.grid(row=0, column=i, padx=8, pady=6, sticky='nsew')
            self.sim_vent_labels.append(lbl)

        btn_frame = tk.Frame(ventana, bg=self.color_fondo)
        btn_frame.grid(row=3, column=0, pady=8)
        ttk.Button(btn_frame, text="▶️ Iniciar Simulación", command=lambda: self.iniciar_simulacion(self.lista_sim)).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text="↩️ Volver", command=ventana.destroy).grid(row=0, column=1, padx=6)

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
                            self._sim_highlight_vent(i, True)
                time.sleep(1)
                for i, v in ventanillas:
                    lista_widget.insert(tk.END, f"   {contador}. ✅ {v}")
                    self.guardar_registro(v)
                    contador += 1
                    self._sim_highlight_vent(i, False)
                    lista_widget.yview(tk.END)
                    time.sleep(0.5)
            lista_widget.insert(tk.END, "\n🎉 Simulación completada.\n")
        threading.Thread(target=simular, daemon=True).start()

    def _sim_highlight_vent(self, index, active=True):
        lbl = self.sim_vent_labels[index]
        if active:
            lbl.config(text=f"Ventanilla {index+1}: Atendiendo... 🚀")
            orig = lbl['bg']
            lbl.config(bg=self._lighten(self.color_tarjeta, 22))
            self.root.after(700, lambda: lbl.config(bg=self.color_tarjeta, text=f"Ventanilla {index+1}: Libre"))
        else:
            lbl.config(text=f"Ventanilla {index+1}: Libre", bg=self.color_tarjeta)

    def abrir_manual(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Modo Manual - SOFTREX")
        try:
            ventana.state('zoomed')
        except Exception:
            pass
        ventana.configure(bg=self.color_fondo)
        ventana.columnconfigure(0, weight=1)
        ventana.rowconfigure(1, weight=1)

        ttk.Label(ventana, text="👥 Modo Manual de Atención", style="Title.TLabel").grid(row=0, column=0, pady=12)

        top = tk.Frame(ventana, bg=self.color_fondo)
        top.grid(row=1, column=0, sticky='ew', padx=20)
        top.columnconfigure((0,1,2,3,4,5,6,7), weight=1)

        form_card = Card(top, width=1200, height=120, radius=14, bg=self.color_tarjeta)
        form_card.grid(row=0, column=0, columnspan=8, sticky='ew')
        form_inner = tk.Frame(form_card, bg=self.color_tarjeta)
        form_card.create_window(8,8, anchor='nw', window=form_inner, width=form_card.width-18, height=form_card.height-18)
        form_inner.columnconfigure((0,1,2,3,4,5,6,7), weight=1)

        ttk.Label(form_inner, text="👤 Nombre:", background=self.color_tarjeta, foreground='white').grid(row=0, column=0, padx=6, pady=8, sticky='w')
        entry_nombre = ttk.Entry(form_inner, font=("Segoe UI",12))
        entry_nombre.grid(row=0, column=1, padx=6, pady=8, sticky='ew')

        ttk.Label(form_inner, text="🎯 Tipo:", background=self.color_tarjeta, foreground='white').grid(row=0, column=2, padx=6, pady=8, sticky='w')
        tipo_combo = ttk.Combobox(form_inner, values=["normal","prioritario"], state='readonly')
        tipo_combo.grid(row=0, column=3, padx=6, pady=8, sticky='ew')
        tipo_combo.current(0)

        ttk.Label(form_inner, text="💳 Movimiento:", background=self.color_tarjeta, foreground='white').grid(row=0, column=4, padx=6, pady=8, sticky='w')
        movimiento_combo = ttk.Combobox(form_inner, values=["Depósito 💰","Retiro 🏧","Transferencia 🔄"], state='readonly')
        movimiento_combo.grid(row=0, column=5, padx=6, pady=8, sticky='ew')
        movimiento_combo.current(0)

        btn_agregar = ttk.Button(form_inner, text="➕ Agregar", command=lambda: self.agregar_manual(entry_nombre, tipo_combo, movimiento_combo))
        btn_atender = ttk.Button(form_inner, text="✅ Atender", command=self.atender_manual_con_ventanillas)
        btn_reiniciar = ttk.Button(form_inner, text="🔄 Reiniciar", command=self.reiniciar_manual)
        btn_registro = ttk.Button(form_inner, text="📜 Ver Registro", command=self.abrir_registro)
        btn_borrar = ttk.Button(form_inner, text="🗑️ Borrar Registro", command=self.borrar_registro)
        btn_volver = ttk.Button(form_inner, text="↩️ Volver", command=ventana.destroy)

        btn_agregar.grid(row=0, column=6, padx=6)
        btn_atender.grid(row=0, column=7, padx=6)
        btn_reiniciar.grid(row=1, column=6, padx=6, pady=8)
        btn_registro.grid(row=1, column=4, padx=6, pady=8)
        btn_borrar.grid(row=1, column=5, padx=6, pady=8)
        btn_volver.grid(row=1, column=7, padx=6, pady=8)

        bottom = tk.Frame(ventana, bg=self.color_fondo)
        bottom.grid(row=2, column=0, sticky='nsew', padx=20, pady=12)
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)
        bottom.rowconfigure(0, weight=1)

        frame_p = tk.Frame(bottom, bg=self.color_secundario)
        frame_p.grid(row=0, column=0, sticky='nsew', padx=8, pady=8)
        frame_n = tk.Frame(bottom, bg=self.color_secundario)
        frame_n.grid(row=0, column=1, sticky='nsew', padx=8, pady=8)

        prio_card = Card(frame_p, width=600, height=420, radius=12, bg=self.color_tarjeta)
        prio_card.pack(fill='both', expand=True)
        prio_inner = tk.Frame(prio_card, bg=self.color_tarjeta)
        prio_card.create_window(8,8, anchor='nw', window=prio_inner, width=prio_card.width-18, height=prio_card.height-18)
        tk.Label(prio_inner, text="👑 Prioritarios", bg=self.color_tarjeta, fg='white', font=("Segoe UI",14,'bold')).pack(anchor='nw', padx=10, pady=8)
        self.list_prioritarios = tk.Listbox(prio_inner, bg="#FFE5EC", font=("Consolas",12))
        self.list_prioritarios.pack(fill='both', expand=True, padx=10, pady=(0,10))

        norm_card = Card(frame_n, width=600, height=420, radius=12, bg=self.color_tarjeta)
        norm_card.pack(fill='both', expand=True)
        norm_inner = tk.Frame(norm_card, bg=self.color_tarjeta)
        norm_card.create_window(8,8, anchor='nw', window=norm_inner, width=norm_card.width-18, height=norm_card.height-18)
        tk.Label(norm_inner, text="🙋 Normales", bg=self.color_tarjeta, fg='white', font=("Segoe UI",14,'bold')).pack(anchor='nw', padx=10, pady=8)
        self.list_normales = tk.Listbox(norm_inner, bg="#E3F2FD", font=("Consolas",12))
        self.list_normales.pack(fill='both', expand=True, padx=10, pady=(0,10))

        # ventanillas below lists
        vent_frame = tk.Frame(ventana, bg=self.color_fondo)
        vent_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=(6,18))
        vent_frame.columnconfigure(tuple(range(5)), weight=1)
        self.ventanillas_labels = []
        for i in range(5):
            lbl = tk.Label(vent_frame, text=f"🏦 Ventanilla {i+1}: Libre", bg=self.color_tarjeta, fg='white', font=("Segoe UI",11,'bold'))
            lbl.grid(row=0, column=i, padx=8, pady=6, sticky='nsew')
            self.ventanillas_labels.append(lbl)

    def obtener_texto_contadores_manual(self):
        return f"👑 Prioritarios hoy: {self.clientes_atendidos_manual['prioritario']}   🙋 Normales hoy: {self.clientes_atendidos_manual['normal']}"

    def actualizar_contadores_manual(self, tipo):
        hoy = date.today()
        if hoy != self.ultimo_dia_manual:
            self.clientes_atendidos_manual = {"prioritario": 0, "normal": 0}
            self.ultimo_dia_manual = hoy
        self.clientes_atendidos_manual[tipo] += 1
        try:
            self.lbl_prio.config(text=f"Prioritarios hoy: {self.clientes_atendidos_manual['prioritario']}")
            self.lbl_norm.config(text=f"Normales hoy: {self.clientes_atendidos_manual['normal']}")
            self.lbl_total.config(text=f"Total Turnos: {Cliente.contador_turno - 1}")
        except Exception:
            pass

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
        try:
            self.lbl_prio.config(text=f"Prioritarios hoy: {self.clientes_atendidos_manual['prioritario']}")
            self.lbl_norm.config(text=f"Normales hoy: {self.clientes_atendidos_manual['normal']}")
            self.lbl_total.config(text=f"Total Turnos: {Cliente.contador_turno - 1}")
        except Exception:
            pass
        self.actualizar_listas()

    def actualizar_listas(self):
        try:
            self.list_prioritarios.delete(0, tk.END)
            self.list_normales.delete(0, tk.END)
            for c in self.banco_manual.cola_prioritarios:
                self.list_prioritarios.insert(tk.END, f"👑 {c}")
            for c in self.banco_manual.cola_normales:
                self.list_normales.insert(tk.END, f"🙋 {c}")
        except Exception:
            pass

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
        frame_list.pack(expand=True, fill='both', padx=10, pady=10)
        scroll = tk.Scrollbar(frame_list)
        scroll.pack(side="right", fill="y")
        list_registro = tk.Listbox(frame_list, font=("Consolas", 11), bg="#F5F5F5", fg="black", yscrollcommand=scroll.set)
        list_registro.pack(expand=True, fill='both')
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

if __name__ == "__main__":
    root = tk.Tk()
    app = BancoUI(root)
    root.mainloop()