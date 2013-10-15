import spidev

from sample import repeated_proportional_sample

s = spidev.SpiDev()
s.open(0, 0)

# Default accuracy, takes about a half second to take this many readings
ACCURACY = 2000

tare_value = 0

def weigh_raw():
    bytes = s.xfer2([1, 0, 0])
    reading = bytes[1] & 3
    reading = reading << 8
    reading += bytes[2]
    return reading


def raw_weights():
    while True:
        yield weigh_raw()


def weigh_untared(accuracy=ACCURACY):
    return repeated_proportional_sample(raw_weights(), accuracy, 5, 3)


def weigh(accuracy=ACCURACY):
    return weigh_untared(accuracy) - tare_value


def tare(accuracy=ACCURACY):
    global tare_value
    tare_value = weigh_untared(accuracy)
