#!python3
import time

from cue_sdk import *


def test(context, result, error):
    print(context, result, error)
    assert context == id(test)


Corsair = CUE("CUESDK.x64_2013.dll")
Corsair.RequestControl(CAM.ExclusiveLightingControl)
Corsair.SetLedsColorsAsync(2, [CorsairLedColor(CLK.H, 255, 255, 255), CorsairLedColor(CLK.G, 255, 255, 255)], test)

while True:
    time.sleep(1)
