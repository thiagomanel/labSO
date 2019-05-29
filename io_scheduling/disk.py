class Disk:
	def __init__(self,track_size):
		self.track_size=track_size
		self.current_position = 0

	def distance(self,new_position):
		return (self.current_position - new_position)%self.track_size
