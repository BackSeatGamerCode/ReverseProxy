import requests

import source.screens.communication.base_communication as base_communication
import source.setting as setting


class NoAction(base_communication.BaseCommunication):
    def send_reward(self, message: str):
        pass
