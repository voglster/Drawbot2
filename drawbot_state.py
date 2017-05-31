import serial
from time import sleep


class DrawBotConf(object):
    def __init__(self):
        self.port = 5
        self.baud = 115200
        self.timeout = 1
        self.debug = True


def read_line(ser, state):
    line = ser.readline().decode("ascii").strip() or ""
    state.input(line)
    print(line)
    return line


def read_till_end(ser, state):
    while ser.inWaiting():
        read_line(ser, state)


class RawDrawBot(object):
    def __init__(self, conf=None):
        if not conf:
            conf = DrawBotConf()
        self.state = DrawBotState()
        self.serial = serial.Serial(conf.port, conf.baud, timeout=conf.timeout)
        sleep(3)
        read_till_end(self.serial, self.state)

    def change_position(self, left_motor_steps=0, right_motor_steps=0, feed_rate=None):
        while not self.state.ready:
            read_till_end(self.serial, self.state)
        self.state.sent_command()
        if feed_rate is None:
            g_code = "G0L{0}R{1}\r\n".format(left_motor_steps, right_motor_steps)
        else:
            g_code = "G0L{0}R{1}F{2}\r\n".format(left_motor_steps, right_motor_steps, feed_rate)

        self.serial.write(g_code.encode())

    def set_feed_rate(self, feed_rate):
        g_code = "G0F{0}\r\n".format(feed_rate)
        self.serial.write(g_code.encode())

    def change_servo_angle(self, angle):
        while not self.state.ready:
            read_till_end(self.serial, self.state)
        self.state.sent_command()
        g_code = "M1A{0}\r\n".format(angle)
        self.serial.write(g_code.encode())

    @property
    def ready(self):
        return self.state.ready

    @property
    def feed_rate(self):
        return self.state.feed_rate


def parse_feed_rate(line):
    line = str(line)
    lines = line.split(":")
    feed_rate = int(lines[1])
    return feed_rate


class DrawBotState(object):
    def __init__(self):
        self.ready = False
        self.feed_rate = -1

    def input(self, line):
        if line == ">":
            self.ready = True
        if "feedrate:" in line:
            self.feed_rate = parse_feed_rate(line)

    def sent_command(self):
        self.ready = False
