class Aging:
  NBITS = 8
  VALUE_SUM = 2**(NBITS - 1)
  SHIFT = 1

  def __init__(self):
    self.allocatedFrames = []

  def put(self, frame):
    """Allocates this frameId for some page"""
    # Notice that in the physical memory we don't care about the pageId, we only
    # care about the fact we were requested to allocate a certain frameId
    self.allocatedFrames.append(frame)

  def evict(self):
    indexOldestFrame = 0
    
    self.allocatedFrames.sort(key=lambda frame: frame.access_counter)
    removedFrame = self.allocatedFrames.pop(indexOldestFrame)
    
    return removedFrame.get_id()

  def clock(self):
    for frame in self.allocatedFrames:
        frame.set_referenced(False)
        frame.set_access_counter(frame.get_access_counter() >> self.SHIFT)
    
  def access(self, frameId, isWrite):
    frame = self._get_frame(frameId)
          
    if not frame.is_referenced():
        frame.set_referenced(True)
        frame.set_access_counter(frame.get_access_counter() + self.VALUE_SUM)
        
  def _get_frame(self, frameId):
    frameWanted = None
      
    for frame in self.allocatedFrames:
        if frame.get_id() == frameId:
            frameWanted = frame
            break
    
    return frameWanted
