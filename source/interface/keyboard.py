import ctypes

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)

VK_CODE = {
    "ESCAPE":          0x01,
    "1":               0x02,
    "2":               0x03,
    "3":               0x04,
    "4":               0x05,
    "5":               0x06,
    "6":               0x07,
    "7":               0x08,
    "8":               0x09,
    "9":               0x0A,
    "0":               0x0B,
    "MINUS":           0x0C,
    "-":               0x0C,
    "EQUALS":          0x0D,
    "=":               0x0D,
    "BACK":            0x0E,
    "TAB":             0x0F,
    "\t":              0x0F,
    "Q":               0x10,
    "W":               0x11,
    "E":               0x12,
    "R":               0x13,
    "T":               0x14,
    "Y":               0x15,
    "U":               0x16,
    "I":               0x17,
    "O":               0x18,
    "P":               0x19,
    "LBRACKET":        0x1A,
    "RBRACKET":        0x1B,
    "RETURN":          0x1C,
    "\n":              0x1C,
    "LCONTROL":        0x1D,
    "A":               0x1E,
    "S":               0x1F,
    "D":               0x20,
    "F":               0x21,
    "G":               0x22,
    "H":               0x23,
    "J":               0x24,
    "K":               0x25,
    "L":               0x26,
    "SEMICOLON":       0x27,
    ";":               0x27,
    "APOSTROPHE":      0x28,
    "'":               0x28,
    "GRAVE":           0x29,
    "`":               0x29,
    "LSHIFT":          0x2A,
    "BACKSLASH":       0x2B,
    "\\":              0x2B,
    "Z":               0x2C,
    "X":               0x2D,
    "C":               0x2E,
    "V":               0x2F,
    "B":               0x30,
    "N":               0x31,
    "M":               0x32,
    "COMMA":           0x33,
    ",":               0x33,
    "PERIOD":          0x34,
    ".":               0x34,
    "SLASH":           0x35,
    "/":               0x35,
    "RSHIFT":          0x36,
    "MULTIPLY":        0x37,
    "LMENU":           0x38,
    "SPACE":           0x39,
    " ":               0x39,
    "CAPITAL":         0x3A,
    "F1":              0x3B,
    "F2":              0x3C,
    "F3":              0x3D,
    "F4":              0x3E,
    "F5":              0x3F,
    "F6":              0x40,
    "F7":              0x41,
    "F8":              0x42,
    "F9":              0x43,
    "F10":             0x44,
    "NUMLOCK":         0x45,
    "SCROLL":          0x46,
    "NUMPAD7":         0x47,
    "NUMPAD8":         0x48,
    "NUMPAD9":         0x49,
    "SUBTRACT":        0x4A,
    "NUMPAD4":         0x4B,
    "NUMPAD5":         0x4C,
    "NUMPAD6":         0x4D,
    "ADD":             0x4E,
    "NUMPAD1":         0x4F,
    "NUMPAD2":         0x50,
    "NUMPAD3":         0x51,
    "NUMPAD0":         0x52,
    "DECIMAL":         0x53,
    "OEM_102":         0x56,
    "F11":             0x57,
    "F12":             0x58,
    "F13":             0x64,
    "F14":             0x65,
    "F15":             0x66,
    "KANA":            0x70,
    "ABNT_C1":         0x73,
    "CONVERT":         0x79,
    "NOCONVERT":       0x7B,
    "YEN":             0x7D,
    "ABNT_C2":         0x7E,
    "NUMPADEQUALS":    0x8D,
    "PREVTRACK":       0x90,
    "AT":              0x91,
    "@":               0x91,
    "COLON":           0x92,
    ":":               0x92,
    "UNDERLINE":       0x93,
    "_":               0x93,
    "KANJI":           0x94,
    "STOP":            0x95,
    "AX":              0x96,
    "UNLABELED":       0x97,
    "NEXTTRACK":       0x99,
    "NUMPADENTER":     0x9C,
    "RCONTROL":        0x9D,
    "MUTE":            0xA0,
    "CALCULATOR":      0xA1,
    "PLAYPAUSE":       0xA2,
    "MEDIASTOP":       0xA4,
    "VOLUMEDOWN":      0xAE,
    "VOLUMEUP":        0xB0,
    "WEBHOME":         0xB2,
    "NUMPADCOMMA":     0xB3,
    "DIVIDE":          0xB5,
    "SYSRQ":           0xB7,
    "RMENU":           0xB8,
    "PAUSE":           0xC5,
    "HOME":            0xC7,
    "UP":              0xC8,
    "PRIOR":           0xC9,
    "LEFT":            0xCB,
    "RIGHT":           0xCD,
    "END":             0xCF,
    "DOWN":            0xD0,
    "NEXT":            0xD1,
    "INSERT":          0xD2,
    "DELETE":          0xD3,
    "LWIN":            0xDB,
    "RWIN":            0xDC,
    "APPS":            0xDD,
    "POWER":           0xDE,
    "SLEEP":           0xDF,
    "WAKE":            0xE3,
    "WEBSEARCH":       0xE5,
    "WEBFAVORITES":    0xE6,
    "WEBREFRESH":      0xE7,
    "WEBSTOP":         0xE8,
    "WEBFORWARD":      0xE9,
    "WEBBACK":         0xEA,
    "MYCOMPUTER":      0xEB,
    "MAIL":            0xEC,
    "MEDIASELECT":     0xED,
}


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class InputI(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", InputI)]


def press_key(key: str):
    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.ki = KeyBdInput(0, VK_CODE[key.upper()], 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(key: str):
    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.ki = KeyBdInput(0, VK_CODE[key.upper()], 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
