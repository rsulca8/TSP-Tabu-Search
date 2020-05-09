from Vertice import Vertice 
from Grafo import Grafo 
from Vertice import Vertice
import copy

class TSP():
    def __init__(self,Grafo: None, precision: int):
        self.__G = Grafo
        self.__Matriz = self.__G.getMatriz()
        self.digitosPrecision = precision 

    def cargarInstancia(self, archivo, metodo):
        if(metodo == "EUC_2D"):
            pass
        elif(metodo == "explicito"):
            print("carga de una matriz en formato explicito")
        elif(metodo == "manual"):
            print("carga manual")
'''
    def cargarDesdeEUC_2D(self,pathArchivo):
        archivo = open(pathArchivo,"r")
        
        self.__G.setMatriz([])
        vertices = []
        aristas = []
        lineas = archivo.readlines()
        indSeccionCoord = lineas.index("NODE_COORD_SECTION\n")
        lineaEOF = lineas.index("EOF\n")
        dim = lineaEOF - indSeccionCoord


        #Lista donde irán las coordenadas
        coordenadas = []

        #Separa las coordenadas en una matriz, es una lista de listas (vertice, coordA, coordB)
        for i in range(indSeccionCoord+1, lineaEOF):
            textoLinea = lineas[i]  
            textoLinea = re.sub("\n", "", textoLinea) #Elimina los saltos de línea
            splitLinea = textoLinea.split(" ") #Divide la línea por " " 
            coordenadas.append([splitLinea[0],splitLinea[1],splitLinea[2]]) 
        
          #Arma la matriz de distancias
        for coordRow in coordenadas:
            fila = []
            v_origen = Vertice(coordRow[0])
            vertices.append(v_origen)
            for coordCol in coordenadas:
                x1 = float(coordRow[1])
                y1 = float(coordRow[2])
                x2 = float(coordCol[1])
                y2 = float(coordCol[2])
                dist = distancia(x1,y1,x2,y2)
                if(dist == 0):
                    dist = 999999999999 #El modelo no debería tener en cuenta a las diagonal, pero por las dudas
                fila.append(dist)
                v_destino = Vertice(coordCol[0])
                aristas.append(Arista(v_origen,v_destino,dist))
            self.__matrizDistancias.append(fila)
            self.setA(aristas)
            self.setV(vertices)

'''