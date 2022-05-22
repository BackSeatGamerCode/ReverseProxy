import requests
from flask import Flask, request
import threading
import source.data_structs.queue as queue

import source.screens.communication.base_communication as base_communication


class HTTPListen(base_communication.BaseCommunication):
    def __init__(self, config: dict, start: bool = True):
        self.app: Flask = None
        self.connection_listener: threading.Thread = None
        self.q = queue.Queue()

        super().__init__(config, start)

    def startup(self):
        self.app = Flask(__name__, template_folder=None, static_folder=None)

        @self.app.route("/")
        def index():
            try:
                return self.q.pop().decode("utf8")
            except IndexError:
                return ""

        @self.app.route("/kill")
        def kill():
            print("SHUTTING DOWN INTERNAL SERVER...")

            func = request.environ.get('werkzeug.server.shutdown')
            if func is not None:
                func()

            return "killed"

        self.connection_listener = threading.Thread(
            target=self.app.run, args=("0.0.0.0", self.port), daemon=True, name="HTTP Server"
        )
        self.connection_listener.start()

    def send_reward(self, message: str):
        self.q.push(message.encode("utf-8"))

    def teardown(self):
        try:
            requests.get("http://{}:{}/kill".format("127.0.0.1", self.port))
        except requests.exceptions.ConnectionError:
            pass
