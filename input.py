from inputs import get_gamepad
from time import sleep
from multiprocessing import Value, Process, freeze_support


def first(iterable):
    for item in iterable or []:
        yield item
        return

MAX = 32768
HYSTERESIS = 256


def convert_to_percentage(value):
    pos = abs(value)
    sign = value / pos
    val = pos - HYSTERESIS
    percent = val / (MAX - HYSTERESIS)
    return round(sign * percent, 2)


def watch_gp(x, y, buttons):
    while 1:
        gp_events = get_gamepad()
        for event in gp_events:
            if event.ev_type == "Absolute":
                if event.code == "ABS_X":
                    x.value = convert_to_percentage(event.state)
                if event.code == "ABS_Y":
                    y.value = convert_to_percentage(event.state) * -1
            if event.ev_type == "Key" and event.state == 1:
                buttons.press(event.code)
        sleep(0.1)


class Buttons(object):
    def __init__(self):
        self.values = {}
        [self.press("BTN_"+i) for i in ['NORTH', 'SOUTH', 'EAST', 'WEST', 'TR', 'TL']]
        self.reset()
        self.has_press = False

    def reset(self):
        for v in self.values.values():
            v.value = 0
        self.has_press = False

    def press(self, key):
        if key not in self.values:
            self.values[key] = Value('i', 0)
        self.values[key].value = 1
        self.has_press = True

    @property
    def button_presses(self):
        for key, value in self.values.items():
            if value.value:
                yield key


class Pad(object):
    def __init__(self):
        self.x = Value('f', 0.0)
        self.y = Value('f', 0.0)
        self._buttons = Buttons()
        self.p = Process(target=watch_gp, args=(self.x, self.y, self._buttons))
        self.p.start()

    @property
    def has_press(self):
        return self._buttons.has_press

    @property
    def buttons(self):
        for b in self._buttons.button_presses:
            yield b
        self._buttons.reset()

if __name__ == '__main__':
    ev_types = ['Key']
    codes = []
    while 1:
        gp_events = get_gamepad()
        for event in gp_events:
            if not ev_types or event.ev_type in ev_types:
                if not codes or event.code in codes:
                    print(event.ev_type, event.code, event.state)


