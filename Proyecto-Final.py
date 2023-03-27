import os
import json
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import random

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
            "ingredients": self.ingredients,
            "steps": self.steps,
            "timers": self.timers,
            "imageURL": self.imageURL
        }
        return json.dumps(recipe_dict, indent=4)

    def save_to_file(self, file_name):
        with open(file_name, 'w') as f:
            f.write(self.a_json())

class RecipeBook:

    def __init__(self, master):
        self.master = master
        master.title("Recetario")
        self.recipe = []
        self.receta_del_dia = {}

        # Configurar los margenes
        self.master.configure(padx=10, pady=10)

        self.botonera()

        # Crear el frame principal
        self.frame_main = tk.Frame(self.master)
        self.frame_main.grid()

        # Crear la caja de listado de recetas
        self.frame_list = tk.LabelFrame(self.frame_main, text="Recetas")
        self.frame_list.grid(padx=10,row=1,column=0, sticky='N', columnspan=1)

        # Crear la caja de detalle de recetas
        self.frame_detail = tk.LabelFrame(self.frame_main,text="Detalle de la receta")
        self.frame_detail.grid(row=1, column=1)

        # Crear la lista de recetas
        self.list_recipes = tk.Listbox(self.frame_list)
        self.list_recipes.grid(row=2, column=0,columnspan=2, ipadx='50px', sticky='W')
        self.btn_accions()


        ###############################
        ##########  RECETAS ###########

        # Obtener la lista de archivos de recetas
        recipe_files = [f for f in os.listdir(
            path="../Proyecto-Final-Python") if f.endswith(".json")]

        # Cargar y agregar cada receta a la lista
        self.recipes = []
        for recipe_file in recipe_files:
            with open(recipe_file) as f:
                recipe = json.load(f)
                self.recipes.append(recipe)
                self.list_recipes.insert(tk.END, recipe['name'])

        ##########  RECETAS ##########
        ##############################

        # Asociar la función de controlador de eventos para la selección de una receta
        self.list_recipes.bind('<<ListboxSelect>>', self.show_recipe_detail)

        # Crear un widget de texto para mostrar los ingredientes y las instrucciones de la receta
        self.text_recipe = tk.Text(self.frame_detail)

        # Imagen
        self.image_label = tk.Label(self.frame_detail, bg="green")

    def btn_accions(self):
        
        # Accions
        self.btn_receta = tk.Button(self.frame_list, text="Receta del dia ★", command=self.day_recipe)
        self.btn_receta.bind('<<random_recipe>>', self.show_recipe_detail)
        self.btn_receta.grid(row=0, column=0, sticky='W', padx=10, pady=10,columnspan=2, ipadx=70)

        # Crea un Entry y un botón para realizar la búsqueda
        self.search_entry = tk.Entry(self.frame_list)
        self.search_entry.grid(row=1, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self.frame_list, text="Buscar", command=self.search)
        self.search_button.grid(row=1, column=0,sticky='N'+'W', padx=10, pady=10)

    def day_recipe(self):
        random_recipe = random.choice(self.recipes)['name']
        self.btn_receta.destroy()
        tk.Label(self.frame_list, text=random_recipe).grid(row=0, column=0, sticky='W', padx=10, pady=10,columnspan=2, ipadx=70)
        print(random_recipe['name'])

    def botonera(self):

        # Botones--------------------------------------------------------------
        self.frame_btns = tk.Menubutton(self.master)
        self.frame_btns.grid(row=0, column=0, sticky='W', padx=10)

        # Crear la caja para agregar una receta
        self.btn_receta = tk.Button(
        self.frame_btns, text="Crear Receta", command=lambda: RecipeForm(root))
        self.btn_receta.grid(row=0, column=0,padx=5)

        # Crear la caja para editar la receta
        self.btn_receta = tk.Button(
        self.frame_btns, text="Editar Receta", command=lambda: EditMode(root, self.recipe))
        self.btn_receta.grid(row=0, column=1, padx=5)

        # Crear la caja para borrar una receta
        self.btn_receta = tk.Button(
        self.frame_btns, text="Eliminar Receta", command=self.delete)
        self.btn_receta.grid(row=0, column=2, padx=5)

        # Botones--------------------------------------------------------------

    def show_recipe_detail(self, event):

        # Añadir un label para la caja de detalle de recetas
        self.label_detail = tk.Label(
        self.frame_detail, text="Selecciona una receta")
        self.label_detail.grid(row=1)

        # Limpiar el widget de texto
        self.text_recipe.delete(1.0, tk.END)

        # Obtener el índice de la receta seleccionada
        index = self.list_recipes.curselection()
        self.recipe = self.list_recipes.selection_get()
        index = index[0]
        # Obtener la receta seleccionada
        self.recipe = self.recipes[index]

        # Actualizar la etiqueta de detalle de recetas con el nombre de la receta
        self.label_detail.config(text=self.recipe['name'])

        # Agregar los ingredientes y las instrucciones al widget de texto
        self.text_recipe.insert(tk.END, "Ingredientes:\n")
        for ingredient in self.recipe['ingredients']:
            self.text_recipe.insert(
                tk.END, f"- {ingredient['name'].upper()}, {ingredient['quantity']}\n")
        self.text_recipe.insert(tk.END, "\nInstrucciones:\n")
        for step in self.recipe['steps']:
            self.text_recipe.insert(tk.END, f"{step}\n")

        self.text_recipe.grid(padx=10, pady=10)

    def search(self):
        # Obtén el texto del Entry
        search_text = self.search_entry.get()

        # Recorre todos los elementos de la Listbox para buscar coincidencias
        found = False
        for i in range(self.list_recipes.size()):
            if search_text.lower() in self.list_recipes.get(i).lower():
                # Se encontró una coincidencia
                self.list_recipes.selection_clear(0, tk.END)
                self.list_recipes.selection_set(i)
                self.list_recipes.see(i)
                found = True
                break

        # Si no se encontraron coincidencias, muestra un mensaje al usuario
        if not found:
            messagebox.showinfo("Búsqueda", "No se encontraron resultados")

    def delete(self):
        # Obtener la receta seleccionada en la listbox
        seleccion = self.list_recipes.curselection()
        if len(seleccion) == 0:
            return

        # Obtener la información de la receta
        indice = self.list_recipes.index(seleccion[0])
        receta = self.recipes[indice]
        nombre = receta['name']

        ruta_archivo = f"./{nombre}.json"
        print(ruta_archivo)
        os.remove(ruta_archivo)

        del self.recipe[indice]
        self.list_recipes.delete(seleccion)

