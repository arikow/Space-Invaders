import curses
from screen_logic import get_middle_scr, frac_dist_from_border, move_obj_right, place_symetrically
from classes import *



def start_screen(stdscr):
    midy, midx = get_middle_scr(stdscr)

    stdscr.addstr(midy, 20, 'Press key to begin...')
    stdscr.refresh()
    key = stdscr.getch()
    stdscr.clear()
    return True


def generate_shilds(stdscr, amount, endurance=4):
    y, x = stdscr.getmaxyx()
    shieldswin = curses.newwin(4, x, y-8, 0)
    placement = place_symetrically(0, x, amount, False, 7)
    shields = []
    for nr, cords in placement:
        shields.append(Shield(shieldswin, endurance, (cords)))
        shields[nr].draw()
    shieldswin.refresh()
    return shieldswin


def generate_spaceship(stdscr):
    stdscr.refresh()
    y, x = stdscr.getmaxyx()
    body = '|-|'
    spaceshipwin = curses.newwin(1, x, y-2, 0)
    xwing = Spaceship(spaceshipwin, 3, body)
    y -= 1 + body.count('/n')
    xwing.draw((0, x//2-1))

    return xwing, spaceshipwin


def play(stdscr):
    f = open('temp', 'w+b')
    stdscr.refresh()
    start_screen(stdscr)
    xwing, spaceshipswin = generate_spaceship(stdscr)
    shieldswin = generate_shilds(stdscr, 5)
    while True:
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:
            xwing.move_right()
        elif key == curses.KEY_LEFT:
            xwing.move_right(False)
        elif key == 32: #space key
            xwing.shot(stdscr)
            stdscr.putwin(f)
        stdscr.refresh()