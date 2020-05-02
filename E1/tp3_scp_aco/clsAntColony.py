import clsAnt as Ant
reload(Ant)

import clsSCPInfo as SCPInfo 
reload(SCPInfo)

import clsPheromone as Pheromone 
reload(Pheromone)


class clsAntColony:
	def __init__(self, nbrOfAnts, alpha, beta, rho, Q0, objSCPInfo, objPheromone, invalidValue, infiniteValue):

		self._nbrOfAnts = nbrOfAnts
		self._alpha = alpha
		self._beta = beta
		self._rho = rho
		self._Q0 = Q0
		
		
		self._bestPos = nbrOfAnts
		self._auxPos = nbrOfAnts + 1

		self._invalidValue = invalidValue
		self._infiniteValue = infiniteValue


		self._objSCPInfo = objSCPInfo
		self._objPheromone = objPheromone 
		
		self.initializeInfo()


	def initializeInfo(self):
		self._myList = []

		for i in range(self._nbrOfAnts + 2):
			self._myList.append(Ant.clsAnt(self.getAlpha(), self.getBeta(), self.getRho(), self.getQ0(), self._objSCPInfo, self._objPheromone, self._infiniteValue, self._invalidValue))


	def getAlpha(self):
		return self._alpha
	
	def getBeta(self):
		return self._beta

	def getRho(self):
		return self._rho

	def getNbrOfAnts(self):
		return self._nbrOfAnts

	def getQ0(self):
		return self._Q0

	
	def updatePheromone(self,k):
		if k>=0 and k<self.getNbrOfAnts():
			self._myList[k].updatePheromone()

		else:
			print "Error clsAntColony updatePheromone " + " posicion invalida"


	def calculateOFValue(self, k):
		if k>=0 and k<self.getNbrOfAnts()+2:
			self._myList[k].calculateOFValue()
		else:
			print "Error clsAntColony calculateOFValue " + " posicion invalida"


	def getOFValue(self, k):
		value = self._infiniteValue

		if k>=0 and k<self.getNbrOfAnts()+2:
			value =  self._myList[k].getOFValue()
		else:
			print "Error clsAntColony getOFValue " + " posicion invalida"

		return value


	# debo actualizar solucion de hormiga k con la mejor
	def updateBestAnt(self, k):
		if k>=0 and k<self.getNbrOfAnts():
			self._myList[self._bestPos].resetPath()

			size = self._myList[k].getPathSize()
			for i in range(size):
				column = self._myList[k].getPathElement(i)
				self._myList[self._bestPos].addElementToPath(column)

			self.calculateOFValue(self._bestPos)


		else:
			print "Error clsAntColony updateBestAnt " + " posicion invalida"


	def selectNextNeighbor(self, k):
		if k>=0 and k<self.getNbrOfAnts():
			self._myList[k].selectNextNeighbor()
		else:
			print "Error clsAntColony updateBestAnt " + " posicion invalida"


	def restartInformation(self):
		for k in range(self.getNbrOfAnts()):
			self._myList[k].restartInformation()


	def startPaths(self):
		for k in range(self.getNbrOfAnts()):
			self._myList[k].startPath()

		