class RecipeForm(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear Nueva Receta")
        self.ingredientes = []
        self.steps = []
        self.times = []

        # Crear widgets para el nombre de la receta
        tk.Label(self, text="Nombre:").grid(row=0, column=0, sticky='W', pady=10)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1,ipadx=40)

        tk.Label(self, text="URL de Imagen:").grid(row=1, column=0, sticky='W')
        self.imageURL_entry = tk.Entry(self)
        self.imageURL_entry.grid(row=1, column=1, pady=5, ipadx=40, padx=10)

        #########################################################
        #ingredientes
        # START

        self.ingredient_frame = tk.LabelFrame(self, text="Ingredientes")
        self.ingredient_frame.grid(row=2, column=0, padx=10)
        self.ingredients_text = tk.Listbox(self.ingredient_frame)
        self.ingredients_text.grid(row=2, column=0)

        # Menu para nombre, cantidad y boton
        self.menu_ingredientes = tk.Frame(self)
        self.menu_ingredientes.grid(row=2,column=1, sticky='W')

        # Nombre y cantidad
        tk.Label(self.menu_ingredientes, text="Nombre del ingrediente:").grid(row=2, column=1)
        self.ingredient_name_entry = tk.Entry(self.menu_ingredientes)
        self.ingredient_name_entry.grid(row=3, column=1)

        tk.Label(self.menu_ingredientes, text="Cantidad del ingrediente:").grid(row=4, column=1)
        self.ingredient_quantity_entry = tk.Entry(self.menu_ingredientes)
        self.ingredient_quantity_entry.grid(row=5, column=1)

        tk.Button(self.menu_ingredientes, text="Agregar Ingrediente", command=self.add_ingredient, padx=10, pady=10).grid(row=6, column=1, pady=10)

        # END
        ##########################################################

        ####################################
        # Pasos

        # Marco para pasos
        self.steps_frame = tk.LabelFrame(self, text="Pasos")
        self.steps_frame.grid(row=3, column=0, pady=10)
        self.steps_text = tk.Listbox(self.steps_frame)
        self.steps_text.grid(row=3, column=0)

        # Menu para paso y agregar paso
        self.menu_steps = tk.Frame(self)
        self.menu_steps.grid(row=3,column=1, sticky='W')

        tk.Label(self.menu_steps, text="Pasos:").grid(row=0, column=0, sticky='W')
        self.steps_entry = tk.Entry(self.menu_steps)
        self.steps_entry.grid(row=1, column=0)

        tk.Button(self.menu_steps, text="Agregar paso", padx=10, pady=10, command=self.add_step).grid(row=2, column=0,  pady=10)

        ####################################

        ####################################
        # Timers

        # Marco para pasos
        self.timer_frame = tk.LabelFrame(self, text="Tiempos")
        self.timer_frame.grid(row=4, column=0, pady=10)
        self.timer_text = tk.Listbox(self.timer_frame)
        self.timer_text.grid(row=4, column=0)

        # Menu para paso y agregar paso
        self.menu_timer = tk.Frame(self)
        self.menu_timer.grid(row=4,column=1, sticky='W')


        tk.Label(self.menu_timer, text="Temporizadores:").grid(row=0, sticky='W')
        self.timers_entry = tk.Entry(self.menu_timer)
        self.timers_entry.grid(row=1)

        tk.Button(self.menu_timer, text="Agregar tiempo", padx=10, pady=10, command=self.add_timer).grid(row=2, column=0, pady=10)

        ####################################

        # Crear boton para guardar la receta
        tk.Button(self, text="Guardar", command=self.save_recipe).grid(row=5, column=0,columnspan=2, ipadx=100, pady=10)
        
    def add_ingredient(self):
        # Recuperar el nombre y la cantidad del ingrediente
        ingredient_name = self.ingredient_name_entry.get()
        ingredient_quantity = self.ingredient_quantity_entry.get()

        # Agregar el nombre y la cantidad a la lista de ingredientes

        ing = {'name':ingredient_name, 'quantity':ingredient_quantity}
        self.ingredients_text.insert(tk.END, f"{ingredient_name}:{ingredient_quantity}")
        self.ingredientes.append(ing)

        # Limpiar las entradas de texto para que el usuario pueda agregar otro ingrediente
        self.ingredient_name_entry.delete(0, tk.END)
        self.ingredient_quantity_entry.delete(0, tk.END)

    def add_timer(self):
        time = self.timers_entry.get()
        self.timer_text.insert(tk.END, time)
        self.times.append(time)
        self.timers_entry.delete(0, tk.END)
        print(sum(self.times))                                                                       ###### suma de tiempo ######

    def add_step(self):
        step = self.steps_entry.get()
        self.steps_text.insert(tk.END, step)
        self.steps.append(step)
        self.steps_entry.delete(0, tk.END)
    
    # Funcion para guardar la receta
    def save_recipe(self):

        name = self.name_entry.get()
        ingredients = self.ingredientes
        steps = self.steps
        timers = self.timers_entry.get()
        imageURL = self.imageURL_entry.get()

        recipe = Recipe(name, ingredients, steps, timers, imageURL)
        if name == '':
            return ValueError
        else:
            recipe.save_to_file(name.lower().replace(" ", "_") + ".json")
        self.destroy()

