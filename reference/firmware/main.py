"""MicroPython adapter for XIAO RP2040. Not flashed or tested on hardware."""
from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms
from timer import Timer

red, amber, green = (Pin(n, Pin.OUT) for n in (26,27,28))
button = Pin(29, Pin.IN, Pin.PULL_UP)
timer = Timer()
last = ticks_ms()
raw = stable = button.value()
changed_at = last
pressed_at = None
long_handled = False

while True:
    now = ticks_ms()
    timer.advance(ticks_diff(now, last))
    last = now
    current = button.value()
    if current != raw:
        raw, changed_at = current, now
    if raw != stable and ticks_diff(now, changed_at) >= 30:
        stable = raw
        if stable == 0:
            pressed_at, long_handled = now, False
        else:
            if pressed_at is not None and not long_handled:
                timer.tap()
            pressed_at = None
    if pressed_at is not None and not long_handled and ticks_diff(now, pressed_at) >= 2000:
        timer.reset()
        long_handled = True
    for pin, value in zip((red, amber, green), timer.lights()):
        pin.value(value)
    sleep_ms(10)
