# cue_sdk
Python wrapper for the CUE SDK

# Example
```python
>>> from cue_sdk import *
>>> Corsair = CUE("CUESDK.x64_2013.dll") # Load CUE DLL. Provide any path.
>>> Corsair.RequestControl(CAM_ExclusiveLightingControl)  #  Gives us exclusive access to controling the lighting and turns everything off.
True
>>> Corsair.SetLedsColors(1, CorsairLedColor(CLK_H, 255, 255, 255))  # Sets the H key to be white.
True
>>> Corsair.GetDeviceCount()  # Returns number of Corsair devices.
1
>>> Corsair.GetDeviceInfo(0)  # Takes zero-based index of device and returns a pointer to the struct with the info
<cue_sdk.cue_api.LP_CorsairDeviceInfo object at 0x000000000294DA48>
>>> device_info = Corsair.GetDeviceInfo(0)
>>> device_info[0].model  # Returns the model of the device
'K70 RGB'
>>> Corsair.GetLedPositions()  # Returns a struct with all the LED positions.
<cue_sdk.cue_api.LP_CorsairLedPositions object at 0x0000000002A976C8>
>>> led_positions = Corsair.GetLedPositions()
>>> led_positions[0].numberOfLed  # Returns number of LEDs on the device. [0] specifies the device (I think?)
111
>>> Corsair.CorsairGetLedIdForKeyName('a')  # Returns the led id for the key name. Relative to logical layout (e.g. on an AZERTY keyboard it will return Q, not A)
38
>>> 38 is CLK_A
True
>>> Corsair.PerformProtocolHandshake()  # Performs protocol handshake. Already called when the CUE class is initialized, no need to call for it yourself.
<cue_sdk.cue_struct.CorsairProtocolDetails object at 0x0000000002A98210>
>>> Corsair.ProtocolDetails # Protocol details are stored here when called handshake is performed.
<cue_sdk.cue_struct.CorsairProtocolDetails object at 0x0000000002A980E0>
>>> Corsair.ProtocolDetails.sdkVersion
'1.10.73'
```
