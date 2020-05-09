from Vertice import Vertice
from Arista import Arista
import sys
import re
import math 
import copy

class Grafo:
    def __init__(self, M: list):
        self.__V = []
        self.__A = []
        self.__matrizDistancias = M
        self.__costoAsociado = 0
        self.cargarDesdeMatriz(M)

    def setA(self, A):
        self.__A = A

    def setV(self, V):
        self.__V = V

    def setCostoAsociado(self, costo):
        self.__costoAsociado = costo
    
    def getCostoAsociado(self):
        return self.__costoAsociado

    def getA(self):
        return self.__A

    def getV(self):
        return self.__V

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
        cantV = len(self.__V)
        for row in range(1,cantV):
            for col in range(1, cantV):
                arista_aux = Arista(row,col,self.__matrizDistancias[row][col])
                A.append(arista_aux)
        
        print("Aristas: \n",A)
        return A
    
    #Nose para que sirve? en q caso se lo utiliza
    def rellenarAristas(self):
        A = self.__A
        V = self.__V
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
    
    def aristasConOrigen(self, V):
        salida = []
        for arista in self.getA():
            if((arista.tieneOrigen(V)) == True):
                salida.append(arista)

        return salida

    def aristasConDestino(self, V):
        salida = []
        for arista in self.getA():
            if((arista.tieneDestino(V)) == True):
                salida.append(arista)
        return salida
    
    #Cargar las aristas
    def cargarDesdeMatriz(self, Matriz):
        for fila in range(0,len(Matriz)):
            self.__V.append(fila+1)
            for columna in range(0, len(Matriz[fila])):
                aux = Arista(self.__V[fila],self.__V[columna],(Matriz[fila][columna]))
                self.__A.append(aux)


    def getMatriz(self):
        return self.__matrizDistancias
    
    def setMatriz(self, M):
        self.__matrizDistancias = M
