import curses


def get_middle_scr(stdscr):
    my, mx = stdscr.getmaxyx()
    return my//2, mx//2

def frac_dist_from_border(stdscr, frac_up, frac_left):
    my, mx = stdscr.getmaxyx()
    return int(my*frac_up), int(mx*frac_left)

def draw_object(stdscr, body, cordinates, color):
    hitbox = []
    body_ls = body.splitlines(True)
    y, x = cordinates
    const_x = x
    length = [len(line) for line in body_ls]
    x -= max(length)//2
    i = 0
    stdscr.attron(color)
    for line in body_ls:
        stdscr.addstr(y+i, x, line)
        hitbox.extend([(y+i, x_cord) for x_cord in range(const_x, const_x+len(line))])
        i += 1
    stdscr.attroff(color)
    return hitbox


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


def move_obj_right(stdscr, obj, direction=True, distance=1):
    y, x = obj.hitbox()[0]

    clear_object(stdscr, obj._spaceship_body, (y, x))

    if direction:
        x += distance
    else:
        x -= distance
    # if obj.isinstance(obj, Spaceship):
    #     obj.draw_spaceship(stdscr, (y, x), color)
    obj.draw_spaceship(stdscr, (y,x))