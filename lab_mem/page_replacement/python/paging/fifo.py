class FIFO:

  def __init__(self):
    self.allocatedFrames = []

  def put(self, frameId):
    self.allocatedFrames.append(frameId)

  def evict(self):
    indexOldFrame = 0
    return self.allocatedFrames.pop(indexOldFrame).get_id()

  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # Clear the reference bits (and/or whatever else you think you must do...)
    pass

  def access(self, frameId, isWrite):
    """A frameId was accessed for read/write (if write, isWrite=True)"""
    pass