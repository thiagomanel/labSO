import sys

class Mapper:

    def processAddrs(self):
        for line in sys.stdin:
            v_addr = int(line, 16)
            if v_addr < 0:
                return
            address, n_page_faults = self.map(v_addr)
            sys.stdout.write(str(address)+" "+str(n_page_faults)+"\n")

    def map(self, addr):
        return (addr, 0)
