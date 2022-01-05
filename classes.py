from math import ceil

class MovingObject():
    pass

class Shield():
    def __init__(self, x, cordinates, endurance=4, direction=False):
        self._cordinates = cordinates
        self._endurance = endurance

    def cordinates(self):
        return self._cordinates


    def draw(self, stdscr):
        line='###'
        strong_line = '@@@'
        
        lvl = 0
        endu = self._endurance
        double_life = self._endurance - 4
        while lvl<endu:
            if double_life>0:
                f_line, f_char = strong_line, '@'
                double_life -= 1
                endu -= 1
            else:
                f_line, f_char = line, '#'
            if lvl<3:
                help_lvl = lvl
                formated_line = (2-lvl)*' ' + f_line + 2*lvl*f_char + '\n'
            else:
                formated_line = (2-help_lvl)*' ' + f_line + 2*help_lvl*f_char + '\n'
            body += formated_line
            lvl+=1
        return stdscr.addstr(*self.cordinates(), body)
