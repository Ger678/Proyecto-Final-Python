import os
import json
from PIL import Image, ImageTk
import tkinter as tk

class RecipeBook:
    def __init__(self, master):
        self.master = master
        master.title("Recetario")

        # Configurar los margenes
        self.master.configure(padx=10, pady=10)

        # Crear el frame principal
        self.frame_main = tk.Frame(self.master)
        self.frame_main.pack(expand=True, fill="both")

        # Crear la caja de listado de recetas
        self.frame_list = tk.LabelFrame(self.frame_main, text="Recetas")
        self.frame_list.pack(side="left", padx=10, pady=10, expand=True, fill="both")

        # Crear la caja de detalle de recetas
        self.frame_detail = tk.LabelFrame(self.frame_main, text="Detalle de la receta")
        self.frame_detail.pack(side="left", padx=10, pady=10, expand=True, fill="both")

        # Crear la lista de recetas
        self.list_recipes = tk.Listbox(self.frame_list)
        self.list_recipes.pack(expand=True, fill="both")

        # Obtener la lista de archivos de recetas
        recipe_files = [f for f in os.listdir(path="C:/Users/feder/OneDrive/Escritorio/Python/Proyecto-Final-Python") if f.endswith(".json")]

        # Cargar y agregar cada receta a la lista
        self.recipes = []
        for recipe_file in recipe_files:
            with open(recipe_file) as f:
                recipe = json.load(f)
                self.recipes.append(recipe)
                self.list_recipes.insert(tk.END, recipe['name'])


        # Añadir un label para la caja de detalle de recetas
        self.label_detail = tk.Label(self.frame_detail, text="Selecciona una receta")
        self.label_detail.pack(padx=10, pady=10)

        # Asociar la función de controlador de eventos para la selección de una receta
        self.list_recipes.bind('<<ListboxSelect>>', self.show_recipe_detail)

        # Crear un widget de texto para mostrar los ingredientes y las instrucciones de la receta
        self.text_recipe = tk.Text(self.frame_detail)

        #Imagen
        self.image_label = tk.Label(self.frame_detail, bg="green")

    def show_recipe_detail(self, event):

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
            self.text_recipe.insert(tk.END, f"- {ingredient['name'].upper()}, {ingredient['quantity']}\n")
        self.text_recipe.insert(tk.END, "\nInstrucciones:\n")
        for step in recipe['steps']:
            self.text_recipe.insert(tk.END, f"{step}\n")
        
        self.image_label.config(image='')
        
        image_url = recipe['imageURL']
        if image_url:
            image = Image.open(image_url)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)


        self.text_recipe.pack(expand=True, fill="both",padx=10, pady=10)


root = tk.Tk()
app = RecipeBook(root)
root.mainloop()