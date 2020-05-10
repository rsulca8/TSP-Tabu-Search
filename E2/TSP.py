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
       print("Se cargo el archivo")
       self.__soluciones = []    #Lista de Grafos que corresponden a las soluciones
       self.__tenureADD = 10 #Mas adelante que se ingrese por ventana
       self.__tenureDROP = 9 #idem jaja
       self.__txt = open("rdo.txt", "w")
       self.__st = ""
       self.tabuSearch()

    def escribe(self, st):
        self.__st = self.__st + st+"\n"
    
    def imprime(self):
        self.__txt.write(self.__st)
        self.__txt.close()
  
    def obtenerSolucionsVecinoCercano(self):
        copiaG = copy.deepcopy(self._G)
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

        return visitados
    
    def vecinoMasCercano(self, matrizDist: list, pos: int, visitados: list):
        masCercano = matrizDist[pos][0]
        for i in range(1, len(matrizDist)-1):
            if(matrizDist[pos][i]<masCercano and i not in visitados):
                masCercano = i
        return masCercano
    
    def obtenerSolucionsVecinoCercano_prueba(self):
        copiaG = copy.deepcopy(self._G)
        inicio = self._G.getVerticeInicio()
        matrizDist = self._G.getMatriz()

        recorrido = []
        visitados = []
        
        recorrido.append(inicio)
        visitados.append(0)
        for i in range(0,len(matrizDist)-1):
            masCercano = self.vecinoMasCercano(matrizDist,i, visitados)
            recorrido.append(Vertice(masCercano))
            visitados.append(masCercano)

        return recorrido
        
    def solucionAlAzar(self):
        inicio = self._G.getVerticeInicio()
        indices_azar = random.sample( range(2,len(self._G.getV())+1), len(self._G.getV())-1)
        alAzar = []
        alAzar.append(inicio)
        for i in indices_azar:
            alAzar.append(i)

        return alAzar

    
    def tabuSearch(self):
        lista_tabu = []     #Tiene objetos de la clase Tabu
        lista_permit = []   #Tiene objetos del tipo vertice
        salida = ""
        soluciones = []
        g1 = self._G.copy()
        solucionVecinoCercano = self.obtenerSolucionsVecinoCercano() #Obtiene un vector de vértices con el tour del vecino más cercano
        g1.cargarDesdeSecuenciaDeVertices(solucionVecinoCercano) #Carga el recorrido a la solución
        self.__soluciones.append(g1) #Agregar solución inicial
        self.escribe("############### GRAFO CARGADO #################")
        self.escribe(str(self._G))
        self.escribe("################ SOLUCION INICIAL #################")
        self.escribe("Vertices:        " + str(g1.getV()))
        self.escribe("Aristas:         " + str(g1.getA()))
        self.escribe("Costo asociado:  " + str(g1.getCostoAsociado()))
        Sol_Actual = self.__soluciones[len(self.__soluciones)-1] #Primera solución
        Sol_Optima = Sol_Actual #Solo para el primer caso 
        iterac = 100
        soluciones.append(Sol_Optima)
        while(iterac>=0):
            lista_permit = self.pertenListaTabu(lista_tabu)    #Obtengo la lista de elementos que no son tabu
            ind_random = random.sample(range(0,len(lista_permit)),2)    #Selecciona dos al azar de la lista de permitidos 
            V1 = lista_permit[ind_random[0]] #Estos dos elementos son los vertices al azar para el swapp
            V2 = lista_permit[ind_random[1]]
            
            ADD = Tabu(V1, self.__tenureADD)   #Elijo mi primer elemento tabu para la proxima iteracion. Para un ADD 
            DROP = Tabu(V2, self.__tenureDROP) #Igual para un DROP
            
            Sol_Nueva = Sol_Actual.swapp(V1,V2)
            self.escribe("################################ " + str(iterac) + " ####################################")
            self.escribe("Vertices:        " + str(Sol_Nueva.getV()))
            self.escribe("Aristas:         " + str(Sol_Nueva.getA()))
            self.escribe("Costo asociado:  " + str(Sol_Nueva.getCostoAsociado())) 
            
            self.__soluciones.append(Sol_Nueva) #Cargo las nuevas soluciones
            if(Sol_Nueva.getCostoAsociado() < Sol_Optima.getCostoAsociado()):
                Sol_Optima = Sol_Nueva  #Actualizo la solucion optima
                
            soluciones.append(Sol_Nueva)
            
            self.escribe("-+-+-+-+-+-+-+-+-+ Lista TABÚ -+-+-+-+-+-+-+-+-+")
            self.decrementaTenure(lista_tabu)  #Decremento el tenure y elimino algunos elementos con tenure igual a 0
            lista_tabu.append(ADD)
            lista_tabu.append(DROP)
            self.escribe("Lista Tabu: "+ str(lista_tabu))
            lista_permit = []
            iterac -= 1
        
        self.escribe("################################ Solucion Optima ####################################")
        self.escribe("Vertices:        " + str(Sol_Optima.getV()))
        self.escribe("Aristas:         " + str(Sol_Optima.getA()))
        self.escribe("Costo asociado:  " + str(Sol_Optima.getCostoAsociado()))
        
    ###NO SIRVE :S 
    #Soluciones [1,2,3,,5,6]
    def mejoresSoluciones(self, cantidad, soluciones):
        mejores = []
        for i in soluciones:
            if(len(mejores)<=cantidad):
                mejores.append(i)
            else:
                for j in mejores:
                    #print(str(i.getCostoAsociado) +" < " + str(j.getCostoAsociado))
                    print(i.getCostoAsociado())
                    print(j.getCostoAsociado())
                    if (i < j):
                        mejores.append(j)
        return mejores

        


    #def solMasLejana(self):#ale

    def pertenListaTabu(self, lista_tabu: list):
        ListaPermit = []
        CopyVert = copy.deepcopy(self._G.getV())
        cantVert = len(copy.deepcopy(self._G.getV()))
        if(len(lista_tabu) == 0):
            ListaPermit = CopyVert
        else:
            for i in range(0, cantVert):
                EP = CopyVert[i]      #EP: Elemento Permitido
                j = 0
                cond = True
                while(j < len(lista_tabu) and cond):
                    ET = lista_tabu[j].getElemento()    #ET: Elemento Tabu
                    if(EP == ET):
                        cond = False
                    j+=1
                if(cond):
                    ListaPermit.append(EP)
        
        ListaPermit.pop(0) #Eliminamos el vertice inicial
        #print("Lista Permitidos: "+str(ListaPermit))
        
        return ListaPermit

    def decrementaTenure(self, lista_tabu: list):
        for elemTabu in lista_tabu:
            elemTabu.decrementaT()
            t = elemTabu.getTenure()
            if(t==0):
                lista_tabu.remove(elemTabu)
    #def condicionParada(self, iter: int):
    #    return (iter-1)

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

