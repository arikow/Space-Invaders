import curses
from screen_logic import get_middle_scr, move_obj_right, place_symetrically, time_to_die
from classes import *



def start_screen(stdscr):
    midy, midx = get_middle_scr(stdscr)
    stdscr.addstr(midy, 20, 'Press key to begin...')
    stdscr.refresh()
    key = stdscr.getch()
    stdscr.clear()
    return key


def generate_shilds(stdscr, amount, space_management, endurance=4):
    y, x = stdscr.getmaxyx()
    stdscr.refresh()
    shieldswin = curses.newwin(4, x, y-8, 0)
    placement = place_symetrically(0, x, amount, False, 7)
    shields = []
    for nr, cords in placement.items():
        shields.append(Shield(shieldswin, endurance, (cords)))
        shields[nr].draw()
        space_management.update(shields[nr].hitbox())
    shieldswin.refresh()
    return True


def generate_spaceship(stdscr):
    stdscr.refresh()
    y, x = stdscr.getmaxyx()
    body = '|o|'
    spaceshipwin = curses.newwin(1, x, y-2, 0)
    tiefighter = Spaceship(spaceshipwin, 3, body)
    y -= 1 + body.count('/n')
    tiefighter.draw((0, x//2-1))
    spaceshipwin.refresh()
    return tiefighter


def generate_enemies(stdscr, space_management):
    stdscr.refresh()
    y ,x = stdscr.getmaxyx()
    amount = y//3-2
    body = '<@>'
    enemies = []
    enemieswin = curses.newwin(y-12, x, 3, 0)
    placement = place_symetrically(0, x, amount, True, 1)
    for nr, cords in placement.items():
        enemies.append(Enemy(enemieswin, 1, body))
        enemies[nr].draw(cords)
        space_management.update(enemies[nr].hitbox())
    enemieswin.refresh()



def play(stdscr):
    space_management = {}
    key = start_screen(stdscr)
    stdscr.nodelay(True)
    tiefighter = generate_spaceship(stdscr)
    generate_shilds(stdscr, 5, space_management)
    generate_enemies(stdscr, space_management)
    i=0
    while key!=27:
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:
            tiefighter.move_right()
        elif key == curses.KEY_LEFT:
            tiefighter.move_right(False)
        elif key == 32: #space key
            tiefighter.shot(stdscr)
        i+=1
        i=i%100000
        time_to_die(stdscr, tiefighter._bullets, space_management, i)
        stdscr.refresh()