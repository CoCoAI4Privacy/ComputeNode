from queue import Queue
from loop_module import LoopModule


class TaskHandler(LoopModule):
    def __init__(self, task_processor):
        super(TaskHandler, self).__init__()

        self.on_exit_callbacks = []
        self.task_processor = task_processor
        self.tasks = Queue()

    def add_task(self, task):
        self.tasks.put(task)

    def loop_body(self):
        task = self.tasks.get()
        self.task_processor(task)

    def on_exit(self):
        self.tasks.put("")
        for callback in self.on_exit_callbacks:
            callback()

    # Callbacks
    def add_on_exit(self, callback):
        if callable(callback):
            self.on_exit_callbacks.append(callback)
        else:
            print("The callback:", callback, "is not callable")
