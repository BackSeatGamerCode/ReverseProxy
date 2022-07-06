import time

import source.interface.keyboard as keyboard
import source.screens.communication.base_communication as base_communication
import source.setting as setting


class KeyPress(base_communication.BaseCommunication):
    @property
    def path(self) -> str:
        return self.additional_settings["path"]

    @property
    def clear(self) -> bool:
        return self.additional_settings["clear"]

    def startup(self):
        self.get_additional_settings("file_write_settings", [
            setting.Setting("Hold Duration", "hold_duration", cast=float, default="0.05"),
        ])
        self.raw_message_data = True

    def send_reward(self, message: str):
        key = message["command"].lstrip("DIK_")
        try:
            keyboard.press_key(key)
            time.sleep(self.additional_settings["hold_duration"])
            keyboard.release_key(key)
        except KeyError:
            self.write_to_console("Key code '{}' is not recognized. Refer to documentation for more info.".format(key))

    def teardown(self):
        pass
