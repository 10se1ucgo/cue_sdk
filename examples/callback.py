#!python3
import time

from cue_sdk import *


def test(context, result, error):
    print(context, result, error)
    assert context == id(test)


Corsair = CUE("CUESDK.x64_2013.dll")
Corsair.RequestControl(CAM_ExclusiveLightingControl)
Corsair.SetLedsColorsAsync(2, [CorsairLedColor(CLK_H, 255, 255, 255), CorsairLedColor(CLK_G, 255, 255, 255)], test)

while True:
    time.sleep(1)
