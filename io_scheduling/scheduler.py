import random as r

class Scheduler:
	def schedule(queue):
		if (len(queue) > 0)
			return queue.pop()



class Random_scheduler(Scheduler):
	def schedule(queue):
		if (len(queue) > 0)
			selected = r.randint(0,len(queue))
			return queue.pop(selected)
