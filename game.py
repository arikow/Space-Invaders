import curses
from screen_logic import get_middle_scr, place_symetrically, time_to_die
from classes import *



def start_screen(stdscr):
    midy, midx = get_middle_scr(stdscr)
    stdscr.addstr(midy, 20, 'Press LEFT/RIGHT arrows to move your fighter...')
    stdscr.refresh()
    key = stdscr.getch()
    stdscr.clear()
    return key


def generate_shilds(stdscr, amount, space_management, endurance=4):
    y, x = stdscr.getmaxyx()
    stdscr.refresh()
    shieldswin = curses.newwin(4, x, y-8, 0)
    placement = place_symetrically(0, x, amount, xcentric=False, width=7)
    shields = []
    for nr, cords in placement.items():
        shields.append(Shield(shieldswin, space_management, endurance, (cords)))
        shields[nr].draw()
    shieldswin.refresh()
    return True


def generate_spaceship(stdscr, space_management):
    stdscr.refresh()
    y, x = stdscr.getmaxyx()
    body = '|o|'
    spaceshipwin = curses.newwin(1, x, y-2, 0)
    fighter = Spaceship(spaceshipwin, space_management, 3, body)
    y -= 1 + body.count('/n')
    fighter.draw((0, x//2-1))
    spaceshipwin.refresh()
    return fighter


def generate_enemies(stdscr, space_management):
    stdscr.refresh()
    y ,x = stdscr.getmaxyx()
    amount = x//3 - 10
    body = '<@>'
    enemies = []
    enemieswin = curses.newwin(y-12, x, 3, 0)
    for row in range(5):
        placement = place_symetrically(row, x-6, amount)
        for nr, cords in placement.items():
            enemies.append(Enemy(enemieswin, space_management, 1, body))
            enemies[nr].draw(cords)
    enemieswin.refresh()
    return enemies



def play(stdscr):
    space_management = {}
    key = start_screen(stdscr)
    stdscr.nodelay(True)
    fighter = generate_spaceship(stdscr, space_management)
    generate_shilds(stdscr, 5, space_management)
    enemeis = generate_enemies(stdscr, space_management)
    i=0
    while key!=27:
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:
            fighter.move_right()
        elif key == curses.KEY_LEFT:
            fighter.move_right(False)
        elif key == 32: #space key
            fighter.shot(stdscr, space_management)
        i+=1
        i=i%100000
        time_to_die(stdscr, fighter._bullets, i)
        stdscr.addstr(0, 0, "yikes scores")
        stdscr.refresh()