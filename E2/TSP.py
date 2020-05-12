from Vertice import Vertice
from Arista import Arista
from Grafo import Grafo
from Tabu import Tabu
import random 
import sys
import re
import math 
import copy
from clsTxt import clsTxt
from time import time

class TSP:
    def __init__(self, M: list, nombreArchivo):
       self._G = Grafo(M)   #Grafo original
       print("Se cargo el archivo")
       self.__soluciones = []   #Lista de Grafos que corresponden a las soluciones
       self.__tenureADD = 7    #Mas adelante que se ingrese por ventana
       self.__tenureDROP = 6   #idem jaja
       self.__txt = clsTxt(str(nombreArchivo))
       self.tabuSearch()
  
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
        masCercano = matrizDist[pos][pos]
        indMasCercano = 0
    
        for i in range(0, len(matrizDist)):
            costo = matrizDist[pos][i]
            if(costo<masCercano and i not in visitados):
                masCercano = costo
                indMasCercano = i
        
        return indMasCercano 

    
    def obtenerSolucionsVecinoCercano_V2(self):
        inicio = self._G.getV()[0]
        matrizDist = self._G.getMatriz()

        recorrido = []
        visitados = []
        
        recorrido.append(inicio)    #Agrego el vertice inicial
        visitados.append(0)     #Agrego el vertice inicial
        masCercano=0
        print("VECINO MÁS CEERCANO")
        for i in range(0,len(matrizDist)-1):
            masCercano = self.vecinoMasCercano(matrizDist,masCercano, visitados) #obtiene la posicion dela matriz del vecino mas cercano
            recorrido.append(Vertice(masCercano+1))
            visitados.append(masCercano)
            i

        return recorrido

    def solucionAlAzar(self):
        inicio = self._G.getVerticeInicio()
        indices_azar = random.sample( range(2,len(self._G.getV())+1), len(self._G.getV())-1)
        alAzar = []
        alAzar.append(inicio)
        for i in indices_azar:
            alAzar.append(Vertice(i))

        return alAzar

    def solMasLejana(self, caminos:list, solLocal):
        pass
        #dist = len(solLocal) #distancia inicial es la cantidad de aristas
        #listaDistancias = []
        # for i in caminos: #recorre la lista de todos los grafos
            #seqV = i.getV()
            #for i in range(len(seqV)-2): #chequea si hay aristas coincidentes
            #    dist = (dist - 1) if (seqV[seqV.index(solLocal[i])+1]==solLocal[i+1]): #si las aristas coinciden se disminuye la distancia
            #dist = (dist - 1) if (seqV[len(seqV)-1]==solLocal[len(solLocal)-1]):
            #listaDistancias.append([dist, i])
        #return max (listaDistancias)[1] #retorna un grafo
    
    def verticesMasCercanos(self, indicesRandom: list, list_permit: list):
        indices = []    #Nueva lista de indices permitidos
        indices_permitidos = [] #Indices permitidos
        matrizDist = self._G.getMatriz()
        
        for x in list_permit:
            indices_permitidos.append(x.getValue()) #Se carga con los indices que ocupan en el grafo. Lo mismo que en lista_permit solo que
            #ahora son indices enteros y no vertices
        
        for i in range(0, len(indicesRandom)):
            indices.append(indicesRandom[i])
            permitidos = list(set(indices_permitidos)-set(indicesRandom))
            ind = self.vecinoMasCercanoV2(matrizDist,i,permitidos)
            indices.append(ind)
            indices_permitidos.pop(ind)
        
        return indices

    #Es identica al de arriba solo difiere en el if (.... i in permitidos)
    def vecinoMasCercanoV2(self, matrizDist: list, pos: int, permitidos: list):
        masCercano = matrizDist[pos][pos]
        indMasCercano = 0

        for ind in permitidos:
            costo = matrizDist[pos][ind-1]
            if(costo<masCercano):
                masCercano = costo
                indMasCercano = permitidos.index(ind)        
        
        return indMasCercano 

    def tabuSearch(self):
        lista_tabu = []     #Tiene objetos de la clase Tabu
        lista_permit = []   #Tiene objetos del tipo vertice
        soluciones = []
        g1 = self._G.copy()
        #solucionAzar = self.solucionAlAzar()
        #g1.cargarDesdeSecuenciaDeVertices(solucionAzar)

        solucionVecinoCercano = self.obtenerSolucionsVecinoCercano_V2() #Obtiene un vector de vértices con el tour del vecino más cercano
        g1.cargarDesdeSecuenciaDeVertices(solucionVecinoCercano) #Carga el recorrido a la solución
        print("Comenzando Tabu Search")
        self.__soluciones.append(g1) #Agregar solución inicial
        self.__txt.escribir("############### GRAFO CARGADO #################")
        self.__txt.escribir(str(self._G))
        self.__txt.escribir("################ SOLUCION INICIAL #################")
        self.__txt.escribir("Vertices:        " + str(g1.getV()))
        self.__txt.escribir("Aristas:         " + str(g1.getA()))
        self.__txt.escribir("Costo asociado:  " + str(g1.getCostoAsociado()))
        Sol_Actual = self.__soluciones[len(self.__soluciones)-1] #Primera solución
        Sol_Optima = Sol_Actual #Solo para el primer caso 
        iterac = 1
        maxIteraciones = 40000
        soluciones.append(Sol_Optima)
        condOptim = False   #En caso de que encontre uno mejor que el optimo lo imprimo
        tiempoIni = time()
        while(iterac <= maxIteraciones):
            lista_permit = self.pertenListaTabu(lista_tabu)    #Obtengo la lista de elementos que no son tabu
            ADD = []
            DROP = []
            nroIntercambios = 6 #Se vuelve a actualizar al final del while asi q si se cambia aqui. cambiar abajo
        
            if(len(lista_permit)>=2):
                if(len(lista_permit)<nroIntercambios):
                    nroIntercambios=len(lista_permit)
                    if(nroIntercambios%2!=0):
                        nroIntercambios-=1
                
                #Al azar
                ind_random = random.sample(range(0,len(lista_permit)),nroIntercambios) #Selecciona al azar de la lista de permitidos 
                
                #Al azar con los vecinos mas cercanos
                #ind_random = random.sample(range(0,len(lista_permit)),int(nroIntercambios/2)) #Con los vecinos mas cercanos
                #ind_random = self.verticesMasCercanos(ind_random, lista_permit)
                
                #Crea los elementos ADD y DROP
                for i in range(0,len(ind_random)):
                    if(i%2==0): #Los pares para ADD y los impares para DROP
                        ADD.append(Tabu(lista_permit[ind_random[i]], self.__tenureADD))
                    else:
                        DROP.append(Tabu(lista_permit[ind_random[i]], self.__tenureDROP))
                    
                #Realiza el intercambio de los vertices seleccionados
                for i in range(0,len(ADD)):
                    Sol_Nueva = Sol_Optima.swapp(ADD[i].getElemento(), DROP[i].getElemento())
                
                self.__soluciones.append(Sol_Nueva) #Cargo las nuevas soluciones
                if(Sol_Nueva.getCostoAsociado() < Sol_Optima.getCostoAsociado()):
                    Sol_Optima = Sol_Nueva  #Actualizo la solucion optima
                    condOptim = True      
                
                if(iterac%100 == 0 or condOptim):
                    self.__txt.escribir("################################ " + str(iterac) + " ####################################")
                    self.__txt.escribir("Vertices:        " + str(Sol_Nueva.getV()))
                    self.__txt.escribir("Aristas:         " + str(Sol_Nueva.getA()))
                    self.__txt.escribir("Costo asociado:  " + str(Sol_Nueva.getCostoAsociado()))
                    condOptim = False 
                    
                soluciones.append(Sol_Nueva) #Agrego mi solucion obtenida al vecindario de soluciones
            self.decrementaTenure(lista_tabu)  #Decremento el tenure y elimino algunos elementos con tenure igual a 0
            lista_tabu.extend(ADD)  
            lista_tabu.extend(DROP)  
            
            if(iterac%100 == 0 or condOptim):   
                self.__txt.escribir("-+-+-+-+-+-+-+-+-+ Lista TABÚ -+-+-+-+-+-+-+-+-+")
                self.__txt.escribir("Lista Tabu: "+ str(lista_tabu))
                condOptim = False
            
            lista_permit = []
            iterac += 1
            
        nroIntercambios = 6
        self.__txt.escribir("\n################################ Solucion Optima ####################################")
        self.__txt.escribir("Vertices:        " + str(Sol_Optima.getV()))
        self.__txt.escribir("Aristas:         " + str(Sol_Optima.getA()))
        self.__txt.escribir("Costo asociado:  " + str(Sol_Optima.getCostoAsociado()))
        
        tiempoFin = time()
        tiempoTotal = tiempoFin - tiempoIni
        self.__txt.escribir("\nNro Intercambios: " + str(nroIntercambios) + "           Maximas Iteraciones: "+str(maxIteraciones))
        self.__txt.escribir("Tenure ADD: " + str(self.__tenureADD) + "           Tenure DROP: "+str(self.__tenureDROP))
        self.__txt.escribir("Tiempo total: " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg")
        print("Termino!! :D")
        self.__txt.imprimir()
        print("Tiempo total: " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg")
        

    #def 
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
        i=0
        while (i <len(lista_tabu)):
            elemTabu=lista_tabu[i]
            elemTabu.decrementaT()
            if(elemTabu.getTenure()<=0):
                lista_tabu.pop(i)
                i-=1
            i+=1

    #def decrementaTenure(self, lista_tabu: list):


    #def condicionParada(self, iter: int):
    #    return (iter-1)


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


