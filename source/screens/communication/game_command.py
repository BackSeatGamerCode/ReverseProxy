import time

import source.enums as enums
import source.interface.keyboard as keyboard_press
import source.screens.communication.base_communication as base_communication

DELAY = 0.2


class GameCommand(base_communication.BaseCommunication):
    def startup(self):
        self.raw_message_data = True

    def send_reward(self, message: str):
        if self._selected_game == enums.GameList.UNKNOWN_GAME:
            return

        if self._selected_game == enums.GameList.SUBNAUTICA:
            self.bump_key("RETURN")

        if self._selected_game == enums.GameList.PORTAL_2:
            self.bump_key("`")

        if self._selected_game == enums.GameList.THE_SIMS_4:
            self.key_combination("LCONTROL", "LSHIFT", 'C')

        time.sleep(DELAY)

        for char in message["command"]:
            self.bump_key(char)

        time.sleep(DELAY)

        self.bump_key("RETURN")

        if self._selected_game == enums.GameList.PORTAL_2:
            self.bump_key("ESCAPE")

        if self._selected_game == enums.GameList.THE_SIMS_4:
            self.key_combination("LCONTROL", "LSHIFT", 'C')

    def teardown(self):
        pass

    @staticmethod
    def bump_key(key: str):
        if key in ("UNDERLINE", "_"):
            keyboard_press.press_key("LSHIFT")
            keyboard_press.press_key("MINUS")

            keyboard_press.release_key("MINUS")
            keyboard_press.release_key("LSHIFT")

        else:
            keyboard_press.press_key(key)
            keyboard_press.release_key(key)

    @staticmethod
    def key_combination(*keys):
        for key in keys:
            if key in ("UNDERLINE", "_"):
                keyboard_press.press_key("LSHIFT")
                keyboard_press.press_key("MINUS")

            else:
                keyboard_press.press_key(key)

        for key in keys:
            if key in ("UNDERLINE", "_"):
                keyboard_press.release_key("MINUS")
                keyboard_press.release_key("LSHIFT")

            else:
                keyboard_press.release_key(key)
