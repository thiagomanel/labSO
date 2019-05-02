class Frame:
    def __init__(self, frame_id):
        self.frame_id = frame_id
        self.referenced = False
        self.modified = False
        self.access_counter = 0

    def get_id(self):
        return self.frame_id

    def is_referenced(self):
        return self.referenced


    def set_referenced(self, referenced):
        self.referenced = referenced


    def is_modified(self):
        return self.modified


    def set_modified(self, modified):
        self.modified = modified


    def get_access_counter(self):
        return self.access_counter


    def set_access_counter(self, access_counter):
        self.access_counter = access_counter


    def increment_access_counter(self):
        self.access_counter += 1
    

    def __eq__(self, other):
        return self.frame_id == other.frame_id


    def __hash__(self):
        return hash(self.frame_id)