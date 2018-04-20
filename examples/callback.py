#!python3
import time

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
    cue = CUESDK("CUESDK_2015.dll")
    cue.request_control(CAM.ExclusiveLightingControl)
    main()
