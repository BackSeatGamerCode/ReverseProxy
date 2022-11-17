import threading

import pynput.keyboard
from pynput.keyboard import Key, Listener


class HotkeyListener:
    def __init__(self):
        self._combinations = {}
        self._combination_state = {}
        self._events = {}

    def add_key_combo(self, name: str, keys: list, event: callable = None):
        self._combination_state[name] = {(k.lower() if isinstance(k, str) else k): False for k in keys}
        self._combinations[name] = False

        if event is not None:
            self._events[name] = event

    def remove_key_combo(self, name: str):
        del self._combinations[name]
        del self._combination_state[name]

    def get_combination_state(self, name: str) -> bool:
        state = self._combinations[name]
        self._combinations[name] = False
        return state

    def _start(self):
        def on_press(key):
            key = getattr(key, 'vk', key)
            key = chr(key) if isinstance(key, int) else key
            key = key.lower() if isinstance(key, str) else key

            for name, combo in self._combination_state.items():
                if key in combo.keys():
                    self._combination_state[name][key] = True

                if all(combo.values()):
                    self._combinations[name] = True

                    if name in self._events:
                        self._events[name]()

        def on_release(key):
            key = getattr(key, 'vk', key)
            key = chr(key) if isinstance(key, int) else key
            key = key.lower() if isinstance(key, str) else key

            for name, combo in self._combination_state.items():
                if key in combo.keys():
                    self._combination_state[name][key] = False

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def start(self) -> threading.Thread:
        t = threading.Thread(target=self._start, daemon=True, name="BackgroundHotkeyListener")
        t.start()
        return t
