import PySimpleGUI as sg
import webbrowser

import source.defaults as defaults


def create_window(release: dict):
    layout = [
        [sg.Text("BackSeatGamer Reverse Proxy")],
        [sg.Text("{} is available".format(release["tag_name"]))],
        [sg.Multiline(disabled=True, size=(50, 10), key="output", autoscroll=True, default_text=release["body"])],
        [
            sg.Button("Close"), sg.Button("Ignore"), sg.Button("Download")
        ]
    ]

    return sg.Window(layout=layout, **defaults.WINDOW_SETTINGS)


def show(release: dict):
    try:
        default_values = defaults.get_defaults("update")

    except KeyError:
        default_values = {"ignore_update": None}

    if default_values.get("ignore_update") == release["tag_name"]:
        return

    window = create_window(release)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Close":
            break

        if event == "Ignore":
            default_values["ignore_update"] = release["tag_name"]
            defaults.set_defaults("update", default_values)
            break

        if event == "Download":
            webbrowser.open(release["html_url"])

    window.close()
