import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from bisect import bisect_left

class PostresManager:
    def __init__(self):
        self.postres = []

    def _key(self, name):
        return name.lower().strip()

    def _find_index(self, name):
        keys = [self._key(p['name']) for p in self.postres]
        return bisect_left(keys, self._key(name))

    def get_names(self):
        return [p['name'] for p in self.postres]

    def get_ingredients(self, name):
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            return list(self.postres[i]['ingredients'])
        raise KeyError(f"El postre '{name}' no existe.")

    def add_ingredient(self, name, ingredient):
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            ingr = self.postres[i]['ingredients']
            # 🔹 Normalizamos ingrediente
            norm_ing = ingredient.strip().title()
            # 🔹 Comparamos sin distinguir mayúsculas
            if all(self._key(x) != self._key(norm_ing) for x in ingr):
                ingr.append(norm_ing)
                ingr.sort(key=str.lower)
                return True
            return False
        raise KeyError(f"No existe el postre '{name}'.")

    def remove_ingredient(self, name, ingredient):
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            ingr = self.postres[i]['ingredients']
            for ing in ingr:
                if self._key(ing) == self._key(ingredient):
                    ingr.remove(ing)
                    return True
            raise ValueError(f"'{ingredient}' no está en '{name}'.")
        raise KeyError(f"No existe el postre '{name}'.")

    def add_postre(self, name, ingredients):
        if not name:
            raise ValueError("Nombre de postre vacío.")
        name = name.strip().title()  # 🔹 Normaliza visualmente el nombre
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            raise KeyError(f"'{name}' ya existe.")
        # 🔹 Normaliza ingredientes y elimina duplicados sin distinguir mayúsculas
        uniq_ing = []
        for ing in ingredients:
            norm_ing = ing.strip().title()
            if norm_ing and all(self._key(x) != self._key(norm_ing) for x in uniq_ing):
                uniq_ing.append(norm_ing)
        uniq_ing.sort(key=str.lower)
        self.postres.insert(i, {'name': name, 'ingredients': uniq_ing})

    def delete_postre(self, name):
        i = self._find_index(name)
        if i < len(self.postres) and self._key(self.postres[i]['name']) == self._key(name):
            del self.postres[i]
            return True
        raise KeyError(f"El postre '{name}' no existe.")

    def remove_duplicates(self):
        if not self.postres:
            return 0
        nueva = []
        prev_key = None
        for item in self.postres:
            k = self._key(item['name'])
            if prev_key is None or k != prev_key:
                uniq_ing = []
                for ing in item['ingredients']:
                    if all(self._key(x) != self._key(ing) for x in uniq_ing):
                        uniq_ing.append(ing)
                nueva.append({'name': item['name'], 'ingredients': uniq_ing})
                prev_key = k
            else:
                base = nueva[-1]['ingredients']
                for ing in item['ingredients']:
                    if all(self._key(x) != self._key(ing) for x in base):
                        base.append(ing)
        removed = len(self.postres) - len(nueva)
        self.postres = nueva
        return removed


