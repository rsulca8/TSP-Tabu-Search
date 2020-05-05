from Vertice import Vertice as V
from Grafo import Grafo as G
from Arista import Arista

if __name__ == "__main__":

    #Vertices
    #Creación del Grafo
    g = G("eil101.tsp")

    v1 = V(1)
    v2 = V(2)
    v3 = V(3)
    v4 = V(4)

    str(v1)

    a1 = Arista(v1,v2,0)
    a2 = Arista(v2,v1,0)
    a3 = Arista(v2,v3,0)
    a4 = Arista(v1,v3,0)


    print("------------------ CARGAR DESDE MATRIZ --------------------------")
    #g.obtenerSolucionVecinoCercano(V(1))
    print("NODOS CON ORIGEN")

    @
    print(g.obtenerSolucionVecinoCercano(V(1)))
    #print(g)
    #print("grafo g: " + str(g))
    #g1 = G(Vertices,None)
    #g1.cargarDesdeMatriz(Vertices,matriz)

    #print("Grafo g1: \n" + str(g1))
    

