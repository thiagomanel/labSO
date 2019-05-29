import sys

class Mapper:

    def processAddrs(self):
        out = ""
        for line in sys.stdin:
            v_addr = int(line, 16)
            if v_addr < 0:
                return out
            hw_address, frame_id, n_pagefaults = self.map(v_addr)
            out += (str(hw_address)+" "+str(frame_id)+" "+str(n_pagefaults)+"\n")
        return out

    def map(self, virtual_address)
        """ 
            Parameters
            ----------
            virtual_address : an integer that represents the virtual address to be translated

            Returns
            -------
            (hw_address, frame_id, n_pagefaults)
            where:
                hw_address: physical address translated
                frame_id: frame id index where hw_address is stored
                n_pagefaults: number of possibly page faults thrown
            
        """
        raise NotImplemented 
