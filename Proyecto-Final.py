from tkinter import *
from tkinter import ttk
root = Tk()

frm = ttk.Frame(root, padding=50)
frm.grid()
ttk.Label(frm, text="Hola mundo soy german!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)
#btn = Button(frm, bg="green", text="Hola", fg="white").grid(column=1, row=1)
#ttk.OptionMenu(frm, variable="German").grid(column=1, row=1)
ttk.Combobox(frm).grid(column=1, row=1)
root.mainloop()