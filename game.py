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
    y, x = stdscr.getmaxyx()
    shieldswin = curses.newwin(4, x, y-8, 0)
    frac_x = frac_dist_from_border(shieldswin, 0, frac_left)[1]
    const_x = frac_x
    frac_x -= 3 # correct to center
    shields = []
    for i in range(amount):
        shields.append(Shield((0, frac_x), endurance))
        shields[i].draw_shield(shieldswin)
        frac_x+=const_x
    shieldswin.refresh()
    return shieldswin


def generate_spaceship(stdscr):
    stdscr.refresh()
    y, x = stdscr.getmaxyx()
    body = '|-|'
    xwing = Spaceship(3, body)
    y -= 1 + body.count('/n')
    spaceshipwin = curses.newwin(1, x, y-1, 0)
    xwing.draw_spaceship(spaceshipwin, (0, x//2-1))

    return xwing, spaceshipwin


def play(stdscr):
    stdscr.refresh()
    start_screen(stdscr)
    xwing, spaceshipswin = generate_spaceship(stdscr)
    shieldswin = generate_shilds(stdscr, 5)
    while True:
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:
            move_obj_right(spaceshipswin, xwing)
        elif key == curses.KEY_LEFT:
            move_obj_right(spaceshipswin, xwing, False)
        elif key == 32: #space
            xwing.shot(stdscr)
        stdscr.refresh()