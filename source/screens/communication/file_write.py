import os
import time

import source.screens.communication.base_communication as base_communication
import source.setting as setting


class FileWrite(base_communication.BaseCommunication):
    @property
    def path(self) -> str:
        return self.additional_settings["path"]

    @property
    def clear(self) -> bool:
        return self.additional_settings["clear"]

    def startup(self):
        self.get_additional_settings("file_write_settings", [
            setting.Setting("Path", "path", input_type="select_folder"),
            setting.Setting(
                "Clear Old Files (WARNING: REMOVES ALL .TXT FILES)", "clear", input_type="checkbox", default=False
            )
        ])

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        if self.clear:
            for filename in os.listdir(self.path):
                if filename.endswith(".txt"):
                    os.remove(os.path.join(self.path, filename))

    def send_reward(self, message: str):
        if isinstance(message, bytes):
            message = message.decode("utf8")

        with open(os.path.join(self.path, "{}.txt".format(time.time())), 'w') as f:
            f.write(message)

    def teardown(self):
        pass
