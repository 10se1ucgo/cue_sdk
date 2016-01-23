from ctypes import *
from .cue_struct import *
from .cue_defines import *
from .cue_exceptions import *
import platform


class CUE(object):

    def __init__(self, dll_path):
        if platform.system() == "Windows":
            self._libcue = CDLL(dll_path)
        else:
            raise RuntimeError("CUE is not supported {platform} as of right now.".format(platform.system()))
        self.ProtocolDetails = self.PerformProtocolHandshake()
        self.ErrorCheck()

    def SetLedsColors(self, size, led_color):
        self._libcue.CorsairSetLedsColors.restype = c_bool
        self._libcue.CorsairSetLedsColors.argtypes = [c_int, POINTER(CorsairLedColor)]
        return self._libcue.CorsairSetLedsColors(size, led_color)

    def SetLedsColorsAsync(self, size, led_color):
        # Callback not implemented yet.
        self._libcue.CorsairSetLedsColorsAsync.restype = c_bool
        self._libcue.CorsairSetLedsColorsAsync.argtypes = [c_int, POINTER(CorsairLedColor), c_void_p, c_void_p]
        return self._libcue.CorsairSetLedsColorsAsync(size, led_color, None, None)

    def GetDeviceCount(self):
        self._libcue.CorsairGetDeviceCount.restype = c_int
        return self._libcue.CorsairGetDeviceCount()

    def GetDeviceInfo(self, device_id):
        self._libcue.CorsairGetDeviceInfo.restype = POINTER(CorsairDeviceInfo)
        self._libcue.CorsairGetDeviceInfo.argtypes = [c_int]
        return self._libcue.CorsairGetDeviceInfo(device_id)

    def GetLedPositions(self):
        self._libcue.CorsairGetLedPositions.restype = POINTER(CorsairLedPositions)
        return self._libcue.CorsairGetLedPositions()

    def GetLedIdForKeyName(self, key_name):
        self._libcue.CorsairGetLedIdForKeyName.restype = c_int
        self._libcue.CorsairGetLedIdForKeyName.argtypes = [c_char]
        return self._libcue.CorsairGetLedIdForKeyName(key_name)

    def RequestControl(self, access_mode):
        self._libcue.CorsairRequestControl.restype = c_bool
        self._libcue.CorsairRequestControl.argtypes = [c_int]
        return self._libcue.CorsairRequestControl(access_mode)

    def PerformProtocolHandshake(self):
        self._libcue.CorsairPerformProtocolHandshake.restype = CorsairProtocolDetails
        return self._libcue.CorsairPerformProtocolHandshake()

    def GetLastError(self):
        self._libcue.CorsairGetLastError.restype = c_int
        return self._libcue.CorsairGetLastError()

    def ErrorCheck(self):
        if self.GetLastError() != CE_Success:
            raise CorsairError[self.GetLastError()]
