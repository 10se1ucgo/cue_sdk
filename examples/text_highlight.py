from cue_sdk import *
import time


def range_float(start, stop, step):
    while start < stop:
        yield start
        start += step


def highlight_key(led_id):
    for x in range_float(0, 2, 0.1):
        val = int((1 - abs(x - 1)) * 255)
        led_color = CorsairLedColor(led_id, val, val, val)
        Corsair.SetLedsColors(1, led_color)
        time.sleep(0.03)


def main():
    word = raw_input("Please, input a word...\n")

    for letter in word:
        print letter
        led_id = Corsair.GetLedIdForKeyName(letter)
        if led_id != CLI_Invalid:
            highlight_key(led_id)

if __name__ == "__main__":
    Corsair = CUE("CUESDK.x64_2013.dll")
    Corsair.RequestControl(CAM_ExclusiveLightingControl)
    main()
