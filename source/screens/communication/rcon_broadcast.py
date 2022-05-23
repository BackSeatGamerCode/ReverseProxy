import socket

import construct

import source.screens.communication.base_communication as base_communication
import source.setting as setting

MESSAGE_FORMAT = construct.GreedyRange(
    construct.Prefixed(construct.Int32sl, construct.Struct(
        "message" / construct.Int32sl, "type" / construct.Int32sl, "command" / construct.CString("utf8"),
        construct.Default(construct.CString("utf8"), "")
    ))
)


class RCONBroadcast(base_communication.BaseCommunication):
    def __init__(self, config: dict, start: bool = True):
        self.get_additional_settings("rcon_settings", [
            setting.Setting("RCON Password", "password"),
            setting.Setting("Server Host", "host", default="127.0.0.1")
        ])
        self.socket: socket.socket = None
        self.last_id = -1
        super().__init__(config, start)

    def get_next_id(self) -> int:
        self.last_id += 1
        return self.last_id

    @property
    def host(self) -> str:
        return self.additional_settings["host"]

    @property
    def password(self) -> str:
        return self.additional_settings["password"]

    def startup(self):
        self.raw_message_data = True
        self.connect()

    def sanitize(self, text: str) -> str:
        return text.replace("\"", "'")

    def send_reward(self, message: str):
        try:
            command: str = message["command"]
            if not command.startswith("/"):
                command = "/" + command

            self.send_command('/c game.print("{} redeemed the reward {}")'.format(
                self.sanitize(message["guest"]), self.sanitize(message["name"])
            ))

            resp = self.send_command(command)
            if resp != "":
                self.write_to_console(resp.rstrip("\n"))

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
                self.send_command(self.password, message_type=3)
                break

            except ConnectionRefusedError:
                result = self.alert_box(
                    "Failed to connect to TCP/IP Server at {}:{}.\n"
                    "Ensure the game is running, and press 'OK' to retry, or 'Cancel' to return to the menu".format(
                        self.host, self.port
                    ),
                    dialog_type="popup_ok_cancel"
                )

                if result in (None, "Cancel"):
                    self.return_to_menu()

    def send_command(self, command: str, message_type: int = 2) -> str:
        self.socket.sendall(MESSAGE_FORMAT.build([{
            "message": self.get_next_id(),
            "type": message_type,
            "command": command
        }]))
        return self.get_response()

    def get_response(self) -> str:
        data = b""
        while True:
            read_data = self.socket.recv(4096)
            if not read_data:
                return ""

            data += read_data
            if len(data) > 2 and data.endswith(b"\x00\x00"):
                break

        return MESSAGE_FORMAT.parse(data)[0].command
