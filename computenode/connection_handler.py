import queue
import logging

from signalrcore.hub_connection_builder import HubConnectionBuilder
from singleton import Singleton


class ConnectionHandler(metaclass=Singleton):
    def __init__(self, request_processor):
        super(ConnectionHandler, self).__init__()

        self.request_processor = request_processor
        self.server_url = "wss://localhost:44385/computeHub"

        self.connection = HubConnectionBuilder()\
            .with_url(self.server_url, options={
                "verify_ssl": False
            })\
            .configure_logging(logging.DEBUG)\
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 15,
                "reconnect_interval": 5,
                "max_attempts": 5
            }).build()

    def start(self):
        self.connection.on_open(lambda: print("Connected!"))
        self.connection.on_close(lambda: print("Disconnected!"))
        self.connection.on("ReceiveMessage", print)
        self.connection.on(
            "SimpleCommand", self.request_processor.add_task)

        print("SignalR connecting to:", self.server_url)
        self.connection.start()

    def exit(self):
        self.connection.stop()
        print("Connection stopped")
