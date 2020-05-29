import clsSolution as Solution 
#reload(Solution)


import clsSCPInfo as SCPInfo 
#reload(SCPInfo)

import clsPheromone as Pheromone 
#reload(Pheromone)

import random
import math


class clsAnt:
	def __init__(self, alpha, beta, rho, Q0, objSCPInfo, objPheromone, infiniteValue, invalidValue):		
		self._alpha=alpha
		self._beta= beta 
		self._rho = rho
		self._Q0 = Q0

		self._objSCPInfo = objSCPInfo
		self._objPheromone = objPheromone
		
		
		self._infiniteValue = infiniteValue
		self._invalidValue = invalidValue

		self.setOFValue(self._infiniteValue)		

		self._objAntPath = Solution.clsSolution(self._objSCPInfo.getNbrOfCols(), self._invalidValue)

		self._objHeuristicInfo = Solution.clsSolution(self._objSCPInfo.getNbrOfCols(), self._invalidValue)

		self._objCoverList = Solution.clsSolution(self._objSCPInfo.getNbrOfCols(), self._invalidValue)

		self._indexList=[]
		self._probabilityList = []

		self.initializeCoverList()
		# inicializo la lista

		self.updateHeuristicInfo(False)
		# calculo la info, OJO con la solucion inicial


	def getAlpha(self):
		return self._alpha
	
	def getBeta(self):
		return self._beta
		
	def getQ0(self):
		return self._Q0

	def getRho(self):
		return self._rho

	def getOFValue(self):
		return self._OFValue

	def setOFValue(self, newValue):
		self._OFValue = newValue


	def calculateOFValue(self):
		newOFValue = 0

		size = self._objAntPath.getSize()
		for j in range(size):
			column = self._objAntPath.getValueAtPos(j)

			newOFValue += self._objSCPInfo.getColumnCost(column)

		self.setOFValue(newOFValue)


	# es para la primera vez. Usare una lista binaria
	def initializeCoverList(self):
		nbrOfRows = self._objSCPInfo.getNbrOfRows()

		if self.getOFValue()==self._infiniteValue:
			for i in range(nbrOfRows):
				self._objCoverList.addValue(0)
		else:
			for j in range(nbrOfRows):
				self._objCoverList.setValueAtPos(j, 0)


	# si restart = True, debo actualizar lista y dejarla lista para que la hormiga elija columnas
	def updateHeuristicInfo(self, restart):
		rowsCoveredList = []
		nbrOfCols = self._objSCPInfo.getNbrOfCols()
		if restart == False:

			if self.getOFValue()==self._infiniteValue and self._objHeuristicInfo.getSize()==0:
				# estoy al inicio y debo calcular para todos
				for j in range(nbrOfCols):
					self._objHeuristicInfo.addValue((self._objSCPInfo.getNbrOfRowsCovered(j) + 0.0)/self._objSCPInfo.getColumnCost(j))

			else:
				# calculo en base a la solucion parcial
				for j in range(nbrOfCols):
					if self._objAntPath.isInside(j)==True:
						self._objHeuristicInfo.setValueAtPos(j, self._invalidValue, False)

					else:
						# si la columna no esta en la solucion en construccion
						rowsCoveredList = self._objSCPInfo.getRowsCovered(j)
						columnCost = self._objSCPInfo.getColumnCost(j)
						
						counter = 0
						for row in rowsCoveredList:
							counter += self._objCoverList.getValueAtPos(row)

						rowsNotCovered = len(rowsCoveredList) - counter

						self._objHeuristicInfo.setValueAtPos(j, (rowsNotCovered + 0.0)/columnCost)

		else:
			# entra en nueva iteracion y debo calcular para todos. Esto se puede calcular una vez y queda fijo
			for j in range(nbrOfCols):
				self._objHeuristicInfo.setValueAtPos(j, (self._objSCPInfo.getNbrOfRowsCovered(j) + 0.0)/self._objSCPInfo.getColumnCost(j))



	def updatePheromone(self):
		for j in range(self._objPheromone.getSize()):
			ratio = 0.0
			if self._objAntPath.isInside(j) == True:
				ratio = 1.0 / self.getOFValue()

			currValue = self._objPheromone.getValueAtPos(j)
			self._objPheromone.setValueAtPos(j, self.getRho()*currValue + ratio)


	# con la lista de cover, si no encuentro 0 es xq cubri todo
	def pathIsBuilt(self):
		response = False

		if self._objCoverList.isInside(0)== False:
			response = True

		return response


	def resetNeighbors(self):
		self._indexList = []
		self._probabilityList = []


	def selectNeighbors(self):
		nbrOfCols = self._objSCPInfo.getNbrOfCols()
		sumP = 0.0

		for j in range(nbrOfCols):
			value = self._objHeuristicInfo.getValueAtPos(j) 
			if value!=self._invalidValue:
				product = math.pow(self._objPheromone.getValueAtPos(j), self.getAlpha())*math.pow(value,self.getBeta())

				self._probabilityList.append(product)
				self._indexList.append(j)

				sumP+=product

		if sumP>0:
			size = len(self._probabilityList)
			for i in range(size):
				self._probabilityList[i] = (self._probabilityList[i] + 0.0) / sumP

		else:

			print ("Error clsAnt selectNeighbors " + " no hay vecinos disponibles")



	def sortProbabilities(self):
		size = len(self._probabilityList)

		for i in range(size-1):
			maxP = i
			for j in range(i+1, size):
				if self._probabilityList[j]>self._probabilityList[maxP]:
					maxP = j


			auxP = self._probabilityList[i]
			auxI = self._indexList[i]

			self._probabilityList[i] = self._probabilityList[maxP]
			self._indexList[i] = self._indexList[maxP]

			self._probabilityList[maxP] = auxP
			self._indexList[maxP] = auxI


	def selectNextNeighbor(self):

		if self.pathIsBuilt()==False:
			self.resetNeighbors()
			self.selectNeighbors()
			self.sortProbabilities()

			probAtRandom = random.random()
			neighbor = self._invalidValue

			if probAtRandom<=self.getQ0():
				if self._probabilityList[0]>0:
					neighbor = self._indexList[0]

			else:
				probAtRandom = random.random()

				sumP = 0.0
				size= len(self._probabilityList)
				i = 0
				
				while i<size and sumP<probAtRandom:
					sumP+=self._probabilityList[i]
					i+=1

				if sumP>=probAtRandom:
					neighbor = self._indexList[i-1]

					self.addElementToPath(neighbor)

				else:

					print ("clsAnt selectNextNeighbor " + " no se puede terminar el camino")


	def getPathElement(self, position):
		return self._objAntPath.getValueAtPos(position) 



	def addElementToPath(self, element):
		self._objAntPath.addValue(element)

		self.updateHeuristicInfo(False)

		# aca debo marcar las filas que cubre la columna
		rowsCoveredList = self._objSCPInfo.getRowsCovered(element)		
		for row in rowsCoveredList:
			self._objCoverList.setValueAtPos(row, 1)	

	# esto se hace la primera vez
	def startPath(self):
		nbrOfCols = self._objSCPInfo.getNbrOfCols()
		column = random.randint(0, nbrOfCols-1)

		self.addElementToPath(column)



	def getPathSize(self):
		size = self._objAntPath.getSize()
		return size

	def resetPath(self):
		self._objAntPath.resetSolution()


	def restartInformation(self):
		self.resetPath()

		self.initializeCoverList()

		self.updateHeuristicInfo(True)

		self.resetNeighbors()

