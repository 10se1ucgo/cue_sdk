from collections import namedtuple
from ctypes import Structure, c_int, c_char_p, c_double, c_bool, POINTER

from .cue_defines import CDT, CPL, CLL, CDC

__all__ = ['CorsairDeviceInfo', 'CorsairLedPosition', 'CorsairLedPositions',
           'CorsairLedColor', 'CorsairProtocolDetails']


class IterableStruct(Structure):
    def __iter__(self):
        for item in self.__slots__:
            yield getattr(self, item)


class _CorsairDeviceInfo(IterableStruct):
    __slots__ = [
        "type",
        "model",
        "physicalLayout",
        "logicalLayout",
        "capsMask"
    ]

_CorsairDeviceInfo._fields_ = [
    ("type", c_int),
    ("model", c_char_p),
    ("physicalLayout", c_int),
    ("logicalLayout", c_int),
    ("capsMask", c_int)
]


class CorsairDeviceInfo(namedtuple('CorsairDeviceInfo', _CorsairDeviceInfo.__slots__)):

    def __new__(cls, dev_info):
        dev_type = CDT(dev_info.type)
        dev_model = dev_info.model.decode()
        dev_pl = CPL(dev_info.physicalLayout)
        dev_ll = CLL(dev_info.logicalLayout)
        dev_cm = CDC(dev_info.capsMask)
        return super(CorsairDeviceInfo, cls).__new__(cls, dev_type, dev_model, dev_pl, dev_ll, dev_cm)


class _CorsairLedPosition(IterableStruct):
    __slots__ = [
        "ledId",
        "top",
        "left",
        "height",
        "width"
    ]

_CorsairLedPosition._fields_ = [
    ("ledId", c_int),
    ("top", c_double),
    ("left", c_double),
    ("height", c_double),
    ("width", c_double)
]

CorsairLedPosition = namedtuple('CorsairLedPosition', _CorsairLedPosition.__slots__)


class _CorsairLedPositions(IterableStruct):
    __slots__ = [
        "numberOfLed",
        "pLedPosition"
    ]

_CorsairLedPositions._fields_ = [
    ("numberOfLed", c_int),
    ("pLedPosition", POINTER(_CorsairLedPosition))
]

CorsairLedPositions = namedtuple('CorsairLedPositions', _CorsairLedPositions.__slots__)


# CorsairLedColor should be mutable, doesn't need a namedtuple.
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


class _CorsairProtocolDetails(IterableStruct):
    __slots__ = [
        "sdkVersion",
        "serverVersion",
        "sdkProtocolVersion",
        "serverProtocolVersion",
        "breakingChanges"
    ]

_CorsairProtocolDetails._fields_ = [
    ("sdkVersion", c_char_p),
    ("serverVersion", c_char_p),
    ("sdkProtocolVersion", c_int),
    ("serverProtocolVersion", c_int),
    ("breakingChanges", c_bool)
]


class CorsairProtocolDetails(namedtuple('CorsairProtocolDetails', _CorsairProtocolDetails.__slots__)):

    def __new__(cls, details):
        sdk_ver = details.sdkVersion.decode()
        server_ver = details.serverVersion.decode()
        return super(CorsairProtocolDetails, cls).__new__(cls, sdk_ver, server_ver, details.sdkProtocolVersion,
                                                          details.serverProtocolVersion, details.breakingChanges)
