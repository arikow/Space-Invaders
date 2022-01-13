import curses


def get_middle_scr(stdscr):
    my, mx = stdscr.getmaxyx()
    return my//2, mx//2

def place_symetrically(y, x, amount, centric=True, width=1, heigth=0) -> dict:
    placement = {}
    x += width
    rest_x = x%(amount+1)
    x -= rest_x
    y -= heigth
    y //= 2
    y -= heigth//2
    interval = x/(amount+1)
    if centric == False:
        x = interval+rest_x//2-2*width//2
    else:
        x = interval+rest_x//2-width//2
    placement[0] = (y, int(x))
    for i in range(1, amount):
        x += interval
        placement[i] = (y, int(x))
    return placement

def draw_object(scr, body, cordinates, color, center=False):
    mock_hitbox = []
    if body[-1] == '\n':
        body = body[:-1]
    body_ls = body.splitlines(True)
    y, x = cordinates
    length = [len(line) for line in body_ls]
    if center==True:
        x -= max(length)//2
    i = 0
    scr.attron(color)
    for line in body_ls:
        scr.addstr(y+i, x, line)
        ls = []
        for new_x in range(x, x+len(line)):
            if line[new_x-x] != ' ':
                ls.append([(y+i, new_x), line[new_x-x]])
        mock_hitbox.extend(ls)
        i += 1
    scr.attroff(color)
    scr.refresh()
    return mock_hitbox


def clear_object(stdscr, body, cordinates):
    body
    body_ls = body.splitlines(True)
    i = 0
    y, x = cordinates
    for line in body_ls:
        line = len(line)*' '
        stdscr.addstr(y+i, x, line)
        i += 1
    return True


def move_obj_right(obj, direction=True, distance=1):
    y, x = obj.mock_hitbox()[1][0]

    obj.scr().clear()

    if direction:
        x += distance
    else:
        x -= distance
    obj.scr().addstr((str(type(obj))))
    obj.draw((y,x))


def bullet_move_up(scr, cord, body='|', direction=True, distance=1):
    y, x = cord
    scr.addstr(y, x, ' ')
    scr.addstr(y-1, x, body)
    scr.refresh()
    return y-1, x

