class clsSolution:
	def __init__(self, cols, invalidValue):
		self.resetSolution()
		self._cols = cols
		self._invalidValue = invalidValue


	def resetSolution(self):
		self._myList=[]


	def getSize(self):
		return len(self._myList)


	def addValue(self, value):
		if self.getSize()<self._cols:
			self._myList.append(value)
		else:
			print ("Error clsSolution addValue. Tamanio excedido")

	# esto lo uso en lista de filas cubiertas por las columnas
	def addValueAtPos(self, position, value):
		if position>=0 and position<self.getSize():
			self._myList[position].append(value)
		else:
			print ("Error clsSolution addValueAtPos." + str(position) + " no existe.")



	def addColumn(self, column):
		if column not in self._myList:
			if self.getSize()<self._cols:
				self._myList.append(column)
			else:
				print ("Error clsSolution addColumn. Tamanio excedido")

		else:

			print ("Error clsSolution addColumn " + str(column) + " ya existe." )


	def delColumn(self, column):
		if column in self._myList:
			position = self._myList.index(column)
			del(self._myList[position])
		else:

			print ("Error clsSolution delColumn " + str(column) + " no existe.")


	def getValueAtPos(self, position):
		value = self._invalidValue
		if position>=0 and position<self.getSize():
			value = self._myList[position]

		else:
			print ("Error clsSolution getValueAtPos " + str(position) + " no existe.")

		return value


	def setValueAtPos(self, position, newValue, checkValue=True):
		if position>=0 and position<self.getSize():
			if checkValue==True:
				if newValue>=0 and newValue<self._cols:
					self._myList[position] = newValue

				else:
					print ("Error clsSolution setValueAtPos " + str(newValue) + " valor incorrecto.")
			else:
				self._myList[position] = newValue
				# esto es para el usar negativos en la lista heuristica

		else:
			print ("Error clsSolution setValueAtPos " + str(position) + " no existe.")



	def isInside(self,element):
		response = False

		if len(self._myList)>0:
			if element in self._myList:
				response = True
		else:
			print ("Error clsSolution isInside " + " lista vacia.")

		return response