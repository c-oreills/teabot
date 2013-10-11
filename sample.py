from collections import Counter
from itertools import islice


def mean(sample, size):
    return sum(sample)/size


def interquartile_mean(sample, size):
    sample = list(sorted(sample))
    cull = size/4
    sample = sample[cull:-cull]
    return mean(sample, size-2*cull)


def conformant_moving_average(seq, n):
    averages = []
    for w in window(seq, n):
        average = interquartile_mean(w, n)
        averages.append(average)
        if len(averages) < n:
            continue
        averages_counter = Counter(averages)
        if len(averages_counter) <= 2:
            (average, _), = averages_counter.most_common(1)
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
