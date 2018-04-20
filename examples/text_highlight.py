# Python port of text_highlight.cpp from the CUE SDK examples.
import time
import sys

import cue_sdk
from cue_sdk import *

try:
    input = raw_input
except NameError:
    pass


def range_float(start, stop, step):
    while start < stop:
        yield start
        start += step


def highlight_key(led_id):
    for x in range_float(0, 2, 0.1):
        val = int((1 - abs(x - 1)) * 255)
        led_color = CorsairLedColor(led_id, val, val, val)
        cue.set_led_colors(led_color)
        time.sleep(0.03)


def main():
    word = input("Please, input a word...\n")

    for letter in word:
        try:
            led_id = CLK(cue.get_led_by_name(letter))
        except cue_sdk.exceptions.InvalidArguments:
            continue
        if led_id != CLK.CLI_Invalid:
            highlight_key(led_id)

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
