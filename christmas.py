from neo_pixel import color, gamma32

# These are the computations to setup the LED values for
# a red, white and blue flag motif with growing/diminishing intensity and a
# theater chase effect (repeating pattern shifting left/right)

intense = [60, 80, 100, 120, 140, 160, 180, 200, 255, 200, 180, 160, 140, 120, 100, 80, 60]
def reds(intensity: int) -> int:
    return gamma32(color(intensity, 0, 0))

def whites(intensity: int) -> int:
    return gamma32(color(intensity, intensity, intensity))

def blues(intensity: int) -> int:
    return gamma32(color(0, 0, intensity))


def flag(i: int) -> [int]:
    return [reds(i), reds(i), reds(i), whites(i), whites(i), whites(i), blues(i), blues(i), blues(i)]
    
print(f"{[flag(i) for i in intense]}")

