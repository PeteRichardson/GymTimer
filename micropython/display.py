""" Display object to interact with the custom 4 char LED strip display """

from neopixel import Neopixel

red =   (255,   0,   0)
green = (0,   255,   0)
blue =  (0,     0, 255)

class Display:
    """Display object to interact with the custom 4 char LED strip display"""
    def __init__(self, numpix, gpiopin, side):
        self.numpix = numpix
        self.gpiopin = gpiopin
        print("numpix=", self.numpix,", gpiopin = ", self.gpiopin)
        self.pixels = Neopixel(self.numpix, 0, self.gpiopin, "GRB")
        self.side = 8
        self.segments = {
            "ones": {
                0: [(8,8+6*side-1),],
                1: [(8, 8+side-1),(8+5*side, 8+6*side-1)],
                2: [(8+side, 8+3*side),(8+4*side, 8+7*side-1)],
                3: [(8, 8+2*side-1),(8+4*side, 8+7*side-1)],
                4: [(8, 8+side-1),(8+3*side, 8+4*side-1), (8+5*side, 8+7*side-1)],
                5: [(8, 8+2*side-1),(8+3*side, 8+5*side-1), (8+6*side, 8+7*side-1)],
                6: [(8, 8+5*side-1), (8+6*side, 8+7*side-1)],
                7: [(8, 8+side-1),(8+4*side, 8+6*side-1)],
                8: [(8, 8+7*side-1)],
                9: [(8, 8+2*side-1),(8+3*side, 8+7*side-1)],
            },
            "tens": {
                0: [(67,67+6*side-1),],
                1: [(67, 67+side-1),(67+5*side, 67+6*side-1)],
                2: [(67+side, 67+3*side-1),(67+4*side, 67+7*side-1)],
                3: [(67, 67+2*side-1),(67+4*side, 67+7*side-1)],
                4: [(67, 67+side-1),(67+3*side, 67+4*side-1), (67+5*side, 67+7*side-1)],
                5: [(67, 67+2*side-1),(67+3*side, 67+5*side-1), (67+6*side, 67+7*side-1)],
                6: [(67, 67+5*side-1), (67+6*side, 67+7*side-1)],
                7: [(67, 67+side-1),(67+4*side, 67+6*side-1)],
                8: [(67, 67+7*side-1)],
                9: [(67, 67+2*side-1),(67+3*side, 67+7*side-1)],
            },
            "hundreds": {
                0: [(156, 156+6*side-1),],
                1: [(156, 156+side-1),(156+5*side, 156+6*side-1)],
                2: [(156+side, 156+3*side-1),(156+4*side, 156+7*side-1)],
                3: [(156, 156+2*side-1),(156+4*side, 156+7*side-1)],
                4: [(156, 156+side-1),(156+3*side, 156+4*side-1), (156+5*side, 156+7*side-1)],
                5: [(156, 156+2*side-1),(156+3*side, 156+5*side-1), (156+6*side, 156+7*side-1)],
                6: [(156, 156+5*side-1), (156+6*side, 156+7*side-1)],
                7: [(156, 156+side-1),(156+4*side, 156+6*side-1)],
                8: [(156, 156+7*side-1),],
                9: [(156, 156+2*side-1),(156+3*side, 156+7*side-1)],           },
            "thousands": {
                0: [(215, 215+6*side-1),],
                1: [(215, 215+side-1),(215+5*side, 215+6*side-1)],
                2: [(215+side, 215+3*side-1),(215+4*side, 215+7*side-1)],
                3: [(215, 215+2*side-1),(215+4*side, 215+7*side-1)],
                4: [(215, 215+side-1),(215+3*side, 215+4*side-1), (215+5*side, 215+7*side-1)],
                5: [(215, 215+2*side-1),(215+3*side, 215+5*side-1), (215+6*side, 215+7*side-1)],
                6: [(215, 215+5*side-1), (215+6*side, 215+7*side-1)],
                7: [(215, 215+side-1),(215+4*side, 215+6*side-1)],
                8: [(215, 215+7*side-1),],
                9: [(215, 215+2*side-1),(215+3*side, 215+7*side-1)],
            }
        }

    def show(self, num, colon, color=blue, brightness=100):
        """ set the four numeric chars to a value."""
        self.pixels.clear()

        if num < 5:
            color = red
        if num == 0:
            color = green
        digit = int(num % 10)
        for segment in self.segments["ones"][digit]:
            self.pixels.set_pixel_line(segment[0], segment[1], color, brightness)

        digit = int((num % 100) / 10)
        for segment in self.segments["tens"][digit]:
            self.pixels.set_pixel_line(segment[0], segment[1], color, brightness)

        digit = int((num % 1000) / 100)
        for segment in self.segments["hundreds"][digit]:
            self.pixels.set_pixel_line(segment[0], segment[1], color, brightness)

        digit = int((num % 10000) / 1000)
        for segment in self.segments["thousands"][digit]:
            self.pixels.set_pixel_line(segment[0], segment[1], color, brightness)

        # Add colon
        colon_brightness = brightness
        if not colon:
            colon_brightness = 0
        self.pixels.set_pixel_line(128,129, color, colon_brightness)
        self.pixels.set_pixel_line(135,136, color, colon_brightness)
        self.pixels.set_pixel_line(141,142, color, colon_brightness)
        self.pixels.set_pixel_line(148,149, color, colon_brightness)

        self.pixels.show()
