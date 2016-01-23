# Python port of color_pulse.cpp from the CUE SDK examples.
from __future__ import division
import win32api
import win32con
import time
from cue_sdk import *


def range_float(start, stop, step):
    while start < stop:
        yield start
        start += step


def get_available_keys():
    colors_vector = []
    led_positions = Corsair.GetLedPositions()
    Corsair.ErrorCheck()
    for led in range(led_positions[0].numberOfLed):
        led_id = led_positions[0].pLedPosition[led].ledId
        colors_vector.append(CorsairLedColor(led_id, 0, 0, 0))

    return colors_vector


def perform_pulse_effect(colors_vector, wave_duration, time_per_frame):
    for x in range_float(0, 2, time_per_frame / wave_duration):
        val = (1 - pow(x - 1, 2)) * 255
        for led in colors_vector:
            # SetLedsColors(Async) takes a size function and an array of CorsairLedColors, but I don't know any C at all
            # so I won't be able to implement this myself. Instead we emulate this with the same for loop that sets the
            # LED green value..
            led.g = int(val)
            Corsair.SetLedsColorsAsync(1, led)

        time.sleep(time_per_frame / 1000)


def main():
    wave_duration = 500
    time_per_frame = 25
    colors_vector = get_available_keys()
    if colors_vector:
        print "Working... Use \"KP_PLUS\" or \"KP_MINUS\" to increase or decrease speed.\nPress Escape to close program"
        while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
            perform_pulse_effect(colors_vector, wave_duration, time_per_frame)
            if win32api.GetAsyncKeyState(win32con.VK_ADD) and wave_duration > 100:
                wave_duration -= 100
                print wave_duration
            if win32api.GetAsyncKeyState(win32con.VK_SUBTRACT) and wave_duration < 2000:
                wave_duration += 100
                print wave_duration
            time.sleep(0.025)


if __name__ == "__main__":
    Corsair = CUE("CUESDK.x64_2013.dll")
    Corsair.RequestControl(CAM_ExclusiveLightingControl)
    main()
