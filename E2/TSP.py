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
    def __init__(self, M: list, nombreArchivo, importFile):
        self._G = Grafo(M)   #Grafo original
        print("Se cargo el archivo")
        self.__soluciones = []   #Lista de Grafos que corresponden a las soluciones
        self.__tenureADD = int(len(M)*0.1)    #Mas adelante que se ingrese por ventana
        self.__tenureMaxADD = int(len(M)*0.15)
        self.__tenureDROP = int(len(M)*0.1)   #idem jaja
        self.__tenureMaxDROP = int(len(M)*0.15)
        self.__txt = clsTxt(str(nombreArchivo))
        self.__importFile = importFile
        self.tabuSearch()

    def vecinoMasCercano(self, matrizDist: list, pos: int, visitados: list):
        masCercano = matrizDist[pos][pos]
        indMasCercano = 0
    
        for i in range(0, len(matrizDist)):
            costo = matrizDist[pos][i]
            if(costo<masCercano and i not in visitados):
                masCercano = costo
                indMasCercano = i
        
        return indMasCercano 

    
    def solucionVecinosCercanos(self):
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
 
    # Para el Tabu Search Granular
    def vecinosMasCercanosTSG(self, indicesRandom: list, list_permit: list):
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

    def vecinoMasCercanoV2(self, matrizDist: list, pos: int, permitidos: list):
        masCercano = matrizDist[pos][pos]
        indMasCercano = 0

        for ind in permitidos:
            costo = matrizDist[pos][ind-1]
            if(costo<masCercano):
                masCercano = costo
                indMasCercano = permitidos.index(ind)        
        
        return indMasCercano 

    #Te devuelve una nueva solucion inicial cuando se estanca
    def pathRelinking(self, solInicial, solGuia):
        i=0
        band = True
        elemInicial = None
        elemGuia = None
        solInicial_1 = solInicial.copy()
        while (i < len(solGuia.getV()) and band):
            if(not(solInicial.getV()[i]==solGuia.getV()[i])):
                elemInicial = solInicial.getV()[i]
                elemGuia = solGuia.getV()[i]      
                band=False
                print("ElemInicial: "+str(elemInicial))
                print("ElemGuia   : "+str(elemGuia))
            i+=1

        if(band):
            print("Al azar")
            VerticesAlAzar = self.solucionAlAzar()
            solInicial_1.cargarDesdeSecuenciaDeVertices(VerticesAlAzar)
        else:
            print("Path relinking!")
            solInicial_1 = solInicial.swapp(elemInicial, elemGuia)
        
        return solInicial_1
    
    ####### Empezamos con Tabu Search #########
    def tabuSearch(self):
        lista_tabu = []     #Tiene objetos de la clase Tabu
        lista_permit = []   #Tiene objetos del tipo vertice      
        g1 = self._G.copyVacio()
        Sol_Actual = self._G.copyVacio()
        
        ########Partimos de una solucion al Azar#############
        #solucionAzar = self.solucionAlAzar()
        #g1.cargarDesdeSecuenciaDeVertices(solucionAzar)

        ########Partimos del vecino mas cercano###########
        vecinosCercanos = self.solucionVecinosCercanos() #Obtiene un vector de vértices
        g1.cargarDesdeSecuenciaDeVertices(vecinosCercanos) #Carga el recorrido a la solución
        self.__soluciones.append(g1) #Agregar solución inicial
        
        print("Comenzando Tabu Search")
        self.__txt.escribir("############### GRAFO CARGADO #################")
        self.__txt.escribir(str(self._G))
        self.__txt.escribir("################ SOLUCION INICIAL #################")
        self.__txt.escribir("Vertices:        " + str(g1.getV()))
        self.__txt.escribir("Aristas:         " + str(g1.getA()))
        self.__txt.escribir("Costo asociado:  " + str(g1.getCostoAsociado()))
        
        Sol_Actual = self.__soluciones[len(self.__soluciones)-1] #Primera solución
        Sol_Optima = copy.deepcopy(Sol_Actual) #Ultima solucion optima obtenida
        Sol_Inicial = copy.deepcopy(Sol_Actual) #Solucion Inicial, utilizada para el path Relinking
        Sol_Nueva = copy.deepcopy(Sol_Actual)   #Solucion Nueva obtenida en cada iteracion
        iterac = 1
        maxIteraciones = 10000
        maxmantenerSolucion = 10000  #Si no obtenemos nada mejor, consideramos un estancamiento
        subIteracion = 0
        condOptim = False   #En caso de que encontre uno mejor que el optimo lo guardo en el archivo txt
        condNoMejora=False  #Se estanco, aplico Path Relinking
        tiempoIni = time()
        tiempoMax = float(1*60)    #1 min
        while(time()-tiempoIni<=tiempoMax):
            lista_permit = self.pertenListaTabu(lista_tabu)    #Obtengo la lista de elementos que no son tabu
            ADD = []
            DROP = []
            nroIntercambios = 6 #Se vuelve a actualizar al final del while asi q si se cambia aqui. cambiar abajo

            #Verifico si hay vertices disponibles suficientes para el intercambio
            if(len(lista_permit)>=2):
                if(len(lista_permit)<nroIntercambios):
                    nroIntercambios=len(lista_permit)
                    if(nroIntercambios%2!=0):
                        nroIntercambios-=1                    
                #Path relinkin luego de determinada cantIteraciones en que no encuentro mejoria
                if(subIteracion == maxmantenerSolucion):
                    subIteracion = 0
                    print("Nueva solución inicial con path Relinking o al azar")
                    #print("Inicial:    "+str(Sol_Inicial.getV())+"  costo: "+str(Sol_Inicial.getCostoAsociado()))
                    #print("Actual:     "+str(Sol_Actual.getV())+"  costo: "+str(Sol_Actual.getCostoAsociado()))
                    #print("Optima:     "+str(Sol_Optima.getV())+"  costo: "+str(Sol_Optima.getCostoAsociado()))
                    Sol_Inicial = self.pathRelinking(Sol_Actual, Sol_Optima)
                    #print("Inicial2:   "+str(Sol_Inicial.getV())+"  costo: "+str(Sol_Inicial.getCostoAsociado()))
                    #print("Actual2:    "+str(Sol_Actual.getV())+"  costo: "+str(Sol_Actual.getCostoAsociado()))
                    #print("Optima2:    "+str(Sol_Optima.getV())+"  costo: "+str(Sol_Optima.getCostoAsociado()))
                    condNoMejora =True    
                
                ######### Tabu search al azar ############
                #ind_random = random.sample(range(0,len(lista_permit)),nroIntercambios) #Selecciona indices al azar de la lista de permitidos 
                
                ######### Tabu Search Granular ############
                ind_random = random.sample(range(0,len(lista_permit)),int(nroIntercambios/2)) #Con los vecinos mas cercanos
                ind_random = self.vecinosMasCercanosTSG(ind_random, lista_permit)
                
                #Crea los elementos ADD y DROP
                for i in range(0,len(ind_random)):
                    if(i%2==0): #Los pares para ADD y los impares para DROP
                        ADD.append(Tabu(lista_permit[ind_random[i]], self.__tenureADD))
                    else:
                        DROP.append(Tabu(lista_permit[ind_random[i]], self.__tenureDROP))

                #Realiza el intercambio de los vertices seleccionados
                for i in range(0,len(ADD)):
                    if(subIteracion==0 and iterac!=1):
                        Sol_Nueva = Sol_Inicial.swapp(ADD[i].getElemento(), DROP[i].getElemento())
                    else:
                        Sol_Nueva = Sol_Actual.swapp(ADD[i].getElemento(), DROP[i].getElemento())

                #Si obtengo una nueva solucion optima
                if(Sol_Nueva < Sol_Optima):
                    Sol_Optima = Sol_Nueva  #Actualizo la solucion optima
                    condOptim = True     
                    print("Esta solución duró " + str(subIteracion)+" iteraciones")
                    subIteracion=0
                    self.__soluciones.append(Sol_Actual) #Cargo las soluciones optimas
                    for i in range(0,len(ADD)):
                        ADD[i].setTenure(self.__tenureMaxADD)
                        DROP[i].setTenure(self.__tenureMaxDROP)
                elif(condNoMejora):
                    #Si hubo un estancamiento, utilizo la ultima solucion obtenida
                    Sol_Actual = Sol_Nueva
                else:
                    #Si no hubo un estancamiento, utilizo la ultima solucion optima obtenida, y sigo aplicando Tabu Search
                    Sol_Actual = Sol_Optima
                
                #Si encontramos un optima local, lo guardamos en el txt
                if(condOptim):
                    self.__txt.escribir("################################ " + str(iterac) + " ####################################")
                    self.__txt.escribir("Vertices:        " + str(Sol_Nueva.getV()))
                    self.__txt.escribir("Aristas:         " + str(Sol_Nueva.getA()))
                    self.__txt.escribir("Costo asociado:  " + str(Sol_Nueva.getCostoAsociado()))
                    self.__txt.escribir("-+-+-+-+-+-+-+-+-+-+-+-+ Lista TABÚ +-+-+-+-+-+-+-+-+-+-+-+-+")
                    self.__txt.escribir("Lista Tabu: "+ str(lista_tabu))
                    condOptim = False 
            
            self.decrementaTenure(lista_tabu)   #Decremento el tenure y elimino algunos elementos con tenure igual a 0
            lista_tabu.extend(ADD)              #Agrego los nuevos vertices a la lista tabu
            lista_tabu.extend(DROP)  
            lista_permit = []
            iterac += 1
            subIteracion += 1

        #Fin del while. Imprimo la solucion optima y algunos atributos
        nroIntercambios = 6
        tiempoFin = time()
        tiempoTotal = tiempoFin - tiempoIni
        self.__txt.escribir("\n################################ Solucion Optima ####################################")
        self.__txt.escribir("Vertices:        " + str(Sol_Optima.getV()))
        self.__txt.escribir("Aristas:         " + str(Sol_Optima.getA()))
        self.__txt.escribir("Costo asociado:  " + str(Sol_Optima.getCostoAsociado()))
        self.__txt.escribir("\nNro Intercambios: " + str(nroIntercambios) + "           Maximas Iteraciones: "+str(maxIteraciones))
        self.__txt.escribir("Tenure ADD: " + str(self.__tenureADD) + "           Tenure DROP: "+str(self.__tenureDROP))
        self.__txt.escribir("Tiempo total: " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg")
        self.__txt.imprimir()
        
        print("Termino!! :)")
        print("Tiempo total: " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg")

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
        
        ListaPermit.pop(0) #Eliminamos el vertice inicial, el 1
        
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
