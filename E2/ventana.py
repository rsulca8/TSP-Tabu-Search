import tkinter as tk
from Grafo import Grafo 

import tkinter.filedialog

class Ventana(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self)
        self.titulo()
        self.barraMenus()
    
    def titulo(self):
        self.__labelTitulo = tk.Label(self,text = "TSP Solver con Tabu Search")
        self.__labelTitulo.pack()

    def barraMenus(self):
        self.__menu = tk.Menu(self)
        self.__menuArchivo = tk.Menu(self.__menu)
        self.__menuArchivo.add_command(label="Abrir", command=self.openFile())
        self.__menu.add_cascade(label="Archivo", menu=self.__menuArchivo)
        self.config(menu = self.__menu)

    def openFile(self):
        self.__nombreArchivo  = tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
        print(self.__nombreArchivo)
        self.__g = Grafo(self.__nombreArchivo)
        print(self.__g)

ventana = Ventana()

ventana.mainloop()