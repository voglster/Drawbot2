from drawbot_state import RawDrawBot, DrawBotConf
import math


class Config(object):
    def __init__(self):
        self.pulley_diameter = float(24.0)
        self.steps_per_rotation = 200 * 32
        self.motor_separation = float(443)
        self.y_offset = float(100)
        self.pen_up_angle = 43
        self.pen_down_angle = 18
        self.max_y = 5000


class DrawBot(object):
    def __init__(self, config=None):
        self.config = config or Config()
        rdbf = DrawBotConf()
        self.bot = RawDrawBot(rdbf)
        self.x = 0.0
        self.y = 0.0
        self.pen_state = "up"
        self.penUp()

    def penUp(self):
        if self.pen_state != "up":
            self.bot.change_servo_angle(self.config.pen_up_angle)
            self.bot.pause(100000)
            self.pen_state = "up"

    def penDown(self):
        if self.pen_state != "down":
            self.bot.change_servo_angle(self.config.pen_down_angle)
            self.bot.pause(100000)
            self.pen_state = "down"

    def home(self):
        self.goto(0, 0)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_home(self):
        self.set_position(0, 0)

    def bound_x(self, x):
        minx = (self.config.motor_separation-(self.config.pulley_diameter/2)-100)/-2
        maxx = minx * -1
        if x < minx:
            return minx
        if x > maxx:
            return maxx
        return x

    def bound_y(self, y):
        if y < 0:
            return 0
        if y > self.config.max_y:
            return self.config.max_y
        return y

    def goto(self, x, y):
        x = self.bound_x(x)
        y = self.bound_y(y)
        left_length, right_length = self.calculate_lengths()
        target_left_length, target_right_length = self.calculate_lengths(x, y)
        left_length_change = target_left_length - left_length
        right_length_change = target_right_length - right_length
        self.bot.change_position(left_length_change, right_length_change)
        self.x = x
        self.y = y

    def jog(self, deltax, deltay):
        left_length_change = deltay + deltax
        right_length_change = deltay - deltax
        self.bot.change_position(left_length_change, right_length_change)

    def move(self, x, y):
        self.goto(self.x+x, self.y+y)

    def calculate_lengths(self, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        y_square = (self.config.y_offset + y) ** 2
        ll_x_square = (self.config.motor_separation/2.0 + x) ** 2
        rl_x_square = (self.config.motor_separation/2.0 - x) ** 2
        left_length = math.sqrt(y_square + ll_x_square)
        right_length = math.sqrt(y_square + rl_x_square)
        left_steps = self.convert_to_steps(left_length)
        right_steps = self.convert_to_steps(right_length)
        return left_steps, right_steps

    def set_feed_rate(self, fr):
        self.bot.set_feed_rate(fr)

    def adjust_feed_rate(self, fr_delta):
        self.bot.set_feed_rate(self.bot.feed_rate + fr_delta)

    @property
    def ready(self):
        return self.bot.ready

    @property
    def feed_rate(self):
        return self.bot.feed_rate

    def convert_to_steps(self, mm):
        c = math.pi * self.config.pulley_diameter
        mm_per_step = c / self.config.steps_per_rotation
        return int(round(mm / mm_per_step))



