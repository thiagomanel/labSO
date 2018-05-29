QS_SIZE           = 32
TICKS_PER_SECOND  = 20
BASELINE_PRIORITY = 50

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
		_update_proc_fields(delta_t)
        pass

    def alloc_proc(self, process, delta_t):
		self._update_proc_fields(delta_t)
		"""Update the data structures to recognize a new process was created"""
		_update_proc_fields(delta_t)
        p_index_class = calculate_class(process.priority)
        self.qs[p_index_class].append(process)

    def exit(self, process_pid):
        pass

    def calculate_class(ker_priority):
        index_class = 0
        for i in xrange(0, 127, 4):
            if i <= ker_priority <= i + 3:
                return index_class
            index_class += 1


	def _update_proc_fields(self, delta_t):
		# update proc fields and reorganize the qs structure.
		temp_qs = [ [] for i in xrange(QS_SIZE)]
		for i in xrange(QS_SIZE):
			p_runnable_c = 0
			for proc in self.qs[i]:
				if proc.state = 'RUNNABLE':
                    p_runnable_c += 1

            load_average = p_runnable_c / len(self.qs[i])
			for proc in self.qs[i]:
                decay_factor = (2 * load_average)/(2 * load_average + 1)
				proc.p_cpu -= (decay_factor * delta_t) # Decrement for each second.
                if proc.state = 'RUNNING':
                    proc.p_cpu += (TICKS_PER_SECOND * delta_t) # Incrememt for each tick.

                # recalculate ker_priority.
                proc.ker_priority = BASELINE_PRIORITY + (self.p_cpu / 4) + (self.priority * 2)
                class_index = calculate_class(proc.ker_priority)
                if class_index != i:
                    temp_qs[class_index].append(proc)
                    self.qs[i].remove(proc)

        for i in xrange(QS_SIZE):
            self.qs[i].extend(temp_qs[i])
				
