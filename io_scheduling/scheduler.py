import random as r

class Scheduler:
	def schedule(queue):
		return 0



class Random_scheduler(Scheduler):
	def schedule(queue):
		return r.randint(0,len(queue))
