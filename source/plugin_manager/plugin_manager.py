import json
import os
import shutil
import traceback
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
            "print": self._print,
            "stop_session": self._parent.disconnect,
            "update_rewards": self._parent.reload_rewards
        }

        self._setup_directory()

    def get_plugin_count(self) -> int:
        return len(self._plugins)

    def _print(self, *args, sep=' ', end='\n'):
        message = "{}{}".format(sep.join(str(a) for a in args), end)
        if message.endswith("\n"):
            message = message[:-1]

        self._parent.write_to_console(message)

    def _setup_directory(self):
        if not os.path.isdir(self._plugin_dir):
            os.makedirs(self._plugin_dir)

        if not os.path.isfile(self._control_file):
            with open(self._control_file, 'w') as f:
                f.write("{}")

    def _load_plugin(self, mod_data) -> plugin_model.Plugin:
        try:
            plugin = plugin_model.Plugin(
                self.builtin_funcs.copy(),
                os.path.join(self._plugin_dir, mod_data["name"]),
                mod_data["name"]
            )
            self._plugins.append(plugin)
            plugin.execute_func("on_start")

            return plugin

        except Exception:
            self.show_plugin_syntax_error(mod_data["name"])

    def reload_plugins(self):
        for plugin in self._plugins:
            plugin.execute_func("on_close")

        self._plugins.clear()

        with open(self._control_file) as f:
            plugin_index = json.loads(f.read())

            for plugin in plugin_index:
                if plugin["enabled"]:
                    self._load_plugin(plugin)

    def get_plugin_index(self) -> dict:
        with open(self._control_file) as f:
            return json.loads(f.read())

    def get_plugin(self, name: str) -> plugin_model.Plugin:
        for plugin in self._plugins:
            if plugin.info.name == name:
                return plugin

    def install_plugin(self, path: str, enable: bool = True) -> plugin_model.Plugin:
        ref_name = os.path.basename(path)

        shutil.copy2(path, os.path.join(self._plugin_dir, ref_name))

        mod_data = {"name": ref_name, "enabled": enable}

        with open(self._control_file) as f:
            plugin_index = json.loads(f.read())
            plugin_index.append(mod_data)

        with open(self._control_file, 'w') as f:
            f.write(json.dumps(plugin_index))

        if enable:
            return self._load_plugin(mod_data)

    def remove_plugin(self, ref_name: str, remove_files: bool = False):
        with open(self._control_file) as f:
            plugin_index = json.loads(f.read())

            plugin_index = [p for p in plugin_index if p["name"] != ref_name]

        with open(self._control_file, 'w') as f:
            f.write(json.dumps(plugin_index))

        if remove_files:
            path = os.path.join(self._plugin_dir, ref_name)

            os.remove(path)

    def _execute_func(self, func: str, *args, **kwargs):
        for plugin in self._plugins:
            try:
                plugin.execute_func(func, *args, **kwargs)
            except Exception:
                self.show_plugin_error(plugin)

    def show_plugin_syntax_error(self, name: str):
        break_length = 100

        self._parent.write_to_console("-" * break_length)
        self._parent.write_to_console("Plugin '{}' encountered the following exception:\n{}".format(
            name, traceback.format_exc(limit=0).replace("<string>", "main.py").rstrip("\n")
        ))
        self._parent.write_to_console("-" * break_length)

    def show_plugin_error(self, plugin: plugin_model.Plugin):
        stacktrace = []
        break_length = 100

        for line in traceback.format_exc(chain=False).split("\n"):
            if line.lower().startswith(("traceback", '  file "<string>"', "  file '<string>'")):
                stacktrace.append(line)

        stacktrace.append(traceback.format_exc().split("\n")[-2])

        self._parent.write_to_console("-" * break_length)
        self._parent.write_to_console("Plugin '{}' encountered the following exception:\n{}".format(
            plugin.info.name, "\n".join(stacktrace).replace("<string>", "main.py")
        ))
        self._parent.write_to_console("-" * break_length)

    def enable_plugin(self, name: str) -> plugin_model.Plugin:
        return self.set_plugin_state(name, True)

    def disable_plugin(self, name: str) -> plugin_model.Plugin:
        return self.set_plugin_state(name, False)

    def set_plugin_state(self, name: str, state: bool) -> plugin_model.Plugin:
        with open(self._control_file) as f:
            control = json.loads(f.read())

        located_plugin = None

        for plugin in control:
            if plugin["name"] == name:
                if plugin["enabled"] != state:

                    if state:
                        p = self._load_plugin(plugin)
                        if p is not None:
                            located_plugin = p

                    else:
                        for p in self._plugins:
                            if p.ref_name == plugin["name"]:
                                located_plugin = p
                                break

                        if located_plugin is not None:
                            located_plugin.execute_func("on_close")
                            self._plugins.remove(located_plugin)

                    plugin["enabled"] = state

        with open(self._control_file, 'w') as f:
            f.write(json.dumps(control))

        return located_plugin

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
