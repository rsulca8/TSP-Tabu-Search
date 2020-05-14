#from Ventana import Ventana
from Vertice import Vertice as V
from Grafo import Grafo as G
from Arista import Arista
#from TSP import TSP
import sys
import re
import math 
import copy
from Solucion import Solucion 
from TSP import TSP

if __name__ == "__main__":
#	V = Ventana()

	matriz = [[999,2,3,5,6,7,8],
			  [2,999,6,4,2,3,4],
			  [3,6,999,8,2,6,6],
			  [5,4,8,999,4,1,3],
			  [6,2,2,4,999,1,3],
			  [7,3,6,1,1,999,3],
			  [8,4,6,3,3,3,999]
			  ]

	g = G(matriz)

	s1 = Solucion([V(1),V(2),V(3),V(4)],matriz)	#21
	print(s1)

	tsp = TSP(matriz, "prueba", True)


#	s2 = Solucion([V(1),V(3),V(2),V(4)],matriz)
#	s3 = Solucion([V(1),V(2),V(4),V(3)],matriz)
#	s4 = Solucion([V(1),V(4),V(3),V(2)],matriz)



		





	
	
	
