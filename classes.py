import curses
from screen_logic import *

class MovingObject():
    pass


class Shield():
    def __init__(self, cordinates, endurance=4, direction=False):
        self._cordinates = cordinates
        self._endurance = endurance


    def cordinates(self):
        return self._cordinates

    def draw_shield(self, stdscr, color):


        line = '###'
        strong_line = '@@@'
        body = []
        lvl = 0
        endu = self._endurance
        double_life = self._endurance - 4
        while lvl < endu:
            if double_life > 0:
                f_line, f_char = strong_line, '@'
                double_life -= 1
                endu -= 1
            else:
                f_line, f_char = line, '#'
            if lvl < 3:
                help_lvl = lvl
                formated_line = (2-lvl)*' ' + f_line + 2*lvl*f_char + '\n'
            else:
                formated_line = (2-help_lvl)*' ' + f_line + 2*help_lvl*f_char + '\n'
            body.append(formated_line)
            lvl += 1
        draw_lines(stdscr, body, self._cordinates, color)

class Spaceship:
    def __init__(self, lifes, spaceship_body):
        self._lifes = lifes
        self._spaceship_body = spaceship_body

    def draw_spaceship(self, stdscr, cordinates, color):
        body_list = self._spaceship_body.splitlines(True)
        y, x = cordinates
        y -= len(body_list)
        draw_lines(stdscr, body_list, (y, x), color)

    def __str__(self):
        return self._spaceship_draw

