from tkinter import Tk
from Vertice import Vertice as V
from Grafo import Grafo as G
from Arista import Arista
from tkinter.filedialog import askopenfilename


if __name__ == "__main__":
	Tk().withdraw()
	filename = askopenfilename()
	print(filename)
	#Vertices
	#Creación del Grafo
	g = G(filename)

	print(g.obtenerSolucionVecinoCercano(V(1)))