import itertools
import platform
from ctypes import CDLL, c_bool, c_int, c_void_p, c_char, POINTER, CFUNCTYPE
from enum import Enum
from warnings import warn

from .enumerations import *
from .exceptions import *
from .structures import *
from .structures import _CorsairDeviceInfo, _CorsairLedPositions, _CorsairProtocolDetails

__all__ = ['CUE', 'CUESDK']


def _error_check(func):
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        if not self.silence_errors:
            self.error_check()
        return res

    return wrapper


class CUESDK(object):
    ERRORS = (ServerNotFound, NoControl, ProtocolHandshakeMissing, IncompatibleProtocol, InvalidArguments)

    def __init__(self, dll_path, silence_errors=False):
        """

        Args:
            dll_path (str): The path to the CUE SDK dll
            silence_errors (bool): Whether or not to raise errors when something goes wrong.
        """
        if platform.system() == "Windows":
            self._libcue = CDLL(dll_path)
        else:
            raise RuntimeError("CUE is not supported on {platform} as of right now.".format(platform=platform.system()))

        self.silence_errors = silence_errors
        self.counter = itertools.count(1)

        # Function prototypes
        self._libcue.CorsairSetLedsColors.restype = c_bool
        self._libcue.CorsairSetLedsColors.argtypes = [c_int, POINTER(CorsairLedColor)]

        self._callback_type = CFUNCTYPE(None, c_void_p, c_bool, c_int)
        self._callback = self._callback_type(self._callback_handler)
        self._libcue.CorsairSetLedsColorsAsync.restype = c_bool
        self._libcue.CorsairSetLedsColorsAsync.argtypes = [c_int, POINTER(CorsairLedColor), self._callback_type,
                                                           c_void_p]

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
        self.protocol_details = self.perform_protocol_handshake()

        # Creates the UpperCase aliases for each function (like the actual API)
        self.SetLedsColors = self.set_led_colors
        self.SetLedsColorsAsync = self.set_led_colors_async
        self.GetDeviceCount = self.get_device_count
        self.GetDeviceInfo = self.get_device_info
        self.GetLedPositions = self.get_led_positions
        self.GetLedIdForKeyName = self.get_led_by_name
        self.RequestControl = self.request_control
        self.ReleaseControl = self.release_control
        self.PerformProtocolHandshake = self.perform_protocol_handshake
        self.GetLastError = self.get_last_error
        self.ErrorCheck = self.error_check
        self.ProtocolDetails = self.protocol_details

    @_error_check
    def set_led_colors(self, led_colors):
        """
        Set specified leds to some colors. The color is retained until changed by successive calls.
        This function does not take logical layout into account.
        This function executes synchronously, if you are concerned about delays consider using set_led_colors_async().

        Args:
            led_colors (CorsairLedColor or list[CorsairLedColor]): The colors for each LED.

        Returns:
            bool: True if successful. Use get_last_error() to check the reason of failure.
                If there is no such ledId present in currently connected hardware
                (missing key in physical keyboard layout, or trying to control mouse while it’s disconnected)
                then function completes successfully and returns true

        Raises:
            ServerNotFound:
            NoControl:
            ProtocolHandshakeMissing:
            InvalidArguments: If some of r, g, b values are beyond 0-255 interval or array contains duplicates of some
                LED ids.
        """
        if hasattr(led_colors, "__iter__"):
            size = len(led_colors)
            led_array = CorsairLedColor * size
            return self._libcue.CorsairSetLedsColors(size, led_array(*led_colors))
        return self._libcue.CorsairSetLedsColors(1, led_colors)

    @_error_check
    def set_led_colors_async(self, led_colors, callback=None, context=None):
        """
        Same as set_led_colors() but returns control to the caller immediately.

        Args:
            led_colors (CorsairLedColor or list[CorsairLedColor]): The colors for each LED.
            callback (Callable[context (Any), result (bool), error (CE)]):
                Callback that is called by SDK when colors are set. Can be None if client is not interested in result.

                - context contains value that was supplied by user in set_led_colors_async() call.
                - result is True if call was successful, False otherwise.
                - error contains error code if call was not successful (result is False)
            context (Any): arbitrary context that will be returned in callback call. Can be None

        Returns:
            bool: True if successful. Use get_last_error() to check the reason of failure

        Raises:
            ServerNotFound:
            NoControl:
            ProtocolHandshakeMissing:
            InvalidArguments: If some of r, g, b values are beyond 0-255 interval or array contains duplicates of some
                LED ids.
        """

        if callback:
            actual_context = next(self.counter)
            if not callable(callback):
                raise TypeError
            self._callbacks[actual_context] = (callback, context)
        else:
            actual_context = None
        if hasattr(led_colors, "__iter__"):
            size = len(led_colors)
            led_array = CorsairLedColor * size
            return self._libcue.CorsairSetLedsColorsAsync(size, led_array(*led_colors), self._callback, actual_context)
        return self._libcue.CorsairSetLedsColorsAsync(1, led_colors, self._callback, actual_context)

    @_error_check
    def get_device_count(self):
        """
        Get number of connected Corsair devices. Returns not more than one device of each type
        (keyboard, mouse, headset) in case if there are multiple devices of the same type connected to the system.
        Use get_device_info() to get information about a certain device.

        Returns:
            int: -1 in case of error. 0-3 are possible values.

        Raises:
            ServerNotFound:
            ProtocolHandshakeMissing:
        """
        return self._libcue.CorsairGetDeviceCount()

    @_error_check
    def get_device_info(self, device_index):
        """
        Gets information about a device based on provided index.

        Args:
            device_index (int): zero-based index of device.
                Should be strictly less than a value returned by get_device_count()

        Returns:
            CorsairDeviceInfo or None: namedtruple that contains information about device
                or None if error has occurred.

        Raises:
            ServerNotFound:
            ProtocolHandshakeMissing:
            InvalidArguments: If device_index is invalid.
        """
        dev_info = self._libcue.CorsairGetDeviceInfo(device_index)
        if not bool(dev_info):  # False if `dev_info` is a NULL pointer
                return None
        return CorsairDeviceInfo(dev_info.contents)

    @_error_check
    def get_led_positions(self, device_index=None):
        """
        Provides a list of keyboard LEDs with their physical positions.

        Warnings:
            DeprecationWarning: If you supply a device_index (which is no longer required)

        Returns:
            CorsairLedPositions or None: namedtuple containing number of LED positions as well as an array of them
                or None if an error has occured.

        Raises:
            ServerNotFound:
            ProtocolHandshakeMissing:
        """
        if device_index is not None:
            warn("device_index is no longer required for GetLedPositions. It will be removed in a future update",
                 DeprecationWarning, stacklevel=2)
        leds = self._libcue.CorsairGetLedPositions()
        if not bool(leds):  # False if `leds` is a NULL pointer
            return None
        return CorsairLedPositions(leds.contents)

    @_error_check
    def get_led_by_name(self, key_name):
        """
        Retrieves led id for key name taking logical layout into account.
        So on AZERTY keyboards if user calls get_led_by_name(‘A’) he gets
        CLK.Q. This id can be used in set_led_colors().

        Args:
            key_name (str): Key name. "A"-"Z" (26 values) are valid values

        Returns:
            CLK: The proper LED id. CLK.CLI_Invalid if error occured.

        Raises:
            ServerNotFound:
            ProtocolHandshakeMissing:
            InvalidArguments: If key_name is invalid.
        """
        return CLK(self._libcue.CorsairGetLedIdForKeyName(key_name.encode('ascii')))

    @_error_check
    def request_control(self, access_mode):
        """
        Requests control using specified access mode. By default client has shared control over lighting
        so there is no need to call request_control() unless a client requires exclusive control.
        Args:
            access_mode (CAM): Requested access mode.

        Returns:
            bool: True if SDK received requested control or False otherwise.

        Raises:
            ProtocolHandshakeMissing:
            ServerNotFound:
            InvalidArguments: If provided access_mode is not supported by this version of the SDK.
        """
        access_mode = access_mode.value if isinstance(access_mode, Enum) else access_mode
        return self._libcue.CorsairRequestControl(access_mode)

    @_error_check
    def release_control(self, access_mode):
        """
         Releases previously requested control for specified access mode.

        Args:
            access_mode (CAM): Requested access mode to be released

        Returns:
            bool: True if SDK released requested control, or False otherwise

        Raises:
            ProtocolHandshakeMissing:
            ServerNotFound:
            InvalidArguments: If provided access_mode is not supported by this version of the SDK.
            IncompatibleProtocol: If the function was called for SDK that implements protocol version 1 or earlier.
        """
        access_mode = access_mode.value if isinstance(access_mode, Enum) else access_mode
        return self._libcue.CorsairReleaseControl(access_mode)

    @_error_check
    def perform_protocol_handshake(self):
        """
        Checks file and protocol version of CUE to understand which of SDK functions can be used.
        This is called automatically, there is no need to call for yourself.

        Returns:
            CorsairProtocolDetails: namedtuple containing protocol details.
        """
        return CorsairProtocolDetails(self._libcue.CorsairPerformProtocolHandshake())

    def get_last_error(self):
        """
        Gets the last error that occurred in this thread while using any CUESDK.* functions.

        Returns:
            CE: Error value.
        """
        return CE(self._libcue.CorsairGetLastError())

    def error_check(self):
        """
        NOT AN OFFICIAL SDK FUNCTION
        Checks for an error and raises it.

        Raises:
            ServerNotFound, NoControl, ProtocolHandshakeMissing, IncompatibleProtocol, InvalidArguments: If an error
                occurred.
        """
        if self.get_last_error() != CE.Success:
            raise self.ERRORS[self.GetLastError().value - 1]

    def _callback_handler(self, context, result, error):
        """
        NOT AN OFFICIAL SDK FUNCTION
        This is the actual callback sent to the SDK. It prevents the garbage collection of the CFUNCTYPE prototypes,
        and handles any context clashes.

        Args:
            context (Any): value that was supplied by user in CUESDK.set_led_colors_async call
            result (bool): True if successful, False otherwise
            error (int): contains error code if call was not successful (result is False)

        Returns:
            None

        Raises:
            ServerNotFound, NoControl, ProtocolHandshakeMissing, IncompatibleProtocol, InvalidArguments: If an error
                occurred and silence_errors is False
        """
        if (not self.silence_errors) and (not result) and error:
            raise self.ERRORS[error - 1]

        if context is not None and context in self._callbacks:
            callback, user_context = self._callbacks.pop(context)
            callback(user_context, result, CE(error))


def CUE(*args, **kwargs):
    warn("CUE has been renamed to CUESDK. It is deprecated and will be removed in an upcoming version",
         DeprecationWarning, stacklevel=2)
    return CUESDK(*args, **kwargs)
