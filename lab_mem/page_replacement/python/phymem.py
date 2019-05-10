from frame import Frame 
from paging.fifo import FIFO
from paging.second_chance import SecondChance
from paging.nru import NRU
from paging.lru import LRU
from paging.aging import Aging

# This is the only file you must implement

# This file will be imported from the main code. The PhysicalMemory class
# will be instantiated with the algorithm received from the input. You may edit
# this file as you which

# NOTE: there may be methods you don't need to modify, you must decide what
# you need...

class PhysicalMemory:
  ALGORITHM_AGING_NBITS = 8
  """How many bits to use for the Aging algorithm"""

  def __init__(self, algorithmType):
    assert algorithmType in {"fifo", "nru", "aging", "second-chance"}
    
    if algorithmType == "fifo":
        self.algorithm = FIFO()

    elif algorithmType == "second-chance":
        self.algorithm = SecondChance()

    elif algorithmType == "nru":
        self.algorithm = NRU()

    elif algorithmType == "lru":
        self.algorithm = LRU()

    elif algorithmType == "aging":
        self.algorithm = Aging()

  def put(self, frameId):
    """Allocates this frameId for some page"""
    # Notice that in the physical memory we don't care about the pageId, we only
    # care about the fact we were requested to allocate a certain frameId
    frameObj = Frame(frameId)
    self.algorithm.put(frameObj)


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
