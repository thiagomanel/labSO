from sys import stderr

class Process(object):
    def __init__(self, timestamp, pid, priority, service_t):
        #FIXME: add usage time to be updated by the engine
        self.timestamp = timestamp
        self.pid = pid
        self.priority = priority
        self.service_t = service_t

    def get_timestamp(self):
        return self.timestamp

    def get_pid(self):
        return self.pid

    def get_priority(self):
        return self.priority

    def get_service_t(self):
        return self.service_t

    def __repr__(self):
        return str(self.__dict__)


class WorkloadParser(object):
    def parse(self, filename):
        file_lines = []
        try:
            with open(filename, 'r') as wk_load_file:
                file_lines = wk_load_file.readlines()
        except IOError:
            stderr.write('Unable to read workload file!\n')
        proc_list = []
        for line in file_lines:
            timestamp, pid, priority, service_t = map(int, line.split())
            proc_list.append(Process(timestamp, pid, priority, service_t))
        return proc_list

def now():
    #to be implemented - engine method
    """Return the current logical timestamp"""
    pass

def alloc_proc(process):
    #plugin method
    """Update the data structures to recognize a new process was created"""
    pass

def schedule(out_process):
    #plugin method
    """Return the next process to run in the cpu.

    out_process -- the process that just left the cpu, or None in case there
                was no process running. The engine is responsible for updating
                the usage time.
    """
    pass

ordered_process_list = []

def run_simulation():

    def enum(**enums):
        return type('Enum', (), enums)

    event_types = (ALLOC_PROC=1, EXIT_PROC=2, SCHEDULE=3)

    def next_event():
        pass

    #oh, boy! stop worring and love non-OO code

    #get the next event
    event = next_event()
    while(event):
        e_type, timestamp, context = event
        #check its type
        #call the handler associated witht the type
        if (e_type == event_types.SCHEDULE):
            #remove process from cpu
            #call schedule hook
            #check process to enter cpu is not None
            #   check service time and usage time
            #   verify (service_time - usage_time) < slice_interval
            #       add EXIT_PROC event
        elif (e_type == event_tyeps.ALLOC_PROC):
            #parse context and create the process object
            #call the pluging hook

if __name__ == '__main__':
    wlp = WorkloadParser()
    ordered_process_list = wlp.parse('workload_file.ffd')

#read the args
    #read workload file in the standard directory
    #run the simulator config
        #interrupt interval
        #tick time
#parse the workload file
#pass the arg to run_simulation
#get the return values from run_simulation
#generate the raw output to the standard output