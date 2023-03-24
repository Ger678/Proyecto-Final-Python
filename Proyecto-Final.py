import os
import json
from PIL import Image, ImageTk
import tkinter as tk
# import urllib.request


class Recipe:
    def __init__(self, name, ingredients, steps, timers, imageURL):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
        self.timers = timers
        self.imageURL = imageURL

    def a_json(self):
        recipe_dict = {
            "name": self.name,
            "ingredientes": self.ingredients,
            "steps": self.steps,
            "timers": self.timers,
            "imageURL": self.imageURL
        }
        return json.dumps(recipe_dict, indent=4)

    def save_to_file(self, file_name):
        with open(file_name, 'w') as f:
            f.write(self.to_json())


class RecipeBook:

    def __init__(self, master):
        self.master = master
        master.title("Recetario")
        self.botonera()

        # Configurar los margenes
        self.master.configure(padx=10, pady=10)

        # Crear el frame principal
        self.frame_main = tk.Frame(self.master)
        self.frame_main.pack(expand=True, fill="both")

        # Crear la caja para agregar una receta
        self.btn_receta = tk.Button(
            self.frame_main, text="Receta del dia ★", width=4, height=1, justify="left")
        self.btn_receta.pack()

        self.search = tk.Entry(self.frame_main)
        self.search.pack()

        # Crear la caja de listado de recetas
        self.frame_list = tk.LabelFrame(self.frame_main, text="Recetas")
        self.frame_list.pack(side="left", padx=10, pady=10,
                             expand=True, fill="both")

        # Crear la caja de detalle de recetas
        self.frame_detail = tk.LabelFrame(
            self.frame_main, text="Detalle de la receta")
        self.frame_detail.pack(side="left", padx=10,
                               pady=10, expand=True, fill="both")

        # Crear la lista de recetas
        self.list_recipes = tk.Listbox(self.frame_list)
        self.list_recipes.pack(expand=True, fill="both")

        # Obtener la lista de archivos de recetas
        recipe_files = [f for f in os.listdir(
            path="C:/Users/feder/OneDrive/Escritorio/Python/Proyecto-Final-Python") if f.endswith(".json")]

        # Cargar y agregar cada receta a la lista
        self.recipes = []
        for recipe_file in recipe_files:
            with open(recipe_file) as f:
                recipe = json.load(f)
                self.recipes.append(recipe)
                self.list_recipes.insert(tk.END, recipe['name'])

        # Asociar la función de controlador de eventos para la selección de una receta
        self.list_recipes.bind('<<ListboxSelect>>', self.show_recipe_detail)

        # Crear un widget de texto para mostrar los ingredientes y las instrucciones de la receta
        self.text_recipe = tk.Text(self.frame_detail)

        # Imagen
        self.image_label = tk.Label(self.frame_detail, bg="green")

    def show_recipe_detail(self, event):

        # Añadir un label para la caja de detalle de recetas
        self.label_detail = tk.Label(
            self.frame_detail, text="Selecciona una receta")
        self.label_detail.pack(padx=10, pady=10)

        # Limpiar el widget de texto
        self.text_recipe.delete('1.0', tk.END)

        # Obtener el índice de la receta seleccionada
        index = self.list_recipes.curselection()[0]

        # Obtener la receta seleccionada
        recipe = self.recipes[index]

        # Actualizar la etiqueta de detalle de recetas con el nombre de la receta
        self.label_detail.config(text=recipe['name'])

        # Agregar los ingredientes y las instrucciones al widget de texto
        self.text_recipe.insert(tk.END, "Ingredientes:\n")
        for ingredient in recipe['ingredients']:
            self.text_recipe.insert(
                tk.END, f"- {ingredient['name'].upper()}, {ingredient['quantity']}\n")
        self.text_recipe.insert(tk.END, "\nInstrucciones:\n")
        for step in recipe['steps']:
            self.text_recipe.insert(tk.END, f"{step}\n")

        self.text_recipe.pack(expand=True, fill="both", padx=10, pady=10)

    def botonera(self):

        # Botones--------------------------------------------------------------
        self.frame_btns = tk.Menubutton(self.master, wraplength="1px")
        self.frame_btns.pack(side="top")

        # Crear la caja para agregar una receta
        self.btn_receta = tk.Button(
            self.frame_btns, text="Crear Nueva Receta", command=lambda: RecipeForm(root))
        self.btn_receta.pack(side="left")

        def nueva(self):
            self.nueva_receta = tk.Frame()

        # Crear la caja para editar la receta
        self.btn_receta = tk.Button(
            self.frame_btns, text="✏", width=4, height=1)
        self.btn_receta.pack(side="left")

        # Crear la caja para borrar una receta
        self.btn_receta = tk.Button(
            self.frame_btns, text="x", width=4, height=1)
        self.btn_receta.pack(side="right")

        # Botones--------------------------------------------------------------


class RecipeForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear Nueva Receta")

        # Crear widgets para el formulario
        tk.Label(self, text="Nombre:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Ingredientes:").grid(row=1, column=0)
        self.ingredients_text = tk.Text(self, height=4, width=30)
        self.ingredients_text.grid(row=1, column=1)

        tk.Label(self, text="Pasos:").grid(row=2, column=0)
        self.steps_text = tk.Text(self, height=4, width=30)
        self.steps_text.grid(row=2, column=1)

        tk.Label(self, text="Temporizadores:").grid(row=3, column=0)
        self.timers_text = tk.Text(self, height=4, width=30)
        self.timers_text.grid(row=3, column=1)

        tk.Label(self, text="URL de Imagen:").grid(row=4, column=0)
        self.imageURL_entry = tk.Entry(self)
        self.imageURL_entry.grid(row=4, column=1)

        # Crear boton para guardar la receta
        tk.Button(self, text="Guardar", command=self.save_recipe).grid(
            row=5, column=1)

    # Funcion para guardar la receta
    def save_recipe(self):
        name = self.name_entry.get()
        ingredients = json.loads(self.ingredients_text.get("1.0", "end"))
        steps = json.loads(self.steps_text.get("1.0", "end"))
        timers = json.loads(self.timers_text.get("1.0", "end"))
        imageURL = self.imageURL_entry.get()

        recipe = Recipe(name, ingredients, steps, timers, imageURL)
        recipe.save_to_file(name.lower().replace(" ", "_") + ".json")
        self.destroy()


root = tk.Tk()
app = RecipeBook(root)
root.geometry("900x300")
root.mainloop()
