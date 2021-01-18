from neo_pixel import color, gamma32

# These are the computations to setup the LED values for
# a red, white and blue flag motif with growing/diminishing intensity and a
# theater chase effect (repeating pattern shifting left/right)

rng = range(20, 255, 10)
intense = list(rng) + [255] + list(reversed(rng))
intense.pop()

def reds(intensity: int) -> int:
    return gamma32(color(intensity, 0, 0))

def whites(intensity: int) -> int:
    return gamma32(color(intensity, intensity, intensity))

def blues(intensity: int) -> int:
    return gamma32(color(0, 0, intensity))

def flag(i: int) -> [int]:
    return [reds(i), reds(i), reds(i), whites(i), whites(i), whites(i), blues(i), blues(i), blues(i)]

# Build C++ code for colors
colors_str = str([flag(i) for i in intense]).replace('[', '{').replace(']', '}')
colors_str = colors_str.replace("}, ", "},\n")

print(f"int intensities={len(intense)}, colors_len={len(flag(1))};\nuint32_t colors[intensities][colors_len] = {colors_str};")


