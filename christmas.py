from neo_pixel import color, gamma32

# These are the computations to setup the LED values for
# a red, white and blue flag motif with growing/diminishing intensity and a
# theater chase effect (repeating pattern shifting left/right)

top = 200
rng = range(40, top-20, 4)
intense = list(rng) + [top] + list(reversed(rng))
intense.pop()

def reds(intensity: int) -> int:
    return gamma32(color(intensity, 0, 0))

def yellows(intensity: int) -> int:
    return gamma32(color(intensity, intensity, 0))

def whites(intensity: int) -> int:
    return gamma32(color(intensity, intensity, intensity))

def blues(intensity: int) -> int:
    return gamma32(color(0, 0, intensity))

def greens(intensity: int) -> int:
    return gamma32(color(0, intensity, 0))

def purples(intensity: int) -> int:
    return gamma32(color(100, 10, intensity))

def repeat(times: int, fn, *args):
    return [fn(*args) for _ in range(times)]

def flag(i: int) -> [int]:
    width = 6
    return repeat(width, greens, i) + repeat(width, yellows, i) + repeat(width, purples, i)


# Build C++ code for colors
colors_str = str([flag(i) for i in intense]).replace('[', '{').replace(']', '}')
colors_str = colors_str.replace("}, ", "},\n")

print(f"int intensities={len(intense)}, colors_len={len(flag(1))};\nuint32_t colors[intensities][colors_len] = {colors_str};")


