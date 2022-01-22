import random

def get_middle_scr(stdscr):
    my, mx = stdscr.getmaxyx()
    return my//2, mx//2

def place_symetrically(y, x, amount, ycentric=False, xcentric=True, width=1, heigth=0) -> dict:
    placement = {}
    x += width
    rest_x = x%(amount+1)
    x -= rest_x
    if ycentric==True:
        y -= heigth
        y //= 2
        y -= heigth//2
    interval = x/(amount+1)
    if xcentric == False:
        x = interval+rest_x//2-2*width//2
    else:
        x = interval+rest_x//2-width//2
    placement[0] = (y, int(x))
    for i in range(1, amount):
        x += interval
        placement[i] = (y, int(x))
    return placement

def draw_object(scr, obj, cordinates, color, center=False):
    body = obj.body()
    mock_hitbox = {}
    if body[-1] == '\n':
        body = body[:-1]
    body_ls = body.splitlines()
    y, x = cordinates
    length = [len(line) for line in body_ls]
    if center==True:
        x -= max(length)//2
    i = 0
    scr.attron(color)
    for line in body_ls:
        scr.addstr(y+i, x, line)
        for index, char in enumerate(line):
            if char != ' ':
                mock_hitbox[(y+i, x+index)] = (obj, char)
        i += 1
    scr.attroff(color)
    scr.refresh()
    return mock_hitbox


def objclear(obj):
    body = obj.body()
    y, x = obj.keys_mock_hitbox()[0]
    body_ls = body.splitlines()
    i = 0
    for line in body_ls:
        line = len(line)*' '
        obj.scr().addstr(y+i, x, line)
        i += 1
    return True


def move_obj_yx(obj, down=None, right=None, distance=1):
    index = len(obj.keys_mock_hitbox())//2
    y, x = obj.keys_mock_hitbox()[index]
    if down==True:
        y += distance
    elif down==False:
        y -= distance

    if right==True:
        x += distance
    elif right==False:
        x -= distance

    obj.draw((y,x))


def time_to_die(scr, bullets, score, running, distance=1): #function which move bullets
    if running == 0:
        for bullet in bullets:
            sm = bullet.space_management()
            y, x = bullet.keys_hitbox()[0]
            body = bullet.vals_hitbox()[0][1]
            scr.addstr(y, x, ' ')
            if y<=0 or y>=scr.getmaxyx()[0]-1:
                bullets.remove(bullet)
            elif (y, x) in sm.keys():
                obj = sm[(y, x)][0]
                if bullet.direction() and obj.body() == '@':
                    score += 1
                elif not bullet.direction() and obj.body() == '|o|':
                    obj.take_damage()
                obj.remove()
                bullets.remove(bullet)
                bullet.new_assigment_sm(delate={(y, x): None})
            else:
                if bullet.direction():
                    move = -1
                else:
                    move = 1
                scr.addstr(y+move, x, body)
                bullet.tick((y, x), distance)
            scr.refresh()
    return score

def move_enemies(scr, allenemies, flag, right, i):
    if i == 0:
        y, x = scr.getmaxyx()
        last_x = 0
        first_x = x
        enemies = []

        for column in allenemies:
            for enemy in column.values():
                x0 = enemy.keys_mock_hitbox()[0][1]
                x1 = enemy.keys_mock_hitbox()[-1][1]
                enemies.append(enemy)
                if first_x > x0:
                    first_x = x0
                if last_x < x1:
                    last_x = x1

        enemies.reverse()

        if flag==False:
            for enemy in enemies:
                if last_x>=x-1:
                    objclear(enemy)
                    move_obj_yx(enemy, down=True)
                    right=False
                    flag=True
                elif first_x<=1:
                    objclear(enemy)
                    move_obj_yx(enemy, down=True)
                    right=True
                    flag=True
                else:
                    objclear(enemy)
                    move_obj_yx(enemy, right=right)
        elif flag==True:
            for enemy in enemies:
                objclear(enemy)
                move_obj_yx(enemy, right=right)
                flag=False
    return flag, right


def random_enemy_shot(scr, columns, intense):
    intense *= 10
    front_row = []
    for column in columns:
        if column:
            max_row = max(column.keys())
            front_row.append(column[max_row])
    if random.randint(0, 100000000) < intense:
        enemy = random.choice(front_row)
        enemy.shot(scr, direction=False)