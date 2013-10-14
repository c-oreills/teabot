from weigh import weigh, tare
from time import sleep


WEIGHT_ERROR = 2

def bot():
    tare()
    current_weight = 0
    while True:
        current_weight = _bot_loop(current_weight)
        sleep(0.5)


def _bot_loop(current_weight):
    new_weight = weigh()
    if abs(new_weight - current_weight) > WEIGHT_ERROR:
        _weight_changed(current_weight, new_weight)
        current_weight = new_weight
    return current_weight

def _weight_changed(current_weight, new_weight):
    print 'Weight was', current_weight, 'now', new_weight
