from Vertice import Vertice as V
from Grafo import Grafo as G
from Arista import Arista

if __name__ == "__main__":

    #Vertices
    v1 = V(1)
    v2 = V(2)
    v3 = V(3)

    Vertices = [v1,v2,v3]

    #Aristas 

    a1 = Arista(v1,v2,0)
    a2 = Arista(v2,v3,0)
    a3 = Arista(v3,v2,0)

    Aristas = [a1,a2,a3]

    #Creación del Grafo
    g = G(Vertices, Aristas)

    print("Grafo g: \n" + str(g))

    #Cargar desde Matriz    
    print("------------------ CARGAR DESDE MATRIZ --------------------------")

    matriz = [[1,0,0],[1,4,5],[2,3,4]]

    g1 = G(V,None)
    g1.cargarDesdeMatriz(g1.getV(),matriz)

    print("Grafo g1: \n" + str(g1))
    

