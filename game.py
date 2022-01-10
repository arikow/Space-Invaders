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
    frac_x -= 3 # correct to center, not needed
    shields = []
    for i in range(amount):
        shields.append(Shield(shieldswin, endurance, (0, frac_x)))
        shields[i].draw_shield()
        frac_x+=const_x
    shieldswin.refresh()
    return shieldswin


def generate_spaceship(stdscr):
    stdscr.refresh()
    y, x = stdscr.getmaxyx()
    body = '|-|'
    spaceshipwin = curses.newwin(1, x, y-2, 0)
    xwing = Spaceship(spaceshipwin, 3, body)
    y -= 1 + body.count('/n')
    xwing.draw_spaceship((0, x//2-1))

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