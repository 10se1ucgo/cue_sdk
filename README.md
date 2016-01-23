# cue_sdk
Python wrapper for the CUE SDK

[On PyPi](https://pypi.python.org/pypi/cue_sdk/)

# Installation
Use pip
```python
>>> pip install cue_sdk
```

# Usage example
```python
>>> from cue_sdk import *
# Load CUE DLL. Provide path to DLL yourself.
>>> Corsair = CUE("CUESDK.x64_2013.dll")
# Gives us exclusive access to controling the lighting and turns everything off.
>>> Corsair.RequestControl(CAM_ExclusiveLightingControl)
True
# Sets the color of the H key to white.
>>> Corsair.SetLedsColors(1, CorsairLedColor(CLK_H, 255, 255, 255))
True
# Returns number of Corsair devices.
>>> Corsair.GetDeviceCount()
1
# Takes zero-based index of device and returns a pointer to the struct with device info.
>>> Corsair.GetDeviceInfo(0)
<cue_sdk.cue_api.LP_CorsairDeviceInfo object at 0x000000000294DA48>
>>> device_info = Corsair.GetDeviceInfo(0)
# Returns the model of the device. Look at cue_structs.py for the other fields. Index with the same device index.
>>> device_info[0].model
'K70 RGB'
# Returns a pointer to the struct with all the LED positions.
>>> Corsair.GetLedPositions() 
<cue_sdk.cue_api.LP_CorsairLedPositions object at 0x0000000002A976C8>
>>> led_positions = Corsair.GetLedPositions()
# Returns number of LEDs on the device. Index with the device index. Look at cue_structs.py for the other fields.
>>> led_positions[0].numberOfLed
111
# Returns the led id for the key name. Relative to logical layout (e.g. on an AZERTY keyboard it will return Q, not A)
>>> Corsair.CorsairGetLedIdForKeyName('a')
38
>>> 38 is CLK_A
True
# Performs protocol handshake and returns details. Already called when the CUE class is initialized, no need to call for it yourself. 
>>> Corsair.PerformProtocolHandshake()
<cue_sdk.cue_struct.CorsairProtocolDetails object at 0x0000000002A98210>
# Protocol details are stored here when called handshake is performed on init.
>>> Corsair.ProtocolDetails
<cue_sdk.cue_struct.CorsairProtocolDetails object at 0x0000000002A980E0>
# Returns the SDK version number. Look at cue_structs.py for the other fields.
>>> Corsair.ProtocolDetails.sdkVersion
'1.10.73'
```
