class IDGenerator:
    def __init__(self):
        self.id = -1

    def get_id(self):
        self.id += 1
        return self.id
