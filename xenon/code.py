import time
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.color_packet import ColorPacket

# Print out the color data from ColorPackets.
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect, and then select colors on the Controller->Color Picker screen.

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

led = DigitalInOut(board.BLUE_LED)
led.direction = Direction.OUTPUT
pixels = neopixel.NeoPixel(board.D2, 16, auto_write=False, brightness=0.2)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)


def rainbow_cycle(wait):
    num_pixels = len(pixels)
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    led.value = False
    pixels.fill((0, 0, 0))
    pixels.show()

    # Advertise when not connected.
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    ble.stop_advertising()    

    while ble.connected:
        print("Enter color")
        packet = Packet.from_stream(uart_server)
        if isinstance(packet, ColorPacket):
            print(packet.color)
            pixels.fill(packet.color)
            pixels.show()
            led.value = True
            time.sleep(1)
            pixels.fill(0)
            pixels.show()
            led.value = False

    # rainbow_cycle(0.01)





