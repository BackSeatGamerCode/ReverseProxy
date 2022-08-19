import dataclasses
import io
import json
import os.path
import shutil
import threading
import zipfile
import tempfile

import pydub
import pydub.playback


def default_func(*_, **__):
    pass


@dataclasses.dataclass
class Info:
    name: str
    version: str
    author: str
    desc: str
    url: str
    proxy_version: str
    main: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data.get("name"), data.get("version"), data.get("author"), data.get("desc"), data.get("url"),
            data.get("proxy_version"), data.get("main", "main.py")
        )

    @classmethod
    def from_string(cls, data: str):
        return cls.from_dict(
            json.loads(data)
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls.from_dict(json.loads(data.decode("utf-8")))


class Plugin:
    def __init__(self, builtin_funcs: dict, path: str, ref_name: str):
        self.ref_name = ref_name
        self._builtin_funcs = builtin_funcs

        self._is_directory = os.path.isdir(path)
        self._path = path

        self._info = Info.from_bytes(self.pull_file('info.json'))
        self._source = self.pull_file(self._info.main).decode("utf-8")

        self._builtin_funcs.update({
            "play_sound": self.play_sound,
            "info": self._info,
            "read_raw": self.pull_file,
            "read": self.pull_text_file,
            "write": self.write_text_file,
            "write_raw": self.write_file,
            "remove_file": self.remove_file
        })

        self._bytecode = self._builtin_funcs

        exec(self._source, self._bytecode)

    def pull_text_file(self, path: str, encoding: str = "utf-8") -> str:
        return self.pull_file(path).decode(encoding)

    def pull_file(self, path: str) -> bytes:
        try:
            if self._is_directory:
                with open(os.path.join(self._path, path), 'rb') as f:
                    return f.read()

            else:
                with zipfile.ZipFile(self._path, 'r') as archive:
                    return archive.read(path)

        except (KeyError, FileNotFoundError):
            raise FileNotFoundError("Requested file '{}' does not exist".format(path))

    def remove_file(self, path):
        if self._is_directory:
            file_path = os.path.join(self._path, path)

            if os.path.isfile(file_path):
                os.remove(file_path)

            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        else:
            temp_dir = tempfile.mkdtemp()

            try:
                temp_name = os.path.join(temp_dir, 'new.zip')
                with zipfile.ZipFile(self._path, 'r') as zipread:
                    with zipfile.ZipFile(temp_name, 'w') as zipwrite:
                        for item in zipread.infolist():
                            if item.filename != path:
                                data = zipread.read(item.filename)
                                zipwrite.writestr(item, data)

                shutil.move(temp_name, self._path)

            finally:
                shutil.rmtree(temp_dir)

    def write_file(self, path: str, content: bytes):
        if self._is_directory:
            with open(os.path.join(self._path, path), 'wb') as f:
                f.write(content)

        else:
            self.remove_file(path)

            with zipfile.ZipFile(self._path, 'a') as archive:
                archive.writestr(path, content)

    def write_text_file(self, path: str, content: str, encoding: str = "utf-8"):
        self.write_file(path, content.encode(encoding))

    def play_sound(self, path: str):
        extension_register = {
            ".wavv": pydub.AudioSegment.from_wav,
            ".wav": pydub.AudioSegment.from_wav,
            ".flv": pydub.AudioSegment.from_flv,
            # ".ogg": pydub.AudioSegment.from_ogg,
            ".mp3": pydub.AudioSegment.from_mp3,
        }

        buffer = io.BytesIO(self.pull_file(path))

        for ext, handler in extension_register.items():
            if path.lower().endswith(ext):
                threading.Thread(
                    target=pydub.playback.play,
                    args=[handler(buffer)],
                    daemon=True
                ).start()
                break

        else:
            raise ValueError(
                "The requested file '{}' is not a supported audio file type. Supported file types:\n{}".format(
                    path, ", ".join(extension_register.keys())
                )
            )

    def execute_func(self, func: str, *args, **kwargs):
        return self._bytecode.get(func, default_func)(*args, **kwargs)

    @property
    def info(self) -> Info:
        return self._info
