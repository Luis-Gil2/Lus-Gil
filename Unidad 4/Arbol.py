import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import deque
from typing import Optional, List, Dict, Tuple
import time
import math
import sys

try:
    from PIL import ImageGrab, Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

class Nodo:
    def __init__(self, valor: int):
        self.valor = valor
        self.izq: Optional['Nodo'] = None
        self.der: Optional['Nodo'] = None

class ArbolBB:
    def __init__(self):
        self.raiz: Optional[Nodo] = None

    def esVacio(self) -> bool:
        return self.raiz is None

    def insertar(self, valor: int) -> bool:
        if not self.raiz:
            self.raiz = Nodo(valor)
            return True
        actual = self.raiz
        while True:
            if valor == actual.valor:
                return False
            elif valor < actual.valor:
                if not actual.izq:
                    actual.izq = Nodo(valor)
                    return True
                actual = actual.izq
            else:
                if not actual.der:
                    actual.der = Nodo(valor)
                    return True
                actual = actual.der

    def buscar(self, valor: int) -> bool:
        n = self.raiz
        while n:
            if valor == n.valor:
                return True
            n = n.izq if valor < n.valor else n.der
        return False

    def preorden(self) -> List[int]:
        res = []
        def _p(n):
            if not n: return
            res.append(n.valor); _p(n.izq); _p(n.der)
        _p(self.raiz)
        return res

    def inorden(self) -> List[int]:
        res = []
        def _i(n):
            if not n: return
            _i(n.izq); res.append(n.valor); _i(n.der)
        _i(self.raiz)
        return res

    def postorden(self) -> List[int]:
        res = []
        def _po(n):
            if not n: return
            _po(n.izq); _po(n.der); res.append(n.valor)
        _po(self.raiz)
        return res

    def por_niveles(self) -> List[int]:
        if not self.raiz: return []
        res = []
        q = deque([self.raiz])
        while q:
            n = q.popleft()
            res.append(n.valor)
            if n.izq: q.append(n.izq)
            if n.der: q.append(n.der)
        return res

    def altura(self) -> int:
        def _h(n): return -1 if not n else 1 + max(_h(n.izq), _h(n.der))
        return _h(self.raiz)

    def contar_hojas(self) -> int:
        def _c(n):
            if not n: return 0
            if not n.izq and not n.der: return 1
            return _c(n.izq) + _c(n.der)
        return _c(self.raiz)

    def contar_nodos(self) -> int:
        def _c(n): return 0 if not n else 1 + _c(n.izq) + _c(n.der)
        return _c(self.raiz)

    def es_lleno(self) -> bool:
        def _f(n):
            if not n: return True
            if (n.izq is None) != (n.der is None): return False
            return _f(n.izq) and _f(n.der)
        return _f(self.raiz)

    def es_completo(self) -> bool:
        if not self.raiz: return True
        q = deque([self.raiz])
        fin = False
        while q:
            n = q.popleft()
            if n:
                if fin: return False
                q.append(n.izq); q.append(n.der)
            else:
                fin = True
        return True

    def eliminar(self, valor: int, metodo="predecesor") -> bool:
        self.raiz, eliminado = self._elim(self.raiz, valor, metodo)
        return eliminado

    def _elim(self, n: Optional[Nodo], v: int, metodo: str):
        if not n: return None, False
        if v < n.valor:
            n.izq, e = self._elim(n.izq, v, metodo)
            return n, e
        elif v > n.valor:
            n.der, e = self._elim(n.der, v, metodo)
            return n, e
        else:
            if not n.izq: return n.der, True
            if not n.der: return n.izq, True
            if metodo == "predecesor":
                pre = self._max(n.izq)
                n.valor = pre.valor
                n.izq, _ = self._elim(n.izq, pre.valor, metodo)
            else:
                suc = self._min(n.der)
                n.valor = suc.valor
                n.der, _ = self._elim(n.der, suc.valor, metodo)
            return n, True

    def _min(self, n):
        while n.izq: n = n.izq
        return n

    def _max(self, n):
        while n.der: n = n.der
        return n

    def vaciar(self):
        self.raiz = None

    def to_dict(self) -> Optional[Dict]:
        def _d(n):
            if not n: return None
            return {"valor": n.valor, "izq": _d(n.izq), "der": _d(n.der)}
        return _d(self.raiz)

