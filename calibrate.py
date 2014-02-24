from pickle import dump
from weigh import raw_weights
from itertools import islice
from datetime import datetime

SAMPLE_SIZE = 10000

def calibrate():
    weights = raw_weights()
    while True:
        sample = list(islice(weights, SAMPLE_SIZE))
        f = open(str(datetime.now()), 'w')
        dump(sample, f)
        f.close()
        print 'Wrote', SAMPLE_SIZE, 'samples to', f.name
