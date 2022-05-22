import socket

import source.screens.communication.base_communication as base_communication


class UDPBroadcast(base_communication.BaseCommunication):
    def __init__(self, config: dict, start: bool = True):
        self.socket: socket.socket = None
        super().__init__(config, start)

    def startup(self):
        self.connect()

    def send_reward(self, message: str):
        try:
            self.socket.sendto(message.encode("utf8"), (self.host, self.port))
        except ConnectionError:

            self.connect()
            self.send_reward(message)

    def teardown(self):
        self.socket.close()

    def connect(self):
        try:
            self.socket.close()
        except Exception:
            pass

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
