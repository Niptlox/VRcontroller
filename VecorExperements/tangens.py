import math


def to_angle(x, y):
    return math.atan2(y, x)

for deg in range(0, 360, 10):
    a = math.pi * 2 * deg / 360
    x = math.cos(a)
    y = math.sin(a)
    angle = to_angle(x, y)
    print("in", x, y, a / math.pi * 180, angle / math.pi * 180)
