import sys
import argparse
class Ingreso():
    def __init__(self, argv): #recibe como parámetro la lista de argumentos recibidos por consola
        self.arg= argv 
        if(len(argv)==0):
            print("No se cargaron argumentos")
            self.mostrarAyuda()
            sys.exit()
        self.tenureADD = 0
        self.tenureMaxADD = 0
        self.tenureDROP = 0
        self.tenureMaxDROP = 0
        self.nombreArchivo = ""
        self.tiempo = 0
        self.iteraciones = 0
        self.intercambios = 0
        self.subiteraciones = 0
        self.solucionInicial = 0
        self.controlArgumentos()
        

    
    def controlArgumentos(self):
        tiempoOiteracion = False
        arg = self.arg 
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", nargs='+', metavar= "FILE", help='Nombre del Archivo',type=str, required=True)
        parser.add_argument("--subiteration", nargs='?', default= 900 , help='Nombre del Archivo',type=int)
        parser.add_argument("--tenureadd", nargs='?', default = 0 , help='--tenureadd tenure add (si no se especifica se toma por defecto el 10% de la cantidad de vertices)',type=int)
        parser.add_argument("--tenureaddmax", nargs='?', default = 0 , help='--tenureaddmax  tenure máximo (si no se especifica se toma por defecto el 15% de la cantidad de vertices)',type=int)
        parser.add_argument("--tenuredrop", nargs='?', default = 0 , help='--tenuredrop tenure drop (si no se especifica se toma por defecto el 10% de la cantidad de vertices)',type=int)
        parser.add_argument("--tenuredropmax", nargs='?', default = 0 , help='--tenuredropmax tenure drop máximo (si no se especifica se toma por defecto el 15% de la cantidad de vertices)',type=int)
        parser.add_argument("--intercambios", nargs='?', default = 0 , help='--intercambios número de intercambios',type=int)
        parser.add_argument("--solucioninicial", nargs='?',default = 0 ,  help='--solucioninicial tipo de solución inicial, 0 para vecino cercano, 1 para solución inicial al azar',type=int)
        parser.add_argument('--iteration', nargs='?', default = 1000 , help='--iteration cantidad máxima de iteraciones, por defecto se toma 1000',type=int)   
        parser.add_argument('--time', nargs='?', default = 0 , help='--time tiempo total de la busqueda se expresa en minutos',type=int)
        parser.add_argument('--hilos',nargs='?', default = 4 , help='Nombre del Archivo',type=int)
        arg = parser.parse_args()
        return [arg.file,
                arg.tenureadd,
                arg.tenureaddmax,
                arg.tenuredrop,
                arg.tenuredropmax,
                arg.iteration, 
                arg.subiteration,
                arg.time,
                arg.intercambios,
                arg.solucioninicial,
                arg.hilos]
    def mostrarAyuda(self):
        mensaje = """
                Se debe cargar una instancia en formato EUC 2D
                -F o --file [Nombre del Archivo]
                -T o --time tiempo total de la busqueda se expresa en minutos
                -I o --iteration cantidad máxima de iteraciones, por defecto se toma 1000
                -i o --subiteration cantidad máxima de subiteraciones, si no se ingresa, se toma el 90% de las iteraciones
                -tA o --tenureadd tenure add (si no se especifica se toma por defecto el 10% de la cantidad de vertices)
                -tAM o --tenureaddmax  tenure máximo (si no se especifica se toma por defecto el 15% de la cantidad de vertices)
                -tD o --tenuredrop tenure drop (si no se especifica se toma por defecto el 10% de la cantidad de vertices)
                -tDM o --tenuredropmax tenure drop máximo (si no se especifica se toma por defecto el 15% de la cantidad de vertices)
                -int o --intercambios número de intercambios
                -sI o --solucioninicial tipo de solución inicial, 0 para vecino cercano, 1 para solución inicial al azar
                """
        print(mensaje)


    def getArchivo(self):
        return self.nombreArchivo
