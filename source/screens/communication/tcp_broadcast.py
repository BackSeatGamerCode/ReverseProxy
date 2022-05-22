import socket

import source.screens.communication.base_communication as base_communication


class TCPBroadcast(base_communication.BaseCommunication):
    def __init__(self, config: dict, start: bool = True):
        self.socket: socket.socket = None
        super().__init__(config, start)

    def startup(self):
        self.connect()

    def send_reward(self, message: str):
        try:
            self.socket.sendall(message.encode("utf8"))
            self.socket.recv(1024)
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

        while True:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                self.socket.connect((self.host, self.port))
                break

            except ConnectionRefusedError:
                self.alert_box(
                    "Failed to connect to TCP/IP Server at {}:{}.\n"
                    "Ensure the game is running, and press 'OK' to retry".format(
                        self.host, self.port
                    )
                )
