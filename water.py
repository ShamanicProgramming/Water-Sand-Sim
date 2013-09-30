import random

class Water(object):
	"""simple class containing only a rect and directional information"""
	def __init__(self, image):
		self.rect = image.get_rect()
		
		self.direction = random.randint(0, 1)