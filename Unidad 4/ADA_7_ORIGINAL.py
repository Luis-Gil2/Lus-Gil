"""
recorrido_estados_grafos.py

Versión corregida y robusta.

Mejoras principales realizadas:
- El botón "Abrir mapa (HTML)" ahora usa la ruta absoluta y muestra mensajes claros si el
  archivo no existe o no se puede abrir.
- Si `folium` no está disponible, se genera un HTML de respaldo con la lista de estados y
  las rutas (para que siempre haya algo que abrir).
- El mapa se abre automáticamente después de generarse (intento seguro con webbrowser).
- Manejo robusto de imports y mensajes (compatibilidad customtkinter <-> tkinter).
- La ventana muestra mensajes en cuadros (messagebox) cuando algo falla.
- Mejoras menores en panning/zoom de la imagen (compatibilidad multiplataforma) y en la
  creación de la imagen del grafo.

Ejecuta: python recorrido_estados_grafos.py
Recomendado: pip install pillow networkx matplotlib folium

"""

from math import radians, sin, cos, asin, sqrt
from itertools import permutations
import os, sys, webbrowser

# GUI framework: preferimos customtkinter si está presente
try:
    import customtkinter as ctk
    TK_CUSTOM = True
    # provide messagebox alias
    from tkinter import messagebox as tk_messagebox
except Exception:
    import tkinter as ctk
    from tkinter import ttk
    from tkinter import messagebox as tk_messagebox
    TK_CUSTOM = False

# Visualización y utilidades
try:
    import networkx as nx
    HAS_NETWORKX = True
except Exception:
    HAS_NETWORKX = False

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except Exception:
    HAS_MATPLOTLIB = False

try:
    import folium
    HAS_FOLIUM = True
except Exception:
    HAS_FOLIUM = False

try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    HAS_PIL = True
except Exception:
    HAS_PIL = False

# --- Datos: 7 estados (nombres y coordenadas aproximadas) ---
states = [
    ("Ciudad de México", 19.432608, -99.133209),
    ("Estado de México", 19.293886, -99.601304),
    ("Puebla", 19.041297, -98.206200),
    ("Morelos", 18.681617, -99.101349),
    ("Hidalgo", 20.091103, -98.762237),
    ("Querétaro", 20.588793, -100.389888),
    ("Tlaxcala", 19.314170, -98.241882)

]

# Haversine para distancia en km
def haversine(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a_h = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a_h))
    R = 6371
    return R * c

n = len(states)

dist = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i == j:
            dist[i][j] = 0.0
        else:
            dist[i][j] = round(haversine((states[i][1], states[i][2]), (states[j][1], states[j][2])), 3)

def edge_cost(i,j):
    return dist[i][j]

# --- a) Mejor recorrido sin repetir (bruto por permutaciones) ---
indices = list(range(n))
min_cost = float('inf')
best_path = None
for perm in permutations(indices):
    cost = 0.0
    for k in range(n-1):
        cost += edge_cost(perm[k], perm[k+1])
    if cost < min_cost:
        min_cost = cost
        best_path = perm
best_path_names = [states[i][0] for i in best_path]
min_cost = round(min_cost,3)

# --- b) Recorrido que repite al menos uno (usar MST + DFS walk) ---
if HAS_NETWORKX:
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(i+1, n):
            G.add_edge(i,j,weight=edge_cost(i,j))
    MST = nx.minimum_spanning_tree(G, weight='weight')
    start = 0
    walk = []
    def dfs_walk(u, parent):
        walk.append(u)
        for v in sorted(MST.adj[u]):
            if v == parent:
                continue
            dfs_walk(v, u)
            walk.append(u)
    dfs_walk(start, None)
else:
    # Fallback: repetir el inicio al final
    walk = list(best_path) + [best_path[0]]

walk_cost = 0.0
for k in range(len(walk)-1):
    walk_cost += edge_cost(walk[k], walk[k+1])
walk_cost = round(walk_cost,3)
walk_names = [states[i][0] for i in walk]

