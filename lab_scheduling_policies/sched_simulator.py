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

def run_simulation(event_stream):

    class Clock:
        current_time = 0
        @classmethod
        def now(cls):
            return Clock.current_time

    class CPU:
        def __init__(self):
            self.running_proc = None
        def take_cpu(self):
            taken = self.running_proc
            if taken:
                taken.set_st_runnable()
            self.running_proc = None
            return taken
        def enter_cpu(self, process):
            self.running_proc = process
            self.running_proc.set_st_running()

    def update_usage_t(proc, usage_interval):
        previous_usage_t = proc.get_usage_t()
        proc.set_usage_t(previous_usage_t + usage_interval)

    def process_is_done(proc):
        return proc.get_service_t() == proc.get_usage_t

    def sched(out_proc, previous_t, current_t):

        out_pid = None
        if (out_proc):
            out_pid = out_proc.get_pid()

        in_proc = scheduler.schedule(out_pid, current_t - previous_t)
        if (in_proc):
            cpu.enter_cpu(in_proc)
            remaining_t = in_proc.get_service_t() - in_proc.get_usage_t()
            if (remaining_t < slice_interval):
                exit_timestamp = Clock.now() + remaining_t
                event_stream.add(Event(event_types.EXIT, exit_timestamp, in_proc))
            else:
                #we were not done yet, then add a new SCHEDULE event
                if (event_stream.has_next()):
                    schedule_timestamp = Clock.now() + SLICE_DURATION
                    event_stream.add(Event(event_types.SCHEDULE, schedule_timestamp, None))

    cpu = CPU()
    scheduler = Scheduler()

    #{pid:  (creation_t, service_t, usage_t, exit_t)}
    output = {}

    while True:
        event = event_stream.next()
        if (not event): break

        previous_t = Clock.current_time
        Clock.current_time = event.get_timestamp()

        if (event.get_type() == event_types.SCHEDULE):
            taken_proc = cpu.take_cpu()
            if (taken_proc):
                update_usage_t(taken_proc, now() - previous_t)
                if process_is_done(taken_proc):
                    taken_proc.set_st_terminated()

            sched(taken_proc, previous_t, Clock.now())
        elif (event.get_type() == event_types.ALLOC_PROC):
            new_proc = event.get_context()

            #update simulation stats
            output[new_proc.get_pid()] = (Clock.now(), new_proc.get_service_t(),
                                            new_proc.get_usage_t(), -1)
            scheduler.alloc_proc(new_proc, Clock.now() - previous_t)
        elif (event.get_type() == event_types.EXIT_PROC):
            exit_proc = event.get_context()
            exit_pid = exit_proc.get_pid()
            update_usage_t(exit_proc, now() - previous_t)

            #update simulation stats
            (creation_t, service_t, usage_t, exit_t) = output[exit_pid]
            output[exit_pid] = (creation_t, service_t, new_proc.get_usage_t(),
                                Clock.now())

            exit_pid = exit_proc.get_pid()
            scheduler.exit(exit_pid)
            sched(exit_proc)

    return output

def enum(**enums):
    return type('Enum', (), enums)
event_types = enum(ALLOC_PROC=1, EXIT_PROC=2, SCHEDULE=3)

class EventStream:
    def __init__(self, event_list):
        self.events = event_list
    def next(self):
        try:
            return self.events.pop(0)
        except IndexError:
            return None
    def add(self, event):
        bisect.insort_left(self.events, event)
    def has_next(self):
        return len(self.events) > 0

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
    output = run_simulation(EventStream(events))
    for pid, stat in output.iteritems():
        print pid, stat
