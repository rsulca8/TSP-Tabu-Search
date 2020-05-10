import sys

class clsTxt:
    def __init__(self, nombreTxt):
        self.__nombre = nombreTxt+".txt"
        try:
            self.__txt = open(self.__nombre, "x")
            self.__txt.close()
        except IOError:
            print ("No se pudo crear el archivo txt. Se intentara crear uno con otro nombre")
            try:
                self.__nombre = nombreTxt+"+.txt"
                self.__txt = open(self.__nombre, "x")
                self.__txt.close()
            except IOError:
                print ("Segundo intento fallido. Arreglá el código Maxi!")
        self.__st = ""


    def escribir(self, st):
        self.__st = self.__st + st+"\n"
    
    def imprimir(self):
        try:
            self.__txt = open(self.__nombre, "w")
            self.__txt.write(self.__st)
            self.__txt.close()
        except IOError:
            print ("No se pudo abrir el txt para imprimir")



#if __name__ == "__main__":
#    txt = clsTxt("NUEVO1")
#    txt.escribir("No lea la linea de abajo")
#    txt.escribir("Puto el que lee!")
#    txt.imprimir()