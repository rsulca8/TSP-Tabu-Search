from Vertice import Vertice
from Arista import Arista
from Grafo import Grafo
from Solucion import Solucion
from Tabu import Tabu
from Ingreso import Ingreso
import random
import sys
import re
import math
import copy
from clsTxt import clsTxt
from time import time
from multiprocessing import Pool, Lock, Manager, Process
import contextlib

class TSP:
    def __init__(self,
    nombreArchivo, tenureADD, tenureMaxADD, tenureDROP, tenureMaxDROP,iteraciones,maxsubiteraciones,tiempo, intercambios,solucionInicial):
        M =self.cargarDesdeEUC_2D(nombreArchivo)
        self._G = Grafo(M)   #Grafo original
        #print("Se cargo el archivo")
        self.__soluciones = []   #Lista de Grafos que corresponden a las soluciones
        if(tenureMaxADD != 0):
            self.__tenureMaxADD =  int(tenureMaxADD) #
        else:
            self.__tenureMaxADD= int(len(M)*0.15)

        if(tenureMaxDROP != 0):
            self.__tenureMaxDROP =  int(tenureMaxDROP) #
        else:
            self.__tenureMaxDROP = int(len(M)*0.15)

        if(tenureADD != 0):
            self.__tenureADD =  int(tenureADD) #
        else:
            self.__tenureADD = int(len(M)*0.10)

        if(tenureDROP != 0):
            self.__tenureDROP =  int(tenureDROP) #
        else:
            self.__tenureDROP= int(len(M)*0.10)

        if(iteraciones != 0):
            self.__maxIteraciones =  int(iteraciones)
        else:
            self.__maxIteraciones = 1000

        if(maxsubiteraciones != 0):
            self.__maxSubiteraciones =  int(maxsubiteraciones)       #
        else:
            self.__maxSubiteraciones = int(self.__maxIteraciones*0.90)

        if(intercambios != 0):
            self.__nroIntercambios =  int(intercambios)  #corresponde al nro de vertices los intercambios. 1intercambio => 2 vertices
        else:
            self.__nroIntercambios = 5

        if(tiempo != 0):
            self.__tiempoMaxEjec = float(tiempo) #Ejecuta el tiempo ingresado
        else:
            self.__tiempoMaxEjec = 5 #Ejecuta el tiempo ingresado
        if(tiempo != 0):
            self.__tiempoMaxEjec = float(tiempo) #Ejecuta el tiempo ingresado
        else:
            self.__tiempoMaxEjec = 5 #Ejecuta el tiempo ingresado

        self.__soluciones = []   #Lista de Grafos que corresponden a las soluciones
        #self.__nroIntercambios=nroIntercambios*2
        #self.__opt=opt
        self.__txt = clsTxt(str(nombreArchivo))

        self.__frecMatriz = []
        for i in range(0, len(self._G.getMatriz())):
            fila = []
            for j in range(0, len(self._G.getMatriz())):
                fila.append(0)
                j
            self.__frecMatriz.append(fila)
            i

        if(solucionInicial == 0):  #Solución Vecino cercano -> 0           Solución al Azar -> 1
            self.__solInicial = self.solucionVecinosCercanos()
        else:
            self.__solInicial = self.solucionAlAzar()

    def cargarDesdeEUC_2D(self,pathArchivo):
        archivo = open(pathArchivo,"r")
        lineas = archivo.readlines()
        #Busco la posiciones de..
        indSeccionCoord = lineas.index("NODE_COORD_SECTION\n")
        lineaEOF = lineas.index("EOF\n")

        #Lista donde irán las coordenadas (vertice, x, y)
        coordenadas = []
        #Separa las coordenadas en una matriz, es una lista de listas (vertice, coordA, coordB)
        for i in range(indSeccionCoord+1, lineaEOF):
            textoLinea = lineas[i]
            textoLinea = re.sub("\n", "", textoLinea) #Elimina los saltos de línea
            splitLinea = textoLinea.split(" ") #Divide la línea por " "
            coordenadas.append([splitLinea[0],splitLinea[1],splitLinea[2]]) #[[v1,x1,y1], [v2,x2,y2], ...]

        matriz = []
        #Arma la matriz de distancias. Calculo la distancia euclidea
        for coordRow in coordenadas:
            fila = []
            for coordCol in coordenadas:
                x1 = float(coordRow[1])
                y1 = float(coordRow[2])
                x2 = float(coordCol[1])
                y2 = float(coordCol[2])
                dist = self.distancia(x1,y1,x2,y2)

                #Para el primer caso. Calculando la distancia euclidea entre si mismo da 0
                if(dist == 0):
                    dist = 999999999999 #El modelo no debería tener en cuenta a las diagonal, pero por las dudas
                fila.append(dist)

            #print("Fila: "+str(fila))
            matriz.append(fila)
        return  matriz


    def distancia(self, x1,y1,x2,y2):
        return round(math.sqrt((x1-x2)**2+(y1-y2)**2),2)

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
    def vecinosMasCercanosTSG(self, indicesRandom: list, lista_permitidos: list, recorrido: list):
        indices = []                #Indices de la lista de permitidos para hacer el swapp
        valores_permitidos = []     #Lista de permitidos como enteros y no como vertices
        valores_recorrido = []              #La solucion como una lista de enteros
        matrizDist = self._G.getMatriz()

        for x in lista_permitidos:
            valores_permitidos.append(x.getValue()) #Se carga con los indices que ocupan en el grafo. Lo mismo que en lista_permit solo que
                                                    #ahora son enteros y no vertices

        for x in recorrido:
            valores_recorrido.append(x.getValue())

        permitRandom = []
        for x in indicesRandom:
            permitRandom.append(valores_permitidos[x])

        permitidos = list(set(valores_permitidos)-set(permitRandom))

        for i in indicesRandom:
            indices.append(i)
            ind = self.vecinoMasCercanoV2(matrizDist,valores_permitidos[i], permitidos, valores_permitidos, valores_recorrido)
            indices.append(ind)
            permitidos.remove(valores_permitidos[ind])

        return indices

    def vecinoMasCercanoV2(self, matrizDist: list, pos: int, permitidos: list, list_permit, recorrido):
        masCercano = 999999999999
        indMasCercano = 0

        posAnterior = recorrido.index(pos)-1
        posAnterior=int(recorrido[posAnterior])

        for ind in permitidos:
            costo = matrizDist[posAnterior-1][ind-1]
            if(costo<masCercano or len(permitidos)==1):
                masCercano = costo
                indMasCercano = list_permit.index(ind)

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

    #Incrementa la frecuencia en cada arista, en caso de que se obtenga un optimo local
    def incrementaFrecuencia(self, sol):
        for x in sol.getA():
            origen = int(x.getOrigen().getValue()-1)
            destino = int(x.getDestino().getValue()-1)
            self.__frecMatriz[origen][destino] = self.__frecMatriz[origen][destino] + 1
            self.__frecMatriz[destino][origen] = self.__frecMatriz[destino][origen] + 1

    #Los ultimos minutos, comenzamos a analizar las aristas mas frecuentadas para mantenerlas estaticas
    def TS_Frecuencia(self, Sol_Optima, lista_tabu, nroIntercambios, lista_Frecuentados):
        aristasSol = Sol_Optima.getA()
        ADD = []
        DROP = []
        vertADD = None
        vertDROP = None

        #Me fijo si "esta llena" la lista tabu, tal que permita realizar los intercambios que se indicaron
        longitud =  len(Sol_Optima.getV()) - len(lista_tabu)    #Longitud de los permitidos
        longitud -= nroIntercambios     #Verifico si hay suficiente permitidos para agregar a la lista tabu

        if(longitud%2 != 0):    #Si la longitud llega a ser impar ya que necesito dos vertices para el ADD y DROP
            print("Longitud: ",longitud)
            print("Long(lista_permitidos): ",(len(Sol_Optima.getV()) - len(lista_tabu)))
            longitud-=1

        #Verifico que se cumpla las condiciones con respecto a longitudes
        if(len(lista_tabu)<longitud):
            mayFrecuencia = -1

            #Recorro las aristas de la ultima solucion optima obtenida
            for a in aristasSol:
                vert_Origen = a.getOrigen()
                vert_Destino = a.getDestino()
                frec_Actual = self.__frecMatriz[vert_Origen.getValue()-1][vert_Destino.getValue()-1]

                pertenece = self.pertenListaTabu_TSF(vert_Origen, vert_Destino, lista_tabu)
                if(frec_Actual > mayFrecuencia and not pertenece):
                    mayFrecuencia = frec_Actual
                    vertADD = vert_Origen
                    vertDROP = vert_Destino
            #Cargamos los mas frecuentados con un Tenure igual a -1, para que no se eliminen
            ADD = Tabu(vertADD, -1)
            DROP = Tabu(vertDROP, -1)
            frecuentados = []
            frecuentados.append(ADD)
            frecuentados.append(DROP)
            lista_Frecuentados.extend(frecuentados)
            print("ADD: "+str(ADD)+"    DROP: "+str(DROP)+ "       Max Frecuencia: "+str(mayFrecuencia))
        else:
            #Si no se cumple, tengo la lista tabu "llena"
            #Elimino una cantidad suficiente de la lista Tabu para que permita realizar los intercambios
            lista_Frecuentados = self.borraFrecuentados(lista_tabu)
        return lista_Frecuentados

    #Pertenece o no a la lista tabu
    def pertenListaTabu_TSF(self, v1, v2, lista_tabu):
        lista_ElementosTabu = []
        e1 = v1.getValue()
        e2 = v2.getValue()
        for x in lista_tabu:
            lista_ElementosTabu.append(x.getElemento().getValue())

        esta = (e1 in lista_ElementosTabu) or (e2 in lista_ElementosTabu)
        return esta

    #Borro una cantidad necesaria para realizar los Swapp proximos
    def borraFrecuentados(self, lista_tabu):
        #Borramos al azar
        #indices_azar = random.sample(range(0,len(lista_tabu)), self.__nroIntercambios)
        indices_azar = range(len(lista_tabu)-self.__nroIntercambios, len(lista_tabu))

        ADD = None
        DROP = None
        print("Borramos menos frecuentados")
        for ind in indices_azar:
            lista_tabu[ind].setTenure(1)
            if(ADD == None):
                ADD = lista_tabu[ind].getElemento().getValue() -1
            elif(DROP == None):
                DROP = lista_tabu[ind].getElemento().getValue() -1
            else:
                self.__frecMatriz[int(ADD)][int(DROP)] = 0
                print("indADD: "+str(ADD)+"        indDROP: "+str(DROP))
                ADD = None
                DROP = None
        self.decrementaTenure(lista_tabu)

        return lista_tabu

    ####### Empezamos con Tabu Search #########
    def tabuSearch(self):
        lista_tabu = []     #Tiene objetos de la clase Tabu
        lista_permit = []   #Tiene objetos del tipo vertice
        g1 = self._G.copyVacio()  #La primera solucion corresponde a g1
        g1.cargarDesdeSecuenciaDeVertices(self.__solInicial) #Carga solución inicial

        self.__soluciones.append(g1) #Agregar solución inicial
        self.incrementaFrecuencia(g1)

        print("Comenzando Tabu Search")
        # self.__txt.escribir("############### GRAFO CARGADO #################")
        # self.__txt.escribir(str(self._G))
        # self.__txt.escribir("################ SOLUCION INICIAL #################")
        # self.__txt.escribir("Vertices:        " + str(g1.getV()))
        # self.__txt.escribir("Aristas:         " + str(g1.getA()))
        # self.__txt.escribir("Costo asociado:  " + str(g1.getCostoAsociado()))

        ##############     Atributos       ################
        #Soluciones a utilizar
        Sol_Actual = self._G.copyVacio()
        Sol_Actual = self.__soluciones[len(self.__soluciones)-1]        #La actual es la Primera solución
        Sol_Optima = copy.deepcopy(Sol_Actual)      #Ultima solucion optima obtenida, corresponde a la primera Solucion
        lista_Frecuentados=[]

        #Atributos banderas utilizados
        condOptim = False   #En caso de que encontre uno mejor que el optimo lo guardo en el archivo txt
        #condNoMejora=False  #Se estanco o no
        condTS_Frecuencia=False #Empezamos a utilizar las aristas mas frecuentadas

        #Atributos de tiempo y otros
        tiempoIni = time()
        tiempoIniNoMejora = tiempoIni
        tiempoMax = float(self.__tiempoMaxEjec*60)
        tiempoEjecuc = 0
        costoAnterior = Sol_Actual.getCostoAsociado()
        iterac = 1

        #Duarnte 3min de no mejora o si es demasiado, la 1/5 parte del tiempo
        tiempoMaxNoMejora = 3*60
        if(tiempoMaxNoMejora > tiempoMax/5):
            tiempoMaxNoMejora = float(tiempoMax/12)  #La 1/5 parte del tiempo, en caso de que los 4min sea demasiado

        print("Tiempo maximo: "+str(int(tiempoMax/60))+"min "+str(int(tiempoMax%60))+"seg")
        print("Tiempo Max No mejora: "+str(int(tiempoMaxNoMejora/60))+"min "+str(int(tiempoMaxNoMejora%60))+"seg")

        nroIntercambios = 2 #Empezamos con 2 al inicio
        while(tiempoEjecuc<=tiempoMax):
            lista_permit = self.pertenListaTabu(lista_tabu)    #Lista de elementos que no son tabu
            ADD = []
            DROP = []

            #Verifico si hay vertices disponibles suficientes para el intercambio
            if(len(lista_permit)>=2):
                #Controla que el nro de intercambios no supere la longitud de permitidos
                if(len(lista_permit)<nroIntercambios):
                    print("Len: ",len(lista_permit))
                    nroIntercambios=len(lista_permit)
                    if(nroIntercambios%2!=0):
                        nroIntercambios-=1

                tiempoRestante = tiempoMax - tiempoEjecuc       #Lo que queda de tiempo
                if(time()-tiempoIniNoMejora>tiempoMaxNoMejora):
                    #+-+-+-+-+- Alternando el nro de Intercambios +-+-+-+-+-
                    tiempoTotal = time()-tiempoIniNoMejora
                    print("\nDurante " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg no hubo mejora")
                    print("Tiempo restante: "+str(int(tiempoRestante/60))+"min "+str(int(tiempoRestante%60))+ "seg")

                    #+-+-+-+-+-+-+-+- Frecuencia de aristas +-+-+-+-+-+-+-+-
                    print("\nAplicamos Lista Tabu con Frecuencia")

                    #la lista de frecuentados, sera luego la lista tabu
                    lista_Frecuentados = self.TS_Frecuencia(Sol_Optima, lista_tabu, nroIntercambios, lista_Frecuentados)
                    lista_tabu = lista_Frecuentados
                    lista_permit = self.pertenListaTabu(lista_tabu)
                    condTS_Frecuencia = True

                    #Obtengo 2/3 de lo que resta de tiempo, para que la proxima vez ingrese en menor tiempo cuando no hay mejoria
                    #solo en caso de que el tiempo restante sea menor al tiempo MaxNoMejora, ya que si no, no habra una proxima
                    #vez en que se estanque
                    if(tiempoRestante<tiempoMaxNoMejora):
                        tiempoMaxNoMejora = tiempoRestante*2/3

                    tiempoIniNoMejora=time()    #Reiniciamos el tiempo de No mejora

                    #Alternamos el nro de intercambios en caso de que haya un estancamiento
                    if(nroIntercambios >= self.__nroIntercambios):
                        nroIntercambios = 2
                        print("Reiniciamos el nro de intercambios")
                    elif (nroIntercambios < self.__nroIntercambios):
                        nroIntercambios+=2
                        print("Aumentamos el nro de intercambios")
                    print("Nro Intercambios: ",nroIntercambios)

                ######### Tabu Search Granular ##########
                ind_random = random.sample(range(0,len(lista_permit)),int(nroIntercambios/2))
                ind_random = self.vecinosMasCercanosTSG(ind_random, lista_permit, Sol_Optima.getV())

                #Crea los elementos ADD y DROP
                for i in range(0,len(ind_random)):
                    if(i%2==0): #Los pares para ADD y los impares para DROP
                        ADD.append(Tabu(lista_permit[ind_random[i]], self.__tenureADD))
                    else:
                        DROP.append(Tabu(lista_permit[ind_random[i]], self.__tenureDROP))

                #Realiza el intercambio de los vertices seleccionados
                for i in range(0,len(ADD)):
                    Sol_Actual = Sol_Actual.swapp(ADD[i].getElemento(), DROP[i].getElemento())

                #Si obtengo una nueva solucion optima
                if(Sol_Actual < Sol_Optima):
                    Sol_Optima = Sol_Actual                  #Actualizo la solucion optima
                    self.incrementaFrecuencia(Sol_Optima)    #Incrementa Frecuencia de Aristas visitadas

                    condOptim = True
                    nroIntercambios = 2

                    tiempoTotal = time() - tiempoIniNoMejora
                    print("Esta solución duró " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg  ---- >  " + str(Sol_Optima.getCostoAsociado()))
                    self.__soluciones.append(Sol_Actual) #Cargo las soluciones optimas
                    tiempoIniNoMejora=time()
                    #Actualizo el tenure con el tenureMax de ADD y DROP
                    for i in range(0,len(ADD)):
                        ADD[i].setTenure(self.__tenureMaxADD)
                        DROP[i].setTenure(self.__tenureMaxDROP)
                else:
                    #Si no hubo un estancamiento, utilizo la ultima solucion optima obtenida, y sigo aplicando Tabu Search
                    Sol_Actual = Sol_Optima

                #Si hemos encontramos un optima local, lo guardamos en el txt
                if(condOptim):
                    self.__txt.escribir("################################ " + str(iterac) + " ####################################")
                    self.__txt.escribir("Vertices:        " + str(Sol_Actual.getV()))
                    self.__txt.escribir("Aristas:         " + str(Sol_Actual.getA()))
                    self.__txt.escribir("Costo asociado:  " + str(Sol_Actual.getCostoAsociado()))
                    self.__txt.escribir("Tiempo actual:   "+ str())
                    self.__txt.escribir("-+-+-+-+-+-+-+-+-+-+-+-+ Lista TABÚ +-+-+-+-+-+-+-+-+-+-+-+-+")
                    self.__txt.escribir("Lista Tabu: "+ str(lista_tabu))
                    self.__txt.CSV(str(iterac),str(Sol_Optima.getV()),str(Sol_Optima.getA()),str(Sol_Optima.getCostoAsociado()),str(self.__nroIntercambios),str(self.__tenureADD),str(self.__tenureDROP),str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg")

                    condOptim = False

            self.decrementaTenure(lista_tabu)   #Decremento el tenure y elimino algunos elementos con tenure igual a 0

            #Agrego los nuevos vertices a la lista tabu o decremento el tiempo de iteracion de TS_Frecuencia
            if(not condTS_Frecuencia):
                lista_tabu.extend(ADD)
                lista_tabu.extend(DROP)

            condTS_Frecuencia = False

            lista_permit = []
            iterac += 1
            tiempoEjecuc = time()-tiempoIni
            valorMovimiento = Sol_Actual.getCostoAsociado()-costoAnterior

            #Si la solucion anterior tieneo un costo menor al siguiente obtenido, incremento la frecuencia
            if(valorMovimiento <= 0):
                self.incrementaFrecuencia(Sol_Actual)
            costoAnterior = Sol_Actual.getCostoAsociado()
        #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
        #Fin del while. Imprimo la solucion optima y algunos atributos
        tiempoFin = time()
        tiempoTotal = tiempoFin - tiempoIni
        self.__txt.escribir("\n################################ Solucion Optima ####################################")
        self.__txt.escribir("Vertices:        " + str(Sol_Optima.getV()))
        self.__txt.escribir("Aristas:         " + str(Sol_Optima.getA()))
        self.__txt.escribir("Costo asociado:  " + str(Sol_Optima.getCostoAsociado()))
        self.__txt.escribir("\nNro Intercambios: " + str(self.__nroIntercambios))
        self.__txt.escribir("Cantidad de iteraciones: "+str(iterac))
        self.__txt.escribir("Tenure ADD: " + str(self.__tenureADD) + "           Tenure DROP: "+str(self.__tenureDROP))
        self.__txt.escribir("Tiempo total: " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg")
        self.__txt.imprimir()
        self.__txt.CSV(str(iterac),str(Sol_Optima.getV()),str(Sol_Optima.getA()),str(Sol_Optima.getCostoAsociado()),str(self.__nroIntercambios),str(self.__tenureADD),str(self.__tenureDROP),str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg")
        print("Termino!! :)")
        print("Tiempo total: " + str(int(tiempoTotal/60))+"min "+str(int(tiempoTotal%60))+"seg\n")

    #Devuelve una lista con los vertices que no pertenecen a la lista tabu
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

    #Decrementa el Tenure en caso de que no sea igual a -1. Si luego de decrementar es 0, lo elimino de la lista tabu
    def decrementaTenure(self, lista_tabu: list):
        i=0
        while (i <len(lista_tabu)):
            elemTabu=lista_tabu[i]
            if(elemTabu.getTenure()!=-1):
                elemTabu.decrementaT()
            if(elemTabu.getTenure()==0):
                lista_tabu.pop(i)
                i-=1
            i+=1

    #Proximamente...
    def Opt_3(self, Sol_Optima, Sol_Nueva, Sol_Actual, tiempoIni, tiempoMax, tiempoIniNoMejora, tiempoMaxNoMejora):
        tiempoEjecuc = time()-tiempoIni
        Sol_Nueva
        while(tiempoEjecuc<tiempoMax):
            A = Sol_Actual.getA()
            A
            #a=[(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10)]
            #3-opt  ==> [(3,4),(4,5),(6,7)] ==> [[3,5],[5,4]]
            #


def resolver(objTSP):
    objTSP.tabuSearch()
if __name__ == "__main__":
    ingreso = Ingreso(sys.argv[1:])
    param = ingreso.controlArgumentos()
    archivos = param[0]
    cantidadHilos = param[len(param)-1]
    param = param[0:len(param)-1]
    listaProcesos = []
#Con pool
    pool = Pool(processes=cantidadHilos)
    listaProcesos = []
    param[0]=archivos[0]
    #for k in range(0,cantidadHilos):
    #    listaProcesos.append(TSP(*param))
    
    #for tsp in listaProcesos:
    #    pool.map(tsp.tabuSearch,)




#Con un proceso
    for i in range(0,len(archivos)):
        param[0]=archivos[i]
        listaProcesos = []
        soluciones = []
        for k in range(0,cantidadHilos):
            objTSP = TSP(*param)
            p = Process(target=objTSP.tabuSearch)
            listaProcesos.append(p)
        for j in listaProcesos:
            j.start()
            print("iniciando %d", j.pid)
        for k in listaProcesos:
            k.join()

        print(soluciones)



#Con lo que pasó el profe ...
        # listaProcesos = []
        # with Manager() as manager:
        #     listaLocks = manager.list([Lock() for x in range(0,cantidadHilos)])
        # for j in range(0,cantidadHilos):
        #     listaProcesos.append(TSP(*param,listaLocks[j]))
        # with contextlib.closing(Pool(processes=cantidadHilos)) as pool:
        #         print(pool.map(resolver, listaProcesos))