import tkinter as tk
import re
import math
from TSP import TSP
from Table import Table
from Vertice import Vertice
import tkinter.filedialog
import os

class Ventana(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("400x400+350+150")
        self.titulo()
        self.barraMenus()
        self.menuGrafo()
        self.__matrizDistancias=[]
    
    def titulo(self):
        self.__labelTitulo = tk.Label(self,text = "TSP Solver con Tabu Search")
        self.__labelTitulo.pack()

    def barraMenus(self):
        self.__menu = tk.Menu(self)
        self.__menuArchivo = tk.Menu(self.__menu)
        self.__menuArchivo.add_command(label="New File", command=self.newFile)
        self.__menuArchivo.add_separator()
        self.__menuArchivo.add_command(label="Open File", command=self.openFile)
        self.__menu.add_cascade(label="File", menu=self.__menuArchivo)
        self.config(menu = self.__menu)
    
    def menuGrafo(self):
        self.__labelEstadoGrafo = tk.Label(self, text = "No se ha cargado Grafo")
        self.__botonMostrarGrafo = tk.Button(self, text = "Mostrar Grafo", command=self.mostrarGrafo,state="disabled")
        self.__labelObtenerCiclo = tk.Label(self, text = "Obtener Ciclo Hamiltoneano más corto ;)")
        self.__botonVecinoCercano = tk.Button(self, text = "Solucion Usando el Vecino Cercano", command=self.mostrarGrafo,state="disabled")
        self.__labelEstadoGrafo.pack(fill=tk.X, padx=40)
        self.__botonMostrarGrafo.pack(fill=tk.X, padx=40)
        self.__botonVecinoCercano.pack(fill=tk.X, padx=40)
        self.__labelObtenerCiclo.pack(fill=tk.X, padx=40)

    def openFile(self):
        nombreArchivo  = tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
        #self.__g = Grafo(self.__nombreArchivo, None, None)
        self.cargarDesdeEUC_2D(nombreArchivo)
        self.__nombreArchivo = os.path.splitext(os.path.basename(nombreArchivo))[0]
        self.__tsp = TSP(self.__matrizDistancias, self.__nombreArchivo)
        self.__labelEstadoGrafo.configure(text = "Grafo Cargado")
        self.__botonMostrarGrafo.configure(state="normal")
                
    #Convierto mi archivo EUC_2D en una matriz en la cual pueda trabajar
    def cargarDesdeEUC_2D(self,pathArchivo):
        archivo = open(pathArchivo,"r")
        lineas = archivo.readlines()
        #Busco la posiciones de..
        indSeccionCoord = lineas.index("NODE_COORD_SECTION\n")
        lineaEOF = lineas.index("EOF\n")

        #Lista donde irán las coordenadas (vertice, x, y)
        coordenadas = []
        #Separa las coordenadas en una matriz, es una lista de listas (vertice, coordA, coordB)
        for i in range(indSeccionCoord+1, lineaEOF):
            textoLinea = lineas[i]  
            textoLinea = re.sub("\n", "", textoLinea) #Elimina los saltos de línea
            splitLinea = textoLinea.split(" ") #Divide la línea por " " 
            coordenadas.append([splitLinea[0],splitLinea[1],splitLinea[2]]) #[[v1,x1,y1], [v2,x2,y2], ...]
        
        matriz = []
        #Arma la matriz de distancias. Calculo la distancia euclidea
        for coordRow in coordenadas:
            fila = []            
            for coordCol in coordenadas:
                x1 = float(coordRow[1])
                y1 = float(coordRow[2])
                x2 = float(coordCol[1])
                y2 = float(coordCol[2])
                dist = self.distancia(x1,y1,x2,y2)
                
                #Para el primer caso. Calculando la distancia euclidea entre si mismo da 0
                if(dist == 0):
                    dist = 999999999999 #El modelo no debería tener en cuenta a las diagonal, pero por las dudas
                fila.append(dist)
                
            matriz.append(fila)
        self.__matrizDistancias =  matriz

    def distancia(self, x1,y1,x2,y2):
        return round(math.sqrt((x1-x2)**2+(y1-y2)**2),2)
   
    #Cargo una matriz de forma manual. Ingreso el nro de vertices y verifico
    def newFile(self):
        t=tk.Toplevel()
        t.geometry("400x100+350+190")

        label1= tk.Label(t, text="Cantidad de vertices:")
        label1.grid(row=0)
        
        nroVertices = tk.StringVar()
        entry1= tk.Entry(t, textvariable=nroVertices)
        entry1.grid(row=0, column=1)

        #Verifico que sea un valor correcto
        def verificar():
            label2= tk.Label(t, text="Debe ser entero mayor que 0")
            try:
                cant = nroVertices.get()
                cant = int(cant)
                #print(cant)
                if(cant is None or cant<=0):
                    label2.grid(row=1,column=0)
                else:
                    t.destroy()
                    self._nroVertices=cant+1 #Defino la cantidad ingresada +1. Para los labels q indican el nro de filas y columnas
                    self.newFile2()
            except ValueError:
                    label2.grid(row=1,column=1)

        button1= tk.Button(t,text='Aceptar', command=verificar)
        button1.grid(row=0,column=2, padx=4, pady=4)

        label = tk.Label(t, text="Nueva ventana")
        label.pack(side="top", fill="both")

    #Cargo los valores de la matriz
    def newFile2(self):
        t=tk.Toplevel()
        self._entry={}
        
        #Cancelar: vuelvo a la primera pantalla
        def exit():
            t.destroy()
        
        def aceptar():
            self.get()
            t.destroy()

        btnCancelar = tk.Button(t, text = "Cancelar", width=7, command=exit)
        btnAceptar = tk.Button(t,text = "Aceptar", width=7,command=aceptar)

        # registra un comando para usar para la validacion
        vcmd = (self.register(self._validate), "%P")

        for r in range(0, self._nroVertices):
            for c in range(0, self._nroVertices):
                if(c!=0 and r!=0):
                    index = (r-1, c-1)
                    cell = tk.Entry(t, width=7, validate="key", validatecommand=vcmd)
                    cell.grid(row=r, column=c, stick="nsew")
                    if(c==r):
                        cell.insert(0,99999)
                    if(c<=r):
                        cell.configure(state='disabled')
                    self._entry[index]=cell
                elif(not(c==0 ^ r==0)):
                    label = tk.Label(t, text=r+c, width=7)
                    label.grid(row=r, column=c)

        btnAceptar.grid(row=self._nroVertices+1, column=self._nroVertices//2, columnspan=3)
        btnCancelar.grid(row=self._nroVertices+1, column=0, columnspan=3)

    #Valida que sea ingrese un numero de tipo float o entero
    def _validate(self, P):  

        if P.strip() == "":
            return True

        try:
            if(float(P)==P):
                print()
        except ValueError:
            self.bell()
            return False
        return True

    def get(self):
        '''Return a list of lists, containing the data in the table'''
        matrizDist = []
        vertices = []

        for row in range(0, self._nroVertices-1):
            current_row = []
            for column in range(0, self._nroVertices-1):
                index = (row, column)
                if (column<row):
                    index = (column, row)
                    current_row.append(float((self._entry[index].get())))
                else:
                    current_row.append(float((self._entry[index].get())))
            matrizDist.append(current_row)
            vertices.append(row+1)
        
        print("Matriz distancias: ",self.__matrizDistancias)
        
        self.__matrizDistancias=matrizDist
        self.__tsp=TSP(self.__matrizDistancias, "MatrizNueva")
        

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