import sys
import os
import csv
class clsTxt:
    def __init__(self, nombreTxt):
        i = 0
        while os.path.exists("%s (%i).txt" %(nombreTxt,i)):
            i += 1
        self.__nombre = "%s (%i)" %(nombreTxt,i)
        self.__txt = open(str(self.__nombre)+".txt", "w")
        self.__ArchivoCSV = open(str(self.__nombre)+".csv", "w",newline="")
        self.__st = ""
        self.__fieldnames = ['iteración','Vertices','Aristas','costo',"intercambios","tenureADD","tenureDROP","tiempo"]
        self.__CSV = csv.DictWriter(self.__ArchivoCSV, fieldnames=self.__fieldnames)

    def escribir(self, st):
        self.__st = self.__st + st+"\n"
    


    def CSV(self,iteracion,Vertices,Aristas,costo,intercambios,tenureADD,tenureDROP,tiempo):
        self.__CSV.writerow({'iteración':str(iteracion),
        'Vertices':str(Vertices),
        'Aristas':str(Aristas),
        'costo':str(costo),
        "intercambios":str(intercambios),
        "tenureADD":str(tenureADD),
        "tenureDROP":str(tenureDROP),
        "tiempo":str(tiempo)}) 

    def imprimir(self):
        try:
            self.__txt = open(self.__nombre, "w")
            self.__txt.write(self.__st)
            self.__txt.close()
        except IOError:
            print ("No se pudo abrir el txt para imprimir")