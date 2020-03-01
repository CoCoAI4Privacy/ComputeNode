import threading
import connection_handler
import data_pipeline
import request_processor
import task_handler


class Lifecycle:
    def __init__(self, *argv):
        print(argv)
        # Initialisation
        if "requests" in argv or "all" in argv:
            print("Initializing RequestProcessor")
            self.requests = request_processor.RequestProcessor()
            self.thread_requests = threading.Thread(
                target=self.requests.start_loop)
        if "connection" in argv or "all" in argv:
            print("Initializing ConnectionHandler")
            self.connection = connection_handler.ConnectionHandler(
                self.requests)
        if "pipeline" in argv or "all" in argv:
            print("Initializing DataPipeline")
            self.pipeline = data_pipeline.DataPipeline()

        # Setup callbacks
        if "connection" in argv and "requests" in argv:
            self.requests.add_on_exit(self.connection.exit)

    def start(self, *argv):
        # Start threads
        if "requests" in argv or "all" in argv:
            print("Starting request thread")
            self.thread_requests.start()
        if "connection" in argv or "all" in argv:
            print("Starting connection thread")
            self.connection.start()

    def wait_for_exit(self):
        # Join threads
        self.thread_requests.join()
        print("Task thread stopped")
