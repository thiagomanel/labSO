# This is just an example of an implementation of the PhysicalMemory
# It implements the Random algorithm:
# https://en.wikipedia.org/wiki/Page_replacement_algorithm#Random

from random import randint

class Random:

  def __init__(self):
    self.allocatedFrames = []

  def put(self, frameId):
    self.allocatedFrames.append(frameId)
    pass

  def evict(self):
    random_index = randint(0, len(self.allocatedFrames) - 1)
    return self.allocatedFrames.pop(random_index)

  def clock(self):
    # No need to do anything here for this algorithm...
    pass

  def access(self, frameId, isWrite):
    # No need to do anything here for this algorithm...
    pass