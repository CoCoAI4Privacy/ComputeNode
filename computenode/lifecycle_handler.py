import logging
import threading
import connection_handler
import request_processor
import task_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Lifecycle:
    def __init__(self, *argv):
        # Initialisation
        if "requests" in argv or "all" in argv:
            logger.info("Initializing RequestProcessor")
            self.requests = request_processor.RequestProcessor()
            self.thread_requests = threading.Thread(
                target=self.requests.start_loop)
        if "connection" in argv or "all" in argv:
            logger.info("Initializing ConnectionHandler")
            self.connection = connection_handler.ConnectionHandler(
                self.requests)

        # Setup callbacks
        if "connection" in argv and "requests" in argv:
            self.requests.add_on_exit(self.exit)

    def start(self, *argv):
        # Start threads
        if "requests" in argv or "all" in argv:
            logger.info("Starting request thread")
            self.thread_requests.start()
        if "connection" in argv or "all" in argv:
            logger.info("Starting connection thread")
            self.connection.start()

    def exit(self):
        try:
            self.requests.task_exit([])
        except Exception:
            logger.warning("Unable to shut down requests")

        try:
            self.connection.exit()
        except Exception:
            logger.warning("Unable to shut down connection")

        self.wait_for_exit()

    def wait_for_exit(self):
        # Join threads
        self.thread_requests.join()
