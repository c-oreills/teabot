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


def repeated_proportional_sample(seq, sample_size, most_common, repeats):
    samples = []
    for i in xrange(100 + repeats):
        samples.append(proportional_sample(seq, sample_size, most_common))
        if len(samples) < repeats:
            continue
        samples = samples[-repeats:]
        samples_counter = Counter(samples)
        if len(samples_counter) > 2:
            continue
        if len(samples_counter) == 1:
            value, = samples_counter.keys()
            return value
        v1, v2 = samples_counter.keys()
        if abs(v1 - v2) > 1:
            continue
        # If we're straddling two numbers then round up
        value = max(v for v in samples_counter)
        return value


def proportional_sample(seq, sample_size, most_common):
    sample = Counter(islice(seq, sample_size))
    vals_and_freqs = sample.most_common(most_common)
    return sum(v*f for v, f in vals_and_freqs)/sum(f for _, f in vals_and_freqs)
