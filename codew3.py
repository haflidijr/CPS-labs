# Metro M4 AirLift IO demo
# Welcome to CircuitPython 4 🙂

import time
from digitalio import DigitalInOut, Direction, Pull
import displayio
import adafruit_displayio_ssd1306
import terminalio
from adafruit_display_text import label
import adafruit_mpl3115a2

import busio
import board
import neopixel
import adafruit_tcs34725
from adafruit_bus_device import i2c_device, spi_device
import adafruit_fxos8700
import adafruit_fxas21002c
import math

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)
sensor.gain = 4

# led setup
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

pixels = neopixel.NeoPixel(board.NEOPIXEL, 4)

color = sensor.color

i2c = board.I2C()
fxos = adafruit_fxos8700.FXOS8700(i2c)
fxas = adafruit_fxas21002c.FXAS21002C(i2c)

WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 5

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White


bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
splash.append(inner_sprite)

while True:
    color_rgb = sensor.color_rgb_bytes
    pixels.fill(color_rgb)
    x_gauss = fxos.magnetometer[0] * 0.48828125
    y_gauss = fxos.magnetometer[1] * 0.48828125
    compass_rad = math.atan2(y_gauss, x_gauss)
    compass_degree = math.degrees(compass_rad)
    if compass_degree > 360:
        compass_degree -= 360
    if compass_degree < 0:
        compass_degree += 360
    if compass_degree <= 45 or compass_degree >= 315:
        led.value = True
    else:
        led.value = False
        
    # Draw a label
    text = f"Direction: {compass_degree}°"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=7, y=int(HEIGHT * 0.33))
    
    text2 = f"RGB: {color_rgb}"
    text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF, x=7, y=int(HEIGHT * 0.66))
    
    splash.append(text_area)
    splash.append(text_area2)
    time.sleep(1)
    splash.pop()
    splash.pop()
    # print(compass_degree)
    # print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*fxos.accelerometer))
    # print('Magnetometer (uTesla): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*fxos.magnetometer))
    # print('Gyroscope (radians/s): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*fxas.gyroscope))
    # print(fxos.magnetometer[0])

