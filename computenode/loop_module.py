class LoopModule:
    def __init__(self):
        self.status = ""
        self.exit_loop = False

    # Loop
    def loop_body(self):
        raise NotImplementedError

    def start_loop(self):
        try:
            while not self.exit_loop:
                    self.loop_body()
        except Exception as e:
            print(e)
            self.exit()


    def exit(self):
        self.on_exit()
        self.exit_loop = True

    def on_exit(self):
        pass

    # Status
    def update_status(self, status):
        self.status = status

    def get_status(self):
        return self.status
