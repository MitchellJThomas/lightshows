import time
from math import atan2, degrees
import board
import busio

import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag

import neopixel
from digitalio import DigitalInOut, Direction, Pull
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.accelerometer_packet import AccelerometerPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.gyro_packet import GyroPacket
from adafruit_bluefruit_connect.location_packet import LocationPacket
from adafruit_bluefruit_connect.magnetometer_packet import MagnetometerPacket
from adafruit_bluefruit_connect.quaternion_packet import QuaternionPacket



# Print out the color data from ColorPackets.
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect, and then select colors on the Controller->Color Picker screen.

ble = BLERadio()
ble.name = "Bike Lights"
print(f"Bluetooth name: {ble.name}")
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)
# advertisement.complete_name = "Blue Lights"
# print(f"Advertisement complete name {advertisement.complete_name}")
# print(f"Advertisement short name {advertisement.short_name}")

led = DigitalInOut(board.BLUE_LED)
led.direction = Direction.OUTPUT

# rgb_led_g = DigitalInOut(board.RGB_LED_GREEN)
# rgb_led_g.direction = Direction.OUTPUT

# rgb_led_r = DigitalInOut(board.RGB_LED_RED)
# rgb_led_r.direction = Direction.OUTPUT

# rgb_led_b = DigitalInOut(board.RGB_LED_BLUE)
# rgb_led_b.direction = Direction.OUTPUT

# pixels = neopixel.NeoPixel(board.D2, 16, auto_write=False, brightness=0.2)
# pixels = neopixel.NeoPixel(board.D2, 80, auto_write=False, brightness=0.4)
pixels = neopixel.NeoPixel(board.D2, 56, auto_write=False, brightness=0.4)

i2c = busio.I2C(board.SCL, board.SDA)
accel_sensor = adafruit_lsm303_accel.LSM303_Accel(i2c)
accel_sensor.mode = adafruit_lsm303_accel.Mode.MODE_LOW_POWER
accel_sensor.set_tap(2, 30)
compass_sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

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

def rainbow_cycle(pixels, wait):
    num_pixels = len(pixels)
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

# def bike_rainbow_cycle(pixels, wait):
#     """
#     Split the string in half and mirror from the middle to the ends
#     """
#     num_middle_pixels = 16
#     num_pixels = len(pixels)
#     left_half_pixels = int(num_pixels / 2) - int(num_middle_pixels / 2)

#     # middle stuff
#     degrees = get_heading(compass_sensor.magnetic)
#     for m in range(num_middle_pixels):
#             pixels[left_half_pixels + m] = wheel(degrees % 255)

#     # left and right half stuff
#     for j in range(255):
#         pixels[left_half_pixels]
#         for i in range(left_half_pixels):
#             pixel_index = (i * 256 // left_half_pixels) + j
#             color = wheel(pixel_index & 255)
#             right = num_pixels - 1 - i
#             pixels[i] = pixels[right] = color
#         pixels.show()
#         time.sleep(wait)

def fade(rgb):
    return (int(rgb[0] * .95),
            int(rgb[1] * .95),
            int(rgb[2] * .95))

def fill_fade(pixels, color):
    while color[0] | color[1] | color[2]:
        pixels.fill(color)
        pixels.show()
        time.sleep(0.01)
        color = fade(color)
    pixels.fill(0)
    pixels.show()

# def compass_fill(pixels, compass_sensor):
#     pixels.fill((255, 0, 0))
#     pixels.show()
#     time.sleep(0.25)
#     for i in range(500):
#         degrees = get_heading(compass_sensor.magnetic)
#         color = wheel(degrees % 255)
#         # print(f"Compass color {color}")
#         pixels.fill(color)
#         pixels.show()
#         time.sleep(0.1)
    
def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle

def get_heading(magnetic):
    magnet_x, magnet_y, _ = magnetic
    return vector_2_degrees(magnet_x, magnet_y)

    
while True:
    led.value = False
    pixels.fill(0)
    pixels.show()

    # print("Bike rainbow")
    # for i in range(10):
    # while True:
    # bike_rainbow_cycle(pixels, 0.004)

    #print("STD rainbow")
    #for i in range(10):
    #    rainbow_cycle(pixels, 0.0001)

    # Advertise when not connected.
    ble.start_advertising(advertisement)
#    rgb_led_r.value = True
#    rgb_led_g.value = False

    print("Waiting to connect")
    while not ble.connected:
        led.value = False
        time.sleep(0.2)
        led.value = True
        time.sleep(0.2)
    # ble.stop_advertising()

    last_color = (120, 120, 120)
    while ble.connected:
        packet = Packet.from_stream(uart_server)
        if isinstance(packet, ColorPacket):
            last_color = packet.color
            print(packet.color)
            led.value = True
            fill_fade(pixels, packet.color)
            led.value = False
        if isinstance(packet, LocationPacket):
                print("Latitude:", packet.latitude)
                print("Longitude", packet.longitude)
                print("Altitude:", packet.altitude)
        if isinstance(packet, AccelerometerPacket):
            print("Acceleration:", packet.x, packet.y, packet.z)
        if isinstance(packet, MagnetometerPacket):
            print("Magnetometer:", packet.x, packet.y, packet.z)
        if isinstance(packet, GyroPacket):
            print("Gyro:", packet.x, packet.y, packet.z)
        if isinstance(packet, QuaternionPacket):
            print("Quaternion:", packet.x, packet.y, packet.z)
        if isinstance(packet, ButtonPacket):
            if packet.pressed:
                print(f"{packet.button} button pressed")
                if packet.button == ButtonPacket.BUTTON_4:
                    compass_fill(pixels, compass_sensor)
                    # pass
                if packet.button == ButtonPacket.BUTTON_3:
                    print("Waiting for tap")
                    while not accel_sensor.tapped:
                         pass
                    print("Tapped")
                    # pass
                if packet.button == ButtonPacket.BUTTON_2:
                     for i in range(100):
                         print(f"Heading {get_heading(compass_sensor.magnetic):.2f} degrees")
                         acc_x, acc_y, acc_z = accel_sensor.acceleration
                         print(f"Acceleration (m/s^2): ({acc_x:10.3f}, {acc_y:10.3f}, {acc_z:10.3f})")
                         time.sleep(0.5)
                    # pass
                if packet.button == ButtonPacket.BUTTON_1:
                    # The 1 button was pressed.
                    rainbow_cycle(pixels, 0.01)
                elif packet.button == ButtonPacket.UP:
                    acc_x, acc_y, acc_z = accel_sensor.acceleration
                    print(f"Acceleration (m/s^2): ({acc_x:10.3f}, {acc_y:10.3f}, {acc_z:10.3f})")                    
                    # pass
                    # The UP button was pressed.
                    print("UP button pressed!")

