#from Ventana import Ventana
from Vertice import Vertice as V
from Grafo import Grafo as G
from Arista import Arista
from TSP import TSP
import sys
import re
import math 
import copy

if __name__ == "__main__":
#	V = Ventana()

	matriz = [[999,2,3,5],[2,999,6,2],[7,6,999,8],[2,4,7,999]]

	g = G(matriz)

	print("g original \n" + str(g))

	
	g1 = g.copy()

	print("g1, copia de g \n" + str(g1.getMatriz()))

	print("ahora a g le paso la secuencia")

	g1.cargarDesdeSecuenciaDeVertices([V(1),V(2),V(4),V(3)])
	print("Vertices de g1  " + str(g1.getV()))
	print("Aristas de g1  " + str(g1.getA()))
	print("Costo asociado de g1 + " + str(g1.getCostoAsociado()))
	print("---------------SWAP---------------------")
	g2 = g1.swapp(V(2),V(4))
	print("Vertices de g2  " + str(g2.getV()))
	print("Aristas de g2  " + str(g2.getA()))
	print("Costo asociado de g2 + " + str(g2.getCostoAsociado()))
	
	print("---------------SWAP---------------------")
	g3 = g2.swapp(V(3),V(2))
	print("Vertices de g3  " + str(g3.getV()))
	print("Aristas de g3  " + str(g3.getA()))
	print("Costo asociado de g3  " + str(g3.getCostoAsociado()))

	print("---------------SWAP---------------------")
	g4 = g3.swapp(V(1),V(4))
	print("Vertices de g4  " + str(g4.getV()))
	print("Aristas de g4 " + str(g4.getA()))
	print("Costo asociado de g4  " + str(g4.getCostoAsociado()))

	a=TSP(matriz)
	print(a.solucionAlAzar())
	


	
	
	
