from ctypes import CDLL, c_bool, c_int, c_void_p, c_char, POINTER, CFUNCTYPE
from .cue_struct import *
from .cue_defines import CorsairError, CE_Success
from .cue_exceptions import *
import platform


class CUE(object):

    def __init__(self, dll_path):
        if platform.system() == "Windows":
            self._libcue = CDLL(dll_path)
        else:
            raise RuntimeError("CUE is not supported {platform} as of right now.".format(platform=platform.system()))

        # Function prototypes
        self._libcue.CorsairSetLedsColors.restype = c_bool
        self._libcue.CorsairSetLedsColors.argtypes = [c_int, POINTER(CorsairLedColor)]

        self._callback_type = CFUNCTYPE(None, c_void_p, c_bool, c_int)
        self._callback = self._callback_type(self._callback_handler)
        self._libcue.CorsairSetLedsColorsAsync.restype = c_bool
        self._libcue.CorsairSetLedsColorsAsync.argtypes = [c_int, POINTER(CorsairLedColor), self._callback_type, c_void_p]

        self._libcue.CorsairGetDeviceCount.restype = c_int

        self._libcue.CorsairGetDeviceInfo.restype = POINTER(CorsairDeviceInfo)
        self._libcue.CorsairGetDeviceInfo.argtypes = [c_int]

        self._libcue.CorsairGetLedPositions.restype = POINTER(CorsairLedPositions)

        self._libcue.CorsairGetLedIdForKeyName.restype = c_int
        self._libcue.CorsairGetLedIdForKeyName.argtypes = [c_char]

        self._libcue.CorsairRequestControl.restype = c_bool
        self._libcue.CorsairRequestControl.argtypes = [c_int]

        self._libcue.CorsairReleaseControl.restype = c_bool
        self._libcue.CorsairReleaseControl.argtypes = [c_int]

        self._libcue.CorsairPerformProtocolHandshake.restype = CorsairProtocolDetails

        self._libcue.CorsairGetLastError.restype = c_int

        self._callbacks = {}
        self.ProtocolDetails = self.PerformProtocolHandshake()
        self.ErrorCheck()

    def SetLedsColors(self, size, led_color):
        if hasattr(led_color, "__getitem__"):
            led_array = CorsairLedColor * size
            return self._libcue.CorsairSetLedsColors(size, led_array(*led_color))
        return self._libcue.CorsairSetLedsColors(size, led_color)

    def SetLedsColorsAsync(self, size, led_color, callback=None, context=None):
        if callback:
            if context is None:
                context = id(callback)
            self._callbacks[context] = callback
        if hasattr(led_color, "__getitem__"):
            led_array = CorsairLedColor * size
            return self._libcue.CorsairSetLedsColorsAsync(size, led_array(*led_color), self._callback, context)
        return self._libcue.CorsairSetLedsColorsAsync(size, led_color, self._callback, context)

    def GetDeviceCount(self):
        return self._libcue.CorsairGetDeviceCount()

    def GetDeviceInfo(self, device_id):
        return self._libcue.CorsairGetDeviceInfo(device_id)

    def GetLedPositions(self):
        return self._libcue.CorsairGetLedPositions()

    def GetLedIdForKeyName(self, key_name):
        return self._libcue.CorsairGetLedIdForKeyName(key_name)

    def RequestControl(self, access_mode):
        return self._libcue.CorsairRequestControl(access_mode)

    def ReleaseControl(self, access_mode):
        return self._libcue.CorsairReleaseControl(access_mode)

    def PerformProtocolHandshake(self):
        return self._libcue.CorsairPerformProtocolHandshake()

    def GetLastError(self):
        return self._libcue.CorsairGetLastError()

    def ErrorCheck(self):
        if self.GetLastError() != CE_Success:
            raise CorsairError[self.GetLastError()]

    def _callback_handler(self, context, result, error):
        if context is not None and context in self._callbacks:
            self._callbacks.pop(context)(context, result, error)