class TreeCanvas:
    def __init__(self, canvas: tk.Canvas, node_r=22):
        self.canvas = canvas
        self.node_r_default = node_r
        self.node_r = node_r
        self.node_art: Dict[Nodo, Tuple[int, int]] = {}
        self.posiciones: Dict[Nodo, Tuple[float, float]] = {}
        self.bg = "#0f1724"
        self.edge_color = "#334155"
        self.node_fill = "#0ea5a4"
        self.node_outline = "#7c3aed"
        self.text_fill = "white"
        self.mode_horizontal = False

    def set_mode_horizontal(self, h: bool):
        self.mode_horizontal = h

    def _calc_positions(self, arbol: ArbolBB, width: int, height: int):
        posiciones = {}
        if arbol.esVacio(): return posiciones
        def calc_pos(n, x, y, dx):
            if not n: return
            posiciones[n] = (x, y)
            if self.mode_horizontal:
                calc_pos(n.izq, x, y - dx, dx / 1.8)
                calc_pos(n.der, x, y + dx, dx / 1.8)
            else:
                calc_pos(n.izq, x - dx, y + 90, dx / 1.8)
                calc_pos(n.der, x + dx, y + 90, dx / 1.8)
        if self.mode_horizontal:
            start_x = width // 2
            start_y = height // 2
            calc_pos(arbol.raiz, start_x, start_y, 180)
        else:
            calc_pos(arbol.raiz, width // 2, 60, max(60, width // 6))
        return posiciones

    def draw_tree(self, arbol: ArbolBB, animate_new: Optional[int] = None, animate_del: Optional[int] = None):
        w = int(self.canvas.winfo_width() or self.canvas['width'])
        h = int(self.canvas.winfo_height() or self.canvas['height'])
        self.canvas.configure(bg=self.bg)
        self.node_r = self.node_r_default
        nuevas_pos = self._calc_positions(arbol, w, h)
        self.canvas.delete("edge")
        for n, (x, y) in nuevas_pos.items():
            if n.izq and n.izq in nuevas_pos:
                x2, y2 = nuevas_pos[n.izq]
                self.canvas.create_line(x, y, x2, y2, width=2, fill=self.edge_color, tags="edge")
            if n.der and n.der in nuevas_pos:
                x2, y2 = nuevas_pos[n.der]
                self.canvas.create_line(x, y, x2, y2, width=2, fill=self.edge_color, tags="edge")
        antiguos = set(self.posiciones.keys())
        actuales = set(nuevas_pos.keys())
        añadidos = [n for n in actuales - antiguos]
        eliminados = [n for n in antiguos - actuales]
        pasos = 12
        duration = 220
        delay = duration // pasos if pasos else 20
        posiciones_inicial = dict(self.posiciones)
        for n in añadidos:
            self.node_art[n] = (None, None)
        self.posiciones = nuevas_pos

        def anim_move(step=0):
            t = step / pasos
            self.canvas.delete("node")
            for n, (x_target, y_target) in self.posiciones.items():
                if n in posiciones_inicial:
                    x0, y0 = posiciones_inicial[n]
                    x = x0 + (x_target - x0) * t
                    y = y0 + (y_target - y0) * t
                else:
                    x, y = x_target, y_target
                r = int(self.node_r * (0.2 + 0.8 * t))
                oval = self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                               fill=self.node_fill, outline=self.node_outline, width=2, tags=("node",))
                txt = self.canvas.create_text(x, y, text=str(n.valor), fill=self.text_fill, font=("Segoe UI", max(8, r//2), "bold"), tags=("node",))
                self.node_art[n] = (oval, txt)
            for n in eliminados:
                if n in posiciones_inicial:
                    x0, y0 = posiciones_inicial[n]
                    r_del = int(self.node_r * (1 - 0.9 * t))
                    oval_d = self.canvas.create_oval(x0 - r_del, y0 - r_del, x0 + r_del, y0 + r_del,
                                                     fill=self.node_fill, outline=self.node_outline, width=2, tags=("node",))
                    txt_d = self.canvas.create_text(x0, y0, text=str(n.valor), fill=self.text_fill, font=("Segoe UI", max(8, r_del//2), "bold"), tags=("node",))
            if step < pasos:
                self.canvas.after(delay, lambda: anim_move(step + 1))
            else:
                if animate_new is not None:
                    for n in añadidos:
                        if n.valor == animate_new:
                            self._animate_grow_node(n)
                            break
                if animate_del is not None:
                    for n in eliminados:
                        if n.valor == animate_del:
                            self._animate_shrink_removed(n, posiciones_inicial.get(n, None))
                            break
        anim_move(0)

    def _animate_grow_node(self, nodo: Nodo):
        pos = self.posiciones.get(nodo)
        if not pos: return
        x, y = pos
        steps = 10
        delay = 20
        def step(i=0):
            t = i / steps
            r = int(self.node_r * (0.1 + 0.9 * t))
            self.canvas.delete("grow")
            oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.node_fill,
                                           outline=self.node_outline, width=2, tags=("grow",))
            txt = self.canvas.create_text(x, y, text=str(nodo.valor), fill=self.text_fill, font=("Segoe UI", max(8, r//2), "bold"), tags=("grow",))
            if i < steps:
                self.canvas.after(delay, lambda: step(i + 1))
            else:
                self.canvas.delete("grow")
        step(0)

    def _animate_shrink_removed(self, nodo: Nodo, old_pos: Optional[Tuple[float, float]]):
        if not old_pos: return
        x, y = old_pos
        steps = 10
        delay = 20
        def step(i=0):
            t = i / steps
            r = int(self.node_r * (1 - 0.9 * t))
            self.canvas.delete("shrink")
            if r > 1:
                oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.node_fill,
                                               outline=self.node_outline, width=2, tags=("shrink",))
                txt = self.canvas.create_text(x, y, text=str(nodo.valor), fill=self.text_fill, font=("Segoe UI", max(8, r//2), "bold"), tags=("shrink",))
                self.canvas.after(delay, lambda: step(i + 1))
            else:
                self.canvas.delete("shrink")
        step(0)

    def highlight_node(self, nodo: Nodo, duration=400):
        if nodo not in self.posiciones:
            return
        x, y = self.posiciones[nodo]
        r = self.node_r + 4
        oval = self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                       outline="#facc15", width=4, tags="highlight")
        self.canvas.after(duration, lambda: self.canvas.delete("highlight"))

    def export_as_image(self, filename: str):
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        bbox = (x, y, x + w, y + h)
        try:
            if PIL_AVAILABLE:
                img = ImageGrab.grab(bbox)
                img.save(filename)
                return True, None
            else:
                ps_file = filename + ".ps"
                self.canvas.postscript(file=ps_file, colormode='color')
                return True, "Guardado como PostScript (instale Pillow para PNG)."
        except Exception as e:
            return False, str(e)

# -------------------------
# Interfaz Gráfica
# -------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Árbol Binario de Búsqueda — Estilo VS Code (Oscuro)")
        self.geometry("1200x720")
        self.bg = "#071024"
        self.style_primary = "#0b1220"
        self.config(bg=self.bg)

        self.arbol = ArbolBB()
        self.save_icon = "💾"
        self.current_view_horizontal = False

        self._crear_ui()
        self.update_idletasks()
        self._update_canvas()

    def _crear_ui(self):
        top_bar = tk.Frame(self, bg="#061422", height=52)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        title = tk.Label(top_bar, text=" Árbol Binario de Búsqueda", bg="#061422", fg="#9ae6b4",
                         font=("Segoe UI", 14, "bold"))
        title.pack(side=tk.LEFT, padx=12)
        btn_save = ttk.Button(top_bar, text=f"{self.save_icon} Guardar", command=self._menu_guardar)
        btn_save.pack(side=tk.RIGHT, padx=8, pady=8)
        self.btn_mode = ttk.Button(top_bar, text="Acostado: OFF", command=self._toggle_mode)
        self.btn_mode.pack(side=tk.RIGHT, padx=8, pady=8)
        btn_update = ttk.Button(top_bar, text="Actualizar", command=self._update_canvas)
        btn_update.pack(side=tk.RIGHT, padx=8, pady=8)

        main = tk.Frame(self, bg=self.bg)
        main.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        left = tk.Frame(main, bg="#071824", width=320, padx=10, pady=10)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)
        right = tk.Frame(main, bg=self.bg, padx=10, pady=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        lbl = tk.Label(left, text="Gestor de Árbol (Oscuro)", bg="#071824", fg="#cbd5e1", font=("Segoe UI", 13, "bold"))
        lbl.pack(pady=(4, 8))
        self.entry_val = ttk.Entry(left, font=("Segoe UI", 12))
        self.entry_val.pack(fill=tk.X, pady=6)
        self.entry_val.insert(0, "Valor entero")

        botones = [
            ("Insertar elemento", self._insertar),
            ("Buscar elemento", self._buscar),
            ("Eliminar (Predecesor)", lambda: self._eliminar("predecesor")),
            ("Eliminar (Sucesor)", lambda: self._eliminar("sucesor")),
            ("Vaciar árbol", self._vaciar),
            ("PreOrden", lambda: self._recorrido('pre')),
            ("InOrden", lambda: self._recorrido('in')),
            ("PostOrden", lambda: self._recorrido('post')),
            ("Por niveles", lambda: self._recorrido('niv')),
            ("Altura", self._altura),
            ("Hojas", self._hojas),
            ("Nodos", self._nodos),
            ("¿Es completo?", self._completo),
            ("¿Es lleno?", self._lleno),
        ]
        for t, c in botones:
            ttk.Button(left, text=t, command=c).pack(fill=tk.X, pady=2)

        self.txt_log = tk.Text(left, height=8, bg="#0f1724", fg="#f1f5f9", font=("Consolas", 10))
        self.txt_log.pack(fill=tk.BOTH, expand=True, pady=8)

        self.canvas = tk.Canvas(right, bg="#0f1724")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.tree = TreeCanvas(self.canvas)

    def _val(self) -> Optional[int]:
        try:
            v = int(self.entry_val.get())
            return v
        except ValueError:
            self._log("⚠ Valor inválido")
            return None

    def _log(self, texto: str):
        self.txt_log.insert(tk.END, texto + "\n")
        self.txt_log.see(tk.END)

    def _update_canvas(self, animate_new=None, animate_del=None):
        self.tree.draw_tree(self.arbol, animate_new=animate_new, animate_del=animate_del)

    def _toggle_mode(self):
        self.current_view_horizontal = not self.current_view_horizontal
        self.tree.set_mode_horizontal(self.current_view_horizontal)
        self.btn_mode.config(text=f"Acostado: {'ON' if self.current_view_horizontal else 'OFF'}")
        self._update_canvas()

    def _insertar(self):
        v = self._val()
        if v is not None:
            inserted = self.arbol.insertar(v)
            self._log(f"Insertar {v}: {'OK' if inserted else 'Ya existe'}")
            if inserted:
                self._update_canvas(animate_new=v)

    def _buscar(self):
        v = self._val()
        if v is not None:
            found = self.arbol.buscar(v)
            self._log(f"Buscar {v}: {'Encontrado' if found else 'No encontrado'}")

    def _vaciar(self):
        self.arbol.vaciar()
        self._update_canvas()
        self._log("Árbol vaciado")

    def _recorrido(self, tipo):
        r = []
        if tipo == 'pre': r = self.arbol.preorden()
        elif tipo == 'in': r = self.arbol.inorden()
        elif tipo == 'post': r = self.arbol.postorden()
        elif tipo == 'niv': r = self.arbol.por_niveles()
        self._log(f"{tipo.upper()} => {r}")

    def _altura(self):
        h = self.arbol.altura()
        self._log(f"Altura: {h}")

    def _hojas(self):
        h = self.arbol.contar_hojas()
        self._log(f"Hojas: {h}")

    def _nodos(self):
        n = self.arbol.contar_nodos()
        self._log(f"Nodos: {n}")

    def _completo(self):
        r = self.arbol.es_completo()
        self._log(f"¿Es completo? {'Sí' if r else 'No'}")

    def _lleno(self):
        r = self.arbol.es_lleno()
        self._log(f"¿Es lleno? {'Sí' if r else 'No'}")

    def _get_nodo_por_valor(self, valor: int) -> Optional[Nodo]:
        n = self.arbol.raiz
        while n:
            if n.valor == valor: return n
            n = n.izq if valor < n.valor else n.der
        return None

    def _eliminar(self, metodo):
        v = self._val()
        if v is not None:
            nodo_a_eliminar = self._get_nodo_por_valor(v)
            if not nodo_a_eliminar:
                self._log(f"Eliminar {v}: No encontrado")
                return
            self.tree.highlight_node(nodo_a_eliminar)
            self.after(400, lambda: self._confirm_delete(v, metodo))

    def _confirm_delete(self, v, metodo):
        existed = self.arbol.buscar(v)
        e = self.arbol.eliminar(v, metodo)
        self._log(f"Eliminar {v}: {'Eliminado' if e else 'No encontrado'}")
        if existed and e:
            self._update_canvas(animate_del=v)

    def _menu_guardar(self):
        filetypes = [('PNG Image', '*.png'), ('JSON', '*.json')]
        fname = filedialog.asksaveasfilename(title="Guardar", defaultextension=".png", filetypes=filetypes)
        if not fname: return
        if fname.endswith(".png"):
            ok, msg = self.tree.export_as_image(fname)
            if ok: self._log(f"Imagen guardada en {fname}")
            else: self._log(f"Error guardar imagen: {msg}")
        elif fname.endswith(".json"):
            data = self.arbol.to_dict()
            with open(fname, 'w') as f:
                json.dump(data, f, indent=2)
            self._log(f"Árbol guardado en {fname}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
