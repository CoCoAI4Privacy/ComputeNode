import logging

import connection_handler
from task_handler import TaskHandler
from singleton import Singleton
from data_pipeline.data_pipeline import DataPipeline

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RequestProcessor(TaskHandler, metaclass=Singleton):
    def __init__(self):
        super(RequestProcessor, self).__init__(self.request_processor)
        self.connection = connection_handler.ConnectionHandler(self)
        self.pipeline = DataPipeline()

        self.handle_cmd = {
            "": print,
            "exit": self.task_exit,
            "process": self.task_process,
            "print": print
        }

    def request_processor(self, args: list):
        if len(args) < 1:
            return

        args = args[0]
        logger.info("Received command: " + str(args))

        self.handle_cmd[args[0]](args[1:])

    def task_exit(self, remainder: list = []):
        logger.debug("Exit was called")
        self.exit()

    def task_process(self, remainder: list = []):
        if not self._check_args(remainder, 1, 1):
            return
        result = self.pipeline.process_url(remainder[0])
        if result == None:
            self._print(
                "Node", 4, "An error occurred while processing the url: " + remainder[0])
        else:
            with open("../data/html.txt", "w+") as f:
                f.write(result[0])
            with open("../data/text.txt", "w+") as f:
                f.write(result[1])
            with open("../data/segments.txt", "a+") as f:
                for segment in result[2]:
                    f.write("\n----------------------------------\n")
                    f.write(segment)
            with open("../data/vectors.txt", "a+") as f:
                for segment in result[3]:
                    f.write("\n----------------------------------\n")
                    f.write(str(segment))
            with open("../data/graphs.txt", "a+") as f:
                for graph in result[4]:
                    f.write("\n----------------------------------\n")
                    f.write(str(graph.get_features()))
            self._print(
                "Node", 3, result[1][:1000])

    def _print(self, tag: str, severity: int, message: str):
        self.connection.connection.send(
            "ToConsole", [tag, severity, message])

    def _check_args(self, remainder: list, minimum=0, maximum=0):
        length = len(remainder)
        if length < minimum:
            logger.info("Received too few arguments! Expected " +
                        str(minimum) + " or more, received:", length)
            return False
        elif length > maximum:
            logger.info("Received too many arguments! Expected " +
                        str(minimum) + " or less, received:", length)
            return False

        return True
