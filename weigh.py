import spidev

from sample import conformant_moving_average

s = spidev.SpiDev()
s.open(0, 0)

tare_value = 0

def weigh_raw():
    bytes = s.xfer2([1, 0, 0])
    reading = bytes[1] & 3
    reading << 8
    reading += bytes[2]
    return reading


def raw_weights():
    while True:
        yield weigh_raw()


def weigh_untared():
    return conformant_moving_average(raw_weights(), 200)


def weigh():
    return weigh_untared() - tare_value


def tare():
    global tare_value
    tare_value = weigh_untared()
