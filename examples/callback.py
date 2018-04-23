#!python3
import time
import sys

from cue_sdk import *


def test(context, result, error):
    print(context, result, error)
    assert context == id(test)


def main():
    cue.set_led_colors_async(led_colors=[CorsairLedColor(CLK.H, 255, 255, 255), CorsairLedColor(CLK.G, 255, 255, 255)],
                             callback=test, context=id(test))
    while True:
        time.sleep(1)


if __name__ == "__main__":
    # To determine whether or not we are using a 64-bit version of Python,
    # we will check sys.maxsize. 64-bit Python will have a maxsize value of
    # 9223372036854775807, while 32-bit Python will have a mazsize value of
    # 2147483647.
    if sys.maxsize == 9223372036854775807:
        cue = CUESDK("CUESDK.x64_2015.dll")
    else:
        cue = CUESDK("CUESDK_2015.dll")
    cue.request_control(CAM.ExclusiveLightingControl)
    main()
