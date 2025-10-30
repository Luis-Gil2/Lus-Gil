import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from bisect import bisect_left

class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

class ListaIngredientes:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre):
        nombre = nombre.strip().title()
        if not nombre or self.contiene(nombre):
            return False
        nuevo = NodoIngrediente(nombre)
        if not self.cabeza:
            self.cabeza = nuevo
            return True
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo
        return True

    def eliminar(self, nombre):
        actual, anterior = self.cabeza, None
        while actual:
            if actual.nombre.lower() == nombre.lower():
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                return True
            anterior, actual = actual, actual.siguiente
        return False

    def contiene(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre.lower() == nombre.lower():
                return True
            actual = actual.siguiente
        return False

    def to_list(self):
        datos, actual = [], self.cabeza
        while actual:
            datos.append(actual.nombre)
            actual = actual.siguiente
        return datos

class PostresManager:
    def __init__(self):
        self.postres = []  

    def _key(self, name): return name.lower().strip()
    def _find_index(self, name):
        keys = [self._key(p['name']) for p in self.postres]
        return bisect_left(keys, self._key(name))

    def get_names(self): return [p['name'] for p in self.postres]
    def get_ingredients(self, name):
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            return self.postres[i]['ingredients'].to_list()
        raise KeyError(f"El postre '{name}' no existe.")

    def add_postre(self, name, ingredients):
        if not name.strip(): raise ValueError("Nombre vacío.")
        name = name.strip().title()
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            raise KeyError(f"'{name}' ya existe.")
        lista = ListaIngredientes()
        for ing in ingredients:
            lista.agregar(ing)
        self.postres.insert(i, {'name': name, 'ingredients': lista})

    def delete_postre(self, name):
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            del self.postres[i]
        else:
            raise KeyError(f"'{name}' no existe.")

    def add_ingredient(self, name, ingredient):
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            return self.postres[i]['ingredients'].agregar(ingredient)
        raise KeyError(f"No existe el postre '{name}'.")

    def remove_ingredient(self, name, ingredient):
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            if not self.postres[i]['ingredients'].eliminar(ingredient):
                raise ValueError(f"'{ingredient}' no está en '{name}'.")
            return True
        raise KeyError(f"No existe el postre '{name}'.")

    def remove_duplicates(self):
        nueva, prev = [], None
        for p in self.postres:
            k = self._key(p['name'])
            if prev != k:
                nueva.append(p)
                prev = k
        eliminados = len(self.postres) - len(nueva)
        self.postres = nueva
        return eliminados

class PostresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍰 Gestor de Postres - Estructura Enlazada")
        self.root.geometry("960x580")
        self.root.configure(bg="#f4f4f4")

        style = ttk.Style()
        style.configure("TFrame", background="#f4f4f4")
        style.configure("TLabel", background="#f4f4f4", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="#333")

        self.manager = PostresManager()
        self._crear_ui()

        self.manager.add_postre("Brownie", ["Chocolate", "Harina", "Azúcar", "Huevo"])
        self.manager.add_postre("Flan", ["Leche", "Huevo", "Azúcar"])
        self.manager.add_postre("Gelatina", ["Grenetina", "Agua", "Colorante"])
        self._actualizar_lista()

    def _crear_ui(self):
        ttk.Label(self.root, text="🍰 GESTOR DE POSTRES", style="Title.TLabel").pack(pady=10)
        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=15, pady=5)

        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True, padx=10)
        ttk.Label(left, text="Lista de Postres:").pack(anchor="w", pady=5)
        self.lst_postres = tk.Listbox(left, font=("Segoe UI", 11), height=15, exportselection=False)
        self.lst_postres.pack(fill="both", expand=True)
        self.lst_postres.bind("<<ListboxSelect>>", lambda e: self._mostrar_ingredientes())

        btns_left = ttk.Frame(left)
        btns_left.pack(pady=5)
        ttk.Button(btns_left, text="➕ Agregar", command=self._nuevo_postre).grid(row=0, column=0, padx=4)
        ttk.Button(btns_left, text="🗑️ Eliminar", command=self._eliminar_postre).grid(row=0, column=1, padx=4)
        ttk.Button(btns_left, text="♻️ Limpiar duplicados", command=self._limpiar).grid(row=0, column=2, padx=4)
        ttk.Button(btns_left, text="👁️ Ver estructura", command=self._ver_estructura).grid(row=0, column=3, padx=4)

        # Derecha
        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True, padx=10)
        ttk.Label(right, text="Ingredientes del Postre:").pack(anchor="w", pady=5)
        self.lst_ing = tk.Listbox(right, font=("Segoe UI", 11), height=15)
        self.lst_ing.pack(fill="both", expand=True)
        btns_right = ttk.Frame(right)
        btns_right.pack(pady=5)
        ttk.Button(btns_right, text="➕ Agregar", command=self._nuevo_ing).grid(row=0, column=0, padx=4)
        ttk.Button(btns_right, text="🗑️ Eliminar", command=self._eliminar_ing).grid(row=0, column=1, padx=4)

    def _actualizar_lista(self):
        self.lst_postres.delete(0, tk.END)
        for p in self.manager.get_names():
            self.lst_postres.insert(tk.END, p)

    def _mostrar_ingredientes(self):
        self.lst_ing.delete(0, tk.END)
        sel = self.lst_postres.curselection()
        if not sel: return
        nombre = self.lst_postres.get(sel[0])
        for ing in self.manager.get_ingredients(nombre):
            self.lst_ing.insert(tk.END, ing)

    def _nuevo_postre(self):
        n = simpledialog.askstring("Nuevo postre", "Nombre:")
        if not n: return
        ings = simpledialog.askstring("Ingredientes", "Separados por coma (,):")
        lista = [i.strip() for i in ings.split(",")] if ings else []
        try:
            self.manager.add_postre(n, lista)
            self._actualizar_lista()
            messagebox.showinfo("Éxito", f"'{n.title()}' agregado.")
        except KeyError as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_postre(self):
        sel = self.lst_postres.curselection()
        if not sel: return messagebox.showwarning("Aviso", "Selecciona un postre.")
        n = self.lst_postres.get(sel[0])
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{n}'?"):
            self.manager.delete_postre(n)
            self._actualizar_lista()
            self.lst_ing.delete(0, tk.END)

    def _nuevo_ing(self):
        sel = self.lst_postres.curselection()
        if not sel: return messagebox.showwarning("Aviso", "Selecciona un postre.")
        postre = self.lst_postres.get(sel[0])
        i = simpledialog.askstring("Nuevo ingrediente", "Nombre:")
        if not i: return
        self.manager.add_ingredient(postre, i)
        self._mostrar_ingredientes()

    def _eliminar_ing(self):
        sel_postre, sel_ing = self.lst_postres.curselection(), self.lst_ing.curselection()
        if not sel_postre or not sel_ing:
            return messagebox.showwarning("Aviso", "Selecciona un ingrediente.")
        p = self.lst_postres.get(sel_postre[0])
        i = self.lst_ing.get(sel_ing[0])
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{i}' de '{p}'?"):
            self.manager.remove_ingredient(p, i)
            self._mostrar_ingredientes()

    def _limpiar(self):
        e = self.manager.remove_duplicates()
        self._actualizar_lista()
        messagebox.showinfo("Limpieza", f"Se eliminaron {e} duplicados." if e else "No había duplicados.")

    def _ver_estructura(self):
        win = tk.Toplevel(self.root)
        win.title("Estructura de Postres (Listas Enlazadas)")
        canvas = tk.Canvas(win, width=1000, height=600, bg="white")
        canvas.pack(fill="both", expand=True)

        box_w, box_h = 120, 40
        x0, y0, spacing_y = 80, 60, 100

        for idx, p in enumerate(self.manager.postres):
            y = y0 + idx * spacing_y

            canvas.create_rectangle(x0, y, x0 + box_w, y + box_h, fill="#FFE69A", outline="black")
            canvas.create_text(x0 + box_w / 2, y + box_h / 2, text=p['name'], font=("Segoe UI", 10, "bold"))

            canvas.create_line(x0 + box_w, y + box_h / 2, x0 + box_w + 30, y + box_h / 2, arrow=tk.LAST)

            actual = p['ingredients'].cabeza
            x = x0 + box_w + 50
            while actual:
                canvas.create_rectangle(x, y, x + box_w, y + box_h, fill="#B8E8B2", outline="black")
                canvas.create_text(x + box_w / 2, y + box_h / 2, text=actual.nombre, font=("Segoe UI", 9))
                if actual.siguiente:
                    canvas.create_line(x + box_w, y + box_h / 2, x + box_w + 20, y + box_h / 2, arrow=tk.LAST)
                else:
                    canvas.create_text(x + box_w + 30, y + box_h / 2, text="NIL", font=("Segoe UI", 9, "italic"))
                x += box_w + 50
                actual = actual.siguiente

if __name__ == "__main__":
    root = tk.Tk()
    app = PostresApp(root)
    root.mainloop()