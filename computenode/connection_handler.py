import queue
import logging

from signalrcore.hub_connection_builder import HubConnectionBuilder
from singleton import Singleton

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ConnectionHandler(metaclass=Singleton):
    def __init__(self, request_processor):
        super(ConnectionHandler, self).__init__()

        self.request_processor = request_processor
        self.server_url = "wss://localhost:44385/computeHub"

        self.connection = HubConnectionBuilder()\
            .with_url(self.server_url, options={
                "verify_ssl": False
            })\
            .configure_logging(logging.INFO)\
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 15,
                "reconnect_interval": 5,
                "max_attempts": 5
            }).build()

    def start(self):
        self.connection.on_open(lambda: logger.info("Connected!"))
        self.connection.on_close(self.handleConnectionLoss)
        self.connection.on("ReceiveMessage", print)
        self.connection.on(
            "SimpleCommand", self.request_processor.add_task)

        logger.info("SignalR connecting to: " + self.server_url)
        try:
            self.connection.start()
        except Exception:
            logger.exception("Failed to start connection")
            self.request_processor.exit()

    def handleConnectionLoss(self):
        logger.info("Disconnected!")
        self.request_processor.exit()

    def exit(self):
        self.connection.stop()
        logger.info("Connection stopped")
