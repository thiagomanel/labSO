# coding: utf-8
class SecondChance:

  def __init__(self):
    self.allocatedFrames = []

  def put(self, frame):
    """Allocates this frameId for some page"""
    # Notice that in the physical memory we don't care about the pageId, we only
    # care about the fact we were requested to allocate a certain frameId
    self.allocatedFrames.append(frame)

  def evict(self):
    """Deallocates a frame from the physical memory and returns its frameId"""
    # You may assume the physical memory is FULL so we need space!
    # Your code must decide which frame to return, according to the algorithm
    # Se pagina mais antiga possui bit R=0, ela eh removida.
    # – Se tiver bit R=1, o bit eh zerado, e a pagina eh colocada no final da fila,. Ou seja: da se uma 2a chance
    indexOldFrame = 0
    if self.allocatedFrames[indexOldFrame].is_referenced():
      self.allocatedFrames[indexOldFrame].set_referenced(False)
      self.allocatedFrames.append(self.allocatedFrames.pop(indexOldFrame))
      return self.evict()
      
    else:
      frameRemoved = self.allocatedFrames.pop(indexOldFrame) 
      return frameRemoved.get_id()

    return self.allocatedFrames.pop(indexOldFrame).get_id()
    
  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # Clear the reference bits (and/or whatever else you think you must do...)
    pass

  def access(self, frameId, isWrite):
    """A frameId was accessed for read/write (if write, isWrite=True)"""
    for frame in self.allocatedFrames:
      if frame.get_id() == frameId: 
        frame.set_referenced(True)
        frame.set_modified(isWrite)
        break
            