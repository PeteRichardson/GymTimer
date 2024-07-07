"""
GymTimer - control a 4 digit timer based on input from a 3 button footpedal
"""

import gc
from time import localtime, sleep_ms
from machine import Pin, Timer

from display import Display

LEFT_BUTTON_PIN   = 16
RIGHT_BUTTON_PIN  = 17
MIDDLE_BUTTON_PIN = 18



def logtime():
    """ get a formatted time to include in log entries """
    return '{:02d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}\t'.format(*localtime())

def two_minute_timer():
    """ Action for left button """
    print(f"# {logtime()}\tStarting two minute counter")
    start_timer(120)

def one_minute_timer():
    """ Action for middle button
        start a 60s counter """
    print(f"# {logtime()}\tStarting one minute counter")
    start_timer(60)

def clear_timer():
    """ Action for right button """
    print(f"# {logtime()}\tClearing timer")
    global value
    value = 0
    gc.collect()

def handler(p):
    """ irq handler to set the "clicked" attribute on all the buttons """
    global buttons
    for button in buttons:
        if p == button.pin:
            button.clicked = True

class Button():
    """ Class for buttons on footpedal

        Button is defined with a gpio pin to watch and an action to take. """

    def __init__(self, gpio, action):
        self.clicked = False
        self.id = gpio
        self.gpio = gpio
        self.pin = Pin(self.gpio, Pin.IN, Pin.PULL_UP)
        self.pin.irq (trigger = Pin.IRQ_FALLING, handler = handler, hard=True)
        self.action = action

    def check_for_action(self):
        """ call the action func if the button was pressed """
        if self.clicked and self.pin.value() == 0:
            self.action()
            # print('\tfree: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))

buttons = [Button(LEFT_BUTTON_PIN, two_minute_timer),
           Button(RIGHT_BUTTON_PIN, one_minute_timer),
           Button(MIDDLE_BUTTON_PIN, clear_timer)]

display = Display(270, 28, 8)

value = 0
colon = True


def update_display(t):
    # This gets called _twice each second_ (to allow us to pulse the colon).
    # So if you want to do something once each second, put it in the
    # if not colon block
    global value, colon

    if not colon:		# only adjust the value every other invocation
        value = value - 1
        value = 0 if value < 0 else value % 10000
    colon = not colon
    display.show(value, colon)   # "clock" converts seconds to MM:SS)

def start_timer(seconds):
    """ get the start value displayed quickly """
    global value   # make sure to update the global
    value = seconds
    display.show(value, True)    

timer = Timer()         # global, single timer
timer.init(period=500, mode=Timer.PERIODIC, callback=update_display)

while True:
    for button in buttons:
        button.clicked = False

    while not buttons[0].clicked and not buttons[1].clicked and not buttons[2].clicked:
        pass

    sleep_ms(20)    # debounce, in addition to HW debounce RC circuit
    for button in buttons:
        button.check_for_action()
