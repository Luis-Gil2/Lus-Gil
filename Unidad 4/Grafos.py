"""
Grafos.py

Interfaz oscura con ttkbootstrap, acordeones (3 secciones), canvas (matplotlib + networkx)
y panel de salida (log) que no se oculta. Aristas dirigidas dibujadas con FancyArrowPatch
para asegurar una sola flecha por arista. Ventana totalmente redimensionable y
actualización automática al modificar el grafo.

Ejecución:
    pip install ttkbootstrap networkx matplotlib
    python Grafos.py
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap import Style
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyArrowPatch
import math

class GraphApp:
    def __init__(self):
        # Estilo oscuro
        self.style = Style(theme="darkly")
        self.root = self.style.master
        self.root.title("Grafo Interactivo — Acordeón (Dark)")
        self.root.geometry("1200x720")
        self.root.minsize(900, 600)

        # Modelo
        self.G = nx.Graph()
        self.directed = False

        # Layout: left controls, center canvas, bottom log
        self._build_layout()
        self._build_left_panel()
        self._build_center_canvas()
        self._build_log_panel()

        # Dibujar estado inicial
        self._draw_graph()
        self._log("Aplicación lista — ventana redimensionable, autoredibujo activo.")

    # -------------------------
    # Construcción de la UI
    # -------------------------
    def _build_layout(self):
        # Frames principales
        self.left_frame = tb.Frame(self.root, width=340)
        self.left_frame.pack(side="left", fill="y", padx=(12,6), pady=12)

        self.center_frame = tb.Frame(self.root)
        self.center_frame.pack(side="left", fill="both", expand=True, padx=(6,12), pady=12)

        self.log_frame = tb.Frame(self.root, height=140)
        self.log_frame.pack(side="bottom", fill="x", padx=12, pady=(0,12))

        # Asegurar que center_frame expanda al redimensionar
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

    def _build_left_panel(self):
        tb.Label(self.left_frame, text="Controles", font=("Helvetica", 16, "bold")).pack(anchor="w", pady=(4,8), padx=8)

        # Switch tipo de grafo
        tipo_frame = tb.Frame(self.left_frame)
        tipo_frame.pack(fill="x", padx=8, pady=(0,8))
        tb.Label(tipo_frame, text="Grafo dirigido:", font=("Helvetica", 10)).pack(side="left")
        self.dir_var = tk.BooleanVar(value=False)
        tb.Checkbutton(tipo_frame, variable=self.dir_var, bootstyle="success-round-toggle", command=self._toggle_directed).pack(side="left", padx=8)

        # Entradas para vértices y aristas (sin placeholder_text)
        tb.Separator(self.left_frame).pack(fill="x", padx=8, pady=(4,8))
        tb.Label(self.left_frame, text="Agregar vértice (id):", font=("Helvetica", 10)).pack(anchor="w", padx=8)
        self.entry_vertex = tb.Entry(self.left_frame)
        self.entry_vertex.pack(fill="x", padx=8, pady=(2,6))
        tb.Button(self.left_frame, text="Agregar vértice", command=self._add_vertex, bootstyle="primary").pack(fill="x", padx=8)

        tb.Label(self.left_frame, text="Agregar arista (u,v):", font=("Helvetica", 10)).pack(anchor="w", padx=8, pady=(8,2))
        frm_uv = tb.Frame(self.left_frame)
        frm_uv.pack(fill="x", padx=8)
        self.entry_u = tb.Entry(frm_uv)
        self.entry_v = tb.Entry(frm_uv)
        self.entry_u.pack(side="left", fill="x", expand=True, padx=(0,6))
        self.entry_v.pack(side="left", fill="x", expand=True)
        tb.Button(self.left_frame, text="Agregar (no dirigida)", command=self._add_edge, bootstyle="outline-primary").pack(fill="x", padx=8, pady=(6,2))
        tb.Button(self.left_frame, text="Agregar dirigida (u -> v)", command=self._add_edge_dir, bootstyle="success").pack(fill="x", padx=8, pady=(0,6))

        tb.Separator(self.left_frame).pack(fill="x", padx=8, pady=(6,8))

        # Acordeón: 3 secciones
        self._make_accordion()

        # Botones adicionales
        tb.Button(self.left_frame, text="Refrescar listas", command=self._refresh_lists, bootstyle="info").pack(fill="x", padx=8, pady=(8,4))
        tb.Button(self.left_frame, text="Limpiar grafo", command=self._clear_graph, bootstyle="danger-outline").pack(fill="x", padx=8)

        # Listboxes para selección
        tb.Label(self.left_frame, text="Vértices:", font=("Helvetica", 10)).pack(anchor="w", padx=8, pady=(10,2))
        self.list_vertices = tk.Listbox(self.left_frame, height=6, selectmode=tk.SINGLE)
        self.list_vertices.pack(fill="x", padx=8)

        tb.Label(self.left_frame, text="Aristas (u,v):", font=("Helvetica", 10)).pack(anchor="w", padx=8, pady=(8,2))
        self.list_edges = tk.Listbox(self.left_frame, height=6, selectmode=tk.SINGLE)
        self.list_edges.pack(fill="x", padx=8, pady=(0,6))

    def _make_accordion(self):
        # Helper para crear secciones plegables
        def make_section(title, parent):
            header = tb.Frame(parent)
            header.pack(fill="x", padx=8, pady=(4,0))
            lbl = tb.Label(header, text=title, font=("Helvetica", 11, "bold"))
            lbl.pack(side="left")
            btn = tb.Button(header, text="-", width=3)  # abierto por defecto
            btn.pack(side="right")
            content = tb.Frame(parent)
            content.pack(fill="x", padx=8, pady=(0,6))
            content.is_shown = True
            def toggle():
                if content.is_shown:
                    content.pack_forget()
                    btn.configure(text="+")
                    content.is_shown = False
                else:
                    content.pack(fill="x", padx=8, pady=(0,6))
                    btn.configure(text="-")
                    content.is_shown = True
            btn.configure(command=toggle)
            return content

        # Sección 1: Operaciones Generales
        sec1 = make_section("Operaciones Generales", self.left_frame)
        tb.Button(sec1, text="numVertices()", command=self._op_num_vertices).pack(fill="x", pady=3)
        tb.Button(sec1, text="numAristas()", command=self._op_num_aristas).pack(fill="x", pady=3)
        tb.Button(sec1, text="vertices()", command=self._op_vertices).pack(fill="x", pady=3)
        tb.Button(sec1, text="aristas()", command=self._op_aristas).pack(fill="x", pady=3)
        tb.Button(sec1, text="grado(v) (selecciona vértice)", command=self._op_grado).pack(fill="x", pady=3)
        tb.Button(sec1, text="verticesAdyacentes(v)", command=self._op_vertices_adyacentes).pack(fill="x", pady=3)
        tb.Button(sec1, text="aristasIncidentes(v)", command=self._op_aristas_incidentes).pack(fill="x", pady=3)
        tb.Button(sec1, text="verticesFinales(e) (selecciona arista)", command=self._op_vertices_finales).pack(fill="x", pady=3)
        tb.Button(sec1, text="opuesto(v,e) (selecciona vértice y arista)", command=self._op_opuesto).pack(fill="x", pady=3)
        tb.Button(sec1, text="esAdyacente(v,w) (usa entradas u/v)", command=self._op_es_adyacente).pack(fill="x", pady=3)

        # Sección 2: Operaciones con aristas dirigidas
        sec2 = make_section("Operaciones con aristas dirigidas", self.left_frame)
        tb.Button(sec2, text="aristasDirigidas()", command=self._op_aristas_dirigidas).pack(fill="x", pady=3)
        tb.Button(sec2, text="aristasNodirigidas()", command=self._op_aristas_no_dirigidas).pack(fill="x", pady=3)
        tb.Button(sec2, text="gradoEnt(v) (selecciona vértice)", command=self._op_grado_ent).pack(fill="x", pady=3)
        tb.Button(sec2, text="gradoSalida(v) (selecciona vértice)", command=self._op_grado_sal).pack(fill="x", pady=3)
        tb.Button(sec2, text="aristasIncidentesEnt(v)", command=self._op_aristas_inc_ent).pack(fill="x", pady=3)
        tb.Button(sec2, text="aristasIncidentesSal(v)", command=self._op_aristas_inc_sal).pack(fill="x", pady=3)
        tb.Button(sec2, text="verticesAdyacentesEnt(v)", command=self._op_vertices_ady_ent).pack(fill="x", pady=3)
        tb.Button(sec2, text="verticesAdyacentesSal(v)", command=self._op_vertices_ady_sal).pack(fill="x", pady=3)
        tb.Button(sec2, text="destino(e) / origen(e) (selecciona arista)", command=self._op_destino_origen).pack(fill="x", pady=3)
        tb.Button(sec2, text="esDirigida(e) (selecciona arista)", command=self._op_es_dirigida_e).pack(fill="x", pady=3)

        # Sección 3: Operaciones de actualización
        sec3 = make_section("Operaciones para actualizar grafos", self.left_frame)
        tb.Button(sec3, text="insertaVertice(o) (usa entrada)", command=self._add_vertex).pack(fill="x", pady=3)
        tb.Button(sec3, text="insertaArista(v,w,o) (usa entradas u/v)", command=self._add_edge).pack(fill="x", pady=3)
        tb.Button(sec3, text="insertaAristaDirigida(v,w,o)", command=self._add_edge_dir).pack(fill="x", pady=3)
        tb.Button(sec3, text="eliminaVertice(v) (selecciona vértice)", command=self._op_delete_vertex).pack(fill="x", pady=3)
        tb.Button(sec3, text="eliminaArista(e) (selecciona arista)", command=self._op_delete_edge).pack(fill="x", pady=3)
        tb.Button(sec3, text="convierteNoDirigida(e) (convierte todo)", command=self._op_convert_to_undirected).pack(fill="x", pady=3)
        tb.Button(sec3, text="invierteDireccion(e) (selecciona arista)", command=self._op_invert_edge).pack(fill="x", pady=3)
        tb.Button(sec3, text="asignaDireccionDesde(e,v) (selecciona arista)", command=self._op_assign_from).pack(fill="x", pady=3)
        tb.Button(sec3, text="asignaDireccionA(e,v) (selecciona arista)", command=self._op_assign_to).pack(fill="x", pady=3)

    def _build_center_canvas(self):
        # Matplotlib figure dentro del center_frame
        self.fig, self.ax = plt.subplots(figsize=(6.5,6))
        self.fig.patch.set_facecolor("#22252a")
        self.ax.set_facecolor("#22252a")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.center_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _build_log_panel(self):
        tb.Label(self.log_frame, text="Salida / Log:", font=("Helvetica", 10, "bold")).pack(anchor="w", padx=8, pady=(8,0))
        self.txt_log = tk.Text(self.log_frame, height=6, bg="#0b1020", fg="#e6eef8", wrap="word")
        self.txt_log.pack(fill="x", padx=8, pady=(4,8))
        scrollbar = tk.Scrollbar(self.log_frame, command=self.txt_log.yview)
        scrollbar.place(relx=0.985, rely=0.05, relheight=0.9)
        self.txt_log.config(yscrollcommand=scrollbar.set)

    # -------------------------
    # Utilidades: log / listas
    # -------------------------
    def _log(self, *msgs):
        for m in msgs:
            self.txt_log.insert(tk.END, f"{m}\n")
        self.txt_log.see(tk.END)

    def _refresh_lists(self):
        self.list_vertices.delete(0, tk.END)
        for n in sorted(self.G.nodes()):
            self.list_vertices.insert(tk.END, n)
        self.list_edges.delete(0, tk.END)
        for u, v in sorted(self.G.edges()):
            self.list_edges.insert(tk.END, f"{u},{v}")

    # -------------------------
    # Operaciones: añadir / eliminar / toggle
    # -------------------------
    def _toggle_directed(self):
        new = self.dir_var.get()
        if new and not self.directed:
            self.G = nx.DiGraph(self.G)
            self.directed = True
            self._log("Cambiado a grafo DIRIGIDO")
        elif not new and self.directed:
            self.G = nx.Graph(self.G)
            self.directed = False
            self._log("Cambiado a grafo NO DIRIGIDO")
        self._draw_graph()
        self._refresh_lists()

    def _add_vertex(self):
        v = self.entry_vertex.get().strip()
        if not v:
            self._log("Error: id de vértice vacío")
            return
        if v in self.G:
            self._log(f"Vértice '{v}' ya existe")
            return
        self.G.add_node(v)
        self.entry_vertex.delete(0, tk.END)
        self._log(f"Vértice '{v}' agregado")
        self._refresh_lists()
        self._draw_graph()

    def _add_edge(self):
        u = self.entry_u.get().strip()
        v = self.entry_v.get().strip()
        if not u or not v:
            self._log("Error: origen o destino vacío")
            return
        if u not in self.G:
            self.G.add_node(u); self._log(f"Vértice '{u}' creado automáticamente")
        if v not in self.G:
            self.G.add_node(v); self._log(f"Vértice '{v}' creado automáticamente")
        self.G.add_edge(u, v)
        if self.directed:
            self._log(f"Arista dirigida {u} -> {v} agregada")
        else:
            self._log(f"Arista no dirigida ({u}, {v}) agregada")
        self._refresh_lists()
        self._draw_graph()

    def _add_edge_dir(self):
        u = self.entry_u.get().strip()
        v = self.entry_v.get().strip()
        if not u or not v:
            self._log("Error: origen o destino vacío")
            return
        if not self.directed:
            self.dir_var.set(True)
            self._toggle_directed()
        if u not in self.G:
            self.G.add_node(u); self._log(f"Vértice '{u}' creado automáticamente")
        if v not in self.G:
            self.G.add_node(v); self._log(f"Vértice '{v}' creado automáticamente")
        self.G.add_edge(u, v)
        self._log(f"Arista dirigida {u} -> {v} agregada")
        self._refresh_lists()
        self._draw_graph()

    def _clear_graph(self):
        self.G = nx.Graph()
        self.directed = False
        self.dir_var.set(False)
        self._log("Grafo limpiado")
        self._draw_graph()
        self._refresh_lists()

    # -------------------------
    # Implementación de operaciones solicitadas
    # -------------------------
    # -- Generales --
    def _op_num_vertices(self):
        self._log("numVertices() →", self.G.number_of_nodes())

    def _op_num_aristas(self):
        self._log("numAristas() →", self.G.number_of_edges())

    def _op_vertices(self):
        self._log("vertices() →", list(self.G.nodes()))

    def _op_aristas(self):
        self._log("aristas() →", list(self.G.edges()))

    def _op_grado(self):
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Seleccione un vértice para grado(v)")
            return
        v = self.list_vertices.get(sel[0])
        g = (self.G.in_degree(v) + self.G.out_degree(v)) if self.directed else self.G.degree(v)
        self._log(f"grado({v}) → {g}")

    def _op_vertices_adyacentes(self):
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Seleccione un vértice para verticesAdyacentes(v)")
            return
        v = self.list_vertices.get(sel[0])
        self._log(f"verticesAdyacentes({v}) →", list(self.G.neighbors(v)))

    def _op_aristas_incidentes(self):
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Seleccione un vértice para aristasIncidentes(v)")
            return
        v = self.list_vertices.get(sel[0])
        self._log(f"aristasIncidentes({v}) →", list(self.G.edges(v)))

    def _op_vertices_finales(self):
        sel = self.list_edges.curselection()
        if not sel:
            self._log("Seleccione una arista para verticesFinales(e)")
            return
        s = self.list_edges.get(sel[0]); u, v = s.split(",",1)
        self._log(f"verticesFinales(({u},{v})) → [{u}, {v}]")

    def _op_opuesto(self):
        selv = self.list_vertices.curselection()
        sele = self.list_edges.curselection()
        if not selv or not sele:
            self._log("Seleccione vértice y arista para opuesto(v,e)")
            return
        v = self.list_vertices.get(selv[0])
        s = self.list_edges.get(sele[0]); u, w = s.split(",",1)
        if v == u:
            self._log(f"opuesto({v},({u},{w})) → {w}")
        elif v == w:
            self._log(f"opuesto({v},({u},{w})) → {u}")
        else:
            self._log("Error: v no es extremo de la arista")

    def _op_es_adyacente(self):
        u = self.entry_u.get().strip()
        v = self.entry_v.get().strip()
        if not u or not v:
            self._log("Introduzca u y v en las entradas para esAdyacente(v,w)")
            return
        self._log(f"esAdyacente({u},{v}) → {self.G.has_edge(u, v)}")

    # -- Dirigidas --
    def _op_aristas_dirigidas(self):
        if not self.directed:
            self._log("Grafo no es dirigido → aristasDirigidas() → []")
            return
        self._log("aristasDirigidas() →", list(self.G.edges()))

    def _op_aristas_no_dirigidas(self):
        if self.directed:
            self._log("Grafo dirigido → aristasNoDirigidas() → []")
        else:
            self._log("aristasNoDirigidas() →", list(self.G.edges()))

    def _op_grado_ent(self):
        if not self.directed:
            self._log("Operación válida solo en grafos dirigidos")
            return
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Selecciona vértice para gradoEnt(v)")
            return
        v = self.list_vertices.get(sel[0])
        self._log(f"gradoEnt({v}) → {self.G.in_degree(v)}")

    def _op_grado_sal(self):
        if not self.directed:
            self._log("Operación válida solo en grafos dirigidos")
            return
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Selecciona vértice para gradoSalida(v)")
            return
        v = self.list_vertices.get(sel[0])
        self._log(f"gradoSalida({v}) → {self.G.out_degree(v)}")

    def _op_aristas_inc_ent(self):
        if not self.directed:
            self._log("Operación válida solo en grafos dirigidos")
            return
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Selecciona vértice")
            return
        v = self.list_vertices.get(sel[0])
        self._log(f"aristasIncidentesEnt({v}) →", list(self.G.in_edges(v)))

    def _op_aristas_inc_sal(self):
        if not self.directed:
            self._log("Operación válida solo en grafos dirigidos")
            return
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Selecciona vértice")
            return
        v = self.list_vertices.get(sel[0])
        self._log(f"aristasIncidentesSal({v}) →", list(self.G.out_edges(v)))

    def _op_vertices_ady_ent(self):
        if not self.directed:
            self._log("Operación válida solo en grafos dirigidos")
            return
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Selecciona vértice")
            return
        v = self.list_vertices.get(sel[0])
        self._log(f"verticesAdyacentesEnt({v}) →", [u for u,_ in self.G.in_edges(v)])

    def _op_vertices_ady_sal(self):
        if not self.directed:
            self._log("Operación válida solo en grafos dirigidos")
            return
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Selecciona vértice")
            return
        v = self.list_vertices.get(sel[0])
        self._log(f"verticesAdyacentesSal({v}) →", [w for _,w in self.G.out_edges(v)])

    def _op_destino_origen(self):
        sel = self.list_edges.curselection()
        if not sel:
            self._log("Selecciona una arista")
            return
        s = self.list_edges.get(sel[0]); u, v = s.split(",",1)
        self._log(f"origen(({u},{v})) → {u}")
        self._log(f"destino(({u},{v})) → {v}")

    def _op_es_dirigida_e(self):
        sel = self.list_edges.curselection()
        if not sel:
            self._log("Selecciona una arista")
            return
        s = self.list_edges.get(sel[0]); u, v = s.split(",",1)
        self._log(f"esDirigida(({u},{v})) → {self.directed}")

    # -- Actualización --
    def _op_delete_vertex(self):
        sel = self.list_vertices.curselection()
        if not sel:
            self._log("Selecciona vértice para eliminar")
            return
        v = self.list_vertices.get(sel[0])
        if v in self.G:
            self.G.remove_node(v)
            self._log(f"Vértice '{v}' eliminado (y aristas incidentes)")
            self._refresh_lists()
            self._draw_graph()
        else:
            self._log("Vértice no encontrado")

    def _op_delete_edge(self):
        sel = self.list_edges.curselection()
        if not sel:
            self._log("Selecciona arista para eliminar")
            return
        s = self.list_edges.get(sel[0]); u, v = s.split(",",1)
        if self.G.has_edge(u, v):
            self.G.remove_edge(u, v)
            self._log(f"Arista ({u},{v}) eliminada")
            self._refresh_lists()
            self._draw_graph()
        else:
            self._log("Arista no encontrada")

    def _op_convert_to_undirected(self):
        self.G = nx.Graph(self.G)
        self.directed = False
        self.dir_var.set(False)
        self._log("Convertido a grafo NO DIRIGIDO")
        self._refresh_lists()
        self._draw_graph()

    def _op_invert_edge(self):
        if not self.directed:
            self._log("Solo válido en grafos dirigidos")
            return
        sel = self.list_edges.curselection()
        if not sel:
            self._log("Selecciona arista para invertir")
            return
        s = self.list_edges.get(sel[0]); u, v = s.split(",",1)
        if self.G.has_edge(u, v):
            attrs = dict(self.G[u][v])
            self.G.remove_edge(u, v)
            self.G.add_edge(v, u, **attrs)
            self._log(f"Arista invertida: {v} -> {u}")
            self._refresh_lists()
            self._draw_graph()
        else:
            self._log("Arista no encontrada")

    def _op_assign_from(self):
        sel = self.list_edges.curselection()
        if not sel:
            self._log("Selecciona arista para asignar dirección desde")
            return
        s = self.list_edges.get(sel[0]); u, v = s.split(",",1)
        if not self.directed:
            self.dir_var.set(True); self._toggle_directed()
        if self.G.has_edge(v, u):
            self.G.remove_edge(v, u)
        self.G.add_edge(u, v)
        self._log(f"Asignada dirección desde {u} hacia {v}")
        self._refresh_lists()
        self._draw_graph()

    def _op_assign_to(self):
        self._op_assign_from()

    # -------------------------
    # Dibujado: una flecha por arista dirigida
    # -------------------------
    def _draw_graph(self):
        self.ax.clear()
        if len(self.G.nodes) == 0:
            self.ax.text(0.5, 0.5, "Grafo vacío", color="#a8b0c0", ha="center", va="center", fontsize=16)
            self.ax.set_axis_off()
            self.canvas.draw()
            return

        pos = nx.spring_layout(self.G, seed=42)

        # nodos y etiquetas
        nx.draw_networkx_nodes(self.G, pos, ax=self.ax, node_color="#7C3AED", node_size=700, edgecolors="#0b1220")
        nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_color="white")

        edge_color = "#94A3B8"

        if self.directed:
            # dibujar una flecha por cada arista (u->v)
            for (u, v) in self.G.edges():
                x1, y1 = pos[u]; x2, y2 = pos[v]
                dx, dy = x2 - x1, y2 - y1
                dist = math.hypot(dx, dy)
                if dist == 0:
                    continue
                shrink = 0.12  # espacio para no tocar centros de nodos
                start = (x1 + shrink * dx, y1 + shrink * dy)
                end = (x2 - shrink * dx, y2 - shrink * dy)
                arrow = FancyArrowPatch(start, end,
                                        arrowstyle='-|>', mutation_scale=18,
                                        linewidth=2, color=edge_color,
                                        shrinkA=0, shrinkB=0,
                                        connectionstyle="arc3,rad=0.0")
                self.ax.add_patch(arrow)
        else:
            nx.draw_networkx_edges(self.G, pos, ax=self.ax, edge_color=edge_color, width=2)

        self.ax.set_axis_off()
        self.canvas.draw()
        self._refresh_lists()

    # Ejecutar app
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GraphApp()
    app.run()