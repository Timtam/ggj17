class Field:
	def __init__(self, ftype):
		self.type  = ftype
		self.tower = None
		
	def getType(self):
		return self.type
		
	def __str__(self):
		return  str(self.type)