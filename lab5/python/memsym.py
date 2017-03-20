import sys

class VirtualMemory:
    def __init__(self, npages, physical_mem):
        #this maps page_id to an entry such as (frame_id, mapped, r, m)
        self.page_table = {}
        self.phy_mem = physical_mem
        self.__build_page_table__(npages)

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
            # need to create a new map between virtual and physical
            # need to evict a page from physical if there is no room for it

if __name__ = "__main__":
    # Usage: python $0 num_pages num_frames algo clock


    # read workload from input file
    for line in sys.stdin.readlines():
        page_id,
    # read parameters
    # setup simulation
    # fire
    # collect results
    # write output

    count = 0
    fault_counter = 0
    #fire
    for load in workload:
        # call we fired clock (say, clock equals to 100) times, we tell the physical_mem to react to a clock event
        if count % clock:
            phy_mem.clock()

        page_id, acc_mode = load
        fault_counter += vmemory.access(page_id, acc_mode)

    #write output
    print fault_counter
