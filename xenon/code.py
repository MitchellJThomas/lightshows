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
print(f"Bluetooth name: {ble.name}")
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

led = DigitalInOut(board.BLUE_LED)
led.direction = Direction.OUTPUT

# rgb_led_g = DigitalInOut(board.RGB_LED_GREEN)
# rgb_led_g.direction = Direction.OUTPUT

# rgb_led_r = DigitalInOut(board.RGB_LED_RED)
# rgb_led_r.direction = Direction.OUTPUT

# rgb_led_b = DigitalInOut(board.RGB_LED_BLUE)
# rgb_led_b.direction = Direction.OUTPUT

# pixels = neopixel.NeoPixel(board.D2, 16, auto_write=False, brightness=0.2)
pixels = neopixel.NeoPixel(board.D2, 80, auto_write=False, brightness=0.2)

i2c = busio.I2C(board.SCL, board.SDA)
accel_sensor = adafruit_lsm303_accel.LSM303_Accel(i2c)
accel_sensor.set_tap(1, 30)
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


def rainbow_cycle(wait):
    num_pixels = len(pixels)
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

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

    # Advertise when not connected.
    ble.start_advertising(advertisement)
#    rgb_led_r.value = True
#    rgb_led_g.value = False
    
    print("Waiting to connect")
    while not ble.connected:
        pass
    # ble.stop_advertising()
#    rgb_led_r.value = False
#    rgb_led_g.value = True    

    while ble.connected:
        packet = Packet.from_stream(uart_server)
        if isinstance(packet, ColorPacket):
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
                if packet.button == ButtonPacket.BUTTON_3:
                    print("Waiting for tap")
                    while not accel_sensor.tapped:
                        pass
                    print("Tapped")
                if packet.button == ButtonPacket.BUTTON_2:
                    for i in range(5):
                        print(f"Heading {get_heading(compass_sensor.magnetic):.2f} degrees")
                        acc_x, acc_y, acc_z = accel_sensor.acceleration
                        print(f"Acceleration (m/s^2): ({acc_x:10.3f}, {acc_y:10.3f}, {acc_z:10.3f})")                    
                        time.sleep(0.5)
                if packet.button == ButtonPacket.BUTTON_1:
                    # The 1 button was pressed.
                    rainbow_cycle(0.01)
                elif packet.button == ButtonPacket.UP:
                    acc_x, acc_y, acc_z = accel_sensor.acceleration
                    print(f"Acceleration (m/s^2): ({acc_x:10.3f}, {acc_y:10.3f}, {acc_z:10.3f})")                    
                    # pass
                    # The UP button was pressed.
                    # print("UP button pressed!")

