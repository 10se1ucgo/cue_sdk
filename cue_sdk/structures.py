from collections import namedtuple
from ctypes import Structure, c_int, c_char_p, c_double, c_bool, POINTER
from operator import attrgetter

from .enumerations import CDT, CPL, CLL, CDC, CLK

__all__ = ['CorsairDeviceInfo', 'CorsairLedPosition', 'CorsairLedPositions',
           'CorsairLedColor', 'CorsairProtocolDetails']


class _CorsairDeviceInfo(Structure):
    """
    Structure containing device info
    """
    __slots__ = [
        "type",
        "model",
        "physicalLayout",
        "logicalLayout",
        "capsMask"
    ]

    _fields_ = [
        ("type", c_int),
        ("model", c_char_p),
        ("physicalLayout", c_int),
        ("logicalLayout", c_int),
        ("capsMask", c_int)
    ]


class CorsairDeviceInfo(namedtuple('CorsairDeviceInfo', _CorsairDeviceInfo.__slots__)):

    def __new__(cls, dev_info):
        """

        Args:
            dev_info (_CorsairDeviceInfo): Structure containing device info

        Returns:
            CorsairDeviceInfo: namedtuple containing device info
        """
        dev_type = CDT(dev_info.type)
        dev_model = dev_info.model.decode()
        dev_pl = CPL(dev_info.physicalLayout)
        dev_ll = CLL(dev_info.logicalLayout)
        dev_cm = CDC(dev_info.capsMask)
        return super(CorsairDeviceInfo, cls).__new__(cls, dev_type, dev_model, dev_pl, dev_ll, dev_cm)


class _CorsairLedPosition(Structure):
    """
    Structure representing a LED position
    """
    __slots__ = [
        "ledId",
        "top",
        "left",
        "height",
        "width"
    ]

    _fields_ = [
        ("ledId", c_int),
        ("top", c_double),
        ("left", c_double),
        ("height", c_double),
        ("width", c_double)
    ]


class CorsairLedPosition(namedtuple('CorsairLedPosition', _CorsairLedPosition.__slots__)):

    def __new__(cls, led):
        """

        Args:
            led (_CorsairLedPosition): LED position structure

        Returns:
            CorsairLedPosition: LED position namedtuple
        """
        return super(CorsairLedPosition, cls).__new__(cls, CLK(led.ledId), led.top, led.left, led.height, led.width)


class _CorsairLedPositions(Structure):
    """
    Structure representing LED positions
    """
    __slots__ = [
        "numberOfLed",
        "pLedPosition"
    ]

    _fields_ = [
        ("numberOfLed", c_int),
        ("pLedPosition", POINTER(_CorsairLedPosition))
    ]


class CorsairLedPositions(namedtuple('CorsairLedPositions', _CorsairLedPositions.__slots__)):

    def __new__(cls, leds):
        """

        Args:
            leds (_CorsairLedPositions): Structure containing LED positions

        Returns:
            CorsairLedPositions: namedtuple containing LED positions
        """
        led_positions = tuple(sorted((CorsairLedPosition(leds.pLedPosition[x]) for x in range(leds.numberOfLed)),
                                     key=attrgetter('ledId.value')))
        return super(CorsairLedPositions, cls).__new__(cls, leds.numberOfLed, led_positions)


# CorsairLedColor should be mutable, doesn't need a namedtuple.
class CorsairLedColor(Structure):
    """
    Structure representing a LED color
    """
    __slots__ = [
        "ledId",
        "r",
        "g",
        "b"
    ]

    _fields_ = [
        ("ledId", c_int),
        ("r", c_int),
        ("g", c_int),
        ("b", c_int)
    ]

    def __init__(self, led_id, r, g, b):
        """

        Args:
            led_id (CLK or int): The LED id you want to set
            r (int): Red component value
            g (int): Green component value
            b (int): You guessed it! Blue component value
        """
        led_id = led_id.value if isinstance(led_id, CLK) else led_id
        super(CorsairLedColor, self).__init__(led_id, r, g, b)


class _CorsairProtocolDetails(Structure):
    """
    Structure representing protocol details
    """
    __slots__ = [
        "sdkVersion",
        "serverVersion",
        "sdkProtocolVersion",
        "serverProtocolVersion",
        "breakingChanges"
    ]

    _fields_ = [
        ("sdkVersion", c_char_p),
        ("serverVersion", c_char_p),
        ("sdkProtocolVersion", c_int),
        ("serverProtocolVersion", c_int),
        ("breakingChanges", c_bool)
    ]


class CorsairProtocolDetails(namedtuple('CorsairProtocolDetails', _CorsairProtocolDetails.__slots__)):

    def __new__(cls, details):
        """

        Args:
            details (_CorsairProtocolDetails): Structure containing the protocol handshake details.

        Returns:
            CorsairProtocolDetails: A namedtuple containing the protocol details.
        """
        sdk_ver = details.sdkVersion.decode()
        server_ver = details.serverVersion.decode()
        return super(CorsairProtocolDetails, cls).__new__(cls, sdk_ver, server_ver, details.sdkProtocolVersion,
                                                          details.serverProtocolVersion, details.breakingChanges)
