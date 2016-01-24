from ctypes import Structure, c_int, c_char_p, c_double, c_bool, POINTER


class CorsairDeviceInfo(Structure):
    __slots__ = [
        "type",
        "model",
        "physicalLayout",
        "logicalLayout",
        "capsMask"
    ]

CorsairDeviceInfo._fields_ = [
    ("type", c_int),
    ("model", c_char_p),
    ("physicalLayout", c_int),
    ("logicalLayout", c_int),
    ("capsMask", c_int)
]


class CorsairLedPosition(Structure):
    __slots__ = [
        "ledId",
        "top",
        "left",
        "height",
        "width"
    ]

CorsairLedPosition._fields_ = [
    ("ledId", c_int),
    ("top", c_double),
    ("left", c_double),
    ("height", c_double),
    ("width", c_double)
]


class CorsairLedPositions(Structure):
    __slots__ = [
        "numberOfLed",
        "pLedPosition"
    ]

CorsairLedPositions._fields_ = [
    ("numberOfLed", c_int),
    ("pLedPosition", POINTER(CorsairLedPosition))
]


class CorsairLedColor(Structure):
    __slots__ = [
        "ledId",
        "r",
        "g",
        "b"
    ]

CorsairLedColor._fields_ = [
    ("ledId", c_int),
    ("r", c_int),
    ("g", c_int),
    ("b", c_int)
]


class CorsairProtocolDetails(Structure):
    __slots__ = [
        "sdkVersion",
        "serverVersion",
        "sdkProtocolVersion",
        "serverProtocolVersion",
        "breakingChanges"
    ]

CorsairProtocolDetails._fields_ = [
    ("sdkVersion", c_char_p),
    ("serverVersion", c_char_p),
    ("sdkProtocolVersion", c_int),
    ("serverProtocolVersion", c_int),
    ("breakingChanges", c_bool)
]
