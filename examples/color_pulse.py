# Python port of color_pulse.cpp from the CUE SDK examples.
from __future__ import division
import win32api
import win32con
import time
import sys

from cue_sdk import *


def range_float(start, stop, step):
    while start < stop:
        yield start
        start += step


def get_available_keys():
    colors = []
    for device_id in range(cue.get_device_count()):
        device_info = cue.get_device_info(device_id)

        if device_info.type == CDT.Mouse:
            for x in range(device_info.physicalLayout.value - CPL.Zones1.value + 1):
                led_id = CLK(CLK.CLM_1.value + x)
                colors.append(CorsairLedColor(led_id, 0, 0, 0))
        elif device_info.type == CDT.Keyboard:
            led_positions = cue.get_led_positions(device_id)
            for led in led_positions.pLedPosition:
                colors.append(CorsairLedColor(led.ledId, 0, 0, 0))
        elif device_info.type == CDT.Headset:
            colors.append(CorsairLedColor(CLK.CLH_LeftLogo, 0, 0, 0))
            colors.append(CorsairLedColor(CLK.CLH_RightLogo, 0, 0, 0))

    return colors


def perform_pulse_effect(colors, wave_duration, time_per_frame):
    for x in range_float(0, 2, time_per_frame / wave_duration):
        val = (1 - pow(x - 1, 2)) * 255
        for led in colors:
            led.g = int(val)
        cue.set_led_colors_async(colors)

        time.sleep(time_per_frame / 1000)


def main():
    wave_duration = 500
    time_per_frame = 25
    colors = get_available_keys()
    if not colors:
        return

    print("Working... Use \"KP_PLUS\" or \"KP_MINUS\" to increase or decrease speed.\nPress Escape to close program")
    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        perform_pulse_effect(colors, wave_duration, time_per_frame)
        if win32api.GetAsyncKeyState(win32con.VK_ADD) and wave_duration > 100:
            wave_duration -= 100
            print(wave_duration)
        if win32api.GetAsyncKeyState(win32con.VK_SUBTRACT) and wave_duration < 2000:
            wave_duration += 100
            print(wave_duration)
        time.sleep(0.025)


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
