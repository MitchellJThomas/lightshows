import math

# This is a port of code found here: https://github.com/adafruit/Adafruit_NeoPixel/
# The intention is to use this code to pre-calculate values for a neo-pixel strip

def gamma_table(gamma:int = 2.6):
    return [int(math.pow((x)/255.0,gamma)*255.0+0.5) for x in range(256)]

GAMMA_TABLE=gamma_table()

def gamma8(x: int) -> int:
    assert x <= len(GAMMA_TABLE)
    return GAMMA_TABLE[x]

def gamma32(x: int) -> int:
    assert x <= 0xffffff # 3 8 bit values packed into a 32 bit number
    r = ((x & 0xff0000) >> 16)
    g = ((x & 0x00ff00) >> 8)
    b = x & 0x0000ff
    return (gamma8(r) << 16) | (gamma8(g) << 8) | gamma8(b)

def color(r: int, g: int, b: int) -> int:
    assert r <= 0xff # 8 bit
    assert g <= 0xff
    assert b <= 0xff
    return (r << 16) | (g <<  8) | b
