class Process(object):
    def __init__(self, timestamp, pid, priority, service_t):
        self.timestamp = timestamp
        self.pid = pid
        self.priority = priority
        self.service_t = service_t
        self.usage_t = 0
        self.p_cpu = 0

    def get_timestamp(self):
        return self.timestamp

    def get_pid(self):
        return self.pid

    def get_priority(self):
        return self.priority

    def get_service_t(self):
        return self.service_t

    def set_usage_t(self, usage):
        self.usage_t = usage

    def get_usage_t(self):
        return self.usage_t

    def get_p_cpu(self):
        return self.p_cpu

    def set_p_cpu(self, p_cpu):
        self.p_cpu = p_cpu

    def __repr__(self):
        return str(self.__dict__)
