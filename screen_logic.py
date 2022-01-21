import curses


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


# def clear_object(stdscr, body, cordinates):
#     body
#     body_ls = body.splitlines(True)
#     i = 0
#     y, x = cordinates
#     for line in body_ls:
#         line = len(line)*' '
#         stdscr.addstr(y+i, x, line)
#         i += 1
#     return True


def move_obj_yx(obj, down=None, right=None, distance=1):
    y, x = obj.keys_mock_hitbox()[1]

    obj.scr().clear()
    if down==True:
        y += distance
    elif down==False:
        y -= distance

    if right==True:
        x += distance
    elif right==False:
        x -= distance

    obj.draw((y,x))


def time_to_die(scr, bullets, i, distance=1):
    if i == 0:
        for bullet in bullets:
            y, x = bullet.keys_hitbox()[0]
            body = bullet.vals_hitbox()[0][1]
            if y<=0:
                bullets.remove(bullet)
            elif (y, x) in list(bullet.space_management().keys()):
                bullets.remove(bullet)
                bullet.new_assigment_sm(delate={(y, x): None})
            else:
                scr.addstr(y-1, x, body)
                bullet.tick((y, x), distance)
            scr.addstr(y, x, ' ')
            scr.refresh()


