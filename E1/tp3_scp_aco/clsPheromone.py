
import clsSolution as Solution
reload(Solution)

class clsPheromone(Solution.clsSolution):
	def __init__(self, initialValue, cols, invalidValue):
		Solution.clsSolution.__init__(self, cols, invalidValue)
		self._initialValue = initialValue

		self.initialize()


	def initialize(self):
		for i in range(self._cols):
			self._myList.append(self._initialValue)
