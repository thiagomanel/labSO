class Scheduler:
    def __init__(self):
	pass
    def schedule(self, out_process_pid):
 	"""Return the next process to run in the cpu.

	out_process_pid -- the pid of the process that just left the cpu, or None
	in case there was no process running. The engine is responsible
 	for updating the usage time.
 	"""
	pass

    def alloc_proc(self, process):
	"""Update the data structures to recognize a new process was created"""
	pass

