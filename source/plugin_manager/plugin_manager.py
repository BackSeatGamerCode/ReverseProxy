import json
import os
import typing

import source.plugin_manager.plugin as plugin_model

if typing.TYPE_CHECKING:
    import source.screens.communication.base_communication as base_communication

PLUGIN_DIR = "plugins"


class PluginManager:
    def __init__(self, parent: 'base_communication.BaseCommunication', plugin_dir: str = PLUGIN_DIR):
        self._parent = parent
        self._plugin_dir = plugin_dir

        self._control_file = os.path.join(self._plugin_dir, "plugins.json")
        self._plugins: typing.List[plugin_model.Plugin] = []

        self.builtin_funcs = {
            "speak": lambda x: self._parent._tts_queue.put(x),
            "get_rewards": lambda: self._parent._rewards,
            "clear_tts_queue": self._parent.clear_tts_queue,
            "set_tts_state": self._parent.set_tts_state,
            "disable_tts": lambda: self._parent.set_tts_state(False),
            "enable_tts": lambda: self._parent.set_tts_state(True),
            "get_tts_state": self._parent.get_tts_state,
            "toggle_tts_state": lambda: self._parent.set_tts_state(not self._parent.get_tts_state),
            "clear_console": self._parent.clear_console,
            "print": self._parent.write_to_console,
            "stop_session": self._parent.disconnect,
            "update_rewards": self._parent.reload_rewards
        }

        self._setup_directory()

    def _setup_directory(self):
        if not os.path.isdir(self._plugin_dir):
            os.makedirs(self._plugin_dir)

        if not os.path.isfile(self._control_file):
            with open(self._control_file, 'w') as f:
                f.write("{}")

    def reload_mods(self):
        with open(self._control_file) as f:
            mod_index = json.loads(f.read())

            for mod in mod_index:
                if mod["enabled"]:
                    self._plugins.append(
                        plugin_model.Plugin(self.builtin_funcs.copy(), os.path.join(self._plugin_dir, mod["name"]))
                    )

        self.on_start()

    def get_mod(self, name: str) -> plugin_model.Plugin:
        for plugin in self._plugins:
            if plugin.info.name == name:
                return plugin

    def _execute_func(self, func: str, *args, **kwargs):
        for plugin in self._plugins:
            plugin.execute_func(func, *args, **kwargs)

    def on_start(self):
        self._execute_func("on_start")

    def on_close(self):
        self._execute_func("on_close")

    def on_command(self, command, name, guest):
        self._execute_func("on_command", command, name, guest)

    def on_console_clear(self):
        self._execute_func("on_console_clear")

    def on_rewards_pull(self, rewards):
        self._execute_func("on_rewards_pull", rewards)
