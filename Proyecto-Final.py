import os
import json
from PIL import Image, ImageTk
import tkinter as tk

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
            #
            #
            #Cambios necesarios de ruta
            #
            #
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
        self.btn_receta = tk.Button(self.frame_list, text="Receta del dia ★")
        self.btn_receta.grid(row=0, column=0, sticky='W')

        self.label_search = tk.Label(self.frame_list, text="Search")
        self.label_search.grid(row=1, column=0,sticky='N'+'W') # type: ignore
        self.search = tk.Entry(self.frame_list).grid(row=1, column=1,sticky='N'+'W')

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
        self.frame_btns, text="Eliminar Receta")
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
        index = self.list_recipes.curselection()[0]
        self.recipe = self.list_recipes.selection_get()                                                                                   ##### PRINT #####

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

        self.text_recipe.grid(padx=10, pady=10)

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
        self.times.append(int(time))
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

        with open(f'../Proyecto-Final-Python/{recipe}' + '.json', 'r') as re:
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

        self.ingredient_frame = tk.LabelFrame(self, text="Ingredientes")
        self.ingredient_frame.grid(row=2, column=0, padx=10)
        self.ingredients_text = tk.Listbox(self.ingredient_frame, listvariable=ingredients)
        for ingredient in ingredients:
            ingredient_name = ingredient['name']
            ingredient_quantity = ingredient['quantity']
            var = ingredient_name +':'+ ingredient_quantity
            print(var)                                                                                                  ##### Print #######
            self.ingredients_text.insert(tk.END, var)
        self.ingredients_text.grid(row=2, column=0)
        index = self.ingredients_text.curselection()[0]
        print(index)                                                                                                    ##### Print #######

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

        tk.Button(self.menu_ingredientes, text="Agregar Ingrediente", padx=10, pady=10).grid(row=6, column=1, pady=10)

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

root = tk.Tk()
app = RecipeBook(root)
root.mainloop()
