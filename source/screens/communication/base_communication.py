import abc
import csv
import io
import json
import queue
import sys
import threading
import time
import typing

import PySimpleGUI as sg
import source.tts as tts

import source.defaults as defaults
import source.exceptions as exceptions
import source.screens.additional_settings as additional_settings_screen
import source.sdk as sdk
import source.setting as setting
import source.screens.tts_settings as tts_settings
import source.constants as constants
import source.plugin_manager.plugin_manager as plugin_manager

TOOLBAR_STRUCTURE = [
    ['Session', ['Clear Console', 'Update Rewards', 'Stop']],
    ["TTS", ["TTS Options", "Clear TTS Queue"]],
    ['Help', 'About']
]


class BaseCommunication(abc.ABC):
    PORT = True

    def __init__(self, config: dict, start: bool = True):
        self._config = config

        self.raw_message_data = False

        self._rewards = []
        self._commands = {}
        self._running = True
        self._show_error = False

        self._tts_queue = queue.Queue()
        self._tts_thread = threading.Thread(target=self._tts_handler, name="TTSHandler", daemon=True)
        self._tts_thread.start()

        self.plugin_manager = plugin_manager.PluginManager()

        if not hasattr(self, "additional_settings"):
            self.additional_settings = {}

        self._window = None
        self._reward_buttons = []
        self._layout = []

        self.reload_rewards()

        self.startup()

        if start:
            self.show_window()

    def reload_rewards(self):
        self._rewards = self._get_rewards()
        self._commands = {i["command"]: i["name"] for i in self._rewards}

        self._reward_buttons = [
            [sg.Button(reward["name"], key="cmd_" + reward["command"])] for reward in self._rewards
        ]
        self._reward_buttons.append([
            sg.Input(key="custom_command_text", size=(30, None)), sg.Button("Execute", key="custom_command")
        ])

        self._layout = [
            [sg.Menu(TOOLBAR_STRUCTURE)],
            [sg.Text("BackSeatGamer Reverse Proxy")],
            [
                sg.Multiline(disabled=True, size=(None, 30), key="output", autoscroll=True),
                sg.Frame("Manually Trigger A Reward", layout=self._reward_buttons)
            ],
            [
                sg.Button("Clear"), sg.Button("Stop"),
                sg.Checkbox("Text to Speech", default=True, key="tts"), sg.Button("Clear TTS Queue")
            ]
        ]

    def _tts_handler(self):
        try:
            default_values = defaults.get_defaults("tts")
        except KeyError:
            default_values = {}

        tts.TTS_ENGINE.setProperty('rate', default_values.get('rate', tts.TTS_ENGINE.getProperty('rate')))
        tts.TTS_ENGINE.setProperty('volume', default_values.get('volume', tts.TTS_ENGINE.getProperty('volume')))
        tts.TTS_ENGINE.setProperty('voice', default_values.get('voice', tts.TTS_ENGINE.getProperty('voice')))

        while self._running:
            message = self._tts_queue.get()
            tts.TTS_ENGINE.say(message)
            tts.TTS_ENGINE.runAndWait()

    def get_additional_settings(self, name: str, settings: typing.List[setting.Setting]):
        self.additional_settings = additional_settings_screen.show(name, settings)

    @property
    def port(self) -> int:
        return self._config["port"]

    @property
    def host(self) -> str:
        return "127.0.0.1"

    @abc.abstractmethod
    def send_reward(self, message: str):
        pass

    def teardown(self):
        pass

    def startup(self):
        pass

    def _poll_server_daemon(self):
        while self._running:
            for reward in self._poll_server():
                try:
                    self._dispatch_reward(
                        reward["reward"]["command"], reward["reward"]["name"], reward["guest"]["name"]
                    )
                except (TypeError, KeyError):
                    self.return_to_menu()
                    break

            time.sleep(self._config["frequency"])

    def _poll_server(self):
        return sdk.poll_server(self._config["server"], self._config["auth_code"])

    def _get_rewards(self):
        try:
            return sdk.get_rewards(self._config["server"], self._config["auth_code"])
        except KeyError:
            self.alert_box("The provided access code is no longer valid. Check the spelling and try again.")
            self.return_to_menu()

    def return_to_menu(self):
        self._show_error = True
        try:
            self._window["Stop"].click()
        except (AttributeError, TypeError):
            raise exceptions.FailedToConnectException()

    def _dispatch_reward(self, command: str, name: str, guest: str):
        self.write_to_console("{} ({}) from: {}".format(name, command, guest))

        if self._window["tts"].get():
            self._tts_queue.put("{} has redeemed {}".format(guest, name))

        data_format = self._config["format"].lower()

        data = dict(
            command=command,
            name=name,
            guest=guest
        )

        self.plugin_manager.on_command(command, name, guest)

        if self.raw_message_data:
            self.send_reward(data)
            return

        if data_format == "json":
            message = json.dumps(data)

        elif data_format == "csv":
            output = io.StringIO()

            writer = csv.DictWriter(output, fieldnames=data.keys())
            writer.writeheader()
            writer.writerows([data])

            output.seek(0)
            message = output.read()
            output.close()

        else:
            message = '<?xml version="1.0" encoding="UTF-8" ?>\n<reward {}/>'.format(
                " ".join("{}=\"{}\"".format(k, v.replace('"', '\\"')) for k, v in data.items())
            )

        self.send_reward(message)

    def write_to_console(self, message: str):
        self._window["output"].update(message + "\n", append=True)

    def show_window(self):
        self._window = sg.Window(layout=self._layout, **defaults.WINDOW_SETTINGS)

        threading.Thread(target=self._poll_server_daemon, daemon=True, name="BSG Reverse Proxy Poll").start()

        while True:
            event, values = self._window.read()

            if event == sg.WIN_CLOSED:
                sys.exit(0)

            elif str(event).startswith("cmd_"):
                self._dispatch_reward(event[4:], self._commands[event[4:]], "ManualTrigger")

            elif event in ("Clear", "Clear Console"):
                self._window["output"].update("")
                self.plugin_manager.on_console_clear()

            elif event == "Update Rewards":
                self._window.close()

                self.reload_rewards()

                self.plugin_manager.on_rewards_pull(self._rewards)

                self.startup()
                self.show_window()

            elif event == "custom_command":
                command = self._window["custom_command_text"].get()
                self._dispatch_reward(command, command, "ManualTrigger")

            elif event == "Stop":
                self._running = False
                self._window.close()

                if self._show_error:
                    self.alert_box("The provided access code is no longer valid. Check the spelling and try again.")

                self.plugin_manager.on_close()
                self.teardown()
                return

            elif event == "About":
                self.alert_box(constants.ABOUT_TEXT)

            elif event == "Clear TTS Queue":
                while not self._tts_queue.empty():
                    self._tts_queue.get()

            elif event == "TTS Options":
                tts_settings.show()

    def alert_box(self, message: str, dialog_type: str = "Popup"):
        settings = defaults.WINDOW_SETTINGS.copy()

        del settings["finalize"]

        return {
            "popup": sg.Popup,
            "error": sg.PopupError,
            "popup_ok_cancel": sg.PopupOKCancel
        }[dialog_type.lower()](message, **settings)
