class PhysicalMemory:
    def

class VirtualMemory:
    def __init__(self):
        #this maps page_id to an entry such as (frame_id, mapped, r, m)
        page_table = {}

    def access(self, page_id, acc_mode):
        pass

if __name__ = "__main__":
    # read workload from input file
    # read parameters: virtual size, physical size, page_replacement_alg, clock
    # setup simulation
    # fire
    # collect results
    # write std out
    count = 0
    fault_counter = 0
    for load in workload:
        page_id, acc_mode = load
        fault_counter += vmemory.access(page_id, acc_mode)
