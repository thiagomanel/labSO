class NRU:
    
  INDEX_REFERENCED_ELEMENT = 0
  INDEX_MODIFIED_ELEMENT = 1  

  def __init__(self):
    self.allocated_frames = {}

  def put(self, frame):
    """Allocates this frameId for some page"""
    # Notice that in the physical memory we don't care about the pageId, we only
    # care about the fact we were requested to allocate a certain frameId
    self.allocated_frames.update({frame.get_id(): ['0', '0']})
    
  def evict(self):
    removed_frame_id = self._get_min_frame_id()
    del self.allocated_frames[removed_frame_id]
    
    return removed_frame_id

  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # Clear the reference bits (and/or whatever else you think you must do...)
    for frame in self.allocated_frames:
        self.allocated_frames[frame][self.INDEX_REFERENCED_ELEMENT] = '0'

  def access(self, frame_id, is_write):
    """A frame_id was accessed for read/write (if write, is_write=True)"""
    self.allocated_frames[frame_id][self.INDEX_REFERENCED_ELEMENT] = '1'
    if is_write:
        self.allocated_frames[frame_id][self.INDEX_MODIFIED_ELEMENT] = '1'
  
  def _get_min_frame_id(self):
        index_oldest_frame = 0
        min_frame_id = self.allocated_frames.keys()[index_oldest_frame]
                        
        for frame_id in self.allocated_frames:
            value_frame = int(''.join(self.allocated_frames[frame_id]), 2)
            value_min_frame = int(''.join(self.allocated_frames[min_frame_id]), 2)
            
            if value_frame <= value_min_frame:
                min_frame_id = frame_id        
            
        return min_frame_id