class EditMode(tk.Toplevel):    
    def __init__(self, parent, recipe):
        super().__init__(parent)
        self.title("Editar Receta")
        name = recipe['name']

        with open(f'../Proyecto-Final-Python/{name}' + '.json', 'r') as re:
            receta = json.load(re)
            nombre = receta['name']
            url = receta['imageURL']
            ingredients = receta['ingredients']
            pasos = receta['steps']
            tiempo = receta['timers']

            #Variables 
            name = tk.StringVar()
            name.set(nombre)

            imageurl = tk.StringVar()
            imageurl.set(url)            

    # Crear widgets para el nombre de la receta
        tk.Label(self, text="Nombre:").grid(row=0, column=0, sticky='W', pady=10)
        self.name_entry = tk.Entry(self, textvariable=name)
        self.name_entry.grid(row=0, column=1,ipadx=40)

        tk.Label(self, text="URL de Imagen:").grid(row=1, column=0, sticky='W')
        self.imageURL_entry = tk.Entry(self, textvariable=imageurl)
        self.imageURL_entry.grid(row=1, column=1, pady=5, ipadx=40, padx=10)

        #########################################################
        #ingredientes
        # START
        self.ingredient_frame_edit = tk.LabelFrame(self, text="Ingredientes")
        self.ingredient_frame_edit.grid(row=2, column=0, padx=10)
        self.ingredients_text = tk.Listbox(self.ingredient_frame_edit, listvariable=ingredients)

        self.ingredients_list = []

        #self.ingredients_text.bind('<<ListboxSelect>>', self.edit_ingredient)

        for ingredient in ingredients:
            self.ingredients_list.append(ingredient)  
            self.ingredients_text.insert(tk.END, ingredient['name'].upper()+':'+ingredient['quantity'])

        inx = self.ingredients_text.get(0)
        print('inde', inx)
            #self.edit_ingredient(inx)

            # Crear botón Editar para cada ingrediente
            #edit_button = tk.Button(self.ingredient_frame, text="Editar", command= lambda index=len(self.ingredients_list)-1: self.edit_ingredient(index))
            #edit_button.grid(row=len(self.ingredients_list)-1, column=1, padx=5)
                                                                                                                                  ##### Print #######
        self.ingredients_text.grid(row=2, column=0)
        index1 = self.ingredients_text.selection_get()
        print('index', index1)                                                                                                    ##### Print #######

        # Menu para nombre, cantidad y boton
        self.menu_ingredientes = tk.Frame(self)
        self.menu_ingredientes.grid(row=2,column=1, sticky='W')

        # END
        ##########################################################

        ####################################
        # Pasos

        # Marco para pasos
        self.steps_frame = tk.LabelFrame(self, text="Pasos")
        self.steps_frame.grid(row=3, column=0, pady=10)
        self.steps_text = tk.Listbox(self.steps_frame)
        self.steps_text.grid(row=3, column=0)

        # Menu para paso y agregar paso
        self.menu_steps = tk.Frame(self)
        self.menu_steps.grid(row=3,column=1, sticky='W')

        tk.Label(self.menu_steps, text="Pasos:").grid(row=0, column=0, sticky='W')
        self.steps_entry = tk.Entry(self.menu_steps)
        self.steps_entry.grid(row=1, column=0)

        tk.Button(self.menu_steps, text="Agregar paso", padx=10, pady=10).grid(row=2, column=0,  pady=10)

        ####################################

        ####################################
        # Timers

        # Marco para pasos
        self.timer_frame = tk.LabelFrame(self, text="Tiempos")
        self.timer_frame.grid(row=4, column=0, pady=10)
        self.timer_text = tk.Listbox(self.timer_frame)
        self.timer_text.grid(row=4, column=0)

        # Menu para paso y agregar paso
        self.menu_timer = tk.Frame(self)
        self.menu_timer.grid(row=4,column=1, sticky='W')


        tk.Label(self.menu_timer, text="Temporizadores:").grid(row=0, sticky='W')
        self.timers_entry = tk.Entry(self.menu_timer)
        self.timers_entry.grid(row=1)

        tk.Button(self.menu_timer, text="Agregar tiempo", padx=10, pady=10, ).grid(row=2, column=0, pady=10)

        ####################################

        # Crear boton para guardar la receta
        tk.Button(self, text="Guardar").grid(row=5, column=0,columnspan=2, ipadx=100, pady=10)

    def edit_ingredient(self, index):
        
        print(index)
        # Obtener el ingrediente seleccionado
        ingredient = self.ingredients_list[index]

        # Crear variables de control para las entradas de texto
        name_var = tk.StringVar(value=ingredient['name'])
        quantity_var = tk.StringVar(value=ingredient['quantity'])

        # Crear widgets para el nombre y cantidad del ingrediente
        tk.Label(self.menu_ingredientes, text="Nombre:").grid(row=0, column=0, sticky='W', pady=10)
        name_entry = tk.Entry(self.menu_ingredientes, textvariable=name_var)
        name_entry.grid(row=0, column=1)

        tk.Label(self.menu_ingredientes, text="Cantidad:").grid(row=1, column=0, sticky='W', pady=10)
        quantity_entry = tk.Entry(self.menu_ingredientes, textvariable=quantity_var)
        quantity_entry.grid(row=1, column=1)

        # Crear botón para guardar los cambios
        #save_button = tk.Button(edit_window, text="Guardar", command=lambda: self.save_ingredient(index, name_var.get(), quantity_var.get(), edit_window))
        #save_button.grid(row=2, column=0, columnspan=2, pady=10)

root = tk.Tk()
app = RecipeBook(root)
root.mainloop()
