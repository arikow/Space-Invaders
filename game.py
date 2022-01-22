import curses
from screen_logic import get_middle_scr, place_symetrically, time_to_die, move_enemies, random_enemy_shot
from classes import *
import time


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


def generate_spaceship(stdscr, space_management, bullets):
    stdscr.refresh()
    y, x = stdscr.getmaxyx()
    body = '|o|'
    spaceshipwin = curses.newwin(1, x, y-2, 0)
    fighter = Spaceship(spaceshipwin, space_management, 3, body, bullets)
    y -= 1 + body.count('/n')
    fighter.draw((0, x//2-1))
    spaceshipwin.refresh()
    return fighter


def generate_enemies(stdscr, space_management, bullets):
    stdscr.refresh()
    y ,x = stdscr.getmaxyx()
    amount = x//3 - 10
    body = '@'
    allenemies = {}
    for i in range(amount):
        allenemies[i] = {}
    enemieswin = curses.newwin(y-12, x, 3, 0)
    for row in range(5):
        placement = place_symetrically(row, x-6, amount)
        row_emy = []
        for nr, cords in placement.items():
            row_emy.append(Enemy(enemieswin, space_management, 1, body, allenemies, row, nr, bullets))
            row_emy[nr].draw(cords)
    enemieswin.refresh()
    return enemieswin, allenemies

def endgame(stdscr, score):
    stdscr.clear()
    midy, midx = get_middle_scr(stdscr)
    stdscr.addstr(midy, 20, 'GAME OVER... to save your score press S, to quit Q/ESC')
    stdscr.addstr(midy+1, 20, f'YOUR SCORE: {score}')
    stdscr.refresh()
    time.sleep(3)
    key = 0
    while key != 27 or 10:
        key = stdscr.getch()



def play(stdscr):
    space_management = {}
    bullets = []
    score = 0
    key = start_screen(stdscr)
    stdscr.nodelay(True)
    fighter = generate_spaceship(stdscr, space_management, bullets)
    generate_shilds(stdscr, 5, space_management)
    enemieswin, allenemies= generate_enemies(stdscr, space_management, bullets)
    i=0
    flag=False
    right=True
    while key!=27 and fighter.endurance() > 0:
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:
            fighter.move_right()
        elif key == curses.KEY_LEFT:
            fighter.move_right(False)
        elif key == 32: #space key
            fighter.shot(stdscr)
        i+=1
        i=i%500000
        score = time_to_die(stdscr, bullets, score, i%10000)
        flag, right=move_enemies(enemieswin, list(allenemies.values()), flag, right, i)
        random_enemy_shot(stdscr, list(allenemies.values()), 1000)
        stdscr.addstr(0, 0, f"yikes score: {score}")
        stdscr.refresh()
    endgame(stdscr, score)