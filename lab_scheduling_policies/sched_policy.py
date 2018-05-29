QS_SIZE = 32

class Scheduler:
	""" Scheduler Simulation
	This class aims to simulate a kernel process scheduler.
	Its implementation is similar to the described in section
	"5.4.2 - Scheduler Implementation" of the Unix Internals book.
	"""
    def __init__(self):
		""" Initialize the object Scheduler.
		Create the processes classes in qs structure.
		Start whichqs with zeros.
		"""
		self.qs = [ [] for i in xrange(QS_SIZE)]
		self.whichqs = [0 for i in xrange(QS_SIZE)]

    def schedule(self, out_process_pid, previous_t, current_t):
		"""Return the next process to run in the cpu.

		out_process_pid -- the pid of the process that just left the cpu, or None
		in case there was no process running. The engine is responsible
		for updating the usage time.
		"""
		pass

    def alloc_proc(self, process, previous_t, current_t):
		"""Update the data structures to recognize a new process was created"""
		pass

    def exit(self, process_pid):
        pass

	def _update_proc_fields(self, previous_t, current_t):
		# update proc fields and reorganize the qs structure.
		pass