# --- Salida visual: generar grafo.png y mapa HTML ---
OUT_DIR = 'salida_grafo'
os.makedirs(OUT_DIR, exist_ok=True)
graph_image_path = os.path.join(OUT_DIR, 'grafo_valores.png')
map_path = os.path.join(OUT_DIR, 'mapa_rutas.html')

# Generar mapa con folium si está disponible
def generar_mapa():
    try:
        if HAS_FOLIUM:
            avg_lat = sum(s[1] for s in states)/n
            avg_lon = sum(s[2] for s in states)/n
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=7)
            for i,(name,lat,lon) in enumerate(states):
                folium.Marker([lat,lon], popup=f"{i} - {name}", tooltip=name).add_to(m)
            best_coords = [(states[i][1], states[i][2]) for i in best_path]
            folium.PolyLine(best_coords, tooltip=f"Hamiltoniano ({min_cost} km)", weight=4).add_to(m)
            walk_coords = [(states[i][1], states[i][2]) for i in walk]
            folium.PolyLine(walk_coords, tooltip=f"Walk ({walk_cost} km)", weight=2, dash_array='5,10').add_to(m)
            m.save(map_path)
            return True, None
        else:
            # Fallback: generar un HTML sencillo con la lista de estados y las rutas
            html = ['<html><head><meta charset="utf-8"><title>Mapa rutas (fallback)</title></head><body>']
            html.append('<h2>Estados</h2><ul>')
            for i,(name,lat,lon) in enumerate(states):
                html.append(f'<li>{i} - {name}: ({lat}, {lon})</li>')
            html.append('</ul>')
            html.append('<h2>Mejor camino (sin repetir)</h2><ol>')
            for i in best_path:
                html.append(f'<li>{states[i][0]}</li>')
            html.append(f'</ol><p>Costo total: {min_cost} km</p>')
            html.append('<h2>Camino con repeticiones</h2><ol>')
            for i in walk:
                html.append(f'<li>{states[i][0]}</li>')
            html.append(f'</ol><p>Costo total: {walk_cost} km</p>')
            html.append('</body></html>')
            with open(map_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(html))
            return True, None
    except Exception as e:
        return False, str(e)

# Generar imagen PNG con networkx + matplotlib o PIL fallback
def generar_imagen_grafo():
    try:
        if HAS_NETWORKX and HAS_MATPLOTLIB:
            pos = {i:(states[i][2], states[i][1]) for i in range(n)}
            plt.figure(figsize=(8,6))
            G_full = nx.Graph()
            for i in range(n):
                G_full.add_node(i)
            for i in range(n):
                for j in range(i+1,n):
                    G_full.add_edge(i,j,weight=edge_cost(i,j))
            nx.draw_networkx_nodes(G_full, pos, node_size=300)
            nx.draw_networkx_labels(G_full, pos, labels={i:states[i][0] for i in range(n)}, font_size=8)
            nx.draw_networkx_edges(G_full, pos, alpha=0.15)
            sp_edges = [(best_path[i], best_path[i+1]) for i in range(n-1)]
            nx.draw_networkx_edges(G_full, pos, edgelist=sp_edges, width=2, edge_color='red')
            edge_labels = {(best_path[i], best_path[i+1]): f"{edge_cost(best_path[i],best_path[i+1])} km" for i in range(n-1)}
            nx.draw_networkx_edge_labels(G_full, pos, edge_labels=edge_labels, font_size=7)
            plt.title('Grafo y mejor camino Hamiltoniano')
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(graph_image_path, dpi=150)
            plt.close()
            return True, None
        elif HAS_PIL:
            # Crear imagen simple
            W, H = 1000, 700
            img = Image.new('RGB', (W,H), (255,255,255))
            draw = ImageDraw.Draw(img)
            lons = [s[2] for s in states]
            lats = [s[1] for s in states]
            min_lon, max_lon = min(lons), max(lons)
            min_lat, max_lat = min(lats), max(lats)
            def project(lat,lon):
                x = int((lon - min_lon)/(max_lon - min_lon) * (W-120)) + 60
                y = int((max_lat - lat)/(max_lat - min_lat) * (H-120)) + 60
                return x,y
            coords = [project(lat,lon) for _,lat,lon in states]
            # Draw edges of best path
            for i in range(len(best_path)-1):
                a = coords[best_path[i]]
                b = coords[best_path[i+1]]
                draw.line((a,b), fill=(200,40,40), width=3)
            # Draw nodes
            for i,(x,y) in enumerate(coords):
                draw.ellipse((x-8,y-8,x+8,y+8), fill=(30,144,255))
                try:
                    font = ImageFont.load_default()
                    draw.text((x+10,y-6), states[i][0], fill=(0,0,0), font=font)
                except Exception:
                    draw.text((x+10,y-6), states[i][0], fill=(0,0,0))
            img.save(graph_image_path)
            return True, None
        else:
            return False, 'No hay librerías para generar la imagen (instala networkx+matplotlib o pillow)'
    except Exception as e:
        return False, str(e)

