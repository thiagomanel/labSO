import algorithms

class PhysicalMemory:
  """How many bits to use for the Aging algorithm"""

  def __init__(self, alg_name):
    
    self.algorithm = algorithms.get_algorithm(alg_name)
  

  def put(self, frameId):
    """Allocates this frameId for some page"""
    # Notice that in the physical memory we don't care about the pageId, we only
    # care about the fact we were requested to allocate a certain frameId
    self.algorithm.put(frameId)

  def evict(self):
    """Deallocates a frame from the physical memory and returns its frameId"""
    # You may assume the physical memory is FULL so we need space!
    # Your code must decide which frame to return, according to the algorithm
    return self.algorithm.evict()

  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # Clear the reference bits (and/or whatever else you think you must do...)
    self.algorithm.clock()

  def access(self, frameId, isWrite):
    """A frameId was accessed for read/write (if write, isWrite=True)"""
    self.algorithm.access(frameId, isWrite)
