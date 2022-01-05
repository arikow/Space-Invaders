import curses
from interface import get_middle_scr
from classes import *
from screen_logic import *


def start_screen(stdscr):
    midy, midx = get_middle_scr(stdscr)

    stdscr.addstr(midy, 20, 'Press key to begin...')
    stdscr.refresh()
    key = stdscr.getch()
    return True

def generate_shilds(stdscr, amount):
    s = Shield(1, (10, 10), 4)
    s.draw(stdscr)
    stdscr.refresh()


def play(stdscr):

    start_screen(stdscr)
    generate_shilds(stdscr, 5)
    get = stdscr.getch()

