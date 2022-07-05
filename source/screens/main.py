import sys

import PySimpleGUI as sg
import source.defaults as defaults
import source.screens.communication as communication
import source.exceptions as exceptions

sg.change_look_and_feel('Dark2')

MODES = {
    "TCP/IP Broadcast": communication.TCPBroadcast,
    "TCP/IP Listen": communication.TCPListen,
    "Write To File": communication.FileWrite,
    "UDP Broadcast": communication.UDPBroadcast,
    "HTTP Listen": communication.HTTPListen,
    "HTTP Broadcast": communication.HTTPBroadcast,
    "RCON Broadcast": communication.RCONBroadcast,
    "No Action": communication.NoAction,
    "Key Press": communication.KeyPress,
}

FORMATS = [
    "JSON",
    "XML",
    "CSV"
]


def create_window():
    defs = defaults.get_defaults()

    layout = [
        [sg.Text("BackSeatGamer Reverse Proxy")],
        [sg.Text("Auth Code"), sg.Input(default_text=defs.get("auth_code", ""), key="auth_code")],
        [sg.Text("Mode"), sg.Combo(list(MODES.keys()), readonly=True, default_value=defs.get("mode", ""), key="mode")],
        [sg.Text("Format"), sg.Combo(FORMATS, readonly=True, default_value=defs.get("format", ""), key="format")],
        [sg.Text("Port"), sg.Input(default_text=defs.get("port", ""), key="port")],
        [sg.Text("Advanced Settings")],
        [sg.Text("Server"), sg.Input(default_text=defs.get("server", ""), key="server")],
        [sg.Text("Frequency"), sg.Input(default_text=defs.get("frequency", ""), key="frequency")],
        [sg.Button("Start")]
    ]

    return sg.Window(layout=layout, **defaults.WINDOW_SETTINGS)


def start_config(config: dict):
    try:
        MODES[config["mode"]](config)
    except (exceptions.FailedToConnectException, exceptions.ReturnToHomeException):
        pass


def show():
    if "--defaults" in sys.argv:
        start_config(defaults.get_defaults())

    window = create_window()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            sys.exit(0)

        if event == "Start":
            config = {
                "auth_code": window["auth_code"].get(),
                "mode": window["mode"].get(),
                "port": window["port"].get(),
                "server": window["server"].get(),
                "frequency": window["frequency"].get(),
                "format": window["format"].get()
            }

            if any(i.strip() == "" for i in config.values()):
                sg.Popup("All fields are mandatory!", **defaults.RAW_WINDOW_SETTINGS)
                continue

            if not config["server"].endswith("/"):
                config["server"] += "/"

            if config["port"].isdigit():
                config["port"] = int(config["port"])
            else:
                sg.Popup("Port must be an integer", **defaults.RAW_WINDOW_SETTINGS)
                continue

            if config["frequency"].isdigit():
                config["frequency"] = int(config["frequency"])
            else:
                sg.Popup("Frequency must be an integer", **defaults.RAW_WINDOW_SETTINGS)
                continue

            if config["frequency"] < 2:
                config["frequency"] = 2

            defaults.set_defaults("main", config)

            window.close()
            start_config(config)
            window = create_window()

    window.close()
