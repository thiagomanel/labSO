import sys
from physical_memory import PhysicalMemory
from virtual_memory import VirtualMemory


class Simulation():

    def __init__(self, alg_name, num_pages, num_frames, clock):
        self.workload = self.setup_workload()
        self.alg_name = alg_name
        self.num_pages = num_pages
        self.num_frames = num_frames
        self.clock = clock
        self.setup_simulation()


    def setup_workload(self):
        # read workload from input file
        workload = []
        for line in sys.stdin.readlines():
            page_id, mode = line.split()
            workload.append((int(page_id), mode == "w"))
        return workload

    def setup_simulation(self):
        self.phyMem = PhysicalMemory(self.alg_name)
        self.vMem = VirtualMemory(self.num_pages, self.num_frames, self.phyMem)

    def run_simulation(self):
        count = 0
        fault_counter = 0
        for load in self.workload:
            # call we fired clock (say, clock equals to 100) times, we tell the physical_mem to react to a clock event
            if (count % self.clock) == 0:
                self.phyMem.clock()
            count += 1
            page_id, acc_mode = load
            fault_counter += self.vMem.access(page_id, acc_mode)

        #TODO
        # collect results
        # write output
        print(fault_counter, " ".join(sys.argv[1:]))

if __name__ == "__main__":
    print(sys.argv)
    # Usage: python $0 num_pages num_frames algo clock
    num_pages = int(sys.argv[1])
    num_frames = int(sys.argv[2])
    alg_name = sys.argv[3]
    clock = int(sys.argv[4])

    Simulation(alg_name, num_pages, num_frames, clock).run_simulation()