# --------------------------------------------------------------------
# ----------------------------- INTERFAZ -----------------------------
# --------------------------------------------------------------------
class PostresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍰 Gestor de Postres - SOFTREX")
        self.root.geometry("900x600")
        self.root.configure(bg="#f9f9f9")

        style = ttk.Style()
        style.configure("TFrame", background="#f9f9f9")
        style.configure("TLabel", background="#f9f9f9", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="#444")

        self.manager = PostresManager()
        self._crear_layout()

        # Datos iniciales
        self.manager.add_postre("Brownie", ["Chocolate", "Harina", "Azúcar", "Huevo"])
        self.manager.add_postre("Flan", ["Leche", "Huevo", "Azúcar"])
        self.manager.add_postre("Gelatina", ["Grenetina", "Agua", "Colorante"])
        self._actualizar_lista_postres()

    def _crear_layout(self):
        ttk.Label(self.root, text="🍰 Gestor de Postres", style="Title.TLabel").pack(pady=10)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        frame_left = ttk.Frame(main_frame)
        frame_left.pack(side="left", fill="both", expand=True, padx=10)

        ttk.Label(frame_left, text="Postres disponibles:").pack(anchor="w", pady=5)
        self.lst_postres = tk.Listbox(frame_left, font=("Segoe UI", 11), height=15, exportselection=False)
        self.lst_postres.pack(fill="both", expand=True, pady=5)
        self.lst_postres.bind("<<ListboxSelect>>", lambda e: self._mostrar_ingredientes())

        btn_frame_left = ttk.Frame(frame_left)
        btn_frame_left.pack(pady=5)
        ttk.Button(btn_frame_left, text="➕ Nuevo Postre", command=self._agregar_postre).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame_left, text="🗑️ Eliminar Postre", command=self._eliminar_postre).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame_left, text="♻️ Eliminar Duplicados", command=self._eliminar_duplicados).grid(row=0, column=2, padx=5)

        frame_right = ttk.Frame(main_frame)
        frame_right.pack(side="right", fill="both", expand=True, padx=10)

        ttk.Label(frame_right, text="Ingredientes:").pack(anchor="w", pady=5)
        self.lst_ingredientes = tk.Listbox(frame_right, font=("Segoe UI", 11), height=15)
        self.lst_ingredientes.pack(fill="both", expand=True, pady=5)

        btn_frame_right = ttk.Frame(frame_right)
        btn_frame_right.pack(pady=5)
        ttk.Button(btn_frame_right, text="➕ Agregar", command=self._agregar_ingrediente).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame_right, text="🗑️ Eliminar", command=self._eliminar_ingrediente).grid(row=0, column=1, padx=5)

    def _actualizar_lista_postres(self):
        self.lst_postres.delete(0, tk.END)
        for p in self.manager.get_names():
            self.lst_postres.insert(tk.END, p)

    def _mostrar_ingredientes(self):
        self.lst_ingredientes.delete(0, tk.END)
        sel = self.lst_postres.curselection()
        if not sel:
            return
        postre = self.lst_postres.get(sel[0])
        try:
            ingredientes = self.manager.get_ingredients(postre)
            for ing in ingredientes:
                self.lst_ingredientes.insert(tk.END, ing)
        except KeyError:
            messagebox.showerror("Error", f"No se encontró '{postre}'.")

    def _agregar_postre(self):
        nombre = simpledialog.askstring("Nuevo Postre", "Nombre del postre:")
        if not nombre:
            return
        ingredientes_str = simpledialog.askstring("Ingredientes", "Escribe los ingredientes separados por coma:")
        ingredientes = [i.strip() for i in ingredientes_str.split(",")] if ingredientes_str else []
        try:
            self.manager.add_postre(nombre, ingredientes)
            messagebox.showinfo("Éxito", f"'{nombre.title()}' agregado correctamente.")
            self._actualizar_lista_postres()
        except KeyError as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_postre(self):
        sel = self.lst_postres.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un postre para eliminar.")
            return
        postre = self.lst_postres.get(sel[0])
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{postre}'?"):
            try:
                self.manager.delete_postre(postre)
                self._actualizar_lista_postres()
                self.lst_ingredientes.delete(0, tk.END)
            except KeyError as e:
                messagebox.showerror("Error", str(e))

    def _agregar_ingrediente(self):
        sel = self.lst_postres.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un postre primero.")
            return
        postre = self.lst_postres.get(sel[0])
        ingr = simpledialog.askstring("Nuevo Ingrediente", f"Ingrediente para '{postre}':")
        if not ingr:
            return
        try:
            added = self.manager.add_ingredient(postre, ingr)
            if added:
                self._mostrar_ingredientes()
            else:
                messagebox.showinfo("Aviso", "El ingrediente ya existía.")
        except KeyError as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_ingrediente(self):
        sel_postre = self.lst_postres.curselection()
        sel_ing = self.lst_ingredientes.curselection()
        if not sel_postre or not sel_ing:
            messagebox.showwarning("Atención", "Selecciona un ingrediente a eliminar.")
            return
        postre = self.lst_postres.get(sel_postre[0])
        ingrediente = self.lst_ingredientes.get(sel_ing[0])
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{ingrediente}' de '{postre}'?"):
            try:
                self.manager.remove_ingredient(postre, ingrediente)
                self._mostrar_ingredientes()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _eliminar_duplicados(self):
        eliminados = self.manager.remove_duplicates()
        self._actualizar_lista_postres()
        if eliminados > 0:
            messagebox.showinfo("Limpieza", f"Se eliminaron {eliminados} duplicados.")
        else:
            messagebox.showinfo("Limpieza", "No había duplicados.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PostresApp(root)
    root.mainloop()