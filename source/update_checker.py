import typing
import urllib.request
import json

import source.constants as constants


def is_update_pending() -> typing.Union[bool, dict]:
    try:
        response = urllib.request.urlopen("https://api.github.com/repos/BackSeatGamerCode/ReverseProxy/releases/latest")
        release = json.loads(response.read().decode("utf8"))
        new_version = release["tag_name"]

    except Exception:
        return False

    if format_version_number(new_version) == format_version_number(constants.VERSION):
        return False

    return release


def format_version_number(number: str) -> str:
    return ''.join(c for c in number if not c.isalpha())
