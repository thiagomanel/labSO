from sys import stderr
from process import Process

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

def schedule(out_process_pid):
    #plugin method
    """Return the next process to run in the cpu.

    out_process_pid -- the pid of the process that just left the cpu, or None
                in case there was no process running. The engine is responsible
                for updating the usage time.
    """
    pass

def run_simulation(events):

    def next_event():
        try:
            return events.pop(0)
        except IndexError:
            return None

    def take_cpu():
        pid = None
        if running_process:
            pid = runing_process.get_pid()
        running_process = None
        return pid

    def enter_cpu(process):
        running_process = process

    def build_process(event_context):
        pass

    def remaining_service_time(process):
        return process.get_service_t() - process.get_usage_t()

    def update_clock(current_t):
        pass

    def now():
        pass

    running_process = None
    before = now()

    #oh, boy! stop worring and love non-OO code
    event = next_event()
    while(event):
        #oh, boy! stop worring and love non-OO code
        e_type, timestamp, context = event

        if (e_type == event_types.SCHEDULE):
            #remove process from cpu
            pid = take_cpu()
            #call the plugin hook
            process_to_enter = schedule(pid)

            if (process_to_enter):
                if (remaining_service_time(process_to_enter)
                        < slice_interval):
                    #we should add a EXIT event
                    pass
                else:
                    pass
        elif (e_type == event_types.ALLOC_PROC):
            new_process = build_process(context)
            #call the pluging hook
            alloc_proc(new_process)

def enum(**enums):
    return type('Enum', (), enums)

event_types = enum(ALLOC_PROC=1, EXIT_PROC=2, SCHEDULE=3)

def alloc_proc_events(processes):
    events = []
    for proc in processes:
        event = (event_types.ALLOC_PROC, proc.get_timestamp(), proc)
        events.append(event)
    return events

if __name__ == '__main__':
    #read the args
    #read workload file in the standard directory
    #parse the workload file
    wlp = WorkloadParser()
    ordered_process_list = wlp.parse('workload_file.ffd')
    events = alloc_proc_events(ordered_process_list)

    #TODO:
    #run the simulator config
        #interrupt interval
        #tick time

    #pass the arg to run_simulation
    #get the return values from run_simulation
    #generate the raw output to the standard output
    output = run_simulation(events)
    for out_sample in output:
        print out_sample
