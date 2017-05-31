from multiprocessing import freeze_support
from time import sleep
from drawing import Square, Point
import math


def draw(drawing):
    bot.penUp()
    first = True
    for point in drawing.path():
        bot.goto(point.x, point.y)
        if first:
            bot.penDown()
            first = False


def control_mode(bot):
    jogger = True
    print("Jogging mode is {}".format(jogger))
    bot.penUp()
    is_pen_up = True
    while 1:
        if pad.x.value or pad.y.value:
            if jogger:
                bot.jog(int(pad.x.value * 100), int(pad.y.value * 100))
            else:
                bot.move(int(pad.x.value * 10), int(pad.y.value * 10))

        for button_name in pad.buttons:
            if button_name == 'BTN_SOUTH':
                break
            if button_name == 'BTN_EAST':
                jogger = not jogger
                print("Jogging mode is {}".format(jogger))
                if not jogger:
                    bot.set_position(0, 0)
                    print("Home position set")
            if button_name == 'BTN_WEST':
                bot.goto(0, 0)
                print("Going home")
            if button_name == 'BTN_NORTH':
                if is_pen_up:
                    bot.penDown()
                else:
                    bot.penUp()
                is_pen_up = not is_pen_up
            if button_name == 'BTN_TR':
                bot.adjust_feed_rate(100)
                print("Adjusting speed up to {}".format(bot.feed_rate))
            if button_name == 'BTN_TL':
                bot.adjust_feed_rate(-100)
                print("Adjusting speed down to {}".format(bot.feed_rate))
        else:
            sleep(0.1)
            continue
        break


if __name__ == '__main__':
    freeze_support()
    from input import Pad
    pad = Pad()
    from drawbot import DrawBot
    bot = DrawBot()

    control_mode(bot)

    center = Point(bot.x, bot.y)
    for i in range(0, 90):
        draw(Square(center, 100-i, i*2))
    bot.penUp()
    bot.goto(0, 0)


