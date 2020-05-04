from Vertice import Vertice
from Arista import Arista
import sys
import re
import math 

class Grafo:
    def __init__(self,V:list,A: list):
        self._V = V
        self._A = A
        self.rellenarAristas() 


    def setA(self, A):
        self._A = A

    def setV(self, V):
        self._V = V

    def getA(self):
        return self._A

    def getV(self):
        return self._V

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
        print(str(self._A))
        for arista in self._A:
            if(arista.getOrigen() == V):
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
       
    
        #Hay un cambio
        
        #Puto el que lee
        




