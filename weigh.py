from itertools import islice

import spidev

s = spidev.SpiDev()
s.open(0, 0)


def weigh_raw(retries=100):
    for i in xrange(retries):
        reading = s.xfer2([1, 0, 0])
        reading = reading[1] * 256 + reading[2]
        if reading > 2**10:
            # Error
            continue
        return reading
    raise Exception('Could not get reading')


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


def weigh():
    return conformant_moving_average(raw_weights())
