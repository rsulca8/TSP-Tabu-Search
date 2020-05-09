#from Ventana import Ventana
from Vertice import Vertice as V
from Grafo import Grafo as G
from Arista import Arista
import sys
import re
import math 
import copy

if __name__ == "__main__":
#	V = Ventana()

	matriz = [[1,2,3,5],[2,4,6,2],[7,6,7,8],[2,4,7,4]]

	g = G(matriz)

	print("g original \n" + str(g))

	
	g1 = g.copy()

	print("g1, copia de g \n" + str(g1.getMatriz()))

	print("ahora a g le paso la secuencia")

	g1.cargarDesdeSecuenciaDeVertices([V(1),V(2),V(4),V(3)])
	print("Vertices de g1 + " + str(g1.getV()))
	print("Aristas de g1 + " + str(g1.getA()))

	
	g2 = g1.swapVertice(V(3),V(4))
	print("---------------SWAP---------------------")
	print("Vertices de g2 + " + str(g2.getV()))
	print("Aristas de g2 + " + str(g2.getA()))
	

