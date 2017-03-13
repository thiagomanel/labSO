
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

    def access(self, page_id, acc_mode):
        pass

if __name__ = "__main__":
    # Usage: python $0 num_pages num_frames algo clock

    # read workload from input file
    # read parameters
    # setup simulation
    # fire
    # collect results
    # write output

    count = 0
    fault_counter = 0
    #fire
    for load in workload:
        page_id, acc_mode = load
        fault_counter += vmemory.access(page_id, acc_mode)

    #write output
    print fault_counter
