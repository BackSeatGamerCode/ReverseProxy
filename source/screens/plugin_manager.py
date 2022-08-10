import PySimpleGUI as sg

import source.defaults as defaults

import typing

if typing.TYPE_CHECKING:
    import source.plugin_manager.plugin_manager as plugin_manager_model


def create_window():
    layout = [
        [sg.Text("Plugin Manager")],
        [
            sg.Frame("Enabled Plugins", [
                [sg.Listbox(values=[], select_mode='extended', key='enabled_list', size=(30, 6))],
                [sg.Button("Disable Selected")]
            ]),
            sg.Frame("Disabled Plugins", [
                [sg.Listbox(values=[], select_mode='extended', key='disabled_list', size=(30, 6))],
                [sg.Button("Enable Selected")]
            ])
        ],
        [
            sg.Button("Install Plugin"),
            sg.Button("Close")
        ]
    ]

    return sg.Window(layout=layout, **defaults.WINDOW_SETTINGS)


def show(plugin_manager: 'plugin_manager_model.PluginManager'):
    def reload_plugin_list():
        plugin_list = plugin_manager.get_plugin_index()
        window["enabled_list"].update([p["name"] for p in plugin_list if p["enabled"]])
        window["disabled_list"].update([p["name"] for p in plugin_list if not p["enabled"]])

    window = create_window()

    reload_plugin_list()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == "Close":
            break

        elif event == "Disable Selected":
            for plugin in window["enabled_list"].get():
                plugin_manager.disable_plugin(plugin)

            reload_plugin_list()

        elif event == "Enable Selected":
            for plugin in window["disabled_list"].get():
                plugin_manager.enable_plugin(plugin)

            reload_plugin_list()

        elif event == "Install Plugin":
            plugins = sg.popup_get_file(
                "Locate your plugins", "Install Plugin", multiple_files=True, file_types=(("Plugin Files", "*.zip"),)
            ).split(";")

            for plugin in plugins:
                plugin_manager.install_plugin(plugin, enable=True)

            reload_plugin_list()

    window.close()
