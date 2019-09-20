# This is the file where you must implement the Aging algorithm

# This file will be imported from the main code. The PhysicalMemory class
# will be instantiated with the algorithm received from the input. You may edit
# this file as you whish

# NOTE: there may be methods you don't need to modify, you must decide what
# you need...

ALGORITHM_AGING_NBITS = 8
"""How many bits to use for the Aging algorithm"""

class Aging:

  def __init__(self):
    pass

  def put(self, frameId):
    pass

  def evict(self):
    pass

  def clock(self):
    pass

  def access(self, frameId, isWrite):
    pass
