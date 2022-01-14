import curses, time
from screen_logic import draw_object, move_obj_right


def colors():
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_WHITE, -1)
    return [curses.color_pair(i) for i in range(2,5)]


class PhysicalObject:
    def __init__(self, scr, endurance=1, body=''):
        self._hitbox = {}
        self._mock_hitbox = {}
        self._body = body
        self._mock_screen = scr
        self._endurance = endurance

    def hitbox(self):
        return self._hitbox

    def keys_hitbox(self):
        return list(self.hitbox().keys())

    def vals_hitbox(self):
        return list(self.hitbox().values())

    def mock_hitbox(self):
        return self._mock_hitbox

    def keys_mock_hitbox(self):
        return list(self.mock_hitbox().keys())

    def vals_mock_hitbox(self):
        return list(self.mock_hitbox().values())

    def endurance(self):
        return self._endurance

    def scr(self):
        return self._mock_screen

    def body(self):
        return self._body

    def update_true_hitbox(self):
        hitbox = {}
        move_y, move_x = self.scr().getbegyx()
        for key, value in self.mock_hitbox().items():
            y, x = key
            y += move_y
            x += move_x
            hitbox[(y, x)] = value
        self._hitbox = hitbox


class Shield(PhysicalObject):
    def __init__(self, scr, endurance, cordinates, color=None):
        super().__init__(scr, endurance)
        self._cordinates = cordinates
        if color == None:
            self.color = colors()[0]
        else:
            self.color = color
        self.create_body()

    def __eq__(self, other):
        return ('Shield', self.cordinates(), self.endurance()) == other

    def cordinates(self):
        return self._cordinates

    def create_body(self):
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
        self._body = body

    def draw(self):
        self._mock_hitbox = draw_object(self.scr(), self, self._cordinates, self.color)
        self.update_true_hitbox()



class Spaceship(PhysicalObject):
    def __init__(self, scr, lifes, body):
        super().__init__(scr, lifes, body)
        self._bullets = []
        self.color = colors()[1]

    def bullets(self):
        return self._bullets

    def draw(self, cordinates):
        self._mock_hitbox = draw_object(self.scr(), self, cordinates, self.color, True)
        self.update_true_hitbox()
        return True

    def move_right(self, direction=True):
        move_obj_right(self, direction)

    def shot(self, scr):
        y, x = self.keys_hitbox()[1]
        self._bullets.append(Bullet(scr, (y-1, x)))


class Enemy(Spaceship):
    pass

class Bullet(PhysicalObject):
    def __init__(self, scr, cordinates, endurance=1, body='|'):
        super().__init__(scr, endurance, body)
        self._hitbox = {cordinates: (self, body)}
        self.puff()

    def puff(self):
        self.scr().addstr(*self.keys_hitbox()[0], '|')

    def tick(self, cord, distance):
        val = self._hitbox[cord]
        self._hitbox.pop(cord)
        y, x = cord
        y -= distance
        self._hitbox[(y ,x)] = val
