import requests

import source.screens.communication.base_communication as base_communication
import source.setting as setting


class HTTPBroadcast(base_communication.BaseCommunication):
    def startup(self):
        self.get_additional_settings("http_broadcast_settings", [
            setting.Setting("Endpoint", "endpoint", default="/"),
            setting.Setting(
                "Method", "method", default="POST", allowed_values=["GET", "POST", "PUT", "PATCH", "DELETE"],
                input_type="dropdown"
            )
        ])

    @property
    def method(self) -> str:
        return self.additional_settings["method"]

    @property
    def endpoint(self) -> str:
        return self.additional_settings["endpoint"].replace("\\", "/")

    def get_url(self) -> str:
        return "http://{}:{}{}".format(
            self.host, self.port, ("/" + self.endpoint) if not self.endpoint.startswith("/") else self.endpoint,
        )

    def send_reward(self, message: str):
        r = requests.request(self.method, self.get_url(), data=message)

        if r.status_code // 100 != 2:
            self.write_to_console("Got HTTP: {}. Response:\n{}".format(r.status_code, r.text))
