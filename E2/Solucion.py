from Grafo import Grafo 
from Vertice import Vertice 
from Arista import Arista
import copy
import random
from time import time
class Solucion(Grafo):
    def __init__(self, secuencia: list, M):
        self.__V = []
        self.__A = []
        super(Solucion, self).__init__(M)
        self.__costoAsociado = 0
        if(len(secuencia) == 0 ):
            self.__V = [self.getVerticeInicio()]
            self.__A = []
        else:
            self.__A = []
            self.cargarDesdeSecuenciaDeVertices(secuencia)

    def __getitem__(self, key):
        return self.__V[key]

    def __str__(self):
        return "Vértices de la solución: " + str(self.__V) +"\nAristas de la solución: "+ str(self.getA()) + " \nCosto Asociado: " + str(self.__costoAsociado)

    def __repr__(self):
        return str(self.getV())

    def setCostoAsociado(self, costo):
        self.__costoAsociado = costo
    
    def getCostoAsociado(self):
        return self.__costoAsociado

    def __eq__(self, otro):
        return (self.__costoAsociado == otro.__costoAsociado)

    def __ne__(self, otro):
        return (self.__costoAsociado != otro.__costoAsociado)
    
    def __gt__(self, otro):
        return self.__costoAsociado > otro.__costoAsociado
    
    def __lt__(self, otro):
        return self.__costoAsociado < otro.__costoAsociado
    def __ge__(self, otro):
        return self.__costoAsociado >= otro.__costoAsociado

    def __le__(self, otro):
        return self.__costoAsociado <= otro.__costoAsociado

    def __len__(self):
        return len(self.__V)

    def copy(self):
        S = Solucion(copy.deepcopy(self.getV()),self.getMatriz())
        return S

    def setA(self, A):
        self.__A = A

    def setV(self, V):
        self.__V = V

    def getA(self):
        return self.__A

    def getV(self):
        return self.__V


    def cargarDesdeSecuenciaDeVertices(self,seq:list):
        self.setV(seq)
        self.__A = []
        rV = [] #Vértices de la matriz ordenados, para obtener la referencia en la matriz de distnacias
        costo = 0
        for j in range(0,len(self.getMatriz())):
            rV.append(Vertice(j+1))
        if(len(seq) == 0):
            self.__V = rV
        #rV = [ V(1),V(2),V(3),V(4),V(5) ]
        #(1,2,4)(2,5,7)(5,3,6)(3,4,9)(4,1,5)
        for i in range(0,len(seq)-1):
            dist = self.getMatriz()[rV.index(seq[i])][rV.index(seq[i+1])] #Referencias en la matriz
            self.getA().append(Arista(seq[i], seq[i+1], dist))
            costo+= dist
        self.setCostoAsociado(costo + self.getMatriz()[rV.index(seq[len(seq)-1])][rV.index(seq[0])])

    def swap(self, v1, v2):
        VA1 = self.getV().index(v1)
        VA2 = self.getV().index(v2)
        self.getV()[VA1]=v2
        self.getV()[VA2]=v1
        self.cargarDesdeSecuenciaDeVertices(self.getV())
        

        
    def solucionVecinoCercano(self):
        inicio = self.__V[0]
        matrizDist = self.getMatriz()

        recorrido = []
        visitados = []       
        recorrido.append(inicio)    #Agrego el vertice inicial
        visitados.append(0)     #Agrego el vertice inicial
        masCercano=0
        for i in range(0,len(matrizDist)-1):
            masCercano = self.__vecinoMasCercano(matrizDist,masCercano, visitados) #obtiene la posicion dela matriz del vecino mas cercano
            recorrido.append(Vertice(masCercano+1))
            visitados.append(masCercano)
            i
        self.cargarDesdeSecuenciaDeVertices(recorrido)

    def __vecinoMasCercano(self, matrizDist: list, pos: int, visitados: list):
        masCercano = matrizDist[pos][pos]
        indMasCercano = 0
    
        for i in range(0, len(matrizDist)):
            costo = matrizDist[pos][i]
            if(costo<masCercano and i not in visitados):
                masCercano = costo
                indMasCercano = i
        
        return indMasCercano 
    
    def solucionAlAzar(self):
        inicio = self.getVerticeInicio()
        indices_azar = random.sample( range(2,len(self.getV())+1), len(self.getV())-1)
        alAzar = []
        alAzar.append(inicio)
        for i in indices_azar:
            alAzar.append(Vertice(i))
        self.cargarDesdeSecuenciaDeVertices(alAzar)


                