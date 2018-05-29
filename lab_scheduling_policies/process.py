class Process(object):
    def __init__(self, timestamp, pid, priority, service_t):
        self.timestamp = timestamp
        self.pid = pid
        self.state = 'RUNNABLE'
        self.priority = priority
        self.ker_priority = priority
        self.service_t = service_t
        self.usage_t = 0
        self.p_cpu = 0

    def get_timestamp(self):
        return self.timestamp

    def get_pid(self):
        return self.pid

    def get_state(self):
        return self.state

    def set_st_runnable(self):
        self.state = 'RUNNABLE'

    def set_st_running(self):
        self.state = 'RUNNING'

    def set_st_terminated(self):
        self.state = 'TERMINATED'

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