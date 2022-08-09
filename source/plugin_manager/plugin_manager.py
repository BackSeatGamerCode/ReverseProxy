import json
import os
import typing

import source.plugin_manager.plugin as plugin_model

PLUGIN_DIR = "plugins"


class PluginManager:
    def __init__(self, plugin_dir: str = PLUGIN_DIR):
        self._plugin_dir = plugin_dir
        self._control_file = os.path.join(self._plugin_dir, "plugins.json")
        self._plugins: typing.List[plugin_model.Plugin] = []

        self._setup_directory()
        self.reload_mods()

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
                        plugin_model.Plugin(os.path.join(self._plugin_dir, mod["name"]))
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
