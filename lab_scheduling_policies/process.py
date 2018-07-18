class Process(object):

    RUNNABLE = 0
    RUNNING = 1
    TERMINATED = 2
    CLOSED = 3

    def __init__(self, timestamp, pid, priority, service_t):
        self.timestamp = timestamp
        self.pid = pid
        self.state = Process.RUNNABLE
        self.priority = priority
        self.ker_priority = priority
        self.service_t = service_t
        self.usage_t = 0
        self.p_cpu = 0
        self.creation_t = -1
        self.exit_t = -1

    def get_creation_t(self):
        return self.creation_t

    def set_creation_t(self, stamp):
        self.creation_t = stamp

    def get_exit_t(self):
        return self.exit_t

    def set_exit_t(self, stamp):
        self.exit_t = stamp

    def get_timestamp(self):
        return self.timestamp

    def get_pid(self):
        return self.pid

    def get_state(self):
        return self.state

    def set_state(self, state):
        assert state in [Process.RUNNABLE, Process.RUNNING, Process.TERMINATED, Process.CLOSED]
        self.state = state

    def get_priority(self):
        return self.priority

    def get_service_t(self):
        return self.service_t

    def set_usage_t(self, usage):
        self.usage_t = usage

    def get_usage_t(self):
        return self.usage_t

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)
