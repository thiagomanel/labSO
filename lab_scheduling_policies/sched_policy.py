QS_SIZE           = 32
TICKS_PER_SECOND  = 2
BASELINE_PRIORITY = 10

class Scheduler:
    """ Scheduler Simulation
    This class aims to simulate a kernel process scheduler.
    Its implementation is similar to the described in section
    "5.4.2 - Scheduler Implementation" of the Unix Internals book.
    """
    def __init__(self):
		""" Initialize the object Scheduler.
		Create the processes classes in qs structure.
		"""
		self.qs = [ [] for i in xrange(QS_SIZE)]

    def schedule(self, out_process_pid, delta_t):
        """Return the next process to run in the cpu.

        out_process_pid -- the pid of the process that just left the cpu, or None
        in case there was no process running. The engine is responsible
        for updating the usage time.
        """
        self._update_proc_fields(delta_t)
        proc_to_alloc = None
        for class_ in self.qs:
            if class_:
                proc_to_alloc = class_.pop(0)
                class_.append(proc_to_alloc)
                return proc_to_alloc

    def alloc_proc(self, process, delta_t):
        self._update_proc_fields(delta_t)
        """Update the data structures to recognize a new process was created"""
        self._update_proc_fields(delta_t)
        p_index_class = self.calculate_class(process.priority)
        self.qs[p_index_class].append(process)

    def exit(self, process_pid):
        pass

    def calculate_class(self, ker_priority):
        index_class = 0
        for i in xrange(0, 127, 4):
            if i <= ker_priority <= i + 3:
                return index_class
            index_class += 1
        return index_class -1


    def _update_proc_fields(self, delta_t):
        # update proc fields and reorganize the qs structure.
        temp_qs = [ [] for i in xrange(QS_SIZE)]
        for i in xrange(QS_SIZE):
            p_runnable_c = 0
            to_discart = []
            for proc in self.qs[i]:
                if proc.state == 'TERMINATED':
                    to_discart.append(proc)
                if proc.state == 'RUNNABLE':
                    p_runnable_c += 1

            # Discart terminated process.
            for proc in to_discart:
                self.qs[i].remove(proc)

            load_average = (p_runnable_c / len(self.qs[i])) if len(self.qs[i]) != 0 else 0
            for proc in self.qs[i]:
                decay_factor = (2 * load_average)/(2 * load_average + 1)
                proc.p_cpu -= (decay_factor * delta_t) # Decrement for each second.
                if proc.state == 'RUNNING':
                    proc.p_cpu += (TICKS_PER_SECOND * (delta_t/2)) # Incrememt for each tick.

                # recalculate ker_priority.
                proc.ker_priority = BASELINE_PRIORITY + (proc.p_cpu / 4) + (proc.priority * 2)
                class_index = self.calculate_class(proc.ker_priority)

                # DEBUG for adjust numbers.
                # print ">> Priority: [%d] to PID [%d] " % (proc.ker_priority, proc.pid)
                # print "Class: [%d] <<" % class_index

                if class_index != i:
                    temp_qs[class_index].append(proc)
                    self.qs[i].remove(proc)

        for i in xrange(QS_SIZE):
            self.qs[i].extend(temp_qs[i])
				
