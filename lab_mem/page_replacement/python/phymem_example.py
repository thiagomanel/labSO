# This is just an example of an implementation of the PhysicalMemory
# It implements the Random algorithm:
# https://en.wikipedia.org/wiki/Page_replacement_algorithm#Random

from random import randint

class PhysicalMemory:
  def __init__(self, algorithm):
    assert algorithm in {"random"}
    self.allocatedFrames = []

  def put(self, frameId):
    """Allocates this frameId for some page"""
    self.allocatedFrames.append(frameId)
    pass

  def evict(self):
    """Deallocates a frame from the physical memory and returns its frameId"""
    random_index = randint(0, len(self.allocatedFrames) - 1)
    return self.allocatedFrames.pop(random_index)

  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # No need to do anything here for this algorithm...
    pass

  def access(self, frameId, isWrite):
    """A frameId was accessed for read/write (if write, isWrite=True)"""
    # No need to do anything here for this algorithm...
    pass