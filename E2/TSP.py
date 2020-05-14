from Vertice import Vertice
from Arista import Arista
from Grafo import Grafo
from Tabu import Tabu
from Solucion import Solucion
import random 
import sys
import re
import math 
import copy
from clsTxt import clsTxt
from time import time

class TSP:
    def __init__(self, M: list, nombreArchivo, importFile):
        self._G = Grafo(M)   #Grafo original
        print("Se cargo el archivo")
        self.__soluciones = []   #Lista de Grafos que corresponden a las soluciones
        self.__Sol_Optima = []
        self.__tenureADD = 7    #Mas adelante que se ingrese por ventana
        self.__tenureDROP = 6   #idem jaja
        self.__txt = clsTxt(str(nombreArchivo))
        self.__importFile = importFile
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
    
    #Para obtener el tabu search granular
    def vecinoMasCercanoV2(self, matrizDist: list, pos: int, permitidos: list):
        masCercano = matrizDist[pos][pos]
        indMasCercano = 0

        for ind in permitidos:
            costo = matrizDist[pos][ind-1]
            if(costo<masCercano):
                masCercano = costo
                indMasCercano = permitidos.index(ind)        
        
        return indMasCercano 

    #Para     
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
            ind = self.vecinoMasCercanoV2(matrizDist,indicesRandom[i],permitidos)
            indices.append(ind)
            indices_permitidos.pop(ind)
        
        return indices

    #Te devuelve una nueva solucion inicial cuando se estanca
    def pathRelinking(self, solInicial, solGuia):
        i=0
        band = True
        elemInicial = None
        elemGuia = None
        while (i < len(solGuia) and band):
            if(not(solInicial[i]==solGuia[i])):
                elemInicial = solInicial[i]      #[1,4,5,3,2]       [1,4,3,2,5] y elemVertice=5
                elemGuia = solGuia[i]            #[1,4,3,3,2]       [1,4,3,2,5]
                band=False
                print("ElemInicial: "+str(elemInicial))
                print("ElemGuia   : "+str(elemGuia))
            i+=1

        print("SolInicial1: "+str(solInicial))
        if(band):
            print("Al azar")
            VerticesAlAzar = self.solucionAlAzar()
            solInicial.cargarDesdeSecuenciaDeVertices(VerticesAlAzar)
        else:
            print("Path relinking!")
            solInicial.swap(elemInicial, elemGuia)        
        print("SolInicial2: "+str(solInicial))

        return solInicial
    
    def tabuSearch(self):
        lista_tabu = []     #Tiene objetos de la clase Tabu
        lista_permit = []   #Tiene objetos del tipo vertice
        Sol_Actual = []

        #A partir del vecino mas cercano
        solucionVecinoCercano = Solucion([],self._G.getMatriz())
        solucionVecinoCercano.solucionVecinoCercano() #Obtiene un vector de vértices con el tour del vecino más cercano
        self.__soluciones.append(solucionVecinoCercano) #Agregar solución inicial
        
        print("Comenzando Tabu Search")
        self.__txt.escribir("############### GRAFO CARGADO #################")
        self.__txt.escribir(str(self._G))
        self.__txt.escribir("################ SOLUCION INICIAL #################")
        self.__txt.escribir(str(solucionVecinoCercano))

        Sol_Actual = self.__soluciones[len(self.__soluciones)-1] #Primera solución
        self.__Sol_Optima = Sol_Actual.copy() #Ultima solucion optima obtenida
        Sol_Inicial = Sol_Actual.copy() #Solucion Inicial, utilizada para el path Relinking
        Sol_Nueva = Sol_Actual.copy()  #Solucion Nueva obtenida en cada iteracion
        iterac = 1
        maxIteraciones = 5000
        maxmantenerSolucion = 1000
        condNoMejora=False  #Si el algoritmo se estanca cambia a True y empieza a utilizar las soluciones iniciales del path relinking
        subIteracion = 0
        
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
                
                #Path relinkin luego de determinada cantIteraciones en que no hay mejoria
                if(subIteracion == maxmantenerSolucion):
                    lista_tabu = []
                    subIteracion = 0
                    
                    print("Nueva solución inicial con path Relinking o al azar")
                    condNoMejora =True
                    if(Sol_Inicial != self.__Sol_Optima):
                        Sol_Inicial = self.pathRelinking(Sol_Inicial,self.__Sol_Optima)
                    #print("Sol_Inicial_1: "+str(Sol_Inicial.getV()))

                ###########Tabu search al azar con ADD's y DROP's al azar#############
                #ind_random = random.sample(range(0,len(lista_permit)),nroIntercambios) #Selecciona al azar de la lista de permitidos 

                ###########Con los vecinos cercanos (tabu search granular)#############
                ind_random = random.sample(range(0,len(lista_permit)),int(nroIntercambios/2))
                ind_random = self.verticesMasCercanos(ind_random, lista_permit)
                
                #Crea los elementos ADD y DROP
                for i in range(0,len(ind_random)):
                    if(i%2==0): #Los pares para ADD y los impares para DROP
                        ADD.append(Tabu(lista_permit[ind_random[i]], self.__tenureADD))
                    else:
                        DROP.append(Tabu(lista_permit[ind_random[i]], self.__tenureDROP))

                #Realiza el intercambio de los vertices seleccionados
                #se decide como será la solución nueva
                if(subIteracion==0 and iterac!=1):
                    Sol_Nueva = Sol_Inicial.copy()
                else:
                    Sol_Nueva = Sol_Actual.copy()
                             
                #swap solución nueva
                #print("Sol nueva antes " + str(Sol_Nueva.getV()) + " Costo "+ str(Sol_Nueva.getCostoAsociado()))
                for i in range(0,len(ADD)):
                    Sol_Nueva.swap(ADD[i].getElemento(), DROP[i].getElemento())

                #self.__txt.escribir("Sol optima "+ str(self.__Sol_Optima.getV()) + " Costo "+str(self.__Sol_Optima.getCostoAsociado()))
                #self.__txt.escribir"Sol nueva despues " + str(Sol_Nueva.getV()) + " Costo "+ str(Sol_Nueva.getCostoAsociado()))
                if(Sol_Nueva < self.__Sol_Optima):
                    self.__Sol_Optima = Sol_Nueva.copy()  #Actualizo la solucion optima
                    condOptim = True     
                    print("Esta solución duró " + str(subIteracion)+" iteraciones")
                    subIteracion=0 
                    self.__soluciones.append(Sol_Actual) #Cargo las nuevas soluciones
                elif(condNoMejora):
                    #Significa que se aplico el pathRelinking y la Sol_Actual debe ser la ultima obtenida
                    #print("elif: "+str(Sol_Actual.getV()))
                    Sol_Actual = Sol_Nueva
                else:
                    #No se estanco, seguimos aplicando tabu search con la ultima solucion Optima
                    #print("else: "+str(Sol_Actual.getV()))
                    Sol_Actual = self.__Sol_Optima
                #print("SolActual Despue del swap: "+str(Sol_Actual.getV()))
                
                #print("Inicial: "+str(Sol_Inicial.getV()))
                #print("Actual:  "+str(Sol_Actual.getV()))
                #print("Optima : "+str(self.__Sol_Optima.getV()))
                #Solo en caso de haber mejoría, cargo todo en un archivo txt
                self.__txt.escribir("################################ " + str(iterac) + " ####################################")
                self.__txt.escribir(str(Sol_Nueva))
                condOptim = False 
            self.decrementaTenure(lista_tabu)  #Decremento el tenure y elimino algunos elementos con tenure igual a 0
            lista_tabu.extend(ADD)  
            lista_tabu.extend(DROP)  
        
            self.__txt.escribir("-+-+-+-+-+-+-+-+-+ Lista TABÚ -+-+-+-+-+-+-+-+-+")
            self.__txt.escribir("Lista Tabu: "+ str(lista_tabu))
            condOptim = False
            
            iterac += 1
            subIteracion += 1
        nroIntercambios = 6
        
        self.__txt.escribir("\n################################ Solucion Optima ####################################")
        self.__txt.escribir(str(self.__Sol_Optima))
        
        tiempoFin = time()
        tiempoTotal = tiempoFin - tiempoIni
        self.__txt.escribir("\nNro Intercambios: " + str(nroIntercambios) + "           Maximas Iteraciones: "+str(maxIteraciones))
        self.__txt.escribir("Tenure ADD: " + str(self.__tenureADD) + "           Tenure DROP: "+str(self.__tenureDROP))
        self.__txt.escribir("Tiempo total: " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg")

        print("Termino!! :)")
        self.__txt.imprimir()
        print("Tiempo total: " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg")

    def mejoresSoluciones(self, cantidad, soluciones):
        mejores = []
        for i in soluciones:
            if(len(mejores)<=cantidad):
                mejores.append(i)
            else:
                for j in mejores:
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
