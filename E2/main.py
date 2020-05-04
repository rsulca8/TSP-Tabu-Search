from Vertice import Vertice as V
from Grafo import Grafo as G
from Arista import Arista

if __name__ == "__main__":

    #Vertices
    #Creación del Grafo
    g = G("eil101.tsp")



    
    print("------------------ CARGAR DESDE MATRIZ --------------------------")
    #g.obtenerSolucionVecinoCercano(V(1))
    print("NODOS CON ORIGEN")
    print("A: " + str(g.getA()) + "\n" +"\n")
    print(g.obtenerSolucionVecinoCercano(V(1)))

    #print("grafo g: " + str(g))
    #g1 = G(Vertices,None)
    #g1.cargarDesdeMatriz(Vertices,matriz)

    #print("Grafo g1: \n" + str(g1))
    

