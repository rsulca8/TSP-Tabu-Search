from Vertice import Vertice
from Arista import Arista
import sys
import re
import math 
import copy

class Grafo:
    def __init__(self, archivo:str, V:list, M: list):
        self._V = V
        self._A = []
        self.__matrizDistancias = []
        if (archivo is None):
            self.__matrizDistancias = M
            self.cargaAristas()
        elif (V is None and M is None):
            self.cargarDesdeEUC_2D(archivo)
        else:
            pass

    def setA(self, A):
        self._A = A

    def setV(self, V):
        self._V = V

    def getA(self):
        return self._A

    def getV(self):
        return self._V

    #Compara entre 2. Se fija si hay aristas de A contenidas en si misma. Si hay aristas, se detiene
    def contieneA(self,A):
        sigue = True
        i = 0
        n = len(self.getA())
        while((sigue == True) and i < n):
            if(self.getA()[i].tieneOrigen(A.getOrigen()) and self.getA()[i].tieneDestino(A.getDestino())):
                sigue = False
                i=n
            i+=1
        return not(sigue)

    def getCostoArista(self, A):
        sigue = True
        i = 0
        n = len(self.getA())
        while((sigue == True) and i < n):
            if(self.getA()[i].tieneOrigen(A.getOrigen()) and self.getA()[i].tieneDestino(A.getDestino())):
                sigue = False
            i+=1
        return i-1

    def cargaAristas(self):
        A=[]
        cantV = len(self._V)
        for row in range(1,cantV):
            for col in range(1, cantV):
                arista_aux = Arista(row,col,self.__matrizDistancias[row][col])
                A.append(arista_aux)
        
        print("Aristas: \n",A)
        return A
    
    #Nose para que sirve? en q caso se lo utiliza
    def rellenarAristas(self):
        A = self._A
        V = self._V
        for i in V:
            for j in V:
                arista_aux = Arista(i,j,0)
                if(not(self.contieneA(arista_aux))):
                    A.append(arista_aux)

    def __str__(self):
        salida = ""
        V = self.getV()
        #Muestra la primera fila con los vertices
        if(len(self.__matrizDistancias) == len(self.getV())):
            for i in range(0,len(V)):
                salida += str(V[i]) + "    "

            salida = salida + "\n"
            for i in range(0,len(V)):
                salida += str(V[i]) + "    "
                for j in range(0,len(V)):
                    salida += str(self.__matrizDistancias[i][j]) + "    "
                salida = salida + "\n"
        else:
            for i in range(0,len(V)):
                salida += str(V[i]) + "    "

            salida = salida + "\n"
            for i in V:
                salida += str(i) + "    "
                for j in V:
                    indice = self.getCostoArista(Arista(i,j,0))
                    salida += str(self.getA()[indice].getPeso()) + "    "
                salida = salida + "\n"
        return salida
    
    def nodosConOrigen(self, V):
        salida = []
        for arista in self.getA():
            if((arista.tieneOrigen(V)) == True):
                salida.append(arista)

        return salida

    def nodosConDestino(self, V):
        salida = []
        for arista in self.getA():
            if((arista.tieneDestino(V)) == True):
                salida.append(arista)
        return salida

    def cargarDesdeMatriz(self,V: list,Matriz: list):
        A = []
        if(1!=1):
            print("La cantidad de vertices debe ser la misma que la cantidad de filas de la Matriz")
        else:
            for fila in range(0,len(Matriz)):
                for columna in range(0, len(Matriz[fila])):
                    aux = Arista(V[fila],V[columna],(Matriz[fila][columna]))
                    A.append(aux)
        self._A = A 

    def getMatriz(self):
        return self.__matrizDistancias
    
    def setMatriz(self, M):
        self.__matrizDistancias = M


    #Convierto mi archivo EUC_2D en una matriz en la cual pueda trabajar
    def cargarDesdeEUC_2D(self,pathArchivo):
        archivo = open(pathArchivo,"r")


        self.__matrizDistancias = []
        vertices = []
        aristas = []
        lineas = archivo.readlines()
        #Busco la posiciones de..
        indSeccionCoord = lineas.index("NODE_COORD_SECTION\n")
        lineaEOF = lineas.index("EOF\n")
        #dim = lineaEOF - indSeccionCoord #y guardo el tamaño de los datos

        #Lista donde irán las coordenadas (vertice, x, y)
        coordenadas = []

        #Separa las coordenadas en una matriz, es una lista de listas (vertice, coordA, coordB)
        for i in range(indSeccionCoord+1, lineaEOF):
            textoLinea = lineas[i]  
            textoLinea = re.sub("\n", "", textoLinea) #Elimina los saltos de línea
            splitLinea = textoLinea.split(" ") #Divide la línea por " " 
            coordenadas.append([splitLinea[0],splitLinea[1],splitLinea[2]]) #[[v1,x1,y1], [v2,x2,y2], ...]
        
        print(coordenadas)

        #Arma la matriz de distancias. Calculo la distancia euclidea
        for coordRow in coordenadas:
            fila = []
            v_origen = Vertice(coordRow[0]) #Obtengo V de [[V,x,y], ...]
            print("\n v_origen:",v_origen)
            vertices.append(v_origen) #[1]
            for coordCol in coordenadas:
                x1 = float(coordRow[1])
                y1 = float(coordRow[2])
                x2 = float(coordCol[1])
                y2 = float(coordCol[2])
                dist = distancia(x1,y1,x2,y2)
                #Para el primer caso. Calculando la distancia euclidea entre si mismo da 0
                if(dist == 0):
                    dist = 999999999999 #El modelo no debería tener en cuenta a las diagonal, pero por las dudas
                fila.append(dist)
                v_destino = Vertice(coordCol[0])
                aristas.append(Arista(v_origen,v_destino,dist))
            self.__matrizDistancias.append(fila)
            self.setA(aristas)
            self.setV(vertices)

        print(aristas)
        #print(self.__matrizDistancias)


    def obtenerSolucionVecinoCercano(self,inicio:Vertice):
        M = self.getMatriz()
        V = self.getV()
        copiaG = copy.copy(self)

        recorrido = []
        visitados = []
        aristasIniciales = copiaG.nodosConOrigen(inicio)
        while(len(copiaG.getA())!=0):
            vecinoCercano = copiaG.getAristaMinima(aristasIniciales)
            recorrido.append(vecinoCercano)
            visitados.append(vecinoCercano.getOrigen())
            for j in visitados:
                    aristasIniciales += copiaG.nodosConDestino(j)        
            for i in (aristasIniciales):
                if(i in copiaG.getA()):
                    copiaG.getA().remove(i)

            aristasIniciales = copiaG.nodosConOrigen(vecinoCercano.getDestino())

        return recorrido

    def getAristaMinima(self,listaAristas):
        minimo = listaAristas[0]
        for i in listaAristas:
            if(i.getPeso() < minimo.getPeso()):
                minimo = i

        return minimo

#Calcula la distancia euclidea en dos nodos A y B 
def distancia(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
