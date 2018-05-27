from sys import stderr
from process import Process
from sched_policy import Scheduler
import bisect

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

def run_simulation(events):

    class Clock:
        current_time = 0
        @classmethod
        def now(cls):
            return Clock.current_time

    class CPU:
        def __init__(self):
            self.running_proc = None

        def take_cpu(self):
            pid = None
            if self.running_proc:
                pid = self.runing_proc.get_pid()
            self.running_proc = None
            return pid

        def enter_cpu(self, process):
            self.running_proc = process

    def next_event():
        try:
            return events.pop(0)
        except IndexError:
            return None

    def add_event(event):
        bisect.insort_left(events, event)

    def has_next_event():
        return len(events) > 0

    def remaining_service_time(process):
        return process.get_service_t() - process.get_usage_t()

    cpu = CPU()
    scheduler = Scheduler()

    output = []

    while True:
        event = next_event()
        if (not event): break
        Clock.current_time = event.get_timestamp()

        if (event.get_type() == event_types.SCHEDULE):
            #remove current process
            pid = cpu.take_cpu()
            if (pid):
                #plugin hook
                process_to_enter = scheduler.schedule(pid)
                if (process_to_enter):
                    if (remaining_service_time(process_to_enter)
                            < slice_interval):
                        #TODO:we should add a EXIT event
                        pass
                    else:
                        cpu.enter(process_to_enter)
            if (has_next_event()):
                #if we were not done yet, add the next SCHEDULE event
                add_event(Event(event_types.SCHEDULE, Clock.now() + SLICE_DURATION, None))

        elif (event.get_type() == event_types.ALLOC_PROC):
            new_process = event.get_context()
            #plugin hook
            scheduler.alloc_proc(new_process)

    return output

def enum(**enums):
    return type('Enum', (), enums)
event_types = enum(ALLOC_PROC=1, EXIT_PROC=2, SCHEDULE=3)

class Event(object):
    def __init__(self, event_type, timestamp, context):
        self.event_type = event_type
        self.timestamp = timestamp
        self.context = context
    def __lt__(self, other):
        return self.timestamp < other.timestamp
    def __gt__(self, other):
        return self.timestamp < other.timestamp
    def __str__(self):
        return 'type: ' + str(self.event_type) + ' stamp: ' + str(self.timestamp) + ' context: ' + str(self.context)
    def get_type(self):
        return self.event_type
    def get_timestamp(self):
        return self.timestamp
    def get_context(self):
        return self.context

SLICE_DURATION = 20

if __name__ == '__main__':
    #read workload file in the standard directory
    wlp = WorkloadParser()
    ordered_process_list = wlp.parse('workload_file.ffd')
    events = [Event(event_types.ALLOC_PROC, proc.get_timestamp(), proc)
                for proc in ordered_process_list]

    #add an schedule event to proper fire the engine
    events.insert(0, Event(event_types.SCHEDULE, 0, None))

    #fire
    output = run_simulation(events)
    for out_sample in output:
        print out_sample
