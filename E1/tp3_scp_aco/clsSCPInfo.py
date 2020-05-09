import clsSolution as Solution 
#reload(Solution)


class clsSCPInfo:	
	def __init__(self, invalidValue, infiniteValue):
		'''
		Datos de SCP
		#Filas, #Columnas, Lista de costos, Lista de filas que cubre
		
		'''
		self._rows = 0 
		self._cols=0

		self._instanceDir=''
		self._instanceName=''
		self._myFile=None


		self._invalidValue = invalidValue
		self._infiniteValue = infiniteValue

		self._costList=None		
		self._colList=None # lista de cols, cada elemento (columna) indica que filas cubre
		

	def setInstanceDir(self, instanceDir):
		self._instanceDir = instanceDir

	def setInstanceName(self, instanceName):
		self._instanceName = instanceName


	def getFilename(self):
		return self._instanceDir + self._instanceName

	def getNbrOfCols(self):
		return self._cols

	def getNbrOfRows(self):
		return self._rows

	def initializeInfo(self):
		pass

	def openFile(self):
		self.initializeInfo()
		
		'''
		2
		1 2 5 6 9 10

		Fila 2
		Cubierta por 1, 2, 5, 6, 9 y 10
		'''

		try:
			self._myFile=open(self.getFilename(), 'r') #leo el nombre del archivo

			linea = self._myFile.readline()
			self._rows, self._cols = linea.strip().split(" ")
			self._rows = int(self._rows)
			self._cols = int(self._cols)

			print (" cols " + str(self._cols) + " rows " + str(self._rows))

			# objeto lista de costos
			self._costList=Solution.clsSolution(self._cols, self._invalidValue)

			# objeto lista de filas cubiertas por columnas			
			self._colList=Solution.clsSolution(self._cols, self._invalidValue)

			#Leo los costos de cada una de las columnas que tiene mi instancia
			linea = self._myFile.readline().strip().split(" ")
			while (len(linea)>1):
				for i in range(len(linea)):
					self._costList.addValue(int(linea[i]))

				linea = self._myFile.readline().strip().split(" ")

			#Para cada columna 
			for j in range(self._cols):
				self._colList.addValue([])
				# inicializo la lista de columnas. cada elemento tendra las filas que cubre


			nbrOfCoverings = int(linea[0])
			row = 0
			counter = 0
			while counter<nbrOfCoverings:
				linea=self._myFile.readline().strip().split(" ")
				print(str(linea)+"\n")

				for j in range(len(linea)):
					#self._colList[int(linea[j])-1].append(row)
					self._colList.addValueAtPos(int(linea[j])-1, row)
					# aca digo que la columna linea[j] cubre a la fila row

				counter+=len(linea)
				if counter ==nbrOfCoverings:
					if row < self._rows - 1:
						linea=self._myFile.readline().strip().split(" ")
						nbrOfCoverings = int(linea[0])
						counter = 0
						row+=1 # paso a otra fila de la matriz
					else:
						counter = nbrOfCoverings + 100
						# me voy

			print (" Lectura exitosa")



		except IOError:
			print ("Error clsSCPInfo openFile. No existe el archivo")

	
	def getColumnCost(self, position):
		cost = self._infiniteValue

		if position>=0 and position<self._costList.getSize():
			cost = self._costList.getValueAtPos(position)

		else:

			print ("Error clsSCPInfo getColumnCost " + " Posicion invalida")

		return cost


	def getNbrOfRowsCovered(self, position):
		counter = self._invalidValue

		if position>=0 and position<self._colList.getSize():
			counter = len(self._colList.getValueAtPos(position))

		else:

			print ("Error clsSCPInfo getColumnCost " + " Posicion invalida")

		return counter

	# devuelve la lista de filas que cubre una columna
	def getRowsCovered(self, position):
		rowsCoveredList = []

		if position>=0 and position<self._colList.getSize():
			rowsCoveredList = self._colList.getValueAtPos(position)

		else:
			print ("Error clsSCPInfo getRowsCovered " + str(position) + " posicion invalida")

		return rowsCoveredList