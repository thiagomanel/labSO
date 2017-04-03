import sys
from phymem import PhysicalMemory

class VirtualMemory:
    def __init__(self, npages, nframes, physicalMemory):
        #this maps page_id to an entry such as (frame_id, mapped, r, m)
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
        if mapped:
            self.phy_mem.access(frame_id, write_mode)
            self.page_table[page_id] = (frame_id, mapped, True, write_mode)
        else:
            if len(self.freeFrames) > 0:
                new_frame_id = self.freeFrames.pop()
                self.frame2page[new_frame_id] = page_id
                self.page_table[page_id] = (new_frame_id, True, True, write_mode)
                self.phy_mem.put(new_frame_id)
                self.phy_mem.access(new_frame_id, write_mode)
            else:
                evicted_frame_id = self.phy_mem.evict()
                assert type(evicted_frame_id) == int, "frameId returned by evict should be an int"
                page_id_out = self.frame2page.get(evicted_frame_id, None)
                assert page_id_out is not None, "frameId returned by evict should be allocated"

                #update page out
                self.page_table[page_id_out] = (-1, False, False, False)

                #allocate the new frame
                self.phy_mem.put(evicted_frame_id)
                #mudar mappeamento pagina in
                self.page_table[page_id] = (evicted_frame_id, True, True, write_mode)
                #update frame2page
                self.frame2page[evicted_frame_id] = page_id
                self.phy_mem.access(evicted_frame_id, write_mode)
                return 1
        return 0

if __name__ == "__main__":

    # Usage: python $0 num_pages num_frames algo clock
    num_pages = int(sys.argv[1])
    num_frames = int(sys.argv[2])
    alg = sys.argv[3]
    clock = int(sys.argv[4])

    # read workload from input file
    workload = []
    for line in sys.stdin.readlines():
        page_id, mode = line.split()
        workload.append((int(page_id), mode == "w"))

    # setup simulation
    phyMem = PhysicalMemory(alg)
    vMem = VirtualMemory(num_pages, num_frames, phyMem)

    # fire
    count = 0
    fault_counter = 0
    for load in workload:
        # call we fired clock (say, clock equals to 100) times, we tell the physical_mem to react to a clock event
        if count % clock == 0:
            phyMem.clock()
        count += 1
        page_id, acc_mode = load
        fault_counter += vMem.access(page_id, acc_mode)

    #TODO
    # collect results
    # write output
    print fault_counter, " ".join(sys.argv[1:])
