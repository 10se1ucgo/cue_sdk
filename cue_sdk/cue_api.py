from ctypes import CDLL, c_bool, c_int, c_void_p, c_char, POINTER, CFUNCTYPE, Structure
from .cue_struct import *
from .cue_struct import _CorsairDeviceInfo, _CorsairLedPositions, _CorsairProtocolDetails
from .cue_defines import *
from .cue_exceptions import *
import platform


class CUE(object):

    def __init__(self, dll_path, silence_errors=False):
        if platform.system() == "Windows":
            self._libcue = CDLL(dll_path)
        else:
            raise RuntimeError("CUE is not supported {platform} as of right now.".format(platform=platform.system()))

        self.silence_errors = silence_errors
        # Function prototypes
        self._libcue.CorsairSetLedsColors.restype = c_bool
        self._libcue.CorsairSetLedsColors.argtypes = [c_int, POINTER(CorsairLedColor)]

        self._callback_type = CFUNCTYPE(None, c_void_p, c_bool, c_int)
        self._callback = self._callback_type(self._callback_handler)
        self._libcue.CorsairSetLedsColorsAsync.restype = c_bool
        self._libcue.CorsairSetLedsColorsAsync.argtypes = [c_int, POINTER(CorsairLedColor), self._callback_type, c_void_p]

        self._libcue.CorsairGetDeviceCount.restype = c_int

        self._libcue.CorsairGetDeviceInfo.restype = POINTER(_CorsairDeviceInfo)
        self._libcue.CorsairGetDeviceInfo.argtypes = [c_int]

        self._libcue.CorsairGetLedPositions.restype = POINTER(_CorsairLedPositions)

        self._libcue.CorsairGetLedIdForKeyName.restype = c_int
        self._libcue.CorsairGetLedIdForKeyName.argtypes = [c_char]

        self._libcue.CorsairRequestControl.restype = c_bool
        self._libcue.CorsairRequestControl.argtypes = [c_int]

        self._libcue.CorsairReleaseControl.restype = c_bool
        self._libcue.CorsairReleaseControl.argtypes = [c_int]

        self._libcue.CorsairPerformProtocolHandshake.restype = _CorsairProtocolDetails

        self._libcue.CorsairGetLastError.restype = c_int

        self._callbacks = {}
        self.ProtocolDetails = self.PerformProtocolHandshake()

    def _error_check(func):
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            if not self.silence_errors:
                self.ErrorCheck()
            return res
        return wrapper

    @_error_check
    def SetLedsColors(self, led_colors):
        if hasattr(led_colors, "__getitem__"):
            size = len(led_colors)
            led_array = CorsairLedColor * size
            return self._libcue.CorsairSetLedsColors(size, led_array(*led_colors))
        return self._libcue.CorsairSetLedsColors(1, led_colors)

    @_error_check
    def SetLedsColorsAsync(self, led_colors, callback=None, context=None):
        if callback:
            if context is None:
                context = id(callback)
            self._callbacks[context] = callback
        if hasattr(led_colors, "__getitem__"):
            size = len(led_colors)
            led_array = CorsairLedColor * size
            return self._libcue.CorsairSetLedsColorsAsync(size, led_array(*led_colors), self._callback, context)
        return self._libcue.CorsairSetLedsColorsAsync(1, _CorsairLedColor(*led_colors), self._callback, context)

    @_error_check
    def GetDeviceCount(self):
        return self._libcue.CorsairGetDeviceCount()

    @_error_check
    def GetDeviceInfo(self, device_id):
        return CorsairDeviceInfo(self._libcue.CorsairGetDeviceInfo(device_id)[device_id])

    @_error_check
    def GetLedPositions(self, device_id):
        leds = self._libcue.CorsairGetLedPositions()[device_id]
        led_positions = []
        for x in range(leds.numberOfLed):
            led_positions.append(CorsairLedPosition(*leds.pLedPosition[x]))
        return CorsairLedPositions(leds.numberOfLed, led_positions)

    @_error_check
    def GetLedIdForKeyName(self, key_name):
        return CLK(self._libcue.CorsairGetLedIdForKeyName(key_name.encode('ascii')))

    @_error_check
    def RequestControl(self, access_mode):
        return self._libcue.CorsairRequestControl(access_mode)

    @_error_check
    def ReleaseControl(self, access_mode):
        return self._libcue.CorsairReleaseControl(access_mode)

    @_error_check
    def PerformProtocolHandshake(self):
        return CorsairProtocolDetails(self._libcue.CorsairPerformProtocolHandshake())

    def GetLastError(self):
        return CE(self._libcue.CorsairGetLastError())

    def ErrorCheck(self):
        if self.GetLastError() != CE.Success:
            raise CorsairError[self.GetLastError()]

    def _callback_handler(self, context, result, error):
        if context is not None and context in self._callbacks:
            self._callbacks.pop(context)(context, result, error)
