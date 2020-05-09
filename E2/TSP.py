from Vertice import Vertice
from Arista import Arista
from Grafo import Grafo
from Tabu import Tabu
import random 
import sys
import re
import math 
import copy
#Rasdfasdfasdfsdfa
class TSP:
    def __init__(self, M: list):
       self._G = Grafo(M)   #Grafo original
       self.__soluciones = []    #Lista de Grafos que corresponden a las soluciones
       self.__soluciones.append(self.obtenerSolucionsVecinoCercano()) #La primera solucion es la del vecino mas cercano
       self.__tenureADD = 2 #Mas adelante que se ingrese por ventana
       self.__tenureDROP = 1 #idem jaja
       self.tabuSearch_Maxi()
  
    def obtenerSolucionsVecinoCercano(self):
        copiaG = copy.deepcopy(self)
        inicio = self._G.getVerticeInicio()

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

        g = self.Grafo()
        return recorrido

    def getAristaMinima(self,listaAristas):
        minimo = listaAristas[0]
        for i in listaAristas:
            if(i.getPeso() < minimo.getPeso()):
                minimo = i

        return minimo
    
    def tabuSearch_Maxi(self):
        lista_tabu = []     #Tiene objetos de la clase Tabu
        lista_permit = []   #Tiene objetos del tipo vertice
        DROP = []
        ADD = []
        Sol_Actual = self.__soluciones[len(self.__soluciones)-1] #Primera solución
        Sol_Optima = Sol_Actual #Solo para el primer caso 
        iterac = 10000
        while(self.condicionParada(iterac)>=0):
            lista_permit = self.pertenListaTabu(lista_tabu)    #Obtengo la lista de elementos que no son tabu
            lista_random = random.sample(lista_permit,2)    #Selecciona dos al azar de la lista de permitidos
            V1 = lista_random[0] #Estos dos elementos son los vertices al azar para el swapp
            V2 = lista_random[1]
            ADD = Tabu(V1, self.__tenureADD)   #Elijo mi primer elemento tabu para la proxima iteracion. Para un ADD 
            DROP = Tabu(V2, self.__tenureDROP) #Igual para un DROP
            
            Sol_Nueva = Sol_Actual.swapp(V1,V2)
            self.__soluciones.append(Sol_Nueva) #Cargo las nuevas soluciones
            if(Sol_Nueva.getCostoAsociado() < Sol_Optima.getCostoAsociado()):
                Sol_Optima = Sol_Nueva  #Actualizo la solucion optima
            
            self.decrementaTenure(lista_tabu)  #Decremento el tenure y elimino algunos elementos con tenure igual a 0
            lista_tabu.append(ADD)
            lista_tabu.append(DROP)
        #return self.__soluciones
                            
    def pertenListaTabu(self, lista_tabu: list):
        ListaVertices = self._G.getV
        ListaPermit = []
        for i in range(0, len(ListaVertices)):
            EP = ListaVertices[i]
            for j in range(0, len(lista_tabu)):
                ET = lista_tabu[j].getElemento()
                if(EP != ET):
                    ListaPermit.append(EP)
        return ListaPermit

    def decrementaTenure(self, lista_tabu: list):
        for i in range(0,len(lista_tabu)):
            lista_tabu[i].decrementaT()
            t = lista_tabu[i].getTenure()
            if(t<=0):
                lista_tabu.pop(i)

    def condicionParada(self, iter: int):
        return (iter-1)

#    def tabuSearch_ale(self):
#        solLocal = self.__soluciones[0]
#        N = solLocal.getGrado()
#        DROP = []
#        ADD = []
#        condicion = True #pensar en condicion
#        while condicion:
#            bandVertice = True
#            while (bandVertice):
#                v2 = solLocal.getV()[random.randint(0,M)]
#                v1 = solLocal.getV()[random.randint(0,M)]
#                solLocal = solLocal.swapVertice(solLocal.getV()[,])
#                bandVertice = ()


#[elementoTabu,tenureActual] #na era para llamarte, con llamada común, pero no importa, vamos por zoom, ahí mando el link
#    def tabuSearch():
        #listaTabu = [] esta lista tabu es como el drop?
        #ADD = []
        #DROP = []
#        pass

#    def tabuSearch_1():
        #add = []
#        pass

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

Solucion: 1->2->5->6->7->9->8->10->3->1
List: {1,2,3,4,5,6,7,8,9,10}
{8,3,1,4,2} -> ListaTabú

Solucion: 1->2->5->6->7->10->8->9->3->1
List: {1,2,3,4,5,6,7,8,9,10}
{3,1,4,2,9,10} -> ListaTabú

Solucion: 1->2->5->6->7->10->8->9->3->1
List: {(1,2),(2,5),(5,6),(6,7),(7,10),(10,8),(8,9),(9,3),(3,1)}
{3,1,4,2,9,10} -> ListaTabú '''

