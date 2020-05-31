import tkinter as tk
import re
import math
import time
from TSP import TSP
from Table import Table
from Vertice import Vertice
import tkinter.filedialog
import os
from tkinter import ttk
from os import listdir
from os.path import isfile, join
import ntpath

class Ventana(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("600x600")
        self.title("TSP Solver con Tabu Search")
        self.__matrizDistancias=[]
        self.__nro = 0
        self.__openFolder = False
        self.__tabs = ttk.Notebook(self)
        self.elementosGUI()
        self.__frames = []
        self.barraMenus()
    
    def barraMenus(self):
        self.__menu = tk.Menu(self)
        self.__menuArchivo = tk.Menu(self.__menu)
        self.__menuArchivo.add_command(label="New File", command=self.newFile)
        self.__menuArchivo.add_separator()
        self.__menuArchivo.add_command(label="Open File", command=self.openFile)
        self.__menu.add_cascade(label="File", menu=self.__menuArchivo)
        self.__menuArchivo.add_command(label="Open Folder", command=self.openFolder)

        self.config(menu = self.__menu)
    
    def elementosGUI(self):
        self.__labelSolInicial = []
        self.__labelEstadoGrafo = []
        self.__eSolInicial = []
        self.__combo1 = []
        self.__labelNroIntercambios = []
        self.__spinboxNroIntercambios = []
        self.__eOpt = []
        self.__comboOpt = []
        self.__nroIntercambios = []
        self.__labelTenureADD = []
        self.__labelTenureDROP = []
        self.__boxADD = []
        self.__spinboxDROP = []
        self.__spinboxADD = []
        self.__boxDROP = []
        self.__labelTiempoEjecucion = []
        self.__eTime = []
        self.__entryTiempoEjecucion = []
        self.__labelTEmin = []
        self.__areaDatos = []
        self.__label_RecomiendacTiempo = []
        self.__matrizDistancias = []
        self.__labelRecomienda =[]
    
    def menuConfig(self,frame,i):
        self.__labelEstadoGrafo.append(tk.Label(frame, text = "No se ha cargado Grafo"))
        self.__labelEstadoGrafo[i].place(relx=0.4,rely=0.05)
        #Pestañas            
        
        #Solucion inicial
        self.__labelSolInicial.append(tk.Label(frame, text = "Solucion inicial"))
        self.__labelSolInicial[i].place(relx=0.3, rely=0.10)
        
        self.__combo1list=['Vecino mas cercano', 'Al azar']
        self.__eSolInicial.append(tk.StringVar())
        self.__combo1.append(ttk.Combobox(frame, textvariable=self.__eSolInicial, values=self.__combo1list, width = 29, state = "disabled"))
        self.__combo1[i].place(relx=0.4, rely=0.10)
        
        #Nro de intercambios
        self.__labelNroIntercambios.append(tk.Label(frame, text= "Max Intercambios"))
        self.__labelNroIntercambios[i].place(relx=0.3, rely = 0.20)
        self.__nroIntercambios.append(tk.IntVar())
        self.__spinboxNroIntercambios.append(tk.Spinbox(frame, from_ = 1, to = 3, width = 5, state = "disabled", textvariable = self.__nroIntercambios))
        self.__spinboxNroIntercambios[i].place(relx=0.6, rely=0.20)
        
        self.__combo2list=['2-opt', '3-opt']
        self.__eOpt.append(tk.StringVar())
        self.__comboOpt.append(ttk.Combobox(frame, textvariable=self.__eOpt, values=self.__combo2list, width = 5, state = "disabled"))
        self.__comboOpt[i].place(relx=0.75, rely=0.20)        
        
        #Tenure ADD
        self.__labelTenureADD.append(tk.Label(frame, text = "Tenure ADD"))
        self.__labelTenureADD[i].place(relx=0.2, rely=0.27)
        self.__boxADD.append(tk.IntVar())
        self.__spinboxADD.append(tk.Spinbox(frame, from_ = 1, to = 100, width = 5, state = "disabled", textvariable = self.__boxADD))
        self.__spinboxADD[i].place(relx=0.4, rely=0.27)

        #Tenure DROP
        self.__labelTenureDROP.append(tk.Label(frame, text = "Tenure DROP"))
        self.__labelTenureDROP[i].place(relx=0.55, rely=0.27)
        self.__boxDROP.append(tk.IntVar())
        self.__spinboxDROP.append(tk.Spinbox(frame, from_ = 1, to = 100, width = 5, state = "disabled", textvariable = self.__boxDROP))
        self.__spinboxDROP[i].place(relx=0.8, rely=0.27)
        
        #Condicion de parada
        self.__labelTiempoEjecucion.append(tk.Label(frame, text = "Tiempo de ejecución"))
        self.__labelTiempoEjecucion[i].place(relx=0.2, rely=0.45)
        self.__eTime.append(tk.StringVar())
        self.__entryTiempoEjecucion.append(tk.Entry(frame, textvariable = self.__eTime, width = 25, state = "disabled"))
        self.__entryTiempoEjecucion[i].place(relx=0.5, rely=0.45,relwidth=0.20)
        self.__labelTEmin.append(tk.Label(frame, text = "(min)"))
        self.__labelTEmin[i].place(relx=0.75, rely=0.45)

        #Mostrar datos
        self.__areaDatos.append(tk.Text(frame, state ="disabled"))
        self.__areaDatos[i].place(relx=0.2, rely=0.6, relwidth=0.6, relheight=0.4)
   



    def cargarDatos(self):
        for i in range(0,len(self.__listaInstancias)):
            self.__nombreArchivo = self.__listaInstancias[i]
            print("RESOLVIENDO ------------------> "+str(self.__nombreArchivo))
            self.__tsp = TSP(self.__matrizDistancias[i], self.__nombreArchivo+"_"+str(self.__eTime[i].get())+"min", self.__eSolInicial[i].get(), self.__nroIntercambios[i].get(),
            self.__eOpt[i].get(), self.__boxADD[i].get(), self.__boxDROP[i].get(), self.__eTime[i].get(), self.__optimo)

        else:
            print("No se permite valores vacios")

    def calcularDatos(self,i):
        if(self.__openFolder):
            self.__labelEstadoGrafo[i].configure(text = "Grafos Cargados")
        else:
            self.__labelEstadoGrafo[i].configure(text = "Grafo Cargado")
            
        self.__labelRecomienda.append(tk.Label(text = "Se recomienda los siguientes valores..."))
        self.__labelRecomienda[i].place(relx=0.3,rely=0.5)        
        
        tenureADD = int(len(self.__matrizDistancias[i])*0.1)
        tenureDROP = int(len(self.__matrizDistancias[i])*0.1)+1

        self.__combo1[i].configure(state = "readonly")
        self.__combo1[i].set('Vecino mas cercano')
        self.__comboOpt[i].configure(state = "readonly")
        self.__comboOpt[i].set('2-opt')

        #Nro intercambios
        cantIntercambios = 2

        self.__nroIntercambios[i].set(cantIntercambios)
        self.__spinboxNroIntercambios[i].configure(state = "readonly", textvariable = self.__nroIntercambios[i])

        #Tenure ADD y DROP
        self.__boxADD[i].set(tenureADD)
        self.__spinboxADD[i].configure(state = "readonly", textvariable=self.__boxADD[i])

        self.__boxDROP[i].set(tenureDROP)
        self.__spinboxDROP[i].configure(state = "readonly", textvariable=self.__boxDROP[i])
        
        self.__label_RecomiendacTiempo.append(tk.Label(text = "Se recomienda como minimo"))
        self.__label_RecomiendacTiempo[i].place(relx=0.4, rely=0.35)
        self.__eTime[i].set(15.0)
        self.__entryTiempoEjecucion[i].configure(state = "normal", textvariable = self.__eTime[i])
        return 

    def listToString(self, s): 
        str1 = ""  
        for ele in s:  
            str1 += ele   

        return str1

    def tabs(self, instancias):
        for i in range(0,len(instancias)):
            print(instancias[i])
            self.__frames.append(tk.Frame(self)) 
            self.menuConfig(self.__frames[i],i)
            self.__tabs.add(child=self.__frames[i],text=instancias[i])
            self.cargarDesdeEUC_2D(self.__mypath+"/"+self.__listaInstancias[i],i)
            self.calcularDatos(i)
            
        self.__tabs.pack(expand=1, fill="both")
        self.__Ok = tk.Button(self, text = "Calcular", command=self.cargarDatos, width = 10, height =30, state="normal")
        self.__Ok.pack(after=self.__tabs)

    def openFolder(self):
        self.__mypath = tk.filedialog.askdirectory(initialdir = ".", title='Seleccione directorio con instancias')
        self.__listaInstancias = [f for f in listdir(self.__mypath) if isfile(join(self.__mypath, f))]
        self.__openFolder = True
        print(self.__listaInstancias)
        self.tabs(self.__listaInstancias)        


        self.__nombreArchivo = os.path.splitext(self.__listaInstancias[0])[0]
        print("Primera instancia: "+str(self.__nombreArchivo))
        #Calcular

       

    def openFile(self):
        self.__listaInstancias = tk.filedialog.askopenfilenames(initialdir = ".",title = "Seleccione Intancia/s TSP",filetypes = (("all files","*.*"),("tsp files","*.tsp")))
        self.__listaInstancias = list(self.__listaInstancias)
        self.__mypath = ntpath.split(self.__listaInstancias[0])[0]
        self.__listaInstancias = [ntpath.split(f)[1] for f in self.__listaInstancias]
        self.tabs(self.__listaInstancias)    
        self.__nombreArchivo = os.path.splitext(os.path.basename(self.__listaInstancias[0]))[0]
        #self.calcularDatos(i)

    #Convierto mi archivo EUC_2D en una matriz en la cual pueda trabajar
    def cargarDesdeEUC_2D(self,pathArchivo,i):
        archivo = open(pathArchivo,"r")
        lineas = archivo.readlines()
        #Busco la posiciones de..
        indSeccionCoord = lineas.index("NODE_COORD_SECTION\n")
        lineaEOF = lineas.index("EOF\n")
        lineaOptimo = [x for x in lineas[0:indSeccionCoord] if re.findall(r"OPTIMO:[\S 0-9]+",x)][0]
        self.__optimo = float(re.findall(r"[0-9]+",lineaOptimo)[0])
        print(self.__optimo)
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

            #print("Fila: "+str(fila))    
            matriz.append(fila)
        self.__matrizDistancias.append(matriz)

    def distancia(self, x1,y1,x2,y2):
        return round(math.sqrt((x1-x2)**2+(y1-y2)**2),3)
   
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
        self.__nombreArchivo = "Matriz Nueva"
        #self.calcularDatos()

    def getMatrizDistancas(self):
        return self.__matrizDistancias

    def verticesATupla(self, V):
        v = []
        for i in V:
            v.append(str(i.getValue()))
        return v


def archivoDePath(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


ventana = Ventana()
ventana.mainloop()