import curses
from curses.textpad import Textbox
from screen_logic import get_middle_scr, place_symetrically, time_to_die, move_enemies, random_enemy_shot, check_endgame
from classes import *
from model_io import save_score
from time import sleep, time

def start_screen(stdscr):
    midy, midx = get_middle_scr(stdscr)
    stdscr.attron(colors()[0])
    stdscr.addstr(midy, 10, 'A long time ago in a galaxy far, far away....')
    stdscr.refresh()
    stdscr.attroff(colors()[0])
    # sleep(3)
    stdscr.attron(colors()[3])
    stdscr.addstr(midy, 10, 'Press LEFT/RIGHT arrows to move your fighter, SPACE to shot...')
    stdscr.refresh()
    stdscr.attroff(colors()[3])
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
    enemieswin = curses.newwin(y-12, x, 4, 0)
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
    stdscr.addstr(midy, 10, 'GAME OVER... to save your score press S, to quit ESC')
    stdscr.addstr(midy+1, 10, f'YOUR SCORE: {score}')
    stdscr.refresh()
    key = 0
    while key != 27 or key == 10:
        key = stdscr.getch()
        if key == 115 or key == 83:
            textwin = curses.newwin(1, 20, midy+2, 31)
            box = Textbox(textwin)
            stdscr.addstr(midy+2, 10, 'ENTER YOUR NICKNAME: ')
            stdscr.refresh()
            box.edit()
            nickname = box.gather()
            save_score(nickname, score)
            return


def play(stdscr):
    space_management = {}
    bullets = []
    score = 0
    enemies_speed = 3
    flag0, flag1, flag2 = False, False, False
    key = start_screen(stdscr)
    stdscr.nodelay(True)
    fighter= generate_spaceship(stdscr, space_management, bullets)
    generate_shilds(stdscr, 5, space_management)
    enemieswin, allenemies = generate_enemies(stdscr, space_management, bullets)
    flag_endgame = False
    flag_run_bullets = False
    flag_run_enemies = True
    flag_direction=False
    right=True
    start_time_bullet = time()
    start_time_enemies = time()
    while key!=27 and fighter.endurance() > 0 and flag_endgame==False:
        dict_enemies = list(allenemies.values())
        enemies = []
        for dict in dict_enemies:
            enemies.extend(list(dict.values()))
        if len(enemies) == 0:
            flag_endgame=True
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:
            fighter.move_right()
        elif key == curses.KEY_LEFT:
            fighter.move_right(False)
        elif key == 32: #space key
            fighter.shot(stdscr)
        if time() - start_time_bullet > 0.08:
            start_time_bullet = time()
            flag_run_bullets = True
        else:
            flag_run_bullets = False
        if time() - start_time_enemies > enemies_speed:
            start_time_enemies = time()
            flag_run_enemies = True
        else:
            flag_run_enemies = False
        if len(enemies) < 40 and not flag0:
            enemies_speed /= 2
            flag0 = True
        if len(enemies) < 20 and not flag1:
            enemies_speed /= 4
            flag1 = True
        if len(enemies) < 2 and not flag2:
            enemies_speed /= 10
            flag2 = True
        score = time_to_die(stdscr, bullets, score, flag_run_bullets)
        flag_direction, right = move_enemies(enemieswin, dict_enemies, flag_direction, right, flag_run_enemies)
        front_row = random_enemy_shot(stdscr, dict_enemies, 50) #last argument determine intense of shooting
        flag_endgame = check_endgame(front_row, flag_endgame)
        stdscr.addstr(0, 0, f"Score: {score}")
        stdscr.attron(colors()[0])
        stdscr.addstr(1, 0, f"Lifes: {fighter.endurance()}")
        stdscr.attroff(colors()[0])
        sleep(0.005)
        stdscr.refresh()
    endgame(stdscr, score)
