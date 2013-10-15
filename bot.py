from datetime import datetime
from time import sleep

from weigh import weigh, tare

WEIGHT_ERROR = 2

def bot():
    tare()
    current_weight = 0
    while True:
        current_weight = _bot_loop(current_weight)
        sleep(0.5)


def _bot_loop(current_weight):
    new_weight_lo_fi = weigh(accuracy=200)
    if abs(new_weight_lo_fi - current_weight) <= WEIGHT_ERROR:
        return current_weight

    new_weight = weigh()
    if abs(new_weight - current_weight) <= WEIGHT_ERROR:
        return current_weight

    _weight_changed(current_weight, new_weight)
    current_weight = new_weight
    return current_weight


def _weight_changed(current_weight, new_weight):
    print datetime.now(), 'Weight was', current_weight, 'now', new_weight
