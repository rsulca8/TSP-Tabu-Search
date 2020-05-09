from Vertice import Vertice
from Arista import Arista
from Grafo import Grafo
import sys
import re
import math 
import copy
#Rasdfasdfasdfsdfa
class TSP:
    def __init__(self, M: list):
       self._G = Grafo(M)   #Grafo original
       self.__soluciones = []    #Lista de Grafos que corresponden a las soluciones
  
    def obtenerSolucionsVecinoCercano(self,inicio:Vertice):
        M = self.getMatriz()
        V = self.getV()
        copiaG = copy.copy(self)

        recorrido = []
        visitados = []
        aristasIniciales = copiaG.aristasConOrigen(inicio)
        while(len(copiaG.getA())!=0):
            vecinoCercano = copiaG.getAristaMinima(aristasIniciales)
            recorrido.append(vecinoCercano)
            visitados.append(vecinoCercano.getOrigen())
            for j in visitados:
                    aristasIniciales += copiaG.aristasConDestino(j)        
            for i in (aristasIniciales):
                if(i in copiaG.getA()):
                    copiaG.getA().remove(i)

            aristasIniciales = copiaG.aristasConOrigen(vecinoCercano.getDestino())

        return recorrido

    def getAristaMinima(self,listaAristas):
        minimo = listaAristas[0]
        for i in listaAristas:
            if(i.getPeso() < minimo.getPeso()):
                minimo = i

        return minimo

'''
[elementoTabu,tenureActual]


'''
    def tabuSearch():
        listaTabu = []
        ADD = []
        DROP = []


    
    def tabuSearch_1():
        add 

'''
[1,2,5,4,6,7,8,9,10,3,1] -> costo1
[(1,2),(2,5),(5,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,3),(3,1)] -> costo1

G.nodosConDestino(V(4)) = [(1,4)(2,4)(3,4)]
[1.get,2,3]
Solucion
    solV=[]
    solA=[]
    costo1=[]

    def compararSoluciones
    def 

1->6->3->4->5->2->1
(1,6) (6,3) (3,4) (4,5) (5,2) (2,1)     #(1,6), (6,3), (2,1) add

1->2->3->4->5->6->1
(1,2) (2,3) (3,4) (4,5) (5,6) (6,1)     #(2,3), (1,2), (6,1) drop
1->2    2->3    3->4    4->5


sol 
Iter 0
1->2->(3->(4)->5)->6->7->8->9->10->1

Iter 1
1->2->5->

#(2,3) (3,4) (10,1) drop
#(2,5) (10,3) (3,1) add

1->2->5->6->7->8->9->10->3->1 -> costo1

Iter 2
1->2->5->6->7->8->9->(10->3)->1 
1->2->5->6->7->(9->8)->10->3->1  -> costo2

Iter3..
ALGORITMO MAXI
1->2->5->6->7->9->8->10->3->1
1->2->(7)->6->(5)->9->8->10->3->1 -> costo3 

DROP (2,5) (5,6) (6,7) (7,9)
ADD  (2,7) (7,6) (6,5) (5,9)

                                                                        ADD                  DROP
#tabu active: 1                             2                       |   
#1                                                                  |   (2,5) (10,3) (3,1)   (2,3) (3,4) (10,1)

#2            (2,5) (10,3) (3,1)            (2,3) (3,4) (10,1)      |   (9,8)  (7,9) (8,10)  (9,10) (7,8)(8,9)

#3            (9,8) (7,9) (8,10)            (9,10) (7,8)(8,9)       |   
              (2,3) (3,4) (10,1)


                                                                        ADD                  DROP
#tabu active: 2                             3                       |   
#1                                                                  |   7                    5

#2            7                             5                       |   8                    3

#3            7 5 8                         3                       |   1                    4

#4            5 8 3 1                       4                       |   7                    2

#5            8 3 1 4                       2                        
{
Solucion: 1->2->5->6->7->9->8->10->3->1
List: {1,2,3,4,5,6,7,8,9,10}
{8,3,1,4,2} -> ListaTabú

Solucion: 1->2->5->6->7->10->8->9->3->1
List: {1,2,3,4,5,6,7,8,9,10}
{3,1,4,2,9,10} -> ListaTabú
}

Solucion: 1->2->5->6->7->10->8->9->3->1
List: {(1,2),(2,5),(5,6),(6,7),(7,10),(10,8),(8,9),(9,3),(3,1)}
{3,1,4,2,9,10} -> ListaTabú '''

'''
    procedure 2optSwap(route, i, k) {
        1. take route[0] to route[i-1] and add them in order to new_route
        2. take route[i] to route[k] and add them in reverse order to new_route
        3. take route[k+1] to end and add them in order to new_route
        return new_route;
'''

