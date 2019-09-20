
class VirtualMemory:
    def __init__(self, npages, nframes, physicalMemory):
        #this maps page_id to an entry such as (frame_id, mapped, (r)eaded, (m)odified)
        self.page_table = {}
        self.phy_mem = physicalMemory
        self.__build_page_table__(npages)
        self.frame_counter = 0
        self.nframes = nframes
        self.frame2page = {}
        self.freeFrames = set(range(nframes))

    def __build_page_table__(self, npages):
        for i in range(npages):
            frame_id = -1
            mapped = False
            r = False
            m = False
            self.page_table[i] = (-1, mapped, r, m)

    def access(self, page_id, write_mode):
        (frame_id, mapped, r, m) = self.page_table[page_id]
        if mapped: #That page is in the physical memory
            self.phy_mem.access(frame_id, write_mode)
            self.page_table[page_id] = (frame_id, mapped, True, write_mode)
        else: #The page is not in the physical memory
            if len(self.freeFrames) > 0: #There is frame that dont have a page in it
                new_frame_id = self.freeFrames.pop()
                self.frame2page[new_frame_id] = page_id
                self.page_table[page_id] = (new_frame_id, True, True, write_mode)
                self.phy_mem.put(new_frame_id)
                self.phy_mem.access(new_frame_id, write_mode)
            else: #All the frames are occupieds, i will need to evict a page in a frame to insert the new page
                evicted_frame_id = self.phy_mem.evict()
                assert type(evicted_frame_id) == int, "frameId returned by evict should be an int"
                page_id_out = self.frame2page.get(evicted_frame_id, None)
                assert page_id_out is not None, "frameId returned by evict should be allocated"

                #Update page out
                self.page_table[page_id_out] = (-1, False, False, False)

                #Allocate the new frame
                self.phy_mem.put(evicted_frame_id)
                #mudar mappeamento pagina in
                self.page_table[page_id] = (evicted_frame_id, True, True, write_mode)
                #Update frame2page
                self.frame2page[evicted_frame_id] = page_id
                self.phy_mem.access(evicted_frame_id, write_mode)
                return 1
        return 0