# Generar ambos
ok_map, err_map = generar_mapa()
ok_img, err_img = generar_imagen_grafo()

# --- GUI interactiva con imagen embebida (pan & zoom) ---
class ImageCanvas(ctk.CTkFrame if TK_CUSTOM else ctk.Frame):
    def __init__(self, master, image_path, **kwargs):
        super().__init__(master, **kwargs)
        self.image_path = image_path
        # Canvas
        if TK_CUSTOM:
            self.canvas = ctk.CTkCanvas(self, width=900, height=600)
        else:
            self.canvas = ctk.Canvas(self, width=900, height=600)
        self.canvas.pack(fill='both', expand=True)

        # Load image if exists
        self.orig_image = None
        if image_path and os.path.exists(image_path) and HAS_PIL:
            try:
                self.orig_image = Image.open(image_path).convert('RGBA')
            except Exception:
                self.orig_image = None

        self.scale = 1.0
        self.tk_image = None
        self.image_id = None

        # Drag state
        self._drag_data = {'x':0,'y':0}

        # Bind events
        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_move_press)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)
        # Mouse wheel
        if sys.platform.startswith('win') or sys.platform == 'darwin':
            self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        else:
            self.canvas.bind('<Button-4>', self.on_mousewheel)
            self.canvas.bind('<Button-5>', self.on_mousewheel)

        # Zoom slider
        if TK_CUSTOM:
            self.zoom_slider = ctk.CTkSlider(self, from_=0.2, to=3.0, number_of_steps=280, command=self.on_slider)
        else:
            self.zoom_slider = ttk.Scale(self, from_=0.2, to=3.0, command=self.on_slider)
        self.zoom_slider.set(1.0)
        self.zoom_slider.pack(fill='x', padx=6, pady=6)

        self._draw_image()

    def _draw_image(self):
        self.canvas.delete('all')
        if not self.orig_image:
            self.canvas.create_text(450,300, text='Imagen no disponible. Se necesita pillow o falló la creación.', fill='black')
            return
        w,h = self.orig_image.size
        new_w = max(1, int(w*self.scale))
        new_h = max(1, int(h*self.scale))
        resized = self.orig_image.resize((new_w,new_h), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        # Create image centered
        self.image_id = self.canvas.create_image(450,300, image=self.tk_image, anchor='center')
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def on_button_press(self, event):
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def on_move_press(self, event):
        dx = event.x - self._drag_data['x']
        dy = event.y - self._drag_data['y']
        self.canvas.move('all', dx, dy)
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def on_button_release(self, event):
        pass

    def on_mousewheel(self, event):
        # Windows/Mac: event.delta, Linux: Button-4/5
        if hasattr(event, 'delta'):
            if event.delta > 0:
                self.scale *= 1.1
            else:
                self.scale /= 1.1
        else:
            if event.num == 4:
                self.scale *= 1.1
            else:
                self.scale /= 1.1
        self.scale = max(0.2, min(self.scale, 3.0))
        try:
            self.zoom_slider.set(self.scale)
        except Exception:
            pass
        self._draw_image()

    def on_slider(self, val):
        try:
            self.scale = float(val)
        except Exception:
            self.scale = 1.0
        self._draw_image()

class App(ctk.CTk if TK_CUSTOM else ctk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Recorrido 7 estados - Grafo interactivo')
        self.geometry('1200x800')

        header = ctk.CTkLabel(self, text='Recorrido de 7 estados (grafo)', font=('Arial',16)) if TK_CUSTOM else ctk.Label(self, text='Recorrido de 7 estados (grafo)', font=('Arial',16))
        header.pack(pady=8)

        container = ctk.CTkFrame(self) if TK_CUSTOM else ctk.Frame(self)
        container.pack(fill='both', expand=True)

        info_frame = ctk.CTkFrame(container, width=320) if TK_CUSTOM else ctk.Frame(container, width=320)
        info_frame.pack(side='left', fill='y', padx=8, pady=8)

        lbl1 = ctk.CTkLabel(info_frame, text=f"Mejor camino (sin repetir): {min_cost} km") if TK_CUSTOM else ctk.Label(info_frame, text=f"Mejor camino (sin repetir): {min_cost} km")
        lbl1.pack(anchor='w', padx=6, pady=4)
        t1 = ctk.CTkTextbox(info_frame, width=300, height=120) if TK_CUSTOM else ctk.Text(info_frame, width=40, height=7)
        t1.pack(padx=6, pady=4)
        t1.insert('end', '\n'.join(best_path_names))
        t1.configure(state='disabled')

        lbl2 = ctk.CTkLabel(info_frame, text=f"Camino que repite: {walk_cost} km") if TK_CUSTOM else ctk.Label(info_frame, text=f"Camino que repite: {walk_cost} km")
        lbl2.pack(anchor='w', padx=6, pady=4)
        t2 = ctk.CTkTextbox(info_frame, width=300, height=120) if TK_CUSTOM else ctk.Text(info_frame, width=40, height=7)
        t2.pack(padx=6, pady=4)
        t2.insert('end', '\n'.join(walk_names))
        t2.configure(state='disabled')

        btn_open_map = ctk.CTkButton(info_frame, text='Abrir mapa (HTML)', command=self.open_map) if TK_CUSTOM else ttk.Button(info_frame, text='Abrir mapa (HTML)', command=self.open_map)
        btn_open_map.pack(pady=6)

        # Show status about generation
        status_txt = ''
        if ok_map:
            status_txt += f'Mapa generado: {os.path.abspath(map_path)}\n'
        else:
            status_txt += f'No se generó mapa: {err_map}\n'
        if ok_img:
            status_txt += f'Imagen generada: {os.path.abspath(graph_image_path)}\n'
        else:
            status_txt += f'No se generó imagen: {err_img}\n'
        lbl_status = ctk.CTkLabel(info_frame, text=status_txt) if TK_CUSTOM else tk_messagebox.showinfo
        if not TK_CUSTOM:
            # show a messagebox at startup with the status
            tk_messagebox.showinfo('Estado de generación', status_txt)

        right_frame = ctk.CTkFrame(container) if TK_CUSTOM else ctk.Frame(container)
        right_frame.pack(side='right', fill='both', expand=True, padx=8, pady=8)

        self.img_canvas = ImageCanvas(right_frame, graph_image_path)
        self.img_canvas.pack(fill='both', expand=True)

    def open_map(self):
        ruta = os.path.abspath(map_path)
        if os.path.exists(ruta):
            try:
                webbrowser.open_new_tab('file://' + ruta)
            except Exception as e:
                tk_messagebox.showerror('Error abriendo mapa', f'No se pudo abrir el mapa:\n{e}')
        else:
            tk_messagebox.showwarning('Mapa no encontrado', f'No se encontró el archivo:\n{ruta}\n\nIntenta regenerarlo instalando folium: pip install folium')

if __name__ == '__main__':
    print('Mejor camino (sin repetir):', ' -> '.join(best_path_names), f'| {min_cost} km')
    print('Camino con repeticiones:', ' -> '.join(walk_names), f'| {walk_cost} km')
    print('Archivos en:', os.path.abspath(OUT_DIR))

    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print('Error al iniciar GUI:', e)
        tk_messagebox.showerror('Error', f'Error al iniciar GUI:\n{e}')

# Fin
