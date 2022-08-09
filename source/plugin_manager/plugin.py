import zipfile
import json
import dataclasses


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

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data.get("name"), data.get("version"), data.get("author"), data.get("desc"), data.get("url"),
            data.get("proxy_version")
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
    def __init__(self, path: str):
        self._path = path

        archive = zipfile.ZipFile(self._path, 'r')

        self._info = Info.from_bytes(archive.read('info.json'))
        self._source = archive.read('main.py').decode("utf-8")
        self._bytecode = {}

        exec(self._source, self._bytecode)

    def execute_func(self, func: str, *args, **kwargs):
        return self._bytecode.get(func, default_func)(*args, **kwargs)

    @property
    def info(self) -> Info:
        return self._info
