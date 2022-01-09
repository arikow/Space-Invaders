import curses, time
from screen_logic import bullet_move_up, draw_object, move_obj_right


def colors():
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_WHITE, -1)
    return [curses.color_pair(i) for i in range(2,5)]


class PhysicalObject:
    def __init__(self, scr, endurance=1):
        self._hitbox = []
        self._mock_hitbox = []
        self._mock_screen = scr
        self._endurance = endurance

    def hitbox(self):
        return self._hitbox

    def mock_hitbox(self):
        return self._mock_hitbox

    def endurance(self):
        return self._endurance

    def scr(self):
        return self._mock_screen

    def set_hitbox(self):
        hitbox = []
        move_y, move_x = self.scr().getbegyx()
        for t in self.mock_hitbox():
            y, x = t
            y += move_y
            x += move_x
            hitbox.append((y, x))
        self._hitbox = hitbox


class Shield(PhysicalObject):
    def __init__(self, scr, endurance, cordinates, direction=False):
        super().__init__(scr, endurance)
        self._cordinates = cordinates
        self.color = colors()[0]

    def cordinates(self):
        return self._cordinates

    def draw_shield(self):

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
        self._mock_hitbox = draw_object(self.scr(), body, self._cordinates, self.color)



class Spaceship(PhysicalObject):
    def __init__(self, scr, lifes, body):
        super().__init__(scr, lifes)
        self._body = body
        self.color = colors()[1]

    def draw_spaceship(self, cordinates):
        y, x = cordinates
        self._mock_hitbox = draw_object(self.scr(), self._body, (y, x), self.color, True)
        self.set_hitbox()
        return True

    def move_right(self, direction=True):
        move_obj_right(self, direction)


    def shot(self, scr):
        y , x = self.hitbox()[1]
        y -= 1
        scr.addstr(y, x, '|')
        while y>0:
            y, x = bullet_move_up(scr, (y, x))
        scr.addstr(y, x, ' ')


    def __str__(self):
        return self._spaceship_draw

