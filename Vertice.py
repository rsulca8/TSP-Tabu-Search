class Vertice():

    def __init__(self,V, N):
        self._value = V
        self._next = N

    def getValue(self):
        return self._value

    def getNext(self):
        return self._next
    
    def setValue(self, V):
        self._value = V
    
    def setNext(self, N):
        self._next = N





