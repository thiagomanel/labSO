import bisect

class EventStream:
    def __init__(self, event_list):
        self.events = event_list
    def next(self):
        try:
            return self.events.pop(0)
        except IndexError:
            return None
    def add(self, event):
        #_ids = []
        #for e in self.events:
        #    _ids.append(e.eid)
        #print  'add event: ' + str(event) + ' event_ids ' + str(_ids) + ' events: ' + str(len(self.events))
        bisect.insort_left(self.events, event)
    def has_next(self):
        return len(self.events) > 0
    def len(self):
        return len(self.events)

class Event(object):
    id_count = 0
    def __init__(self, event_type, timestamp, context):
        self.event_type = event_type
        self.timestamp = timestamp
        self.context = context
        self.eid = Event.id_count
        Event.id_count = Event.id_count + 1
    def __lt__(self, other):
        return self.timestamp < other.timestamp
    def __gt__(self, other):
        return self.timestamp < other.timestamp
    def __str__(self):
        return 'id: ' + str(self.eid) + ' type: ' + str(self.event_type) + ' stamp: ' + str(self.timestamp) + ' context: ' + str(self.context)
    def get_type(self):
        return self.event_type
    def get_timestamp(self):
        return self.timestamp
    def get_context(self):
        return self.context
