import sys
import typing

import PySimpleGUI as sg

import source.defaults as defaults
import source.setting as setting
import source.exceptions as exceptions


def show(name: str, settings: typing.List[setting.Setting]) -> dict:
    try:
        default_values = defaults.get_defaults(name)
        if "--defaults" in sys.argv:
            return default_values

    except KeyError:
        default_values = {}

    def get_field(s: setting.Setting) -> list:
        if s.input_type == "text":
            return [
                sg.Text(s.display),
                sg.Input(default_text=default_values.get(s.key, s.default), key="K_" + s.key)
            ]

        elif s.input_type == "select_folder":
            return [
                sg.Text(s.display),
                sg.In(key="K_" + s.key, default_text=default_values.get(s.key, s.default)),
                sg.FolderBrowse(enable_events=True)
            ]

        elif s.input_type == "checkbox":
            return [
                sg.Checkbox(s.display, default=default_values.get(s.key, s.default), key="K_" + s.key)
            ]

        elif s.input_type == "dropdown":
            return [
                sg.Text(s.display),
                sg.Combo(
                    s.allowed_values, readonly=True, default_value=default_values.get(s.key, s.default),
                    key="K_" + s.key
                )
            ]

    def alert_box(message: str):
        props = defaults.WINDOW_SETTINGS.copy()
        del props["finalize"]

        sg.Popup(message, **props)

    layout = [
        [
            *get_field(s)
        ] for s in settings
    ]
    layout += [[sg.Button("Start"), sg.Button("Home")]]

    window = sg.Window(layout=layout, **defaults.WINDOW_SETTINGS)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            sys.exit(0)

        if event == "Start":
            response = {}
            for s in settings:
                value = window["K_" + s.key].get()

                if isinstance(value, str):
                    if not s.is_valid(value):
                        alert_box("{} is in an invalid format!".format(s.display))
                        break

                    if s.mandatory and value.strip() == "":
                        alert_box("{} is mandatory!".format(s.display))
                        break

                try:
                    response[s.key] = s.cast(value)
                except Exception:
                    alert_box("{} is in an invalid format!".format(s.display))
                    break

            else:
                defaults.set_defaults(name, response)
                window.close()
                return response

        if event == "Home":
            window.close()
            raise exceptions.ReturnToHomeException("RTS")
