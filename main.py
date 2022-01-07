import curses
from game import play
from screen_logic import *


def main(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()

    select_menu = ['PLAY', 'LOAD OPTIONS', 'SCOREBOARD', 'HELP', 'EXIT']

    select_idx = menu(stdscr, select_menu)

    menu_idx = {0: play(stdscr), 1: load_options(), 2: scoreboard(), 3: help(), 4: ext()}

    menu_idx[select_idx]

def set_position(key, pos, len):
    if key == curses.KEY_UP and pos>0:
        return pos-1
    elif key == curses.KEY_DOWN and pos<len-1:
        return pos+1
    else:
        return pos


def menu(stdscr, select):

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)

    position_idx = 0

    key = None

    while key!=10:

        midy, midx = get_middle_scr(stdscr)

        stdscr.erase()

        for word in select:
            if position_idx == select.index(word):
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(midy-len(select)//2+select.index(word), midx-len(word)//2, word)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(midy-len(select)//2+select.index(word), midx-len(word)//2, word)

        stdscr.refresh()

        key = stdscr.getch()
        position_idx = set_position(key, position_idx, len(select))

    stdscr.erase()
    return position_idx

def scoreboard():
    pass

def help():
    pass

def ext():
    pass

def load_options():
    pass



curses.wrapper(main)
