from Vertice import Vertice as V
from Grafo import Grafo as G
from Arista import Arista

if __name__ == "__main__":

    #Vertices
    v1 = V("1")
    v2 = V("2")
    v3 = V("3")

    Vertices = [v1,v2,v3]

    #Aristas 

    a1 = Arista(v1,v2,1)
    a2 = Arista(v2,v3,3)
    a3 = Arista(v3,v2,2)
    a4 = Arista(v1,v3,3)
    a5 = Arista(v1,v1,4)

    Aristas = [a1,a2,a3,a4,a5]

    #Creación del Grafo
    g = G(Vertices, Aristas)

    #print("Grafo g: \n" + str(g))


    print("----------")


    
    print("------------------ CARGAR DESDE MATRIZ --------------------------")

    g.cargarDesdeEUC_2D(g.getV, "eil101.tsp")
    #print("grafo g: " + str(g))
    #g1 = G(Vertices,None)
    #g1.cargarDesdeMatriz(Vertices,matriz)

    #print("Grafo g1: \n" + str(g1))
    

