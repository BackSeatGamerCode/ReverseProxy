import socket
import threading
import source.data_structs.queue as queue

import source.screens.communication.base_communication as base_communication


class TCPListen(base_communication.BaseCommunication):
    def __init__(self, config: dict, start: bool = True):
        self.socket: socket.socket = None
        self.connection_listener: threading.Thread = None
        self.queues = {}

        super().__init__(config, start)

    def startup(self):
        self.connect()

    def send_reward(self, message: str):
        for q in self.queues.values():
            q.push(message.encode("utf-8"))

    def teardown(self):
        self.socket.close()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", self.port))
        self.socket.listen()

        self.connection_listener = threading.Thread(target=self.listen_for_connections, daemon=True, name="TCP Conn")
        self.connection_listener.start()

    def listen_for_connections(self):
        while self._running:
            try:
                sock, addr = self.socket.accept()
                threading.Thread(
                    target=self.new_connection, args=(sock, addr), daemon=True, name="TCP Listen {}".format(addr)
                ).start()
                self.write_to_console("Received TCP/IP Connection From {}:{}".format(*addr))

                self.queues[addr] = queue.Queue()

            except OSError:
                break

    def new_connection(self, sock, addr):
        while self._running:
            try:
                sock.recv(1024)
                if not self.queues[addr].is_empty():
                    sock.send(self.queues[addr].pop())

                else:
                    sock.send("null".encode("utf8"))

            except ConnectionAbortedError:
                self.write_to_console("Lost TCP/IP Connection From {}:{}".format(*addr))
                del self.queues[addr]

                break
