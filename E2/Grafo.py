from Vertice import Vertice
from Arista import Arista
import sys
import re
import math 

class Grafo:
    def __init__(self,V,A):
        self._V = V
        self._A = A 

    def setA(self, A):
        self._A = A

    def setV(self, V):
        self._V = V

    def getA(self):
        return self._A

    def getV(self):
        return self._V

    def __str__(self):
        salida = ""
        A = self._A
        for i in range(0,len(A)):
            salida = salida + str(A[i]) + "\n"
        return salida
    
    def cargarDesdeMatriz(self,V: list,Matriz: list):
        A = []
        print(type(Matriz))
        if(len(V)!= len(Matriz)):
            print("La cantidad de vertices debe ser la misma que la cantidad de filas de la Matriz")
        else:
            for fila in range(0,Matriz):
                for columna in range(0, fila):
                    A.append(Arista(V[fila],V[columna],Matriz[fila][columna]))
        self._A = A 
       
    
        #Hay un cambio
        
        




