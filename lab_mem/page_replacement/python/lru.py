class LRU:

  def __init__(self):
    self.allocated_frames = {}

  def put(self, frame):
    """Allocates this frameId for some page"""
    # Notice that in the physical memory we don't care about the pageId, we only
    # care about the fact we were requested to allocate a certain frameId
    self.allocated_frames.update({frame.get_id(): ['0'] * len(self.allocated_frames)})
    
    for frame in self.allocated_frames:
        self.allocated_frames[frame].append('0')

  def evict(self):
    index_oldest_frame = 0
    
    copy_frames = self._copy_dict()
    sorted_frames = sorted(copy_frames, key=copy_frames.get)    
    removed_frame_id = sorted_frames.pop(index_oldest_frame)
    index_removed_frame_id = self.allocated_frames.keys().index(removed_frame_id)
    del self.allocated_frames[removed_frame_id]
        
    for frame in self.allocated_frames:
        del self.allocated_frames[frame][index_removed_frame_id]
    
    return removed_frame_id

  def clock(self):
    """The amount of time we set for the clock has passed, so this is called"""
    # Clear the reference bits (and/or whatever else you think you must do...)
    pass

  def access(self, frame_id, is_write):
    """A frame_id was accessed for read/write (if write, is_write=True)"""
    self.allocated_frames[frame_id] = ['1'] * len(self.allocated_frames)
    index_frame_id = self.allocated_frames.keys().index(frame_id)
    
    for frame in self.allocated_frames:
        self.allocated_frames[frame][index_frame_id] = '0'

  def _copy_dict(self):
    return { frame: int(''.join(self.allocated_frames[frame]), 2) for frame in self.allocated_frames }
