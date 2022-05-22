def default_valid(_: str):
    return True


def default_cast(value: str):
    return value


class Setting:
    def __init__(
            self, display: str, key: str, input_type: str = "text", default="", mandatory: bool = True,
            is_valid: callable = default_valid, cast: callable = default_cast
    ):
        self.display = display
        self.key = key
        self.input_type = input_type
        self.default = default
        self.mandatory = mandatory
        self.is_valid = is_valid
        self.cast = cast
