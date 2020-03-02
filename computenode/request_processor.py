from task_handler import TaskHandler
import connection_handler
from singleton import Singleton


class RequestProcessor(TaskHandler, metaclass=Singleton):
    def __init__(self):
        super(RequestProcessor, self).__init__(self.request_processor)
        self.connection = connection_handler.ConnectionHandler(self)

        self.handle_cmd = {
            "": print,
            "exit": self.task_exit,
            "process": self.task_process
        }

    def request_processor(self, args: list):
        args = args[0]
        print("Received command:", args)

        self.handle_cmd[args[0]](args[1:])

    def task_exit(self, remainder: list):
        print("Exit task")
        self.connection.exit()
        self.exit()

    def task_process(self, remainder: list):
        if not self._check_args(remainder, 1, 5):
            return

    def _print(self, tag: str, severity: int, message: str):
        self.connection.connection.send(
            "ToConsole", [tag, severity, message])

    def _check_args(self, remainder: list, minimum=0, maximum=0):
        length = len(remainder)
        if length < minimum:
            print("Received too few arguments! Expected " +
                  str(minimum) + " or more, received:", length)
            return False
        elif length > maximum:
            print("Received too many arguments! Expected " +
                  str(minimum) + " or less, received:", length)
            return False

        return True
