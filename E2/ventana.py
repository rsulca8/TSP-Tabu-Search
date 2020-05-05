import tkinter as tk
from Grafo import Grafo 
from Table import Table
from Vertice import Vertice
import tkinter.filedialog
from tkinter import ttk

class Ventana(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("600x300")
        self.titulo()
        self.barraMenus()
        self.menuGrafo()
        self.vecinoCercano()
    
    def titulo(self):
        self.__labelTitulo = tk.Label(self,text = "TSP Solver con Tabu Search")
        self.__labelTitulo.pack()

    def barraMenus(self):
        self.__menu = tk.Menu(self)
        self.__menuArchivo = tk.Menu(self.__menu)
        self.__menuArchivo.add_command(label="Abrir", command=self.openFile)
        self.__menu.add_cascade(label="Archivo", menu=self.__menuArchivo)
        self.config(menu = self.__menu)
    
    def menuGrafo(self):
        self.__labelEstadoGrafo = tk.Label(self, text = "No se ha cargado Grafo")
        self.__botonMostrarGrafo = tk.Button(self, text = "Mostrar Grafo", command=self.mostrarGrafo,state="disabled")
        self.__labelObtenerCiclo = tk.Label(self, text = "Obtener Ciclo Hamiltoneano más corto ;)")
        self.__labelEstadoGrafo.pack(fill=tk.X, padx=40)
        self.__botonMostrarGrafo.pack(fill=tk.X, padx=40)
        self.__labelObtenerCiclo.pack(fill=tk.X, padx=40)


    def vecinoCercano(self):
        self.__botonVecinoCercano = tk.Button(self, text = "Solucion Usando el Vecino Cercano", command=self.mostrarGrafo,state="disabled")
        self.__botonVecinoCercano = tk.Button(self, text = "Seleccione Vertice Inicial", command=self.mostrarGrafo,state="disabled")
        self.__comboVerticeInicial = ttk.Combobox(self, state="readonly")
        self.__botonMostrarGrafo = tk.Button(self, text = "Mostrar Grafo", command=self.mostrarGrafo,state="disabled")
        self.__botonVecinoCercano.pack(fill=tk.X, padx=40)
        self.__comboVerticeInicial.pack(padx=40)       

    def openFile(self):
        self.__nombreArchivo  = tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
        print(self.__nombreArchivo)
        self.__g = Grafo(self.__nombreArchivo)
        self.__labelEstadoGrafo.configure(text = "Grafo Cargado")
        self.__botonMostrarGrafo.configure(state="normal")
        self.__vertices = tuple(self.__g.getV())
        self.__comboVerticeInicial.configure(values = self.__vertices)
        #print(self.__g)

    def mostrarSolucionVecinoCercano(self): 
        lista = self.__g.obtenerSolucionVecinoCercano(Vertice(int(self.__comboVerticeInicial.get())))

    def mostrarGrafo(self):
        self.__ventanaTabla = tk.Toplevel(self)
        self.__ventanaTabla.title("Grafo Cargado")
        self.__ventanaTabla.geometry('600x600')
        
        #vertices_header = tuple(i for i in str(self.__g.getV()[i].getValue()))
        #print(vertices_header)
        vertices_header=verticesATupla([Vertice(" ")]+self.__g.getV())
        tabla = Table(self.__ventanaTabla, title="Vertices", headers=vertices_header)
        M = self.__g.getMatriz()
        for i in range(0,len(M)):
            fila = []
            fila.append(i+1)
            for j in range(0,len(M)):
                fila.append(M[i][j])
            tabla.add_row(fila)
        tabla.pack()


def verticesATupla(V):
    v = []
    for i in V:
        v.append(str(i.getValue()))
    return v

ventana = Ventana()

ventana.mainloop()