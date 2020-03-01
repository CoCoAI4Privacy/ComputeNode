from task_handler import TaskHandler
import connection_handler
import data_pipeline
from singleton import Singleton
from importlib import reload


class RequestProcessor(TaskHandler, metaclass=Singleton):
    def __init__(self):
        super(RequestProcessor, self).__init__(self.request_processor)
        self.connection = connection_handler.ConnectionHandler(self)
        self.pipeline = data_pipeline.DataPipeline()

        self.handle_cmd = {
            "": print,
            "exit": self.task_exit,
            "process": self.task_process,
            "reload": self.task_reload
        }

    def request_processor(self, args: list):
        args = args[0]
        print("Received command:", args)

        self.handle_cmd[args[0]](args[1:])

    def task_exit(self, remainder: list):
        print("Exit task")
        self.connection.exit()
        self.pipeline.close()
        self.exit()

    def task_process(self, remainder: list):
        if not self._check_args(remainder, 1, 5):
            return

        html, clean_text, segments, vector_segments = self.pipeline.process_url(
            remainder[0])

        if "html" in remainder:
            self._print("Result", 2, html)
        if "text" in remainder:
            self._print("Result", 2, clean_text)
        if "segments" in remainder:
            self._print("Result", 2, segments)
        if "vectors" in remainder:
            self._print("Result", 2, vector_segments)

    def task_reload(self, remainder: list):
        if not self._check_args(remainder, 1, 1):
            return

        if "pipeline" in remainder:
            print("Reloading data_pipeline")
            self.pipeline.close()
            reload(data_pipeline)
            self.pipeline = data_pipeline.DataPipeline()
            print("data_pipeline reloaded")

        if "connection" in remainder:
            print("Reloading connection_handler")
            self.connection.exit()
            reload(connection_handler)
            self.connection = connection_handler.ConnectionHandler(self)
            print("connection_handler reloaded")

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
