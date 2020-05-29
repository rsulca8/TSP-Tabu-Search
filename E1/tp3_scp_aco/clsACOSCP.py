import clsSCPInfo as SCPInfo 
#reload(SCPInfo)

import clsAntColony as AntColony 
#reload(AntColony)

import clsPheromone as Pheromone 
#reload(Pheromone)


class clsACOSCP:
	def __init__(self):		
		self._alpha=0
		self._beta= 0
		self._rho = 0
		self._initialValue  = 0.0  # debo ser si esto es un parametro 0.001
		self._Q0=0.0

		self._iters = 0
		self._ants = 0
		
		self._instanceName=''
		self._resultDir=''
		self._instanceDir=''
		self._invalidValue = -1 # valor invalido de posiciones
		self._infiniteValue = 100000

		self._objSCPInfo = SCPInfo.clsSCPInfo(self._invalidValue, self._infiniteValue)
		self._objAntColony = None
		self._objPheromone = None 
		self._bestOF= self._infiniteValue
		
		self._currOF = self._infiniteValue
		self._currPos = self._invalidValue

	def setAlpha(self, alpha):
		self._alpha = alpha

	def getAlpha(self):
		return self._alpha

	def setBeta(self, beta):
		self._beta = beta

	def getBeta(self):
		return self._beta

	def setRho(self, rho):
		self._rho = rho

	def getRho(self):
		return self._rho

	def setQ0(self, Q0):
		self._Q0=Q0

	def getQ0(self):
		return self._Q0

	def setInitialValue(self, initialValue):
		self._initialValue = initialValue

	def getInitialValue(self):
		return self._initialValue

	def setNbrOfAnts(self, nbrOfAnts):
		self._nbrOfAnts = nbrOfAnts

	def getNbrOfAnts(self):
		return self._nbrOfAnts

	def setNbrOfIters(self, iters):
		self._iters = iters

	def getNbrOfIters(self):
		return self._iters

	def setBestOFValue(self, newValue):
		self._bestOF = newValue

	def getBestOFValue(self):
		return self._bestOF

	
	def setResultDir(self, resultDir):
		self._resultDir = resultDir


	def setInstanceDir(self, instanceDir):
		self._instanceDir = instanceDir

		self._objSCPInfo.setInstanceDir(instanceDir)


	def getFilename(self):
		return self._instanceDir + self._instanceName


	def setInstanceName(self, instanceName):
		self._instanceName = instanceName

		self._objSCPInfo.setInstanceName(instanceName)



	def openFile(self):
		self._objSCPInfo.openFile()

	
	# aplico LS sobre una solucion
	def applyLocalSearch(self, position):
		 pass



	def isInfoLoaded(self):
		response = False

		if self.getAlpha()>0 and self.getBeta()>0 and self.getRho()>0 and self.getInitialValue()>0 and self.getQ0()>0 and self.getNbrOfIters()>0 and self.getNbrOfAnts()>0 and self.getFilename()!='':
			response = True

		return response

'''
Parametros de ACO:
iters: nro de iteraciones,
steps: # de pasos,
ants: cantidad de hormigas
alfa: importancia de la informacion heuristica
beta:
rho:

currOF: funcion objetivo actual

INFO para las hormigas = {Heuristica, Aprendizaje}
Heuristica = info especifica del problema. Es estatica. 
Aprendizaje = feromona = es lo que la Colonia va aprendiendo durante la ejecucion
feromona = es dinamica
'''
	def solveProblem(self):
		if self.isInfoLoaded()==True:

			self._objPheromone = Pheromone.clsPheromone(self._initialValue, self._objSCPInfo.getNbrOfCols(), self._invalidValue) 
			# instanciado e inicializado

			self._objAntColony = AntColony.clsAntColony(self.getNbrOfAnts(), self.getAlpha(), self.getBeta(), self.getRho(), self.getQ0(), self._objSCPInfo, self._objPheromone, self._invalidValue, self._infiniteValue)
			# instancio la colonia

			nbrOfSteps = self._objSCPInfo.getNbrOfCols()
			for iter in range(self.getNbrOfIters()):
				print (" Iter " + str(iter))

				for step in range(nbrOfSteps):					
					if step==0:
						self._objAntColony.startPaths()
						# debo generar inicio de camino de las hormigas

					for k in range(self.getNbrOfAnts()):						
						self._objAntColony.selectNextNeighbor(k)


				self._currOF = self._infiniteValue
				self._currPos = self._invalidValue

				#Me fijo cual es la mejor hormiga
				for k in range(self.getNbrOfAnts()):
					self._objAntColony.calculateOFValue(k)
					currOF = self._objAntColony.getOFValue(k)

					print ("Ant " + str(k) + " currOF " + str(currOF))
					if currOF < self._currOF:
						self._currOF = currOF
						self._currPos = k


				self.applyLocalSearch(self._currPos)
				# aplico LS a la mejor hormiga de la iteracion

				self._objAntColony.updatePheromone(self._currPos)
				# actualiza pheromone la mejor hormiga. Solamente deposita pheromone la mejor hormiga
				# la pheromone es dinamica. Es APRENDIZAJE
				currOF = self._objAntColony.getOFValue(self._currPos)

				if currOF<self.getBestOFValue():
					self.setBestOFValue(currOF)
					self._objAntColony.updateBestAnt(self._currPos)
					# debo hacer copia de solucion


				self._objAntColony.restartInformation()


			print ("Instance "  + self._instanceName + " Best OF " + str(self.getBestOFValue())) 

		else:
			print ("Error clsACOCSP solveProblem " + " Falta info para resolver el problema.")



	def saveResults(self):
		pass

