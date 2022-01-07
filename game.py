import curses
from screen_logic import get_middle_scr, frac_dist_from_border, move_obj_right
from classes import *



def start_screen(stdscr):
    midy, midx = get_middle_scr(stdscr)

    stdscr.addstr(midy, 20, 'Press key to begin...')
    stdscr.refresh()
    key = stdscr.getch()
    stdscr.clear()
    return True


def generate_shilds(stdscr, amount, endurance=4):
    frac_left = 1/(amount+1)
    const_y, const_x = frac_dist_from_border(stdscr, 0.8, frac_left)
    x = const_x
    shields = []
    for i in range(amount):
        shields.append(Shield((const_y, x), 6))
        shields[i].draw_shield(stdscr)
        x+=const_x
    stdscr.refresh()

def generate_spaceship(stdscr):
    body = ' /^\\'
    xwing = Spaceship(3, body)
    y, x = stdscr.getmaxyx()
    y -= 1 + body.count('/n')
    x//=2
    xwing.draw_spaceship(stdscr, (y, x))
    return xwing


def play(stdscr):

    start_screen(stdscr)
    xwing = generate_spaceship(stdscr)
    generate_shilds(stdscr, 8)
    get = stdscr.getch()
    for i in range(5):
        move_obj_right(stdscr, xwing)
        stdscr.getch()