class Status:
    def __init__(self):
        self.status = ""

    def update_status(self, status):
        self.status = status

    def get_status(self):
        return self.status