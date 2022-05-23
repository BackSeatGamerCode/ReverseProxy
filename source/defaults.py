import os
import json

DEFAULTS_FILE_PATH = "defaults.json"
DEFAULT_DATA = dict(
    main=dict(
        auth_code="",
        mode="",
        port="29175",
        server="https://backseatgamer.pythonanywhere.com",
        frequency="2",
        format="JSON"
    )
)

WINDOW_SETTINGS = {
    "title": "BackSeatGamer Reverse Proxy",
    "finalize": True,
    "icon": "assets/logo.ico" if os.name == 'nt' else "assets/logo.png"
}

RAW_WINDOW_SETTINGS = WINDOW_SETTINGS.copy()
del RAW_WINDOW_SETTINGS["finalize"]


def init():
    if not os.path.isfile(DEFAULTS_FILE_PATH):
        with open(DEFAULTS_FILE_PATH, 'w') as f:
            f.write(json.dumps(DEFAULT_DATA))


def get_defaults(menu: str = "main") -> dict:
    with open(DEFAULTS_FILE_PATH) as f:
        return json.loads(f.read())[menu]


def set_defaults(menu: str, defaults: dict):
    with open(DEFAULTS_FILE_PATH) as f:
        data = json.loads(f.read())

    data[menu] = defaults

    with open(DEFAULTS_FILE_PATH, 'w') as f:
        f.write(json.dumps(data))


init()
