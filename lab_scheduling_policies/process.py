class Process(object):
    def __init__(self, timestamp, pid, priority, service_t):
        #FIXME: add usage time to be updated by the engine
        self.timestamp = timestamp
        self.pid = pid
        self.priority = priority
        self.service_t = service_t
        selg.usage_t = 0

    def get_timestamp(self):
        return self.timestamp

    def get_pid(self):
        return self.pid

    def get_priority(self):
        return self.priority

    def get_service_t(self):
        return self.service_t

    def usage_time(self):
        return self.usage_t

    def set_usage_t(self, usage):
        pass

    def get_usage_t(self):
        pass

    def __repr__(self):
        return str(self.__dict__)
