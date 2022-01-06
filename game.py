import curses
from screen_logic import *
from classes import *
from screen_logic import *


def start_screen(stdscr):
    midy, midx = get_middle_scr(stdscr)

    stdscr.addstr(midy, 20, 'Press key to begin...')
    stdscr.refresh()
    key = stdscr.getch()
    return True

def generate_shilds(stdscr, amount, endurance=4):
    frac_left = 1/(amount+1)
    const_y, const_x = frac_dist_from_border(stdscr, 0.8, frac_left)
    x = const_x-3
    shields = []
    for i in range(amount):
        shields.append(Shield((const_y, x), 6))
        shields[i].draw(stdscr)
        x+=const_x
    stdscr.refresh()


def play(stdscr):

    start_screen(stdscr)
    generate_shilds(stdscr, 10)
    get = stdscr.getch()

