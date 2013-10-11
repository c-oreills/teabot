from itertools import islice

import spidev

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


def mean(sample, size):
    return sum(sample)/size


def interquartile_mean(sample, size):

    sample = list(sorted(sample))
    cull = size/4
    sample = sample[cull:-cull]
    return mean(sample, size-2*cull)


def conformant_moving_average(seq, n=50):
    averages = []
    for w in window(seq, n):
        average = interquartile_mean(w, n)
        averages.append(average)
        if len(averages) < n:
            continue
        averages_set = set(averages)
        print averages_set
        if len(averages_set) <= 2:
            return average
        averages = averages[1:]


def window(seq, n):
    seq = iter(seq)
    result = tuple(islice(seq, n))
    if len(result) == n:
        yield result
    for i in seq:
        result = result[1:] + (i,)
        yield result


def weigh_untared():
    return conformant_moving_average(raw_weights())


def weigh():
    return weigh_untared() - tare_value


def tare():
    global tare_value
    tare_value = weigh_untared()
