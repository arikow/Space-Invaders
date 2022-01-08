import curses, time
from screen_logic import bullet_move_up, draw_object


def colors():
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_WHITE, -1)
    return [curses.color_pair(i) for i in range(2,5)]


class Shield():
    def __init__(self, cordinates, endurance, direction=False):
        self._cordinates = cordinates
        self._endurance = endurance
        self._hitbox = []
        self._mock_hitbox = []
        self.color = colors()[0]

    def cordinates(self):
        return self._cordinates

    def hitbox(self):
        return self._hitbox

    def mock_hitbox(self):
        return self._mock_hitbox

    def draw_shield(self, stdscr):

        line = '###'
        strong_line = '@@@'
        body = ''
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
            body += formated_line
            lvl += 1
        self._hitbox = draw_object(stdscr, body, self._cordinates, self.color)



class Spaceship:
    def __init__(self, lifes, spaceship_body):
        self._lifes = lifes
        self._spaceship_body = spaceship_body
        self._hitbox = []
        self._mock_hitbox = []
        self.color = colors()[1]

    def hitbox(self):
        return self._hitbox

    def mock_hitbox(self):
        return self._mock_hitbox


    def draw_spaceship(self, scr, cordinates):
        y, x = cordinates
        self._mock_hitbox = draw_object(scr, self._spaceship_body, (y, x), self.color, True)
        hitbox = []
        move_y, move_x = scr.getbegyx()
        for t in self.mock_hitbox():
            y, x = t
            y += move_y
            x += move_x
            hitbox.append((y, x))
        self._hitbox = hitbox
        return True

    def shot(self, scr):
        y , x = self.hitbox()[1]
        y -= 1
        scr.addstr(y, x, '|')
        while y>0:
            y, x = bullet_move_up(scr, (y, x))
        scr.addstr(y, x, ' ')


    def __str__(self):
        return self._spaceship_draw

